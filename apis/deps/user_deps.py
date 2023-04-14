from fastapi.security import OAuth2PasswordRequestForm
from apis.utils import OAuth2PasswordBearerWithCookie
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from jose import jwt,JWTError

from db.session import get_db
from core.config import settings
from db.repository.login import get_user_email,authenticate_user
from db.repository.login import get_user_authentication,authenticate_user

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/login/token")


async def get_current_user_from_token(token:str = Depends(oauth2_scheme),db:Session=Depends(get_db)):
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


async def get_current_user(token:str = Depends(oauth2_scheme),db:Session=Depends(get_db)):
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
    user = get_user_authentication(username=username, db=db)
    if user is None:
        raise credentials_exception
    return user
