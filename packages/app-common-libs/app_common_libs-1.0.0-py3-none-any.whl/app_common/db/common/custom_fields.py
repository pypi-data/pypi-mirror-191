import datetime
import json
from datetime import date, datetime

import iso8601
from sqlalchemy import (BigInteger, Text, types)
from sqlalchemy.types import TIMESTAMP, TypeDecorator

from app_common.constants import DATETIME_FORMAT, UTC_DATETIME_FORMAT


class TimestampField(types.TypeDecorator):
    impl = BigInteger
    date_format = DATETIME_FORMAT

    def process_bind_param(self, value, dialect):
        from app_common.db.common import epoch_timestamp
        if value is None:
            return None
        elif isinstance(value, int):
            return value
        elif isinstance(value, datetime) or isinstance(value, date):
            return int(value.strftime('%s'))
        else:
            return epoch_timestamp(value, self.date_format)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        else:
            return datetime.utcfromtimestamp(value).strftime(self.date_format)


class JsonField(types.TypeDecorator):
    """Enables JSON storage by encoding and decoding on the fly."""
    impl = Text

    def process_bind_param(self, value, dialect):
        from app_common.db.common import DecimalEncoder
        if value is None:
            return '{}'
        else:
            return json.dumps(value, cls=DecimalEncoder)

    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)


class ISO8601DateTime(TypeDecorator):
    impl = TIMESTAMP

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, datetime.datetime):
            return value.strftime(UTC_DATETIME_FORMAT)
        return value

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return iso8601.parse_date(value)
