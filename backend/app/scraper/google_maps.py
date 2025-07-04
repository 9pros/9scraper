import re
from typing import Any, Dict, List, Optional
from urllib.parse import quote

import structlog
from playwright.async_api import TimeoutError

from app.scraper.base import BaseScraper

logger = structlog.get_logger(__name__)


class GoogleMapsScraper(BaseScraper):
    """Google Maps scraper implementation."""
    
    BASE_URL = "https://www.google.com/maps"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    async def search_businesses(
        self, 
        keyword: str, 
        location: str, 
        radius_miles: int = 25
    ) -> List[Dict[str, Any]]:
        """Search for businesses on Google Maps."""
        try:
            # Construct search query
            query = f"{keyword} near {location}"
            search_url = f"{self.BASE_URL}/search/{quote(query)}"
            
            logger.info(f"Searching Google Maps: {query}")
            
            # Navigate to search page
            await self.page.goto(search_url, wait_until="networkidle")
            await self.random_delay(2, 4)
            
            # Wait for results to load
            await self.page.wait_for_selector('[data-value="Search results"]', timeout=10000)
            
            businesses = []
            page_num = 1
            
            while len(businesses) < 100 and page_num <= 5:  # Limit to 5 pages
                logger.info(f"Extracting page {page_num}")
                
                # Extract businesses from current page
                page_businesses = await self._extract_businesses_from_page()
                businesses.extend(page_businesses)
                
                # Try to go to next page
                if not await self._go_to_next_page():
                    break
                    
                page_num += 1
                await self.random_delay(2, 4)
            
            logger.info(f"Found {len(businesses)} businesses for '{query}'")
            return businesses
            
        except Exception as e:
            logger.error(f"Error searching Google Maps: {e}")
            return []
    
    async def _extract_businesses_from_page(self) -> List[Dict[str, Any]]:
        """Extract business data from the current page."""
        businesses = []
        
        try:
            # Wait for business listings
            await self.page.wait_for_selector('[data-result-index]', timeout=5000)
            
            # Get all business listing elements
            business_elements = await self.page.query_selector_all('[data-result-index]')
            
            for element in business_elements:
                try:
                    business_data = await self._extract_business_from_element(element)
                    if business_data:
                        businesses.append(business_data)
                        
                except Exception as e:
                    logger.warning(f"Error extracting business: {e}")
                    continue
                    
        except TimeoutError:
            logger.warning("No business listings found on page")
            
        return businesses
    async def _extract_business_from_element(self, element) -> Optional[Dict[str, Any]]:
        """Extract business information from a listing element."""
        try:
            business_data = {}
            
            # Extract name
            name_element = await element.query_selector('[data-value="Business name"]')
            if name_element:
                business_data["name"] = await name_element.text_content()
            
            # Extract rating
            rating_element = await element.query_selector('[data-value="Rating"]')
            if rating_element:
                rating_text = await rating_element.text_content()
                rating_match = re.search(r'(\d+\.?\d*)', rating_text or "")
                if rating_match:
                    business_data["rating"] = rating_match.group(1)
            
            # Extract review count
            review_element = await element.query_selector('[data-value="Reviews"]')
            if review_element:
                review_text = await review_element.text_content()
                review_match = re.search(r'(\d+)', review_text or "")
                if review_match:
                    business_data["review_count"] = int(review_match.group(1))
            
            # Extract address
            address_element = await element.query_selector('[data-value="Address"]')
            if address_element:
                business_data["address"] = await address_element.text_content()
            
            # Extract phone
            phone_element = await element.query_selector('[data-value="Phone"]')
            if phone_element:
                business_data["phone"] = await phone_element.text_content()
            
            # Extract business URL for detailed scraping
            link_element = await element.query_selector('a[href*="/maps/place/"]')
            if link_element:
                business_data["maps_url"] = await link_element.get_attribute("href")
            
            # Only return if we have at least a name
            if "name" in business_data:
                business_data["source"] = "google_maps"
                return business_data
                
        except Exception as e:
            logger.warning(f"Error extracting business element: {e}")
            
        return None
    
    async def _go_to_next_page(self) -> bool:
        """Navigate to the next page of results."""
        try:
            # Look for next button
            next_button = await self.page.query_selector('[aria-label="Next page"]')
            if next_button:
                is_disabled = await next_button.get_attribute("disabled")
                if not is_disabled:
                    await next_button.click()
                    await self.random_delay(2, 4)
                    return True
                    
        except Exception as e:
            logger.warning(f"Error navigating to next page: {e}")
            
        return False
    
    async def extract_business_details(self, business_url: str) -> Dict[str, Any]:
        """Extract detailed business information from business page."""
        try:
            logger.info(f"Extracting details from: {business_url}")
            
            # Navigate to business page
            await self.page.goto(business_url, wait_until="networkidle")
            await self.random_delay(2, 4)
            
            details = {}
            
            # Extract business name
            name_element = await self.page.query_selector('h1[data-value="Business name"]')
            if name_element:
                details["name"] = await name_element.text_content()
            
            # Extract address
            address_element = await self.page.query_selector('[data-value="Address"]')
            if address_element:
                details["address"] = await address_element.text_content()
            
            # Extract phone number
            phone_element = await self.page.query_selector('[data-value="Phone"]')
            if phone_element:
                details["phone"] = await phone_element.text_content()
            
            # Extract website
            website_element = await self.page.query_selector('[data-value="Website"]')
            if website_element:
                website_link = await website_element.query_selector('a')
                if website_link:
                    details["website"] = await website_link.get_attribute("href")
            
            # Extract hours
            hours_element = await self.page.query_selector('[data-value="Hours"]')
            if hours_element:
                details["hours"] = await hours_element.text_content()
            
            # Extract description
            description_element = await self.page.query_selector('[data-value="Description"]')
            if description_element:
                details["description"] = await description_element.text_content()
            
            # Extract additional data
            details["source"] = "google_maps"
            details["scraped_url"] = business_url
            
            return details
            
        except Exception as e:
            logger.error(f"Error extracting business details: {e}")
            return {}
