from fastapi import APIRouter

main_router = APIRouter()
from .auth import auth_router

main_router.include_router(auth_router)
from .authRegUser import regUser_router

main_router.include_router(regUser_router)

from .authCategory import catUser_router

main_router.include_router(catUser_router)
