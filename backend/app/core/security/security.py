import re
import html
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.security.security_config import (
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
    JWT_ACCESS_TOKEN_EXPIRES_MINUTES,
    DANGEROUS_PATTERN,
)


# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Input Sanitization
def sanitize_input(value: str) -> str:
    """Escape HTML dan tolak pola berbahaya."""
    value = html.escape(value)
    lowered = value.lower()
    for pattern in DANGEROUS_PATTERN:
        if pattern in lowered:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Input contains forbidden characters or patterns"
            )
    return value


# JWT Token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRES_MINUTES)
    )
    payload.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def verify_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not valid or expired",
            headers={"WWW-Authenticate": "Bearer"}
        )


# Dependency — Current User
bearer_scheme = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    payload = verify_access_token(credentials.credentials)
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload invalid: missing subject"
        )

    return payload