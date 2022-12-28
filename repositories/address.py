from sqlalchemy.orm import Session

from db.models import sql_models
from db.models.sql_models import AddressEntity


def fetch_all_addresses(db: Session) -> list[AddressEntity]:
    return db.query(AddressEntity).all()


def create_address(adentity: AddressEntity, db: Session) -> AddressEntity:
    db.add(adentity)
    db.commit()
    db.refresh(adentity)
    return adentity


def fetch_address_by_id(db: Session, organisation_id: int) -> AddressEntity:
    return db.query(sql_models.AddressEntity).filter(
        sql_models.AddressEntity.organisation_id == organisation_id).first()


def delete_address(db: Session, organisation_id: int):
    db.query(sql_models.AddressEntity).filter(sql_models.AddressEntity.organisation_id == organisation_id).delete()
    db.commit()


def update_address(db: Session, organisation_id: int):
    entity = fetch_address_by_id(db, organisation_id)
    return entity
