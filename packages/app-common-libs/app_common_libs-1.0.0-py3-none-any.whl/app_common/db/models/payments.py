from sqlalchemy import Column, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app_common.db.base import BaseModel
from app_common.db.common import JsonField, PaymentStatus, PaymentTypes, Tables


class DriverPaymentsModel(BaseModel):
    __tablename__ = Tables.DRIVER_PAYMENTS.value
    # Field description
    campaign_id = Column(
        'campaign_id',
        ForeignKey(f'{Tables.CAMPAIGNS.value}.id', ondelete='CASCADE')
    )
    user_id = Column('user_id', ForeignKey(f'{Tables.DRIVERS.value}.id', ondelete='CASCADE'))
    transaction_id = Column(
        'transaction_id', String(250), doc='Transaction id is received from stripe'
    )
    payment_id = Column(
        'payment_id', String(250), doc='Payment id is received from stripe on payout'
    )
    payment_uuid = Column(
        'payment_uuid', String(250), doc='TODO Should be removed not in use anymore'
    )
    amount = Column('amount', Float())
    payment_type = Column(
        'payment_type', Enum(PaymentTypes, values_callable=PaymentTypes.values)
    )
    reason = Column('reason', Text())
    comment = Column('comment', Text())
    response_code = Column('response_code', Integer())
    status = Column('status', Enum(PaymentStatus, values_callable=PaymentStatus.values))
    request_payload = Column('request_payload', JsonField())
    pg_response = Column('pg_response', JsonField())

    # Foreign key relationship
    campaign = relationship('CampaignModel', foreign_keys=[campaign_id])
    user = relationship('DriverUserModel', foreign_keys=[user_id])

    class Meta(BaseModel.Meta):
        HISTORY_FIELDS = ['status']
