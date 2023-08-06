import uuid

from app_common.db.common import PaymentStatus, PaymentTypes
from app_common.db.models import CampaignDriverModel
from app_common.logger import Logger
from app_common.sqs_queues import send_message_on_queue_for_payment
from app_common.stripe_payments.constants import StripeErrorCode

logger = Logger.create_logger(__name__)


def initiate_payment(user, campaign, campaign_diver, **kwargs):
    custom_account_id = user.payment.get('stripe_account_id')
    queue_payload = {
        'payment_payload': {
            'amount': kwargs.get('amount'),
            'currency': 'usd',
            'destination': custom_account_id,
            'transfer_group': campaign.name,
            'metadata': {
                'user_id': user.id,
                'campaign_id': campaign.id,
                'payment_uuid': str(uuid.uuid4())
            }
        },
    }
    kwargs['request_payload'] = queue_payload
    # Insert into payment history for the initiated payment with the status INITIATED
    driver_payment = insert_into_payment_history(campaign_diver, **kwargs)

    response = send_message_on_queue_for_payment(driver_payment.id)
    if response['code'] != 200:
        # Change status in payment history table as push to queue is failed
        driver_payment.status = PaymentStatus.FAILED.value
        driver_payment.response_code = StripeErrorCode.PAYOUT_FAILED
        driver_payment.pg_response = response['message']
        driver_payment.update()
    logger.info(driver_payment)
    return response


def insert_into_payment_history(campaign_driver: CampaignDriverModel, **kwargs):
    from app_common.db.models import DriverPaymentsModel
    logger.info('under payment history')
    logger.info(kwargs)
    req_payload = kwargs.get('request_payload')
    try:
        return DriverPaymentsModel(
            campaign_id=campaign_driver.campaign_id,
            user_id=campaign_driver.user_id,
            payment_uuid=req_payload.get('payment_payload').get('metadata').get('payment_uuid'),
            status=PaymentStatus.INITIATED.value,
            amount=kwargs.get('amount'),
            payment_type=kwargs.get('payment_type'),
            reason=kwargs.get('reason'),
            comment=kwargs.get('comment'),
            response_code=StripeErrorCode.PAYOUT_INITIATED,
            request_payload=req_payload
        ).save()
    except Exception as ex:
        logger.error(f'Error in insert payment history {ex}')
        raise ex


def get_adhoc_amount(amount, *args):
    return int(amount * 100)


def get_advance_payment_amount(campaign, *args):
    amount = campaign.amount_per_car * (campaign.upfront_payment / 100)
    return int(amount * 100)


def get_full_payment_amount(campaign, campaign_driver):
    logger.info('look')
    logger.info(campaign_driver.as_dict())
    amount = campaign.amount_per_car - (campaign.amount_per_car * (campaign.upfront_payment / 100))
    amount_in_cents = int(amount * 100)
    return amount_in_cents


def get_bonus_payment_amount(campaign, campaign_driver):
    logger.info('look')
    logger.info(campaign_driver.as_dict())
    if campaign_driver.is_self_unwrap:
        amount_in_cents = 1000
        return amount_in_cents
    return False



PAYMENT_TYPE_AMOUNT = {
    PaymentTypes.ADVANCE.value: get_advance_payment_amount,
    PaymentTypes.FULL.value: get_full_payment_amount,
    PaymentTypes.UNWRAP.value: get_bonus_payment_amount,
}


def check_for_existing_payment(amount, user_id, campaign, campaign_diver, payment_type):
    if payment_type in (PaymentTypes.ADVANCE.value, PaymentTypes.FULL.value, PaymentTypes.UNWRAP.value):
        from app_common.db.models import DriverPaymentsModel
        logger.info('under check for payment')
        DriverPaymentsModel.exists(
            DriverPaymentsModel.user_id == user_id,
            DriverPaymentsModel.campaign_id == campaign.id,
            DriverPaymentsModel.payment_type == payment_type,
            DriverPaymentsModel.status.in_(
                [PaymentStatus.SUCCESS.value, PaymentStatus.INITIATED.value]
            ),
            raise_on_exists=True,
            message=f'{payment_type} payment is already triggered for the driver in campaign'
        )
        return PAYMENT_TYPE_AMOUNT.get(payment_type)(campaign, campaign_diver)
    elif payment_type == PaymentTypes.ADHOC.value:
        return get_adhoc_amount(amount)
    raise Exception(f'Payment type({payment_type}) not supported')
