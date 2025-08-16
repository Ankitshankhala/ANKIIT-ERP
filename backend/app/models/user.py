from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from passlib.hash import bcrypt

from .base import BaseModel


class User(BaseModel):
    """User model for authentication and user management"""
    __tablename__ = "users"
    
    # Basic user information
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    
    # Authentication
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    email_verified_at = Column(DateTime(timezone=True), nullable=True)
    
    # Profile
    avatar_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    timezone = Column(String(50), default="UTC", nullable=False)
    language = Column(String(10), default="en", nullable=False)
    
    # Relationships
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    
    # Relationships
    organization = relationship("Organization", back_populates="users")
    role = relationship("Role", back_populates="users")
    
    def __init__(self, **kwargs):
        if "password" in kwargs:
            kwargs["hashed_password"] = self.hash_password(kwargs.pop("password"))
        super().__init__(**kwargs)
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        return bcrypt.hash(password)
    
    def verify_password(self, password: str) -> bool:
        """Verify password against hash"""
        return bcrypt.verify(password, self.hashed_password)
    
    @property
    def full_name(self) -> str:
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_superuser(self) -> bool:
        """Check if user is superuser"""
        return self.role.name == "superuser" if self.role else False
    
    def to_dict(self):
        """Convert user to dictionary (excluding sensitive data)"""
        data = super().to_dict()
        data.pop("hashed_password", None)
        data["full_name"] = self.full_name
        data["is_superuser"] = self.is_superuser
        return data
