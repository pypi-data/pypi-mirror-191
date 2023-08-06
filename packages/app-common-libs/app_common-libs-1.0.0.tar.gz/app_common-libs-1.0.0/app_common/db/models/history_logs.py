from sqlalchemy import BigInteger, Column, Enum, ForeignKey, String
from sqlalchemy.orm import relationship

from app_common.db.base import BaseModel
from app_common.db.common import CampaignTransitionStatus, JsonField, Tables

ALLOWED_CAMPAIGN_ACTIVITY_STATUS = (
    CampaignTransitionStatus.APPLIED.value,
    CampaignTransitionStatus.APPROVED.value,
    CampaignTransitionStatus.REJECTED.value,
    CampaignTransitionStatus.WRAP_SCHEDULED.value,
    CampaignTransitionStatus.PENDING_WRAP_APPROVAL.value,
    CampaignTransitionStatus.WRAP_REJECTED.value,
    CampaignTransitionStatus.WRAP_APPROVED.value,
    CampaignTransitionStatus.ADVANCE_PAYMENT_DONE.value,
    CampaignTransitionStatus.ADVANCE_PAYMENT_FAILED.value,
    CampaignTransitionStatus.CAMPAIGN_IN_PROGRESS.value,
    CampaignTransitionStatus.CAMPAIGN_FINISHED.value,
    CampaignTransitionStatus.PENDING_END_WRAP_APPROVAL.value,
    CampaignTransitionStatus.END_WRAP_APPROVED.value,
    CampaignTransitionStatus.END_WRAP_REJECTED.value,
    CampaignTransitionStatus.PENDING_UNWRAP_APPROVAL.value,
    CampaignTransitionStatus.UNWRAP_SCHEDULED.value,
    CampaignTransitionStatus.UNWRAP_APPROVED.value,
    CampaignTransitionStatus.UNWRAP_REJECTED.value,
    CampaignTransitionStatus.FINAL_PAYMENT_DONE.value,
    CampaignTransitionStatus.FINAL_PAYMENT_FAILED.value,
    CampaignTransitionStatus.REMOVED.value,
    CampaignTransitionStatus.UNDO_REMOVED.value,
    CampaignTransitionStatus.FINAL_UNWRAP_PAYMENT_DONE.value,
    CampaignTransitionStatus.FINAL_UNWRAP_PAYMENT_FAILED.value,
)


class CampaignActivityModel(BaseModel):
    __tablename__ = Tables.CAMPAIGN_ACTIVITY.value
    # Field description
    campaign_id = Column(
        'campaign_id', ForeignKey(f'{Tables.CAMPAIGNS.value}.id', ondelete='CASCADE')
    )
    user_id = Column('user_id', ForeignKey(f'{Tables.DRIVERS.value}.id', ondelete='CASCADE'))
    meta_data = Column('meta_data', JsonField())
    status = Column(
        'status', Enum(CampaignTransitionStatus, values_callable=CampaignTransitionStatus.values)
    )
    user = relationship('DriverUserModel', foreign_keys=[user_id])

    @staticmethod
    def add(campaign_id, user_id, meta_data, status):
        if status in ALLOWED_CAMPAIGN_ACTIVITY_STATUS:
            campaign_activity = CampaignActivityModel(
                user_id=user_id,
                campaign_id=campaign_id,
                status=status,
                meta_data=meta_data,
            ).save()
            return campaign_activity
        return CampaignActivityModel()


class HistoryLogModel(BaseModel):
    __tablename__ = Tables.HISTORY_LOG.value
    # Field description
    # __table_args__ = (Index('history_fields', "ref_table", 'ref_id'),)
    ref_table = Column('ref_table', String(50))
    # mapped foreign key using ids of payment table as currently payment history is only kept
    ref_id = Column('ref_id', BigInteger())
    field = Column('field', String(50))
    new_value = Column('new_value', String(512))
    old_value = Column('old_value', String(512))
