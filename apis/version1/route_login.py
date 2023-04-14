from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi import Response

from db.session import get_db
from db.repository.login import get_user_email,authenticate_user

from core.config import settings
from core.security import create_access_token,create_refresh_token


router = APIRouter()

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