import boto3

from zeno_etl_libs.config.common import Config


class DMS:
    """
    Helper class to integrate with AWS DMS
    """

    def __init__(self):
        configobj = Config.get_instance()
        self.secrets = configobj.get_secrets()
        self.client = boto3.client('dms')

    def start(self, task_id):
        arn = f"arn:aws:dms:{self.secrets['AWS_REGION']}:{self.secrets['AWS_ACCOUNT_ID']}:task:{task_id}"
        return self.client.start_replication_task(
            ReplicationTaskArn=arn,
            StartReplicationTaskType='resume-processing'
        )

    def stop(self, task_id):
        arn = f"arn:aws:dms:{self.secrets['AWS_REGION']}:{self.secrets['AWS_ACCOUNT_ID']}:task:{task_id}"
        return self.client.stop_replication_task(ReplicationTaskArn=arn)

    def describe_table_statistics(self, task_id, table_state=None):
        arn = f"arn:aws:dms:{self.secrets['AWS_REGION']}:{self.secrets['AWS_ACCOUNT_ID']}:task:{task_id}"
        filters = None
        if table_state:
            filters = [
                {
                    'Name': 'table-state',
                    'Values': [
                        table_state
                    ]
                },
            ]
        return self.client.describe_table_statistics(
            ReplicationTaskArn=arn,
            Filters=filters
        )
