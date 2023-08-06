def migrate():
    from app_common.db.models import BaseModel, CampaignModel
    session = BaseModel.session()
    try:
        session.execute(
            f'ALTER TABLE {CampaignModel.__tablename__} ADD COLUMN audience TEXT NULL;'
        )
    except Exception as ex:
        session.rollback()
        raise ex
