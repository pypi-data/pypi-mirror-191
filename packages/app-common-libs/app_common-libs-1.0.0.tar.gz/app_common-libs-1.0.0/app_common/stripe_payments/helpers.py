from app_common.config.base import SITE_BASE_URL, SLACK_PAYMENT_CHANNEL, STRIPE_BASE_URL
from app_common.logger import Logger
from app_common.providers.slack import SlackMessageBuilder
from app_common.stripe_payments.constants import StripeErrorCode

DRIVER_URL = f'{SITE_BASE_URL}drivers?q_email=%s'
STRIPE_TOP_UP_URL = f'{STRIPE_BASE_URL}payments?status%5B%5D=successful'
logger = Logger.create_logger(__name__)
STRIPE_MESSAGES = {
    StripeErrorCode.PAYOUT_BALANCE_INSUFFICIENT_ERR_CODE: {
        'heading': 'Stripe balance is insufficient',
        'sub_heading': (
            'Trying to initiate transaction amount ${transaction_amount} but balance in stripe '
            'account is insufficient, Please top-up account with required balance.'
        ),

    },
    StripeErrorCode.PAYOUT_FAILED: {
        'heading': 'Payment transfer failed',
        'sub_heading': 'Please check the details',
        'message': (
            'Driver:- {driver_name}({driver_email})\n\n'
            'Campaign:- {campaign_name}\n\n'
            'Payment Type:- {payment_type}\n\n'
            'Amount:- ${amount}\n\n'
            'Failure Message:- {failure_message}\n\n'
        ),
    }
}


def balance_is_insufficient(**kwargs):
    from app_common.db.models import GlobalConfigModel
    logger.info('Inside Slack notification balance_is_insufficient')
    if GlobalConfigModel.is_triggered_insufficient_balance():
        logger.info('Slack notification is already triggered for the event')
        return
    # Trigger slack notification on insufficient balance
    message_dict = STRIPE_MESSAGES.get(StripeErrorCode.PAYOUT_BALANCE_INSUFFICIENT_ERR_CODE)
    heading = message_dict.get("heading")
    sub_heading = message_dict.get('sub_heading').format(**kwargs)
    SlackMessageBuilder(f'>*{heading}*').add_line(
        f'\n{sub_heading}'
    ).add_redirection_button().add_redirection_url(
        'Top-up', STRIPE_TOP_UP_URL
    ).end().post(channel=SLACK_PAYMENT_CHANNEL)
    GlobalConfigModel.insufficient_balance()
    logger.info(f'Balance insufficient notification trigger on slack {SLACK_PAYMENT_CHANNEL}')


def transaction_failure(**kwargs):
    logger.info(f'Inside Slack notification transaction failure for {kwargs}')
    # Trigger slack notification on transaction failure
    message_dict = STRIPE_MESSAGES.get(StripeErrorCode.PAYOUT_FAILED)
    heading = message_dict.get("heading")
    sub_heading = message_dict.get('sub_heading')
    message = message_dict.get('message').format(**kwargs)
    SlackMessageBuilder(f'>*{heading}*').add_line(
        f'\n{sub_heading}'
    ).add_line(f'\n{message}').add_redirection_button().add_redirection_url(
        'Driver info', DRIVER_URL % kwargs.get('driver_email', '')
    ).end().post(channel=SLACK_PAYMENT_CHANNEL)
    logger.info(f'Payment failed notification trigger on slack {SLACK_PAYMENT_CHANNEL}')
