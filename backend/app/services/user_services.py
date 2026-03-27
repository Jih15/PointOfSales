from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.http.models.user import User
from app.http.models.user_detail import UserDetail
from app.http.request.user_request import UserCreate, UserUpdate

from app.core.security.security import hash_password, sanitize_input


# Helpers
def _get_user_or_404(db: Session, user_id: int) -> User:
    user = (
        db.query(User)
        .filter(User.id_user == user_id, User.deleted_at.is_(None))
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

def _assert_unique_username(db: Session, username: str, exclude_id: Optional[int]=None):
    q = db.query(User).filter(User.username == username, User.deleted_at.is_(None))
    if exclude_id:
        q = q.filter(User.id_user != exclude_id)
    if q.first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already taken!"
        )
    
def _assert_unique_email(db: Session, email: str, exclude_id: Optional[int] = None):
    q = db.query(User).filter(User.email == email, User.deleted_at.is_(None))
    if exclude_id:
        q = q.filter(User.id_user != exclude_id)
    if q.first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered!"
        )
    

# USER CRUD
def get_all_users(db: Session, page: int = 1, limit: int = 20)-> dict:
    offset = (page - 1) * limit
    query  = db.query(User).filter(User.deleted_at.is_(None))
    total  = query.count()
    users  = query.offset(offset).limit(limit).all()

    return {
        "total" : total,
        "page"  : page,
        "limit" : limit,
        "data"  : users
    }

def get_users_by_id(db: Session, user_id: int) -> User:
    return _get_user_or_404(db, user_id)

def create_user(db: Session, payload: UserCreate)-> User:
    _assert_unique_username(db, payload.username)
    _assert_unique_email(db, payload.email)

    user = User(
        username  = sanitize_input(payload.username),
        email     = sanitize_input(payload.email),
        password  = hash_password(payload.password),
        is_active = True, 
    )
    db.add(User)
    db.flush()

    d = payload.detail
    detail = UserDetail(
        id_user   = user.id_user,
        full_name = sanitize_input(d.full_name),
        gender    = d.gender,
        phone     = d.phone,
        address   = sanitize_input(d.address) if d.address else None,
        role      = d.role,
    )
    db.add(detail)

    db.commit()
    db.refresh(User)
    return User

def update_user(db: Session, user_id: int, payload: UserUpdate) -> User:
    user = _get_user_or_404(db, user_id)

    if payload.username is not None:
        _assert_unique_username(db, payload.username, exclude_id=user_id)
        user.username = sanitize_input(payload.username)

    if payload.email is not None:
        _assert_unique_email(db, payload.email, exclude_id=user_id)
        user.email = sanitize_input(payload.email)

    if payload.password is not None:
        user.password = hash_password(payload.password)

    if payload.is_active is not None:
        user.is_active = payload.is_active

    db.commit()
    db.refresh(User)
    return User

def soft_delete_user(db: Session, user_id: int) -> dict:
    user = _get_user_or_404(db, user_id)
    now  = datetime.now(timezone.utc) 

    user.deleted_at = now
    if user.detail:
        user.detail.deleted_at = now

    db.commit()
    return {
        "message": f"User {user_id} deleted successfully!"
    }