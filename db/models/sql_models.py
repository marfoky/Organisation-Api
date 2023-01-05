# from sqlalchemy import ForeignKey, Integer, String, Text
# from sqlalchemy.orm import relationship
# from sqlalchemy_utils import URLType
#
# from mixins import *
# from ..db_setup import *
# from ..domains import OrganisationDomain, AddressDomain, SocialDomain
#
#
# class OrganisationEntity(model, Timestamp):
#     __tablename__ = "organisations"
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(100), nullable=False)
#     email = Column(String, unique=True, index=True)
#     about = Column(Text)
#     phone = Column(String, nullable=False)
#     profile_link = Column(String, nullable=True)
#
#     socials = relationship("SocialEntity", back_populates="organisation")
#     address = relationship("AddressEntity", back_populates="organisation", uselist=False)
#
#
# class SocialEntity(model):
#     __tablename__ = "socials"
#
#     id = Column(Integer, primary_key=True, index=True)
#     social_name = Column(String(100), nullable=False)
#     url = Column(URLType, nullable=False)
#     organisation_id = Column(Integer, ForeignKey('organisations.id'))
#
#     organisation = relationship("OrganisationEntity", back_populates="socials")
#
#
# class AddressEntity(model):
#     __tablename__ = "address"
#
#     id = Column(Integer, primary_key=True, index=True)
#     address_line1 = Column(String(100), nullable=False)
#     address_line2 = Column(String(100), nullable=True)
#     country = Column(String(100), nullable=False)
#     state = Column(String(100), nullable=False)
#     city = Column(String(100), nullable=False)
#     code = Column(String, nullable=False)
#     organisation_id = Column(Integer, ForeignKey('organisations.id'))
#     organisation = relationship("OrganisationEntity", back_populates="address")
#
#
# def to_domain(self, organisation, address, socials) -> OrganisationDomain:
#     domain = OrganisationDomain()
#     domain.id = self.organisation.id
#     domain.name = self.organisation.name
#     domain.email = self.organisation.email
#     domain.phone = self.organisation.phone
#     domain.about = self.organisation.about
#     domain.profile_link = self.organisation.profile_link
#
#     address_domain = AddressDomain()
#     address_domain.country = self.address.country
#     address_domain.state = self.address.state
#     address_domain.city = self.address.city
#     address_domain.code = self.address.code
#     address_domain.address_line1 = self.address.address_line1
#     address_domain.address_line2 = self.address.address_line2
#
#     social_domains = []
#     for social_entities in self.socials:
#         social_domain = SocialDomain()
#         social_domain.social_name = social_entities.social_name
#         social_domain.id = social_entities.id
#         social_domain.url = social_entities.url
#         social_domain.organisation_id = social_entities.organisation_id
#         social_domains.append(social_domain)
#
#     domain.address = address_domain
#     domain.socials = social_domains
#     return domain
