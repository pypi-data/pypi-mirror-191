from app_common.db.common import CampaignStatus, DriverStatus
from app_common.db.models import CampaignDriverModel, CampaignModel
from app_common.logger import Logger

logger = Logger.create_logger(__name__)


def check_for_active_campaign(user_id):
    from app_common.db.models import CampaignDriverModel
    logger.info('under check_for_active_campaign')
    return CampaignDriverModel.exists(
        CampaignDriverModel.user_id == user_id,
        CampaignDriverModel.status == DriverStatus.ACTIVE.value
    )


def active_users_in_campaign():
    return {
        campaign_driver.user_id for campaign_driver in
        CampaignDriverModel.filter(
            CampaignDriverModel.active_status == DriverStatus.ACTIVE.value
        ).join(CampaignModel).filter(
            CampaignModel.status == CampaignStatus.ACTIVE.value
        ).with_entities(CampaignDriverModel.user_id)
    }
