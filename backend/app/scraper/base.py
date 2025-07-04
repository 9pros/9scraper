import asyncio
import random
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

import structlog
from playwright.async_api import Browser, BrowserContext, Page, Playwright, async_playwright

from app.core.config import settings

logger = structlog.get_logger(__name__)


class BaseScraper(ABC):
    """Abstract base class for all scrapers."""
    
    def __init__(self, use_proxy: bool = True, headless: bool = True):
        self.use_proxy = use_proxy
        self.headless = headless
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.session_data: Dict[str, Any] = {}
        
    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.cleanup()
        
    async def initialize(self) -> None:
        """Initialize browser and setup anti-detection."""
        try:
            self.playwright = await async_playwright().start()
            
            # Browser options with stealth
            browser_options = {
                "headless": self.headless,
                "args": [
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-blink-features=AutomationControlled",
                    "--disable-features=VizDisplayCompositor",
                ]
            }
            
            # Launch browser
            self.browser = await self.playwright.chromium.launch(**browser_options)
            
            # Create context with anti-detection
            context_options = await self._get_context_options()
            self.context = await self.browser.new_context(**context_options)
            
            # Apply stealth techniques
            await self._apply_stealth_techniques()
            
            # Create page
            self.page = await self.context.new_page()
            
            logger.info("Browser initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize browser: {e}")
            await self.cleanup()
            raise

    async def cleanup(self) -> None:
        """Clean up browser resources."""
        try:
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
                
            logger.info("Browser cleanup completed")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    async def _get_context_options(self) -> Dict[str, Any]:
        """Get browser context options with anti-detection."""
        options = {
            "viewport": {"width": 1920, "height": 1080},
            "user_agent": await self._get_random_user_agent(),
            "locale": "en-US",
            "timezone_id": "America/New_York",
            "permissions": ["geolocation"],
            "geolocation": {"latitude": 40.7128, "longitude": -74.0060},  # NYC
        }
        
        # Add proxy if enabled
        if self.use_proxy and settings.USE_PROXIES:
            proxy_config = await self._get_proxy_config()
            if proxy_config:
                options["proxy"] = proxy_config
                
        return options
    
    async def _apply_stealth_techniques(self) -> None:
        """Apply various stealth techniques to avoid detection."""
        if not self.context:
            return
            
        # Override navigator properties
        await self.context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
            
            window.chrome = {
                runtime: {},
            };
        """)
        
        # Randomize screen properties
        await self.context.add_init_script(f"""
            Object.defineProperty(screen, 'availHeight', {{
                get: () => {random.randint(1000, 1080)},
            }});
            Object.defineProperty(screen, 'availWidth', {{
                get: () => {random.randint(1800, 1920)},
            }});
        """)
    
    async def _get_random_user_agent(self) -> str:
        """Get a random user agent string."""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        ]
        return random.choice(user_agents)
    
    async def _get_proxy_config(self) -> Optional[Dict[str, str]]:
        """Get proxy configuration."""
        if not settings.USE_PROXIES:
            return None
            
        if settings.PROXY_PROVIDER == "brightdata":
            if not all([settings.PROXY_HOST, settings.PROXY_PORT, 
                       settings.PROXY_USERNAME, settings.PROXY_PASSWORD]):
                logger.warning("Incomplete Bright Data proxy configuration")
                return None
                
            proxy_config = {
                "server": f"https://{settings.PROXY_HOST}:{settings.PROXY_PORT}",
                "username": settings.PROXY_USERNAME,
                "password": settings.PROXY_PASSWORD,
            }
            
            # Note: For production, you may need to handle SSL certificate verification
            # For now, we'll use the proxy without custom certificate handling
            # as Playwright should handle it automatically
            
            logger.info(f"Using Bright Data proxy: {settings.PROXY_HOST}:{settings.PROXY_PORT}")
            return proxy_config
            
        # Add other proxy providers here if needed
        return None
    
    async def random_delay(self, min_seconds: float = 0.5, max_seconds: float = 2.0) -> None:
        """Add random delay to simulate human behavior."""
        delay = random.uniform(min_seconds, max_seconds)
        await asyncio.sleep(delay)
    
    async def human_scroll(self, direction: str = "down", speed: str = "medium") -> None:
        """Simulate human-like scrolling."""
        if not self.page:
            return
            
        scroll_amounts = {
            "slow": 100,
            "medium": 300,
            "fast": 500,
        }
        
        amount = scroll_amounts.get(speed, 300)
        if direction == "down":
            amount = amount
        else:
            amount = -amount
            
        await self.page.evaluate(f"window.scrollBy(0, {amount})")
        await self.random_delay(0.5, 1.5)
    
    @abstractmethod
    async def search_businesses(
        self, 
        keyword: str, 
        location: str, 
        radius_miles: int = 25
    ) -> List[Dict[str, Any]]:
        """Search for businesses. Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    async def extract_business_details(self, business_url: str) -> Dict[str, Any]:
        """Extract detailed business information. Must be implemented by subclasses."""
        pass
