from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import require_permission
from app.models.role import Role
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[dict])
async def get_roles(
    current_user: User = Depends(require_permission("read:role")),
    db: Session = Depends(get_db),
):
    """Get all roles"""
    roles = db.query(Role).all()
    return [role.to_dict() for role in roles]


@router.post("/", response_model=dict)
async def create_role(
    role_data: dict,
    current_user: User = Depends(require_permission("create:role")),
    db: Session = Depends(get_db),
):
    """Create new role"""
    role = Role(**role_data)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role.to_dict()


@router.put("/{role_id}", response_model=dict)
async def update_role(
    role_id: int,
    role_data: dict,
    current_user: User = Depends(require_permission("update:role")),
    db: Session = Depends(get_db),
):
    """Update role"""
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )
    for field, value in role_data.items():
        if hasattr(role, field) and field not in ["id", "created_at", "updated_at"]:
            setattr(role, field, value)
    db.commit()
    db.refresh(role)
    return role.to_dict()


@router.delete("/{role_id}")
async def delete_role(
    role_id: int,
    current_user: User = Depends(require_permission("delete:role")),
    db: Session = Depends(get_db),
):
    """Delete role"""
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )
    db.delete(role)
    db.commit()
    return {"message": "Role deleted successfully"}
