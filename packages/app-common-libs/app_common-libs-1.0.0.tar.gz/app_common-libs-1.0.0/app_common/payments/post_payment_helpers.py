from app_common.db.common import CampaignTransitionStatus, NotificationSource, PaymentTypes
from app_common.db.common.constants import DriverStatus
from app_common.db.models import CampaignActivityModel, CampaignDriverModel, CampaignNotificationsModel
from app_common.logger import Logger

logger = Logger.create_logger(__name__)

# TODO this payment type need to change with initiated and later on stripe callback it can be done
PAYMENT_SUCCESS_STATUS_MAP = {
    PaymentTypes.ADVANCE: CampaignTransitionStatus.ADVANCE_PAYMENT_DONE.value,
    PaymentTypes.ADHOC: CampaignTransitionStatus.AD_HOC_PAYMENT_DONE.value,
    PaymentTypes.FULL: CampaignTransitionStatus.FINAL_PAYMENT_DONE.value,
    PaymentTypes.UNWRAP: CampaignTransitionStatus.FINAL_UNWRAP_PAYMENT_DONE.value,
}

PAYMENT_FAILED_STATUS_MAP = {
    PaymentTypes.ADVANCE: CampaignTransitionStatus.ADVANCE_PAYMENT_FAILED.value,
    PaymentTypes.ADHOC: CampaignTransitionStatus.AD_HOC_PAYMENT_FAILED.value,
    PaymentTypes.FULL: CampaignTransitionStatus.FINAL_PAYMENT_FAILED.value,
    PaymentTypes.UNWRAP: CampaignTransitionStatus.FINAL_UNWRAP_PAYMENT_FAILED.value,
}


def after_payment_initiated(driver_payment):
    """
    Update necessary object on payment initiation is success
    :param driver_payment: Driver payment object
    """
    try:
        transaction_id = driver_payment.transaction_id
        payment_type = driver_payment.payment_type
        status = (
                     transaction_id and PAYMENT_SUCCESS_STATUS_MAP.get(payment_type, None)
                 ) or PAYMENT_FAILED_STATUS_MAP.get(payment_type)
        logger.info(f'Under for payment type {payment_type} with status {status}')
        # If payment type is not Adhoc then only update the driver info
        if payment_type != PaymentTypes.ADHOC:
            update_campaign_driver_with_payment(status, driver_payment)
        trigger_notification(status, driver_payment)
    except Exception as ex:
        logger.error(ex)


def update_campaign_driver_with_payment(status, driver_payment):
    campaign_driver = CampaignDriverModel.get_filter(
        CampaignDriverModel.user_id == driver_payment.user_id,
        CampaignDriverModel.campaign_id == driver_payment.campaign_id,
    )
    total_payment_done = campaign_driver.total_payment_done or 0
    amount = round(driver_payment.amount / 100, 2)
    # if payment is success then only update the campaign total payment amount
    transaction_id = driver_payment.transaction_id
    if transaction_id:
        total_payment_done = round(total_payment_done + amount, 2)
    meta_data = {
        'reason': driver_payment.reason,
        'amount': amount,
        'transactionId': transaction_id,
        'status': status,
        'payment_uuid': driver_payment.id
    }
    if status not in (CampaignTransitionStatus.FINAL_UNWRAP_PAYMENT_FAILED.value, CampaignTransitionStatus.FINAL_UNWRAP_PAYMENT_DONE.value):
        campaign_driver.update_values(
            status=status,
            total_payment_done=total_payment_done,
            active_status=DriverStatus.ACTIVE.value,
            meta_data=meta_data
        )
    campaign_activity = CampaignActivityModel.add(
        campaign_id=driver_payment.campaign_id,
        user_id=driver_payment.user_id,
        meta_data=meta_data,
        status=status,
    )
    logger.info('campaign_activity obj created')
    logger.info(campaign_activity.as_dict())


def trigger_notification(status, driver_payment):
    transaction_id = driver_payment.transaction_id
    print('under push_notification_to_queue')
    amount = round(driver_payment.amount / 100, 2)
    source_type = [NotificationSource.ADMIN.value, NotificationSource.SELF.value]
    meta_data = {
        'reason': driver_payment.reason,
        'comment': driver_payment.comment,
        'amount': amount,
        'transactionId': transaction_id,
        'status': status,
        'payment_uuid': driver_payment.id
    }
    for val in source_type:
        CampaignNotificationsModel(
            user_id=driver_payment.user_id,
            campaign_id=driver_payment.campaign_id,
            status=status,
            source_type=val,
            meta_data=meta_data
        ).save()
    return True
