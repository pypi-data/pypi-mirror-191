import os

import boto3
from botocore.exceptions import ClientError

from app_common.helpers.csv_helper import write_into_csv
from app_common.logger import Logger

s3_resources = boto3.resource('s3')
content_bucket = os.environ.get('content_bucket')
logger = Logger.create_logger(__name__)


def is_file_exists(file_key):
    # Get the service client.
    # Check whether file exists with the provided key or not
    try:
        logger.info(f'Looking for file {file_key} in bucket {content_bucket}')
        boto3.client('s3').head_object(
            Bucket=content_bucket, Key=file_key
        )
        return True
    except ClientError as ex:
        logger.info('File not found')
        print(ex)
        return False


def save_array_as_csv_on_contents_bucket(data, file_key):
    """
    Function will convert provide array in csv and
    :param data:
    :param file_key:
    :return:
    """
    if isinstance(data, list):
        file_obj = write_into_csv(data)
        response = s3_resources.Object(content_bucket, f'public/{file_key}').put(
            Body=file_obj.getvalue()
        )
        if response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200:
            return file_key
        logger.error('File saving on s3 failed:- ', response)
    else:
        logger.error('Data type should be list')
    raise Exception('CSV can\'t be generated at moment')
