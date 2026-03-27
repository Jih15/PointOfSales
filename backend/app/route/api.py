from fastapi import APIRouter

from app.http.controller.auth_controller import router as auth_router
from app.http.controller.user_controller import router as user_router


api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(user_router)