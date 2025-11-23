#!/usr/bin/env python3
"""Debug script to inspect HTML structure of developer.adobe.com."""

import asyncio
import httpx
from bs4 import BeautifulSoup


async def inspect_html_structure(url: str):
    """Inspect HTML structure of a URL to find content selectors."""
    print(f'\nInspecting: {url}')
    print('=' * 80)

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            follow_redirects=True,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            },
            timeout=30,
        )

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all divs with ids
    print('\nDivs with IDs:')
    for div in soup.find_all('div', id=True):
        print(f'  #{div.get("id")} - text length: {len(div.get_text(strip=True))}')

    # Find all divs with classes
    print('\nTop-level divs with classes (text > 1000 chars):')
    for div in soup.find_all('div', class_=True, recursive=False):
        text_len = len(div.get_text(strip=True))
        if text_len > 1000:
            classes = ' '.join(div.get('class', []))
            print(f'  .{classes} - text length: {text_len}')

    # Find main, article, section tags
    print('\nSemantic tags:')
    for tag_name in ['main', 'article', 'section']:
        tags = soup.find_all(tag_name)
        for tag in tags[:3]:  # First 3
            classes = ' '.join(tag.get('class', []))
            tag_id = tag.get('id', '')
            text_len = len(tag.get_text(strip=True))
            print(
                f'  <{tag_name}> id="{tag_id}" class="{classes}" - text length: {text_len}'
            )


asyncio.run(
    inspect_html_structure(
        'https://developer.adobe.com/experience-cloud/experience-manager-apis/guides/events/'
    )
)
