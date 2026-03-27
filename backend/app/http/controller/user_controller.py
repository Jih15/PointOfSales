from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.security.security import get_current_user

from app.http.request.user_request import UserCreate, UserUpdate, UserResponse, UserListResponse
from app.http.request.user_detail_request import UserDetailCreate, UserDetailUpdate, UserDetailResponse

from app.services import user_services, user_detail_services

router = APIRouter(prefix="/users", tags=["Users"])


# User
@router.get("/", response_model=UserListResponse, summary="Get all users")
def index(
    page  : int      = Query(default=1, ge=1),
    limit : int      = Query(default=20, ge=1, le=100),
    db    : Session  = Depends(get_db),
    _     : dict     = Depends(get_current_user),
): 
    return user_services.get_all_users(db, page=page, limit=limit)

@router.get("/{user_id}", response_model=UserResponse, summary="Get user by ID")
def show(
    user_id : int,
    db      : Session = Depends(get_db),
    _       : dict    = Depends(get_current_user),
):
    return user_services.get_users_by_id(db, user_id)

@router.post("/", response_model=UserResponse, status_code=201, summary="Create user")
def store(
    payload : UserCreate,
    db      : Session = Depends(get_db),
    _       : dict    = Depends(get_current_user),
):
    return user_services.create_user(db, payload)

@router.put("/{user_id}", response_model=UserResponse, summary="Update user")
def update(
    user_id : int,
    payload : UserUpdate,
    db      : Session = Depends(get_db),
    _       : dict    = Depends(get_current_user),
): 
    return user_services.update_user(db, payload, user_id)

@router.delete("/{user_id}", summary="Delete user")
def destroy(
    user_id : int,
    db      : Session = Depends(get_db),
    _       : dict    = Depends(get_current_user),
):
    return user_services.soft_delete_user(db, user_id)
    

# User Detail
@router.get("/{user_id}/detail", response_model=UserDetailResponse, summary="Get users detail")
def show_detail(
    user_id : int, 
    db      : Session = Depends(get_db),
    _       : dict    = Depends(get_current_user),
):
    return user_detail_services.get_user_detail(db, user_id)

@router.post("/{user_id}/detail", response_model=UserDetailResponse, status_code=201, summary="Create user detail")
def store_detail(
    user_id : int, 
    payload : UserDetailCreate,
    db      : Session = Depends(get_db),
    _       : dict    = Depends(get_current_user)
):
    return user_detail_services.create_user_detail(db, user_id, payload)

@router.put("/{user_id}/detail", response_model=UserDetailResponse, summary="Update user detail")
def update_detail(
    user_id : int,
    payload : UserDetailUpdate,
    db      : Session = Depends(get_db),
    _       : dict    = Depends(get_current_user)
):
    return user_detail_services.update_user_detail(db, user_id, payload)

@router.delete("/{user_id}/detail", summary="Delete user detail")
def destroy_detail(
    user_id : int,
    db      : Session = Depends(get_db),
    _       : dict    = Depends(get_current_user)
):
    return user_detail_services.soft_delete_user_detail(db, user_id)