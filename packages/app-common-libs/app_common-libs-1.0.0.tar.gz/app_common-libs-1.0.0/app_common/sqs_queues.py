import json
import os

import boto3

from app_common.constants import ApiErrorCode
from app_common.logger import Logger
from app_common.db.common import PaymentStatus

logger = Logger.create_logger(__name__)


def push_to_queue_for_notifications(notification_id):
    logger.info('pushing to queue')
    sqs_client = boto3.client('sqs')
    sqs_queue_url = os.environ['notificationQ']
    logger.info(os.environ['notificationQ'])
    queue_payload = {'notification_id': notification_id}
    msg = sqs_client.send_message(
        QueueUrl=sqs_queue_url,
        MessageBody=json.dumps(queue_payload)
    )
    return msg


def push_to_queue_for_campaigns(campaign_id):
    logger.info('pushing to new campaign queue')
    sqs_client = boto3.client('sqs')
    sqs_queue_url = os.environ['newCampQ']
    queue_payload = {'campaign_id': campaign_id}
    msg = sqs_client.send_message(
        QueueUrl=sqs_queue_url,
        MessageBody=json.dumps(queue_payload)
    )
    logger.info('post push')
    logger.info(msg)
    return msg


def send_message_on_queue_for_payment(payment_id):
    logger.info('before send')
    try:
        queue_payload = {'payment_id': payment_id}
        sqs_client = boto3.client('sqs')

        sqs_queue_url = os.environ['paymentQ']
        msg = sqs_client.send_message(
            QueueUrl=sqs_queue_url,
            MessageBody=json.dumps(queue_payload)
        )
        logger.info('post sent')
        if msg['ResponseMetadata']['HTTPStatusCode'] == ApiErrorCode.OK:
            return {
                'code': ApiErrorCode.OK,
                'data': payment_id,
                'message': PaymentStatus.SUCCESS.value
            }
    except Exception as ex:
        logger.error(str(ex))
    return {
        'code': ApiErrorCode.FAILURE,
        'data': payment_id,
        'message': 'Push to Queue Failed.'
    }


def push_locations_in_to_aurora_queue(payload):
    if len(json.dumps(payload).encode('utf-8')) > 250000:
        half = int(len(payload) / 2)
        return push_locations_in_to_aurora_queue(
            payload[:half]
        ) and push_locations_in_to_aurora_queue(payload[half:])
    else:
        logger.info('pushing to location queue for aurora db operation')
        queue_payload = json.dumps(payload)
        print('queue_payload:- ', queue_payload)
        sqs_client = boto3.client('sqs')
        sqs_queue_url = os.environ['locationsQ']
        msg = sqs_client.send_message(
            QueueUrl=sqs_queue_url,
            MessageBody=queue_payload
        )
        logger.info('post push')
        logger.info(msg)
        return True
