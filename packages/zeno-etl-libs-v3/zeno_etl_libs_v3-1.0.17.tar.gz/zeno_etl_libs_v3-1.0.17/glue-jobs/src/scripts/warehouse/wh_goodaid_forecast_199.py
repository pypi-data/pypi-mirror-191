#!pip install zeno_etl_libs==1.0.36

"""
Created on Sun May 26 23:28:09 2021

@author: vivek.sidagam@zeno.health

Purpose: To generate forecast for Goodaid drugs at Bhiwandi warehouse
"""

import os
import sys
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from dateutil.tz import gettz
from scipy.stats import norm
from calendar import monthrange

sys.path.append('../../../..')

from zeno_etl_libs.db.db import DB
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper.email.email import Email
from zeno_etl_libs.utils.ipc.doid_update_ss import doid_update
from zeno_etl_libs.helper.parameter.job_parameter import parameter

#tag = parameters
env = "dev"

os.environ['env'] = env

job_params = parameter.get_params(job_id=130)
email_to = job_params['email_to']
days = job_params['days']
lead_time_mean = job_params['lead_time_mean']
lead_time_std = job_params['lead_time_std']
max_review_period = job_params['max_review_period']
wh_id = 199
cap_ss_days = job_params['cap_ss_days']
service_level = job_params['service_level']
ordering_freq = job_params['ordering_freq']

logger = get_logger()
logger.info("Scripts begins. Env = " + env)

status = False
err_msg = ''
df_uri = ''
run_date = str(datetime.now().strftime("%Y-%m-%d"))
drugs_not_in_doi = 0
drugs_missed = 0
drugs_updated = 0

def get_launch_stock_per_store(rs_db, days, drugs):
    new_stores_list_query = """
        select
            id as store_id,
            date("opened-at") as opened_at
        from
            "prod2-generico".stores s
        where
            "opened-at" >= CURRENT_DATE - {days}
            and id not in (281, 297)
    """.format(days=days)
    new_stores_list = rs_db.get_df(new_stores_list_query)

    store_ids_list = tuple(new_stores_list['store_id'].astype(str))

    # get shortbook launch orders
    sb_orders_query = '''
        select
            distinct sb."store-id" as store_id,
            sb."drug-id" as drug_id,
            date(sb."created-at") as created_at,
            sb.quantity as ordered_quantity,
            date(s2."opened-at") as opened_at
        from
            "prod2-generico"."short-book-1" sb
        left join "prod2-generico".stores s2 on
            s2.id = sb."store-id"
        where
            "store-id" in {store_ids}
            and date(sb."created-at") < date(s2."opened-at")
    '''.format(store_ids=store_ids_list, days=days)
    sb_orders = rs_db.get_df(sb_orders_query)

    df = sb_orders.copy()
    df = df[df['drug_id'].isin(drugs['drug_id'])]
    df = df[['store_id', 'drug_id', 'ordered_quantity']]
    df.drop_duplicates(inplace=True)
    new_stores_count = sb_orders['store_id'].nunique()
    df = df[['drug_id', 'ordered_quantity']]
    launch_stock = df.groupby('drug_id').sum().reset_index()
    launch_stock_per_store = launch_stock.copy()
    launch_stock_per_store['ordered_quantity'] = \
        launch_stock['ordered_quantity'] / new_stores_count
    launch_stock_per_store.rename(
        columns={'ordered_quantity': 'launch_stock_per_store'}, inplace=True)

    return launch_stock_per_store

try:
    rs_db = DB()
    rs_db.open_connection()
    # read inputs file to get parameters
    logger.info('reading input file to get parameters')
    params_table_query = """
        select
            "param-name" as param,
            value
        from
            "prod2-generico"."wh-goodaid-forecast-input"
        where
            "param-name" not in ('drug_lvl_fcst_inputs' , 's_and_op_factors')
    """
    logger.info('input parameters read')
    params_table = rs_db.get_df(params_table_query)
    params_table = params_table.apply(pd.to_numeric, errors='ignore')

    revenue_min = int(params_table.where(
        params_table['param'] == 'revenue_min', axis=0).dropna()['value'])
    revenue_max = int(params_table.where(
        params_table['param'] == 'revenue_max', axis=0).dropna()['value'])

    #getting expected new stores openings
    params_table_query = """
                select
                    "month-begin-dt" as month_begin_dt,
                    value as expected_nso
                from
                    "prod2-generico"."wh-forecast-repln-input"
                where
                    "param-name" = 'expected_nso'
            """
    params_table = rs_db.get_df(params_table_query)
    logger.info('expected_nso parameter read')
    params_table = params_table.apply(pd.to_numeric, errors='ignore')

    params_table['month_begin_dt'] = params_table['month_begin_dt'].astype(str)

    current_month_date = (
            datetime.now(tz=gettz('Asia/Kolkata')).date() -
            timedelta(days=datetime.now(tz=gettz('Asia/Kolkata')).day - 1))

    try:
        expected_new_stores = int(params_table[
                               params_table[
                                   'month_begin_dt'] == str(current_month_date)][
                               'expected_nso'])
    except Exception as error:
        expected_new_stores = 0
    logger.info("expected new stores --> " + str(expected_new_stores))

    # get active gaid drugs list
    drugs_query = '''
        select
            wssm."drug-id" as drug_id,
            d.composition,
            d."drug-name" as drug_name,
            d.company,
            d."type",
            d.category
        from
            "prod2-generico"."wh-sku-subs-master" wssm
        left join "prod2-generico".drugs d on
            d.id = wssm."drug-id"
        where
            wssm."add-wh" = 'Yes'
            and d."type" not in ('discontinued-products')
            and d.company = 'GOODAID'
        '''
    drugs = rs_db.get_df(drugs_query)
    logger.info('active drugs list pulled from wssm')

    # get 28 days sales for active gaid drugs
    drug_sales_query = '''
        select
            "drug-id" as drug_id,
            date("created-at") as created_at,
            sum(quantity) as drug_sales_quantity
        from
            "prod2-generico".sales
        where
            "drug-id" in {drug_ids}
            and date("created-at") >= current_date - {days}
            and date("created-at") < current_date
        group by
            "drug-id",
            date("created-at")
    '''.format(days=days, drug_ids=tuple(drugs['drug_id']))
    sales_data_for_std = rs_db.get_df(drug_sales_query)
    drugs_std = sales_data_for_std.groupby('drug_id').std().reset_index()
    drugs_std = drugs_std.rename(columns={'drug_sales_quantity': 'demand_daily_deviation'})
    drug_sales = sales_data_for_std.groupby('drug_id').sum().reset_index()
    logger.info('drug sales data pulled from rs')
    drug_sales['drug_sales_quantity'] = drug_sales[
                                            'drug_sales_quantity'] * 28 / days

    # get non-ethical composition level sale
    composition_sales_query = '''
        select
            composition as composition,
            sum(quantity) as composition_sales_quantity
        from
            "prod2-generico".sales
        where
            composition in {compositions}
            and date("created-at") >= current_date - {days}
            and date("created-at") < current_date
            and "type" <> 'ethical'
        group by
            composition
    '''.format(days=days, compositions=tuple(drugs['composition']))
    composition_sales = rs_db.get_df(composition_sales_query)
    logger.info('composition data pulled from rs')
    composition_sales['composition_sales_quantity'] = composition_sales[
                                                          'composition_sales_quantity'] * 28 / days

    # merging data
    main_df = drugs.merge(drug_sales, on='drug_id', how='left')
    main_df['drug_sales_quantity'].fillna(0, inplace=True)
    main_df = main_df.merge(composition_sales, on='composition',
                            how='left')
    main_df['composition_sales_quantity'].fillna(0, inplace=True)

    # getting 50% of composition level sales
    main_df['composition_sales_quantity_50%'] = main_df[
                                                    'composition_sales_quantity'] * 0.5
    main_df['composition_sales_quantity_50%'] = main_df[
        'composition_sales_quantity_50%'].round(0)

    # calculate month-on-month sales growth
    # getting last-to-last 28 day sales for calcuating growth factor
    last_to_last_sales_query = '''
        select
            "drug-id" as drug_id,
            sum(quantity) as last_to_last_28_day_sales
        from
            "prod2-generico".sales
        where
            "drug-id" in {drug_ids}
            and date("created-at") >= current_date - 56
            and date("created-at") < current_date - 28
        group by
            "drug-id"
    '''.format(drug_ids=tuple(drugs['drug_id']))
    last_to_last_sales = rs_db.get_df(last_to_last_sales_query)
    logger.info('last-to-last 28 day sales data pulled from rs')

    # getting last 28 day sales
    last_sales_query = '''
        select
            "drug-id" as drug_id,
            sum(quantity) as last_28_day_sales
        from
            "prod2-generico".sales
        where
            "drug-id" in {drug_ids}
            and date("created-at") >= current_date - 28
            and date("created-at") < current_date
        group by
            "drug-id"
    '''.format(drug_ids=tuple(drugs['drug_id']))
    last_sales = rs_db.get_df(last_sales_query)
    logger.info('last 28 day sales data pulled from rs')

    # merging to main_df
    main_df = main_df.merge(last_to_last_sales, on='drug_id', how='left')
    main_df['last_to_last_28_day_sales'].fillna(0, inplace=True)
    main_df = main_df.merge(last_sales, on='drug_id', how='left')
    main_df['last_28_day_sales'].fillna(0, inplace=True)
    main_df['growth_factor'] = main_df['last_28_day_sales'] / main_df[
        'last_to_last_28_day_sales']
    main_df['growth_factor'].fillna(1, inplace=True)
    main_df['growth_factor'] = np.where(main_df[
                                            'growth_factor'] == np.inf, 1,
                                        main_df['growth_factor'])
    # growth factor capped at 150% - min at 100%
    main_df['growth_factor'] = np.where(main_df[
                                            'growth_factor'] > 1.5, 1.5,
                                        main_df['growth_factor'])
    main_df['growth_factor'] = np.where(main_df[
                                            'growth_factor'] < 1, 1,
                                        main_df['growth_factor'])
    # growth factor foreced to 1 when 50% comp sales > drug sales
    main_df['growth_factor'] = np.where(main_df[
                                            'composition_sales_quantity_50%'] >
                                        main_df[
                                            'drug_sales_quantity'], 1,
                                        main_df['growth_factor'])
    main_df['s_op_factor'] = 1

    # get avg gaid sales for 13-16 lakh revenue stores
    # getting stores lists to compare with
    stores_cmp_query = '''
        select
            "store-id" as store_id,
            round(sum("revenue-value")) as revenue
        from
            "prod2-generico".sales
        where
            date("created-at") >= current_date - 28
            and date("created-at") < current_date
        group by
            "store-id"
    '''
    stores_cmp = rs_db.get_df(stores_cmp_query)
    stores_cmp = stores_cmp[stores_cmp['revenue'] > revenue_min]
    stores_cmp = stores_cmp[stores_cmp['revenue'] < revenue_max]
    stores_list_to_comp = tuple(stores_cmp['store_id'])
    logger.info('list of stores with revenue between 1.3 and 1.6 mil -->'
                + str(stores_list_to_comp))

    # adding expected_new_stores column
    main_df['expected_new_stores'] = expected_new_stores

    # getting avg sales
    avg_store_sales_query = '''
        select
            composition ,
            sum(quantity)/ {count} as avg_drug_sales_quantity
        from
            "prod2-generico".sales
        where
            composition in {compositions}
            and date("created-at") >= current_date - 28
            and date("created-at") < current_date
            and "type" <> 'ethical'
            and "store-id" in {stores_list_to_comp}
        group by
            composition
    '''.format(compositions=tuple(drugs['composition']), \
               stores_list_to_comp=stores_list_to_comp, \
               count=len(stores_list_to_comp))
    avg_store_sales = rs_db.get_df(avg_store_sales_query)
    logger.info('avg composition sales retrieved for sample stores')
    avg_store_sales['avg_drug_sales_quantity'] = avg_store_sales[
        'avg_drug_sales_quantity'].round()

    # merge to main_df
    main_df = main_df.merge(avg_store_sales, on='composition', how='left')
    main_df['avg_drug_sales_quantity'].fillna(0, inplace=True)

    # get final forecast figures
    main_df['forecast'] = main_df[[
        'drug_sales_quantity',
        'composition_sales_quantity_50%']].max(axis=1)
    main_df['forecast'] = main_df['forecast'] * main_df['growth_factor'] * \
                          main_df['s_op_factor'] + main_df[
                              'expected_new_stores'] * \
                          main_df['avg_drug_sales_quantity']
    main_df['forecast'] = main_df['forecast'].round()

    main_df['demand_daily'] = main_df['forecast'] / 28
    main_df = main_df.merge(drugs_std, on='drug_id', how='left')
    main_df['demand_daily_deviation'].fillna(0, inplace=True)
    main_df['lead_time_mean'] = lead_time_mean
    main_df['lead_time_std'] = lead_time_std
    main_df['review_period'] = max_review_period
    main_df['ordering_freq'] = ordering_freq
    main_df['service_level'] = service_level

    # calculate ss min max
    main_df['ss_wo_cap'] = (norm.ppf(main_df['service_level']).round(2) * np.sqrt(
                                    (
                                            main_df['lead_time_mean'] *
                                            main_df['demand_daily_deviation'] *
                                            main_df['demand_daily_deviation']
                                    ) +
                                    (
                                            main_df['lead_time_std'] *
                                            main_df['lead_time_std'] *
                                            main_df['demand_daily'] *
                                            main_df['demand_daily']
                                    )
                                )
                            ).round(0)
    main_df['cap_ss_days'] = np.where(main_df['ss_wo_cap'] / main_df['forecast'] * 28 > cap_ss_days,
                                      cap_ss_days, '')
    main_df['safety_stock'] = np.where(main_df['ss_wo_cap'] / main_df['forecast'] * 28 > cap_ss_days,
                                       main_df['drug_sales_quantity'] / 28 * cap_ss_days,
                                       main_df['ss_wo_cap']).round(0)
    main_df['rop_without_nso'] = (
            main_df['safety_stock'] +
            main_df['demand_daily'] *
            (
                    main_df['lead_time_mean'] + main_df['review_period']
            )
    ).round()
    launch_stock_per_store = get_launch_stock_per_store(rs_db, 90, drugs)
    main_df = main_df.merge(launch_stock_per_store, on='drug_id', how='left')
    main_df['launch_stock_per_store'].fillna(0, inplace=True)
    num_days = monthrange(current_month_date.year, current_month_date.month)[1]
    main_df['reorder_point'] = main_df['rop_without_nso'] + \
                             np.round((main_df['lead_time_mean'] + main_df['review_period']) *
                                      main_df['expected_new_stores'] / num_days) * \
                             main_df['launch_stock_per_store']

    main_df['order_upto_point'] = (
            main_df['reorder_point'] +
            main_df['ordering_freq'] * main_df['demand_daily']
    ).round()

    main_df['safety_stock_doh'] = main_df['safety_stock'] / main_df['forecast'] * 28
    main_df['reorder_point_doh'] = main_df['reorder_point'] / main_df['forecast'] * 28
    main_df['order_upto_point_doh'] = main_df['order_upto_point'] / main_df['forecast'] * 28

    # get table structure to write to
    to_upload_query = '''
        select
            *
        from
            "prod2-generico"."wh-safety-stock"
        limit 1
    '''
    to_upload = rs_db.get_df(to_upload_query)
    to_upload.columns = [c.replace('-', '_') for c in to_upload.columns]

    to_upload.drop(0, axis=0, inplace=True)

    to_upload['drug_id'] = main_df['drug_id']
    to_upload['drug_name'] = main_df['drug_name']
    to_upload['type'] = main_df['type']
    to_upload['category'] = main_df['category']
    to_upload['company'] = main_df['company']
    # to_upload['bucket'] = main_df['bucket']
    to_upload['fcst'] = main_df['forecast'].astype(int, errors='ignore')
    to_upload['wh_id'] = wh_id
    to_upload['forecast_type'] = 'goodaid_199'
    to_upload['lead_time_mean'] = main_df['lead_time_mean']
    to_upload['max_review_period'] = main_df['review_period'].astype(int, errors='ignore')
    to_upload['demand_daily'] = main_df['demand_daily']
    to_upload['std'] = main_df['demand_daily_deviation']
    to_upload['safety_stock'] = main_df['safety_stock'].astype(int, errors='ignore')
    to_upload['expected_nso'] = expected_new_stores
    to_upload['rop_without_nso'] = main_df['rop_without_nso'].astype(int, errors='ignore')
    to_upload['reorder_point'] = main_df['reorder_point'].astype(int, errors='ignore')
    to_upload['order_upto_point'] = main_df['order_upto_point'].astype(int, errors='ignore')
    to_upload['last_month_sales'] = main_df['drug_sales_quantity'].astype(int, errors='ignore')
    to_upload['safety_stock_days'] = main_df['safety_stock_doh']
    to_upload['reorder_point_days'] = main_df['reorder_point_doh']
    to_upload['order_upto_days'] = main_df['order_upto_point_doh']
    to_upload['reset_date'] = run_date
    to_upload['month'] = str(datetime.now(tz=gettz('Asia/Kolkata')).strftime("%m"))
    to_upload['year'] = str(datetime.now(tz=gettz('Asia/Kolkata')).strftime("%Y"))
    to_upload['month_begin_dt'] = str(
        datetime.now(tz=gettz('Asia/Kolkata')).date() - timedelta(days=datetime.now(tz=gettz('Asia/Kolkata')).day - 1))
    to_upload['created_at'] = datetime.now(tz=gettz('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")
    to_upload['created_by'] = 'etl-automation'
    to_upload['updated_at'] = datetime.now(tz=gettz('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")
    to_upload['updated_by'] = 'etl-automation'
    to_upload['cap_ss_days'] = main_df['cap_ss_days']
    to_upload['ss_wo_cap'] = main_df['ss_wo_cap'].astype(int, errors='ignore')
    to_upload['lead_time_std'] = main_df['lead_time_std']
    to_upload['ordering_freq'] = main_df['ordering_freq']
    to_upload = to_upload.fillna('')

    #write connection
    rs_db_write = DB(read_only=False)
    rs_db_write.open_connection()
    s3 = S3()
    s3.write_df_to_db(df=to_upload, table_name='wh-safety-stock', db=rs_db_write, schema='prod2-generico')
    logger.info("wh-safety-stock table updated")

    # WRITING ATTACHMENTS FOR SUCCESS
    df_uri = s3.save_df_to_s3(df=main_df,
                              file_name='BHW_goodaid_forecast_{date}.csv'.format(date=str(run_date)))

    # writing to doid
    logger.info('writing to doid for ' +
                str(int(to_upload[['drug_id']].nunique())) + ' drugs')
    ss_data_upload = to_upload.query('order_upto_point > 0')[
        ['wh_id', 'drug_id', 'safety_stock', 'reorder_point',
         'order_upto_point']]
    ss_data_upload.columns = [
        'store_id', 'drug_id', 'corr_min', 'corr_ss', 'corr_max']
    type_list = tuple(drugs['type'].unique())
    ss_data_upload = ss_data_upload.astype(float)
    new_drug_entries, missed_entries = doid_update(ss_data_upload, type_list, rs_db, 'prod2-generico', logger, gaid_omit=False)
    rs_db.connection.close()
    drugs_not_in_doi = len(new_drug_entries)
    drugs_missed = len(missed_entries)
    drugs_updated = len(ss_data_upload) - len(missed_entries) - len(new_drug_entries)
    rs_db.close_connection()
    rs_db_write.close_connection()
    status = True

except Exception as e:
    err_msg = str(e)
    logger.info('wh_goodaid_forecast_199 job failed')
    logger.exception(e)

# Sending email
email = Email()
if status:
    result = 'Success'
    email.send_email_file(subject=f"Bhiwandi Warehouse GOODAID forecast ({env}): {result}",
                          mail_body=f"""
                            drugs updated successfully --> {drugs_updated}
                            drugs not updated --> {drugs_missed}
                            drugs not in doid --> {drugs_not_in_doi}
                          """,
                          to_emails=email_to, file_uris=[df_uri])
else:
    result = 'Failed'
    email.send_email_file(subject=f"Bhiwandi Warehouse GOODAID forecast ({env}): {result}",
                          mail_body=f"Run time: {datetime.now(tz=gettz('Asia/Kolkata'))} {err_msg}",
                          to_emails=email_to, file_uris=[])

logger.info("Script ended")

"""
DDL

create table "prod2-generico"."wh-goodaid-forecast-input" ( 
	"param-name" text ENCODE lzo,
	value text ENCODE lzo,
	"drug-id" text ENCODE lzo,
	"lead_time_doh" int8 ENCODE az64,	
	"safety_stock_doh"  int8 ENCODE az64,	
	"review_period" int8 ENCODE az64,
	"start-date" date ENCODE az64,
	"end-date" date ENCODE az64,
	description text ENCODE lzo,
	"created-at" TIMESTAMP without TIME zone default getdate() ENCODE az64,
	"created-by" VARCHAR default 'etl-automation' ENCODE lzo,
	"updated-at" TIMESTAMP without TIME zone default getdate() ENCODE az64,
	"updated-by" VARCHAR default 'etl-automation' ENCODE lzo 
);

ALTER TABLE "prod2-generico"."wh-goodaid-forecast-input" owner to "admin";
"""
