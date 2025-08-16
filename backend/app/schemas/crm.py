from typing import Optional, List, Dict
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, Field


class CustomerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: Optional[str] = Field(None, max_length=200)
    phone: Optional[str] = Field(None, max_length=50)
    address: Optional[str] = Field(None, max_length=2000)
    website: Optional[str] = Field(None, max_length=200)
    is_active: bool = True


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    email: Optional[str] = Field(None, max_length=200)
    phone: Optional[str] = Field(None, max_length=50)
    address: Optional[str] = Field(None, max_length=2000)
    website: Optional[str] = Field(None, max_length=200)
    is_active: Optional[bool] = None


class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CustomerList(BaseModel):
    customers: List[CustomerResponse]
    total: int
    page: int
    size: int


class LeadBase(BaseModel):
    customer_id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=200)
    email: Optional[str] = Field(None, max_length=200)
    phone: Optional[str] = Field(None, max_length=50)
    source: Optional[str] = Field(None, max_length=100)
    status: Optional[str] = Field('new')
    notes: Optional[str] = Field(None, max_length=2000)


class LeadCreate(LeadBase):
    pass


class LeadUpdate(BaseModel):
    customer_id: Optional[int] = None
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    email: Optional[str] = Field(None, max_length=200)
    phone: Optional[str] = Field(None, max_length=50)
    source: Optional[str] = Field(None, max_length=100)
    status: Optional[str] = None
    notes: Optional[str] = Field(None, max_length=2000)


class LeadResponse(LeadBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LeadList(BaseModel):
    leads: List[LeadResponse]
    total: int
    page: int
    size: int


class OpportunityBase(BaseModel):
    customer_id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=200)
    value: Decimal = Field(0, ge=0)
    stage: Optional[str] = Field('prospecting')
    close_date: Optional[datetime] = None
    notes: Optional[str] = Field(None, max_length=2000)


class OpportunityCreate(OpportunityBase):
    pass


class OpportunityUpdate(BaseModel):
    customer_id: Optional[int] = None
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    value: Optional[Decimal] = Field(None, ge=0)
    stage: Optional[str] = None
    close_date: Optional[datetime] = None
    notes: Optional[str] = Field(None, max_length=2000)


class OpportunityResponse(OpportunityBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OpportunityList(BaseModel):
    opportunities: List[OpportunityResponse]
    total: int
    page: int
    size: int


class CommunicationBase(BaseModel):
    customer_id: Optional[int] = None
    lead_id: Optional[int] = None
    opportunity_id: Optional[int] = None
    type: str = Field(..., max_length=20)
    subject: Optional[str] = Field(None, max_length=200)
    content: Optional[str] = Field(None, max_length=2000)
    occurred_at: Optional[datetime] = None


class CommunicationCreate(CommunicationBase):
    pass


class CommunicationResponse(CommunicationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CommunicationList(BaseModel):
    communications: List[CommunicationResponse]
    total: int
    page: int
    size: int


OpportunityPipeline = Dict[str, List[OpportunityResponse]]


