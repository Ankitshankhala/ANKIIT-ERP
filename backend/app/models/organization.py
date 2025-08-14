from sqlalchemy import Column, String, Boolean, Text, JSON, Integer, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import BaseModel


class Organization(BaseModel):
    """Organization model for multi-tenant support"""
    __tablename__ = "organizations"
    
    # Basic organization information
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    display_name = Column(String(255), nullable=True)
    
    # Contact information
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    website = Column(String(500), nullable=True)
    
    # Address
    address_line1 = Column(String(255), nullable=True)
    address_line2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    country = Column(String(100), nullable=True)
    
    # Business information
    industry = Column(String(100), nullable=True)
    company_size = Column(String(50), nullable=True)
    founded_year = Column(String(4), nullable=True)
    tax_id = Column(String(100), nullable=True)
    
    # Organization settings
    timezone = Column(String(50), default="UTC", nullable=False)
    currency = Column(String(3), default="USD", nullable=False)
    language = Column(String(10), default="en", nullable=False)
    date_format = Column(String(20), default="YYYY-MM-DD", nullable=False)
    
    # Features and modules
    enabled_modules = Column(JSON, default=list, nullable=False)
    subscription_plan = Column(String(50), default="basic", nullable=False)
    max_users = Column(Integer, default=10, nullable=False)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    trial_ends_at = Column(DateTime(timezone=True), nullable=True)
    
    # Branding
    logo_url = Column(String(500), nullable=True)
    primary_color = Column(String(7), default="#3B82F6", nullable=False)
    secondary_color = Column(String(7), default="#1F2937", nullable=False)
    
    # Relationships
    users = relationship("User", back_populates="organization", cascade="all, delete-orphan")
    tenants = relationship("Tenant", back_populates="organization", cascade="all, delete-orphan")
    
    def __init__(self, **kwargs):
        if "name" in kwargs and "slug" not in kwargs:
            kwargs["slug"] = self.generate_slug(kwargs["name"])
        super().__init__(**kwargs)
    
    @staticmethod
    def generate_slug(name: str) -> str:
        """Generate slug from organization name"""
        import re
        slug = re.sub(r'[^\w\s-]', '', name.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')
    
    @property
    def full_address(self) -> str:
        """Get full formatted address"""
        parts = [
            self.address_line1,
            self.address_line2,
            self.city,
            self.state,
            self.postal_code,
            self.country
        ]
        return ", ".join(filter(None, parts))
    
    def has_module(self, module_name: str) -> bool:
        """Check if organization has access to specific module"""
        return module_name in self.enabled_modules
    
    def can_add_user(self) -> bool:
        """Check if organization can add more users"""
        if self.max_users == -1:  # Unlimited
            return True
        return len(self.users) < self.max_users
    
    def to_dict(self):
        """Convert organization to dictionary"""
        data = super().to_dict()
        data["full_address"] = self.full_address
        data["user_count"] = len(self.users)
        data["can_add_user"] = self.can_add_user()
        return data
