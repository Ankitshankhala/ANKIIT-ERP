from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .base import BaseModel, Base


class LeadStatus(str, enum.Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    LOST = "lost"


class OpportunityStage(str, enum.Enum):
    PROSPECTING = "prospecting"
    QUALIFICATION = "qualification"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    WON = "won"
    LOST = "lost"


class CommunicationType(str, enum.Enum):
    CALL = "call"
    EMAIL = "email"
    MEETING = "meeting"
    NOTE = "note"


class Customer(BaseModel, Base):
    __tablename__ = "customers"

    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=True, index=True)
    phone = Column(String(50), nullable=True)
    address = Column(Text, nullable=True)
    website = Column(String(200), nullable=True)
    is_active = Column(Boolean, default=True)

    leads = relationship("Lead", back_populates="customer")
    opportunities = relationship("Opportunity", back_populates="customer")


class Lead(BaseModel, Base):
    __tablename__ = "leads"

    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=True, index=True)
    phone = Column(String(50), nullable=True)
    source = Column(String(100), nullable=True)
    status = Column(Enum(LeadStatus), nullable=False, default=LeadStatus.NEW)
    notes = Column(Text, nullable=True)

    customer = relationship("Customer", back_populates="leads")


class Opportunity(BaseModel, Base):
    __tablename__ = "opportunities"

    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    name = Column(String(200), nullable=False)
    value = Column(Numeric(12, 2), nullable=False, default=0)
    stage = Column(Enum(OpportunityStage), nullable=False, default=OpportunityStage.PROSPECTING)
    close_date = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)

    customer = relationship("Customer", back_populates="opportunities")


class Communication(BaseModel, Base):
    __tablename__ = "communications"

    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=True)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"), nullable=True)
    type = Column(Enum(CommunicationType), nullable=False)
    subject = Column(String(200), nullable=True)
    content = Column(Text, nullable=True)
    occurred_at = Column(DateTime, nullable=False, server_default=func.now())

    customer = relationship("Customer")
    lead = relationship("Lead")
    opportunity = relationship("Opportunity")


