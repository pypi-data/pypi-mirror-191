"""
Objective: Write to MSSQL in parallel. This job breaks the input CSV file into smaller
parts(=batch_count), and calls another job which writes to MSSQL asynchronously.

How to Use:
1. Upload your Data/Frame to S3 CSV.
2. Call this job from your code.
```
from zeno_etl_libs.helper.aws.glue import Glue
glue = Glue()
arguments = {
        "--batch_count":5,
        "--s3_uri":<your_s3_uri>,
        "--table_name":<your_table_name>,
        "--database_name":<your_database_name>,
        "--email_to": <email_to> # After every batch upload get notification on this email
    }

    ''' trigger the glue job in parallel '''
    response = glue.start_job_run(job_name=f"{env_prefix}-194-mssql-bulk-write", arguments=arguments)

    logger.info(f"Job trigger response: {response}")
```
"""

import argparse
import os
import sys

sys.path.append('../../../..')

from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.helper.helper import batch
from zeno_etl_libs.helper.aws.glue import Glue

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False,
                    help="This is env(dev, stage, prod)")
parser.add_argument('-bc', '--batch_count', default=5, type=int, required=False)
parser.add_argument('-u', '--s3_uri',
                    default='',
                    type=str, required=False)
parser.add_argument('-tn', '--table_name', default="ob-transactions-test", type=str, required=False)
parser.add_argument('-db', '--database_name', default="ZenoInputs", type=str, required=False)
parser.add_argument('-et', '--email_to', default="NA", type=str, required=False)

args, unknown = parser.parse_known_args()
env = args.env
batch_count = args.batch_count
s3_uri = args.s3_uri
table_name = args.table_name
database_name = args.database_name
email_to = args.email_to

os.environ['env'] = env
logger = get_logger()

logger.info(f"batch_count: {batch_count}")
logger.info(f"s3_uri: {s3_uri}")
logger.info(f"table_name: {table_name}")
logger.info(f"database_name: {database_name}")

if s3_uri and s3_uri.startswith("s3://"):
    pass
else:
    logger.error(f"s3_uri can not be empty: {s3_uri}")
    raise Exception("Invalid s3 uri.")

s3 = S3()
glue = Glue()

names = s3_uri.split("//")[-1].split("/")
bucket_name = names[0]
key = "/".join(names[1:])
df = s3.read_df_from_s3_csv(bucket_name=bucket_name,object_key=key)

# """ temp """
# path = "/Users/kuldeep/"
# file_name = "ob_data.csv"
# df = pd.read_csv(path+file_name)
# uri = s3.save_df_to_s3(df=df)

env_prefix = "prod" if env == 'prod' else "stage"

batch_size = round(len(df)/batch_count)+1

batch_counter = 0
for s_df in batch(df, batch_size):
    logger.info(f"len: {len(s_df)}")

    """ uploading the smaller file to s3 """
    uri = s3.save_df_to_s3(df=s_df)
    batch_counter += 1
    arguments = {
        "--s3_uri":uri,
        "--table_name":table_name,
        "--database_name":database_name,
        "--email_to": email_to,
        "--identifier": f"Batch -> {batch_counter}"
    }

    """ trigger the glue job in parallel """
    response = glue.start_job_run(job_name=f"{env_prefix}-193-s3-to-mssql-write", arguments=arguments)

    logger.info(f"Job trigger response: {response}")