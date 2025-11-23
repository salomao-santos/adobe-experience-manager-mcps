#!/usr/bin/env python3
"""
Adobe Experience Manager MCP Server

This server provides tools to extract and transform AEM documentation from
Experience League into clean Markdown format suitable for LLMs.
"""

import asyncio
import logging
from typing import Any
from urllib.parse import urlparse

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool, TextContent, ImageContent, EmbeddedResource

from playwright.async_api import async_playwright, Browser, Page
from bs4 import BeautifulSoup
import html2text

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server instance
app = Server("adobe-experience-manager-mcps")

# Global browser instance
browser: Browser | None = None

# Selectors for elements to remove from the page
UNWANTED_SELECTORS = 'nav, header, footer, .nav, .header, .footer, .sidebar, .navigation, script, style, .cookie-banner, .feedback, .breadcrumb'


async def get_browser() -> Browser:
    """Get or create a browser instance."""
    global browser
    if browser is None:
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=True)
    return browser


async def read_aem_doc(url: str) -> str:
    """
    Extract documentation content from an AEM Experience League URL.
    
    This function:
    1. Uses Playwright to load the page and handle dynamic content
    2. Extracts the main content area while filtering out navigation, headers, footers
    3. Converts HTML to clean Markdown using html2text
    
    Args:
        url: The Experience League documentation URL
        
    Returns:
        Clean Markdown content suitable for LLM consumption
        
    Raises:
        Exception: If page loading or parsing fails
    """
    # Validate URL is from Experience League
    parsed = urlparse(url)
    # Check if the domain is adobe.com or a subdomain of adobe.com
    if not (parsed.netloc == 'adobe.com' or parsed.netloc.endswith('.adobe.com')):
        logger.warning(f"URL {url} may not be from Adobe Experience League")
    
    browser = await get_browser()
    page = await browser.new_page()
    
    try:
        logger.info(f"Loading URL: {url}")
        await page.goto(url, wait_until="networkidle", timeout=30000)
        
        # Wait for main content to load
        try:
            await page.wait_for_selector("main, article, .content, [role='main']", timeout=10000)
        except Exception as e:
            logger.warning(f"Main content selector not found, proceeding with full page: {e}")
        
        # Get page content
        content = await page.content()
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(content, 'lxml')
        
        # Remove unwanted elements
        for element in soup.select(UNWANTED_SELECTORS):
            element.decompose()
        
        # Try to find main content area
        main_content = None
        
        # Common selectors for main content in Experience League
        content_selectors = [
            'main',
            'article',
            '[role="main"]',
            '.content',
            '.main-content',
            '.article-content',
            '.documentation',
            '#main-content',
        ]
        
        for selector in content_selectors:
            main_content = soup.select_one(selector)
            if main_content:
                logger.info(f"Found main content using selector: {selector}")
                break
        
        # If no main content found, use body
        if not main_content:
            logger.warning("Could not find main content area, using body")
            main_content = soup.body or soup
        
        # Convert to markdown
        h2t = html2text.HTML2Text()
        h2t.ignore_links = False
        h2t.ignore_images = False
        h2t.ignore_emphasis = False
        h2t.body_width = 0  # Don't wrap lines
        h2t.single_line_break = False
        
        markdown = h2t.handle(str(main_content))
        
        # Clean up excessive whitespace
        lines = markdown.split('\n')
        cleaned_lines = []
        prev_empty = False
        
        for line in lines:
            is_empty = line.strip() == ''
            if is_empty and prev_empty:
                continue
            cleaned_lines.append(line)
            prev_empty = is_empty
        
        result = '\n'.join(cleaned_lines).strip()
        
        logger.info(f"Successfully extracted {len(result)} characters of markdown content")
        return result
        
    except Exception as e:
        logger.error(f"Error extracting content from {url}: {e}")
        raise
        
    finally:
        await page.close()


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="read_aem_doc",
            description=(
                "Extract and convert Adobe Experience Manager documentation from Experience League "
                "to clean Markdown format. This tool scrapes the main content from AEM documentation "
                "pages (code quality rules, release notes, guides, etc.) while filtering out "
                "navigation menus, headers, and footers. Returns structured Markdown suitable for "
                "LLM consumption."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": (
                            "The Experience League documentation URL to extract. "
                            "Example: https://experienceleague.adobe.com/docs/experience-manager-cloud-service/..."
                        ),
                    },
                },
                "required": ["url"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""
    if name == "read_aem_doc":
        url = arguments.get("url")
        if not url:
            raise ValueError("url parameter is required")
        
        try:
            markdown_content = await read_aem_doc(url)
            return [
                TextContent(
                    type="text",
                    text=markdown_content,
                )
            ]
        except Exception as e:
            error_msg = f"Error extracting documentation: {str(e)}"
            logger.error(error_msg)
            return [
                TextContent(
                    type="text",
                    text=error_msg,
                )
            ]
    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    """Main entry point for the MCP server."""
    logger.info("Starting Adobe Experience Manager MCP Server")
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
