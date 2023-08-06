from datetime import datetime

import pytz

from app_common.constants import DATETIME_FORMAT


def epoch_timestamp(date_string, date_format=DATETIME_FORMAT):
    return int(
        datetime.strptime(date_string, date_format).replace(tzinfo=pytz.utc).timestamp()
    )
