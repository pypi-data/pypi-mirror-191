"""
sqlalchemy-aurora-data-api
"""

import aurora_data_api
import sqlalchemy.dialects as dls
from sqlalchemy.dialects.mysql.base import MySQLDialect

DRIVER_TYPE = 'aurora_data_api'


class AuroraServerlessMySQLDataAPIDialect(MySQLDialect):
    driver = DRIVER_TYPE
    default_schema_name = None

    @classmethod
    def dbapi(cls):
        return aurora_data_api

    def _detect_charset(self, connection):
        return connection.execute('SHOW VARIABLES LIKE "character_set_client"').fetchone()[1]

    def _extract_error_code(self, exception):
        return exception.args[0].value


dls.registry.register(
    f'mysql.{DRIVER_TYPE}', __name__, AuroraServerlessMySQLDataAPIDialect.__name__
)
