from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ....core.database import get_db
from ....core.security import require_permission
from ....models.user import User
from ....services.crm_service import CRMService
from ....schemas.crm import (
    CustomerCreate, CustomerUpdate, CustomerResponse, CustomerList,
    LeadCreate, LeadUpdate, LeadResponse, LeadList,
    OpportunityCreate, OpportunityUpdate, OpportunityResponse, OpportunityList
)

router = APIRouter()


# Customers
@router.post('/customers', response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(payload: CustomerCreate, db: Session = Depends(get_db), current_user: User = Depends(require_permission('crm:customer:create'))):
    return CRMService(db).create_customer(payload)


@router.get('/customers', response_model=CustomerList)
async def list_customers(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), q: Optional[str] = Query(None), db: Session = Depends(get_db), current_user: User = Depends(require_permission('crm:customer:read'))):
    svc = CRMService(db)
    customers = svc.list_customers(skip=skip, limit=limit, q=q)
    total = svc.count_customers(q=q)
    return CustomerList(customers=customers, total=total, page=skip // limit + 1, size=limit)


@router.put('/customers/{customer_id}', response_model=CustomerResponse)
async def update_customer(customer_id: int, payload: CustomerUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_permission('crm:customer:update'))):
    svc = CRMService(db)
    customer = svc.update_customer(customer_id, payload)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Customer not found')
    return customer


# Leads
@router.post('/leads', response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
async def create_lead(payload: LeadCreate, db: Session = Depends(get_db), current_user: User = Depends(require_permission('crm:lead:create'))):
    return CRMService(db).create_lead(payload)


@router.get('/leads', response_model=LeadList)
async def list_leads(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), q: Optional[str] = Query(None), db: Session = Depends(get_db), current_user: User = Depends(require_permission('crm:lead:read'))):
    svc = CRMService(db)
    leads = svc.list_leads(skip=skip, limit=limit, q=q)
    total = svc.count_leads(q=q)
    return LeadList(leads=leads, total=total, page=skip // limit + 1, size=limit)


@router.put('/leads/{lead_id}', response_model=LeadResponse)
async def update_lead(lead_id: int, payload: LeadUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_permission('crm:lead:update'))):
    svc = CRMService(db)
    lead = svc.update_lead(lead_id, payload)
    if not lead:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Lead not found')
    return lead


# Opportunities
@router.post('/opportunities', response_model=OpportunityResponse, status_code=status.HTTP_201_CREATED)
async def create_opportunity(payload: OpportunityCreate, db: Session = Depends(get_db), current_user: User = Depends(require_permission('crm:opportunity:create'))):
    return CRMService(db).create_opportunity(payload)


@router.get('/opportunities', response_model=OpportunityList)
async def list_opportunities(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), q: Optional[str] = Query(None), db: Session = Depends(get_db), current_user: User = Depends(require_permission('crm:opportunity:read'))):
    svc = CRMService(db)
    opps = svc.list_opportunities(skip=skip, limit=limit, q=q)
    total = svc.count_opportunities(q=q)
    return OpportunityList(opportunities=opps, total=total, page=skip // limit + 1, size=limit)


@router.put('/opportunities/{opp_id}', response_model=OpportunityResponse)
async def update_opportunity(opp_id: int, payload: OpportunityUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_permission('crm:opportunity:update'))):
    svc = CRMService(db)
    opp = svc.update_opportunity(opp_id, payload)
    if not opp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Opportunity not found')
    return opp


