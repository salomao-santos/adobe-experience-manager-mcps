#!/usr/bin/env python3
"""Quick test script to validate HTML extraction from Adobe documentation."""

import asyncio
import sys
from adobelabs.aem_documentation_mcp_server.util import (
    extract_content_from_html,
    extract_page_title,
    is_html_content,
)
import httpx


async def test_url(url: str):
    """Test fetching and extracting content from a URL."""
    print(f'\n{"="*80}')
    print(f'Testing URL: {url}')
    print("=" * 80)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                follow_redirects=True,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
                },
                timeout=30,
            )

        print(f'Status Code: {response.status_code}')
        print(f'Content-Type: {response.headers.get("content-type")}')

        if response.status_code >= 400:
            print(f'ERROR: Failed to fetch - status code {response.status_code}')
            return

        page_raw = response.text
        content_type = response.headers.get('content-type', '')

        # Extract title
        title = extract_page_title(page_raw)
        print(f'Title: {title}')

        # Check if HTML
        is_html = is_html_content(page_raw, content_type)
        print(f'Is HTML: {is_html}')

        if is_html:
            # Extract content
            content = extract_content_from_html(page_raw)
            print(f'\nContent Length: {len(content)} characters')
            print(f'\nFirst 500 characters of extracted markdown:')
            print('-' * 80)
            print(content[:500])
            print('-' * 80)
            print(f'\nLast 500 characters of extracted markdown:')
            print('-' * 80)
            print(content[-500:])
            print('-' * 80)

    except Exception as e:
        print(f'ERROR: {str(e)}')
        import traceback

        traceback.print_exc()


async def main():
    """Main test function."""
    test_urls = [
        'https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/overview/introduction',
        'https://experienceleague.adobe.com/en/docs/experience-manager-65',
        'https://developer.adobe.com/experience-cloud/experience-manager-apis/guides/events/',
    ]

    for url in test_urls:
        await test_url(url)

    print(f'\n{"="*80}')
    print('All tests completed!')
    print('=' * 80)


if __name__ == '__main__':
    asyncio.run(main())
