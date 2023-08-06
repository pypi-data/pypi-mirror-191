import os
import time
from io import BytesIO, StringIO

import boto3
import pandas as pd
import pg8000
import pymongo
import redshift_connector as rc
from sqlalchemy import create_engine

from zeno_etl_libs.config.common import Config


class Athena:
    def __init__(self):
        configobj = Config.get_instance()
        secrets = configobj.get_secrets()
        self.athena_connection = None
        self.db_secrets = secrets
        self.region = 'ap-south-1'
        self.aws_access_key_id = secrets['AWS_ACCESS_KEY_ID']
        self.aws_secret_access_key = secrets['AWS_SECRET_ACCESS_KEY_ID']
        self.bucket_name = 'aws-glue-temporary-921939243643-ap-south-1'
        self.s3_resource = boto3.resource('s3', self.region, aws_access_key_id=self.aws_access_key_id,
                                          aws_secret_access_key=self.aws_secret_access_key)
        self.s3_client = boto3.client('s3', self.region, aws_access_key_id=self.aws_access_key_id,
                                      aws_secret_access_key=self.aws_secret_access_key)
        self.athena_client = boto3.client(service_name='athena', region_name=self.region)

    def connection(self, query=None, schema_name=None):
        """
            This function creates an Athena connection based on the schema name
            input:
                schema_name: STRING (This variable connects with the specified database in Athena, default value: None)
            output:
                Athena Connection object
        """
        if schema_name:
            database = schema_name
        else:
            database = self.db_secrets['DATALAKE_DATABASE']
        response = self.athena_client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={'Database': database},
            ResultConfiguration={'OutputLocation': 's3://{}/athena/'.format(self.bucket_name)},
        )
        return response

        # s3_staging_dir = 's3://aws-glue-temporary-921939243643-ap-south-1/athena/'
        # if schema_name:
        #     conn_str = f"awsathena+rest://{self.db_secrets['AWS_ACCESS_KEY_ID']}:{self.db_secrets['AWS_SECRET_ACCESS_KEY_ID']}@athena.{self.db_secrets['AWS_REGION']}.amazonaws.com:443/{schema_name}?s3_staging_dir{s3_staging_dir}&work_group=primary"
        # else:
        #     schema_name = self.db_secrets['DATALAKE_DATABASE']
        #     conn_str = f"awsathena+rest://{self.db_secrets['AWS_ACCESS_KEY_ID']}:{self.db_secrets['AWS_SECRET_ACCESS_KEY_ID']}@athena.{self.db_secrets['AWS_REGION']}.amazonaws.com:443/{schema_name}?s3_staging_dir{s3_staging_dir}&work_group=primary"
        # # Create the SQLAlchemy connection. Note that you need to have pyathena installed for this.
        # engine = create_engine(
        #     conn_str.format(
        #         aws_access_key_id=self.db_secrets['AWS_ACCESS_KEY_ID'],
        #         aws_secret_access_key=self.db_secrets['AWS_SECRET_ACCESS_KEY_ID'],
        #         region_name=self.db_secrets['AWS_REGION'],
        #         schema_name=schema_name,
        #         s3_staging_dir=s3_staging_dir,
        #     )
        # )
        # athena_connection = engine.connect()
        # self.athena_connection = athena_connection
        # return athena_connection

    def validate_query(self, query_id):
        resp = ["FAILED", "SUCCEEDED", "CANCELLED"]
        response = self.athena_client.get_query_execution(QueryExecutionId=query_id)
        # wait until query finishes
        while response["QueryExecution"]["Status"]["State"] not in resp:
            response = self.athena_client.get_query_execution(QueryExecutionId=query_id)

        return response["QueryExecution"]["Status"]["State"]

    def get_df(self, query=None, schema_name=None):
        print('start query: {}\n'.format(query))
        qe = self.connection(query, schema_name)
        qstate = self.validate_query(qe["QueryExecutionId"])
        print('query state: {}\n'.format(qstate))

        file_name = "athena/{}.csv".format(qe["QueryExecutionId"])
        obj = self.s3_client.get_object(Bucket=self.bucket_name, Key=file_name)
        return pd.read_csv(obj['Body'])

    def ingest_df_to_datalake(self, df, table_name=None, index=False, is_mis=False, file_format='csv'):
        if file_format == 'parquet':
            file_name = self.db_secrets[
                            'DATALAKE_DATABASE'] + '/' + table_name + f"/LOAD{int(time.time() * 1000)}.parquet"
        else:
            file_name = self.db_secrets[
                            'DATALAKE_DATABASE'] + '/' + table_name + f"/LOAD{int(time.time() * 1000)}.csv"
        path = "/".join(os.getcwd().split("/")[:-2]) + "/tmp/"
        if not os.path.exists(path):
            os.mkdir(path, 0o777)
        if file_format == 'parquet':
            buffer = BytesIO()
            # df.to_parquet(parquet_buffer, index=index, engine='fastparquet')
            df.to_parquet(buffer, index=index, engine='auto')
            # df.to_csv(local_file_path_csv)
        else:
            buffer = StringIO()
            df.to_csv(buffer, index_label=False, index=index, header=True)
        if is_mis:
            bucket_name = 'prod-mis-datalake'
        else:
            bucket_name = 'zeno-data-lake'
        self.s3_resource.Object(bucket_name, file_name).put(Body=buffer.getvalue())
        s3_uri = f"s3://{bucket_name}/{file_name}"
        return s3_uri


class DB:
    def __init__(self, read_only=True):
        configobj = Config.get_instance()
        secrets = configobj.get_secrets()
        self.db_secrets = secrets
        self.cursor = None
        self.connection = None
        self.read_only = read_only

    def open_connection(self):
        """ :return DB cursor """
        """function returns the redshift connection or cursor"""
        if self.read_only:
            self.connection = rc.connect(
                host=self.db_secrets['REDSHIFT_HOST'],
                database=self.db_secrets['REDSHIFT_DB'],
                user=self.db_secrets['REDSHIFT_USER'],
                password=self.db_secrets['REDSHIFT_PASSWORD'],
                port=int(self.db_secrets['REDSHIFT_PORT']),
                ssl=bool(int(self.db_secrets['REDSHIFT_SSL']))
            )
        else:
            self.connection = rc.connect(
                host=self.db_secrets['REDSHIFT_WRITE_HOST'],
                database=self.db_secrets['REDSHIFT_WRITE_DB'],
                user=self.db_secrets['REDSHIFT_WRITE_USER'],
                password=self.db_secrets['REDSHIFT_WRITE_PASSWORD'],
                port=int(self.db_secrets['REDSHIFT_WRITE_PORT']),
                ssl=bool(int(self.db_secrets['REDSHIFT_WRITE_SSL']))
            )

        self.connection.autocommit = True
        cursor: rc.Cursor = self.connection.cursor()
        self.cursor = cursor
        return cursor

    def execute(self, query, params=None):
        """
        query: "select * from table where col = '%s' and col2 = '%s' "
        params: (x, y)
        """
        try:
            self.cursor.execute(query, params)
        except Exception as e:
            print(f"e: {e}")
            if not self.connection.autocommit:
                self.cursor.execute("rollback")
            raise Exception(e)

    def get_df(self, query) -> pd.DataFrame:
        self.execute(query, params=None)
        df: pd.DataFrame = self.cursor.fetch_dataframe()
        if isinstance(df, type(None)):
            return pd.DataFrame(
                columns=[desc[0].decode("utf-8") for desc in self.cursor.description])
        else:
            return df

    def close_connection(self):
        """ make sure to close the connection, after all the DB operation are over """
        print("Redshift DB connection closed successfully.")
        self.cursor.close()


class RedShiftDB(DB):
    pass


class RedShiftPG8000:
    def __init__(self):
        configobj = Config.get_instance()
        secrets = configobj.get_secrets()
        self.db_secrets = secrets
        self.cursor = None
        self.connection = None

    def open_connection(self):
        """ :return DB cursor """
        """function returns the redshift connection or cursor"""
        self.connection = pg8000.connect(
            host=self.db_secrets['REDSHIFT_HOST'],
            database=self.db_secrets['REDSHIFT_DB'],
            user=self.db_secrets['REDSHIFT_USER'],
            password=self.db_secrets['REDSHIFT_PASSWORD'],
            port=int(self.db_secrets['REDSHIFT_PORT'])
        )
        self.connection.autocommit = True
        cursor: rc.Cursor = self.connection.cursor()
        self.cursor = cursor
        return cursor

    def execute(self, query):
        """
        query: "select * from table where col = '%s' and col2 = '%s' "
        params: (x, y)
        """
        try:
            self.cursor.execute(query)
        except Exception as e:
            print(f"e: {e}")
            self.cursor.execute("rollback")
            # self.cursor.execute(query)
            # self.cursor.execute(query)
            raise Exception(e)

    def close_connection(self):
        """ make sure to close the connection, after all the DB operation are over """
        print("Redshift DB connection closed successfully.")
        self.cursor.close()


class RedShift:
    def __init__(self):
        configobj = Config.get_instance()
        secrets = configobj.get_secrets()
        self.db_secrets = secrets
        self.connection = None
        self.engine = None  # dispose the engine after user
        self.url = f"postgresql+psycopg2://{self.db_secrets['REDSHIFT_USER']}:{self.db_secrets['REDSHIFT_PASSWORD']}@" \
                   f"{self.db_secrets['REDSHIFT_HOST']}:{self.db_secrets['REDSHIFT_PORT']}/" \
                   f"{self.db_secrets['REDSHIFT_DB']}"

    def open_connection(self):
        """ :return DB cursor """
        """function returns the redshift connection or cursor"""
        self.engine = create_engine(self.url)
        self.connection = self.engine.connect()
        self.connection.autocommit = True
        return self.connection

    def execute(self, query):
        try:
            self.engine.execute(query)
        except Exception as e:
            print(f"e: {e}")
            self.engine.execute("rollback")
            raise Exception(e)

    def close_connection(self):
        """ make sure to close the connection, after all the DB operation are over """

        self.connection.close()
        self.engine.dispose()

        print("Redshift DB connection closed successfully.")


class MySQL:
    """ MySQL DB Connection """
    """ implementing singleton design pattern for DB Class """

    def __init__(self, read_only=True):
        configobj = Config.get_instance()
        secrets = configobj.get_secrets()
        self.db_secrets = secrets

        if read_only:
            self.user = self.db_secrets['MS_USER']
            self.password = self.db_secrets['MS_PASSWORD']
            self.host = self.db_secrets['MS_HOST']
            self.port = self.db_secrets['MS_PORT']
            self.db = self.db_secrets['MS_DB']
        else:
            self.user = self.db_secrets['MYSQL_WRITE_USER']
            self.password = self.db_secrets['MYSQL_WRITE_PASSWORD']
            self.host = self.db_secrets['MYSQL_WRITE_HOST']
            self.port = self.db_secrets['MYSQL_WRITE_PORT']
            self.db = self.db_secrets['MYSQL_WRITE_DATABASE']

        self.url = f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
        self.engine = None
        self.connection = None
        self.cursor = None

        # Not calling open_connection() function, to avoid DB connection at class instantiation
        # self.connection = self.open_connection()

    def open_connection(self):
        """
        :return: connection to mysql DB using pymysql lib
        """
        # self.connection = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db,
        #                                   port=int(self.port))
        self.engine = create_engine(self.url, connect_args={'connect_timeout': 3600})
        self.connection = self.engine.raw_connection()
        self.cursor = self.connection.cursor()
        return self.cursor

    def close(self):
        """
        closes the DB connection
        :return None
        """
        print("MySQL DB connection closed successfully!")
        self.connection.close()
        self.engine.dispose()


class PostGre:
    """ MySQL DB Connection """
    """ implementing singleton design pattern for DB Class """

    def __init__(self, is_internal=False):
        """
        @param is_internal: True means DB is owned by tech team, we want a connection with that
        """
        configobj = Config.get_instance()
        secrets = configobj.get_secrets()
        self.db_secrets = secrets
        if is_internal:
            self.user = self.db_secrets[f'INTERNAL_PG_USER']
            self.password = self.db_secrets['INTERNAL_PG_PASSWORD']
            self.host = self.db_secrets['INTERNAL_PG_HOST']
            self.port = self.db_secrets['INTERNAL_PG_PORT']
            self.db = self.db_secrets['INTERNAL_PG_DB']
        else:
            self.user = self.db_secrets['PG_USER']
            self.password = self.db_secrets['PG_PASSWORD']
            self.host = self.db_secrets['PG_HOST']
            self.port = self.db_secrets['PG_PORT']
            self.db = self.db_secrets['PG_DB']
        self.url = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
        self.connection = None
        self.cursor = None

    def open_connection(self):
        # import psycopg2
        # conn_string = f"dbname='{self.db}' port='{self.port}' user='{self.user}' password='{self.password}' " \
        #               f"host='{self.host}'"

        # self.connection = psycopg2.connect(conn_string)

        self.connection = pg8000.connect(
            database=self.db,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.cursor = self.connection.cursor()
        return self.connection

    def connection(self):
        """
        :return: connection to mysql DB using pymysql lib
        """

        return self.open_connection()

    def execute(self, query, params=None):
        """
        query: "select * from table where col = '%s' and col2 = '%s' "
        params: (x, y)
        """
        try:
            self.connection.execute(query, params)
        except Exception as e:
            print(f"e: {e}")
            self.connection.execute("rollback")

    def close(self):
        """
        closes the DB connection
        :return None
        """
        self.connection.close()
        print("PostGre DB connection closed successfully!")

    def close_connection(self):
        self.close()


class PostGreWrite:
    """ implementing singleton design pattern for DB Class """

    def __init__(self, is_internal=False):
        configobj = Config.get_instance()
        secrets = configobj.get_secrets()
        self.db_secrets = secrets

        if is_internal:
            self.user = self.db_secrets[f'INTERNAL_PG_USER']
            self.password = self.db_secrets['INTERNAL_PG_PASSWORD']
            self.host = self.db_secrets['INTERNAL_PG_HOST']
            self.port = self.db_secrets['INTERNAL_PG_PORT']
            self.db = self.db_secrets['INTERNAL_PG_DB']
        else:
            self.user = self.db_secrets['PG_USER']
            self.password = self.db_secrets['PG_PASSWORD']
            self.host = self.db_secrets['PG_HOST']
            self.port = self.db_secrets['PG_PORT']
            self.db = self.db_secrets['PG_DB']
        self.url = f"postgresql+pg8000://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
        # self.url = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
        self.engine = None
        self.connection = None
        self.cursor = None

    def open_connection(self):
        """
        :return: connection to mysql DB using pymysql lib
        """
        self.engine = create_engine(self.url)
        self.connection = self.engine.raw_connection()
        self.cursor = self.connection.cursor()
        return self.connection

    def close(self):
        """
        closes the DB connection
        :return None
        """
        print("PostGre DB connection closed successfully!")
        self.engine.dispose()

    def close_connection(self):
        self.close()


class RedshiftEngine:
    def __init__(self):
        configobj = Config.get_instance()
        secrets = configobj.get_secrets()
        self.db_secrets = secrets
        self.connection = None

    def open_connection(self):
        """ :return DB cursor """
        """function returns the redshift connection or cursor"""
        host = self.db_secrets['REDSHIFT_HOST']
        database = self.db_secrets['REDSHIFT_DB']
        user = self.db_secrets['REDSHIFT_USER']
        password = self.db_secrets['REDSHIFT_PASSWORD']
        port = int(self.db_secrets['REDSHIFT_PORT'])
        ssl = bool(int(self.db_secrets['REDSHIFT_SSL']))

        uri = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        self.connection = pg8000.connect(uri)

    def execute(self, query, params=None):
        """
        query: "select * from table where col = '%s' and col2 = '%s' "
        params: (x, y)
        """
        try:
            self.connection.execute(query, params)
        except Exception as e:
            print(f"e: {e}")
            self.connection.execute("rollback")

    def create_report_table_using_df(self, df, table_name, schema):
        try:
            df.head(5).to_sql(
                name=table_name,
                con=self.connection,
                index=False,
                if_exists='fail',
                schema=schema)
            query = f"""truncate table "{schema}"."{table_name}"; """
            self.connection.execute(query)
            print(f"Created table: {table_name}, successfully.")
        except Exception as e:
            print(f"Error creating table: {e}")

    def close_connection(self):
        """ make sure to close the connection, after all the DB operation are over """
        print("Redshift DB connection closed successfully.")
        self.connection.close()


class MongoDB:
    """ Mongo DB Connection """
    """ implementing singleton design pattern for DB Class """

    def __init__(self):
        configobj = Config.get_instance()
        secrets = configobj.get_secrets()
        self.db_secrets = secrets
        self.user = self.db_secrets['MONGO_USER']
        self.password = self.db_secrets['MONGO_PASSWORD']
        self.host = self.db_secrets['MONGO_HOST']
        self.port = self.db_secrets['MONGO_PORT']
        self.connection = None
        self.cursor = None

    def open_connection(self, auth_source):
        self.connection = pymongo.MongoClient(self.host, self.port, username=self.user,
                                              password=self.password,
                                              authSource=auth_source)

        return self.connection

    def connection(self, auth_source):
        return self.open_connection(auth_source)

    def close(self):
        """
        closes the DB connection
        :return None
        """
        self.connection.close()
        print("Mongo DB connection closed successfully!")

    def close_connection(self):
        self.close()


def download_private_key_from_s3():
    # s3 = boto3.resource('s3')
    # file = "id_rsa"
    # ssh_pkey_full_path = '/tmp/' + file
    # bucket_name = "aws-prod-glue-assets-921939243643-ap-south-1"
    # logger.info(f"bucket_name: {bucket_name}")
    # logger.info(f"ssh_pkey_full_path: {ssh_pkey_full_path}")
    # s3.Bucket(bucket_name).download_file("private/" + file, file)
    # logger.info(f"ssh_pkey_full_path downloaded successfully")
    # return ssh_pkey_full_path
    pass


class MSSql:
    """ MSSQL DB Connection """
    """ implementing singleton design pattern for DB Class """

    def __init__(self, connect_via_tunnel=True, db=None, one_beat_type=None):
        configobj = Config.get_instance()
        secrets = configobj.get_secrets()
        self.db_secrets = secrets
        if str(one_beat_type).lower() == 'in' :
            self.user = self.db_secrets['IN_OB_MSSQL_USER']
            self.password = self.db_secrets['IN_OB_MSSQL_PASSWORD']
            self.host = self.db_secrets['IN_OB_MSSQL_HOST']
            self.port = self.db_secrets['IN_OB_MSSQL_PORT']
            if db is None:
                self.db = self.db_secrets['IN_OB_MSSQL_DATABASE']
            else:
                self.db = db
            self.connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=" + self.host + ";DATABASE=" + \
                                     self.db + ";UID=" + self.user + ";PWD=" + self.password + ";TrustServerCertificate=yes"
        elif str(one_beat_type).lower() == 'out' :
            self.user = self.db_secrets['OUT_OB_MSSQL_USER']
            self.password = self.db_secrets['OUT_OB_MSSQL_PASSWORD']
            self.host = self.db_secrets['OUT_OB_MSSQL_HOST']
            self.port = self.db_secrets['OUT_OB_MSSQL_PORT']
            if db is None:
                self.db = self.db_secrets['OUT_OB_MSSQL_DATABASE']
            else:
                self.db = db
            self.connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=" + self.host + ";DATABASE=" + \
                                     self.db + ";UID=" + self.user + ";PWD=" + self.password + ";TrustServerCertificate=yes"
        else:
            self.user = self.db_secrets['WH_MSSQL_USER']
            self.password = self.db_secrets['WH_MSSQL_PASSWORD']
            self.host = self.db_secrets['WH_MSSQL_HOST']
            self.port = self.db_secrets['WH_MSSQL_PORT']
            if db is None:
                self.db = self.db_secrets['WH_MSSQL_DATABASE']
            else:
                self.db = db
            self.connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=" + self.host + ";DATABASE=" + \
                                     self.db + ";UID=" + self.user + ";PWD=" + self.password + ";TrustServerCertificate=yes"
        # self.url = f"mssql+pymssql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
        # TODO: switch on tunnel connect
        self.connect_via_tunnel = False
        self.connection = None
        self.cursor = None
        self.tunnel = None

    def __start_tunnel(self):
        from sshtunnel import SSHTunnelForwarder
        try:
            self.tunnel = SSHTunnelForwarder(
                ('workstation.generico.in', 22),
                ssh_username='glue',
                ssh_pkey=download_private_key_from_s3(),
                ssh_private_key_password='',
                remote_bind_address=('wh1.zeno.health', 1433)
            )
            # logger.info("Tunnel class ok")
            self.tunnel.start()
            # logger.info("Tunnel started")
        except Exception as error:
            raise Exception("MSSQL error while starting tunnel is: {}".format(error))

    def open_connection(self):
        try:
            if self.connect_via_tunnel:
                self.__start_tunnel()
            import pymssql
            self.connection = pymssql.connect(server=self.host, user=self.user,
                                              password=self.password, database=self.db, port=self.port)

            self.cursor = self.connection.cursor()
            return self.connection
        except Exception as error:
            raise Exception("MSSQL error while establishing connection is: {}".format(error))

    def connection(self):
        """
        :return: connection to mysql DB using pymysql lib
        """
        return self.open_connection()

    def get_table_info(self, table_name):
        table_info = pd.read_sql(
            f"SELECT TOP 0 * FROM {self.db}.dbo.[{table_name}];", self.connection)
        return table_info

    def close(self):
        """
        closes the DB connection
        :return None
        """
        self.connection.close()

        if self.connect_via_tunnel:
            self.tunnel.close()
        print("MSSQL DB connection closed successfully!")

    def close_connection(self):
        self.close()
