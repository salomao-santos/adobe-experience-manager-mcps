#!/usr/bin/env python3
"""
Example usage of the AEM documentation extraction function.

This script demonstrates how to use the read_aem_doc function to extract
documentation from Adobe Experience League.
"""

import asyncio
import sys
from adobe_experience_manager_mcps.server import read_aem_doc


async def main():
    """Example usage of read_aem_doc function."""
    
    # Example URLs from Adobe Experience League
    example_urls = [
        "https://experienceleague.adobe.com/docs/experience-manager-cloud-service/content/release-notes/release-notes/release-notes-current.html",
        "https://experienceleague.adobe.com/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/code-quality-testing.html",
    ]
    
    if len(sys.argv) > 1:
        # Use URL from command line
        url = sys.argv[1]
    else:
        # Use first example URL
        url = example_urls[0]
        print(f"No URL provided, using example: {url}")
        print(f"\nUsage: python examples/example_usage.py <url>\n")
    
    print(f"Extracting documentation from: {url}\n")
    print("=" * 80)
    
    try:
        markdown_content = await read_aem_doc(url)
        
        print(markdown_content)
        print("\n" + "=" * 80)
        print(f"\nExtracted {len(markdown_content)} characters of markdown content")
        print(f"Lines: {len(markdown_content.splitlines())}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
