# script to get conversion of waba campaigns
# author : neha.karekar@zeno.health

# SOP to be written here
"""
A) Upload cohort file in datalake folder waba_campaigns_cohort with campaign_name_yyyy_mm_dd
   column name : 'patient-id'	'phone'	'consumer-type'	'abv'	'case'	'sent on'	'name'
   upload only after cohort is sent

B) Upload karix file in datalale folder waba_campaigns_karix with campaign_name_yyyy_mm_dd_karix
   column name : 'Date & Time'	'PhoneNumber'	'Status'	'Failure Reason'	'EventCode'	'EventMessage'
   upload only next day cohort is sent
"""

# todo timestamp conversion

import os
import argparse
import datetime
from datetime import datetime, timedelta
import pandas as pd
from dateutil.tz import gettz

from zeno_etl_libs.db.db import Athena
from zeno_etl_libs.db.db import DB
from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.helper import helper
import numpy as np

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False)
args, unknown = parser.parse_known_args()
env = args.env
os.environ['env'] = env

# setting up Athena connection
Athena = Athena()

db = DB()
db.open_connection()
logger = get_logger()

rs_db = DB(read_only=False)
rs_db.open_connection()
s3 = S3()

# table info
schema = 'prod2-generico'
table_name = 'waba-campaign-conversion'
table_info = helper.get_table_info(db=rs_db, table_name=table_name, schema=schema)

last_year_date = datetime.now() - timedelta(365)
# cohorts data
cohort_query = """select * from waba_campaigns_cohort;"""
#
# # Reading data from Athena need to pass only query and connection name stored in above step
cohort = Athena.get_df(query=cohort_query)
cohort['phone'] = cohort['phone'].astype(float).apply(lambda x: '%.f' % x).values.tolist()
# print(cohort.to_string())
cohort.drop_duplicates().shape
cohort.head()

# karix data
karix_query = """select * from waba_campaigns_karix ;"""
# # Reading data from Athena need to pass only query and connection name stored in above step
karix = Athena.get_df(query=karix_query)
# phone scientific to normal format
karix['phonenumber'] = karix['phonenumber'].astype(float).apply(lambda x: '%.f' % x).values.tolist()
logger.info("cohort length is {}".format(len(cohort)))
logger.info("karix length is {}".format(len(karix)))
karix.head()

# process karix data
karix['ranking'] = karix['status'].map({'READ': 1, 'DELIVERED': 2, 'SENT': 3, 'FAILED': 4}).fillna(5)
karix = karix.sort_values(by=['ranking'])
karix = karix.groupby(['phonenumber'], as_index=False).first()
karix.rename(columns={'phonenumber': 'phone'}, inplace=True)
cohort['phone'] = cohort['phone'].astype(str)
# merge cohort and karix
cohort_status = pd.merge(cohort, karix, on=['phone', 'partition_0'], how='left')
logger.info("cohort_status length is {}".format(len(cohort_status)))
cohort_status = cohort_status[
    ['patient-id', 'phone', 'consumer-type', 'abv', 'status', 'case', 'sent on', 'partition_0']]
cohort_status.rename(columns={'partition_0': 'campaign_name', 'sent on': 'campaign_date'}, inplace=True)
cohort_status['campaign_date'] = pd.to_datetime(cohort_status['campaign_date'], format='%d-%m-%y').dt.date
cohort_status['campaign_date_3'] = cohort_status['campaign_date'] + timedelta(2)
cohort_status['campaign_date_7'] = cohort_status['campaign_date'] + timedelta(6)

min_date = cohort_status['campaign_date'].min()
max_date = cohort_status['campaign_date'].max() + timedelta(6)

patients = tuple(cohort_status["patient-id"].unique())
logger.info("cohort_status length is {}".format(len(cohort_status)))
cohort_status = cohort_status.drop_duplicates()
logger.info("cohort_status length is {}".format(len(cohort_status)))

# retention master to find conversion
ret_q = f"""select rm."patient-id","created-at","total-spend" from "prod2-generico"."retention-master" rm 
            where "patient-id" in {patients} 
            and date("created-at") between  '{min_date}' and  '{max_date}'
          """
ret = rs_db.get_df(ret_q)
ret['created-at'] = pd.to_datetime(ret['created-at'])
ret['total-spend'] = ret['total-spend'].astype(float)
cohort_status['status'] = np.where(cohort_status['status'].isna(), '0', cohort_status['status'])
cohort_status_ret = pd.merge(cohort_status, ret, on='patient-id', how='left')
cohort_status_ret["created-at"] = pd.to_datetime(cohort_status_ret["created-at"]).dt.date

cohort_status_ret['patient_1'] = np.where(cohort_status_ret["created-at"] == cohort_status_ret["campaign_date"], 1, 0)
cohort_status_ret['total_spend_1'] = np.where(cohort_status_ret["created-at"] == cohort_status_ret["campaign_date"],
                                              cohort_status_ret['total-spend'], 0)

cohort_status_ret['patient_3'] = np.where((cohort_status_ret["created-at"] >= cohort_status_ret["campaign_date"]) &
                                          (cohort_status_ret["created-at"] <= cohort_status_ret["campaign_date_3"])
                                          , 1, 0)
cohort_status_ret['total_spend_3'] = np.where((cohort_status_ret["created-at"] >= cohort_status_ret["campaign_date"]) &
                                              (cohort_status_ret["created-at"] <= cohort_status_ret["campaign_date_3"])
                                              , cohort_status_ret['total-spend'], 0)

cohort_status_ret['patient_7'] = np.where((cohort_status_ret["created-at"] >= cohort_status_ret["campaign_date"]) &
                                          (cohort_status_ret["created-at"] <= cohort_status_ret["campaign_date_7"])
                                          , 1, 0)
cohort_status_ret['total_spend_7'] = np.where((cohort_status_ret["created-at"] >= cohort_status_ret["campaign_date"]) &
                                              (cohort_status_ret["created-at"] <= cohort_status_ret["campaign_date_7"])
                                              , cohort_status_ret['total-spend'], 0)

cohort_status_ret = cohort_status_ret.groupby(['patient-id', 'phone', 'consumer-type', 'case',
                                               'abv', 'status', 'campaign_name', 'campaign_date', 'campaign_date_3',
                                               'campaign_date_7'],
                                              as_index=False).agg(
    {'patient_3': 'max', 'total_spend_3': 'sum', 'patient_1': 'max', 'total_spend_1': 'sum',
     'patient_7': 'max', 'total_spend_7': 'sum'})

data = cohort_status_ret.copy()
data.columns = [c.replace('_', '-') for c in data.columns]
data['updated-at'] = datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')

# To Avoid Duplication
truncate_query = f"""
          DELETE
          FROM
              "prod2-generico"."waba-campaign-conversion";
              """
logger.info(truncate_query)
rs_db.execute(truncate_query)
s3.write_df_to_db(df=data[table_info['column_name']],
                  table_name='waba-campaign-conversion',
                  db=rs_db, schema='prod2-generico')

# Closing the DB Connection
rs_db.close_connection()
