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
    parser.add_argument('-et', '--email_to', default="vivek.sidagam@zeno.health,akshay.bhutada@zeno.health",
                        type=str, required=False)
    parser.add_argument('-sd', '--start_date', default='NA', type=str, required=False)
    parser.add_argument('-ed', '--end_date', default='NA', type=str, required=False)
    args, unknown = parser.parse_known_args()
    env = args.env
    os.environ['env'] = env
    email_to = args.email_to
    start_date = args.start_date
    end_date = args.end_date

    err_msg = ''

    logger = get_logger()
    logger.info("Script begins")


    cur_date = datetime.datetime.now(tz=gettz('Asia/Kolkata')).date()

    d = datetime.timedelta(days=15)

    start_dt = cur_date - d

    end_dt = cur_date - datetime.timedelta(1)
    status = False

    if start_date == 'NA' and end_date == 'NA':
        start_date = start_dt
        end_date = end_dt


    try:
        # MSSql connection
        mssql = MSSql(connect_via_tunnel=False)
        mssql_connection = mssql.open_connection()
        # RS Connection
        rs_db = DB()
        rs_db.open_connection()
        q1 = """
                select
        'bhiwandi-warehouse' as source,
        cast(b.Barcode as int) as drug_id,
        cast(a.Vdt as date) as purchase_date,
        c.Altercode as distributor_id,
        a.Qty as quantity,
        f.mrp as mrp,
        (a.NetAmt + a.Taxamt)/ qty as purchase_rate,
        cast(a.Vno as varchar) + cast('-' as varchar) + cast(a.Itemc as varchar) + cast('-' as varchar) + cast(a.Psrlno as varchar) as id,
        199 as store_id
        from
        SalePurchase2 a
        left join Item b on
        b.code = a.Itemc
        left join acm c on
        c.code = a.Acno
        left join Master m on
        m.code = b.ItemCat
        left join FIFO f on 
            (f.Pbillno = a.Pbillno
            and f.Psrlno = a.Psrlno
            and f.Itemc = a.Itemc
            and f.Vdt = a.Vdt)
        where
        b.Barcode not like '%[^0-9]%'
        and c.Altercode not like '%[^0-9]%'
        and a.Vtype in (N'PB')
        and a.Qty > 0
        and  a.vdt >= '{}'  and  a.vdt <= '{}'
        """.format(start_date,end_date)

        logger.info("getting data from WMS tables")
        bhiwandi_wh_purchase = pd.read_sql(q1, mssql_connection)
        logger.info("Data pulled from WMS tables")

        mssql = MSSql(connect_via_tunnel=False, db='Esdata_WS_2')

        cnxn = mssql.open_connection()

        cursor = cnxn.cursor()
        q_2='''
            select
        'goodaid-warehouse' as source,
        cast(b.Barcode as int) as drug_id,
        cast(a.Vdt as date) as purchase_date,
        c.Altercode as distributor_id,
        a.Qty as quantity,
        f.mrp as mrp,
        (a.NetAmt + a.Taxamt)/ qty as purchase_rate,
        cast(a.Vno as varchar) + cast('-' as varchar) + cast(a.Itemc as varchar) + cast('-' as varchar) + cast(a.Psrlno as varchar) as id,
        343 as store_id
        from
        SalePurchase2 a
        left join Item b on
        b.code = a.Itemc
        left join acm c on
        c.code = a.Acno
        left join Master m on
        m.code = b.ItemCat
        left join FIFO f on 
            (f.Pbillno = a.Pbillno
            and f.Psrlno = a.Psrlno
            and f.Itemc = a.Itemc
            and f.Vdt = a.Vdt)
        where
        b.Barcode not like '%[^0-9]%'
        and c.Altercode not like '%[^0-9]%'
        and a.Vtype in (N'PB')
        and a.Qty > 0
        and  a.vdt >= '{}'  and a.vdt <= '{}'
        '''.format(start_date,end_date)

        goodaid_warehouse_purchase = pd.read_sql(q_2, cnxn)

        q3 = """
            select
                'dc' as source,
                ii."drug-id" as drug_id,
                date(i."approved-at") as purchase_date,
                cast(i."distributor-id" as varchar) as distributor_id,
                ii."actual-quantity" as quantity,
                ii.mrp,
                (ii."net-value" / ii."actual-quantity") as purchase_rate,
                cast(ii.id as varchar) as id,
                i."store-id" as store_id
            from
                "prod2-generico".invoices i
            left join "prod2-generico"."invoice-items" ii on
                ii."invoice-id" = i.id
            where
             "distributor-id" <> 8105
                and ii."drug-id" is not null and  date(i."approved-at") >='{}' and 
                date(i."approved-at") <='{}'
        """.format(start_date,end_date)
        logger.info("Getting data from RS")
        dc = rs_db.get_df(q3)
        logger.info("Data pulled from RS")

        drugs = rs_db.get_df("""  
            select
                drg.id as drug_id,
                drg."drug-name" as drug_name,
                drg."type",
                drg.company,
                drg.category,
                drg."available-in" as available_in,
                drg."sub-type" as sub_type,
                drg."category-drug-type" as category_drug_type
            from
                "prod2-generico".drugs drg
        """)

        stores = rs_db.get_df("""
            select
                sm.id as store_id,
                sm.store as store_name,
                sm.city as city_name,
                sm."franchisee-name" as franchisee_name,
                sm."opened-at" as store_opened_at
            from
                "prod2-generico"."stores-master" sm
        """)

        distributors = rs_db.get_df("""
            select
                id as distributor_id,
                d."name" as distributor_name
            from
                "prod2-generico".distributors d
        """)

        df = pd.concat([dc, bhiwandi_wh_purchase,goodaid_warehouse_purchase])

        df = df.merge(drugs, on='drug_id', how='left')
        df = df.merge(stores, on='store_id', how='left')
        df['distributor_id'] = np.where(df['distributor_id'] == '', 0, df['distributor_id'])
        df['distributor_id'] = df['distributor_id'].astype(int)
        df = df.merge(distributors, on='distributor_id', how='left')

        created_at = datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")
        df['created-at'] = created_at
        df['created-by'] = 'etl-automation'
        df['updated-at'] = created_at
        df['updated-by'] = 'etl-automation'

        df['quantity'] = df['quantity'].astype(int)

        #writing to RS
        delete_q = """
                DELETE
                FROM
                    "prod2-generico"."purchase-margin"
                WHERE
                    date("created_at") >= '{start_date_n}'
                    and date("created_at") <= '{end_date_n}'
            """.format(start_date_n=start_date, end_date_n=end_date)

        rs_db.execute(delete_q)
        s3 = S3()
        delete_one_year='''
          DELETE
                FROM
                    "prod2-generico"."purchase-margin"
                WHERE
                    date("created_at") < date_trunc('month', current_date) - INTERVAL '1 year'      
        '''
        s3.write_df_to_db(df=df, table_name='purchase-margin', db=rs_db, schema='prod2-generico')

        rs_db.execute(delete_one_year)

        status = True

    except Exception as e:
        err_msg = str(e)
        logger.info('purchase_margin job failed')
        logger.exception(e)

    # Sending email
    email = Email()
    if status:
        result = 'Success'
        email.send_email_file(subject=f"purchase_margin ({env}): {result}",
                              mail_body=f"Run time: {cur_date}",
                              to_emails=email_to, file_uris=[])
    else:
        result = 'Failed'
        email.send_email_file(subject=f"purchase_margin ({env}): {result}",
                              mail_body=f"Run time: {cur_date}  {err_msg}",
                              to_emails=email_to, file_uris=[])

    logger.info("Script ended")

#DDL for table
"""
create table "prod2-generico"."purchase-margin" ( "source" text,
	"drug_id" int,
	"created_at" date,
	"distributor_id" int,
	"quantity" int,
	"mrp" float,
	"purchase_rate" float,
	"id" text,
	"store_id" int,
	"drug_name" text,
	"type" text,
	"company" text,
	"category" text,
	"available_in" text,
	"sub_type" text,
	"category_drug_type" text,
	"store_name" text,
	"city_name" text,
	"franchisee_name" text,
	"store_opened_at" date,
	"distributor_name" text,
	"created-at" TIMESTAMP without TIME zone default getdate(),
	"created-by" VARCHAR default 'etl-automation',
	"updated-at" TIMESTAMP without TIME zone default getdate(),
	"updated-by" VARCHAR default 'etl-automation'
);

alter table "prod2-generico"."purchase-margin" owner to admin;
"""
