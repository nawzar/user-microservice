from sqlalchemy import Column, Integer, String, Boolean, Date , ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base
from uuid import UUID, uuid4
from pydantic import EmailStr

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    keycloakId = Column(Integer)
    permissionLevel = Column(String,nullable=False)
    firstName = Column(String)
    lastName = Column(String)
    gender = Column(String)
    email = Column(String,nullable=False,unique=True,index=True)
    phone = Column(String)
    username = Column(String)
    password = Column(String, nullable=False)
    birthDate = Column(Date)
    avatar = Column(String)
    status = Column(String, default=True)
    createdAt = Column(Date)
    modifiedAt = Column(Date)
    address = relationship("Address", uselist=False, back_populates="user")
    status = Column(String)
    # is_superuser = Column(Boolean(), default=False)
