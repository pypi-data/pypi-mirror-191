import os
import sys
import datetime
import numpy as np
import pandas as pd
from dateutil.tz import gettz
from pyspark.context import SparkContext
from awsglue.utils import getResolvedOptions
from datetime import datetime, timedelta

from zeno_etl_libs.db.db import Athena
from zeno_etl_libs.db.db import DB
from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.helper import helper

sc = SparkContext.getOrCreate()

args = getResolvedOptions(sys.argv, ["ENV"])
env = args["ENV"]
os.environ['env'] = env

# setting up Athena connection
Athena = Athena()
conn = Athena.connection()

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
cohort_query = """select * from waba_campaigns_cohort ;"""
#
# # Reading data from Athena need to pass only query and connection name stored in above step
cohort = Athena.get_df(query=cohort_query)
print(cohort)