"""
wrapper for recording daily out-of-shelf on store-sku & store level
author: vivek.revi@zeno.health
"""
import os
import sys

import pandas as pd
import datetime as dt
import dateutil.relativedelta as date_util
import numpy as np
from dateutil.tz import gettz

sys.path.append('../../../..')

from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.db.db import DB
from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper.email.email import Email
from zeno_etl_libs.helper import helper
from zeno_etl_libs.db.db import Athena

import argparse


def main(debug_mode, as_inactive_exclude_types, mature_delta_days,
         exclude_stores, rs_db_read, rs_db_write, read_schema, write_schema,
         logger):
    s3 = S3()
    athena = Athena()
    logger.info(f"Debug Mode: {debug_mode}")
    status = 'Failed'
    run_date = dt.date.today()
    mature_delta_start_date = run_date - dt.timedelta(days=mature_delta_days)

    # define empty variables
    out_of_shelf = pd.DataFrame()
    store_count, oos_sys, oos_ethical, oos_generic, oos_others = 0, 0, 0, 0, 0
    sanity_check = "Not-Verified"

    try:
        logger.info("Getting all store IDs")
        stores = get_stores(exclude_stores, rs_db_read, read_schema)
        store_id_list = list(stores['id'])
        logger.info("All stores ID's fetched!")

        # sanity check - ensure past "mature_delta_days" data present in OOS table
        logger.info("Performing data sanity check in OOS table")
        q_dates_preset = """
                select distinct "closing-date" 
                from "{schema}"."out-of-shelf-drug-level" oosdl 
                where "closing-date" >= '{start_date}'
                and "closing-date" < '{end_date}' 
                """.format(schema=read_schema,
                           start_date=mature_delta_start_date.strftime("%Y-%m-%d"),
                           end_date=run_date.strftime("%Y-%m-%d"))
        df_dates_preset = rs_db_read.get_df(q_dates_preset)
        df_dates_preset.columns = [c.replace('-', '_') for c in
                                   df_dates_preset.columns]
        date_count = len(df_dates_preset["closing_date"].to_list())

        if date_count < mature_delta_days:
            missing_days = mature_delta_days - date_count
            sanity_check = f"{missing_days}/{mature_delta_days} of recent " \
                           f"days data missing in OOS table"
            logger.info(sanity_check)
            return status, sanity_check, run_date, store_count, oos_sys, \
                   oos_ethical, oos_generic, oos_others

        else:
            sanity_check = "Verified!"
            logger.info("Data verified in OOS table")

        # getting oos iteratively
        for store_id in store_id_list:
            logger.info(f"Getting required data for store: {store_id}")

            # getting current inventory
            inventory = get_inventory(store_id, rs_db_read, read_schema)

            # getting past 30d sales values of drugs in store
            df_30d_sales = get_past_30d_sales(store_id, rs_db_read, run_date,
                                              read_schema)

            # getting ipc buckets
            df_buckets = get_buckets(store_id, rs_db_read, read_schema)

            # getting doi info for drugs whose max is set
            doi_class_1 = get_drug_list(store_id, rs_db_read, read_schema, max_set='Y',
                                        drugs=[])
            doi_class_1["max_set"] = 'Y'

            # getting doi info for drugs whose max is not set,
            # but sold in past 3 months
            drug_list = list(df_30d_sales.drug_id.unique())
            doi_class_2 = get_drug_list(store_id, rs_db_read, read_schema, max_set='N',
                                        drugs=drug_list)
            doi_class_2["max_set"] = 'N'

            # combine both doi_class tables
            doi_class = doi_class_1.append(doi_class_2)

            # getting std_qty of all drugs in system
            drug_std_qty = get_std_qty(rs_db_read, read_schema)

            # get mature drug flags
            df_mature_flag = mature_drugs_flag(
                store_id, run_date, mature_delta_start_date, mature_delta_days,
                rs_db_read, read_schema)

            # ==========================================
            #       Out of shelf calculation starts
            # ==========================================
            store_name = inventory["store_name"].unique()[0]
            out_of_shelf_store = doi_class.merge(inventory[['store_id',
                                                            'store_name',
                                                            'drug_id',
                                                            'quantity']],
                                                 on=['store_id', 'drug_id'],
                                                 how='left')
            out_of_shelf_store['quantity'].fillna(0, inplace=True)
            out_of_shelf_store['store_name'].fillna(store_name, inplace=True)

            # set OUP = 0, for NPI drugs in max_set = 'N'
            out_of_shelf_store["order_upto_point"] = np.where(
                out_of_shelf_store["max_set"] == 'N',
                0, out_of_shelf_store["order_upto_point"])

            # merging buckets of drugs
            out_of_shelf_store = out_of_shelf_store.merge(df_buckets,
                                                          on=["store_id",
                                                              "drug_id"],
                                                          how="left")
            out_of_shelf_store["bucket"].fillna('NA', inplace=True)

            # merging std_qty of drugs
            out_of_shelf_store = out_of_shelf_store.merge(drug_std_qty,
                                                          on="drug_id",
                                                          how="left")
            out_of_shelf_store["std_qty"].fillna(1, inplace=True)

            # merging past 30d sales value of store-drugs
            out_of_shelf_store = out_of_shelf_store.merge(df_30d_sales,
                                                          on="drug_id",
                                                          how="left")
            out_of_shelf_store["gross_sales_val"].fillna(0, inplace=True)

            # add mature drug_flag
            out_of_shelf_store = out_of_shelf_store.merge(
                df_mature_flag, how='left', on=['store_id', 'drug_id'])
            out_of_shelf_store['mature_flag'].fillna('N', inplace=True)

            out_of_shelf = out_of_shelf.append(out_of_shelf_store)

        out_of_shelf["closing_date"] = run_date
        logger.info("All stores required data fetched!")

        # calculating store wise OOS percent high-value-ethical
        logger.info("Creating OOS report on store-drug level")
        out_of_shelf["type"] = np.where(
            out_of_shelf["type"] == 'high-value-ethical', 'ethical',
            out_of_shelf["type"])
        out_of_shelf["type"] = np.where(
            out_of_shelf["type"].isin(['generic', 'ethical']),
            out_of_shelf["type"], 'others')

        out_of_shelf["oos_flag"] = np.where(out_of_shelf["quantity"] == 0, 1, 0)

        # adding inv<min (SS) flag
        out_of_shelf["oos_min_flag"] = np.where(
            out_of_shelf["quantity"] <= out_of_shelf["safety_stock"], 1, 0)

        # adding inv<std_qty flag
        out_of_shelf["oos_std_qty_flag"] = np.where(
            out_of_shelf["quantity"] < out_of_shelf["std_qty"], 1, 0)

        # adding 30d sales value
        out_of_shelf["oos_sales_loss_30d"] = out_of_shelf["gross_sales_val"] * \
                                             out_of_shelf["oos_flag"]

        out_of_shelf["sales_30d"] = out_of_shelf["gross_sales_val"]

        # exclude as-active = 0 based on specified drug types
        out_of_shelf = out_of_shelf.loc[~((out_of_shelf["as_active"] == 0) &
                                          (out_of_shelf["type"].isin(
                                              as_inactive_exclude_types)))]

        # OOS group store drug level
        out_of_shelf_group = pd.DataFrame(out_of_shelf.groupby(
            ['store_id', 'store_name', 'drug_id', 'drug_name', 'type', 'bucket',
             'drug_grade', 'max_set', 'mature_flag']).agg(
            {'oos_flag': ['sum', 'count'], 'oos_min_flag': ['sum', 'count'],
             'oos_std_qty_flag': ['sum', 'count'],
             'oos_sales_loss_30d': 'sum', 'sales_30d': 'sum'})).reset_index()
        out_of_shelf_group.columns = [
            'store_id', 'store_name', 'drug_id', 'drug_name', 'type', 'bucket',
            'drug_grade', 'max_set', 'mature_flag', 'oos_count', 'drug_count',
            'oos_min_count', 'oos_min_drug_count', 'oos_std_qty_count',
            'oos_std_qty_drug_count', 'oos_sales_loss_30d', 'sales_30d']

        # add customer segment info
        customer_segment = get_customer_segment(rs_db_read, read_schema, interval=90)
        out_of_shelf_group = out_of_shelf_group.merge(
            customer_segment, how='left', on=['store_id', 'drug_id'])
        out_of_shelf_group['customer_type'].fillna('Non-premium', inplace=True)

        # add min, safe-stock, max and current-inventory
        out_of_shelf_group = out_of_shelf_group.merge(
            out_of_shelf[["store_id", "drug_id", "as_active", "safety_stock",
                          "reorder_point", "order_upto_point", "quantity"]],
            on=["store_id", "drug_id"], how="left")
        out_of_shelf_group.rename(
            {"safety_stock": "min", "reorder_point": "safe-stock",
             "order_upto_point": "max", "quantity": "inventory_quantity"},
            axis=1, inplace=True)

        out_of_shelf_group['closing_date'] = run_date

        # OOS group store type grade level
        out_of_shelf_store_group = pd.DataFrame(out_of_shelf.groupby(
            ['store_id', 'store_name', 'type', 'bucket', 'max_set']).agg(
            {'oos_flag': ['sum', 'count'], 'oos_min_flag': ['sum', 'count'],
             'oos_std_qty_flag': ['sum', 'count'], 'oos_sales_loss_30d': 'sum',
             'sales_30d': 'sum'})).reset_index()
        out_of_shelf_store_group.columns = [
            'store_id', 'store_name', 'type', 'bucket', 'max_set', 'oos_count',
            'drug_count', 'oos_min_count', 'oos_min_drug_count',
            'oos_std_qty_count', 'oos_std_qty_drug_count',
            'oos_sales_loss_30d', 'sales_30d']

        out_of_shelf_store_group['closing_date'] = run_date

        # required format for RS write
        logger.info("Formatting table for RS-DB write")

        out_of_shelf_group.columns = [c.replace('_', '-') for c in
                                      out_of_shelf_group.columns]
        out_of_shelf_store_group.columns = [c.replace('_', '-') for c in
                                           out_of_shelf_store_group.columns]

        out_of_shelf_group['created-at'] = dt.datetime.now(
            tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
        out_of_shelf_group['created-by'] = 'etl-automation'
        out_of_shelf_group['updated-at'] = dt.datetime.now(
            tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
        out_of_shelf_group['updated-by'] = 'etl-automation'

        out_of_shelf_store_group['created-at'] = dt.datetime.now(
            tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
        out_of_shelf_store_group['created-by'] = 'etl-automation'
        out_of_shelf_store_group['updated-at'] = dt.datetime.now(
            tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
        out_of_shelf_store_group['updated-by'] = 'etl-automation'

        if debug_mode == 'N':
            logger.info("Writing table to RS-DB")
            logger.info("Writing to table: out-of-shelf-drug-level")
            table_info = helper.get_table_info(db=rs_db_write,
                                               table_name='out-of-shelf-drug-level',
                                               schema=write_schema)
            columns = list(table_info['column_name'])
            out_of_shelf_group = out_of_shelf_group[columns]  # required column order
            s3.write_df_to_db(df=out_of_shelf_group,
                              table_name='out-of-shelf-drug-level',
                              db=rs_db_write, schema=write_schema)

            logger.info("Writing to table: out-of-shelf-store-level")
            table_info = helper.get_table_info(db=rs_db_write,
                                               table_name='out-of-shelf-store-level',
                                               schema=write_schema)
            columns = list(table_info['column_name'])
            out_of_shelf_store_group = out_of_shelf_store_group[columns]  # required column order
            s3.write_df_to_db(df=out_of_shelf_store_group,
                              table_name='out-of-shelf-store-level',
                              db=rs_db_write, schema=write_schema)
            logger.info("Writing table to RS-DB completed!")

            logger.info("Writing table to Athena")
            logger.info("Writing to table: out-of-shelf-drug-level")
            athena.ingest_df_to_datalake(
                out_of_shelf_group,
                table_name=f"out_of_shelf_drug_level/{run_date.strftime('%Y-%m-%d')}")

            logger.info("Writing to table: out-of-shelf-store-level")
            athena.ingest_df_to_datalake(
                out_of_shelf_store_group,
                table_name=f"out_of_shelf_store_level/{run_date.strftime('%Y-%m-%d')}")
            logger.info("Writing table to Athena completed!")

            # logger.info("Deleting data from RS-DB older than 1year")
            # max_history_keep = run_date - date_util.relativedelta(months=12)
            # max_history_keep = max_history_keep.replace(day=1)
            # rs_db_write.execute(
            #     f"""
            #     delete from "{write_schema}"."out-of-shelf-drug-level"
            #     where "closing-date" < '{max_history_keep.strftime('%Y-%m-%d')}'
            #     """)
            # rs_db_write.execute(
            #     f"""
            #     delete from "{write_schema}"."out-of-shelf-store-level"
            #     where "closing-date" < '{max_history_keep.strftime('%Y-%m-%d')}'
            #     """)
            # logger.info("Deleting completed!")

        else:
            logger.info("All data writes skipped")

        # get metrics for email notification
        df_max_set = out_of_shelf_store_group.loc[
            out_of_shelf_store_group["max-set"] == 'Y']
        df_ethical = df_max_set.loc[df_max_set["type"] == 'ethical']
        df_generic = df_max_set.loc[df_max_set["type"] == 'generic']
        df_others = df_max_set.loc[df_max_set["type"] == 'others']
        store_count = len(df_max_set["store-id"].unique())
        oos_sys = round(
            (100 * df_max_set["oos-count"].sum() / df_max_set["drug-count"].sum()), 2)
        oos_ethical = round(
            (100 * df_ethical["oos-count"].sum() / df_ethical["drug-count"].sum()), 2)
        oos_generic = round(
            (100 * df_generic["oos-count"].sum() / df_generic["drug-count"].sum()), 2)
        oos_others = round(
            (100 * df_others["oos-count"].sum() / df_others["drug-count"].sum()), 2)

        status = 'Success'
        logger.info(f"OOS code execution status: {status}")

    except Exception as error:
        logger.exception(error)
        logger.info(f"OOS code execution status: {status}")

    return status, sanity_check, run_date, store_count, oos_sys, oos_ethical, \
           oos_generic, oos_others


def get_stores(exclude_stores, db, schema):
    if not exclude_stores:
        exclude_stores = "(0)"
    else:
        exclude_stores = tuple(exclude_stores)
    q_store = """
    select id
    from "{schema}".stores
    where name <> 'Zippin Central'
    and name <> 'Marketing'
    and "is-active" = 1
    and "opened-at" != '0101-01-01 00:00:00'
    and id not in {exclude_stores}
    """.format(schema=schema, exclude_stores=exclude_stores)
    df_stores = db.get_df(q_store)

    return df_stores


def get_inventory(store_id, db, schema):
    q_inventory = """
    select "store-id" , s.name as "store-name", "drug-id" , 
        sum(quantity+"locked-quantity"+"locked-for-audit"+
        "locked-for-check") as quantity,
        sum(quantity+"locked-quantity"+"locked-for-audit"+
        "locked-for-check"+"locked-for-transfer"+"locked-for-return")
        as "total-system-quantity"
    from "{schema}"."inventory-1" i 
    left join "{schema}".stores s
    on i."store-id" = s.id
    where "store-id" = {0}
    group by "store-id" , s.name, "drug-id" 
    """.format(store_id, schema=schema)
    df_inventory = db.get_df(q_inventory)
    df_inventory.columns = [c.replace('-', '_') for c in df_inventory.columns]

    return df_inventory


def get_past_30d_sales(store_id, db, run_date, schema):
    start_date = run_date - dt.timedelta(days=30)
    end_date = run_date
    q_sales = """
    select "drug-id", sum("revenue-value") as "gross-sales-val"
    from "{schema}".sales s 
    where "store-id" = {0}
    and "bill-flag" = 'gross'
    and date("created-at") between '{1}' and '{2}'
    group by "drug-id" 
    """.format(store_id, start_date.strftime("%Y-%m-%d"),
               end_date.strftime("%Y-%m-%d"), schema=schema)
    df_30d_sales = db.get_df(q_sales)
    df_30d_sales.columns = [c.replace('-', '_') for c in df_30d_sales.columns]
    df_30d_sales = df_30d_sales.dropna()
    df_30d_sales["drug_id"] = df_30d_sales["drug_id"].astype(int)

    return df_30d_sales


def get_std_qty(db, schema):
    q_std_qty = f"""
    select "drug-id" , "std-qty" 
    from "{schema}"."drug-std-info" dsi 
    """
    df_drug_std_qty = db.get_df(q_std_qty)
    df_drug_std_qty.columns = [c.replace('-', '_') for c in df_drug_std_qty.columns]

    return df_drug_std_qty


def get_buckets(store_id, db, schema):
    q_latest_buckets = f"""
    select "store-id" , "drug-id" , bucket 
    from "{schema}"."ipc2-segmentation" is2 
    where "store-id" = {store_id}
    and "reset-date" = (select max("reset-date") 
        from "{schema}"."ipc2-segmentation" where "store-id" = {store_id})
    """
    df_latest_buckets = db.get_df(q_latest_buckets)
    df_latest_buckets['bucket'] = np.where(df_latest_buckets['bucket'] == '',
                                           'NA', df_latest_buckets['bucket'])
    df_latest_buckets.columns = [c.replace('-', '_') for c in
                                 df_latest_buckets.columns]

    return df_latest_buckets


def get_customer_segment(db, schema, interval=90):
    q_customer_seg = """
    select distinct "store-id" , "drug-id" , seg."segment-calculation-date" , 
	    case 
	    when seg."value-segment" in ('platinum', 'gold', 'silver') then 'Premium'
	    else 'Non-premium'
	    end as "customer-type"
    from "{schema}".sales s
    left join (
    select "patient-id" , "segment-calculation-date", "value-segment"
    from "{schema}"."customer-value-segment"
    where "segment-calculation-date" = (select max("segment-calculation-date") 
            from "{schema}"."customer-value-segment")
    ) as seg on s."patient-id" = seg."patient-id" 
    where DATEDIFF(day, date(s."created-at"), current_date) <= {0}
    and "customer-type" = 'Premium' 
    order by "store-id" , "drug-id"
    """.format(interval, schema=schema)
    df_customer_seg = db.get_df(q_customer_seg)
    df_customer_seg.columns = [c.replace('-', '_') for c in
                               df_customer_seg.columns]

    return df_customer_seg


def get_drug_list(store_id, db, schema, max_set='Y', drugs=None):
    if max_set == 'Y':
        max_condition = "max > 0"
        drugs_condition = ""
    elif max_set == 'N' and drugs != []:
        max_condition = "max = 0"
        drugs_condition = """and "drug-id" in {0}""".format(
            str(drugs).replace('[', '(').replace(']', ')'))
    else:
        max_condition = "max = 0"
        drugs_condition = """and "drug-id" in (0)"""

    # getting max from drug-order-info
    doi_query = """
    select "store-id", "drug-id", "drug-name", type, category, "drug-grade",
    min, doi."safe-stock", max, "as-active"
    from "{schema}"."drug-order-info" doi
    join "{schema}".drugs d on d.id = doi."drug-id"
    where {1} and d.type not in ('discontinued-products', 'banned')
    and "store-id" = {0}
    {2}
    """.format(store_id, max_condition, drugs_condition,
               schema=schema)
    df_doi = db.get_df(doi_query)
    df_doi.columns = [c.replace('-', '_') for c in df_doi.columns]
    df_doi.columns = ['store_id', 'drug_id', 'drug_name', 'type', 'category',
                   'drug_grade', 'safety_stock', 'reorder_point',
                   'order_upto_point', 'as_active']

    return df_doi


def mature_drugs_flag(store_id, run_date, mature_delta_start_date,
                      mature_delta_days, db, schema):
    q_mature_days = """
            select "store-id" , "drug-id" , sum("drug-count") as mature_days
            from "{schema}"."out-of-shelf-drug-level" oosdl 
            where "closing-date" < '{0}'
            and "closing-date" >= '{1}'
            and "max-set" = 'Y' 
            and "store-id" = {2}
            group by "store-id" , "drug-id" 
            """.format(run_date.strftime("%Y-%m-%d"),
                       mature_delta_start_date.strftime("%Y-%m-%d"),
                       store_id, schema=schema)
    df_mature_flag = db.get_df(q_mature_days)
    df_mature_flag.columns = [c.replace('-', '_') for c in df_mature_flag.columns]
    df_mature_flag["mature_flag"] = np.where(
        df_mature_flag["mature_days"] == mature_delta_days, 'Y', 'N')
    df_mature_flag.drop("mature_days", axis=1, inplace=True)

    return df_mature_flag


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="This is ETL script.")
    parser.add_argument('-e', '--env', default="dev", type=str, required=False)
    parser.add_argument('-d', '--debug_mode', default="Y", type=str,
                        required=False)
    parser.add_argument('-et', '--email_to',
                        default="vivek.revi@zeno.health", type=str,
                        required=False)
    parser.add_argument('-exlist', '--as_inact_ex_types',
                        default="generic,others", type=str,
                        required=True)
    parser.add_argument('-mdd', '--mature_delta_days',
                        default=7, type=int, required=False)
    parser.add_argument('-exs', '--exclude_stores',
                        default="52,60,92,243,281", type=str,
                        required=True)
    args, unknown = parser.parse_known_args()

    env = args.env
    os.environ['env'] = env
    debug_mode = args.debug_mode
    email_to = args.email_to
    as_inactive_exclude_types = args.as_inact_ex_types.replace(" ", "").split(",")
    mature_delta_days = args.mature_delta_days
    exclude_stores = args.exclude_stores.replace(" ", "").split(",")

    # ensure input is correct
    if not all([i in ['generic', 'ethical', 'others'] for i in
                as_inactive_exclude_types]):
        as_inactive_exclude_types = ['generic', 'others']  # default types

    #convert string store_ids to int
    exclude_stores = [int(i) for i in exclude_stores]

    read_schema = 'prod2-generico'
    write_schema = 'prod2-generico'
    logger = get_logger()
    rs_db_read = DB()
    rs_db_write = DB(read_only=False)

    # open RS connection
    rs_db_read.open_connection()
    rs_db_write.open_connection()

    """ calling the main function """
    status, sanity_check, run_date, store_count, oos_sys, oos_ethical, \
    oos_generic, oos_others = main(
        debug_mode, as_inactive_exclude_types, mature_delta_days, exclude_stores,
        rs_db_read, rs_db_write, read_schema, write_schema, logger)

    # close RS connection
    rs_db_read.close_connection()
    rs_db_write.close_connection()

    # SEND EMAIL ATTACHMENTS
    logger.info("Sending email attachments..")
    email = Email()
    email.send_email_file(
        subject=f"OOS Job (GLUE-{env}) {run_date}: {status}",
        mail_body=f"""
                    Sanity Check: {sanity_check}
                    Debug Mode: {debug_mode}
                    Job Params: {args}

                    ===SYSTEM LEVEL===
                    TOTAL   : {oos_sys}%
                    GENERIC : {oos_generic}%
                    ETHICAL : {oos_ethical}%
                    OTHERS  : {oos_others}% 
                    STORES  : {store_count}
                    (flags: max_set='Y', mature_flag='All')
                    """,
        to_emails=email_to)

    logger.info("Script ended")
