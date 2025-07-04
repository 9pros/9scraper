#!/usr/bin/env python3
"""
Test script to verify Bright Data proxy configuration
"""
import asyncio
import os
from pathlib import Path

# Add the backend directory to the Python path
import sys
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app.core.config import settings


async def test_proxy_config():
    """Test the proxy configuration."""
    print("=== Bright Data Proxy Configuration Test ===\n")
    
    print("Configuration loaded from .env:")
    print(f"USE_PROXIES: {settings.USE_PROXIES}")
    print(f"PROXY_PROVIDER: {settings.PROXY_PROVIDER}")
    print(f"PROXY_HOST: {settings.PROXY_HOST}")
    print(f"PROXY_PORT: {settings.PROXY_PORT}")
    print(f"PROXY_USERNAME: {settings.PROXY_USERNAME}")
    print(f"PROXY_PASSWORD: {'*' * len(settings.PROXY_PASSWORD) if settings.PROXY_PASSWORD else 'Not set'}")
    print(f"PROXY_SSL_CERT_PATH: {settings.PROXY_SSL_CERT_PATH}")
    
    if settings.PROXY_SSL_CERT_PATH and os.path.exists(settings.PROXY_SSL_CERT_PATH):
        print(f"\n✓ SSL certificate file exists at: {settings.PROXY_SSL_CERT_PATH}")
    else:
        print("\n⚠ SSL certificate file not found or not configured")
    
    print("\n=== Testing with Playwright ===")
    
    try:
        from playwright.async_api import async_playwright
        
        async with async_playwright() as p:
            print("Launching browser with proxy configuration...")
            
            browser = await p.chromium.launch(headless=True)
            
            context_options = {
                "viewport": {"width": 1920, "height": 1080},
            }
            
            if settings.USE_PROXIES and settings.PROXY_PROVIDER == "brightdata":
                context_options["proxy"] = {
                    "server": f"https://{settings.PROXY_HOST}:{settings.PROXY_PORT}",
                    "username": settings.PROXY_USERNAME,
                    "password": settings.PROXY_PASSWORD,
                }
                print(f"Using proxy: {settings.PROXY_HOST}:{settings.PROXY_PORT}")
            
            context = await browser.new_context(**context_options)
            page = await context.new_page()
            
            # Test the connection by checking IP
            print("\nChecking IP address...")
            await page.goto("https://httpbin.org/ip")
            content = await page.content()
            print(f"Response: {content}")
            
            # Clean up
            await context.close()
            await browser.close()
            
            print("\n✓ Proxy test completed successfully!")
            
    except Exception as e:
        print(f"\n✗ Error during proxy test: {e}")
        print("\nMake sure you have playwright installed:")
        print("pip install playwright")
        print("playwright install chromium")


if __name__ == "__main__":
    asyncio.run(test_proxy_config())