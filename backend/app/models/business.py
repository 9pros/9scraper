import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class TimestampMixin:
    """Mixin for created_at and updated_at timestamps."""
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )


class Business(Base, TimestampMixin):
    """Business entity model."""
    __tablename__ = "businesses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, index=True)
    address = Column(Text)
    phone = Column(String(50))
    email = Column(String(255))
    website = Column(String(500))
    rating = Column(String(10))  # e.g., "4.5"
    review_count = Column(Integer)
    
    # Flexible additional data storage
    data = Column(JSONB)
    
    # Relationships
    job_results = relationship("JobResult", back_populates="business")
    
    def __repr__(self) -> str:
        return f"<Business(id={self.id}, name='{self.name}')>"
