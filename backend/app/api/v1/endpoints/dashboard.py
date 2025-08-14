from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import Dict, Any, List

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.audit import AuditLog
from app.models.organization import Organization

router = APIRouter()


@router.get("/stats", response_model=Dict[str, Any])
async def get_dashboard_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get dashboard statistics"""
    
    # Get basic counts
    total_users = db.query(User).count()
    total_organizations = db.query(Organization).count()
    
    # Get user's organization stats
    user_org = db.query(Organization).filter(Organization.id == current_user.organization_id).first()
    org_users = db.query(User).filter(User.organization_id == current_user.organization_id).count()
    
    # Mock data for now - in real app this would come from actual business logic
    stats = {
        "total_users": total_users,
        "total_organizations": total_organizations,
        "organization_users": org_users,
        "organization_name": user_org.name if user_org else "Unknown",
        "recent_activity": [
            {
                "id": 1,
                "action": "User logged in",
                "user": current_user.full_name,
                "time": "Just now"
            }
        ],
        "quick_actions": [
            {"name": "Add User", "icon": "user-plus", "href": "/users/new"},
            {"name": "Create Organization", "icon": "building", "href": "/organizations/new"},
            {"name": "View Reports", "icon": "bar-chart", "href": "/reports"},
            {"name": "Settings", "icon": "settings", "href": "/settings"}
        ]
    }
    
    return stats


@router.get("/recent-activity", response_model=List[Dict[str, Any]])
async def get_recent_activity(
    request: Request,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get recent activity for the dashboard from audit logs"""
    tenant_id = getattr(request.state, "tenant_id", None)
    query = db.query(AuditLog)
    if tenant_id is not None:
        query = query.filter(AuditLog.tenant_id == tenant_id)
    logs = query.order_by(AuditLog.created_at.desc()).limit(20).all()
    activities: List[Dict[str, Any]] = []
    for log in logs:
        activities.append({
            "id": log.id,
            "action": f"{log.method} {log.path}" if log.method and log.path else log.action,
            "user": str(log.actor_user_id) if log.actor_user_id else None,
            "time": str(log.created_at),
            "type": log.resource_type,
            "status": log.status_code
        })
    return activities


@router.get("/quick-stats", response_model=Dict[str, Any])
async def get_quick_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get quick statistics for dashboard cards"""
    
    # Mock quick stats - in real app this would come from actual business data
    quick_stats = {
        "users": {
            "total": 1234,
            "change": "+12%",
            "change_type": "positive"
        },
        "organizations": {
            "total": 89,
            "change": "+5%",
            "change_type": "positive"
        },
        "revenue": {
            "total": "$45,678",
            "change": "+23%",
            "change_type": "positive"
        },
        "projects": {
            "total": 34,
            "change": "-3%",
            "change_type": "negative"
        }
    }
    
    return quick_stats
