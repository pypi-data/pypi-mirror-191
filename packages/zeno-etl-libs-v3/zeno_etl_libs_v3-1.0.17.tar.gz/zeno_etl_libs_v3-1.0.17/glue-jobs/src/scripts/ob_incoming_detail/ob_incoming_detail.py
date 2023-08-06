# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 21:45:59 2022

@author: vivek.sidagam@zeno.health

@Purpose: To populate table purchase_margin
"""

import os
import sys
import argparse
import pandas as pd
import datetime
import numpy as np
import pymssql
import requests
import json

sys.path.append('../../../..')

from zeno_etl_libs.db.db import DB, MSSql
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper.email.email import Email
from dateutil.tz import gettz

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Populates table purchase_margin")
    parser.add_argument('-e', '--env', default="dev", type=str, required=False)
    # parser.add_argument('-et', '--email_to', default="vivek.sidagam@zeno.health,akshay.bhutada@zeno.health",
    #                     type=str, required=False)
    # parser.add_argument('-sd', '--start_date', default='NA', type=str, required=False)
    # parser.add_argument('-ed', '--end_date', default='NA', type=str, required=False)
    args, unknown = parser.parse_known_args()
    env = args.env
    os.environ['env'] = env
    # email_to = args.email_to
    # start_date = args.start_date
    # end_date = args.end_date

    err_msg = ''

    logger = get_logger()
    logger.info("Script begins")

    cur_date = datetime.datetime.now(tz=gettz('Asia/Kolkata')).date()

    d = datetime.timedelta(days=15)

    start_dt = cur_date - d

    end_dt = cur_date - datetime.timedelta(1)
    status = False

    # if start_date == 'NA' and end_date == 'NA':
    #     start_date = start_dt
    #     end_date = end_dt

    try:
        # MSSql connection
        mssql = MSSql(connect_via_tunnel=False, one_beat_type='out')
        mssql_connection = mssql.open_connection()

        sql_query = "SELECT TOP 200 id, drug_id, store_id, quantity FROM ob_incoming_detail WHERE status = 0 ORDER BY id DESC"

        df = pd.read_sql_query(sql_query, mssql_connection)
        df['drug_id']=df['drug_id'].astype('string')
        df['store_id']=df['store_id'].astype('string')
        df['id']=df['id'].astype('string')
        df['quantity']=df['quantity'].astype('string')
        df.rename(columns = {'drug_id':'drug-id'}, inplace = True)
        df.rename(columns = {'store_id':'store-id'}, inplace = True)
        df.rename(columns = {'id':'ob-incoming-details-id'}, inplace = True)

        # Split the dataframe into smaller batches
        batches = [df[i:i+BATCH_SIZE] for i in range(0, df.shape[0], BATCH_SIZE)]

        grouped = df.groupby('store-id')
        for name, group in grouped:
            clustered_data = group.to_dict(orient='records')

            store_id = clustered_data[0].get('store-id')

            headers = {
              'Token': '8b57e763bc8e890c',
              'Content-Type': 'application/json',
            }

            payload = json.dumps({
              "store-id": store_id,
              "items": clustered_data
            })

            url = "https://dev3-api.generico.in/api/v1/short-book"
            # response = requests.post(url, json=clustered_data)
            started_at = datetime.datetime.now()
            response = requests.request("POST", url, headers=headers, data=payload)
            logger.info(response.text)
            if response.status_code != 200:
                raise Exception("API request failed with status code: " + str(response.status_code))

            api_response = response.json()

            df = pd.DataFrame(response.json())

        # Loop through each row in the dataframe
            for i, row in df.iterrows():
                ob_incoming_detail_id= row.data.get('ob-incoming-details-id')
                started_at= started_at
                created_at= datetime.datetime.now()
                api_response= str(row.data)
                status= response.status_code
                sb_id= row.data.get('short-book-id')

                logger.info(ob_incoming_detail_id,started_at,created_at,api_response,status,sb_id)
                # insert_stmt = f"INSERT INTO <table_name> (column1, column2, glue_job_id, insert_timestamp) VALUES (?, ?, ?, ?)"

                cursor.execute(f"INSERT INTO ob_cron_detail (ob_incoming_detail_id,started_at,created_at,api_response,status,sb_id) VALUES({ob_incoming_detail_id},{started_at},{created_at},{api_response},{status},{sb_id})")

                # cursor.execute(f"UPDATE <table_name> SET column1 = {column1}, column2 = {column2} WHERE id = {id}")
                cursor.execute(f"UPDATE ob_cron_detail SET status=1 WHERE id = ob_incoming_detail_id")

        mssql_connection.commit()
        # Close the connection
        mssql_connection.close()
    except Exception as e:
        err_msg = str(e)
        logger.info('One beat incoming detail job failed')
        logger.exception(e)


