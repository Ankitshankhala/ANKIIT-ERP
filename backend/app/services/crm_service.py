from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ..models.crm import Customer, Lead, Opportunity, OpportunityStage, Communication
from ..schemas.crm import (
    CustomerCreate, CustomerUpdate,
    LeadCreate, LeadUpdate,
    OpportunityCreate, OpportunityUpdate,
    CommunicationCreate
)
from ..core.exceptions import ValidationError


class CRMService:
    def __init__(self, db: Session):
        self.db = db

    # Customers
    def create_customer(self, data: CustomerCreate) -> Customer:
        customer = Customer(**data.dict())
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def update_customer(self, customer_id: int, data: CustomerUpdate) -> Optional[Customer]:
        customer = self.db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            return None
        for field, value in data.dict(exclude_unset=True).items():
            setattr(customer, field, value)
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def list_customers(self, skip: int = 0, limit: int = 10, q: Optional[str] = None) -> List[Customer]:
        query = self.db.query(Customer)
        if q:
            like = f"%{q}%"
            query = query.filter((Customer.name.ilike(like)) | (Customer.email.ilike(like)))
        return query.order_by(desc(Customer.created_at)).offset(skip).limit(limit).all()

    def count_customers(self, q: Optional[str] = None) -> int:
        query = self.db.query(Customer)
        if q:
            like = f"%{q}%"
            query = query.filter((Customer.name.ilike(like)) | (Customer.email.ilike(like)))
        return query.count()

    def delete_customer(self, customer_id: int) -> bool:
        customer = self.db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            return False
        self.db.delete(customer)
        self.db.commit()
        return True

    # Leads
    def create_lead(self, data: LeadCreate) -> Lead:
        lead = Lead(**data.dict())
        self.db.add(lead)
        self.db.commit()
        self.db.refresh(lead)
        return lead

    def update_lead(self, lead_id: int, data: LeadUpdate) -> Optional[Lead]:
        lead = self.db.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            return None
        for field, value in data.dict(exclude_unset=True).items():
            setattr(lead, field, value)
        self.db.commit()
        self.db.refresh(lead)
        return lead

    def list_leads(self, skip: int = 0, limit: int = 10, q: Optional[str] = None) -> List[Lead]:
        query = self.db.query(Lead)
        if q:
            like = f"%{q}%"
            query = query.filter((Lead.name.ilike(like)) | (Lead.email.ilike(like)) | (Lead.phone.ilike(like)))
        return query.order_by(desc(Lead.created_at)).offset(skip).limit(limit).all()

    def count_leads(self, q: Optional[str] = None) -> int:
        query = self.db.query(Lead)
        if q:
            like = f"%{q}%"
            query = query.filter((Lead.name.ilike(like)) | (Lead.email.ilike(like)) | (Lead.phone.ilike(like)))
        return query.count()

    def delete_lead(self, lead_id: int) -> bool:
        lead = self.db.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            return False
        self.db.delete(lead)
        self.db.commit()
        return True

    # Opportunities
    def create_opportunity(self, data: OpportunityCreate) -> Opportunity:
        opp = Opportunity(**data.dict())
        self.db.add(opp)
        self.db.commit()
        self.db.refresh(opp)
        return opp

    def update_opportunity(self, opp_id: int, data: OpportunityUpdate) -> Optional[Opportunity]:
        opp = self.db.query(Opportunity).filter(Opportunity.id == opp_id).first()
        if not opp:
            return None
        for field, value in data.dict(exclude_unset=True).items():
            setattr(opp, field, value)
        self.db.commit()
        self.db.refresh(opp)
        return opp

    def list_opportunities(self, skip: int = 0, limit: int = 10, q: Optional[str] = None) -> List[Opportunity]:
        query = self.db.query(Opportunity)
        if q:
            like = f"%{q}%"
            query = query.filter(Opportunity.name.ilike(like))
        return query.order_by(desc(Opportunity.created_at)).offset(skip).limit(limit).all()

    def count_opportunities(self, q: Optional[str] = None) -> int:
        query = self.db.query(Opportunity)
        if q:
            like = f"%{q}%"
            query = query.filter(Opportunity.name.ilike(like))
        return query.count()

    def delete_opportunity(self, opp_id: int) -> bool:
        opp = self.db.query(Opportunity).filter(Opportunity.id == opp_id).first()
        if not opp:
            return False
        self.db.delete(opp)
        self.db.commit()
        return True

    def advance_opportunity(self, opp_id: int) -> Optional[Opportunity]:
        opp = self.db.query(Opportunity).filter(Opportunity.id == opp_id).first()
        if not opp:
            return None
        stages = list(OpportunityStage)
        try:
            idx = stages.index(opp.stage)
            if idx < len(stages) - 1:
                opp.stage = stages[idx + 1]
                self.db.commit()
                self.db.refresh(opp)
        except ValueError:
            pass
        return opp

    def get_opportunity_pipeline(self) -> Dict[str, List[Opportunity]]:
        pipeline = {stage.value: [] for stage in OpportunityStage}
        for opp in self.db.query(Opportunity).all():
            pipeline[opp.stage.value].append(opp)
        return pipeline

    # Communications
    def create_communication(self, data: CommunicationCreate) -> Communication:
        comm = Communication(**data.dict())
        self.db.add(comm)
        self.db.commit()
        self.db.refresh(comm)
        return comm

    def list_communications(
        self,
        skip: int = 0,
        limit: int = 10,
        customer_id: Optional[int] = None,
        lead_id: Optional[int] = None,
        opportunity_id: Optional[int] = None,
    ) -> List[Communication]:
        query = self.db.query(Communication)
        if customer_id:
            query = query.filter(Communication.customer_id == customer_id)
        if lead_id:
            query = query.filter(Communication.lead_id == lead_id)
        if opportunity_id:
            query = query.filter(Communication.opportunity_id == opportunity_id)
        return query.order_by(desc(Communication.occurred_at)).offset(skip).limit(limit).all()

    def count_communications(
        self,
        customer_id: Optional[int] = None,
        lead_id: Optional[int] = None,
        opportunity_id: Optional[int] = None,
    ) -> int:
        query = self.db.query(Communication)
        if customer_id:
            query = query.filter(Communication.customer_id == customer_id)
        if lead_id:
            query = query.filter(Communication.lead_id == lead_id)
        if opportunity_id:
            query = query.filter(Communication.opportunity_id == opportunity_id)
        return query.count()
