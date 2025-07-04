#!/usr/bin/env python3
"""
Standalone test script to verify Bright Data proxy configuration
"""
import asyncio
from playwright.async_api import async_playwright
import ssl
import os

async def test_proxy():
    proxy_config = {
        "server": "brd.superproxy.io:33335",
        "username": "brd-customer-hl_c2f94a5d-zone-residential_proxy1",
        "password": "9w2xx83lltkv",
    }
    
    print(f"Testing proxy configuration:")
    print(f"Server: {proxy_config['server']}")
    print(f"Username: {proxy_config['username']}")
    print(f"Password: {'*' * len(proxy_config['password'])}")
    print()
    
    async with async_playwright() as p:
        # Try with Chrome/Chromium (most common)
        browser = await p.chromium.launch(
            headless=True,
            proxy=proxy_config,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        try:
            context = await browser.new_context(
                ignore_https_errors=True,  # Since we're using proxy with self-signed cert
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            page = await context.new_page()
            
            # Test 1: Check IP location (should show proxy location)
            print("Testing proxy connection...")
            await page.goto('https://geo.brdtest.com/welcome.txt?product=resi&method=native', timeout=30000)
            content = await page.content()
            print(f"Proxy test response:\n{content}\n")
            
            # Test 2: Check actual IP
            print("Checking IP address...")
            await page.goto('https://api.ipify.org?format=json', timeout=30000)
            ip_data = await page.content()
            print(f"Current IP data: {ip_data}\n")
            
            print("✅ Proxy configuration is working correctly!")
            
        except Exception as e:
            print(f"❌ Error testing proxy: {e}")
            
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(test_proxy())