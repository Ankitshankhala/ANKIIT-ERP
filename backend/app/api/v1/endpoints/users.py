from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_active_user, require_permission
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[dict])
async def get_users(
    current_user: User = Depends(require_permission("read:user")),
    db: Session = Depends(get_db)
):
    """Get all users"""
    users = db.query(User).all()
    return [user.to_dict() for user in users]


@router.get("/{user_id}", response_model=dict)
async def get_user(
    user_id: int,
    current_user: User = Depends(require_permission("read:user")),
    db: Session = Depends(get_db)
):
    """Get user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user.to_dict()


@router.put("/{user_id}", response_model=dict)
async def update_user(
    user_id: int,
    user_data: dict,
    current_user: User = Depends(require_permission("update:user")),
    db: Session = Depends(get_db)
):
    """Update user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update user fields
    for field, value in user_data.items():
        if hasattr(user, field) and field not in ['id', 'created_at', 'updated_at']:
            setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user.to_dict()


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(require_permission("delete:user")),
    db: Session = Depends(get_db)
):
    """Delete user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
