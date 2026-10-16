from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_active_user, require_permission
from app.models.organization import Organization
from app.models.user import User

router = APIRouter()


def _visible_organizations(db: Session, current_user: User):
    """Superusers manage every organization; everyone else only sees their own."""
    query = db.query(Organization)
    if not current_user.is_superuser:
        query = query.filter(Organization.id == current_user.organization_id)
    return query


@router.get("/", response_model=List[dict])
async def get_organizations(
    current_user: User = Depends(require_permission("read:organization")),
    db: Session = Depends(get_db)
):
    """Get all organizations"""
    organizations = _visible_organizations(db, current_user).all()
    return [org.to_dict() for org in organizations]


@router.get("/{org_id}", response_model=dict)
async def get_organization(
    org_id: int,
    current_user: User = Depends(require_permission("read:organization")),
    db: Session = Depends(get_db)
):
    """Get organization by ID"""
    org = _visible_organizations(db, current_user).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    return org.to_dict()


@router.post("/", response_model=dict)
async def create_organization(
    org_data: dict,
    current_user: User = Depends(require_permission("create:organization")),
    db: Session = Depends(get_db)
):
    """Create new organization"""
    org = Organization(**org_data)
    db.add(org)
    db.commit()
    db.refresh(org)
    return org.to_dict()


@router.put("/{org_id}", response_model=dict)
async def update_organization(
    org_id: int,
    org_data: dict,
    current_user: User = Depends(require_permission("update:organization")),
    db: Session = Depends(get_db)
):
    """Update organization"""
    org = _visible_organizations(db, current_user).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    # Update organization fields
    for field, value in org_data.items():
        if hasattr(org, field) and field not in ['id', 'created_at', 'updated_at']:
            setattr(org, field, value)
    
    db.commit()
    db.refresh(org)
    return org.to_dict()


@router.delete("/{org_id}")
async def delete_organization(
    org_id: int,
    current_user: User = Depends(require_permission("delete:organization")),
    db: Session = Depends(get_db)
):
    """Delete organization"""
    org = _visible_organizations(db, current_user).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    db.delete(org)
    db.commit()
    return {"message": "Organization deleted successfully"}
