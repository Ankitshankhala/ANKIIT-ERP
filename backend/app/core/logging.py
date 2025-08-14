import logging
import sys
from typing import Any
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import time

from app.core.database import SessionLocal
from app.models.audit import AuditLog

def setup_logging() -> None:
    """Setup logging configuration for the application"""
    
    # Create logger
    logger = logging.getLogger("ankiit_erp")
    logger.setLevel(logging.INFO)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    # Set specific loggers
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    
    logger.info("Logging configured successfully")


class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = None
        error_text = None
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            error_text = str(exc)
            raise
        finally:
            duration_ms = int((time.time() - start_time) * 1000)
            try:
                db = SessionLocal()
                try:
                    actor_user_id = getattr(getattr(request, 'state', None), 'user_id', None)
                    tenant_id = getattr(getattr(request, 'state', None), 'tenant_id', None)
                    organization_id = getattr(getattr(request, 'state', None), 'organization_id', None)
                    status_code = getattr(response, 'status_code', None)

                    log = AuditLog(
                        actor_user_id=actor_user_id,
                        actor_role=None,
                        tenant_id=tenant_id,
                        organization_id=organization_id,
                        action=f"{request.method}",
                        resource_type="HTTP",
                        resource_id=None,
                        ip_address=request.client.host if request.client else None,
                        user_agent=request.headers.get('user-agent'),
                        method=request.method,
                        path=str(request.url.path),
                        status_code=status_code,
                        metadata={
                            "duration_ms": duration_ms,
                            "query": request.url.query
                        },
                        error=error_text
                    )
                    db.add(log)
                    db.commit()
                finally:
                    db.close()
            except Exception:
                # Never block request path on audit log failure
                pass
