from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine
from app.api.v1.api import api_router
from app.core.logging import setup_logging, AuditMiddleware
from app.core.tenant import TenantMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    setup_logging()
    yield
    # Shutdown
    await engine.dispose()


def create_application() -> FastAPI:
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title="ANKIIT ERP API",
        description="Full Stack ERP SaaS Platform API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # Security middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Tenant and audit middlewares
    app.add_middleware(TenantMiddleware)
    app.add_middleware(AuditMiddleware)

    # Include API router
    app.include_router(api_router, prefix="/api/v1")

    @app.get("/")
    async def root():
        return {
            "message": "Welcome to ANKIIT ERP API",
            "version": "1.0.0",
            "docs": "/docs"
        }

    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "service": "ANKIIT ERP API"}

    return app


app = create_application()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
