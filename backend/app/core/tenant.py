from typing import Optional
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import contextvars
import logging

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.tenant import Tenant


# Per-request tenant schema context
tenant_schema_ctx: contextvars.ContextVar[str] = contextvars.ContextVar(
    "tenant_schema_ctx", default=settings.DEFAULT_TENANT_SCHEMA
)


def set_tenant_schema(schema_name: str) -> None:
    tenant_schema_ctx.set(schema_name)


def get_tenant_schema() -> str:
    return tenant_schema_ctx.get()


class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger = logging.getLogger(__name__)
        header_name = settings.TENANT_HEADER
        tenant_identifier: Optional[str] = request.headers.get(header_name)

        resolved_schema = settings.DEFAULT_TENANT_SCHEMA
        resolved_tenant_id: Optional[int] = None

        if tenant_identifier:
            # Resolve tenant schema using default connection
            db = SessionLocal()
            try:
                tenant: Optional[Tenant] = None
                # Try by numeric id, else by slug
                if tenant_identifier.isdigit():
                    tenant = db.query(Tenant).filter(Tenant.id == int(tenant_identifier)).first()
                if tenant is None:
                    tenant = db.query(Tenant).filter(Tenant.slug == tenant_identifier).first()
                if tenant and tenant.is_active:
                    resolved_schema = tenant.schema_name
                    resolved_tenant_id = tenant.id
            except Exception as exc:
                logger.warning(f"Tenant resolution failed for '{tenant_identifier}': {exc}")
            finally:
                db.close()

        # Set request-scoped schema for downstream DB sessions
        set_tenant_schema(resolved_schema)

        # Expose resolved values on request.state
        request.state.tenant_schema = resolved_schema
        request.state.tenant_id = resolved_tenant_id
        request.state.tenant_header = tenant_identifier

        response: Response = await call_next(request)
        return response


