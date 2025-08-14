from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
    get_current_user
)
from app.models.user import User
from app.models.role import Role
from app.models.organization import Organization
from app.schemas.auth import (
    Token,
    UserLogin,
    UserRegister,
    UserResponse,
    PasswordReset,
    PasswordResetConfirm
)

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    user_credentials: UserLogin,
    db: Session = Depends(get_db)
) -> Any:
    """User login endpoint"""
    
    # Find user by email or username
    user = db.query(User).filter(
        (User.email == user_credentials.email_or_username) |
        (User.username == user_credentials.email_or_username)
    ).first()
    
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email/username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account"
        )
    
    # Create access and refresh tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
) -> Any:
    """User registration endpoint"""
    
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()
    
    if existing_user:
        if existing_user.email == user_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    # Create organization if provided
    organization = None
    if user_data.organization_name:
        organization = Organization(
            name=user_data.organization_name,
            email=user_data.email
        )
        db.add(organization)
        db.flush()  # Get the ID
    
    # Get default role (user role)
    default_role = db.query(Role).filter(Role.name == "user").first()
    if not default_role:
        # Create default roles if they don't exist
        default_role = Role(
            name="user",
            display_name="User",
            description="Default user role",
            permissions='["read:profile", "update:profile"]'
        )
        db.add(default_role)
        db.flush()
    
    # Create user
    user = User(
        username=user_data.username,
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        password=user_data.password,
        organization_id=organization.id if organization else None,
        role_id=default_role.id
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
) -> Any:
    """Refresh access token using refresh token"""
    
    # Verify refresh token
    from app.core.security import verify_token
    try:
        payload = verify_token(refresh_token)
        token_type = payload.get("type")
        if token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token type"
            )
        
        user_id = payload.get("sub")
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or inactive user"
            )
        
        # Create new access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )


@router.post("/logout")
async def logout() -> Any:
    """User logout endpoint"""
    # In a stateless JWT system, logout is handled client-side
    # by removing the token. For additional security, you could
    # implement a token blacklist using Redis.
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get current user information"""
    data = current_user.to_dict()
    # attach role name and permissions for permission-aware UI
    data["role_name"] = current_user.role.name if current_user.role else None
    try:
        perms = current_user.role.permission_list if current_user.role else []
    except Exception:
        perms = []
    data["permissions"] = perms
    return data


@router.post("/password-reset")
async def request_password_reset(
    email: str,
    db: Session = Depends(get_db)
) -> Any:
    """Request password reset"""
    user = db.query(User).filter(User.email == email).first()
    
    if user:
        # In a real application, send password reset email
        # For now, just return success message
        pass
    
    # Always return success to prevent email enumeration
    return {"message": "If the email exists, a password reset link has been sent"}


@router.post("/password-reset-confirm")
async def confirm_password_reset(
    reset_data: PasswordResetConfirm,
    db: Session = Depends(get_db)
) -> Any:
    """Confirm password reset with token"""
    # In a real application, verify the reset token
    # For now, just return success message
    return {"message": "Password reset successful"}
