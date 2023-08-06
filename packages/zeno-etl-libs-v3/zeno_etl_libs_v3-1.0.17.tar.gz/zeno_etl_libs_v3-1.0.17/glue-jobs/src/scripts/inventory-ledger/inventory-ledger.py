"""
Owner: kuldeep.singh@zeno.health
Purpose: This script calculates the movement(all reasons) of inventory, for all the stores, between two dates.
"""
import argparse
import datetime
import os
import sys

sys.path.append('../../../..')

from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.db.db import DB
from zeno_etl_libs.utils.inventory.inventory import Data
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.helper import helper

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False,
                    help="This is env(dev, stage, prod)")
parser.add_argument('-sd', '--start_date', default="NA", type=str, required=False,
                    help="Start date in IST")
parser.add_argument('-ed', '--end_date', default="NA", type=str, required=False,
                    help="End date in IST")
parser.add_argument('-bs', '--batch_size', default=1, type=int, required=False,
                    help="How many stores to process in one go")
parser.add_argument('-fr', '--is_full_run', default="NO", type=str, required=False,
                    help="Only one batch or all to process")

args, unknown = parser.parse_known_args()
env = args.env
start_date = args.start_date
end_date = args.end_date
batch_size = args.batch_size
is_full_run = args.is_full_run

os.environ['env'] = env
logger = get_logger()

write_schema = "prod2-generico" if env == 'prod' else 'test-generico'

""" read connection """
db = DB()
db.open_connection()

""" write connection """
w_db = DB(read_only=False)
w_db.open_connection()

s3 = S3(bucket_name=f"{env}-zeno-s3-db")

if not (start_date and end_date) or start_date == "NA" or end_date == "NA":
    """ if no dates given, then run for yesterday """
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    start_date = datetime.datetime.now() + datetime.timedelta(days=-1)
    start_date = start_date.strftime("%Y-%m-%d")

"""
Instructions to use(README):
    0. Make sure tables for both the dates (start and end) are present in public schema (eg: bills-1-mis-2022-06-11)
    1. set the start date and end date
    2. Set the store id if only one store changes are required, if all stores are required then don't set store id
    3. Data is uploaded to s3(prod-zeno-s3-db) inside "inventory/ledger/" folder (eg: s3://dev-zeno-s3-db/inventory/ledger/2022/06/11/240.csv)
    4. S3 Data can be queried using AWS Athena

Tables Required:
    inventory-1,invoice-items-1,invoices-1,customer-return-items-1,customer-returns-1,stock-transfer-items-1,
    stock-transfers-1,bill-items-1,bills-1,return-items-1,returns-to-dc-1,deleted-invoices,deleted-invoices-1,
    inventory-changes-1 

Improvements:
    1. use parquet format to store the data
        import pandas as pd
        df = pd.read_csv('example.csv')
        df.to_parquet('output.parquet')

Meaning of columns:
    "o": Opening/Start
    "cr": Customer Return
    "xin": Stock transfer in
    "xout": Stock transfer out
    "sold": Sold to customer
    "ret": Return to DC
    "ar": Audit
    "rr": Reverted Return 
    "del": Invoice Deleted
    "c": closing 
"""

""" get all the stores """
q = f"""
    select
        distinct "store-id" as "store-id"
    from
        "prod2-generico"."inventory-1" i
"""
stores = db.get_df(query=q)

""" this column order will be maintained across all csv files """
column_order = ["id", "barcode", "ptr", "o", "cr", "xin", "cin", "xout", "cout", "sold", "ret",
                "ar", "rr", "del", "c", "e"]

""" clean existing records, if any """
q = f"""
    delete from "{write_schema}"."inventory-ledger" where date("start-time") = '{start_date}'; 
"""
w_db.execute(query=q)

batch = 0
for store_id_batch in helper.batch(stores['store-id'], batch_size):
    csv_store_ids = ','.join([str(s) for s in store_id_batch])
    batch += 1
    logger.info(f"batch: {batch}, csv store ids: {csv_store_ids}")

    data = Data(db=db, csv_store_ids=csv_store_ids, start_date=start_date, end_date=end_date)
    recon_df = data.concat()

    uri = s3.save_df_to_s3(df=recon_df[column_order],
                           file_name=f"inventory/ledger/{start_date.replace('-', '/')}/batch_{batch}.csv",
                           index=False)
    table_info = helper.get_table_info(db=w_db, table_name="inventory-ledger", schema=write_schema)

    recon_df['start-time'] = data.start_ts
    recon_df['end-time'] = data.end_ts
    recon_df['created-at'] = datetime.datetime.now()
    recon_df['updated-at'] = datetime.datetime.now()
    recon_df['created-by'] = "etl-automation"
    recon_df['updated-by'] = "etl-automation"

    s3.write_df_to_db(df=recon_df[table_info['column_name']], table_name="inventory-ledger",
                      db=w_db, schema=write_schema)

    logger.info(f"Uploaded successfully @ {uri}")

    if is_full_run.lower() == "no":
        logger.info(f"Stopping after one batch, since is_full_run: {is_full_run}")
        db.close_connection()
        w_db.close_connection()
        break

db.close_connection()
w_db.close_connection()
