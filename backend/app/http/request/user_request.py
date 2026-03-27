from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator

from app.http.request.user_detail_request import UserDetailCreate, UserDetailResponse

# Request

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    detail: UserDetailCreate

    @field_validator("username")
    @classmethod
    def validate_username(cls, v:str) -> str:
        v = v.strip()
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters!")
        if len(v) > 20:
            raise ValueError("Username must not exceed 50 characters!")
        if not v.replace("_","").replace("-","").isalnum():
            raise ValueError("Username may only contain letters, numbers, hypens and underscore!")
        return v.lower()
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v:str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters!")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter!")
        if not any(c.isdigit() for c in v):
            raise ValueError("Pasword must contain at least one digit number!")
        return v
    
class UserUpdate(BaseModel):
    username : Optional[str]      = None
    email    : Optional[EmailStr] = None
    password : Optional[str]      = None
    is_active: Optional[bool]     = None

    @field_validator("username")
    @classmethod
    def validate_username(cls, v:str) -> str:
        v = v.strip()
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters!")
        if len(v) > 20:
            raise ValueError("Username must not exceed 50 characters!")
        if not v.replace("_","").replace("-","").isalnum():
            raise ValueError("Username may only contain letters, numbers, hypens and underscore!")
        return v.lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v:str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters!")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter!")
        if not any(c.isdigit() for c in v):
            raise ValueError("Pasword must contain at least one digit number!")
        return v
    
# Response 
class UserResponse(BaseModel):
    id_user    : int
    username   : str
    email      : str
    is_active  : bool
    created_at : datetime
    updated_at : datetime
    detail     : Optional[UserDetailResponse]

    model_config = {
        "from_attributes" : True
    } 

class UserListResponse(BaseModel):
    total : int
    page  : int
    limit : int
    data  : list[UserResponse]  