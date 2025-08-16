from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime

from ..models.hr import Employee, Attendance, Payroll, Leave
from ..schemas.hr import (
    EmployeeCreate,
    EmployeeUpdate,
    AttendanceCreate,
    PayrollCreate,
    LeaveCreate,
)


class HRService:
    def __init__(self, db: Session):
        self.db = db

    # Employees
    def create_employee(self, data: EmployeeCreate) -> Employee:
        employee = Employee(**data.dict())
        self.db.add(employee)
        self.db.commit()
        self.db.refresh(employee)
        return employee

    def update_employee(self, employee_id: int, data: EmployeeUpdate) -> Optional[Employee]:
        employee = self.db.query(Employee).filter(Employee.id == employee_id).first()
        if not employee:
            return None
        for field, value in data.dict(exclude_unset=True).items():
            setattr(employee, field, value)
        self.db.commit()
        self.db.refresh(employee)
        return employee

    def list_employees(self, skip: int = 0, limit: int = 10, q: Optional[str] = None) -> List[Employee]:
        query = self.db.query(Employee)
        if q:
            like = f"%{q}%"
            query = query.filter((Employee.first_name.ilike(like)) | (Employee.last_name.ilike(like)) | (Employee.email.ilike(like)))
        return query.order_by(desc(Employee.created_at)).offset(skip).limit(limit).all()

    def count_employees(self, q: Optional[str] = None) -> int:
        query = self.db.query(Employee)
        if q:
            like = f"%{q}%"
            query = query.filter((Employee.first_name.ilike(like)) | (Employee.last_name.ilike(like)) | (Employee.email.ilike(like)))
        return query.count()

    # Attendance
    def create_attendance(self, data: AttendanceCreate) -> Attendance:
        attendance = Attendance(**data.dict())
        self.db.add(attendance)
        self.db.commit()
        self.db.refresh(attendance)
        return attendance

    def list_attendance(self, employee_id: Optional[int] = None, skip: int = 0, limit: int = 10) -> List[Attendance]:
        query = self.db.query(Attendance)
        if employee_id:
            query = query.filter(Attendance.employee_id == employee_id)
        return query.order_by(desc(Attendance.date)).offset(skip).limit(limit).all()

    def count_attendance(self, employee_id: Optional[int] = None) -> int:
        query = self.db.query(Attendance)
        if employee_id:
            query = query.filter(Attendance.employee_id == employee_id)
        return query.count()

    # Payroll
    def create_payroll(self, data: PayrollCreate) -> Payroll:
        payload = data.dict()
        if payload.get("net_pay") is None:
            payload["net_pay"] = payload.get("base_salary", 0) + payload.get("allowances", 0) - payload.get("deductions", 0)
        payroll = Payroll(**payload)
        self.db.add(payroll)
        self.db.commit()
        self.db.refresh(payroll)
        return payroll

    def list_payrolls(self, employee_id: Optional[int] = None, skip: int = 0, limit: int = 10) -> List[Payroll]:
        query = self.db.query(Payroll)
        if employee_id:
            query = query.filter(Payroll.employee_id == employee_id)
        return query.order_by(desc(Payroll.period_start)).offset(skip).limit(limit).all()

    def count_payrolls(self, employee_id: Optional[int] = None) -> int:
        query = self.db.query(Payroll)
        if employee_id:
            query = query.filter(Payroll.employee_id == employee_id)
        return query.count()

    # Leave
    def create_leave(self, data: LeaveCreate) -> Leave:
        leave = Leave(**data.dict())
        self.db.add(leave)
        self.db.commit()
        self.db.refresh(leave)
        return leave

    def list_leaves(self, employee_id: Optional[int] = None, skip: int = 0, limit: int = 10) -> List[Leave]:
        query = self.db.query(Leave)
        if employee_id:
            query = query.filter(Leave.employee_id == employee_id)
        return query.order_by(desc(Leave.start_date)).offset(skip).limit(limit).all()

    def count_leaves(self, employee_id: Optional[int] = None) -> int:
        query = self.db.query(Leave)
        if employee_id:
            query = query.filter(Leave.employee_id == employee_id)
        return query.count()


