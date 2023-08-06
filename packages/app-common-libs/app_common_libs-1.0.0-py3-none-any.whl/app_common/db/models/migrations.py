from sqlalchemy import (Column, Integer, String)

from app_common.db.base import BaseModel
from app_common.db.common import Tables


class Migrations(BaseModel):
    __tablename__ = Tables.MIGRATIONS.value
    # Brand details
    m_index = Column('m_index', Integer(), unique=True)
    m_name = Column('m_name', String(256))
