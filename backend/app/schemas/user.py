from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str] = None
    is_active: bool = True


class UserCreate(UserBase):
    password: str
    organization_id: Optional[int] = None
    role_id: Optional[int] = None


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    timezone: Optional[str] = None
    language: Optional[str] = None


class UserResponse(UserBase):
    id: int
    is_verified: bool
    avatar_url: Optional[str]
    bio: Optional[str]
    timezone: str
    language: str
    organization_id: int
    role_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserList(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    is_active: bool
    organization_id: int
    role_id: int
    created_at: datetime

    class Config:
        from_attributes = True
