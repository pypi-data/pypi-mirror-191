from functools import partial

from app_common.db.common import (
    CampaignStatus, CampaignTransitionStatus, PaymentStatus,
    UTC_DATETIME_FORMAT
)
from app_common.db.migrations.data_migration.parser import (
    by_pass, by_pass_bool, default_datetime, default_none, driver_campaign_map,
    driver_status_parsed, foreign_key_from_queryset, foreign_key_map,
    notification_source, parse_float,
    parse_int, parse_to_date, parse_to_datetime, parse_to_time, string_max_length, to_json
)
from app_common.db.models import (
    BrandModel, CampaignModel, CampaignWrapLocationsModel, DriverPaymentsModel, DriverUserModel
)

# This dict will be used in cache api request for dumping data from dynamo db to mysql
BRAND_UUID_MAP = {}
CAMPAIGN_UUID_MAP = {}
DRIVER_UUID_MAP = {}
DRIVER_PAYMENTS_MAP = {}
CAMPAIGN_WRAP_LOCATION_UUID_MAP = {}
CAMPAIGN_DRIVERS_APPOINTMENT_MAP = {}

# DynamoDB table to sql key and parser mappers
BASE_KEYS_MAPPING = {
    'created_at': (
        'created_at', partial(parse_to_datetime, default_value_fn=default_datetime)
    ),
    'updated_at': (
        'updated_at', partial(parse_to_datetime, default_value_fn=default_datetime)
    ),
}
ADMIN_PARSER_MAP = {
    **BASE_KEYS_MAPPING,
    'uuid': ('admin_id', by_pass),
    'email': ('email', by_pass),
}
DRIVER_PARSER_MAP = {
    **BASE_KEYS_MAPPING,
    'uuid': ('user_id', by_pass),
    'email': ('email', by_pass),
    'first_name': ('first_name', by_pass),
    'last_name': ('last_name', by_pass),
    'identityId': ('identityId', by_pass),
    'heardAboutMobilads': ('heardAboutMobilads', by_pass),
    'score': ('score', by_pass),
    'car': ('car', to_json),
    'car_image': ('car_image', by_pass),
    'city': ('city', by_pass),
    'city_id': ('city_id', by_pass),
    'dob': ('dob', partial(parse_to_date, default_value_fn=default_none)),
    'phone': ('phone', by_pass),
    'end_point_arn': ('end_point_arn', by_pass),
    'payment': ('payment', by_pass),
    'platform': ('platform', by_pass),
    'status': ('status', driver_status_parsed),
    'tos_acceptance_ip': ('tos_acceptance_ip', partial(string_max_length, max_length=50)),
    'tos_acceptance_time': (
        'tos_acceptance_time', partial(parse_to_datetime, default_value_fn=default_datetime)
    ),
}
BRAND_PARSER_MAP = {
    **BASE_KEYS_MAPPING,
    'uuid': ('id', by_pass),
    'name': ('name', by_pass),
    'email': ('email', by_pass),
    'phone': ('phone', by_pass),
    'city': ('city', by_pass),
    'city_id': ('city_id', by_pass),
    'img_url': ('img_url', by_pass),
    'description': ('description', by_pass),
}
DASHBOARD_PARSER_MAP = {
    **BASE_KEYS_MAPPING,
    'uuid': ('id', by_pass),
    'updated_at': (
        'last_updated_at', partial(parse_to_datetime, default_value_fn=default_datetime)
    ),
    'active_campaign_count': ('active_campaign_count', partial(by_pass, default_value=0)),
    'active_driver_count': ('active_driver_count', partial(by_pass, default_value=0)),
    'campaigns_in_last_week': ('campaigns_in_last_week', partial(by_pass, default_value=0)),
    'drivers_in_last_week': ('drivers_in_last_week', partial(by_pass, default_value=0)),
    'hours_driven_last_week': ('hours_driven_last_week', partial(by_pass, default_value=0)),
    'hours_driven_this_week': ('hours_driven_this_week', partial(by_pass, default_value=0)),
    'total_campaign_count': ('total_campaign_count', partial(by_pass, default_value=0)),
    'total_driver_count': ('total_driver_count', partial(by_pass, default_value=0)),
    'total_hours_driven': ('total_hours_driven', partial(by_pass, default_value=0)),
    'total_payment_to_driver': ('total_payment_to_driver', partial(by_pass, default_value=0)),
}
GLOBAL_CONFIG_PARSER_MAP = {
    **BASE_KEYS_MAPPING,
    'uuid': ('id', by_pass),
    'insufficient_balance_event_triggered': ('insufficient_balance_event_triggered', by_pass),
}
CAMPAIGN_PARSER_MAP = {
    **BASE_KEYS_MAPPING,
    'uuid': ('id', by_pass),
    'status': ('status', partial(by_pass, override_value=CampaignStatus.COMPLETED)),
    'name': ('name', partial(by_pass, default_value='')),
    'brand_id': ('brand_id', partial(
        foreign_key_map,
        model=BrandModel,
        cache_dict=BRAND_UUID_MAP
    )),
    'campaign_type': ('campaign_type', partial(by_pass, default_value='')),
    'city_id': ('city_id', partial(by_pass, default_value=0)),
    'city': ('city', partial(by_pass, default_value='')),
    'amount_per_car': ('amount_per_car', partial(by_pass, default_value=1)),
    'number_of_drivers': ('number_of_drivers', partial(by_pass, default_value=1)),
    'client_price': ('client_price', partial(by_pass, default_value=1)),
    'total_estimated': ('total_estimated', partial(by_pass, default_value=0)),
    'upfront_payment': ('upfront_payment', partial(by_pass, default_value=5)),
    'description': ('description', partial(by_pass, default_value='')),
    'published_at': (
        'published_at', partial(parse_to_datetime, default_value_fn=default_datetime)
    ),
    'end_date': ('end_date', parse_to_date),
    'start_date': ('start_date', parse_to_date),
    'wrap_end_date': ('wrap_end_date', parse_to_date),
    'wrap_start_date': ('wrap_start_date', parse_to_date),

}
CAMPAIGN_DRIVERS_PARSER_MAP = {
    **BASE_KEYS_MAPPING,
    'uuid': ('id', by_pass),
    'campaign_id': ('campaign_id', partial(
        foreign_key_map,
        model=CampaignModel,
        cache_dict=CAMPAIGN_UUID_MAP
    )),
    'user_id': ('user_id', partial(
        foreign_key_map,
        model=DriverUserModel,
        cache_dict=DRIVER_UUID_MAP
    )),
    'active_status': (
        'active_status', driver_status_parsed
    ),
    'status': ('status', partial(by_pass, default_value=CampaignTransitionStatus.NONE)),
    'start_association_time': ('start_association_time', partial(
        parse_to_datetime, default_value_fn=default_datetime, to_format=UTC_DATETIME_FORMAT
    )),
    'end_association_time': ('end_association_time', partial(
        parse_to_datetime, default_value_fn=default_datetime, to_format=UTC_DATETIME_FORMAT
    )),
    'total_payment_done': ('total_payment_done', partial(by_pass, default_value=0)),
    'is_self_unwrap': ('isSelfUnwrap', by_pass_bool),
    'total_time_driven': ('total_time_driven', partial(by_pass, default_value=0)),
}
CAMPAIGN_ACTIVITY_PARSER_MAP = {
    **BASE_KEYS_MAPPING,
    'uuid': ('id', by_pass),
    'campaign_id': ('campaign_id', partial(
        foreign_key_map,
        model=CampaignModel,
        cache_dict=CAMPAIGN_UUID_MAP
    )),
    'user_id': ('user_id', partial(
        foreign_key_map,
        model=DriverUserModel,
        cache_dict=DRIVER_UUID_MAP
    )),
    'meta_data': ('meta_data', partial(by_pass, default_value={})),
    'status': ('status', partial(by_pass, default_value=CampaignTransitionStatus.NONE)),
}
CAMPAIGN_WRAP_LOCATIONS_PARSER_MAP = {
    **BASE_KEYS_MAPPING,
    'uuid': ('id', by_pass),
    'name': ('name', partial(by_pass, default_value='')),
    'campaign_id': ('campaign_id', partial(
        foreign_key_map,
        model=CampaignModel,
        cache_dict=CAMPAIGN_UUID_MAP
    )),
    'is_wrap_location': ('is_wrap_location', by_pass_bool),
    'locationName': ('locationName', partial(by_pass, default_value='')),
    'locationNotes': ('locationNotes', partial(by_pass, default_value='')),
    'lat': ('lat', partial(parse_float, default_value=0)),
    'long': ('long', partial(parse_float, default_value=0)),
    'multiplicity': ('multiplicity', parse_int),
    'availableHours': ('availableHours', partial(by_pass, default_value={})),
    'slots': ('slots', partial(by_pass, default_value={})),
    'startDate': ('startTime', parse_to_date),
    'endDate': ('endTime', parse_to_date),
    'timezone_id': ('timezone_id', partial(by_pass, default_value='utc')),
}
CAMPAIGN_WRAP_APPOINTMENT_PARSER_MAP = {
    **BASE_KEYS_MAPPING,
    'uuid': ('id', by_pass),
    'user_id': ('user_id', partial(
        foreign_key_map,
        model=DriverUserModel,
        cache_dict=DRIVER_UUID_MAP
    )),
    'campaign_id': ('campaign_id', partial(
        foreign_key_map,
        model=CampaignModel,
        cache_dict=CAMPAIGN_UUID_MAP
    )),
    'campaign_driver_id': (['campaign_id', 'user_id'], partial(
        foreign_key_from_queryset,
        queryset=driver_campaign_map,
        cache_dict=CAMPAIGN_DRIVERS_APPOINTMENT_MAP
    )),
    'wrap_location_id': ('wrap_location_id', partial(
        foreign_key_map,
        model=CampaignWrapLocationsModel,
        cache_dict=CAMPAIGN_WRAP_LOCATION_UUID_MAP
    )),
    'is_wrap_appointment': ('is_wrap_appointment', by_pass_bool),
    'slot_timing': ('slot_timimg', parse_to_time),
    'wrap_date': ('wrap_date', parse_to_date),
}
CAMPAIGN_SHIFT_RECORD_PARSER_MAP = {
    **BASE_KEYS_MAPPING,
    'uuid': ('shift_id', by_pass),
    'user_id': ('user_id', partial(
        foreign_key_map,
        model=DriverUserModel,
        cache_dict=DRIVER_UUID_MAP
    )),
    'campaign_id': ('campaign_id', partial(
        foreign_key_map,
        model=CampaignModel,
        cache_dict=CAMPAIGN_UUID_MAP
    )),
    'start_time': ('start_time', parse_to_datetime),
    'end_time': ('end_time', parse_to_datetime),
}

CAMPAIGN_NOTIFICATION_PARSER_MAP = {
    **BASE_KEYS_MAPPING,
    'uuid': ('id', by_pass),
    'campaign_id': ('campaign_id', partial(
        foreign_key_map,
        model=CampaignModel,
        cache_dict=CAMPAIGN_UUID_MAP
    )),
    'user_id': ('driver_id', partial(
        foreign_key_map,
        model=DriverUserModel,
        cache_dict=DRIVER_UUID_MAP
    )),
    'status': ('status', partial(by_pass, default_value=CampaignTransitionStatus.NONE)),
    'source_type': ('user_id', notification_source),
    'seen_at': ('seen_at', parse_to_datetime),
    'message': ('message', partial(by_pass, default_value='')),
    'meta_data': ('meta_data', partial(by_pass, default_value={})),
}
DRIVER_PAYMENTS_PARSER_MAP = {
    **BASE_KEYS_MAPPING,
    'uuid': ('id', by_pass),
    'campaign_id': ('campaign_id', partial(
        foreign_key_map,
        model=CampaignModel,
        cache_dict=CAMPAIGN_UUID_MAP
    )),
    'user_id': ('user_id', partial(
        foreign_key_map,
        model=DriverUserModel,
        cache_dict=DRIVER_UUID_MAP
    )),
    'transaction_id': ('transaction_id', by_pass),
    'payment_id': ('payment_id', by_pass),
    'payment_uuid': ('payment_uuid', by_pass),
    'amount': ('amount', partial(by_pass, default_value=0)),
    'payment_type': ('payment_type', by_pass),
    'reason': ('reason', partial(by_pass, default_value='')),
    'response_code': ('response_code', by_pass),
    'status': ('status', partial(by_pass, default_value=PaymentStatus.NONE)),
    'request_payload': ('request_payload', partial(by_pass, default_value={})),
    'pg_response': ('pg_response', partial(by_pass, default_value={})),
}
HISTORY_LOGS_PARSER_MAP = {
    **BASE_KEYS_MAPPING,
    'uuid': ('id', by_pass),
    'ref_table': (
        'ref_table', partial(by_pass, override_value=DriverPaymentsModel.__tablename__, )
    ),
    'ref_id': ('ref_id', partial(
        foreign_key_map,
        model=DriverPaymentsModel,
        cache_dict=DRIVER_PAYMENTS_MAP
    )),
    'field': ('field', by_pass),
    'new_value': ('new_value', by_pass),
    'old_value': ('old_value', by_pass),
}
