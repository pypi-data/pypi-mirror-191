import json
import os

import stripe

from app_common.db.models import PaymentStatus
from app_common.logger import Logger
from app_common.stripe_payments.constants import BALANCE_INSUFFICIENT_ERR_CODE, StripeErrorCode
from app_common.stripe_payments.helpers import balance_is_insufficient

api_key = os.environ.get('stripe_key')
stripe.api_key = api_key
logger = Logger.create_logger(__name__)


def list_all_account(limit=10):
    return stripe.Account.list(limit=limit).get('data')


def list_balance_transactions(**kwargs):
    try:
        return stripe.BalanceTransaction.list(**kwargs).get('data', [])
    except Exception as ex:
        logger.warning(f'{str(ex)}')
    return []


def retrieve_payout(account_id, payout_id):
    try:
        payout_list = stripe.Payout.list(stripe_account=account_id).get('data', [])
        for payout in payout_list:
            if payout.get('id') == payout_id:
                return payout
    except Exception as ex:
        logger.warning(f'{str(ex)}')
    return None


def create_account(**kwargs):
    try:
        response = stripe.Account.create(**kwargs)
        logger.info("testing")
        response = json.dumps(response)
        create_account_response = json.loads(response)
        logger.info(create_account_response)
        return create_account_response
    except Exception as ex:
        logger.error(ex)


def update_account(stripe_account_id, **kwargs):
    try:
        logger.info("Under update call")
        response = stripe.Account.modify(str(stripe_account_id), **kwargs)
        response = json.dumps(response)
        update_account_response = json.loads(response)
        logger.info(update_account_response)
        return update_account_response
    except Exception as ex:
        logger.error(ex)


def transfer_payment(payment_payload):
    payment_amount = payment_payload.get('amount')
    if stripe_balance() >= payment_amount:
        try:
            response = stripe.Transfer.create(**payment_payload)
            response = json.dumps(response)
            transfer_to_account_response = json.loads(response)
            logger.info(transfer_to_account_response)
            return {
                'id': transfer_to_account_response.get('id'),
                'payment_id': transfer_to_account_response.get('destination_payment'),
                'status': PaymentStatus.INITIATED.value,
                'code': StripeErrorCode.SUCCESS,
            }
        except Exception as ex:
            logger.error(ex)
            return {
                'status': PaymentStatus.FAILED.value,
                'message': str(ex),
                'code': StripeErrorCode.PAYOUT_FAILED
            }
    else:
        # Trigger slack notification for balance is insufficient
        balance_is_insufficient(transaction_amount=round(payment_amount / 100, 2))
    return {
        'message': f'Insufficient balance in account for the transaction amount {payment_amount}',
        'status': PaymentStatus.FAILED.value,
        'code': StripeErrorCode.PAYOUT_BALANCE_INSUFFICIENT_ERR_CODE
    }


def handle_payout_failure(payload):
    if payload.code == BALANCE_INSUFFICIENT_ERR_CODE:
        logger.error('Low balance stop here.')
    else:
        logger.error(f'error in initiate payout with code {payload.code}')


def stripe_balance():
    available_balances = stripe.Balance.retrieve().get('available', {})
    return (len(available_balances) > 0 and available_balances[0]).get('amount', 0) or 0
