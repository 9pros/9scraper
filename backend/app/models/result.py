import uuid
from decimal import Decimal

from sqlalchemy import Column, Decimal as SQLDecimal, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.business import TimestampMixin


class JobResult(Base, TimestampMixin):
    """Association table linking jobs to businesses with metadata."""
    __tablename__ = "job_results"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey("scraping_jobs.id"), nullable=False)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id"), nullable=False)
    
    # Metadata about the result
    source = Column(String(50), nullable=False)  # google_maps, yelp, etc.
    confidence_score = Column(SQLDecimal(3, 2), default=Decimal("1.00"))
    search_term = Column(String(255))  # The exact search that found this
    search_position = Column(String(10))  # Position in search results
    
    # Relationships
    job = relationship("ScrapingJob", back_populates="job_results")
    business = relationship("Business", back_populates="job_results")
    
    def __repr__(self) -> str:
        return f"<JobResult(job_id={self.job_id}, business_id={self.business_id}, source='{self.source}')>"
