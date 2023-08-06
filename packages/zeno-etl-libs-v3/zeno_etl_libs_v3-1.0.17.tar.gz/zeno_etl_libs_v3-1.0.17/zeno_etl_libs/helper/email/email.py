# https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types
import re

import requests

from zeno_etl_libs.config.common import Config
from zeno_etl_libs.helper.aws.s3 import S3

FILE_TYPES_MIME_MAPPING = {
    'csv': 'application/csv',
    'txt': 'text/plain',
    'log': 'text/plain',
    'xls': 'application/vnd.ms-excel',
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'zip': 'application/zip'
}


def determine_file_mime_type(file_name):
    if file_name.endswith(".csv"):
        return FILE_TYPES_MIME_MAPPING['csv']
    elif file_name.endswith(".txt"):
        return FILE_TYPES_MIME_MAPPING['txt']
    elif file_name.endswith(".log"):
        return FILE_TYPES_MIME_MAPPING['log']
    elif file_name.endswith(".xls"):
        return FILE_TYPES_MIME_MAPPING['xls']
    elif file_name.endswith(".xlsx"):
        return FILE_TYPES_MIME_MAPPING['xlsx']
    elif file_name.endswith(".zip"):
        return FILE_TYPES_MIME_MAPPING['zip']
    raise ValueError("No MIME type available")


class Email:
    def __init__(self):
        configobj = Config.get_instance()
        secrets = configobj.get_secrets()
        self.url = secrets['NODE_NOTIFICATION_BASE_URL']
        self.NOTIFICATION_EMAIL_FILE_POSTFIX_URL = "api/v1/queueing-notification/send-mail"
        self.auth_token = secrets['NOTIFICATION_AUTH_TOKEN']
        self.s3 = S3()

    def send_email_file(self, subject, mail_body, to_emails, file_uris=None, file_paths=None, from_email='tech-team@generico.in'):
        file_paths = file_paths if file_paths else []
        multiple_files = list()
        url = self.url + self.NOTIFICATION_EMAIL_FILE_POSTFIX_URL
        headers = {'Authorization': self.auth_token}

        if isinstance(to_emails, list):
            to_emails = ','.join(email_id for email_id in to_emails)

        data = {
            'subject': subject,
            'body': mail_body,
            'to_emails': to_emails,
            'from_email': from_email,
            'is_html': 'false',
        }
        if file_uris is not None:
            for file_uri in file_uris:
                file_name = file_uri.split('/')[-1]
                mime_type = determine_file_mime_type(file_name)
                file_bytes = self.s3.get_file_object(uri=file_uri)
                multiple_files.append(('file', (file_name, file_bytes, mime_type)))

        for file_path in file_paths:
            file_name = file_path.split('/')[::-1][0]
            mime_type = determine_file_mime_type(file_name)
            multiple_files.append(('file', (file_name, open(file_path, 'rb'), mime_type)))

        response = requests.post(url, data=data, files=multiple_files, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Email sending failed: {response.text}")
        else:
            print(f"Email sending successful: {response.text}")


def is_string_an_email(email: str):
    """
    Checks if a given string is proper email or some fake string.

    Eg:
    email = "somename@comapany.com"
    is_string_an_email(email) --> True

    :param email: email id string
    :return: True | False
    """

    email_regx = "^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$"
    if re.match(email_regx, email):
        return True
    return False


def any_email_in_string(csv_emails):
    """
    In a given comma separated string, if any email id is present then returns True

    :param csv_emails: comma separated email id strings

    :returns: True | False
    """
    for string in csv_emails.split(","):
        if is_string_an_email(email=string):
            return True
    return False
