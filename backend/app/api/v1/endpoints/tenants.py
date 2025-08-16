from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import require_permission
from app.models.tenant import Tenant
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[dict])
async def get_tenants(
    current_user: User = Depends(require_permission("read:tenant")),
    db: Session = Depends(get_db),
):
    """Get all tenants"""
    tenants = db.query(Tenant).all()
    return [tenant.to_dict() for tenant in tenants]


@router.post("/", response_model=dict)
async def create_tenant(
    tenant_data: dict,
    current_user: User = Depends(require_permission("create:tenant")),
    db: Session = Depends(get_db),
):
    """Create new tenant"""
    tenant = Tenant(**tenant_data)
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant.to_dict()


@router.put("/{tenant_id}", response_model=dict)
async def update_tenant(
    tenant_id: int,
    tenant_data: dict,
    current_user: User = Depends(require_permission("update:tenant")),
    db: Session = Depends(get_db),
):
    """Update tenant"""
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )
    for field, value in tenant_data.items():
        if hasattr(tenant, field) and field not in ["id", "created_at", "updated_at"]:
            setattr(tenant, field, value)
    db.commit()
    db.refresh(tenant)
    return tenant.to_dict()


@router.delete("/{tenant_id}")
async def delete_tenant(
    tenant_id: int,
    current_user: User = Depends(require_permission("delete:tenant")),
    db: Session = Depends(get_db),
):
    """Delete tenant"""
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )
    db.delete(tenant)
    db.commit()
    return {"message": "Tenant deleted successfully"}
