import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

MYSQL_AURORA_DATA_API = 'mysql+aurora_data_api'
DATABASE_URL_SCHEME = '%s://:@/{database_name}' % MYSQL_AURORA_DATA_API


def create_session():
    region = os.environ.get('region')
    aurora_cluster_ref = os.environ.get('auroraClusterRef')
    cluster_arn = f'arn:aws:rds:{region}:289895589654:cluster:{aurora_cluster_ref}'
    secret_arn = os.environ.get('auroraSecretRef')
    database_name = os.environ.get('auroraDBName')
    engine = create_engine(
        DATABASE_URL_SCHEME.format(database_name=database_name),
        connect_args=dict(aurora_cluster_arn=cluster_arn, secret_arn=secret_arn),
        echo=True, echo_pool=True,
        pool_size=1,
        pool_timeout=60,
        encoding='UTF-8',
        convert_unicode=True,
    )
    return sessionmaker(bind=engine, autocommit=True, )()
