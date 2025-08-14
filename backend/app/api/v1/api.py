from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, organizations, dashboard, finance
from app.api.v1.endpoints import inventory, crm, hr

# Create main API router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(organizations.router, prefix="/organizations", tags=["Organizations"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

# ERP module routers
api_router.include_router(finance.router, prefix="/finance", tags=["Finance"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
api_router.include_router(crm.router, prefix="/crm", tags=["CRM"])
api_router.include_router(hr.router, prefix="/hr", tags=["HR"])

# Future ERP module routers will be added here:
# api_router.include_router(hr.router, prefix="/hr", tags=["HR"])
# api_router.include_router(crm.router, prefix="/crm", tags=["CRM"])
# api_router.include_router(projects.router, prefix="/projects", tags=["Projects"])
