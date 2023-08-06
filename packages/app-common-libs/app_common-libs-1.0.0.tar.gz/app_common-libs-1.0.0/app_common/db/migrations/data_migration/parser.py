import json
from datetime import datetime

from sqlalchemy import func

from app_common.constants import DATE_FORMAT, DATETIME_FORMAT, TIME_FORMAT, UTC_DATETIME_FORMAT
from app_common.db.common import DriverStatus, NotificationSource


def default_none():
    return None


def default_datetime(to_format=DATETIME_FORMAT):
    return datetime.utcnow().strftime(to_format)


def to_json(item=None, current_state=None, keys=None):
    """
    Values required no formatting
    """
    value = get_value(item, keys)
    return value and json.loads(value) or None


def by_pass(default_value=None, override_value=None, item=None, current_state=None,
            keys=None):
    """
    Values required no formatting
    """
    value = get_value(item, keys)
    if override_value:
        return override_value
    return value or default_value


def string_max_length(
    default_value=None, override_value=None, item=None, current_state=None, keys=None,
    max_length=None
):
    """
    Values required no formatting
    """
    value = get_value(item, keys)
    if override_value:
        return override_value
    value = value or default_value
    if max_length:
        return str(value)[:max_length]
    else:
        return value


def by_pass_bool(override_value=None, item=None, current_state=None, keys=None):
    """
    Values required no formatting
    """
    value = get_value(item, keys)
    if override_value:
        return override_value
    return value


def parse_float(default_value=0, item=None, current_state=None, keys=None):
    """
    Parse value into float
    """
    value = get_value(item, keys)
    try:
        return float(value)
    except Exception as ex:
        print(ex)
        return default_value


def parse_int(default_value=0, item=None, current_state=None, keys=None):
    """
    Parse value into float
    """
    value = get_value(item, keys)
    try:
        return int(value)
    except Exception as ex:
        print(ex)
        return default_value


def driver_status_parsed(item=None, current_state=None, keys=None):
    """
    Values required no formatting
    """
    value = get_value(item, keys)
    if value == 0:
        return DriverStatus.ACTIVE
    return DriverStatus.IN_ACTIVE


def parse_to_date(default_value_fn=None, from_date_format=UTC_DATETIME_FORMAT, item=None,
                  current_state=None, keys=None):
    """
    Convert UTC date string to epoch timestamp value if value is available else
    default_value_fn will called to get default value
    """
    value = get_value(item, keys)
    try:
        return datetime.strptime(value, from_date_format).strftime(DATE_FORMAT)
    except:
        try:
            return datetime.strptime(value[:10], DATE_FORMAT).strftime(DATE_FORMAT)
        except:
            if default_value_fn:
                return default_value_fn()


def parse_to_time(default_value_fn=default_none, item=None, current_state=None, keys=None):
    """
    Convert UTC time string to datetime.time value if value is available else
    default_value_fn will called to get default value
    """
    value = get_value(item, keys)
    try:
        return datetime.strptime(value, TIME_FORMAT).strftime(TIME_FORMAT)
    except:
        try:
            return datetime.strptime(value[:10], TIME_FORMAT).strftime(TIME_FORMAT)
        except:
            if default_value_fn:
                return default_value_fn()


def parse_to_datetime(default_value_fn=None, from_date_format=UTC_DATETIME_FORMAT,
                      to_format=DATETIME_FORMAT, item=None, current_state=None, keys=None):
    """
    Convert UTC date string to epoch timestamp value if value is available else
    default_value_fn will called to get default value
    """
    value = get_value(item, keys)
    try:
        return str(datetime.strptime(value, from_date_format).strftime(to_format))
    except:
        if default_value_fn:
            return default_value_fn(to_format)


def foreign_key_map(model, cache_dict, item=None, current_state=None, keys=None):
    """
    return mapped value in foreign key
    """
    value = get_value(item, keys)
    if not cache_dict and isinstance(cache_dict, dict):
        cache_dict.update(**model.unique_uuid_dict())
    return cache_dict.get(value, None)


def foreign_key_from_queryset(queryset, cache_dict, item=None, current_state=None, keys=None):
    """
    return mapped value in foreign key
    """
    key = get_value(current_state, keys)
    if not cache_dict and isinstance(cache_dict, dict):
        cache_dict.update(queryset())
    return cache_dict.get(key, None)


def driver_campaign_map():
    from app_common.db.models import CampaignDriverModel
    return {
        item.cu_id: item[0].id for item in CampaignDriverModel.query(
            func.concat(
                CampaignDriverModel.campaign_id, '_', CampaignDriverModel.user_id).label('cu_id')
        ).all()
    }


def get_value(value_map, key):
    if isinstance(key, list):
        return '_'.join([str(value_map.get(key)) for key in key])
    else:
        return value_map.get(key)


def notification_source(item=None, current_state=None, keys=None):
    value = get_value(item, keys)
    return value == 'admin' and NotificationSource.ADMIN or NotificationSource.SELF
