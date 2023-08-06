from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app_common.db.base import BaseModel
from app_common.db.common import JsonField, Tables, TimestampField


class CampaignWrapLocationsModel(BaseModel):
    __tablename__ = Tables.CAMPAIGN_WRAP_LOCATIONS.value
    # Field description
    name = Column('name', String(250))
    campaign_id = Column('campaign_id', ForeignKey(f'{Tables.CAMPAIGNS.value}.id'))
    is_wrap_location = Column('is_wrap_location', Boolean(), default=True)
    locationName = Column('locationName', String(250))
    locationNotes = Column('locationNotes', String(250))
    lat = Column('lat', Float())
    long = Column('long', Float())
    multiplicity = Column('multiplicity', Integer(), default=0)
    availableHours = Column('availableHours', JsonField())
    slots = Column('slots', JsonField())
    startDate = Column('startDate', Date())
    endDate = Column('endDate', Date())
    timezone_id = Column('timezone_id', String(50))
    # Foreign key relationship
    campaign = relationship('CampaignModel', foreign_keys=[campaign_id])


class CampaignWrapAppointmentsModel(BaseModel):
    __tablename__ = Tables.CAMPAIGN_WRAP_APPOINTMENT.value
    # Field description
    campaign_id = Column(
        'campaign_id',
        ForeignKey(f'{Tables.CAMPAIGNS.value}.id', ondelete='CASCADE')
    )
    user_id = Column('user_id', ForeignKey(f'{Tables.DRIVERS.value}.id', ondelete='CASCADE'))
    campaign_driver_id = Column(
        'campaign_driver_id', ForeignKey(f'{Tables.CAMPAIGN_DRIVER.value}.id', ondelete='CASCADE')
    )
    wrap_location_id = Column(
        'wrap_location_id',
        ForeignKey(f'{Tables.CAMPAIGN_WRAP_LOCATIONS.value}.id', ondelete='CASCADE'),
        default=None
    )
    is_wrap_appointment = Column('is_wrap_appointment', Boolean(), default=True)
    wrap_date = Column('wrap_date', Date())
    slot_timing = Column('slot_timing', String(10))

    # Foreign key relationship
    campaign = relationship('CampaignModel', foreign_keys=[campaign_id])
    user = relationship('DriverUserModel', foreign_keys=[user_id])
    wrap_location = relationship('CampaignWrapLocationsModel', foreign_keys=[wrap_location_id])


class RideShiftRecordsModel(BaseModel):
    __tablename__ = Tables.RIDE_SHIFT_RECORDS.value
    # Field description
    campaign_id = Column('campaign_id', ForeignKey(f'{Tables.CAMPAIGNS.value}.id'))
    user_id = Column('user_id', ForeignKey(f'{Tables.DRIVERS.value}.id'))
    start_time = Column('start_time', TimestampField())
    end_time = Column('end_time', TimestampField())

    # Foreign key relationship
    campaign = relationship('CampaignModel', foreign_keys=[campaign_id])
    user = relationship('DriverUserModel', foreign_keys=[user_id])
