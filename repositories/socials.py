from sqlalchemy.orm import Session

from db.models import sql_models
from db.models.sql_models import SocialEntity


def fetch_social_by_id(db: Session, organisation_id: int) -> list[SocialEntity]:
    return db.query(sql_models.SocialEntity).filter(sql_models.SocialEntity.organisation_id == organisation_id)


def fetch_all_socials(db: Session) -> list[SocialEntity]:
    return db.query(SocialEntity).all()


def create_social(soentity: SocialEntity, db: Session) -> SocialEntity:
    db.add(soentity)
    db.commit()
    db.refresh(soentity)
    return soentity


def update_socials(db: Session, organisation_id: int) -> list[SocialEntity]:
    entity = fetch_social_by_id(db, organisation_id)
    return entity


def create_socials(social_entities: list[SocialEntity], db: Session):
    db.add_all(social_entities)
    db.commit()
    return social_entities


def delete_socials(db: Session, organisation_id: int):
    db.query(sql_models.SocialEntity).filter(sql_models.SocialEntity.organisation_id == organisation_id).delete()
    db.commit()
