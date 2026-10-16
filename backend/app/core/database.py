from fastapi import HTTPException
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import logging

from app.core.config import settings
from app.core.tenant_context import get_tenant_schema
# All models inherit from this Base; re-exported here for convenience
from app.models.base import Base  # noqa: F401

# Configure logging
logger = logging.getLogger(__name__)

IS_SQLITE = settings.DATABASE_URL.startswith("sqlite")

# Create database engine
if IS_SQLITE:
    # Local development / tests. SQLite has no schemas, so tenant search_path is skipped.
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=settings.DEBUG,
    )
else:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_size=settings.DATABASE_POOL_SIZE,
        max_overflow=settings.DATABASE_MAX_OVERFLOW,
        pool_pre_ping=True,
        echo=settings.DEBUG,
    )

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Metadata for multi-tenancy
metadata = MetaData()


def _quote_identifier(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def get_db() -> Generator[Session, None, None]:
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        # Set PostgreSQL search_path for tenant-aware queries
        if not IS_SQLITE:
            try:
                tenant_schema = get_tenant_schema()
                if tenant_schema:
                    # Prefer tenant schema, fallback to public
                    db.execute(text(f"SET search_path TO {_quote_identifier(tenant_schema)}, public"))
            except Exception as e:
                logger.warning(f"Failed to set tenant search_path: {e}")
                db.rollback()
        yield db
    except HTTPException:
        # Normal API errors (401/403/404...) raised by the endpoint, not DB failures
        db.rollback()
        raise
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def init_db() -> None:
    """Initialize database tables"""
    try:
        # Import all models here to ensure they are registered
        import app.models  # noqa: F401

        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        raise


def check_db_connection() -> bool:
    """Check if database connection is working"""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return False


# Multi-tenant database utilities
def get_tenant_db(tenant_id: str) -> Session:
    """Get database session for specific tenant"""
    # This will be implemented with tenant-specific database connections
    # For now, return the default session
    return SessionLocal()


def create_tenant_schema(tenant_id: str) -> bool:
    """Create schema for new tenant"""
    if IS_SQLITE:
        return True
    try:
        with engine.connect() as connection:
            # Create tenant-specific schema
            connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {_quote_identifier(f'tenant_{tenant_id}')}"))
            connection.commit()
        return True
    except Exception as e:
        logger.error(f"Failed to create tenant schema {tenant_id}: {e}")
        return False
