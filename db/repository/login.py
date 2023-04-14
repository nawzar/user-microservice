from sqlalchemy.orm import Session
from db.models.users import User
from core.hashing import get_hash_password,verify_password

def get_user(username:str,db:Session):
    user = db.query(User).filter(User.email == username).first()
    return user

def get_user_email(username:str,db:Session):
    user = db.query(User.id,User.email).filter(User.email == username).first()
    return user

def get_user_authentication(username:str,db:Session):
    user = db.query(User).filter(User.email == username).first()
    if user.permissionLevel == 'admin':
        return user
    else:
        return None

def authenticate_user(username:str,password:str,db:Session):
    user = get_user(username=username,db=db)
    print(user)
    if not user:
        return False
    if not verify_password(password,user.password):
        return False
    return user