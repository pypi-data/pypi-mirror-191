
import sys
import argparse
import os
import pandas as pd
import numpy as np
sys.path.append('../../../..')
# sys.path.insert(0,'/Users/tusharuike/ETL')

from dateutil.tz import gettz
from zeno_etl_libs.helper.aws.s3 import S3 as S3
from zeno_etl_libs.helper.email.email import Email as Email
from zeno_etl_libs.db.db import DB,MySQL
from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper import helper as helper
from zeno_etl_libs.db.db import MSSql
import datetime as datetime

def main(debug_mode, stores, db, rs_db_write, read_schema, write_schema, logger, s3):

    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib import dates
    import datetime as datetime
    from dateutil.relativedelta import relativedelta
    

    todays_date = datetime.date.today() - relativedelta(days = 1)
    start_d = todays_date 
    end_d = start_d
    start_d = str(start_d)
    end_d = str(end_d)
    print(start_d, end_d)
    df_transactions_final = pd.DataFrame()

    stores = [2,16,19,20,23,26,28,31,45,51,54,63,115,134,144,146,154,184,193,218,223,229,234,244,260]
    logger.info("Running script for store ids: {}".format(stores))
    # stores = [2,16]
    try: 
        for i in stores:
            logger.info("Running script for store id: {}".format(i))
            logger.info("Fetching purchase qty - IN")

        #purchase qty - IN 
            df_1='''
            select
                b."store-id" ,
                a."drug-id" ,
                date(b."received-at") as "date",
                i."distributor-id",
                round(coalesce(sum(a."actual-quantity"), 0)) "purchase_quantity"
            from
                "prod2-generico"."prod2-generico"."invoice-items-1" a
            join "prod2-generico"."prod2-generico"."invoices-1" b on
                a."franchisee-invoice-id" = b.id
            left join "prod2-generico"."prod2-generico".invoices i on
             	i.id = a."invoice-id"            
            where
                date(b."received-at") BETWEEN '{start_d}' and '{end_d}'
                and b."store-id" = {store_id} and a."actual-quantity" !=0
            GROUP By
                b."store-id" ,
                a."drug-id" ,
                date(b."received-at"),
                i."distributor-id" 
            '''.format(store_id=i, start_d= start_d, end_d = end_d, read_schema= read_schema)

            df_1=rs_db.get_df(query=df_1)
            df_1.columns = [c.replace('-', '_') for c in df_1.columns]
            # df_1['from'] = 'WH'
            df_1['type'] = 'IN'
            df_1.rename(columns={'purchase_quantity':'quantity','distributor_id':'from'},inplace=True)

            logger.info("Fetching customer return - IN")

        #customer return - IN
            df_2='''
            select
                s."store-id" ,
                s."drug-id" ,
                date(s."created-at") as "date",
                SUM(s.quantity) as "customer-return"
            from
                "{read_schema}".sales s
            where
                date(s."created-at")>=  '{start_d}' 
                and date(s."created-at")<=  '{end_d}'
                and s."bill-flag" = 'return' and s."store-id"={store_id}
            group by
                s."store-id" ,
                s."drug-id" ,
                date(s."created-at")
            '''.format(store_id=i, start_d= start_d, end_d = end_d, read_schema= read_schema)

            df_2=rs_db.get_df(query=df_2)
            df_2.columns = [c.replace('-', '_') for c in df_2.columns]
            df_2['from'] = 9999
            df_2['type'] = 'return'
            df_2.rename(columns={'customer_return':'quantity'},inplace=True)

            logger.info("Fetching return to DC - OUT")
        #return_to_DC -WH -- OUT 

            df_3='''
                select
                    b."store-id",
                    c."drug-id",
                    date(b."created-at") as "date" ,
                    coalesce(sum(a."returned-quantity"), 0) "returned-to-dc",
                    coalesce(a."return-dc-id",0) as "return-dc-id"
                from
                    "{read_schema}"."return-items-1" a
                join "{read_schema}"."returns-to-dc-1" b on
                    a."return-id" = b.id
                join "{read_schema}"."inventory-1" c on
                    a."inventory-id" = c.id
                LEFT JOIN "{read_schema}"."debit-note-items-1" dni 
                ON
                    a.id = dni."item-id"
                    AND dni."is-active" != 0
                LEFT JOIN "{read_schema}"."debit-notes-1" dn
                ON
                    dni."debit-note-id" = dn.id
                where
                    date(b."created-at") BETWEEN '{start_d}' and '{end_d}'
                    and b."store-id" = {store_id}
                    and (dn."is-internal-debit-note" = 0 or dn."is-internal-debit-note" is null)
                GROUP BY
                    b."store-id",
                    c."drug-id" ,
                    a."return-dc-id",
                    date(b."created-at")
            '''.format(store_id=i, start_d= start_d, end_d = end_d, read_schema= read_schema)

            df_3=rs_db.get_df(query=df_3)

            df_3.columns = [c.replace('-', '_') for c in df_3.columns]
            # df_3['from'] = 'DC'
            df_3['type'] = 'OUT'
            df_3.rename(columns={'returned_to_dc':'quantity','store_id':'from','return-dc-id':'store_id'},inplace=True)

            logger.info("Fetching gross sales - OUT")
        #gross sales - OUT 

            df_4='''     
            select
                s."store-id" ,
                s."drug-id" ,
                date(s."created-at") as "date",
                SUM(s.quantity) as "sold"
            from
                "{read_schema}".sales s
            where
                date(s."created-at")>= '{start_d}'
                and date(s."created-at")<= '{end_d}'
                and s."bill-flag" = 'gross' and s."store-id"={store_id}
            group by
                s."store-id" ,
                s."drug-id" ,
                date(s."created-at")
            '''.format(store_id=i, start_d= start_d, end_d = end_d, read_schema= read_schema)

            df_4=rs_db.get_df(query=df_4)

            df_4.columns = [c.replace('-', '_') for c in df_4.columns]
            df_4['type'] = 'OUT'
            df_4.rename(columns={'sold':'quantity','store_id':'from'},inplace=True)
            df_4['store_id'] = 9999
            
            logger.info("Fetching reverted items from DC - IN")
        #reverted - IN

            df_5='''
                            
                select
                b."store-id" ,
                c."drug-id" ,
                date(a."reverted-at") as "date",
                coalesce (sum(a."returned-quantity"),
                0) "reverted",
                coalesce(a."return-dc-id",0) as "return-dc-id"
            from
                "{read_schema}"."return-items-1" a
            join "{read_schema}"."returns-to-dc-1" b on
                a."return-id" = b.id
            join "{read_schema}"."inventory-1" c on
                a."inventory-id" = c.id
            LEFT JOIN "{read_schema}"."debit-note-items-1" dni 
            ON
                a.id = dni."item-id"
                AND dni."is-active" != 0
            LEFT JOIN "{read_schema}"."debit-notes-1" dn
            ON
                dni."debit-note-id" = dn.id
            where
                date(a."reverted-at") BETWEEN '{start_d}' and '{end_d}'
                and b."store-id" = {store_id}
                and (dn."is-internal-debit-note" = 0 or dn."is-internal-debit-note" is null)
            GROUP By
                b."store-id",
                c."drug-id" ,
                a."return-dc-id",
                date(a."reverted-at")
            '''.format(store_id=i, start_d= start_d, end_d = end_d, read_schema= read_schema)

            df_5=rs_db.get_df(query=df_5)

            df_5.columns = [c.replace('-', '_') for c in df_5.columns]
            # df_5['from'] = 'reverted'
            df_5['type'] = 'IN'
            df_5.rename(columns={'reverted':'quantity','return_dc_id':'from'},inplace=True)

            logger.info("Fetching transferred items - IN")
        # tranfer - IN 

            df_6='''
            
                
            select
                t."store-id",
                t."drug-id" ,
                t."transfer-in-date" as "date",
                t."source-store",
                sum(t.transferred)  as "transferred_in"
            from
                (
            select
                    c."store-id",
                    c."drug-id" ,
                    b."source-store",
                    date(b."received-at") as "transfer-in-date",
                sum(a.quantity) "transferred"
            from
                    "{read_schema}"."stock-transfer-items-1" a
            join "{read_schema}"."stock-transfers-1" b on
                    a."transfer-id" = b.id
            join "{read_schema}"."inventory-1" c on
                    (a."inventory-id" = c.id)
            where
                    b."destination-store" = c."store-id"
                and date(b."received-at") BETWEEN '{start_d}' and '{end_d}'
                and c."store-id"={store_id}
            GROUP BY
                c."store-id",c."drug-id",b."source-store"  ,date(b."received-at")
            union
            select
                c."store-id",
                c."drug-id" ,
                b."source-store",
                date(b."received-at") as "transfer-in-date" ,
                sum(a.quantity) "transferred"
            from
                "{read_schema}"."stock-transfer-items-1" a
            join "{read_schema}"."stock-transfers-1" b on
                a."transfer-id" = b.id
            join "{read_schema}"."inventory-1" c on
                (a."inventory-id" = c."barcode-reference")
            where
                b."destination-store" = c."store-id"
                and date(b."received-at") BETWEEN '{start_d}' and '{end_d}'
                and c."store-id"={store_id}
            GROUp BY
                c."store-id",
                c."drug-id" ,
                b."source-store",
                date(b."received-at")
                        ) t
                GROUP BY t."store-id",
                t."source-store",
                t."drug-id" ,
                t."transfer-in-date"
            '''.format(store_id=i, start_d= start_d, end_d = end_d, read_schema= read_schema)

            df_6=rs_db.get_df(query=df_6)

            df_6.columns = [c.replace('-', '_') for c in df_6.columns]
            df_6.rename(columns={'source_store':'from'},inplace=True)
            df_6['from'] = df_6['from'].astype(str)
            df_6['type'] = 'IN'
            df_6.rename(columns={'transferred_in':'quantity'},inplace=True)
            
            logger.info("Fetching transferred items - OUT")
        #tranfer out - OUT 

            df_7='''
            
                
                select
                t."store-id",
                t."destination-store",
                t."drug-id" ,
                t."transfer-out-date" as "date",
                sum(t.transferred) transferred_out
            from
                (
            select
                    c."store-id",
                    c."drug-id" ,
                    b."destination-store" ,
                    date(a."transferred-at") as "transfer-out-date",
                    sum(a.quantity) "transferred"
                from
                    "{read_schema}"."stock-transfer-items-1" a
                join "{read_schema}"."stock-transfers-1" b on
                    a."transfer-id" = b.id
                join "{read_schema}"."inventory-1" c on
                    (a."inventory-id" = c.id )
                where
                    b."source-store" = c."store-id"
                    and
                date(a."transferred-at") BETWEEN '{start_d}' and '{end_d}'
                and c."store-id"={store_id}
                GROUP BY
                    c."store-id",b."destination-store",c."drug-id",date(a."transferred-at") 
            union	
            select
                    c."store-id",
                    b."destination-store",
                    c."drug-id" ,
                    date(a."transferred-at"),
                    sum(a.quantity) "transferred"
            from
                    "{read_schema}"."stock-transfer-items-1" a
            join "{read_schema}"."stock-transfers-1" b on
                    a."transfer-id" = b.id
            join "{read_schema}"."inventory-1" c on
                    (a."inventory-id" = c."barcode-reference" )
            where
                    b."source-store" = c."store-id"
                and
            date(a."transferred-at") BETWEEN '{start_d}' and '{end_d}'
            and c."store-id"={store_id}
            GROUP BY
                    c."store-id",b."destination-store",c."drug-id" ,date(a."transferred-at")
                ) t
            GROUP BY
                t."store-id",
                t."destination-store",
                t."drug-id" ,
                t."transfer-out-date"
            '''.format(store_id=i, start_d= start_d, end_d = end_d, read_schema= read_schema)

            df_7=rs_db.get_df(query=df_7)

            df_7.columns = [c.replace('-', '_') for c in df_7.columns]
            df_7.rename(columns={'store_id':'from'},inplace=True)
            df_7.rename(columns={'destination_store':'store_id'},inplace=True)
            # df_7['from'] = df_7['store_id'].astype(str)
            df_7['type'] = 'OUT'
            df_7.rename(columns={'transferred_out':'quantity'},inplace=True)

            df_transactions = pd.concat([df_1,df_2,df_3,df_4,df_5,df_6,df_7])
            df_transactions.rename(columns={'type':'trans_type','from':'from_location','store_id':'to_location','drug_id':'sku'},inplace=True)
            df_transactions['date'] = pd.to_datetime(df_transactions['date'])
            df_transactions['reported_year'] = df_transactions['date'].dt.year
            df_transactions['reported_month'] = df_transactions['date'].dt.month
            df_transactions['reported_day'] = df_transactions['date'].dt.day
            df_transactions.drop(columns=['date'],inplace=True)
            df_transactions['adjust'] = ''
            df_transactions = df_transactions[['trans_type','from_location','to_location','sku','quantity','reported_year','reported_month','reported_day','adjust']]

            df_transactions_final = pd.concat([df_transactions_final,df_transactions])

        # df_transactions_final.columns = ['TransType','FromLocation','ToLocation','Sku','Quantity','RptYr','RptMth','RptDay',    'Adjust']
        #2nd file - SKU status


        todays_date = datetime.date.today() - relativedelta(days = 1)
        start_d = todays_date - relativedelta(months = 6)
        end_d = todays_date
        start_d = str(start_d)
        end_d = str(end_d)
        print(start_d, end_d)


        store_sku = f'''

        select "store-id" as stock_location, "drug-id" as sku, sum("net-quantity") from "{read_schema}".sales s 
        where "created-date" >= '{start_d}' and "created-at" <= '{end_d}' and "store-id" in {tuple(stores)}
        group by "store-id", "drug-id"  

        '''

        curr_inv = f''' 
                    select "store-id" as stock_location, "drug-id" as sku, sum("locked-quantity") as inv_on_way, sum(quantity+
                        "locked-for-audit"+"locked-for-check"
                       ) as curr_inventory
                    from "{read_schema}"."inventory-1" i 
                    where "store-id" in {tuple(stores)}
                    group by "store-id", "drug-id"  

        '''

        df_store_sku=rs_db.get_df(query=store_sku)
        df_curr_inv=rs_db.get_df(query=curr_inv)


        df_store_sku.columns = [c.replace('-', '_') for c in df_store_sku.columns]
        df_curr_inv.columns = [c.replace('-', '_') for c in df_curr_inv.columns]


        df_status = pd.merge(df_store_sku, df_curr_inv, how='left', on = ['stock_location','sku'])


        df_status.rename(columns={'stock_location':'stock_location_code','sku':'sku_name', 'inv_on_way':'inv_on_the_way', 'curr_inventory':'inv_at_hand' }, inplace=True)
        df_status.drop(columns=['sum'],inplace=True)


        df_status['reported_year'] = todays_date.year
        df_status['reported_month'] = todays_date.month
        df_status['reported_day'] = todays_date.day

        #location masters file
        # loc_master = '''select id as stock_location, store as store_description, "store-type", city  from "prod2-generico"."prod2-generico"."stores-master" sm 
        # where city like '%MUM' '''

        # df_loc_master = rs_db.get_df(query=loc_master)
        # df_loc_master.columns = [c.replace('-', '_') for c in df_loc_master.columns]
        # df_loc_master['reported_year'] = todays_date.year
        # df_loc_master['reported_month'] = todays_date.month
        # df_loc_master['reported_day'] = todays_date.day
        # df_loc_master['updated-at'] = datetime.datetime.now(
        #     tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
        # df_loc_master.columns = [c.replace('_', '-') for c in
        #                         df_loc_master.columns]
        # logger.info("mySQL - Insert starting")

        #writing to mysql                  
        # mysql_write = MySQL(read_only=False)
        # mysql_write.open_connection()

        # df_loc_master.to_sql(name='ob-location-master', con=mysql_write.engine,
        #                     if_exists='append', index=False,
        #                     method='multi', chunksize=500)

        # logger.info("mySQL - Insert ended")


        logger.info('Writing sku status file to ZenoInputs')

        df_status['updated-at'] = datetime.datetime.now(
            tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
        df_status.columns = [c.replace('_', '-') for c in
                                df_status.columns]
        table_info = helper.get_table_info(db=rs_db_write,
                                            table_name='ob-sku-status',
                                            schema=write_schema)
        columns = list(table_info['column_name'])
        df_status = df_status[columns]  # required column order
        # df_status.columns = ['SKU Name','Stock Location Code','Reported Date Year','Reported Date Month','Reported Date Day','Inventory At Hand','Inventory on the Way','updated-at']
        # logger.info("Writing to table: ob-transactions")
        # s3.write_df_to_db(df=df_status,
        #                     table_name='ob-sku-status',
        #                     db=rs_db_write, schema=write_schema)
        mssql = MSSql(connect_via_tunnel=False, db = 'ZenoInputs', is_ob=True,one_beat_type = 'in')
        mssql = mssql.open_connection()
        cursor=mssql.cursor()

        df_status = df_status.fillna('')
        sql_data = tuple(map(tuple, df_status.values))
        cursor = mssql.cursor()
        query = """INSERT INTO ZenoInputs.dbo.[ob-sku-status-test]
                ([stock-location-code], [sku-name], [inv-on-the-way], [inv-at-hand], [reported-year], [reported-month], [reported-day], [updated-at]) values (%s,%s,%s,%s,%s,%s,%s,%s);"""
        cursor.executemany(query, sql_data)

        mssql.commit()
        cursor.close()
        mssql.close()
        # mssql = MSSql(connect_via_tunnel=False, is_ob=True)
        # mssql = mssql.open_connection()
        # cursor=mssql.cursor()


        # for index,row in df_status.iterrows():
        #     cursor.execute("""INSERT INTO ZenoInputs.dbo.[ob-sku-status]
        #     ([stock-location-code], [sku-name], [inv-on-the-way], [inv-at-hand], [reported-year], [reported-month], [reported-day], [updated-at]) values ({},'{}','{}','{}',{},{},{},'{}');""".format(row['stock-location-code'],row['sku-name'],row['inv-on-the-way'],row['inv-at-hand'],row['reported-year'],row['reported-month'],row['reported-day'],row['updated-at']))
        #     mssql.commit()
        # cursor.close()
        # mssql.close()




        # inserting data into prod

        # logger.info("mySQL - Insert starting")

        # df_status.to_sql(name='ob-sku-status', con=mysql_write.engine,
        #                     if_exists='append', index=False,
        #                     method='multi', chunksize=500)

        # logger.info("mySQL - Insert ended")

        logger.info('Writing transactions file to ZenoInputs')

        df_transactions_final['updated-at'] = datetime.datetime.now(
            tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
        df_transactions_final.columns = [c.replace('_', '-') for c in
                                df_transactions_final.columns]
        table_info = helper.get_table_info(db=rs_db_write,
                                            table_name='ob-transactions',
                                            schema=write_schema)
        columns = list(table_info['column_name'])
        df_transactions_final = df_transactions_final[columns]  # required column order
        df_transactions_final['from-location'].fillna(8105, inplace=True)
        df_transactions_final['from-location'] = df_transactions_final['from-location'].astype(int)
        
        df_transactions_final = df_transactions_final.fillna('')
        mssql = MSSql(connect_via_tunnel=False, db = 'ZenoInputs', is_ob=True,one_beat_type = 'in')
        mssql = mssql.open_connection()
        cursor=mssql.cursor()

        sql_data = tuple(map(tuple, df_transactions_final.values))
        cursor = mssql.cursor()
        query = """INSERT INTO dbo.[ob-transactions-test]([from-location],[to-location],[trans-type],[sku],[quantity],
                    [reported-year],[reported-month],[reported-day],[adjust],[updated-at])
                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
        cursor.executemany(query, sql_data)

        mssql.commit()
        cursor.close()
        mssql.close()


        # for index,row in df_transactions_final.iterrows():
        #     cursor.execute("""INSERT INTO ZenoInputs.dbo.[ob-transactions]
        #     ([from-location], [to-location], [trans-type], sku, quantity, [reported-year], [reported-month], [reported-day], adjust, [updated-at]) values ({},'{}','{}','{}',{},{},{},'{}','{}','{}');""".format(row['from-location'],row['to-location'],row['trans-type'],row['sku'],row['quantity'],row['reported-year'],row['reported-month'],row['reported-day'],row['adjust'],row['updated-at']))
        #     mssql.commit()
        # cursor.close()
        # mssql.close()



        # logger.info("Writing to table: ob-transactions")
        # s3.write_df_to_db(df=df_transactions_final,
        #                     table_name='ob-transactions',
        #                     db=rs_db_write, schema=write_schema)

        # df_transactions_final.to_sql(name='ob-transactions', con=mysql_write.engine,
        #                     if_exists='append', index=False,
        #                     method='multi', chunksize=500)

        status = 'Success'
        logger.info(f"Onebeat code execution status: {status}")
        logger.info('Script Completed')

    except Exception as error:
        logger.exception(error)
        logger.info(f"Onebeat code execution status: {status}")

    return df_transactions_final, df_status, status

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="This is ETL script.")
    parser.add_argument('-e', '--env', default="dev", type=str, required=False)
    parser.add_argument('-d', '--debug_mode', default="Y", type=str,
                        required=False)
    parser.add_argument('-et', '--email_to',
                        default="tushar.uike@zeno.health", type=str,
                        required=False)
    parser.add_argument('-rs', '--ob_stores',
                        default=[2,17], nargs='+', type=int,
                        required=False)

    args, unknown = parser.parse_known_args()

    env = args.env
    os.environ['env'] = env
    debug_mode = args.debug_mode
    email_to = args.email_to
    stores = args.ob_stores
    s3 = S3()


    read_schema = 'prod2-generico'
    write_schema = 'prod2-generico'
    logger = get_logger()
    rs_db = DB()
    rs_db_write = DB(read_only=False)

    # open RS connection
    rs_db.open_connection()
    rs_db_write.open_connection()

    """ calling the main function """
    df_transactions, df_status, status = main(
        debug_mode, stores, rs_db, rs_db_write, read_schema, write_schema, logger,s3)

    # close RS connection
    rs_db.close_connection()
    rs_db_write.close_connection()

    logger.info("Script ended")
    run_date  = str(datetime.date.today())

    # SEND EMAIL ATTACHMENTS (Onebeat code-RUN STATUS)
    logger.info("Sending email attachments..")
    email = Email()
    email.send_email_file(
        subject=f"Onebeat input files push (SM-{env}) {run_date}: {status}",
        mail_body=f"""
                Debug Mode: {debug_mode}
                Reset Stores: {stores}
                Job Params: {args}
                """,
        to_emails=email_to)



