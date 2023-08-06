from dynamorm import DynaModel
from marshmallow import fields
from app_common.database_models import BaseModel

from app_common.logger import Logger

logger = Logger.create_logger(__name__)


class FAQSupport(BaseModel, DynaModel):
    # Define our DynamoDB properties
    class Table(BaseModel.Table):
        name = f'{BaseModel.Table.name}faq-support'
        hash_key = 'id'
        read = 25
        write = 5

    # Define our data schema, each property here will become a property on instances of the Book
    # class
    class Schema(BaseModel.Schema):
        subject = fields.String()
        campaign_id = fields.String()
        campaign_name = fields.String()
        user_id = fields.String()
        user_email = fields.String()
        message = fields.String()

    @staticmethod
    def on_update(ref_id, **kwargs):
        instance = FAQSupport.instance(ref_id=ref_id)
        return instance and instance.update_values(**kwargs)
