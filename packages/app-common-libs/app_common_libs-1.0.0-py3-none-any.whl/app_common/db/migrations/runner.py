import importlib
import os

UTF_MB_UNICODE_CI = 'CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'
database_name = os.environ.get('auroraDBName')


def update_character_set():
    f"""
        ALTER DATABASE {database_name} {UTF_MB_UNICODE_CI};
            For existing table and data in columns
        ALTER TABLE <table_name> CONVERT TO {UTF_MB_UNICODE_CI};
        ALTER TABLE <table_name> CHANGE column_name <column_name> VARCHAR(191) {UTF_MB_UNICODE_CI};
    """
    from app_common.db.models import BaseModel
    session = BaseModel.session()
    try:
        session.execute(f'ALTER DATABASE {database_name} {UTF_MB_UNICODE_CI};')
    except Exception as ex:
        session.rollback()
        raise ex


def refresh_tables():
    # Import all models which need to be migrated
    from app_common.db.models import BaseModel

    engine = BaseModel.session().get_bind()
    BaseModel.metadata.reflect(bind=engine)
    BaseModel.metadata.create_all(engine, checkfirst=True)


def migrate():
    from app_common.db.models import Migrations
    last_migration = Migrations.query().order_by(Migrations.id.desc()).first()
    last_migration_index = last_migration and last_migration.m_index
    migration_index = last_migration_index is not None and (last_migration_index + 1) or 0
    while True:
        try:
            migration_file = f'migration_{migration_index}'
            print(f'Running migration {migration_file}')
            importlib.import_module(migration_file).migrate()
            Migrations(
                m_index=migration_index,
                m_name=migration_file
            ).save()
            migration_index += 1
        except Exception as ex:
            print(ex)
            print('Migration completed')
            break


if __name__ == '__main__':
    update_character_set()
    refresh_tables()
    # Run missing migrations
    migrate()
