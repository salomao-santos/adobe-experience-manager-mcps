#!/usr/bin/env python3
"""
MCP Server for Adobe Experience Manager Documentation.

This server provides tools to extract and convert AEM documentation from HTML to clean Markdown,
filtering out navigation elements and focusing on main content.
"""

import asyncio
import logging
from typing import Any
from urllib.parse import urlparse

from mcp.server import Server
from mcp.types import Tool, TextContent
from playwright.async_api import async_playwright, Browser, Page
from bs4 import BeautifulSoup
import html2text

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP server
app = Server("aem-mcp-server")

# Global browser instance
browser: Browser | None = None


async def get_browser() -> Browser:
    """Get or create browser instance."""
    global browser
    if browser is None:
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=True)
    return browser


def extract_main_content(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Extract main content from Adobe documentation page.
    
    Removes navigation menus, footers, headers, and other non-content elements.
    
    Args:
        soup: BeautifulSoup object of the page
        
    Returns:
        BeautifulSoup object containing only main content
    """
    # Remove common navigation and non-content elements
    selectors_to_remove = [
        'nav',
        'header',
        'footer',
        '.header',
        '.footer',
        '.navigation',
        '.nav',
        '.sidebar',
        '.menu',
        '.breadcrumb',
        '.toc',
        '#header',
        '#footer',
        '#navigation',
        '#sidebar',
        '[role="navigation"]',
        '[role="banner"]',
        '[role="contentinfo"]',
        '.globalNav',
        '.feds-topnav',
        '.feds-footer',
        'script',
        'style',
        'noscript',
    ]
    
    for selector in selectors_to_remove:
        for element in soup.select(selector):
            element.decompose()
    
    # Try to find main content area
    main_content = None
    
    # Common main content selectors for Adobe documentation
    main_selectors = [
        'main',
        '[role="main"]',
        '.main-content',
        '#main-content',
        'article',
        '.article',
        '.content',
        '#content',
        '.markdown-body',
        '.documentation',
    ]
    
    for selector in main_selectors:
        main_content = soup.select_one(selector)
        if main_content:
            logger.info(f"Found main content using selector: {selector}")
            break
    
    # If no main content area found, use body
    if not main_content:
        main_content = soup.find('body')
        logger.info("Using body as main content")
    
    return main_content if main_content else soup


def html_to_markdown(html_content: str) -> str:
    """
    Convert HTML to clean Markdown.
    
    Args:
        html_content: HTML string
        
    Returns:
        Clean Markdown string
    """
    h = html2text.HTML2Text()
    
    # Configure html2text for clean output
    h.ignore_links = False
    h.ignore_images = False
    h.ignore_emphasis = False
    h.body_width = 0  # Don't wrap lines
    h.ignore_tables = False
    h.single_line_break = True
    h.mark_code = True
    
    markdown = h.handle(html_content)
    
    # Clean up excessive whitespace
    lines = markdown.split('\n')
    cleaned_lines = []
    prev_empty = False
    
    for line in lines:
        is_empty = not line.strip()
        # Skip multiple consecutive empty lines
        if is_empty and prev_empty:
            continue
        cleaned_lines.append(line)
        prev_empty = is_empty
    
    return '\n'.join(cleaned_lines).strip()


async def fetch_aem_doc(url: str) -> str:
    """
    Fetch and convert AEM documentation to Markdown.
    
    Args:
        url: URL of the AEM documentation page
        
    Returns:
        Clean Markdown representation of the documentation
        
    Raises:
        ValueError: If URL is invalid
        Exception: If fetching or conversion fails
    """
    # Validate URL
    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        raise ValueError(f"Invalid URL: {url}")
    
    logger.info(f"Fetching documentation from: {url}")
    
    browser = await get_browser()
    page: Page = await browser.new_page()
    
    try:
        # Navigate to page with timeout
        await page.goto(url, wait_until="networkidle", timeout=30000)
        
        # Wait for content to load
        await page.wait_for_load_state("domcontentloaded")
        
        # Get page content
        html_content = await page.content()
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(html_content, 'lxml')
        
        # Extract main content
        main_content = extract_main_content(soup)
        
        # Convert to markdown
        markdown = html_to_markdown(str(main_content))
        
        logger.info(f"Successfully converted {url} to Markdown ({len(markdown)} characters)")
        
        return markdown
        
    except Exception as e:
        logger.error(f"Error fetching {url}: {str(e)}")
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
                "Extract and convert Adobe Experience Manager documentation from a URL to clean Markdown. "
                "This tool fetches AEM documentation pages (such as code quality rules, release notes, "
                "or technical documentation), removes navigation elements, headers, footers, and other "
                "non-content elements, then converts the main content to well-structured Markdown format "
                "suitable for LLM consumption. "
                "Supports Adobe Experience Manager Cloud Service documentation and other Adobe documentation sites."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL of the AEM documentation page to extract and convert",
                    }
                },
                "required": ["url"],
            },
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""
    if name == "read_aem_doc":
        url = arguments.get("url")
        if not url:
            raise ValueError("URL parameter is required")
        
        try:
            markdown = await fetch_aem_doc(url)
            return [
                TextContent(
                    type="text",
                    text=markdown,
                )
            ]
        except Exception as e:
            error_message = f"Error extracting documentation from {url}: {str(e)}"
            logger.error(error_message)
            return [
                TextContent(
                    type="text",
                    text=error_message,
                )
            ]
    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    """Run the MCP server."""
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
