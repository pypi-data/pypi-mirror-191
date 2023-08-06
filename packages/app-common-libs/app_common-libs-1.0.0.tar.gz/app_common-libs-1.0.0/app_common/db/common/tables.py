import enum


class Tables(enum.Enum):
    MIGRATIONS = 'migrations'
    ADMINS = 'admins'
    BRANDS = 'brands'
    BRANDS_SESSIONS = 'brands_sessions'
    CAMPAIGNS = 'campaigns'
    CAMPAIGN_ACTIVITY = 'campaign_activity'
    CAMPAIGN_DRIVER = 'campaign_drivers'
    CAMPAIGN_DRIVER_LOCATIONS_PERMISSION = 'campaign_driver_locations_permission'
    CAMPAIGN_WRAP_LOCATIONS = 'campaign_wrap_locations'
    CAMPAIGN_WRAP_APPOINTMENT = 'campaign_wrap_appointment'
    DASHBOARD = 'dashboard'
    DRIVER_PAYMENTS = 'driver_payments'
    DRIVERS = 'drivers'
    GLOBAL_CONFIG = 'global_config'
    HISTORY_LOG = 'history_log'
    CAMPAIGN_NOTIFICATIONS = 'campaign_notifications'
    RIDE_SHIFT_RECORDS = 'ride_shift_records'


