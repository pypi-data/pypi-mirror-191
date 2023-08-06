"""
Sometime only a few table fail to load and DMS keeps running with the error status. So till the
entire DMS task fails, we do know about the table failures. So to get the alerts for these specific
tables, this job fetches the status from DMS and notifies the team over email.
"""
import argparse
import os
import sys

sys.path.append('../../../..')

from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper.aws.dms import DMS
from zeno_etl_libs.helper.email.email import Email

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False,
                    help="This is env(dev, stage, prod)")
parser.add_argument('-ids', '--task_ids', default="CBS5J6V4AVST5D3DEZSQDNH363A37XI4F6JU3II",
                    type=str, required=False,
                    help="task id in csv")
parser.add_argument('-et', '--email_to', default="kuldeep.singh@zeno.health", type=str, required=False)
args, unknown = parser.parse_known_args()
env = args.env
email_to = args.email_to
task_ids = args.task_ids

os.environ['env'] = env
logger = get_logger()

logger.info(f"env: {env}")

""" DMS class """
dms = DMS()
email = Email()

for task_id in task_ids.split(','):
    logger.info(f"task id: {task_id}")
    response = dms.describe_table_statistics(task_id=task_id, table_state='Table error')
    logger.info(f"response: {response}")
    table_statistics_old = response.get('TableStatistics')
    table_statistics = []
    for table in table_statistics_old:
        if '_' in table['TableName']:
            continue
        table_statistics.append(table)
    if table_statistics:
        tables = ', '.join([i['TableName'] for i in table_statistics])
        email.send_email_file(subject=f"DMS[Table Error]: Total {len(table_statistics)} tables",
                              mail_body=f'Following tables are in failed state: {tables}',
                              to_emails=email_to, file_uris=[], file_paths=[])


