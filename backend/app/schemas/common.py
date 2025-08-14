from pydantic import BaseModel
from typing import Generic, TypeVar, List, Optional

T = TypeVar('T')


class PaginationParams(BaseModel):
    page: int = 1
    size: int = 20
    sort_by: Optional[str] = None
    sort_order: str = "asc"  # asc or desc


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int
    has_next: bool
    has_prev: bool


class SuccessResponse(BaseModel):
    message: str
    data: Optional[dict] = None


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None


class HealthCheck(BaseModel):
    status: str
    service: str
    version: str
    timestamp: str
