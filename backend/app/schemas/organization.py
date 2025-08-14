from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime


class OrganizationBase(BaseModel):
    name: str
    display_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    founded_year: Optional[str] = None
    tax_id: Optional[str] = None
    timezone: str = "UTC"
    currency: str = "USD"
    language: str = "en"
    date_format: str = "YYYY-MM-DD"


class OrganizationCreate(OrganizationBase):
    enabled_modules: List[str] = []
    subscription_plan: str = "basic"
    max_users: int = 10


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    display_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    founded_year: Optional[str] = None
    tax_id: Optional[str] = None
    timezone: Optional[str] = None
    currency: Optional[str] = None
    language: Optional[str] = None
    date_format: Optional[str] = None
    enabled_modules: Optional[List[str]] = None
    subscription_plan: Optional[str] = None
    max_users: Optional[int] = None
    logo_url: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None


class OrganizationResponse(OrganizationBase):
    id: int
    slug: str
    enabled_modules: List[str]
    subscription_plan: str
    max_users: int
    is_active: bool
    is_verified: bool
    trial_ends_at: Optional[datetime]
    logo_url: Optional[str]
    primary_color: str
    secondary_color: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrganizationList(BaseModel):
    id: int
    name: str
    slug: str
    email: Optional[str]
    industry: Optional[str]
    company_size: Optional[str]
    subscription_plan: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
