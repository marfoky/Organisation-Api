from pydantic import BaseModel


class SocialDto(BaseModel):
    social_name: str
    url: str


class AddressDto(BaseModel):
    address_line1: str
    address_line2: str
    country: str
    state: str
    city: str
    code: str


class OrganisationDto(BaseModel):
    name: str
    email: str
    phone: str
    profile_link: str
    about: str | None = None
    address: AddressDto
    socials: list[SocialDto]
