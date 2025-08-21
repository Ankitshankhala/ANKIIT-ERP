from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import validator
import os


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "ANKIIT ERP"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database
    DATABASE_URL: str = "sqlite:///./dev.db"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 30
    
    # Redis (optional for development)
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_POOL_SIZE: int = 10
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000"
    ]
    
    # Hosts
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Email (for future use)
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    # File Storage
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # Multi-tenancy
    DEFAULT_TENANT_SCHEMA: str = "public"
    TENANT_HEADER: str = "X-Tenant-ID"

    # Default GL account codes (can be overridden per environment)
    ACCOUNTS_CASH_CODE: str = "1000_CASH"
    ACCOUNTS_AR_CODE: str = "1100_AR"
    ACCOUNTS_INVENTORY_CODE: str = "1400_INVENTORY"
    ACCOUNTS_AP_CODE: str = "2100_AP"
    ACCOUNTS_REVENUE_CODE: str = "4000_REVENUE"
    ACCOUNTS_EXPENSE_CODE: str = "5000_EXPENSE"
    ACCOUNTS_COGS_CODE: str = "5100_COGS"
    
    @validator("ALLOWED_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    @validator("ALLOWED_HOSTS", pre=True)
    def assemble_allowed_hosts(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()

# Environment-specific overrides
if settings.ENVIRONMENT == "production":
    settings.DEBUG = False
    settings.ALLOWED_HOSTS = ["*.ankiit-erp.com", "ankiit-erp.com"]
elif settings.ENVIRONMENT == "staging":
    settings.DEBUG = True
    settings.ALLOWED_HOSTS = ["*.staging.ankiit-erp.com"]
