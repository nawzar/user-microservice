from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from db.session import get_db
from db.models.users import User
from schemas.user_schema import UserCreate,UserUpdate,ShowUser
from schemas.auth_schema import Resetpassword,ChangeEmail
from db.repository.users import (create_new_user,
        retreive_user,list_users,
        update_user_by_id,
        delete_user_by_id,
        retreive_user_by_email,
        update_user_by_email,
        update_user_new_email)

from apis.utils import OAuth2PasswordBearerWithCookie
from jose import jwt,JWTError
from core.config import settings
from db.repository.login import get_user_authentication,authenticate_user
from apis.deps.user_deps import get_current_user_from_token,get_current_user

from typing import List


router = APIRouter()



@router.post("/create-user",response_model=ShowUser)
def create_user(user: UserCreate,db : Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    try:
        user = create_new_user(user=user, db=db)
        return user
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.get("/get/{id}")
def retreive_user_by_id(id:int,db:Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    user = retreive_user(id=id, db=db)
    print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Job with id {id} does not exist")
    return user

@router.get("/all")
def retreive_all_users(db:Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    users = list_users(db=db)
    return users

@router.put("/update/{id}")
def update_user(id:int,user:UserUpdate,db:Session=Depends(get_db)):
    user_retrieved = retreive_user(id=id, db=db)
    if not user_retrieved:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Job with id {id} does not exist")
    message = update_user_by_id(id=id, user=user, db=db)
    return {"detail":"Successfully updated data."}

@router.delete("/delete/{id}")
def delete_user(id:int,db:Session=Depends(get_db),current_user: User = Depends(get_current_user)):
    user = retreive_user(id=id, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id {id} does not exist")
    delete_user_by_id(id=id, db=db)
    return {"detail":"User Successfully deleted"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    detail="You are not permitted!!")


@router.post('/change/password')
def change_password(data: Resetpassword,db: Session = Depends(get_db)):
    # querying database to check if user already exist
    user_model = User()
    user = retreive_user_by_email(email=data.email, db=db)
    if user is None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found"
        )
    updated_user = update_user_by_email(user.id,data,db)
    return {"detail":"Password Successfully changed "}

@router.post('/change/email')
def change_password(data: ChangeEmail,db: Session = Depends(get_db)):
    # querying database to check if user already exist
    user_model = User()
    user = retreive_user_by_email(email=data.old_email, db=db)
    if user is None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found"
        )
    updated_user = update_user_new_email(user.id,data,db)
    return {"detail":"Email Successfully updated "}

