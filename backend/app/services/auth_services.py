from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.http.models.user import User
from app.http.request.auth_request import LoginRequest, TokenResponse
from app.core.security.security import verify_password, create_access_token, sanitize_input
from app.core.config.security_config import JWT_ACCESS_TOKEN_EXPIRES_MINUTES

def login(db: Session, payload: LoginRequest)-> TokenResponse:
    username = sanitize_input(payload.username.strip().lower())

    user = (
        db.query(User)
        .filter(User.username == username, User.deleted_at.is_(None))
        .first()
    )

    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password!",
            headers={"WWW-Authenticate" : "Bearer"}
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive. Contact administrator."
        )
    
    
    token = create_access_token(data={
        "sub"      : str(user.id_user),
        "username" : user.username,
        "role"     : user.detail.role if user.detail else None
    })

    return TokenResponse(
        access_token=token,
        token_type= "bearer",
        expires_in= JWT_ACCESS_TOKEN_EXPIRES_MINUTES * 60
    )