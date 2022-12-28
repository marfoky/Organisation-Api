from pydantic import BaseModel

from db.models.sql_models import OrganisationEntity


class SocialDomain(BaseModel):
    social_name: str | None = None
    url: str | None = None


class AddressDomain(BaseModel):
    country: str | None = None
    state: str | None = None
    city: str | None = None
    code: str | None = None
    address_line1: str | None = None
    address_line2: str | None = None


class OrganisationDomain(BaseModel):
    id: int | None = None
    name: str | None = None
    email: str | None = None
    about: str | None = None
    phone: str | None = None
    profile_link: str | None = None
    address: AddressDomain | None = None
    socials: list[SocialDomain] | None = None

