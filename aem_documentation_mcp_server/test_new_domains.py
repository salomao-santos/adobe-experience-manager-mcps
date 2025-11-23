#!/usr/bin/env python3
"""Quick test script for new domain support."""

import asyncio
from adobelabs.aem_documentation_mcp_server.server_utils import (
    read_documentation_impl,
    validate_adobe_url,
)


class MockContext:
    """Mock context for testing."""

    async def error(self, message):
        print(f'❌ Error: {message}')

    async def info(self, message):
        print(f'ℹ️  Info: {message}')


async def test_url(url: str, description: str):
    """Test fetching a URL."""
    print(f'\n{"="*80}')
    print(f'Testing: {description}')
    print(f'URL: {url}')
    print(f'{"="*80}')

    # Validate URL
    is_valid, error_msg = validate_adobe_url(url)
    if not is_valid:
        print(f'❌ Validation failed: {error_msg}')
        return

    print('✅ URL validated successfully')

    # Fetch content
    ctx = MockContext()
    try:
        result = await read_documentation_impl(ctx, url, 2000, 0, 'test-session')
        print(f'\n📄 Content Preview (first 500 chars):')
        print('-' * 80)
        print(result[:500])
        print('-' * 80)
        print(f'\n📊 Total length: {len(result)} characters')
    except Exception as e:
        print(f'❌ Failed to fetch: {e}')


async def main():
    """Run all tests."""
    test_urls = [
        ('https://github.com/adobe/aem-project-archetype', 'GitHub - AEM Project Archetype'),
        (
            'https://sling.apache.org/documentation/bundles/models.html',
            'Apache Sling Models Documentation',
        ),
        ('https://adapt.to/2025/schedule', 'adaptTo() 2025 Schedule'),
        (
            'https://www.youtube.com/watch?v=nJ8QTNQEkD8',
            'YouTube - AEM Video (Transcript Guidance)',
        ),
        (
            'https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/overview/introduction',
            'Adobe Experience League - AEM Cloud Service Intro',
        ),
    ]

    for url, description in test_urls:
        await test_url(url, description)

    print(f'\n{"="*80}')
    print('✅ All domain tests completed!')
    print(f'{"="*80}')


if __name__ == '__main__':
    asyncio.run(main())
