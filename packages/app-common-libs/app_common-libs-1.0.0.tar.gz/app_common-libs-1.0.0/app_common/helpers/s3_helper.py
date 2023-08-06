import boto3
from botocore.exceptions import ClientError

from app_common.logger import Logger

logger = Logger.create_logger(__name__)


def s3_presigned_read_url(bucket, file_key):
    # Get the service client.
    # Generate the URL to get 'key-name' from 'bucket-name'
    return boto3.client('s3').generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket,
            'Key': file_key
        },
    )


def upload_s3_file(bucket, file_body, file_key):
    """
        Upload a file to an S3 bucket
        :param file_key: File to upload
        :param bucket: Bucket to upload to
        :param file_body: file byte stream body
        :return: True if file was uploaded, else False
    """
    # Upload the file
    try:
        s3_resources = boto3.resource('s3')
        s3_resources.Object(bucket, file_key).put(Body=file_body)
    except ClientError as e:
        logger.error(e)
        return False
    return True
