import time

import boto3

from zeno_etl_libs.config.common import Config


class Glue:
    """
    Helper class to integrate with AWS Glue
    """

    def __init__(self):
        configobj = Config.get_instance()
        self.secrets = configobj.get_secrets()
        self.client = boto3.client('glue')

    def start_job_run(self, job_name, arguments):
        try:
            run = boto3.client('glue').start_job_run(JobName=job_name, Arguments=arguments)
            print(f"run data: {run}")
            time.sleep(1)
            status = self.client.get_job_run(JobName=job_name, RunId=run['JobRunId'])
            print(f"job status : {status}")
            return status
        except Exception as e:
            print(f"[ERROR] while triggering the job: {e}")
            return {"error": e.__str__()}

