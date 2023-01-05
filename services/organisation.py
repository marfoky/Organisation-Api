import fastapi
from sqlalchemy.orm import Session

from db.models.schemas import OrganisationDto
from db.models.sql_models import *
from repositories import address as address_repository
from repositories import organisation as organisation_repository
from repositories import socials as socials_repository

def fetch_all_organisations(db: Session) -> list[OrganisationDomain]:
    organisation_entities = organisation_repository.fetch_all_organisations(db)
    domains = []
    social_domains = []
    # Convert to domain
    domain = OrganisationDomain()
    address_entity = AddressDomain()
    for entity in organisation_entities:
        domain.id = entity.id
        domain.name = entity.name
        domain.email = entity.email
        domain.about = entity.about
        domain.phone = entity.phone
        domain.profile_link = entity.profile_link
        domains.append(domain)

        address_entities = address_repository.fetch_address_by_id(db, entity.id)
        address_entity.country = address_entities.country
        address_entity.state = address_entities.state
        address_entity.city = address_entities.city
        address_entity.code = address_entities.code
        address_entity.address_line1 = address_entities.address_line1
        address_entity.address_line2 = address_entities.address_line2

    social_entities = socials_repository.fetch_social_by_id(db, domain.id)
    for social_entity in social_entities:
        social_domain = SocialDomain()
        social_domain.social_name = social_entity.social_name
        social_domain.url = social_entity.url
        social_domains.append(social_domain)

    domain.socials = social_domains
    domain.address = address_entity

    return domains


def fetch_organisation_by_id(db: Session, organisation_id: int) -> OrganisationDomain:
    organisation = organisation_repository.fetch_organisation_by_id(db, organisation_id)
    if organisation is None:
        raise fastapi.HTTPException(status_code=404, detail='Id not valid')
    else:
        domain = OrganisationDomain()
        domain.id = organisation.id
        domain.name = organisation.name
        domain.email = organisation.email
        domain.about = organisation.about
        domain.phone = organisation.phone
        domain.profile_link = organisation.profile_link

        address_entities = address_repository.fetch_address_by_id(db, organisation_id)
        address_entity = AddressEntity()
        address_entity.country = address_entities.country
        address_entity.state = address_entities.state
        address_entity.city = address_entities.city
        address_entity.code = address_entities.code
        address_entity.address_line1 = address_entities.address_line1
        address_entity.address_line2 = address_entities.address_line2

    social_entities = socials_repository.fetch_social_by_id(db, organisation_id)
    social_domains = []
    for social_entity in social_entities:
        social_domain = SocialDomain()
        social_domain.social_name = social_entity.social_name
        social_domain.url = social_entity.url
        social_domains.append(social_domain)

    domain.socials = social_domains
    domain.address = address_entity

    return domain


def create_organisation(dto: OrganisationDto, db: Session):
    organisation_entity = OrganisationEntity()
    organisation_entity.name = dto.name
    organisation_entity.phone = dto.phone
    organisation_entity.about = dto.about
    organisation_entity.email = dto.email
    organisation_entity.profile_link = dto.profile_link
    organisation_entity = organisation_repository.create_entity(organisation_entity, db)

    address_entity = AddressEntity()
    address_entity.organisation_id = organisation_entity.id
    address_entity.country = dto.address.country
    address_entity.state = dto.address.state
    address_entity.city = dto.address.city
    address_entity.code = dto.address.code
    address_entity.address_line1 = dto.address.address_line1
    address_entity.address_line2 = dto.address.address_line2
    address_entity = socials_repository.create_social(address_entity, db)

    social_entities = []
    for social in dto.socials:
        social_entity = SocialEntity()
        social_entity.organisation_id = organisation_entity.id
        social_entity.social_name = social.social_name
        social_entity.url = social.url
        social_entities.append(social_entity)

    social_entities = socials_repository.create_socials(social_entities, db)

    domain = OrganisationDomain()
    domain.name = organisation_entity.name
    domain.id = organisation_entity.id
    domain.email = organisation_entity.email
    domain.about = organisation_entity.about
    domain.phone = organisation_entity.phone
    domain.profile_link = organisation_entity.profile_link

    addDomain = AddressDomain()
    addDomain.country = address_entity.country
    addDomain.state = address_entity.state
    addDomain.city = address_entity.city
    addDomain.code = address_entity.code
    addDomain.address_line1 = address_entity.address_line1
    addDomain.address_line2 = address_entity.address_line2
    social_domains = []
    for social_entity in social_entities:
        social_domain = SocialDomain()
        social_domain.social_name = social_entity.social_name
        social_domain.url = social_entity.url
        social_domains.append(social_domain)

    domain.address = addDomain
    domain.socials = social_domains

    return domain


def delete_organisation(db: Session, organisation_id: int):
    domain = fetch_organisation_by_id(db, organisation_id)
    organisation_repository.delete_organisation(db, domain.id)
    address_repository.delete_address(db, organisation_id)
    socials_repository.delete_socials(db, organisation_id)


def update_organisation(organisation_id: int, dto: OrganisationDto, db: Session):
    # Fetch organisation
    entity = fetch_organisation_by_id(db, organisation_id)
    # if not found, return error
    if entity is None:
        raise fastapi.HTTPException(status_code=404, detail='Id not valid')
    else:
        # if not found, return error
        entity.name = dto.name
        entity.email = dto.email
        entity.phone = dto.phone
        entity.profile_link = dto.profile_link
        entity.about = dto.about

        # use the address repo to fetch the address by organisation id
        address_entity = address_repository.update_address(db, organisation_id)
        if address_entity is not None:
            address_entity.country = dto.address.country
            address_entity.state = dto.address.state
            address_entity.city = dto.address.city
            address_entity.code = dto.address.code
            address_entity.address_line1 = dto.address.address_line1
            address_entity.address_line2 = dto.address.address_line2
        else:
            raise fastapi.HTTPException(status_code=404, detail='Address not valid')

        # use the social repo to fetch the socials by organisation id
        social_array = []
        social_entity = socials_repository.update_socials(db, organisation_id)
        for social_entities in social_entity:
            social_entity.social_name = social_entities.social_name
            social_entity.url = social_entities.url
            social_array.append(social_array)
        db.commit()

    domain = to_domain(entity, address_entity, social_array)
    return domain
