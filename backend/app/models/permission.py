from sqlalchemy import Column, String, Text, Boolean
from sqlalchemy.orm import relationship

from .base import BaseModel


class Permission(BaseModel):
    """Permission model for granular access control"""
    __tablename__ = "permissions"
    
    # Permission identification
    name = Column(String(100), unique=True, index=True, nullable=False)
    display_name = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    
    # Permission structure
    resource = Column(String(100), nullable=False)  # e.g., "user", "organization", "invoice"
    action = Column(String(50), nullable=False)     # e.g., "create", "read", "update", "delete"
    
    # Permission scope
    is_global = Column(Boolean, default=False, nullable=False)  # Applies to all resources
    is_system = Column(Boolean, default=False, nullable=False)  # System permission
    
    # Metadata
    module = Column(String(100), nullable=True)  # Which ERP module this belongs to
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.display_name:
            self.display_name = f"{self.action.title()} {self.resource.title()}"
    
    @property
    def full_name(self) -> str:
        """Get full permission name (action:resource)"""
        return f"{self.action}:{self.resource}"
    
    @property
    def is_crud_permission(self) -> bool:
        """Check if this is a CRUD permission"""
        return self.action in ["create", "read", "update", "delete"]
    
    @property
    def is_list_permission(self) -> bool:
        """Check if this is a list permission"""
        return self.action in ["list", "search", "export"]
    
    def matches(self, action: str, resource: str) -> bool:
        """Check if permission matches action and resource"""
        if self.is_global:
            return True
        
        return self.action == action and self.resource == resource
    
    def to_dict(self):
        """Convert permission to dictionary"""
        data = super().to_dict()
        data["full_name"] = self.full_name
        data["is_crud_permission"] = self.is_crud_permission
        data["is_list_permission"] = self.is_list_permission
        return data
    
    @classmethod
    def get_crud_permissions(cls, resource: str) -> list:
        """Get all CRUD permissions for a resource"""
        return [
            f"create:{resource}",
            f"read:{resource}",
            f"update:{resource}",
            f"delete:{resource}"
        ]
    
    @classmethod
    def get_list_permissions(cls, resource: str) -> list:
        """Get all list permissions for a resource"""
        return [
            f"list:{resource}",
            f"search:{resource}",
            f"export:{resource}"
        ]
    
    @classmethod
    def get_all_permissions(cls, resource: str) -> list:
        """Get all permissions for a resource"""
        return cls.get_crud_permissions(resource) + cls.get_list_permissions(resource)
