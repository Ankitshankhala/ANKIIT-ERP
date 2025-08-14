from sqlalchemy import Column, String, Boolean, Text, JSON, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .base import BaseModel


class Tenant(BaseModel):
    """Tenant model for multi-tenant database schema management"""
    __tablename__ = "tenants"
    
    # Tenant identification
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    schema_name = Column(String(100), unique=True, nullable=False)
    
    # Organization relationship
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    organization = relationship("Organization", back_populates="tenants")
    
    # Tenant configuration
    database_url = Column(String(500), nullable=True)  # Custom database connection
    is_active = Column(Boolean, default=True, nullable=False)
    is_primary = Column(Boolean, default=False, nullable=False)
    
    # Settings and configuration
    settings = Column(JSON, default=dict, nullable=False)
    custom_fields = Column(JSON, default=dict, nullable=False)
    
    # Metadata
    description = Column(Text, nullable=True)
    tags = Column(JSON, default=list, nullable=False)
    
    def __init__(self, **kwargs):
        if "name" in kwargs and "slug" not in kwargs:
            kwargs["slug"] = self.generate_slug(kwargs["name"])
        if "slug" in kwargs and "schema_name" not in kwargs:
            kwargs["schema_name"] = f"tenant_{kwargs['slug']}"
        super().__init__(**kwargs)
    
    @staticmethod
    def generate_slug(name: str) -> str:
        """Generate slug from tenant name"""
        import re
        slug = re.sub(r'[^\w\s-]', '', name.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')
    
    def get_setting(self, key: str, default=None):
        """Get tenant setting value"""
        return self.settings.get(key, default)
    
    def set_setting(self, key: str, value):
        """Set tenant setting value"""
        if not self.settings:
            self.settings = {}
        self.settings[key] = value
    
    def get_custom_field(self, key: str, default=None):
        """Get tenant custom field value"""
        return self.custom_fields.get(key, default)
    
    def set_custom_field(self, key: str, value):
        """Set tenant custom field value"""
        if not self.custom_fields:
            self.custom_fields = {}
        self.custom_fields[key] = value
    
    def add_tag(self, tag: str):
        """Add tag to tenant"""
        if not self.tags:
            self.tags = []
        if tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str):
        """Remove tag from tenant"""
        if self.tags and tag in self.tags:
            self.tags.remove(tag)
    
    def has_tag(self, tag: str) -> bool:
        """Check if tenant has specific tag"""
        return tag in (self.tags or [])
    
    @property
    def full_schema_name(self) -> str:
        """Get full schema name for database operations"""
        return f"tenant_{self.slug}"
    
    def to_dict(self):
        """Convert tenant to dictionary"""
        data = super().to_dict()
        data["full_schema_name"] = self.full_schema_name
        data["organization_name"] = self.organization.name if self.organization else None
        return data
