from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Numeric, Enum
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


class Attendance(BaseModel, Base):
    __tablename__ = "attendance"

    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    date = Column(DateTime, nullable=False, default=func.now())
    check_in = Column(DateTime, nullable=True)
    check_out = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)


