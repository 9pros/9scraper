from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, HttpUrl


class BusinessBase(BaseModel):
    """Base business schema."""
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[HttpUrl] = None
    rating: Optional[str] = None
    review_count: Optional[int] = None
    data: Optional[Dict[str, Any]] = None


class BusinessCreate(BusinessBase):
    """Schema for creating a business."""
    pass


class BusinessUpdate(BaseModel):
    """Schema for updating a business."""
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[HttpUrl] = None
    rating: Optional[str] = None
    review_count: Optional[int] = None
    data: Optional[Dict[str, Any]] = None


class BusinessInDB(BusinessBase):
    """Schema for business in database."""
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class Business(BusinessInDB):
    """Schema for business API response."""
    pass
