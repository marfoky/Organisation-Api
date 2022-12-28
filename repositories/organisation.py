from sqlalchemy.orm import Session

from db.models import sql_models
from db.models.sql_models import OrganisationEntity


def fetch_all_organisations(db: Session) -> list[OrganisationEntity]:
    return db.query(OrganisationEntity).all()


def create_entity(entity: OrganisationEntity, db: Session) -> OrganisationEntity:
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity


def fetch_organisation_by_id(db: Session, organisation_id: int):
    return db.query(sql_models.OrganisationEntity).filter(sql_models.OrganisationEntity.id == organisation_id).first()


def delete_organisation(db: Session, organisation_id: int):
    db.query(sql_models.OrganisationEntity).filter(sql_models.OrganisationEntity.id == organisation_id).delete()
    db.commit()


def update_entity(db: Session, organisation_id: int):
    entity = fetch_organisation_by_id(db, organisation_id)
    return entity
