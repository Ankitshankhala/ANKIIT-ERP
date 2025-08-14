from sqlalchemy import Column, Integer, String, DateTime, JSON, Text
from sqlalchemy.sql import func

from .base import BaseModel, Base


class AuditLog(BaseModel, Base):
    __tablename__ = "audit_logs"

    # Who and where
    actor_user_id = Column(Integer, nullable=True, index=True)
    actor_role = Column(String(100), nullable=True)
    tenant_id = Column(Integer, nullable=True, index=True)
    organization_id = Column(Integer, nullable=True, index=True)

    # What
    action = Column(String(100), nullable=False, index=True)
    resource_type = Column(String(100), nullable=False, index=True)
    resource_id = Column(String(100), nullable=True)

    # Request context
    ip_address = Column(String(64), nullable=True)
    user_agent = Column(String(255), nullable=True)
    method = Column(String(16), nullable=True)
    path = Column(String(512), nullable=True)
    status_code = Column(Integer, nullable=True)

    # Payloads
    metadata = Column(JSON, nullable=True)
    before = Column(JSON, nullable=True)
    after = Column(JSON, nullable=True)
    error = Column(Text, nullable=True)

    # Timestamps (override BaseModel if needed)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


