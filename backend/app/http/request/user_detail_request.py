from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator

from app.http.models.user import RoleEnum

# Request
class UserDetailCreate(BaseModel):
    full_name   : str
    gender      : Optional[str] = None
    phone       : Optional[str] = None
    address     : Optional[str] = None
    role        : RoleEnum      = RoleEnum.cashier

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, v):
        if len(v.strip()) < 2:
            raise ValueError("Full name must be at least 2 character")
        return v.strip()
    
    @field_validator
    @classmethod
    def validate_gender(cls, v):
        if v and v not in ("male", "female"):
            raise ValueError("Gender must be 'male' or 'female'")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        if v and not v.replace("+","").replace("-","").isdigit():
            raise ValueError("Phone number is not valid")
        if v and len(v) > 20:
            raise ValueError("Phone number is too long")
        return v
    
class UserDetailUpdate(BaseModel):
    full_name   : Optional[str]      = None
    gender      : Optional[str]      = None
    phone       : Optional[str]      = None
    address     : Optional[str]      = None
    role        : Optional[RoleEnum] = None  

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, v):
        if len(v.strip()) < 2:
            raise ValueError("Full name must be at least 2 character")
        return v.strip()
    
    @field_validator
    @classmethod
    def validate_gender(cls, v):
        if v and v not in ("male", "female"):
            raise ValueError("Gender must be 'male' or 'female'")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        if v and not v.replace("+","").replace("-","").isdigit():
            raise ValueError("Phone number is not valid")
        if v and len(v) > 20:
            raise ValueError("Phone number is too long")
        return v
    
# Response

class UserDetailResponse(BaseModel):
    id_detail   : int
    id_user     : int
    full_name   : str
    gender      : Optional[str]
    phone       : Optional[str]
    address     : Optional[str]
    role        : RoleEnum
    created_at  : datetime
    updated_at  : datetime
 
    model_config = {"from_attributes": True}
 
