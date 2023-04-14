from typing import List, Optional
from pydantic import BaseModel
from datetime import date,datetime
from schemas.address_schema import Address,AddressCreate,AddressUpdate

class UserBase(BaseModel):
    keycloakId: Optional[int] =None
    permissionLevel: Optional[str] =None
    firstName: Optional[str] =None
    lastName: Optional[str] =None
    gender: Optional[str] =None
    email: Optional[str] =None
    phone: Optional[str] =None
    username: Optional[str] =None
    password: Optional[str] =None
    birthDate: Optional[date] =datetime.now().date()
    address: AddressCreate
    createdAt: date = datetime.now().date()
    modifiedAt: date = datetime.now().date()
    status: Optional[str] =None

class UserCreate(UserBase):
    keycloakId:int
    permissionLevel: str
    firstName: str
    lastName: str
    gender: str
    email: str
    phone: str
    username: str
    password: str
    birthDate: date
    address: AddressCreate
    createdAt: date = datetime.now().date()
    modifiedAt: date = datetime.now().date()
    status: str

class UserUpdate(UserBase):
    keycloakId: Optional[int] = None
    permissionLevel: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    gender: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    username: Optional[str] = None
    birthDate: date
    status: str
    modifiedAt: date = datetime.now().date()
    address: AddressUpdate

class ShowUser(UserBase):
    id: int
    keycloakId: int
    permissionLevel: str
    firstName: str
    lastName: str
    gender: str
    email: str
    phone: str
    username: str
    # password: str
    birthDate: date
    status: str
    address: Address
    createdAt: date
    modifiedAt: date


    class Config:
        orm_mode = True


class UserOut(UserBase):
    id: int
    email: str

    class Config:
        orm_mode = True
        exclude = ["session"]


class User(UserBase):
    keycloakId: int
    permissionLevel: str
    firstName: str
    lastName: str
    gender: str
    email: str
    phone: str
    username: str
    password: str
    birthDate: date
    status: str
    createdAt: date
    modifiedAt: date
    address: Address = None

    class Config:
        orm_mode = True

