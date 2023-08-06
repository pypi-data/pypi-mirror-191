from sqlalchemy import Column, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship

from app_common.db.base import BaseModel
from app_common.db.common import (
    CampaignTransitionStatus, JsonField, NotificationSource, Tables, TimestampField
)


class CampaignNotificationsModel(BaseModel):
    __tablename__ = Tables.CAMPAIGN_NOTIFICATIONS.value
    # Field description
    campaign_id = Column(
        'campaign_id', ForeignKey(f'{Tables.CAMPAIGNS.value}.id', ondelete='CASCADE')
    )
    # Driver id from dynamo table is stored as user id in here
    user_id = Column('user_id', ForeignKey(f'{Tables.DRIVERS.value}.id', ondelete='CASCADE'))
    status = Column(
        'status', Enum(CampaignTransitionStatus, values_callable=CampaignTransitionStatus.values)
    )
    source_type = Column(
        'source_type', Enum(NotificationSource, values_callable=NotificationSource.values)
    )
    seen_at = Column('seen_at', TimestampField())
    message = Column('message', Text())
    meta_data = Column('meta_data', JsonField())
    sns_response = Column('sns_response', JsonField())

    # Foreign key relationship
    campaign = relationship('CampaignModel', foreign_keys=[campaign_id])
    user = relationship('DriverUserModel', foreign_keys=[user_id])

    def post_create(self):
        from app_common.sqs_queues import push_to_queue_for_notifications
        """
        On creation of instance trigger event for the notification
        """
        sns_response = push_to_queue_for_notifications(self.id)
        self.update_values(sns_response=sns_response)
