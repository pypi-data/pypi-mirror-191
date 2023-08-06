def migrate():
    from app_common.db.models import (
        BaseModel, DriverPaymentsModel, CampaignDriverModel, CampaignActivityModel, CampaignNotificationsModel
    )
    from app_common.db.common import CampaignTransitionStatus, PaymentTypes

    session = BaseModel.session()
    try:

        transition_status = tuple(CampaignTransitionStatus.values_list())
        payment_types = tuple(PaymentTypes.values_list())
        for table in (CampaignDriverModel, CampaignActivityModel, CampaignNotificationsModel):
            session.execute(
                f"ALTER TABLE {table.__tablename__} MODIFY COLUMN status ENUM{transition_status}"
            )
        session.execute(
            f"ALTER TABLE {DriverPaymentsModel.__tablename__} MODIFY COLUMN payment_type ENUM{payment_types}"
        )
    except Exception as ex:
        session.rollback()
        raise ex
