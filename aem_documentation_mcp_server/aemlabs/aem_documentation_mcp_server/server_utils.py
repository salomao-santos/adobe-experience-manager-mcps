# Copyright 2024-2025 Salomão Santos (salomaosantos777@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Shared utilities for Adobe AEM Documentation MCP Server."""

import httpx
import os
from aemlabs.aem_documentation_mcp_server.util import (
    extract_content_from_html,
    extract_page_title,
    format_documentation_result,
    is_html_content,
)
from aemlabs.aem_documentation_mcp_server.youtube_utils import (
    extract_video_id,
    is_youtube_url,
)
from importlib.metadata import version
from loguru import logger
from mcp.server.fastmcp import Context
from typing import Optional
from urllib.parse import urlparse


try:
    __version__ = version('aemlabs.aem-documentation-mcp-server')
except Exception:
    from . import __version__


# Allow User-Agent override via environment variable
BASE_USER_AGENT = os.getenv(
    'MCP_USER_AGENT',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
)
DEFAULT_USER_AGENT = (
    f'{BASE_USER_AGENT} ModelContextProtocol/{__version__} (Adobe AEM Documentation Server)'
)


async def read_documentation_impl(
    ctx: Context,
    url_str: str,
    max_length: int,
    start_index: int,
    session_uuid: str,
) -> str:
    """Implementation of the read_documentation tool.

    This function fetches Adobe AEM documentation pages and converts them
    to Markdown format with support for pagination.

    Args:
        ctx: MCP context for logging and error handling
        url_str: URL of the documentation page
        max_length: Maximum number of characters to return
        start_index: Starting character index for pagination
        session_uuid: Unique session identifier for tracking

    Returns:
        Formatted markdown documentation or error message
    """
    logger.debug(f'Fetching Adobe AEM documentation from {url_str}')

    # Special handling for YouTube URLs
    if is_youtube_url(url_str):
        video_id = extract_video_id(url_str)
        if video_id:
            await ctx.info(f'Detected YouTube video: {video_id}')
            content = f'# YouTube Video: {video_id}\n\n'
            content += f'**Video URL**: {url_str}\n\n'
            content += f'**Video ID**: {video_id}\n\n'
            content += '## Note on Transcripts\n\n'
            content += 'To extract video transcripts, you can:\n'
            content += f'1. Visit the YouTube page directly: https://www.youtube.com/watch?v={video_id}\n'
            content += '2. Use YouTube\'s transcript feature (click "..." → "Show transcript")\n'
            content += '3. Use third-party tools or APIs like youtube-transcript-api\n\n'
            content += '**Note**: Automatic transcript extraction requires additional dependencies '
            content += 'and API access not included in this version.\n'

            result, _ = format_documentation_result(url_str, content, start_index, max_length)
            return result

    # Parse URL and check if it's a PDF file
    parsed_url = urlparse(url_str)
    is_pdf = url_str.lower().endswith('.pdf')
    
    if is_pdf:
        await ctx.info(f'Detected PDF file: {url_str}')
        # Extract filename from URL
        filename = parsed_url.path.split('/')[-1]
        content = f'# PDF Document: {filename}\n\n'
        content += f'**PDF URL**: {url_str}\n\n'
        content += f'**Filename**: {filename}\n\n'
        content += '## Note on PDF Access\n\n'
        content += 'This is a PDF document. To access the content:\n\n'
        content += f'1. **Direct Download**: Download the PDF from: {url_str}\n'
        content += '2. **View in Browser**: Open the URL directly in your browser\n'
        content += '3. **Extract Text**: Use PDF extraction tools like PyPDF2 or pdfplumber\n\n'
        content += '**Note**: Automatic PDF text extraction requires additional dependencies '
        content += '(PyPDF2, pdfplumber) not included in this version.\n\n'
        
        # Try to detect if it's an adaptTo() presentation
        if 'adapt.to' in url_str and '/presentations/' in url_str:
            content += '## adaptTo() Presentation\n\n'
            content += 'This appears to be a presentation from the adaptTo() conference. '
            content += 'These presentations typically contain:\n'
            content += '- Technical architecture diagrams\n'
            content += '- Code examples and best practices\n'
            content += '- Case studies and real-world implementations\n'
            content += '- Performance optimization techniques\n\n'
        
        result, _ = format_documentation_result(url_str, content, start_index, max_length)
        return result

    # Parse URL and check if it's a search page
    is_search_page = '/search' in parsed_url.path or (parsed_url.fragment and parsed_url.fragment.startswith('q='))
    is_adaptto = 'adapt.to' in parsed_url.netloc
    
    # For search pages, preserve the hash fragment as it contains search parameters
    # For adapt.to, preserve hash fragments for day navigation (e.g., #day-1, #day-2)
    if is_search_page or is_adaptto:
        clean_url = url_str
        await ctx.info(f'Detected special page type (search or adapt.to), preserving hash fragment')
    else:
        # Remove hash fragment for regular documentation pages
        clean_url = parsed_url._replace(fragment='').geturl()

    # Add session tracking parameter
    separator = '&' if '?' in clean_url else '?'
    url_with_session = f'{clean_url}{separator}session={session_uuid}'

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url_with_session,
                follow_redirects=True,
                headers={
                    'User-Agent': DEFAULT_USER_AGENT,
                    'X-MCP-Session-Id': session_uuid,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.9',
                },
                timeout=30,
            )
        except httpx.HTTPError as e:
            error_msg = f'Failed to fetch {url_str}: {str(e)}'
            logger.error(error_msg)
            await ctx.error(error_msg)
            return error_msg

        if response.status_code >= 400:
            error_msg = f'Failed to fetch {url_str} - status code {response.status_code}'
            logger.error(error_msg)
            await ctx.error(error_msg)
            return error_msg

        page_raw = response.text
        content_type = response.headers.get('content-type', '')

    # Extract title
    title = extract_page_title(page_raw)

    # Convert to markdown
    if is_html_content(page_raw, content_type):
        content = extract_content_from_html(page_raw)
    else:
        content = page_raw

    # Add title to content if available
    if title and not content.startswith('# '):
        content = f'# {title}\n\n{content}'

    # Format with pagination
    result, is_truncated = format_documentation_result(url_str, content, start_index, max_length)

    # Log if content was truncated
    if is_truncated:
        logger.debug(
            f'Content truncated at {start_index + max_length} of {len(content)} characters'
        )

    return result


def validate_adobe_url(url: str) -> tuple[bool, Optional[str]]:
    """Validate if URL is from supported Adobe and AEM-related domains.

    Args:
        url: URL to validate

    Returns:
        Tuple of (is_valid, error_message). error_message is None if valid.
    """
    import re

    # Supported Adobe and AEM-related domains
    supported_domains = [
        # Adobe official domains (including search pages)
        r'^https?://experienceleague\.adobe\.com/',
        r'^https?://developer\.adobe\.com/',
        r'^https?://helpx\.adobe\.com/',
        r'^https?://docs\.adobe\.com/',
        r'^https?://business\.adobe\.com/',
        # GitHub repositories (any organization, with or without repo path) and GitHub Pages
        r'^https?://github\.com/[^/]+',
        r'^https?://[^/]+\.github\.io/',
        # Apache Sling documentation
        r'^https?://sling\.apache\.org/',
        # adaptTo() conference (all years 2011-2025+, including PDFs)
        r'^https?://adapt\.to/',
        # YouTube channels (Adobe-related)
        r'^https?://(?:www\.)?youtube\.com/',
        r'^https?://(?:www\.)?youtu\.be/',
    ]

    # Check if URL matches any supported domain
    if not any(re.match(domain_regex, url) for domain_regex in supported_domains):
        return False, (
            f'Invalid URL: {url}. URL must be from supported domains: '
            'Adobe domains (experienceleague, developer, helpx, docs, business), '
            'GitHub (github.com, *.github.io), Apache Sling (sling.apache.org), '
            'adaptTo() (adapt.to, including PDFs), or YouTube'
        )

    return True, None
