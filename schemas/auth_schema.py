from uuid import UUID
from pydantic import BaseModel, Field


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: UUID = None
    exp: int = None

class UserAuth(BaseModel):
    email: str
    password: str

class Resetpassword(BaseModel):
    email: str
    old_password: str
    new_password: str

class ChangeEmail(BaseModel):
    old_email: str
    new_email: str

class UserOut(BaseModel):
    id: int
    email: str

class SystemUser(UserOut):
    id: int
    email: str

class ResetPasswordResponse(BaseModel):
    message: str

class ResetPasswordRequest(BaseModel):
    username: str
    email: str
