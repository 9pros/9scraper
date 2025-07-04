from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, validator

from app.models.job import JobStatus


class JobOptionsBase(BaseModel):
    """Base options for scraping jobs."""
    include_emails: bool = True
    include_social: bool = True
    include_reviews: bool = False
    max_results: Optional[int] = None
    min_rating: Optional[float] = None


class ScrapingJobBase(BaseModel):
    """Base scraping job schema."""
    keyword: str = Field(..., min_length=1, max_length=255)
    location: str = Field(..., min_length=1, max_length=255)
    radius_miles: int = Field(default=25, ge=1, le=100)
    sources: List[str] = Field(default=["google_maps"])
    options: JobOptionsBase = Field(default_factory=JobOptionsBase)
    
    @validator("sources")
    def validate_sources(cls, v):
        valid_sources = {"google_maps", "yelp", "yellow_pages", "facebook"}
        if not all(source in valid_sources for source in v):
            raise ValueError(f"Invalid sources. Must be subset of {valid_sources}")
        return v


class ScrapingJobCreate(ScrapingJobBase):
    """Schema for creating a scraping job."""
    pass


class ScrapingJobUpdate(BaseModel):
    """Schema for updating a scraping job."""
    status: Optional[JobStatus] = None
    progress: Optional[int] = Field(None, ge=0, le=100)
    results_count: Optional[int] = Field(None, ge=0)
    error_message: Optional[str] = None


class ScrapingJobInDB(ScrapingJobBase):
    """Schema for scraping job in database."""
    id: UUID
    status: JobStatus
    progress: int
    results_count: int
    error_message: Optional[str] = None
    retry_count: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ScrapingJob(ScrapingJobInDB):
    """Schema for scraping job API response."""
    estimated_completion: Optional[datetime] = None
    
    @property
    def is_running(self) -> bool:
        return self.status in [JobStatus.PENDING, JobStatus.RUNNING]
    
    @property
    def is_completed(self) -> bool:
        return self.status in [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED]
