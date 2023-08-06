def add_unique_constraints():
    from app_common.db.models import BaseModel
    session = BaseModel.session()
    try:
        session.execute(
            'ALTER TABLE campaign_drivers ADD CONSTRAINT constraint_name UNIQUE KEY(campaign_id,'
            'user_id)'
        )
    except Exception as ex:
        session.rollback()
        raise ex


def dump_data():
    from app_common.db.migrations.data_migration.source import dump_dynamo_data
    from app_common.db.migrations.data_migration.migrate import MIGRATION_MAPPINGS
    for mapping in MIGRATION_MAPPINGS:
        dump_dynamo_data(*mapping)


def migrate():
    add_unique_constraints()
    dump_data()
