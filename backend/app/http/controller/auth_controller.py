from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.security.security import get_current_user
from app.core.security.limiter import limiter
from app.core.config.security_config import RATE_LIMIT_CREATE

from app.http.request.auth_request import LoginRequest, TokenResponse
from app.services import auth_services

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login",response_model=TokenResponse, summary="Login")
@limiter.limit(RATE_LIMIT_CREATE)
def login(
    request : Request,
    payload : LoginRequest,
    db      : Session = Depends(get_db),
):
    return auth_services.login(db, payload)


@router.get("/me", summary="Get currend logged in")
def me(current_user: dict = Depends(get_current_user)):
    return {
        "id_user"  : current_user.get("sub"),
        "username" : current_user.get("username"),
        "role"     : current_user.get("role")
    }

@router.post("/logout", summary="Logout")
def logout(_ : dict = Depends(get_current_user)):
    return {
        "message" : "Logged out successfully!"
    }