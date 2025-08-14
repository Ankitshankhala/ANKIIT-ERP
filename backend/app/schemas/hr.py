from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class EmployeeBase(BaseModel):
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    email: str = Field(..., max_length=200)
    phone: Optional[str] = Field(None, max_length=50)
    department: Optional[str] = Field(None, max_length=100)
    title: Optional[str] = Field(None, max_length=100)
    status: Optional[str] = Field('active')


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=50)
    department: Optional[str] = Field(None, max_length=100)
    title: Optional[str] = Field(None, max_length=100)
    status: Optional[str] = None


class EmployeeResponse(EmployeeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EmployeeList(BaseModel):
    employees: List[EmployeeResponse]
    total: int
    page: int
    size: int


class AttendanceCreate(BaseModel):
    employee_id: int
    date: Optional[datetime] = None
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None
    notes: Optional[str] = Field(None, max_length=1000)


class AttendanceResponse(AttendanceCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AttendanceList(BaseModel):
    records: List[AttendanceResponse]
    total: int
    page: int
    size: int


