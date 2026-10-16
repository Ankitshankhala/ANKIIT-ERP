import contextvars

from app.core.config import settings


# Per-request tenant schema context. Kept separate from app.core.tenant so that
# app.core.database can read it without importing the middleware (which needs
# a database session itself).
tenant_schema_ctx: contextvars.ContextVar[str] = contextvars.ContextVar(
    "tenant_schema_ctx", default=settings.DEFAULT_TENANT_SCHEMA
)


def set_tenant_schema(schema_name: str) -> None:
    tenant_schema_ctx.set(schema_name)


def get_tenant_schema() -> str:
    return tenant_schema_ctx.get()
