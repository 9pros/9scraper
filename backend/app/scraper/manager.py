from typing import Dict, List, Type

import structlog

from app.scraper.base import BaseScraper
from app.scraper.google_maps import GoogleMapsScraper

logger = structlog.get_logger(__name__)


class ScraperManager:
    """Manages multiple scraper instances."""
    
    def __init__(self):
        self.scrapers: Dict[str, Type[BaseScraper]] = {
            "google_maps": GoogleMapsScraper,
            # Add more scrapers here as they're implemented
            # "yelp": YelpScraper,
            # "yellow_pages": YellowPagesScraper,
        }
    
    def get_available_sources(self) -> List[str]:
        """Get list of available scraper sources."""
        return list(self.scrapers.keys())
    
    def create_scraper(self, source: str, **kwargs) -> BaseScraper:
        """Create a scraper instance for the given source."""
        if source not in self.scrapers:
            raise ValueError(f"Unknown scraper source: {source}")
        
        scraper_class = self.scrapers[source]
        return scraper_class(**kwargs)
    
    async def scrape_multiple_sources(
        self,
        sources: List[str],
        keyword: str,
        location: str,
        radius_miles: int = 25,
        **kwargs
    ) -> Dict[str, List[Dict]]:
        """Scrape from multiple sources concurrently."""
        results = {}
        
        for source in sources:
            try:
                logger.info(f"Starting scraping from {source}")
                
                async with self.create_scraper(source, **kwargs) as scraper:
                    businesses = await scraper.search_businesses(
                        keyword, location, radius_miles
                    )
                    results[source] = businesses
                    
                logger.info(f"Completed scraping from {source}: {len(businesses)} businesses")
                
            except Exception as e:
                logger.error(f"Error scraping from {source}: {e}")
                results[source] = []
        
        return results


# Global scraper manager instance
scraper_manager = ScraperManager()
