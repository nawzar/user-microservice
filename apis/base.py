from fastapi import APIRouter

from apis.version1 import route_users
from apis.version1 import route_auth
from apis.version1 import route_login

api_router = APIRouter()

api_router.include_router(route_auth.router,prefix="/auth",tags=["Auth"])
api_router.include_router(route_users.router,prefix="/users",tags=["User Management"])
api_router.include_router(route_login.router,prefix="/login",tags=["Login"])