from sqlalchemy import (Column, Date, Enum, Integer, String)

from app_common.db.base import BaseModel
from app_common.db.common import DriverStatus, JsonField, Tables, TimestampField


class UserBase(object):
    email = Column('email', String(256))
    # Even uuid is deleted from Base model it will still remain in userBase
    # uuid = Column('uuid', String(128), info='Cognito user pool id')


class AdminUserModel(UserBase, BaseModel):
    __tablename__ = Tables.ADMINS.value


class DriverUserModel(UserBase, BaseModel):
    __tablename__ = Tables.DRIVERS.value

    # user_id will saved in uuid column of parent
    first_name = Column('first_name', String(256))
    last_name = Column('last_name', String(256))
    identityId = Column('identityId', String(256), info='Cognito identification id')
    # Details fields
    heardAboutMobilads = Column('heardAboutMobilads', String(512))

    score = Column('score', Integer())
    car = Column('car', JsonField())
    car_image = Column('car_image', String(512))
    city = Column('city', String(128))
    city_id = Column('city_id', Integer())
    dob = Column('dob', Date())
    phone = Column('phone', String(20))
    end_point_arn = Column('end_point_arn', String(256))
    payment = Column('payment', JsonField())
    platform = Column('platform', String(50))
    status = Column(
        'status',
        Enum(DriverStatus, values_callable=DriverStatus.values),
        default=DriverStatus.ACTIVE.value
    )
    tos_acceptance_ip = Column('tos_acceptance_ip', String(50))
    tos_acceptance_time = Column('tos_acceptance_time', TimestampField())

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'
