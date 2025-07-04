import re
from typing import Any, Dict, Optional

import phonenumbers
import structlog
from email_validator import EmailNotValidError, validate_email

logger = structlog.get_logger(__name__)


class DataProcessor:
    """Process and clean scraped business data."""
    
    def __init__(self):
        self.phone_region = "US"  # Default region for phone parsing
    
    async def process_business_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process raw business data into clean format."""
        processed = {}
        
        # Clean name
        if name := raw_data.get("name"):
            processed["name"] = self._clean_text(name)
        
        # Clean address
        if address := raw_data.get("address"):
            processed["address"] = self._clean_address(address)
        
        # Clean phone
        if phone := raw_data.get("phone"):
            processed["phone"] = self._clean_phone(phone)
        
        # Clean email
        if email := raw_data.get("email"):
            processed["email"] = self._clean_email(email)
        
        # Clean website
        if website := raw_data.get("website"):
            processed["website"] = self._clean_url(website)
        
        # Clean rating
        if rating := raw_data.get("rating"):
            processed["rating"] = self._clean_rating(rating)
        
        # Clean review count
        if review_count := raw_data.get("review_count"):
            processed["review_count"] = self._clean_number(review_count)
        
        # Store additional data
        additional_data = {
            k: v for k, v in raw_data.items()
            if k not in ["name", "address", "phone", "email", "website", "rating", "review_count"]
        }
        if additional_data:
            processed["data"] = additional_data
        
        return processed
    
    def _clean_text(self, text: str) -> str:
        """Clean general text fields."""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove common prefixes/suffixes
        text = re.sub(r'^(Business Name|Name):\s*', '', text, flags=re.IGNORECASE)
        
        return text
    
    def _clean_address(self, address: str) -> str:
        """Clean address field."""
        if not address:
            return ""
        
        # Basic address cleaning
        address = self._clean_text(address)
        
        # Remove common prefixes
        address = re.sub(r'^(Address|Located at):\s*', '', address, flags=re.IGNORECASE)
        
        return address
    
    def _clean_phone(self, phone: str) -> Optional[str]:
        """Clean and validate phone number."""
        if not phone:
            return None
        
        try:
            # Parse phone number
            parsed = phonenumbers.parse(phone, self.phone_region)
            
            # Validate
            if phonenumbers.is_valid_number(parsed):
                # Format as E164
                return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
                
        except phonenumbers.NumberParseException:
            # Try cleaning and parsing again
            cleaned = re.sub(r'[^\d+]', '', phone)
            if cleaned:
                try:
                    parsed = phonenumbers.parse(cleaned, self.phone_region)
                    if phonenumbers.is_valid_number(parsed):
                        return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
                except phonenumbers.NumberParseException:
                    pass
        
        logger.warning(f"Could not parse phone number: {phone}")
        return None
    
    def _clean_email(self, email: str) -> Optional[str]:
        """Clean and validate email address."""
        if not email:
            return None
        
        try:
            # Basic email validation
            validated = validate_email(email.strip().lower())
            return validated.email
            
        except EmailNotValidError:
            logger.warning(f"Invalid email address: {email}")
            return None
    
    def _clean_url(self, url: str) -> Optional[str]:
        """Clean and validate URL."""
        if not url:
            return None
        
        url = url.strip()
        
        # Add protocol if missing
        if not re.match(r'^https?://', url):
            url = f"https://{url}"
        
        # Basic URL validation
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        if url_pattern.match(url):
            return url
        
        logger.warning(f"Invalid URL: {url}")
        return None
    
    def _clean_rating(self, rating: Any) -> Optional[str]:
        """Clean rating field."""
        if not rating:
            return None
        
        # Convert to string and extract number
        rating_str = str(rating)
        rating_match = re.search(r'(\d+\.?\d*)', rating_str)
        
        if rating_match:
            rating_value = float(rating_match.group(1))
            # Validate rating range (assuming 0-5 scale)
            if 0 <= rating_value <= 5:
                return f"{rating_value:.1f}"
        
        return None
    
    def _clean_number(self, number: Any) -> Optional[int]:
        """Clean numeric fields."""
        if not number:
            return None
        
        # Extract numbers from string
        if isinstance(number, str):
            number_match = re.search(r'(\d+)', number.replace(',', ''))
            if number_match:
                return int(number_match.group(1))
        
        try:
            return int(number)
        except (ValueError, TypeError):
            return None
