import os

SITE_BASE_URL = 'http://localhost:8000/'
STRIPE_BASE_URL = 'https://dashboard.stripe.com/test/'
SLACK_PAYMENT_CHANNEL = 'payment-notification-dev'
SLACK_LOCATION_PERMISSION = 'location-permission-dev'
SLACK_BUGS_CHANNEL = 'api-errors-dev'
SLACK_FAQ_CHANNEL = 'faq-support-dev'
IS_PROD = os.environ.get('environment') == 'prod'
if IS_PROD:
    from app_common.config.prod import *
else:
    from app_common.config.stage import *
print(CONFIG_MESSAGE)
