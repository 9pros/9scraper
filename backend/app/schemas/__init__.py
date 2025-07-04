"""Pydantic schemas for API validation and serialization."""

from .business import Business, BusinessCreate, BusinessInDB, BusinessUpdate
from .job import JobOptionsBase, ScrapingJob, ScrapingJobCreate, ScrapingJobInDB, ScrapingJobUpdate
from .response import (
    ErrorResponse,
    ExportRequest,
    ExportResponse,
    JobResultsResponse,
    PaginatedResponse,
    SuccessResponse,
)

__all__ = [
    "Business",
    "BusinessCreate", 
    "BusinessInDB",
    "BusinessUpdate",
    "ErrorResponse",
    "ExportRequest",
    "ExportResponse",
    "JobOptionsBase",
    "JobResultsResponse",
    "PaginatedResponse",
    "ScrapingJob",
    "ScrapingJobCreate",
    "ScrapingJobInDB", 
    "ScrapingJobUpdate",
    "SuccessResponse",
]
