import boto3
from botocore.exceptions import ClientError
from zeno_etl_libs.config.common import Config


class crawler:
    """
    Helper class to integrate with AWS Glue crawler
    """

    def __init__(self):
        configobj = Config.get_instance()
        self.secrets = configobj.get_secrets()
        self.session = boto3.session.Session()
        self.glue_client = self.session.client('glue')
        self.crawler_name = f"datalake-{self.secrets['ENV']}-crawler"

    def start_crawler(self):
        try:
            response = self.glue_client.start_crawler(Name=self.crawler_name)
            return response
        except ClientError as e:
            raise Exception("boto3 client error in start_a_crawler: " + e.__str__())
        except Exception as e:
            raise Exception("Unexpected error in start_a_crawler: " + e.__str__())

