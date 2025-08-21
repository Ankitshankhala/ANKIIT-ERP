from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from typing import Generator
import logging

from app.core.config import settings
# from app.core.tenant import get_tenant_schema  # Commented to avoid circular import

# Configure logging
logger = logging.getLogger(__name__)

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
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

# Create base class for models
Base = declarative_base()

# Metadata for multi-tenancy
metadata = MetaData()


def get_db() -> Generator[Session, None, None]:
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        # Set PostgreSQL search_path for tenant-aware queries (disabled for SQLite)
        # try:
        #     tenant_schema = get_tenant_schema()
        #     if tenant_schema:
        #         # Prefer tenant schema, fallback to public
        #         db.execute(f'SET search_path TO "{tenant_schema}", public')
        # except Exception as e:
        #     logger.warning(f"Failed to set tenant search_path: {e}")
        yield db
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
        from app.models import user, organization, tenant  # noqa
        
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
            connection.execute("SELECT 1")
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
    try:
        with engine.connect() as connection:
            # Create tenant-specific schema
            connection.execute(f"CREATE SCHEMA IF NOT EXISTS tenant_{tenant_id}")
            connection.commit()
        return True
    except Exception as e:
        logger.error(f"Failed to create tenant schema {tenant_id}: {e}")
        return False
