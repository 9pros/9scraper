from typing import Any, Dict, Optional

import structlog
from Levenshtein import ratio
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Business

logger = structlog.get_logger(__name__)


class DeduplicationEngine:
    """Engine for detecting and handling duplicate businesses."""
    
    def __init__(self):
        self.name_threshold = 0.8  # Similarity threshold for names
        self.address_threshold = 0.7  # Similarity threshold for addresses
        self.phone_match_weight = 0.9  # Weight for exact phone matches
        
    async def find_duplicate(
        self, 
        db: AsyncSession, 
        business_data: Dict[str, Any]
    ) -> Optional[Business]:
        """Find existing duplicate business in database."""
        
        # First check for exact phone match (highest confidence)
        if phone := business_data.get("phone"):
            existing = await self._find_by_phone(db, phone)
            if existing:
                logger.info(f"Found duplicate by phone: {phone}")
                return existing
        
        # Check for name + address similarity
        if (name := business_data.get("name")) and (address := business_data.get("address")):
            existing = await self._find_by_name_address_similarity(db, name, address)
            if existing:
                logger.info(f"Found duplicate by name/address similarity: {name}")
                return existing
        
        return None
    
    async def _find_by_phone(self, db: AsyncSession, phone: str) -> Optional[Business]:
        """Find business by exact phone match."""
        stmt = select(Business).where(Business.phone == phone)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def _find_by_name_address_similarity(
        self, 
        db: AsyncSession, 
        name: str, 
        address: str
    ) -> Optional[Business]:
        """Find business by name and address similarity."""
        
        # Get businesses with similar names (using basic text search)
        # This is a simplified approach - in production you might use
        # PostgreSQL's full-text search or fuzzy matching extensions
        
        # Extract key words from name for basic filtering
        name_words = name.lower().split()
        search_terms = [word for word in name_words if len(word) > 3]
        
        if not search_terms:
            return None
        
        # Build query to find potential matches
        conditions = []
        for term in search_terms[:3]:  # Limit to first 3 significant words
            conditions.append(Business.name.ilike(f"%{term}%"))
        
        if not conditions:
            return None
        
        stmt = select(Business).where(or_(*conditions))
        result = await db.execute(stmt)
        candidates = result.scalars().all()
        
        # Check similarity for each candidate
        for candidate in candidates:
            if await self._is_duplicate(candidate, name, address):
                return candidate
        
        return None
    
    async def _is_duplicate(
        self, 
        existing: Business, 
        name: str, 
        address: str
    ) -> bool:
        """Check if existing business is a duplicate based on similarity."""
        
        # Calculate name similarity
        name_similarity = ratio(
            existing.name.lower() if existing.name else "", 
            name.lower()
        )
        
        # Calculate address similarity
        address_similarity = 0.0
        if existing.address and address:
            address_similarity = ratio(
                existing.address.lower(), 
                address.lower()
            )
        
        # Determine if it's a duplicate
        if name_similarity >= self.name_threshold:
            if address_similarity >= self.address_threshold:
                logger.info(
                    f"Duplicate found - Name: {name_similarity:.2f}, "
                    f"Address: {address_similarity:.2f}"
                )
                return True
            elif name_similarity >= 0.95:  # Very high name similarity
                logger.info(f"Duplicate found - Very high name similarity: {name_similarity:.2f}")
                return True
        
        return False
    
    def calculate_confidence_score(
        self, 
        existing: Business, 
        new_data: Dict[str, Any]
    ) -> float:
        """Calculate confidence score for a match."""
        
        score = 0.0
        factors = 0
        
        # Name similarity
        if existing.name and new_data.get("name"):
            name_sim = ratio(existing.name.lower(), new_data["name"].lower())
            score += name_sim * 0.4
            factors += 0.4
        
        # Address similarity  
        if existing.address and new_data.get("address"):
            addr_sim = ratio(existing.address.lower(), new_data["address"].lower())
            score += addr_sim * 0.3
            factors += 0.3
        
        # Phone match
        if existing.phone and new_data.get("phone"):
            if existing.phone == new_data["phone"]:
                score += self.phone_match_weight
                factors += 0.3
        
        # Normalize score
        if factors > 0:
            return score / factors
        
        return 0.0
    
    async def merge_business_data(
        self, 
        existing: Business, 
        new_data: Dict[str, Any]
    ) -> Business:
        """Merge new data into existing business record."""
        
        # Update empty fields with new data
        if not existing.phone and new_data.get("phone"):
            existing.phone = new_data["phone"]
        
        if not existing.email and new_data.get("email"):
            existing.email = new_data["email"]
        
        if not existing.website and new_data.get("website"):
            existing.website = new_data["website"]
        
        # Merge additional data
        if new_data.get("data") and existing.data:
            # Merge JSONB data
            existing.data = {**existing.data, **new_data["data"]}
        elif new_data.get("data") and not existing.data:
            existing.data = new_data["data"]
        
        return existing
