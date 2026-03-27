from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.http.models.user_detail import UserDetail
from app.http.request.user_detail_request import UserDetailCreate, UserDetailUpdate
from app.core.security.security import sanitize_input
from app.services.user_services import _get_user_or_404

# Helpers
def _get_detail_or_404(db:Session, user_id:int) -> UserDetail:
    detail =  (
        db.query(UserDetail)
        .filter(UserDetail.id_user == user_id, UserDetail.deleted_at.is_(None))
        .first()
    )
    if not detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User detail not found!"
        )
    return detail

# User Detail CRUD
def get_user_detail(db:Session, user_id:int) -> UserDetail:
    _get_user_or_404(db, user_id)
    return _get_detail_or_404(db, user_id)

def create_user_detail(db:Session, user_id: int, payload: UserDetailCreate) -> UserDetail:
    _get_user_or_404(db, user_id)

    existing = (
        db.query(UserDetail)
        .filter(UserDetail.id_user == user_id, UserDetail.deleted_at.is_(None))
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User detail already exist. Use PUT to update!"
        )
    
    detail = UserDetail(
        id_user   = user_id,
        full_name = sanitize_input(payload.full_name),
        gender    = payload.gender,
        phone     = payload.phone,
        address   = sanitize_input(payload.address) if payload.address else None,
        role      = payload.role
    )
    db.add(detail)
    db.commit()
    db.refresh(detail)

    return detail

def update_user_detail(db:Session, user_id:int , payload: UserDetailUpdate) -> UserDetail:
    _get_user_or_404(db, user_id)
    detail = _get_detail_or_404(db, user_id)

    if payload.full_name is not None:
        detail.full_name = sanitize_input(payload.full_name)
    if payload.gender is not None:
        detail.gender = payload.gender
    if payload.phone is not None:
        detail.phone = payload.phone
    if payload.address is not None:
        detail.address = sanitize_input(payload.address)
    if payload.role is not None:
        detail.role = payload.role

    db.commit()
    db.refresh(detail)
    return detail


def soft_delete_user_detail(db:Session, user_id:int) -> dict:
    _get_user_or_404(db, user_id)
    detail = _get_detail_or_404(db, user_id)
    detail.deleted_at = datetime.now(timezone.utc)
    db.commit()
    return {
        "message" : f"User detail for user {user_id} deleted successfully!"
    }


