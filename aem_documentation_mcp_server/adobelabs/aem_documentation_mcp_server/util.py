# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
"""Utility functions for Adobe AEM Documentation MCP Server."""

import markdownify
from typing import Optional
from bs4 import BeautifulSoup


def extract_content_from_html(html: str) -> str:
    """Extract and convert HTML content to Markdown format.

    This function processes Adobe documentation HTML and converts it to
    clean Markdown format, removing navigation elements and focusing on
    the main content.

    Args:
        html: Raw HTML content to process

    Returns:
        Simplified markdown version of the content
    """
    if not html:
        return '<e>Empty HTML content</e>'

    try:
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Try to find the main content area
        main_content = None

        # Adobe-specific and common content container selectors
        content_selectors = [
            # Developer.adobe.com specific (Gatsby-based)
            '#___gatsby',
            '#gatsby-focus-wrapper',
            'main.css-7wiue4',
            # Adobe Experience League specific
            '.article-content',
            '.doc-content',
            '.documentation-content',
            '.page-content',
            '.sp-wrapper',
            '.content-container',
            '#article-content-body',
            # GitHub specific
            'article.markdown-body',
            '.repository-content',
            '#readme',
            '.Box-body',
            # Apache Sling specific
            '.content',
            '#content',
            # adaptTo() specific
            '.main-content',
            '.content-wrapper',
            # Common selectors
            'main',
            'article',
            '#main-content',
            '.main-content',
            '#content',
            '.content',
            "div[role='main']",
        ]

        # Try to find the main content using common selectors
        for selector in content_selectors:
            content = soup.select_one(selector)
            if content:
                main_content = content
                break

        # If no main content found, use the body
        if not main_content:
            main_content = soup.body if soup.body else soup

        # Remove navigation elements that might be in the main content
        nav_selectors = [
            'noscript',
            'script',
            'style',
            'nav',
            'header',
            'footer',
            'aside',
            # Adobe-specific navigation and UI elements
            '.adobe-header',
            '.adobe-footer',
            '.navigation',
            '.breadcrumb',
            '.breadcrumbs',
            '.cookie-banner',
            '.cookie-notice',
            '.cookie-consent',
            '.feedback-widget',
            '.feedback-container',
            '.language-selector',
            '.lang-selector',
            '.page-nav',
            '.side-nav',
            '.sidebar',
            '.toc',
            '.table-of-contents',
            '.prev-next',
            '.pagination',
            # Social and sharing
            '.social-share',
            '.share-buttons',
            # Adobe Experience League specific
            '.feds-header',
            '.feds-footer',
            '.feds-navList',
            '.spectrum-Accordion',
            '.mini-toc-container',
            # GitHub specific
            '.Box-header',
            '.pagehead',
            '.reponav',
            '.file-navigation',
            # Apache Sling specific
            '#navigation',
            '.nav',
            # adaptTo() specific
            '.site-header',
            '.site-footer',
            # Advertising and tracking
            '.advertisement',
            '.ad-container',
            '.tracking',
        ]

        for selector in nav_selectors:
            for element in main_content.select(selector):
                element.decompose()

        # Define tags to strip completely
        tags_to_strip = [
            'script',
            'style',
            'noscript',
            'meta',
            'link',
            'svg',
            'iframe',
        ]

        # Use markdownify on the cleaned HTML content
        content = markdownify.markdownify(
            str(main_content),
            heading_style=markdownify.ATX,
            autolinks=True,
            default_title=True,
            escape_asterisks=False,
            escape_underscores=False,
            newline_style='SPACES',
            strip=tags_to_strip,
        )

        if not content or len(content.strip()) < 10:
            return '<e>Page failed to be simplified from HTML or content too short</e>'

        return content.strip()

    except Exception as e:
        return f'<e>Error converting HTML to Markdown: {str(e)}</e>'


def is_html_content(page_raw: str, content_type: str) -> bool:
    """Determine if content is HTML.

    Args:
        page_raw: Raw page content
        content_type: Content-Type header

    Returns:
        True if content is HTML, False otherwise
    """
    return (
        '<html' in page_raw[:200].lower()
        or 'text/html' in content_type.lower()
        or not content_type
    )


def format_documentation_result(
    url: str, content: str, start_index: int, max_length: int
) -> tuple[str, bool]:
    """Format documentation result with pagination information.

    Args:
        url: Documentation URL
        content: Content to format
        start_index: Start index for pagination
        max_length: Maximum content length

    Returns:
        Tuple of (formatted documentation result, is_truncated)
    """
    original_length = len(content)

    if start_index >= original_length:
        return f'Adobe AEM Documentation from {url}:\n\n<e>No more content available.</e>', False

    # Calculate the end index, ensuring we don't go beyond the content length
    end_index = min(start_index + max_length, original_length)
    truncated_content = content[start_index:end_index]

    if not truncated_content:
        return f'Adobe AEM Documentation from {url}:\n\n<e>No more content available.</e>', False

    actual_content_length = len(truncated_content)
    remaining_content = original_length - (start_index + actual_content_length)

    result = f'Adobe AEM Documentation from {url}:\n\n{truncated_content}'

    is_truncated = remaining_content > 0

    # Only add the prompt to continue fetching if there is still remaining content
    if is_truncated:
        next_start = start_index + actual_content_length
        result += f'\n\n<e>Content truncated. Call the read_documentation tool with start_index={next_start} to get more content. Total length: {original_length}, Retrieved: {end_index}</e>'

    return result, is_truncated


def extract_page_title(html: str) -> Optional[str]:
    """Extract page title from HTML.

    Args:
        html: Raw HTML content

    Returns:
        Page title if found, None otherwise
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')

        # Try various title sources
        # 1. <title> tag
        if soup.title and soup.title.string:
            return soup.title.string.strip()

        # 2. h1 heading
        h1 = soup.find('h1')
        if h1:
            return h1.get_text().strip()

        # 3. meta og:title
        og_title = soup.find('meta', property='og:title')
        if og_title and og_title.get('content'):
            return og_title.get('content').strip()

        return None

    except Exception:
        return None
