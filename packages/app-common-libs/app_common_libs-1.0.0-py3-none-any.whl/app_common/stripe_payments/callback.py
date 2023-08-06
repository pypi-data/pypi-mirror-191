from app_common.db.common import PaymentStatus
from app_common.db.models import DriverPaymentsModel, GlobalConfigModel
from app_common.logger import Logger
from app_common.payments.constants import PayoutStatus
from app_common.sqs_queues import send_message_on_queue_for_payment
from app_common.stripe_payments import base as stripe_handler
from app_common.stripe_payments.constants import (
    DEFAULT_FAILURE_RESPONSE, PAYOUT_FAILURE_MAP, StripeErrorCode
)
from app_common.stripe_payments.helpers import transaction_failure

STRIPE_TYPE_CHILD_PAYOUT = 'payout_failure'
STRIPE_TYPE_PAYMENT = 'payment'

logger = Logger.create_logger(__name__)


def payout_status(account_id, payout_id, arrival_date):
    """
    Get latest payout status using account if and payout id
    :param account_id: Customer account id
    :param arrival_date arrival_date: Payout arrival date
    :param payout_id: Payout id
    :return: latest payout status
    """
    # TODO need to check arrival_date in query filter first need to test with stag data then
    #  only implement this query filter
    logger.info(f'Arrival data {arrival_date}')
    payout = stripe_handler.retrieve_payout(
        account_id=account_id, payout_id=payout_id
    )
    p_status = payout.get('status')
    return (
        p_status in PayoutStatus.PAID and PaymentStatus.SUCCESS.value or
        p_status in PayoutStatus.FAILED and PaymentStatus.FAILED.value or
        None
    )


def get_payout_balance_transactions(customer_account_id, payout_id, balance_transactions=None):
    """
    Retrieve all balance transaction using payout id, the received payout id can be belong to a
    payout retry event so balance transaction id can be retrieve first getting payout ids in
    payout failed event
    :param customer_account_id: Customer account if for which payout event is received
    :param payout_id: payout id
    :param balance_transactions: list of balance transaction in case of multiple payout retried
    :return: Combined List of all balance transaction in a payout
    """
    balance_transactions = balance_transactions is not None and balance_transactions or []
    try:
        child_payouts = stripe_handler.list_balance_transactions(
            stripe_account=customer_account_id,
            payout=payout_id,
            type=STRIPE_TYPE_CHILD_PAYOUT
        )
        # If payout is a retry event for failed payout then get all the child payout and retrieve
        # balance transaction from the child payout objects
        if len(child_payouts) > 0:
            logger.info(f'Child payout found in {payout_id}:- {child_payouts}')
            for child_payout in child_payouts:
                child_payout_id = child_payout.get('source')
                transactions = get_payout_balance_transactions(
                    customer_account_id, child_payout_id, balance_transactions=[]
                )
                logger.info(f'Balance transactions found in {child_payout_id}:- {transactions}')
                balance_transactions.extend(transactions)

        # Also try to retrieve all payment try in this payout and
        # send back payment ids for updating status in DB
        balance_transactions.extend(stripe_handler.list_balance_transactions(
            stripe_account=customer_account_id,
            payout=payout_id,
            type=STRIPE_TYPE_PAYMENT
        ))
    except Exception as ex:
        logger.error(ex)
    return balance_transactions


def handle_payout_events(payload):
    customer_account_id = payload.get('account')
    payout_details = payload.get('data', {}).get('object', {})
    payout_id = payout_details.get('id')
    arrival_date = payout_details.get('arrival_date')

    p_status = payout_status(customer_account_id, payout_id, arrival_date)
    if not p_status:
        logger.warning(f'Received payout status for id ({payout_id}) is not required to handle')
        return
    balance_transactions = get_payout_balance_transactions(customer_account_id, payout_id)
    if not balance_transactions:
        return

    # Get all the payment history from DB for the payout
    all_payments_id = [bt.get('source') for bt in balance_transactions]
    logger.info(f'Received payment ids:- {all_payments_id}')
    payments = DriverPaymentsModel.filter(
        DriverPaymentsModel.payment_id.in_(all_payments_id)
    )

    if p_status == PaymentStatus.SUCCESS.value:
        handle_payout_paid(payout_details, payments)
    elif p_status == PaymentStatus.FAILED.value:
        handle_payout_failure(payout_details, payments)


def handle_payout_paid(payout_details, payments):
    for payment in payments:
        logger.info(f'Payment success for payment id {payment.id}')
        payment.update_values(
            status=PaymentStatus.SUCCESS.value,
            response_code=StripeErrorCode.SUCCESS,
            pg_response=payout_details,
            request_payload={}
        )


def handle_payout_failure(payout_details, payments):
    failure_code = payout_details.get('failure_code')
    if failure_code:
        failure_reason = PAYOUT_FAILURE_MAP.get(failure_code, DEFAULT_FAILURE_RESPONSE)
        for payment in payments:
            payment.update_values(
                status=PaymentStatus.FAILED.value,
                response_code=failure_reason.get('code'),
                pg_response=payout_details,
            )
            # Trigger slack notification
            transaction_failure(
                driver_email=payment.user.email,
                driver_name=payment.user.first_name,
                campaign_name=payment.campaign.name,
                payment_type=payment.payment_type,
                failure_message=failure_reason.get('message'),
                amount=payment.amount / 100,
            )
            logger.warning(f'Payment failed for the transfers with reason {failure_reason}')


def handle_balance_available(payload):
    balance_object = payload.get('data', {}).get('object', {})
    if not balance_object:
        return False
    available_balance = (
        len(balance_object.get('available')) > 0 and balance_object.get('available')[0] or {}
    )
    available_balance = available_balance.get('amount', 0)
    # Update global config as stripe account balance is loaded
    if available_balance > 0:
        GlobalConfigModel.insufficient_balance(False)

    # Get all the failed due to insufficient balance transaction from DB with amount less than
    # available balance in stripe account
    failed_payments = DriverPaymentsModel.filter(
        DriverPaymentsModel.status == PaymentStatus.FAILED.value,
        DriverPaymentsModel.response_code == StripeErrorCode.PAYOUT_BALANCE_INSUFFICIENT_ERR_CODE,
        DriverPaymentsModel.amount < available_balance
    )
    logger.info(f'Failed payments {failed_payments}')
    retry_payments(available_balance, failed_payments)


def retry_payments(available_balance, failed_payments):
    payment_initiated = []
    for payment in failed_payments:
        if available_balance >= payment.amount:
            response = send_message_on_queue_for_payment(payment.id)
            if response.get('code') == 200:
                payment_initiated.append(payment.id)
                logger.info(f'SQS push successful {response}')
                available_balance -= payment.amount
        else:
            logger.info(f'Balance insufficient for :- {payment}')

    logger.info(f'Payment initiated for objects with id:- {payment_initiated}')
