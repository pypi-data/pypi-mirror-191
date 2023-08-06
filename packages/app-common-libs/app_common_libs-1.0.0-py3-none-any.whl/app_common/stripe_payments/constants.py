class StripeErrorCode:
    PAYOUT_INITIATED = 201
    SUCCESS = 200
    PAYOUT_FAILED = 5000  # Failure reason is not provided by stripe
    PAYOUT_FAILED_ACCOUNT_CLOSED = 5001
    PAYOUT_FAILED_ACCOUNT_FROZEN = 5002
    PAYOUT_FAILED_BANK_ACCOUNT_RESTRICTED = 5003
    PAYOUT_FAILED_BANK_OWNERSHIP_CHANGED = 5004
    PAYOUT_FAILED_COULD_NOT_PROCESS = 5005
    PAYOUT_FAILED_DEBIT_NOT_AUTHORIZED = 5006
    PAYOUT_FAILED_DECLINED = 5007
    PAYOUT_FAILED_INSUFFICIENT_FUNDS = 5008
    PAYOUT_FAILED_INVALID_ACCOUNT_NUMBER = 5009
    PAYOUT_FAILED_INCORRECT_ACCOUNT_HOLDER_NAME = 5010
    PAYOUT_FAILED_INVALID_CURRENCY = 5011
    PAYOUT_FAILED_NO_ACCOUNT = 5012
    PAYOUT_BALANCE_INSUFFICIENT_ERR_CODE = 5013


BALANCE_INSUFFICIENT_ERR_CODE = 'balance_insufficient'
DEFAULT_FAILURE_RESPONSE = 'stripe.unknownError'

PAYOUT_FAILURE_MAP = {
    'account_closed': {
        'code': StripeErrorCode.PAYOUT_FAILED_ACCOUNT_CLOSED,
        'message': 'The bank account has been closed.'
    },
    'account_frozen': {
        'code': StripeErrorCode.PAYOUT_FAILED_ACCOUNT_FROZEN,
        'message': 'The bank account has been frozen.'
    },
    'bank_account_restricted': {
        'code': StripeErrorCode.PAYOUT_FAILED_BANK_ACCOUNT_RESTRICTED,
        'message': 'The bank account has restrictions on either the type, or the number, '
                   'of payouts allowed. This normally indicates that the bank account is a '
                   'savings or other non-checking account.'
    },
    'bank_ownership_changed': {
        'code': StripeErrorCode.PAYOUT_FAILED_BANK_OWNERSHIP_CHANGED,
        'message': 'The destination bank account is no longer valid because its branch has '
                   'changed ownership.'
    },
    'could_not_process': {
        'code': StripeErrorCode.PAYOUT_FAILED_COULD_NOT_PROCESS,
        'message': 'The bank could not process this payout.'
    },
    'debit_not_authorized': {
        'code': StripeErrorCode.PAYOUT_FAILED_DEBIT_NOT_AUTHORIZED,
        'message': 'Debit transactions are not approved on the bank account. (Stripe requires '
                   'bank accounts to be set up for both credit and debit payouts.)'
    },
    'declined': {
        'code': StripeErrorCode.PAYOUT_FAILED_DECLINED,
        'message': 'The bank has declined this transfer. Please contact the bank before retrying.'
    },
    'insufficient_funds': {
        'code': StripeErrorCode.PAYOUT_FAILED_INSUFFICIENT_FUNDS,
        'message': 'Your account has insufficient funds to cover the transfer.'
    },
    'invalid_account_number': {
        'code': StripeErrorCode.PAYOUT_FAILED_INVALID_ACCOUNT_NUMBER,
        'message': 'The routing number seems correct, but the account number is invalid.'
    },
    'incorrect_account_holder_name': {
        'code': StripeErrorCode.PAYOUT_FAILED_INCORRECT_ACCOUNT_HOLDER_NAME,
        'message': 'Your bank notified us that the bank account holder name on file is incorrect.'
    },
    'invalid_currency': {
        'code': StripeErrorCode.PAYOUT_FAILED_INVALID_CURRENCY,
        'message': 'The bank was unable to process this payout because of its currency. This is '
                   'probably because the bank account cannot accept payments in that currency.'
    },
    'no_account': {
        'code': StripeErrorCode.PAYOUT_FAILED_NO_ACCOUNT,
        'message': 'The bank account details on file are probably incorrect. No bank account '
                   'could be located with those details.'
    },
    BALANCE_INSUFFICIENT_ERR_CODE: {
        'code': StripeErrorCode.PAYOUT_BALANCE_INSUFFICIENT_ERR_CODE,
        'message': 'Your Stripe account has insufficient funds to cover the transfer.'
    },
    DEFAULT_FAILURE_RESPONSE: {
        'code': StripeErrorCode.PAYOUT_FAILED,
        'message': 'Failed reason is not provided by payment gateway.'
    },

}
