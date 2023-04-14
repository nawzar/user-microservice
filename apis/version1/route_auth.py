from fastapi.security import OAuth2PasswordRequestForm
from apis.utils import OAuth2PasswordBearerWithCookie
from fastapi import Depends,HTTPException,status
from fastapi import APIRouter
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import jwt,JWTError
from fastapi import Response
from fastapi.responses import RedirectResponse
from db.models.users import User

from db.session import get_db
from db.repository.login import get_user_email,authenticate_user
from db.repository.users import retreive_user_by_email,update_user_by_email

from core.config import settings
from core.security import create_access_token,create_refresh_token
from core.hashing import get_hash_password

from schemas.auth_schema import UserAuth, UserOut, SystemUser, Resetpassword

from typing import Any


router = APIRouter()

@router.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')

@router.post('/signup')
def signup_user(data: UserAuth,db: Session = Depends(get_db)):
    # querying database to check if user already exist
    user_model = User()
    # user = db.query(User).filter(User.email == data.email).first()
    user = retreive_user_by_email(data.email,db)
    if user is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    user = {
        'email': data.email,
        'password': get_hash_password(data.password)
    }
    user_model.email = user['email']
    user_model.password = user['password']
    user_model.permissionLevel = 'user'
    user = db.add(user_model)
    db.commit()
    return {"message":"User is successfully register"}

@router.post('/login', summary="Create access and refresh tokens for user")
async def login(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)) -> Any:

    user = authenticate_user(username=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
    }

@router.post('/resetpassword', response_model=Resetpassword)
def reset_password(data: Resetpassword,db: Session = Depends(get_db)):
    # querying database to check if user already exist
    user_model = User()
    user = retreive_user_by_email(email=data.email, db=db)
    if user is None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found"
        )
    updated_user = update_user_by_email(user.id,data,db)
    return updated_user

@router.post("/token")
def login_for_access_token(response:Response,form_data:OAuth2PasswordRequestForm=Depends(),
    db:Session = Depends(get_db)):
    user = authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password")
    access_token_expire = timedelta(minutes= settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(subject=user.email,expires_delta=access_token_expire)
    response.set_cookie(key="access_token",value=f"Bearer {access_token}",httponly=True)
    return {"access_token":access_token,"token_type":"bearer"}

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/login/token")


def get_current_user_from_token(token:str = Depends(oauth2_scheme),db:Session=Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials")
    try:
        payload = jwt.decode(token,settings.JWT_SECRET_KEY,algorithms=[settings.ALGORITHM])
        username:str = payload.get("sub")
        print("email is",username)
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_email(username=username, db=db)
    if user is None:
        raise credentials_exception
    return user

@router.get('/me', summary='Get details of currently logged in user', response_model=UserOut)
async def get_me(user: SystemUser = Depends(get_current_user_from_token)):
    return user




