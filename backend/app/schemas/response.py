from typing import Any, Dict, Generic, List, Optional, TypeVar
from uuid import UUID

from pydantic import BaseModel

from app.schemas.business import Business
from app.schemas.job import ScrapingJob

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response schema."""
    items: List[T]
    total: int
    page: int
    size: int
    pages: int


class JobResultsResponse(BaseModel):
    """Response schema for job results."""
    job: ScrapingJob
    businesses: List[Business]
    total_results: int
    page: int
    size: int
    pages: int


class ExportRequest(BaseModel):
    """Request schema for exporting data."""
    format: str = "csv"  # csv, json, excel
    fields: Optional[List[str]] = None
    filters: Optional[Dict[str, Any]] = None
    
    class Config:
        schema_extra = {
            "example": {
                "format": "csv",
                "fields": ["name", "phone", "email", "website", "address"],
                "filters": {
                    "min_rating": 4.0,
                    "has_website": True
                }
            }
        }


class ExportResponse(BaseModel):
    """Response schema for export operation."""
    download_url: str
    expires_at: str
    file_size: int
    record_count: int


class ErrorResponse(BaseModel):
    """Error response schema."""
    detail: str
    code: Optional[str] = None


class SuccessResponse(BaseModel):
    """Success response schema."""
    message: str
    data: Optional[Dict[str, Any]] = None
