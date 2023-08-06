from sqlalchemy import (
    Boolean, Column, Date, DateTime, Enum, Float, ForeignKey, Integer, String, Text
)
from sqlalchemy.orm import relationship

from app_common.db.base import BaseModel
from app_common.db.common import (
    CampaignStatus, CampaignTransitionStatus, DriverStatus, JsonField, LocationPermissionStatus,
    Tables, TimestampField, ReportStatus
)


class CampaignModel(BaseModel):
    __tablename__ = Tables.CAMPAIGNS.value
    # Field description
    name = Column('name', String(250))
    brand_id = Column('brand_id', ForeignKey(f'{Tables.BRANDS.value}.id', ondelete='CASCADE'))
    campaign_type = Column('campaign_type', String(250))
    city_id = Column('city_id', Integer())
    city = Column('city', String(250))
    city_center = Column('city_center', Text())
    status = Column(
        'status', Enum(CampaignStatus, values_callable=CampaignStatus.values)
    )
    amount_per_car = Column('amount_per_car', Integer())
    number_of_drivers = Column('number_of_drivers', Integer())
    client_price = Column('client_price', Integer())
    total_estimated = Column('total_estimated', Integer())
    upfront_payment = Column('upfront_payment', Integer())
    description = Column('description', Text())
    audience = Column('audience', JsonField())
    published_at = Column('published_at', TimestampField())
    end_date = Column('end_date', Date())
    start_date = Column('start_date', Date())
    wrap_end_date = Column('wrap_end_date', Date())
    wrap_start_date = Column('wrap_start_date', Date())
    reports_generated = Column('reports_generated', Boolean(), default=False)
    reports_status = Column(
        'reports_status', Enum(ReportStatus, values_callable=ReportStatus.values),
        default=ReportStatus.TODO.value
    )
    # Foreign key relationship
    brand = relationship('BrandModel', foreign_keys=[brand_id])
    wrap_schedules = relationship(
        "CampaignWrapLocationsModel",
        primaryjoin="and_(CampaignWrapLocationsModel.campaign_id==CampaignModel.id, "
                    "CampaignWrapLocationsModel.is_wrap_location==True)"
    )
    unwrap_schedules = relationship(
        "CampaignWrapLocationsModel",
        primaryjoin="and_(CampaignWrapLocationsModel.campaign_id==CampaignModel.id, "
                    "CampaignWrapLocationsModel.is_wrap_location==False)"
    )
    schedules = relationship(
        "CampaignWrapLocationsModel",
        primaryjoin="CampaignWrapLocationsModel.campaign_id==CampaignModel.id"
    )
    appointments = relationship(
        "CampaignWrapAppointmentsModel",
        primaryjoin="CampaignWrapAppointmentsModel.campaign_id==CampaignModel.id"
    )
    drivers = relationship(
        "CampaignDriverModel",
        primaryjoin="CampaignDriverModel.campaign_id==CampaignModel.id"
    )

    @classmethod
    def report_available_campaigns(cls, brand_id, as_dict=True):
        campaigns = cls.filter(
            cls.brand_id == brand_id,
            cls.reports_generated == True
        ).order_by(cls.id.desc())
        return [campaign.as_dict() if as_dict else campaign for campaign in campaigns]

    @classmethod
    def latest_report_available_campaign(cls, brand_id):
        return cls.filter(
            cls.brand_id == brand_id,
            cls.reports_generated == True
        ).order_by(cls.id.desc()).first()


class CampaignDriverModel(BaseModel):
    __tablename__ = Tables.CAMPAIGN_DRIVER.value
    # Field description
    campaign_id = Column(
        'campaign_id', ForeignKey(f'{Tables.CAMPAIGNS.value}.id', ondelete='CASCADE')
    )
    user_id = Column('user_id', ForeignKey(f'{Tables.DRIVERS.value}.id', ondelete='CASCADE'))
    active_status = Column(
        'active_status', Enum(DriverStatus, values_callable=DriverStatus.values),
        default=DriverStatus.ACTIVE.value
    )
    status = Column(
        'status', Enum(CampaignTransitionStatus, values_callable=CampaignTransitionStatus.values)
    )
    start_association_time = Column('start_association_time', DateTime())
    end_association_time = Column('end_association_time', DateTime())
    total_payment_done = Column('total_payment_done', Float(precision=2), default=0)
    total_time_driven = Column('total_time_driven', Float(precision=2), default=0)
    is_self_unwrap = Column('is_self_unwrap', Boolean(), default=False)

    # Foreign key relation ship model
    user = relationship('DriverUserModel', foreign_keys=[user_id])


class CampaignDriverLocationPermissionModel(BaseModel):
    __tablename__ = Tables.CAMPAIGN_DRIVER_LOCATIONS_PERMISSION.value
    campaign_id = Column(
        'campaign_id', ForeignKey(f'{Tables.CAMPAIGNS.value}.id', ondelete='CASCADE')
    )
    user_id = Column('user_id', ForeignKey(f'{Tables.DRIVERS.value}.id', ondelete='CASCADE'))
    permission_type = Column(
        'permission_type',
        Enum(LocationPermissionStatus, values_callable=LocationPermissionStatus.values)
    )
