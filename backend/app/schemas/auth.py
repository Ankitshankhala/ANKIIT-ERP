from pydantic import BaseModel, EmailStr, validator
from typing import Optional


class Token(BaseModel):
    """Token response schema"""
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int


class UserLogin(BaseModel):
    """User login request schema"""
    email_or_username: str
    password: str
    
    @validator('email_or_username')
    def validate_email_or_username(cls, v):
        if not v.strip():
            raise ValueError('Email or username cannot be empty')
        return v.strip()
    
    @validator('password')
    def validate_password(cls, v):
        if not v:
            raise ValueError('Password cannot be empty')
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters')
        return v


class UserRegister(BaseModel):
    """User registration request schema"""
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    organization_name: Optional[str] = None
    phone: Optional[str] = None
    
    @validator('username')
    def validate_username(cls, v):
        if not v.strip():
            raise ValueError('Username cannot be empty')
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters')
        if len(v) > 50:
            raise ValueError('Username must be less than 50 characters')
        # Check for valid characters
        import re
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Username can only contain letters, numbers, underscores, and hyphens')
        return v.strip()
    
    @validator('first_name', 'last_name')
    def validate_names(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        if len(v) > 100:
            raise ValueError('Name must be less than 100 characters')
        return v.strip()
    
    @validator('password')
    def validate_password(cls, v):
        if not v:
            raise ValueError('Password cannot be empty')
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if len(v) > 128:
            raise ValueError('Password must be less than 128 characters')
        # Check for password strength
        import re
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        return v
    
    @validator('phone')
    def validate_phone(cls, v):
        if v:
            import re
            # Remove all non-digit characters
            digits_only = re.sub(r'\D', '', v)
            if len(digits_only) < 10:
                raise ValueError('Phone number must have at least 10 digits')
        return v


class UserResponse(BaseModel):
    """User response schema"""
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    phone: Optional[str]
    is_active: bool
    is_verified: bool
    avatar_url: Optional[str]
    bio: Optional[str]
    timezone: str
    language: str
    organization_id: int
    role_id: int
    role_name: Optional[str]
    permissions: Optional[list[str]]
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True


class PasswordReset(BaseModel):
    """Password reset request schema"""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation schema"""
    token: str
    new_password: str
    
    @validator('new_password')
    def validate_new_password(cls, v):
        if not v:
            raise ValueError('Password cannot be empty')
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if len(v) > 128:
            raise ValueError('Password must be less than 128 characters')
        # Check for password strength
        import re
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        return v
