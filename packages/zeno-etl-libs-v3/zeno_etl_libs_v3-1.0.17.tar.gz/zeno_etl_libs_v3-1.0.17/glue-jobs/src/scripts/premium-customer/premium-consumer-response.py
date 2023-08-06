"""
# Author - shubham.gupta@zeno.health
# Purpose - script for reading G-sheet inputs (premium consumers), preprocessing and writing in redshift
"""

import argparse
import os
import sys
from datetime import datetime as dt
from datetime import timedelta
from dateutil.tz import gettz

import pandas as pd

sys.path.append('../../../..')

from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.db.db import DB
from zeno_etl_libs.helper import helper
from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper.google.sheet.sheet import GoogleSheet
from zeno_etl_libs.helper.email.email import Email

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False)

args, unknown = parser.parse_known_args()
env = args.env
os.environ['env'] = env

gs = GoogleSheet()
logger = get_logger()

# params
read_schema = 'prod2-generico'
table_name = 'premium-response-record'

rs_db = DB()
rs_db.open_connection()

s3 = S3(bucket_name='aws-glue-temporary-921939243643-ap-south-1')

table_info = helper.get_table_info(db=rs_db, table_name=table_name, schema=read_schema)
logger.info(table_info)
if isinstance(table_info, type(None)):
    logger.info(f"table: {table_name} do not exist")

run_date = dt.today().date() - timedelta(days=1)

# Read

file_path = s3.download_file_from_s3(file_name='Shubham_G/premium-response/Premium consumers (Responses) - Form Responses 1.csv')

response_data = pd.read_csv(file_path)

response_data['record-date'] = pd.to_datetime(response_data['Timestamp']).dt.date
response_data = response_data[response_data['record-date'] == run_date]

response_data['Please select the reason '] = response_data['Please select the reason '].fillna('').astype(str) + response_data['Unnamed: 7'].fillna('').astype(str)
response_data['call-connected-remark'] = response_data['Please select the reason '].str.strip()

response_data = response_data.drop(columns=['Unnamed: 5',
                                            'Unnamed: 7',
                                            'Please select the reason ',
                                            'How many months',
                                            'Comments'])

reminders = [col for col in response_data.columns if 'Reminder' in col.split(' ')]
response_data['reminder-date'] = response_data[reminders].apply(lambda x: ''.join(x.dropna().astype(str)), axis=1)
response_data.drop(columns=reminders, inplace=True)

follow_ups = [col for col in response_data.columns if 'Followup' in col.split(' ')]
response_data['followup-date'] = response_data[follow_ups].apply(lambda x: ''.join(x.dropna().astype(str)), axis=1)
response_data.drop(columns=follow_ups, inplace=True)

remarks = [col for col in response_data.columns if 'Remarks' in col.split('.')]

response_data['remarks'] = response_data[remarks].apply(lambda x: ''.join(x.dropna().astype(str)), axis=1)
response_data = response_data.drop(columns=remarks)

response_data.columns = ['-'.join(col.lower().strip().split(' ')) for col in response_data]

response_data['reminder-date'] = pd.to_datetime(response_data['reminder-date'], errors='coerce')
# etl
response_data['created-at'] = dt.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
response_data['created-by'] = 'etl-automation'
response_data['updated-at'] = dt.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
response_data['updated-by'] = 'etl-automation'


# truncate data if current month data already exist

if isinstance(table_info, type(None)):
    logger.info(f"table: {table_name} do not exist")
else:
    truncate_query = f"""
            DELETE
            FROM
                "{read_schema}"."{table_name}"
            WHERE
                "record-date" = '{run_date }';
                """
    logger.info(truncate_query)
    rs_db.execute(truncate_query)

# Write to db
s3.write_df_to_db(df=response_data[table_info['column_name']], table_name=table_name,
                  db=rs_db, schema=read_schema)

logger.info("Script ran successfully")

# closing connection
rs_db.close_connection()
