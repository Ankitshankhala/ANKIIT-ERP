from sqlalchemy import Column, String, Text, Boolean, JSON
from sqlalchemy.orm import relationship

from .base import BaseModel


class Role(BaseModel):
    """Role model for role-based access control"""
    __tablename__ = "roles"
    
    # Role information
    name = Column(String(100), unique=True, index=True, nullable=False)
    display_name = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    
    # Permissions
    permissions = Column(JSON, nullable=True)
    is_system_role = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    users = relationship("User", back_populates="role")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.display_name:
            self.display_name = self.name.title()
    
    def has_permission(self, permission: str) -> bool:
        """Check if role has specific permission"""
        if not self.permissions:
            return False
        perms = self.permissions
        if isinstance(perms, str):
            try:
                import json
                perms = json.loads(perms)
            except Exception:
                perms = [p.strip() for p in perms.split(',') if p.strip()]
        if isinstance(perms, dict):
            if "permissions" in perms and isinstance(perms["permissions"], list):
                perms = perms["permissions"]
            else:
                perms = list(perms.keys())
        if not isinstance(perms, list):
            return False
        return permission in perms
    
    def add_permission(self, permission: str) -> bool:
        """Add permission to role"""
        perms = self.permissions or []
        if isinstance(perms, str):
            try:
                import json
                perms = json.loads(perms)
            except Exception:
                perms = [p.strip() for p in perms.split(',') if p.strip()]
        if isinstance(perms, dict):
            perms = perms.get("permissions", []) if isinstance(perms.get("permissions"), list) else list(perms.keys())
        if permission not in perms:
            perms.append(permission)
            self.permissions = perms
            return True
        return False
    
    def remove_permission(self, permission: str) -> bool:
        """Remove permission from role"""
        perms = self.permissions or []
        if isinstance(perms, str):
            try:
                import json
                perms = json.loads(perms)
            except Exception:
                perms = [p.strip() for p in perms.split(',') if p.strip()]
        if isinstance(perms, dict):
            perms = perms.get("permissions", []) if isinstance(perms.get("permissions"), list) else list(perms.keys())
        if permission in perms:
            perms = [p for p in perms if p != permission]
            self.permissions = perms
            return True
        return False
    
    @property
    def permission_list(self) -> list:
        """Get list of permissions"""
        perms = self.permissions or []
        if isinstance(perms, str):
            try:
                import json
                perms = json.loads(perms)
            except Exception:
                perms = [p.strip() for p in perms.split(',') if p.strip()]
        if isinstance(perms, dict):
            perms = perms.get("permissions", []) if isinstance(perms.get("permissions"), list) else list(perms.keys())
        if not isinstance(perms, list):
            return []
        return perms
    
    def to_dict(self):
        """Convert role to dictionary"""
        data = super().to_dict()
        data["permission_list"] = self.permission_list
        data["user_count"] = len(self.users)
        return data
