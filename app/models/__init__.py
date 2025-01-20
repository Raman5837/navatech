from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Admin(Base):
    """
    For Admin's information (email, password, etc.)
    """

    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)

    password = Column(String)
    email = Column(String, unique=True, index=True)

    organization_id = Column(Integer, ForeignKey("organizations.id"))
    organization = relationship("Organization", back_populates="admins")


class Organization(Base):
    """
    To store Organization's metadata
    """

    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, unique=True, index=True)

    admins = relationship("Admin", back_populates="organization")
    db_info = relationship("DynamicDB", back_populates="organization", uselist=False)


class DynamicDB(Base):
    """
    To store the dynamic database information for each organization
    """

    __tablename__ = "dynamic_db"
    id = Column(Integer, primary_key=True, index=True)

    url = Column(String, unique=True)
    name = Column(String, unique=True)

    resource_id = Column(Integer, ForeignKey("organizations.id"))
    organization = relationship("Organization", back_populates="db_info")
