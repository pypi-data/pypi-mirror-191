import datetime

from sqlalchemy import (Column, Date, Float, Integer)

from app_common.db.base import BaseModel
from app_common.db.common import Tables

DEFAULT_DATE = '1970-01-01'


class SingleRowMixin:
    @classmethod
    def latest(cls):
        if issubclass(cls, BaseModel):
            references = cls.query().first()
            if not references:
                references = cls().save()
            return references
        return None


class DashboardModel(BaseModel, SingleRowMixin):
    __tablename__ = Tables.DASHBOARD.value
    # Dashboard details
    active_campaign_count = Column('active_campaign_count', Integer(), default=0)
    active_driver_count = Column('active_driver_count', Integer(), default=0)
    campaigns_in_last_week = Column('campaigns_in_last_week', Integer(), default=0)
    drivers_in_last_week = Column('drivers_in_last_week', Integer(), default=0)
    total_campaign_count = Column('total_campaign_count', Integer(), default=0)
    total_driver_count = Column('total_driver_count', Integer(), default=0)
    total_payment_to_driver = Column('total_payment_to_driver', Float(), default=0)

    total_hours_driven = Column('total_hours_driven', Float(), default=0)
    hours_driven_this_week = Column('hours_driven_this_week', Integer(), default=0)
    hours_driven_last_week = Column('hours_driven_last_week', Integer(), default=0)


class GlobalConfigModel(BaseModel, SingleRowMixin):
    __tablename__ = Tables.GLOBAL_CONFIG.value
    # Dashboard details
    insufficient_balance_event_triggered = Column('insufficient_balance_event_triggered', Date())

    @classmethod
    def insufficient_balance(cls, is_insufficient=True):
        """
        Toggle DB status for insufficient_balance_event_triggered with today's date on event so we
        can avoid triggering duplicate notification for insufficient fund in same day
        """
        today_date = datetime.date.today().strftime('%Y-%m-%d')
        trigger_time = is_insufficient and today_date or DEFAULT_DATE
        ref = cls.latest()
        ref.insufficient_balance_event_triggered = trigger_time
        ref.update()

    @classmethod
    def is_triggered_insufficient_balance(cls):
        """
        Check whether the notification time is today or not if it is today then return True
        else False will be return so notification can be triggered
        """
        ref = cls.latest()
        trigger_time = ref.insufficient_balance_event_triggered
        return datetime.date.today().strftime('%Y-%m-%d') == trigger_time
