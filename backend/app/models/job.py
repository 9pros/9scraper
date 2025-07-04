import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from sqlalchemy import (
    Column,
    DateTime,
    Enum as SQLEnum,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.business import TimestampMixin


class JobStatus(str, Enum):
    """Job status enumeration."""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ScrapingJob(Base, TimestampMixin):
    """Scraping job model."""
    __tablename__ = "scraping_jobs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    keyword = Column(String(255), nullable=False, index=True)
    location = Column(String(255), nullable=False, index=True)
    radius_miles = Column(Integer, default=25)
    
    # Job configuration
    sources = Column(JSONB)  # ["google_maps", "yelp", "yellow_pages"]
    options = Column(JSONB)  # Additional options like include_emails, etc.
    
    # Job status and progress
    status = Column(SQLEnum(JobStatus), default=JobStatus.PENDING, index=True)
    progress = Column(Integer, default=0)  # 0-100
    results_count = Column(Integer, default=0)
    
    # Error tracking
    error_message = Column(Text)
    retry_count = Column(Integer, default=0)
    
    # Timing
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    job_results = relationship("JobResult", back_populates="job")
    
    def __repr__(self) -> str:
        return f"<ScrapingJob(id={self.id}, keyword='{self.keyword}', status='{self.status}')>"
