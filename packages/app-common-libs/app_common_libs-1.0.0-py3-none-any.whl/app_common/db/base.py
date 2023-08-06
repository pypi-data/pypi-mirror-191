import enum
import json
import logging
import os
import sys
import time

from sqlalchemy import (Column, Integer, String)
from sqlalchemy.ext.declarative import declarative_base

from app_common.db.common import TimestampField
from app_common.db.manager import create_session

# Sqlalchemy session
SESSION = create_session()
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))  # noqa

logging.basicConfig(level=logging.INFO)
logging.getLogger("aurora_data_api").setLevel(logging.DEBUG)
logging.getLogger("urllib3.connectionpool").setLevel(logging.INFO)
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

Base = declarative_base()


class BaseModel(Base):
    __tablename__ = 'abstract'
    __abstract__ = True
    __table_args__ = {'extend_existing': True}
    """
    Base class of all model which keep re
    """
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    updated_at = Column('updated_at', TimestampField(), nullable=False)
    created_at = Column('created_at', TimestampField(), nullable=False)
    deleted = Column('deleted', TimestampField(), nullable=True, default=None)

    # As we are migrating from DynamoDb the unique identifier is used as this uuid need to remove
    # once all linking and dependency is removed
    uuid = Column('uuid', String(128))

    class Meta:
        HISTORY_FIELDS = []

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return other.id == self.id

    def pre_create(self):
        """
        If instance is created then this function will be created before before saving it
        """
        self.created_at = int(time.time())

    def post_create(self):
        """
        If instance is created then this function will be created before after it
        """
        pass

    def save(self):
        """
        If id is already available it means object is required to update else create an new entry
        :return:
        """
        self.updated_at = int(time.time())
        new_instance = not self.id
        if new_instance:
            # Before creation of instance call pre create function
            self.pre_create()
            self.created_at = int(time.time())
            self.session().add(self)

        self.session().flush()

        self.session().refresh(self)

        # On successful creation of instance call post create function
        if new_instance:
            self.post_create()
        return self

    def update(self):
        self.updated_at = int(time.time())
        self.session().flush()
        return self

    def update_values(self, **kwargs):
        from app_common.db.models import HistoryLogModel
        history = []
        for field, value in kwargs.items():
            if field in self.Meta.HISTORY_FIELDS and getattr(self, field) != value:
                history.append(dict(
                    ref_id=self.id,
                    ref_table=self.__tablename__,
                    field=field,
                    old_value=str(getattr(self, field)),
                    new_value=str(value),
                    created_at=int(time.time()),
                    updated_at=int(time.time()),
                ))
            if hasattr(self, field):
                setattr(self, field, value)
        # Update the table and receive updated fields
        instance = self.update()
        # Save entry in history table for each changed value
        if history:
            HistoryLogModel.bulk_insert_dict(history)
        return instance

    def as_dict(self):
        table_columns = self.__table__.columns.keys()
        data_dict = {}
        for field in table_columns:
            value = getattr(self, field)
            if isinstance(value, enum.Enum):
                value = value.value
            elif isinstance(value, BaseModel):
                value = value.as_dict()
            elif isinstance(value, dict):
                value = json.dumps(value)
            data_dict[field] = value
        return data_dict

    @staticmethod
    def session():
        return SESSION

    @classmethod
    def projection(cls, *projection):
        return cls.session().query(*projection)

    @classmethod
    def query(cls, *criterion):
        return cls.session().query(cls, *criterion)

    @classmethod
    def get(cls, pk):
        try:
            return cls.query().get({'id': pk})
        except Exception as ex:
            print(ex)
            raise Exception(f'No reference found in {cls} with the primary key {pk}')

    @classmethod
    def get_filter(cls, *criterion):
        return cls.query().filter(*criterion).first()

    @classmethod
    def filter(cls, *criterion):
        return cls.query().filter(*criterion)

    @classmethod
    def delete(cls, *criterion):
        return cls.query().filter(*criterion).delete(synchronize_session='evaluate')

    @classmethod
    def exists(cls, *criterion, raise_on_exists=False, message='Object is already exists'):
        exists = bool(cls.query().filter(*criterion).first())
        if exists and raise_on_exists:
            raise Exception(message)
        return exists

    @classmethod
    def bulk_insert_dict(cls, objects):
        # print(f'Bulk insertion in {cls} with payload {objects}')
        if isinstance(objects, list):
            mapped_objects = [cls.instance(**kwargs) for kwargs in objects]
            cls.session().bulk_save_objects(mapped_objects, return_defaults=True)
            return mapped_objects
        raise Exception('Data dict should be type of list of dictionary')

    @classmethod
    def instance(cls, **kwargs):
        table_columns = cls.__table__.columns.keys()
        kwargs = {field: kwargs.get(field, None) for field in table_columns}
        kwargs['updated_at'] = int(time.time())
        kwargs['created_at'] = int(time.time())
        # print(f'Parsed kwargs for {cls} {kwargs}')
        return cls(**kwargs)

    @classmethod
    def update_with_filters(cls, *filters, **fields):
        fields['updated_at'] = int(time.time())
        return cls.filter(*filters).update(fields, synchronize_session='evaluate')

    @classmethod
    def query_and_update_with_filters(cls, *filters, **fields):
        fields['updated_at'] = int(time.time())
        query = cls.filter(*filters)
        query.update(fields, synchronize_session='evaluate')
        return query

    @classmethod
    def unique_uuid_dict(cls):
        return {r.uuid: r.id for r in cls.query().with_entities(cls.id, cls.uuid)}

    @classmethod
    def query_dict(cls, query):
        query_dict = []
        for ref in query:
            if isinstance(ref, cls):
                query_dict.append(ref.as_dict())
            else:
                raise Exception('Not a BaseModel inherited class')
        return query_dict

    def __repr__(self):
        return f'<{self.__class__} model {self.id}>'
