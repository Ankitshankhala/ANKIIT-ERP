from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Numeric, Enum, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .base import BaseModel, Base


class EmploymentStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ON_LEAVE = "on_leave"


class Employee(BaseModel, Base):
    __tablename__ = "employees"

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(200), nullable=False, unique=True, index=True)
    phone = Column(String(50), nullable=True)
    department = Column(String(100), nullable=True)
    title = Column(String(100), nullable=True)
    status = Column(Enum(EmploymentStatus), nullable=False, default=EmploymentStatus.ACTIVE)
    attendance_records = relationship("Attendance", back_populates="employee")
    payrolls = relationship("Payroll", back_populates="employee")
    leaves = relationship("Leave", back_populates="employee")


class Attendance(BaseModel, Base):
    __tablename__ = "attendance"

    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    date = Column(DateTime, nullable=False, default=func.now())
    check_in = Column(DateTime, nullable=True)
    check_out = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    employee = relationship("Employee", back_populates="attendance_records")


class PayrollStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"


class Payroll(BaseModel, Base):
    __tablename__ = "payrolls"

    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    base_salary = Column(Numeric(12, 2), nullable=False)
    allowances = Column(Numeric(12, 2), nullable=False, default=0)
    deductions = Column(Numeric(12, 2), nullable=False, default=0)
    net_pay = Column(Numeric(12, 2), nullable=False)
    status = Column(Enum(PayrollStatus), nullable=False, default=PayrollStatus.PENDING)
    employee = relationship("Employee", back_populates="payrolls")


class LeaveType(str, enum.Enum):
    SICK = "sick"
    VACATION = "vacation"
    UNPAID = "unpaid"


class LeaveStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class Leave(BaseModel, Base):
    __tablename__ = "leaves"

    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    type = Column(Enum(LeaveType), nullable=False)
    status = Column(Enum(LeaveStatus), nullable=False, default=LeaveStatus.PENDING)
    reason = Column(Text, nullable=True)
    employee = relationship("Employee", back_populates="leaves")


