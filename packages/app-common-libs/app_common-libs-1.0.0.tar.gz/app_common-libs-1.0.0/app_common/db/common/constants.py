import enum


# noinspection PyTypeChecker
class BaseChoices(enum.Enum):
    @staticmethod
    def values(elements):
        return [e.value for e in elements]

    def __str__(self):
        return self.value

    @classmethod
    def values_list(cls):
        return cls.values(list(cls))

    @classmethod
    def name_list(cls):
        return [e.name for e in list(cls)]

    @classmethod
    def item_dict(cls):
        return {e.name: e.value for e in list(cls)}


class DriverStatus(BaseChoices):
    NONE = 'NONE'
    IN_ACTIVE = 'IN_ACT'
    ACTIVE = 'ACT'


class LocationPermissionStatus(BaseChoices):
    DENY = 'DENY'
    IN_USE = 'IN_USE'
    FULL = 'FULL'


class CampaignTransitionStatus(BaseChoices):
    NONE = 'NONE'
    AD_HOC_PAYMENT_INITIATED = 'ADHOCI'
    AD_HOC_PAYMENT_DONE = 'ADHOCD'
    AD_HOC_PAYMENT_FAILED = 'ADHOCF'
    NEW_CAMPAIGN = 'NEWCAMP'
    CAMPAIGN_ENDED = 'CAMPEND'
    APPLIED = 'APLD'
    APPROVED = 'APRD'
    REJECTED = 'REJ'
    WRAP_SCHEDULED = 'WSCH'
    PENDING_WRAP_APPROVAL = 'PWAPR'
    WRAP_APPROVED = 'WAPRD'
    WRAP_REJECTED = 'WREJ'
    ADVANCE_PAYMENT_INITIATED = 'APAYI'
    ADVANCE_PAYMENT_DONE = 'APAYD'
    ADVANCE_PAYMENT_FAILED = 'APAYF'
    CAMPAIGN_IN_PROGRESS = 'CIP'
    CAMPAIGN_FINISHED = 'CF'
    PENDING_END_WRAP_APPROVAL = 'PEWAPR'
    END_WRAP_APPROVED = 'EWAPRD'
    END_WRAP_REJECTED = 'EWREJ'
    UNWRAP_SCHEDULED = 'UWSCH'
    PENDING_UNWRAP_APPROVAL = 'PUWAPR'
    UNWRAP_APPROVED = 'UWAPRD'
    UNWRAP_REJECTED = 'UWREJ'
    FINAL_PAYMENT_INITIATED = 'FI'
    FINAL_PAYMENT_DONE = 'FD'
    FINAL_PAYMENT_FAILED = 'FF'
    FINAL_UNWRAP_PAYMENT_INITIATED = 'FUWI'
    FINAL_UNWRAP_PAYMENT_DONE = 'FUWD'
    FINAL_UNWRAP_PAYMENT_FAILED = 'FUWF'
    REMOVE = 'REMOVE'
    REMOVED = 'REM'
    UNDO_REMOVED = 'UREM'
    OFFLINE_2_DAYS = 'OFFNOTI'
    REMINDER_2_DAYS = '2DAYS'
    WRAP_APP_REMINDER = 'WRAPAPPT'
    WRAP_LOCATION_UPDATED = 'UPDTWRAPLOC'
    WRAP_SCHEDULES_UPDATED = 'UPDTWRAPSCHED'
    REMINDER_MID_DAYS = 'MID_DAYS'


class CampaignStatus(BaseChoices):
    NONE = 'NONE'
    COMPLETED = 'COM'
    PUBLISH = 'PUB'
    DRAFT = 'DFT'
    ACTIVE = 'ACT'


class PaymentTypes(BaseChoices):
    NONE = 'NONE'
    ADVANCE = 'ADVANCE'
    ADHOC = 'ADHOC'
    FULL = 'FULL'
    UNWRAP = 'UNWRAP'


class NotificationSource(BaseChoices):
    NONE = 'NONE'
    ADMIN = 'ADMIN'
    SELF = 'SELF'


class PaymentStatus(BaseChoices):
    NONE = 'NONE'
    INITIATED = 'INITIATED'
    FAILED = 'FAILED'
    SUCCESS = 'SUCCESS'
    CANCELED = 'CANCELED'
    REVERTED = 'REVERTED'


class ReportStatus(BaseChoices):
    TODO = 'TODO'
    IN_PROGRESS = 'IN_PROGRESS'
    GENERATED = 'GENERATED'
    FAILURE = 'FAILURE'
