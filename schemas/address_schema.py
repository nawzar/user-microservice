from pydantic import BaseModel
from typing import List, Optional

class AddressBase(BaseModel):
    address: str
    city: str
    postalCode: str
    state: str
    primary: bool
    label : str

class AddressCreate(AddressBase):
    pass

class AddressUpdate(AddressBase):
    address: Optional[str] = ''
    city: Optional[str] = ''
    postalCode: Optional[str] = ''
    state: Optional[str] = ''
    primary: Optional[bool] = True
    label: Optional[str] = ''


class Address(AddressBase):
    id: int
    user_id: int
    address: str
    city: str
    postalCode: str
    state: str
    primary: bool
    label: str

    class Config:
        orm_mode = True