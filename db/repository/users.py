from sqlalchemy.orm import Session
from schemas.user_schema import UserCreate,UserUpdate
from db.models.users import User
from db.models.address import Address
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from schemas.auth_schema import Resetpassword,ChangeEmail
from core.hashing import get_hash_password

from schemas.auth_schema import UserAuth, UserOut

def get_user_by_email(email: str, db: Session) -> Optional[User]:
    user = db.query(User).filter(User.email == email).first()
    return user

def create_address(address: Address,db : Session):
    try:
        db_address = Address(**address.dict())
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
        return db_address
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

def get_address(self, address_id: int):
    return self.db.query(Address).filter(Address.id == address_id).first()

def create_new_user(user: UserCreate,db : Session):
    try:
        print(db)
        user_dict = user.dict()
        user = User()
        password = get_hash_password(user_dict['password'])
        user.keycloakId = user_dict['keycloakId']
        user.permissionLevel = user_dict['permissionLevel']
        user.firstName = user_dict['firstName']
        user.lastName = user_dict['lastName']
        user.gender = user_dict['gender']
        user.email = user_dict['email']
        user.phone = user_dict['phone']
        user.username = user_dict['username']
        user.password = password
        user.birthDate = user_dict['birthDate']
        user.status = user_dict['status']
        user.birthDate = user_dict['birthDate']
        user.status = user_dict['status']
        user.modifiedAt = user_dict['modifiedAt']
        user.createdAt = user_dict['createdAt']
        db.add(user)
        db.commit()
        db.refresh(user)
        address = Address()
        address_dict = user_dict['address']
        address.address = address_dict['address']
        address.city = address_dict['city']
        address.postalCode = address_dict['postalCode']
        address.state = address_dict['state']
        address.primary = address_dict['primary']
        address.label = address_dict['label']
        address.user_id = user.id
        address.user = user
        db.add(address)
        db.commit()
        db.refresh(address)
        return user
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

def retreive_user(id: int, db: Session):
    user = db.query(User).filter(User.id == id).first()
    return user

def retreive_user_by_email(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user

def list_users(db: Session):
    users = db.query(User).all()
    return users

def update_user_by_email(id: int, data: Resetpassword, db: Session):
    db_user = db.query(User).filter(User.id == id).first()
    new_password = get_hash_password(data.new_password)

    db_user.password = new_password
    db.commit()
    db.refresh(db_user)
    return data

def update_user_new_email(id: int, data: ChangeEmail, db: Session):
    db_user = db.query(User).filter(User.id == id).first()
    db_user.email = data.new_email
    db.commit()
    db.refresh(db_user)
    return data


def update_user_by_id(id: int, user: UserUpdate, db: Session):
    db_user = db.query(User).filter(User.id == id).first()
    password = get_hash_password(user.password)
    db_user.keycloakId = user.keycloakId
    db_user.permissionLevel = user.permissionLevel
    db_user.firstName = user.firstName
    db_user.lastName = user.lastName
    db_user.gender = user.gender
    db_user.email = user.email
    db_user.phone = user.phone
    db_user.username = user.username
    db_user.password = password
    db_user.birthDate = user.birthDate
    db_user.status = user.status
    db_user.birthDate = user.birthDate
    db_user.status = user.status
    db_user.modifiedAt = user.modifiedAt
    # user.__dict__.update(owner_id=owner_id)
    db.commit()
    db.refresh(db_user)
    db_address = db.query(Address).filter(Address.user_id == id).first()
    if db_address is not None:
        db_address.address = user.address.address
        db_address.city = user.address.city
        db_address.postalCode = user.address.postalCode
        db_address.state = user.address.state
        db_address.primary = user.address.primary
        db.commit()
        db.refresh(db_address)
    return user

def delete_user_by_id(id: int, db: Session):
    existing_user = db.query(User).filter(User.id == id)
    if not existing_user.first():
        return 0
    existing_user.delete(synchronize_session=False)
    db.commit()
    return 1


    # def create_address_for_user(
    #     user_id: int, address: AddressCreate, db: Session = Depends(get_db)
    # ):
    #     user = db.query(User).filter(User.id == user_id).first()
    #     if not user:
    #         raise HTTPException(status_code=404, detail='User not found')
    #     db_address = Address(**address.dict(), user_id=user_id)
    #     db.add(db_address)
    #     db.commit()
    #     db.refresh(db_address)
    #     return db_address

    # @router.post("/users/", response_model=schemas.User)
    # def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    #     address = repositories.address_repository.create_address(db=db, address=user.address)
    #     user_dict = user.dict(exclude={"address"})
    #     user_dict["address_id"] = address.id
    #     db_user = models.User(**user_dict)
    #     db.add(db_user)
    #     db.commit()
    #     db.refresh(db_user)
    #     return db_user
    #
    # @router.get("/users/{user_id}", response_model=schemas.User)
    # def read_user(user_id: int, db: Session = Depends(database.get_db)):
    #     db_user = repositories.user_repository.get_user(db=db, user_id=user_id)
    #     if db_user is None:
    #         raise HTTPException(status_code=404, detail="User not found")
    #     return db_user