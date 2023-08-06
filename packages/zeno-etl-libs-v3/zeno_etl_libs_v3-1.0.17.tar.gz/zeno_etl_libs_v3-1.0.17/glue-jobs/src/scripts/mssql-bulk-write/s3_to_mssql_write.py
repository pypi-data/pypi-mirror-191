"""
Objective of this job is to write the data from S3 CSV file to MSSQL DB. This JOB can be called in
parallel to write faster. So cool.
"""
import argparse
import os
import sys

sys.path.append('../../../..')

from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.db.db import MSSql
from zeno_etl_libs.helper.email.email import Email

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False,
                    help="This is env(dev, stage, prod)")
parser.add_argument('-u', '--s3_uri', default='', type=str, required=False)
parser.add_argument('-tn', '--table_name', default="ob-transactions-test", type=str, required=False)
parser.add_argument('-db', '--database_name', default="ZenoInputs", type=str, required=False)
parser.add_argument('-et', '--email_to', default="NA", type=str, required=False)
parser.add_argument('-id', '--identifier', default="Batch --> 1", type=str, required=False)

args, unknown = parser.parse_known_args()
env = args.env
s3_uri = args.s3_uri
table_name = args.table_name
database_name = args.database_name
email_to = args.email_to
identifier = args.identifier

os.environ['env'] = env
logger = get_logger()

logger.info(f"ENV: {env}")
logger.info(f"s3_uri: {s3_uri}")
logger.info(f"table_name: {table_name}")
logger.info(f"database_name: {database_name}")
logger.info(f"identifier: {identifier}")

subject = ""
mail_body = ""

try:
    if s3_uri and s3_uri.startswith("s3://"):
        pass
    else:
        logger.error(f"s3_uri can not be empty: {s3_uri}")
        raise Exception("Invalid s3 uri.")

    s3 = S3()
    names = s3_uri.split("//")[-1].split("/")
    bucket_name = names[0]
    key = "/".join(names[1:])

    df = s3.read_df_from_s3_csv(bucket_name=bucket_name,object_key=key)
    df = df.fillna('')

    logger.info(f"data length: {len(df)}")

    mssql = MSSql(connect_via_tunnel=False, db='ZenoInputs', one_beat_type ='in')
    mssql_connection = mssql.open_connection()

    table_info = mssql.get_table_info(table_name=table_name)
    logger.info(f"table info: {table_info}")

    cursor = mssql_connection.cursor()

    sql_data = tuple(map(tuple, df.values))
    col_str = f"[{'], ['.join(table_info.columns)}]"
    val_place_holder_str = ('%s,' * len(table_info.columns))[:-1]

    query = f"""
        INSERT INTO 
            {database_name}.dbo.[{table_name}] 
            ({col_str}) 
        values 
            ({val_place_holder_str});"""

    logger.info(f"query: {query}")

    response = cursor.executemany(query, sql_data)
    logger.info(f"response: {response}")

    """ commit  and closing the connection  """
    mssql_connection.commit()
    cursor.close()
    mssql.close()
    logger.info(f"Write to the DB successful")
    mail_body = f'S3 URI: {s3_uri} and table: {table_name}, DB: {database_name}'
    subject = f"MSSQL[Table Insert Successful]: Job identifier: {identifier}",
except Exception as e:
    # logger.exception(e)
    subject = f"MSSQL[Table Insert Failed]: Job identifier: {identifier}",
    mail_body = f'S3 URI: {s3_uri} and table: {table_name}, DB: {database_name}, \n' \
                f'error: {e.__str__()}'
finally:
    """ sending the email notification to the user """
    if email_to and email_to != "NA":
        logger.info("Sending email...")
        email = Email()
        email.send_email_file(
            subject=subject,
            mail_body=mail_body,
            to_emails=email_to, file_uris=[], file_paths=[]
        )