import pandas as pd
from zeno_etl_libs.db.db import MSSql

mssql = MSSql(connect_via_tunnel=False, is_ob=True)
mssql = mssql.open_connection()
bhw1 = pd.read_csv('/Users/surbhi/Downloads/_ob_sku_status__202302011532.csv', header='infer')
bhw1 = bhw1.fillna('')
# sql_data = tuple(map(tuple, bhw1.values))
cursor = mssql.cursor()
# query = """INSERT INTO dbo.[ob-transactions-test]([from-location],[to-location],[trans-type],[sku],[quantity],
#             [reported-year],[reported-month],[reported-day],[adjust],[updated-at])
#             values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
# cursor.executemany(query, sql_data)
# for index,row in bhw1.iterrows():
#     cursor.execute("""INSERT INTO dbo.[ob-location-master]([stock-location],[store-description],[store-type],[city], [reported-year],[reported-month],[reported-day],[updated-at]) values ({},'{}','{}','{}',{},{},{},'{}');""".format(row['stock-location'],row['store-description'],row['store-type'],row['city'],row['reported-year'], row['reported-month'], row['reported-day'], row['updated-at']))
# query = """exec msdb.dbo.rds_download_from_s3
#  @s3_arn_of_file='arn:aws:s3:::aws-glue-temporary-921939243643-ap-south-1/onebeat-mssql/_ob_sku_status__202302011532.csv',
#  @rds_file_path='D:\\S3\\aws-glue-temporary-921939243643-ap-south-1\\_ob_sku_status__202302011532.csv',
#  @overwrite_file=1;"""
# cursor.execute(query)
cursor.execute("""BULK INSERT dbo.[ob-sku-status-test]
               FROM 'D:\\S3\\aws-glue-temporary-921939243643-ap-south-1\\_ob_sku_status__202302011532.csv'
               WITH
               (
                   FIRSTROW = 2,
                   FIELDTERMINATOR = ',',
                   ROWTERMINATOR = '\n'
               )""")

mssql.commit()
cursor.close()
mssql.close()
