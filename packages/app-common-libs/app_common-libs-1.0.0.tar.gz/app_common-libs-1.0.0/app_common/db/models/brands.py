from sqlalchemy import (Column, ForeignKey, Integer, String, Text)
from sqlalchemy.orm import relationship

from app_common.db.base import BaseModel
from app_common.db.common import Tables


class BrandModel(BaseModel):
    __tablename__ = Tables.BRANDS.value
    # Brand details
    email = Column('email', String(190), unique=True)
    password = Column('password', String(190))
    city = Column('city', String(128))
    city_id = Column('city_id', Integer())
    description = Column('description', Text())
    img_url = Column('img_url', String(190))
    name = Column('name', String(190))
    phone = Column('phone', String(20))
    campaigns = relationship(
        "CampaignModel",
        primaryjoin="CampaignModel.brand_id==BrandModel.id"
    )


class BrandAuthSessions(BaseModel):
    __tablename__ = Tables.BRANDS_SESSIONS.value
    # Brand details
    brand_id = Column('brand_id', ForeignKey(f'{Tables.BRANDS.value}.id', ondelete='CASCADE'))
    username = Column('username', String(190))
    token = Column('token', String(190), unique=True)
    # Foreign key relationship
    brand = relationship('BrandModel', foreign_keys=[brand_id])
