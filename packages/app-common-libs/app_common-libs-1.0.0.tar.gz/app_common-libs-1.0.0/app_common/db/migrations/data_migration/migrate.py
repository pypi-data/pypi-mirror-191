from app_common.db.migrations.data_migration.mappers import (
    ADMIN_PARSER_MAP, BRAND_PARSER_MAP, CAMPAIGN_ACTIVITY_PARSER_MAP, CAMPAIGN_DRIVERS_PARSER_MAP,
    CAMPAIGN_NOTIFICATION_PARSER_MAP, CAMPAIGN_PARSER_MAP, CAMPAIGN_SHIFT_RECORD_PARSER_MAP,
    CAMPAIGN_WRAP_APPOINTMENT_PARSER_MAP,
    CAMPAIGN_WRAP_LOCATIONS_PARSER_MAP, DASHBOARD_PARSER_MAP,
    DRIVER_PARSER_MAP, DRIVER_PAYMENTS_PARSER_MAP, GLOBAL_CONFIG_PARSER_MAP,
    HISTORY_LOGS_PARSER_MAP
)
from app_common.db.models import (
    AdminUserModel, BrandModel, CampaignActivityModel, CampaignDriverModel, CampaignModel,
    CampaignNotificationsModel, CampaignWrapAppointmentsModel, CampaignWrapLocationsModel,
    DashboardModel,
    DriverPaymentsModel, DriverUserModel,
    GlobalConfigModel, HistoryLogModel, RideShiftRecordsModel
)

# Source Dynamo DB tables
ADMIN_TABLE = 'admins'
DRIVER_TABLE = 'drivers'
BRANDS_TABLE = 'brands'
DASHBOARD_TABLE = 'dashboard_summary'
GLOBAL_TABLE = 'global_config'
CAMPAIGN_TABLE = 'campaigns'
CAMPAIGN_DRIVER_TABLE = 'campaign_driver'
CAMPAIGN_ACTIVITY_TABLE = 'campaign_activity'
CAMPAIGN_NOTIFICATIONS_TABLE = 'notifications'
DRIVER_PAYMENT = 'payment_history'
HISTORY_LOGS = 'history'
CAMPAIGN_WRAP_LOCATION_TABLE = 'wrap_location'
WRAP_APPOINTMENT = 'wrap_appointment'
SHIFT_RIDE = 'shift_records'

# Mapping params for tables
MIGRATION_MAPPINGS = [
    (AdminUserModel, ADMIN_TABLE, ADMIN_PARSER_MAP),
    (DriverUserModel, DRIVER_TABLE, DRIVER_PARSER_MAP),
    (BrandModel, BRANDS_TABLE, BRAND_PARSER_MAP),
    (DashboardModel, DASHBOARD_TABLE, DASHBOARD_PARSER_MAP),
    (GlobalConfigModel, GLOBAL_TABLE, GLOBAL_CONFIG_PARSER_MAP),
    (CampaignModel, CAMPAIGN_TABLE, CAMPAIGN_PARSER_MAP),
    (CampaignDriverModel, CAMPAIGN_DRIVER_TABLE, CAMPAIGN_DRIVERS_PARSER_MAP),
    (CampaignActivityModel, CAMPAIGN_ACTIVITY_TABLE, CAMPAIGN_ACTIVITY_PARSER_MAP),
    (CampaignWrapLocationsModel, CAMPAIGN_WRAP_LOCATION_TABLE, CAMPAIGN_WRAP_LOCATIONS_PARSER_MAP),
    (CampaignWrapAppointmentsModel, WRAP_APPOINTMENT, CAMPAIGN_WRAP_APPOINTMENT_PARSER_MAP),
    (RideShiftRecordsModel, SHIFT_RIDE, CAMPAIGN_SHIFT_RECORD_PARSER_MAP),
    (CampaignNotificationsModel, CAMPAIGN_NOTIFICATIONS_TABLE, CAMPAIGN_NOTIFICATION_PARSER_MAP),
    (DriverPaymentsModel, DRIVER_PAYMENT, DRIVER_PAYMENTS_PARSER_MAP),
    (HistoryLogModel, HISTORY_LOGS, HISTORY_LOGS_PARSER_MAP),
]
