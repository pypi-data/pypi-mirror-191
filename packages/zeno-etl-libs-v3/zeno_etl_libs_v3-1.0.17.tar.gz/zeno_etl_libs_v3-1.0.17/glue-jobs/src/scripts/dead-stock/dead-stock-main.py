#!/usr/bin/env python
# coding: utf-8

'''
Purpose - NPI or Dead stock categorisation script
'''

import os
import sys

sys.path.append('../../../..')

from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.helper.email.email import Email
from zeno_etl_libs.db.db import DB
from zeno_etl_libs.logger import get_logger, send_logs_via_email
from zeno_etl_libs.helper import helper
from dateutil.tz import gettz

import json

import datetime
import argparse
import pandas as pd
import numpy as np
import traceback
from dateutil.relativedelta import relativedelta

from zeno_etl_libs.queries.dead_stock import dead_stock_queries

from zeno_etl_libs.queries.dead_stock.dead_stock_categorisation import dead_stock_categorization, dead_data_prep, dead_value_bucket
from zeno_etl_libs.utils.doid_write import doid_custom_write

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False)
parser.add_argument('-et', '--email_to', default="saurav.maskar@zeno.health", type=str, required=False)
parser.add_argument('-d', '--days', default=90, type=int, required=False)
parser.add_argument('-ed', '--expiry_days', default=150, type=int, required=False)
parser.add_argument('-fed', '--fofo_expiry_days', default=270, type=int, required=False)
parser.add_argument('-ned', '--npi_expiry_days', default=30, type=int, required=False)
parser.add_argument('-emc', '--expiry_month_cutoff', default=1, type=int, required=False)
parser.add_argument('-jn', '--job_name', default=None, type=str, required=False)
parser.add_argument('-lem', '--log_email_to', default="saurav.maskar@zeno.health", type=str, required=False)
parser.add_argument('-gif', '--goodaid_inclusion_flag', default=1, type=int, required=False)
parser.add_argument('-aiosr', '--add_in_omit_ss_reset', default=0, type=int, required=False)
parser.add_argument('-csmm', '--change_ss_min_max', default=0, type=int, required=False)
args, unknown = parser.parse_known_args()
env = args.env
email_to = args.email_to
days = args.days
expiry_days = args.expiry_days
fofo_expiry_days = args.fofo_expiry_days
npi_expiry_days = args.npi_expiry_days
expiry_month_cutoff = args.expiry_month_cutoff
job_name = args.job_name
log_email_to = args.log_email_to.split(",")
goodaid_inclusion_flag = args.goodaid_inclusion_flag
add_in_omit_ss_reset = args.add_in_omit_ss_reset
change_ss_min_max = args.change_ss_min_max

os.environ['env'] = env

logger = get_logger(level = 'INFO')

logger.info(f"env: {env}")

#secrets = config.secrets

rs_db = DB()

rs_db.open_connection()

rs_db_write = DB(read_only=False)
rs_db_write.open_connection()

s3 = S3()
start_time = datetime.datetime.now(tz=gettz('Asia/Kolkata'))
logger.info('Script Manager Initialized')
logger.info(f"env: {env}")
logger.info("email_to - " + email_to)
logger.info("days - " + str(days))
logger.info("expiry_days - " + str(expiry_days))
logger.info("fofo_expiry_days - " + str(fofo_expiry_days))
logger.info("npi_expiry_days - " + str(npi_expiry_days))
logger.info("expiry_month_cutoff - " + str(expiry_month_cutoff))
logger.info("job_name - " + str(job_name))
logger.info("log_email_to - " + str(log_email_to))
logger.info("goodaid_inclusion_flag - " + str(goodaid_inclusion_flag))
logger.info("add_in_omit_ss_reset - " + str(add_in_omit_ss_reset))
logger.info("change_ss_min_max - " + str(change_ss_min_max))
logger.info("")

# date parameter
logger.info("code started at {}".format(datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime(
    '%Y-%m-%d %H:%M:%S')))
logger.info("")

status = 'Failed'
doid_missed_entries = pd.DataFrame()

try :

    # get stores open date
    stores_date_query = '''
    select
        s.id as "store-id",
        s."franchisee-id" ,
        date(s."opened-at") as "opened-date",
        case
            when s."franchisee-id" = 1
            and DATEDIFF(d,
            s."opened-at",
            current_date)>= 182 then 'old'
            when s."franchisee-id" != 1
            and DATEDIFF(d,
            s."opened-at",
            current_date)>= 90 then 'old'
            else 'new'
        end as "store-age-flag"
    from
        "prod2-generico".stores s
    where
         s."opened-at" != '0101-01-01 00:00:00.000'
    '''
    stores_date = rs_db.get_df(stores_date_query)

    stores_list = stores_date.loc[
        stores_date['store-age-flag'] == 'old', 'store-id']

    trucate_inv_query = '''
    DELETE FROM "prod2-generico"."dead-stock-inventory"
    '''

    truncate_sns_query = '''
    delete from "prod2-generico"."dead-stock-inventory-sns" 
    where "snapshot-date" = CURRENT_DATE + 1
    '''
    insert_sns_query = ''' 
    insert
        into
        "prod2-generico"."dead-stock-inventory-sns"
        select
        CURRENT_DATE + 1 as "snapshot-date",
        "inventory-type",
        "store-id",
        "store-name",
        "drug-type",
        "drug-grade",
        sum(quantity) as quantity,
        sum(value) as value,
        sum("locked-quantity") as "locked-quantity",
        sum("locked-value") as "locked-value"
    from
        "prod2-generico"."dead-stock-inventory"
    group by
        "inventory-type",
        "store-id",
        "store-name",
        "drug-type",
        "drug-grade"
    '''

    sales = pd.DataFrame()
    inventory = pd.DataFrame()
    store_inventory_sales = pd.DataFrame()
    '''Getting sales and inventory data by store '''
    for store_id in sorted(stores_date['store-id'].unique()):
        logger.info('Loading data for store ' + str(store_id))
        sales_store, inventory_store, store_inventory_sales_store = dead_data_prep(
                store_id, days, logger, connection = rs_db)
        sales = sales.append(sales_store)
        inventory = inventory.append(inventory_store)
        store_inventory_sales = store_inventory_sales.append(
            store_inventory_sales_store)

    # GA drugs inclusion flag
    if int(goodaid_inclusion_flag)==0:
        logger.info('removing GA drugs from categorisation')
        goodaid_drug_query = '''
                select
                    d.id as "drug-id"
                from
                    "prod2-generico".drugs d
                where
                    d."company-id" = 6984
            '''
        goodaid_drugs = rs_db.get_df(goodaid_drug_query)
        goodaid_drug_id = tuple(map(int,goodaid_drugs['drug-id'].unique()))
        sales = sales[~sales['drug-id'].isin(goodaid_drug_id)]
        inventory = inventory[~inventory['drug-id'].isin(goodaid_drug_id)]
        store_inventory_sales = store_inventory_sales[~store_inventory_sales['drug-id'].isin(goodaid_drug_id)]
        logger.info('removed GA drugs from categorisation')
    else:
        logger.info('not removing GA drugs from categorisation')


    '''Inventory categorisation into different buckets'''
    zippin_inventory, store_drug_no_sale, store_drug_with_sale,expiry_barcodes, return_barcodes, rotation_barcodes, fifo_barcodes = dead_stock_categorization(
                sales, inventory, store_inventory_sales,
                stores_list, logger, days, expiry_days, fofo_expiry_days,connection = rs_db)

    rs_db_write.execute(trucate_inv_query)

    schema = 'prod2-generico'
    table_name = 'dead-stock-inventory'
    table_info = helper.get_table_info(db=rs_db, table_name=table_name, schema=schema)

    expiry_barcodes['uploaded-at']= datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
    expiry_barcodes['created-date']= datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d')
    expiry_barcodes[['invoice-item-id','invoice-id','distributor-id','short-book-id']] = expiry_barcodes[['invoice-item-id','invoice-id','distributor-id','short-book-id']].apply(pd.to_numeric, errors='ignore').astype('Int64')

    s3.write_df_to_db(df=expiry_barcodes[table_info['column_name']], table_name=table_name, db=rs_db_write,
                      schema=schema)

    return_barcodes['uploaded-at']= datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
    return_barcodes['created-date']= datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d')
    return_barcodes[['invoice-item-id','invoice-id','distributor-id','short-book-id']] = return_barcodes[['invoice-item-id','invoice-id','distributor-id','short-book-id']].apply(pd.to_numeric, errors='ignore').astype('Int64')

    s3.write_df_to_db(df=return_barcodes[table_info['column_name']], table_name=table_name, db=rs_db_write,
                      schema=schema)

    rotation_barcodes['uploaded-at']= datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
    rotation_barcodes['created-date']= datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d')
    rotation_barcodes[['invoice-item-id','invoice-id','distributor-id','short-book-id']] = rotation_barcodes[['invoice-item-id','invoice-id','distributor-id','short-book-id']].apply(pd.to_numeric, errors='ignore').astype('Int64')

    s3.write_df_to_db(df=rotation_barcodes[table_info['column_name']], table_name=table_name, db=rs_db_write,
                      schema=schema)

    fifo_barcodes['uploaded-at']= datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
    fifo_barcodes['created-date']= datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d')
    fifo_barcodes[['invoice-item-id','invoice-id','distributor-id','short-book-id']] = fifo_barcodes[['invoice-item-id','invoice-id','distributor-id','short-book-id']].apply(pd.to_numeric, errors='ignore').astype('Int64')

    s3.write_df_to_db(df=fifo_barcodes[table_info['column_name']], table_name=table_name, db=rs_db_write,
                      schema=schema)

    rs_db_write.execute(truncate_sns_query)
    rs_db_write.execute(insert_sns_query)

    # Rotation drugs to be appended in omit_ss_reset table
    omit_drug_store = rotation_barcodes[["drug-id",
                                         "store-id"]].drop_duplicates()
    omit_drug_store["updated-at"] = datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
    omit_drug_store["created-at"] = datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
    omit_drug_store["created-by"] = 'data.sciene@zeno.health'
    omit_drug_store["updated-by"] = 'data.sciene@zeno.health'
    omit_drug_store["start-date"] = datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d')
    omit_drug_store["end-date"] =  (datetime.datetime.now(tz=gettz('Asia/Kolkata')) + datetime.timedelta(
        days=npi_expiry_days)).strftime('%Y-%m-%d')

   # If you want to block in ipc, then (add_in_omit_ss_reset) parameter must be 1
    if int(add_in_omit_ss_reset) == 1:
        omit_drug_store["is-active"] = 1
        logger.info('adding to omit_ss_reset, is-active = 1')
    else:
        omit_drug_store["is-active"] = 0
        logger.info('not adding to omit_ss_reset, is-active = 0')

    omit_drug_store["reason"] = 'NPI'
    schema = 'prod2-generico'
    table_name = 'omit-ss-reset'

    # Uncomment following part once omit-ss-reset table is transferred to DSS

    table_info = helper.get_table_info(db=rs_db, table_name=table_name, schema=schema)

    s3.write_df_to_db(df=omit_drug_store[table_info['column_name']], table_name=table_name, db=rs_db_write,
                      schema=schema)

    if int(change_ss_min_max) == 1:
        logger.info('changing Min, max,SS to 0')
        # set max=0 for npi drugs in DOID
        npi_store_drugs = omit_drug_store[["store-id", "drug-id"]]
        npi_store_drugs.columns = [c.replace('-', '_') for c in npi_store_drugs.columns]
        doid_missed_entries = doid_custom_write(npi_store_drugs, logger)

    else :
        logger.info('Not changing min,max,SS to 0')
        doid_missed_entries = pd.DataFrame()

    # save email attachements to s3
    curr_date = str(datetime.date.today())
    doid_missed_entries_uri = s3.save_df_to_s3(doid_missed_entries,
                                           file_name=f"doid_missed_entries_{curr_date}.csv")

    # Commenting Value Bucketing because relevant tables were not getting updated in DSS also

    # '''Value bucketing done once a week: Monday morning'''
    # if datetime.datetime.now().date().weekday() == 0:
    #
    #     store_line_query= """
    #     select
    #         sm.id as "store-id",
    #         sm.line
    #     from
    #         "prod2-generico"."stores-master" sm
    #     """
    #     store_line = rs_db.get_df(store_line_query)
    #
    #     rotation_barcodes = rotation_barcodes.merge(
    #         store_line, on='store-id', how='inner')
    #
    #     rotation_barcodes['type-flag'] = np.select(
    #         [rotation_barcodes['drug-type'] == 'ethical',
    #          rotation_barcodes['drug-type'] == 'generic'],
    #         ['ethical', 'generic'], default='others'
    #     )
    #     rotation_value_bucket = rotation_barcodes.groupby(
    #         ['line']).apply(dead_value_bucket).reset_index()
    #     if 'level_1' in rotation_value_bucket.columns:
    #         rotation_value_bucket.drop('level_1', axis=1, inplace=True)
    #     if 'level-1' in rotation_value_bucket.columns:
    #         rotation_value_bucket.drop('level-1', axis=1, inplace=True)
    #     week_date = str(datetime.datetime.now().date())
    #     rotation_value_bucket['week-date'] = week_date
    #     engine.execute(
    #         '''delete from rotation_value_bucket where week_date = '{}'
    #         '''.format(week_date))
    #     rotation_value_bucket.to_sql(
    #         name='rotation_value_bucket', con=engine, if_exists='append',
    #         chunksize=500, method='multi', index=False)


    # Commenting expiry_monthly_ss because this part was commented in DSS also
    # '''Expired/Near Expiry barcode shapshot for first of the month'''
    # # commenting out expiry snapshot as it is manual now
    # '''
    # current_date = datetime.datetime.now().date()
    # if current_date.day == 1:
    #     logger.info('Month beginning snapshot for expired/near expiry')
    #     expiry_date_limit = (
    #         current_date + relativedelta(
    #             months=expiry_month_cutoff, days=-current_date.day))
    #     expiry_monthly_ss = expiry_barcodes[
    #         expiry_barcodes.expiry <= expiry_date_limit]
    #     expiry_monthly_ss['snapshot_date'] = str(current_date)
    #     expiry_monthly_ss.to_sql(
    #         name='expiry_monthly_ss', con=engine, if_exists='append',
    #         chunksize=500, method='multi', index=False)

    status = 'Success'
except:
    status = 'Failed'
    logger.info('table load failed')
    doid_missed_entries_uri = None
    table_name = None


end_time = datetime.datetime.now(tz=gettz('Asia/Kolkata'))
difference = end_time - start_time
min_to_complete = round(difference.total_seconds() / 60, 2)
email = Email()

if status == 'Success':
    email.send_email_file(subject=f"{env}-{status} : {table_name}",
                          mail_body=f"{table_name} update {status}, Time for job completion - {min_to_complete} mins,"
                                    f"DOID missed entries: {doid_missed_entries.shape[0]} ",
                          to_emails=email_to, file_uris=[doid_missed_entries_uri])
elif status=='Failed':
    email.send_email_file(subject=f"{env}-{status} : {table_name}",
                          mail_body=f"{table_name} update {status}, Time for job completion - {min_to_complete} mins,",
                          to_emails=email_to, file_uris=[])

# send_logs_via_email(job_name=job_name, email_to=log_email_to)

# Closing the DB Connection
rs_db.close_connection()
rs_db_write.close_connection()