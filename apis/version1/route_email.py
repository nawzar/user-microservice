from fastapi import FastAPI,APIRouter,HTTPException
from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List
import os


class EmailSchema(BaseModel):
    email: List[EmailStr]

from dotenv import load_dotenv
load_dotenv('.env')


class Envs:
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_FROM = os.getenv('MAIL_FROM')
    MAIL_PORT = int(os.getenv('MAIL_PORT'))
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_FROM_NAME = os.getenv('MAIN_FROM_NAME')


conf = ConnectionConfig(
    MAIL_USERNAME=Envs.MAIL_USERNAME,
    MAIL_PASSWORD=Envs.MAIL_PASSWORD,
    MAIL_FROM=Envs.MAIL_FROM,
    MAIL_PORT=Envs.MAIL_PORT,
    MAIL_SERVER=Envs.MAIL_SERVER,
    MAIL_FROM_NAME=Envs.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER='./templates/email'
)

router = APIRouter()

@router.post("/email")
async def send_with_template(email: EmailSchema) -> JSONResponse:
    try:
        message = MessageSchema(
            subject="Fastapi-Mail module",
            recipients=email.dict().get("email"),
            template_body=email.dict().get("body"),
            subtype='html',
            )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="email_template.html")
        return JSONResponse(status_code=200, content={"message": "email has been sent"})
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
