from sqlalchemy import Column, Integer, String, Boolean, Date , ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base

class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(100))
    city = Column(String(100))
    postalCode = Column(String(50))
    state = Column(String(50))
    primary = Column(Boolean(), default=True)
    label = Column(String(50))
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="address")

