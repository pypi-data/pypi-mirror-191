''' Script for Ops-data-query  '''

#@owner: akshay.bhutada@zeno.health

#@Purpose: To find purchase sales ration at store and network level


import os
import sys
from dateutil.tz import gettz
import datetime
import argparse
import pandas as pd
import numpy as np

sys.path.append('../../../..')

from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.helper.email.email import Email
from zeno_etl_libs.db.db import DB
from zeno_etl_libs.db.db import MSSql
from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper import helper


parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False)
parser.add_argument('-et', '--email_to',
                    default=
                    "akshay.bhutada@zeno.health,rajesh.shinde@zeno.health,swapnil.gade@zeno.health",
                    type=str, required=False)
parser.add_argument('-sd', '--start_date', default='NA', type=str, required=False)
parser.add_argument('-ed', '--end_date', default='NA', type=str, required=False)
args, unknown = parser.parse_known_args()
env = args.env
email_to = args.email_to
start_date = args.start_date
end_date = args.end_date

os.environ['env'] = env

cur_date = datetime.datetime.now(tz=gettz('Asia/Kolkata')).date()

d = datetime.timedelta(days = 5)

start_dt=cur_date-d

end_dt = cur_date - datetime.timedelta(1)


if start_date == 'NA' and end_date == 'NA':
    start_date = start_dt
    end_date = end_dt

s3=S3()

logger = get_logger(level='INFO')

rs_db = DB()
rs_db.open_connection()



#Store-sales

q_1='''select
	'store' as "type-1",
	s."store-id" as "entity-id" ,
	s."store-name" as "entity-name" ,
	'SB' as "sub-type-1",
	'' as "sub-type-2",
	'' as "sub-type-3",
	s."type" as "drug-type",
	s.category as "drug-category",
	(case when s."company-id"=6984 then 'true'
	else 'false' end) as "goodaid-flag",
	(case when s."invoice-item-reference" is null then 76
		else s."distributor-id" end ) as "distributor-id",
	(case when s."invoice-item-reference"  is null then 'Local Purchase'
		else s."distributor-name" end )  as "distributor-name",
	(case when sb."patient-id"=4480 and sb."auto-short"=1 then 'AS'
	When sb."auto-short"=0 and sb."auto-generated"=0 and sb."patient-id"!=4480 then 'PR'
	when sb."auto-short" =1 and sb."patient-id" !=4480  then 'MS'
	else 'distributor-dump' end ) as "as-ms-pr",
	date(s."created-at") as "approved-date",
	SUM(s."net-quantity") as "net-quantity",
	SUM(s."net-quantity"*s.rate) as "net-value"
from
	"prod2-generico".sales s 
left join (select * from (select
	"invoice-item-id",
	"short-book-id",
	row_number() over(partition by "invoice-item-id" 
order by
	"short-book-id" desc) as count_new
from
	"prod2-generico"."prod2-generico"."short-book-invoice-items" sbii  ) a
where a.count_new=1 ) g on
		s."invoice-item-reference" = g."invoice-item-id"
left join "prod2-generico"."prod2-generico"."short-book-1" sb on
		g."short-book-id" = sb.id
where date(s."created-at")>='{}' and date(s."created-at")<='{}' and  s."franchisee-id" =1
and  s."store-b2b" ='Store'
	group by 
	 "type-1" ,
	s."store-id" ,
	s."store-name" ,
	 "sub-type-1",
	 "sub-type-2",
	 "sub-type-3",
	s."type" ,
	s.category ,
	(case when s."company-id"=6984 then 'true'
	else 'false' end) ,
	(case when s."invoice-item-reference" is null then 76
		else s."distributor-id" end ) ,
	(case when s."invoice-item-reference"  is null then 'Local Purchase'
		else s."distributor-name" end ) ,
	(case when sb."patient-id"=4480 and sb."auto-short"=1 then 'AS'
	When sb."auto-short"=0 and sb."auto-generated"=0 and sb."patient-id"!=4480 then 'PR'
	when sb."auto-short" =1 and sb."patient-id" !=4480  then 'MS'
	else 'distributor-dump' end ) ,
	date(s."created-at")
'''.format(start_date, end_date)


store_sales=rs_db.get_df(query=q_1)


#Store DC/WH Purchase

q_2='''
select
	'store' as "type-1",
	i."store-id" as "entity-id" ,
	s."name"  as "entity-name",
	'PB' as "sub-type-1",
	(case
		when i."distributor-id" = 8105 then 'WH'
		else 'DC' end) as "sub-type-2",
	'' as "sub-type-3",
	d."type" as "drug-type",
	d.category as "drug-category",
	(case
		when d."company-id" = 6984 then 'true'
		else 'false'
	end) as "goodaid-flag",
	i."distributor-id" ,
	d2."name" as "distributor-name",
	(case when sb."patient-id"=4480 and sb."auto-short"=1 then 'AS'
	When sb."auto-short"=0 and sb."auto-generated"=0 and sb."patient-id"!=4480 then 'PR'
	when sb."auto-short" =1 and sb."patient-id" !=4480  then 'MS'
	else 'distributor-dump' end ) as "as-ms-pr",
	date(i."approved-at") as "approved-date",
	SUM(ii."actual-quantity") as "net-quantity",
	SUM(ii."net-value") as "net-value"
from
	"prod2-generico"."prod2-generico"."invoice-items" ii
left join "prod2-generico"."prod2-generico".invoices i on
	ii."invoice-id" = i.id
left join "prod2-generico"."prod2-generico".stores s on
	s.id = i."store-id"
left join "prod2-generico"."prod2-generico".drugs d on
	ii."drug-id" = d.id
left join "prod2-generico"."prod2-generico".distributors d2 on
i."distributor-id" =d2.id 
left join (select * from (select
	"invoice-item-id",
	"short-book-id",
	row_number() over(partition by "invoice-item-id" 
order by
	"short-book-id" desc) as count_new
from
	"prod2-generico"."prod2-generico"."short-book-invoice-items" sbii  ) a
where a.count_new=1 ) g on
		ii.id = g."invoice-item-id"
	left join "prod2-generico"."prod2-generico"."short-book-1" sb on
		g."short-book-id" = sb.id
where
	 date(i."approved-at") >='{}' and date(i."approved-at") <='{}'
	and s."franchisee-id" =1
group by
	"type-1",
	i."store-id" ,
	s."name" ,
	"sub-type-1",
	(case
		when i."distributor-id" = 8105 then 'WH'
		else 'DC' end)  ,
	"sub-type-3",
	d."type" ,
	d.category ,
	(case
		when d."company-id" = 6984 then 'true'
		else 'false'
	end),
	i."distributor-id" ,
	d2."name" ,
	(case when sb."patient-id"=4480 and sb."auto-short"=1 then 'AS'
	When sb."auto-short"=0 and sb."auto-generated"=0 and sb."patient-id"!=4480 then 'PR'
	when sb."auto-short" =1 and sb."patient-id" !=4480  then 'MS'
	else 'distributor-dump' end ),
	date(i."approved-at")
'''.format(start_date, end_date)

store_dc_wh_purchase=rs_db.get_df(query=q_2)

#Store Local Purchase

q_3='''
select
	'store' as "type-1",
	i."store-id" as "entity-id" ,
	s."name"  as "entity-name",
	'PB' as "sub-type-1",
	'LP' as "sub-type-2",
	'' as "sub-type-3",
	d."type" as "drug-type",
	d.category as "drug-category",
	(case
		when d."company-id" = 6984 then 'true'
		else 'false'
	end) as "goodaid-flag",
	i."distributor-id" ,
	d2."name" as "distributor-name",
	'' as "as-ms-pr",
	date(i."approved-at") as "approved-date",
	SUM(ii."actual-quantity") as "net-quantity",
	SUM(ii."net-value") as "net-value"
from
	"prod2-generico"."prod2-generico"."invoice-items-1" ii
left join "prod2-generico"."prod2-generico"."invoices-1" i on ii."franchisee-invoice-id" =i.id 
left join "prod2-generico"."prod2-generico".stores s on
	s.id = i."store-id"
left join "prod2-generico"."prod2-generico".drugs d on
	ii."drug-id" = d.id
left join "prod2-generico"."prod2-generico".distributors d2 on
i."distributor-id" =d2.id 
where
	ii."invoice-item-reference" is null and s."franchisee-id" =1 and 
	 date(i."approved-at") >='{}' and date(i."approved-at") <='{}'
group by
  	"type-1",
	i."store-id" ,
	s."name" ,
	"sub-type-1",
	"sub-type-2",
	"sub-type-3",
	d."type" ,
	d.category ,
	(case
		when d."company-id" = 6984 then 'true'
		else 'false'
	end),
	i."distributor-id" ,
	d2."name" ,
	"as-ms-pr",
	date(i."approved-at")
'''.format(start_date, end_date)

store_lp_purchase=rs_db.get_df(query=q_3)


#Network Level

# DC Purchase

q_4='''
select
	'network' as "type-1",
	i."dc-id" as "entity-id" ,
	s."name"  as "entity-name",
	'PB' as "sub-type-1",
	'DC' as "sub-type-2",
	'' as "sub-type-3",
	d."type" as "drug-type",
	d.category as "drug-category",
	(case
		when d."company-id" = 6984 then 'true'
		else 'false'
	end) as "goodaid-flag",
	i."distributor-id" ,
	d2."name" as "distributor-name",
	(case when sb."patient-id"=4480 and sb."auto-short"=1 then 'AS'
	When sb."auto-short"=0 and sb."auto-generated"=0 and sb."patient-id"!=4480 then 'PR'
	when sb."auto-short" =1 and sb."patient-id" !=4480  then 'MS'
	else 'distributor-dump' end ) as "as-ms-pr",
	date(i."approved-at") as "approved-date",
	SUM(ii."actual-quantity") as "net-quantity",
	SUM(ii."net-value") as "net-value"
from
	"prod2-generico"."prod2-generico"."invoice-items" ii
left join "prod2-generico"."prod2-generico".invoices i on
	ii."invoice-id" = i.id
left join "prod2-generico"."prod2-generico".stores s on
	i."dc-id" =s.id 
left join "prod2-generico"."prod2-generico".stores s2 on
i."store-id" =s2.id
left join "prod2-generico"."prod2-generico".drugs d on
	ii."drug-id" = d.id
left join "prod2-generico"."prod2-generico".distributors d2 on
i."distributor-id" =d2.id 
left join (select * from (select
	"invoice-item-id",
	"short-book-id",
	row_number() over(partition by "invoice-item-id" 
order by
	"short-book-id" desc) as count_new
from
	"prod2-generico"."prod2-generico"."short-book-invoice-items" sbii  ) a
where a.count_new=1 ) g on
		ii.id = g."invoice-item-id"
	left join "prod2-generico"."prod2-generico"."short-book-1" sb on
		g."short-book-id" = sb.id
where
	  date(i."approved-at") >='{}' and date(i."approved-at") <='{}'
	and s2."franchisee-id" =1 and i."distributor-id" !=8105
group by 
	"type-1",
	i."dc-id" ,
	s."name" ,
	"sub-type-1",
	"sub-type-2",
	"sub-type-3",
	d."type" ,
	d.category ,
	(case
		when d."company-id" = 6984 then 'true'
		else 'false'
	end),
	i."distributor-id" ,
	d2."name" ,
	(case when sb."patient-id"=4480 and sb."auto-short"=1 then 'AS'
	When sb."auto-short"=0 and sb."auto-generated"=0 and sb."patient-id"!=4480 then 'PR'
	when sb."auto-short" =1 and sb."patient-id" !=4480  then 'MS'
	else 'distributor-dump' end ) ,
	date(i."approved-at")
'''.format(start_date, end_date)


network_dc_purchase=rs_db.get_df(query=q_4)

# Local purchase network

q_5='''
select
	'network' as "type-1",
	'' as "entity-id",
	''  as "entity-name",
	'PB' as "sub-type-1",
	'LP' as "sub-type-2",
	'' as "sub-type-3",
	d."type" as "drug-type",
	d.category as "drug-category",
	(case
		when d."company-id" = 6984 then 'true'
		else 'false'
	end) as "goodaid-flag",
	i."distributor-id" ,
	d2."name" as "distributor-name",
	'' as "as-ms-pr",
	date(i."approved-at") as "approved-date",
	SUM(ii."actual-quantity") as "net-quantity",
	SUM(ii."net-value") as "net-value"
from
	"prod2-generico"."prod2-generico"."invoice-items-1" ii
left join "prod2-generico"."prod2-generico"."invoices-1" i on ii."franchisee-invoice-id" =i.id 
left join "prod2-generico"."prod2-generico".stores s on
	s.id = i."store-id"
left join "prod2-generico"."prod2-generico".drugs d on
	ii."drug-id" = d.id
left join "prod2-generico"."prod2-generico".distributors d2 on
i."distributor-id" =d2.id 
where
	ii."invoice-item-reference" is null and s."franchisee-id" =1 and 
	 date(i."approved-at") >='{}' and date(i."approved-at") <='{}'
group by
  	"type-1",
	"entity-id" ,
	"entity-name" ,
	"sub-type-1",
	"sub-type-2",
	"sub-type-3",
	d."type" ,
	d.category ,
	(case
		when d."company-id" = 6984 then 'true'
		else 'false'
	end),
	i."distributor-id" ,
	d2."name" ,
	date(i."approved-at")
'''.format(start_date, end_date)

network_lp_purchase=rs_db.get_df(query=q_5)


# Sale to Franchisee

q_6='''
select
	'network' as "type-1",
	s."franchisee-id" as "entity-id" ,
	f."name" as "entity-name",
	'SB' as "sub-type-1",
	'Franchisee' as "sub-type-2",
	(case
		when i."distributor-id" = 8105 then 'WH'
		else 'DC' end) as "sub-type-3",
	d."type" as "drug-type",
	d.category as "drug-category",
	(case
		when d."company-id" = 6984 then 'true'
		else 'false'
	end) as "goodaid-flag",
	i."distributor-id" ,
	d2."name" as "distributor-name",
	'' as "as-ms-pr",
	date(i1."approved-at") as "approved-date",
	SUM(ii."actual-quantity") as "net-quantity",
	SUM(ii."net-value") as "net-value"
from
"prod2-generico"."prod2-generico"."invoice-items-1" ii 
left join "prod2-generico"."prod2-generico"."invoices-1" i1 on ii."franchisee-invoice-id" =i1.id 
left join "prod2-generico"."prod2-generico".invoices i on
	ii."invoice-id" =i.id 
left join "prod2-generico"."prod2-generico".stores s on
	i1."store-id" =s.id 
left join "prod2-generico"."prod2-generico".franchisees f 
on s."franchisee-id" =f.id 
left join "prod2-generico"."prod2-generico".drugs d on
	ii."drug-id" = d.id
left join "prod2-generico"."prod2-generico".distributors d2 on
i."distributor-id" =d2.id 
where
	  date(i1."approved-at") >='{}' and date(i1."approved-at") <='{}'
	and s."franchisee-id" !=1 and i1."franchisee-invoice" =0
group by 
	"type-1",
	s."franchisee-id" ,
	f."name" ,
	"sub-type-1",
	"sub-type-2",
	(case
		when i."distributor-id" = 8105 then 'WH'
		else 'DC' end),
	d."type" ,
	d.category ,
	(case
		when d."company-id" = 6984 then 'true'
		else 'false'
	end),
	i."distributor-id" ,
	d2."name" ,
	date(i1."approved-at");
'''.format(start_date, end_date)

network_franchisee_sale=rs_db.get_df(query=q_6)

#Drug INFO


# drug info


drug_info = '''

select
	d.id as "drug-id",
	d."type" as "drug-type" ,
	d."category" as "drug-category",
	(case when d."company-id" =6984 then 'true'
	else 'false'  end) as "goodaid-flag"
from
	"prod2-generico".drugs d 
'''

drug_info = rs_db.get_df(query=drug_info)

# Warehouse purchase network

# Bhiwandi Warehouse

mssql_bhw = MSSql(connect_via_tunnel=False)

cnxn = mssql_bhw.open_connection()

cursor = cnxn.cursor()

q_7='''
select
	'network' as "type-1",
	199 as "entity-id" ,
	'bhiwandi-warehouse' as "entity-name",
	'PB' as "sub-type-1",
	'WH' as "sub-type-2",
	(CASE
		when sp.vno>0 then 'barcoded'
		else 'non-barcoded'
	end) as "sub-type-3",
	i.Barcode as "drug-id",
	sp.acno as "distributor-id",
	a."name" as "distributor-name",
	(CASE when f.Uid is null then 'Auto'
	else 'manual' end ) as "as-ms-pr",
	CONVERT(date ,
	sp.Vdt) as "approved-date",
	SUM(sp.qty) as "net-quantity",
	SUM(sp.netamt + sp.taxamt) as "net-value"
from
	salepurchase2 sp
left join item i on
	sp.itemc = i.code
left join acm a on
	sp.acno = a.code
left join (Select Uid,Vtyp,Vdt,Acno,Vno FROM Salepurchase1 sp1 where sp1.Vtyp ='PO' and sp1.Slcd ='SL') f 
on (f.Vno=sp.RefVno and convert(date,sp.RefVdt) =convert(date,f.Vdt) and sp.Acno =f.acno)
where
	sp.vtype = 'PB'
	and sp.vdt >= '{}'
	and sp.vdt <= '{}'
	and sp.qty >0
	and 
	isnumeric(i.Barcode) = 1
	and i.barcode not like '%[^0-9]%' and sp.Acno not IN (59489)
group by
	(CASE
		when sp.vno>0 then 'barcoded'
		else 'non-barcoded'
	end),
	i.Barcode ,
	sp.acno ,
	a."name" ,
		(CASE when f.Uid is null then 'Auto'
	else 'manual' end ),
	sp.Vdt;
'''.format(start_date, end_date)

network_wh_purchase_bhiwandi= pd.read_sql(q_7,cnxn)

# GOODAID Warehouse


mssql_ga = MSSql(connect_via_tunnel=False,db='Esdata_WS_2')

cnxn = mssql_ga.open_connection()

cursor = cnxn.cursor()

q_8='''
select
	'network' as "type-1",
	343 as "entity-id" ,
	'goodaid-warehouse' as "entity-name",
	'PB' as "sub-type-1",
	'WH' as "sub-type-2",
	(CASE
		when sp.vno>0 then 'barcoded'
		else 'non-barcoded'
	end) as "sub-type-3",
	i.Barcode as "drug-id",
	sp.acno as "distributor-id",
	a."name" as "distributor-name",
	(CASE when f.Uid is null then 'Auto'
	else 'manual' end ) as "as-ms-pr",
	CONVERT(date ,
	sp.Vdt) as "approved-date",
	SUM(sp.qty) as "net-quantity",
	SUM(sp.netamt + sp.taxamt) as "net-value"
from
	salepurchase2 sp
left join item i on
	sp.itemc = i.code
left join acm a on
	sp.acno = a.code
left join (Select Uid,Vtyp,Vdt,Acno,Vno FROM Salepurchase1 sp1 where sp1.Vtyp ='PO' and sp1.Slcd ='SL') f 
on (f.Vno=sp.RefVno and convert(date,sp.RefVdt) =convert(date,f.Vdt) and sp.Acno =f.acno)
where
	sp.vtype = 'PB'
	and sp.vdt >= '{}'
	and sp.vdt <= '{}'
	and sp.qty >0 and 
	isnumeric(i.Barcode) = 1
	and i.barcode not like '%[^0-9]%'
group by
	(CASE
		when sp.vno>0 then 'barcoded'
		else 'non-barcoded'
	end),
	i.Barcode ,
	sp.acno ,
	a."name" ,
		(CASE when f.Uid is null then 'Auto'
	else 'manual' end ),
	sp.Vdt
'''.format(start_date, end_date)

network_wh_purchase_goodaid= pd.read_sql(q_8,cnxn)


mssql_tepl = MSSql(connect_via_tunnel=False,db='Esdata_TEPL')

cnxn = mssql_tepl.open_connection()

cursor = cnxn.cursor()

q_9='''
select
	'network' as "type-1",
	342 as "entity-id" ,
	'tepl-warehouse' as "entity-name",
	'PB' as "sub-type-1",
	'WH' as "sub-type-2",
	(CASE
		when sp.vno>0 then 'barcoded'
		else 'non-barcoded'
	end) as "sub-type-3",
	i.Barcode as "drug-id",
	sp.acno as "distributor-id",
	a."name" as "distributor-name",
	(CASE when f.Uid is null then 'Auto'
	else 'manual' end ) as "as-ms-pr",
	CONVERT(date ,
	sp.Vdt) as "approved-date",
	SUM(sp.qty) as "net-quantity",
	SUM(sp.netamt + sp.taxamt) as "net-value"
from
	salepurchase2 sp
left join item i on
	sp.itemc = i.code
left join acm a on
	sp.acno = a.code
left join (Select Uid,Vtyp,Vdt,Acno,Vno FROM Salepurchase1 sp1 where sp1.Vtyp ='PO' and sp1.Slcd ='SL') f 
on (f.Vno=sp.RefVno and convert(date,sp.RefVdt) =convert(date,f.Vdt) and sp.Acno =f.acno)
where
	sp.vtype = 'PB'
	and sp.vdt >= '{}'
	and sp.vdt <= '{}'
	and sp.qty >0 and 
	isnumeric(i.Barcode) = 1
	and i.barcode not like '%[^0-9]%'
group by
	(CASE
		when sp.vno>0 then 'barcoded'
		else 'non-barcoded'
	end),
	i.Barcode ,
	sp.acno ,
	a."name" ,
		(CASE when f.Uid is null then 'Auto'
	else 'manual' end ),
	sp.Vdt
'''.format(start_date, end_date)

network_wh_purchase_tepl= pd.read_sql(q_9,cnxn)


network_wh_purchase=\
    pd.concat([network_wh_purchase_bhiwandi,network_wh_purchase_goodaid,network_wh_purchase_tepl],
              sort=False,ignore_index=False)

network_wh_purchase[['drug-id']]= network_wh_purchase[['drug-id']].\
    apply(pd.to_numeric, errors='ignore').\
    astype('Int64')

network_wh_purchase=pd.merge(network_wh_purchase,drug_info,how='left',on='drug-id')

network_wh_purchase[['drug-type','drug-category', 'goodaid-flag']]=\
    network_wh_purchase[['drug-type','drug-category', 'goodaid-flag']].\
        fillna('NA')

network_wh_purchase=network_wh_purchase.drop(['drug-id'],axis=1)

network_wh_purchase[['net-quantity']]=network_wh_purchase[['net-quantity']].astype(np.int64)



network_wh_purchase=network_wh_purchase.\
    groupby(['type-1','entity-id','entity-name','sub-type-1',
            'sub-type-2','sub-type-3','drug-type','drug-category',
            'goodaid-flag','distributor-id',
        'distributor-name','as-ms-pr','approved-date']).sum()

network_wh_purchase=network_wh_purchase.reset_index()



network_wh_purchase[['entity-id']]=network_wh_purchase[['entity-id']].replace(0, np.nan)



network_wh_purchase=network_wh_purchase[['type-1','entity-id','entity-name','sub-type-1',
                            'sub-type-2','sub-type-3','drug-type','drug-category',
                            'goodaid-flag','distributor-id',
                            'distributor-name','as-ms-pr','approved-date','net-quantity',
                            'net-value']]



sale_purchase_all=pd.concat([store_sales,store_dc_wh_purchase,store_lp_purchase,
                 network_dc_purchase,
                network_lp_purchase,network_wh_purchase,network_franchisee_sale],
                 sort=False,ignore_index=False)


sale_purchase_all[['entity-id', 'distributor-id']]= \
    sale_purchase_all[['entity-id','distributor-id']].\
    apply(pd.to_numeric, errors='ignore').astype('Int64')

sale_purchase_all[['net-quantity']]=sale_purchase_all[['net-quantity']].astype(np.int64)

sale_purchase_all[['net-value']]=sale_purchase_all[['net-value']].astype(np.float64)



#code for daily investor mail

sale_purchase_investor=sale_purchase_all[sale_purchase_all["approved-date"]==end_date]

sale_purchase_investor=sale_purchase_investor[sale_purchase_investor["type-1"]=='store']


sale_purchase_investor=sale_purchase_investor[sale_purchase_investor["sub-type-1"]=='PB']


sale_purchase_investor=sale_purchase_investor.\
    drop(["type-1","sub-type-1","sub-type-3","drug-type",
          "drug-category","goodaid-flag","distributor-id",
          "distributor-name","as-ms-pr","net-quantity"],axis=1)


sale_purchase_investor=sale_purchase_investor.groupby(['entity-id','entity-name',
                                                 'sub-type-2',
                                                 'approved-date']).sum()

sale_purchase_investor = pd.pivot_table(sale_purchase_investor,
                                   values='net-value',
                                   index=['entity-id', 'entity-name','approved-date'],
                                   columns=['sub-type-2']).reset_index()

sale_purchase_investor=sale_purchase_investor.fillna(0)


sale_purchase_investor=sale_purchase_investor.reset_index()

sale_purchase_investor=sale_purchase_investor.drop(["index"],axis=1)


sale_purchase_file_name = 'purchase_sale/sale_purchase_report_{}.csv'.format(end_date)

sale_purchase_uri = s3.save_df_to_s3(df=sale_purchase_investor, file_name=sale_purchase_file_name)





created_at = datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")
sale_purchase_all['created-at']=datetime.datetime.strptime(created_at,"%Y-%m-%d %H:%M:%S")
updated_at = datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")
sale_purchase_all['updated-at']=datetime.datetime.strptime(updated_at,"%Y-%m-%d %H:%M:%S")
sale_purchase_all['created-by'] = 'etl-automation'
sale_purchase_all['updated-by'] = 'etl-automation'



sale_purchase_all.columns = [c.replace('_', '-') for c in sale_purchase_all.columns]



schema = "prod2-generico"
table_name = "purchase-sales-meta"
table_info = helper.get_table_info(db=rs_db, table_name=table_name, schema=schema)


#truncating the last 5 days data

delete_q = """
        DELETE
        FROM
            "prod2-generico"."purchase-sales-meta"
        WHERE
            date("approved-date") >= '{start_date_n}'
            and date("approved-date") <= '{end_date_n}'
    """.format(start_date_n=start_date, end_date_n=end_date)


rs_db.execute(delete_q)

#Keep only Last one year data

delete_one_year='''

delete from "prod2-generico"."purchase-sales-meta" 
where date("approved-date")<=current_date -interval '12 months'
'''
rs_db.execute(delete_one_year)

s3.write_df_to_db(df=sale_purchase_all[table_info['column_name']], table_name=table_name, db=rs_db,
                  schema=schema)


status=True


if status==True:
    script_status="Success"
else:
    script_status="Failed"


email = Email()

#email.send_email_file(subject=f"purchase_sales
# start date: {start_date} end date: {end_date} {script_status}",
         #mail_body=f"purchase_sales status: {script_status} ",
                      #to_emails=email_to)

email.send_email_file(subject=f"sale purchase report  for date {end_date}",
                      mail_body=f"PFA sale purchase data for date   {end_date} ",
                      to_emails=email_to, file_uris=[sale_purchase_uri])


rs_db.close_connection()
mssql_bhw.close_connection()
mssql_ga.close_connection()

