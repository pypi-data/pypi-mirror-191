import os

from dynamorm import DynaModel
from marshmallow import fields

from app_common.constants import ApiErrorCode

API_NAME = os.environ.get('api_name')


class BaseModel:
    class Table:
        name = f'{API_NAME}-'
        hash_key = 'id'
        read = 25
        write = 5

    class Schema:
        id = fields.String()
        created_at = fields.String()

    @classmethod
    def list(cls, **kwargs):
        if issubclass(cls, DynaModel):
            return list(cls.scan(**kwargs))
        return []

    @classmethod
    def get(cls, **kwargs):
        items = cls.list(**kwargs)
        if len(items) > 0:
            return items[0]
        return None

    @classmethod
    def instance(cls, ref_id):
        if issubclass(cls, DynaModel):
            return cls.get(id=ref_id)
        return None

    def update_values(self, **kwargs):
        if not isinstance(self, DynaModel):
            return {
                'code': ApiErrorCode.FAILURE,
                'data': kwargs
            }
        # Update the table and receive updated fields
        instance = self.update(**kwargs)
        # Return success response
        return {
            'code': ApiErrorCode.OK,
            'data': instance
        }
