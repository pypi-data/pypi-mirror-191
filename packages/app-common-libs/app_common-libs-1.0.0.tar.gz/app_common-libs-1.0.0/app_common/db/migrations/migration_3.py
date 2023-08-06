def migrate():
    from app_common.db.common import CampaignTransitionStatus
    from app_common.db.models import (
        BaseModel, CampaignDriverModel, CampaignActivityModel, CampaignNotificationsModel
    )
    session = BaseModel.session()
    try:
        # noinspection PyTypeChecker
        status = tuple(CampaignTransitionStatus.values_list())
        for table in (CampaignDriverModel, CampaignActivityModel, CampaignNotificationsModel):
            session.execute(
                f"ALTER TABLE {table.__tablename__} MODIFY COLUMN status ENUM{status}"
            )
    except Exception as ex:
        session.rollback()
        raise ex
