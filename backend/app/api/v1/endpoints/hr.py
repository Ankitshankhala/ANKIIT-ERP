from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ....core.database import get_db
from ....core.security import require_permission
from ....models.user import User
from ....services.hr_service import HRService
from ....schemas.hr import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
    EmployeeList,
    AttendanceCreate,
    AttendanceResponse,
    AttendanceList,
    PayrollCreate,
    PayrollResponse,
    PayrollList,
    LeaveCreate,
    LeaveResponse,
    LeaveList,
)

router = APIRouter()


@router.post('/employees', response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
async def create_employee(payload: EmployeeCreate, db: Session = Depends(get_db), current_user: User = Depends(require_permission('hr:employee:create'))):
    return HRService(db).create_employee(payload)


@router.get('/employees', response_model=EmployeeList)
async def list_employees(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), q: Optional[str] = Query(None), db: Session = Depends(get_db), current_user: User = Depends(require_permission('hr:employee:read'))):
    svc = HRService(db)
    employees = svc.list_employees(skip=skip, limit=limit, q=q)
    total = svc.count_employees(q=q)
    return EmployeeList(employees=employees, total=total, page=skip // limit + 1, size=limit)


@router.put('/employees/{employee_id}', response_model=EmployeeResponse)
async def update_employee(employee_id: int, payload: EmployeeUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_permission('hr:employee:update'))):
    svc = HRService(db)
    emp = svc.update_employee(employee_id, payload)
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Employee not found')
    return emp


@router.post('/attendance', response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
async def create_attendance(payload: AttendanceCreate, db: Session = Depends(get_db), current_user: User = Depends(require_permission('hr:attendance:create'))):
    return HRService(db).create_attendance(payload)


@router.get('/attendance', response_model=AttendanceList)
async def list_attendance(employee_id: Optional[int] = Query(None), skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db), current_user: User = Depends(require_permission('hr:attendance:read'))):
    svc = HRService(db)
    records = svc.list_attendance(employee_id=employee_id, skip=skip, limit=limit)
    total = svc.count_attendance(employee_id=employee_id)
    return AttendanceList(records=records, total=total, page=skip // limit + 1, size=limit)


@router.post('/payrolls', response_model=PayrollResponse, status_code=status.HTTP_201_CREATED)
async def create_payroll(payload: PayrollCreate, db: Session = Depends(get_db), current_user: User = Depends(require_permission('hr:payroll:create'))):
    return HRService(db).create_payroll(payload)


@router.get('/payrolls', response_model=PayrollList)
async def list_payrolls(employee_id: Optional[int] = Query(None), skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db), current_user: User = Depends(require_permission('hr:payroll:read'))):
    svc = HRService(db)
    records = svc.list_payrolls(employee_id=employee_id, skip=skip, limit=limit)
    total = svc.count_payrolls(employee_id=employee_id)
    return PayrollList(records=records, total=total, page=skip // limit + 1, size=limit)


@router.post('/leaves', response_model=LeaveResponse, status_code=status.HTTP_201_CREATED)
async def create_leave(payload: LeaveCreate, db: Session = Depends(get_db), current_user: User = Depends(require_permission('hr:leave:create'))):
    return HRService(db).create_leave(payload)


@router.get('/leaves', response_model=LeaveList)
async def list_leaves(employee_id: Optional[int] = Query(None), skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db), current_user: User = Depends(require_permission('hr:leave:read'))):
    svc = HRService(db)
    records = svc.list_leaves(employee_id=employee_id, skip=skip, limit=limit)
    total = svc.count_leaves(employee_id=employee_id)
    return LeaveList(records=records, total=total, page=skip // limit + 1, size=limit)


