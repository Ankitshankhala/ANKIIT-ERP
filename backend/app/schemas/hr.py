from typing import Optional, List
from datetime import datetime, date
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


class PayrollCreate(BaseModel):
    employee_id: int
    period_start: date
    period_end: date
    base_salary: float
    allowances: Optional[float] = 0
    deductions: Optional[float] = 0
    net_pay: Optional[float] = None
    status: Optional[str] = Field('pending')


class PayrollResponse(PayrollCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PayrollList(BaseModel):
    records: List[PayrollResponse]
    total: int
    page: int
    size: int


class LeaveCreate(BaseModel):
    employee_id: int
    start_date: date
    end_date: date
    type: str
    status: Optional[str] = Field('pending')
    reason: Optional[str] = Field(None, max_length=1000)


class LeaveResponse(LeaveCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LeaveList(BaseModel):
    records: List[LeaveResponse]
    total: int
    page: int
    size: int


