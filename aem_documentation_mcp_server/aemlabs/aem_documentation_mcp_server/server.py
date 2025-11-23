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
"""Adobe AEM Documentation MCP Server implementation."""

import os
import sys
import uuid
from aemlabs.aem_documentation_mcp_server.models import ServiceInfo
from aemlabs.aem_documentation_mcp_server.server_utils import (
    DEFAULT_USER_AGENT,
    read_documentation_impl,
    validate_adobe_url,
)
from aemlabs.aem_documentation_mcp_server.search_utils import (
    build_experience_league_search_url,
    EXPERIENCE_MANAGER_PRODUCTS,
    ALL_PRODUCTS,
    CONTENT_TYPES,
    ROLES,
)
from loguru import logger
from mcp.server.fastmcp import Context, FastMCP
from pydantic import Field
from typing import List, Union


# Set up logging
logger.remove()
logger.add(sys.stderr, level=os.getenv('FASTMCP_LOG_LEVEL', 'WARNING'))

SESSION_UUID = str(uuid.uuid4())

mcp = FastMCP(
    'aemlabs.aem-documentation-mcp-server',
    instructions="""
    # Adobe AEM Documentation MCP Server

    This server provides tools to access public Adobe Experience Manager (AEM) documentation
    and convert it to markdown format for easy consumption.

    ## Best Practices

    - Use `search_experience_league` to find relevant documentation before reading specific pages
    - Always use `get_available_services` first to see available AEM documentation areas
    - For long documentation pages, make multiple calls to `read_documentation` with different `start_index` values for pagination
    - For very long documents (>30,000 characters), stop reading if you've found the needed information
    - Always cite the documentation URL when providing information to users
    - Hash fragments in URLs are preserved for search pages and adapt.to conference schedules

    ## Tool Selection Guide

    - Use `search_experience_league` when: You need to find documentation about a specific topic
    - Use `get_available_services` when: You need to know what AEM services and documentation areas are available
    - Use `read_documentation` when: You have a specific documentation URL and need its content converted to markdown

    ## Supported Domains

    - experienceleague.adobe.com - Main Adobe Experience League documentation (including search)
    - developer.adobe.com - Adobe Developer documentation and APIs
    - helpx.adobe.com - Adobe Help documentation
    - docs.adobe.com - Adobe technical documentation
    - business.adobe.com - Adobe Summit and business resources
    - github.com - GitHub repositories (all organizations, not limited to Adobe)
    - *.github.io - GitHub Pages documentation sites
    - sling.apache.org - Apache Sling documentation (AEM foundation)
    - adapt.to - adaptTo() conference content (all years: 2011-2025+, including PDFs)
    - youtube.com - YouTube videos (Adobe Developers, AEM User Group channels)

    ## Special Features

    - **Experience League Search**: Full search support with filters for content type, products, and roles
    - **adaptTo() Conference**: Support for all conference years with hash fragment navigation (#day-1, #day-2, etc.)
    - **PDF Documents**: Detection and guidance for PDF downloads (adaptTo() presentations, etc.)
    - **GitHub Organizations**: Support for any GitHub organization (Adobe, Netcentric, ACS, etc.)
    - **GitHub Pages**: Support for documentation hosted on *.github.io
    - **Search Results**: Preserves hash fragments for search pages to maintain filter parameters
    """,
    dependencies=[
        'pydantic',
        'httpx',
        'beautifulsoup4',
        'markdownify',
    ],
)


@mcp.tool()
async def read_documentation(
    ctx: Context,
    url: str = Field(description='URL of the Adobe AEM documentation page to read'),
    max_length: int = Field(
        default=10000,
        description='Maximum number of characters to return.',
        gt=0,
        lt=1000000,
    ),
    start_index: int = Field(
        default=0,
        description='On return output starting at this character index, useful if a previous fetch was truncated and more content is required.',
        ge=0,
    ),
) -> str:
    """Fetch and convert an Adobe AEM documentation page to markdown format.

    ## Usage

    This tool retrieves the content of an Adobe AEM documentation page and converts it
    to markdown format. For long documents, you can make multiple calls with different
    start_index values to retrieve the entire content in chunks.

    ## URL Requirements

    - Must be from supported Adobe domains:
      - experienceleague.adobe.com
      - developer.adobe.com
      - helpx.adobe.com
      - docs.adobe.com
    - Hash fragments (#) are automatically removed before fetching

    ## Example URLs

    - https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/overview/introduction
    - https://experienceleague.adobe.com/en/docs/experience-manager-65
    - https://developer.adobe.com/experience-cloud/experience-manager-apis/guides/events/
    - https://github.com/adobe/aem-project-archetype
    - https://github.com/Adobe-Consulting-Services/acs-aem-commons
    - https://github.com/Netcentric/aem-multitenant-demo
    - https://adobe-consulting-services.github.io/acs-aem-commons/
    - https://sling.apache.org/documentation/bundles/models.html
    - https://adapt.to/2025/schedule
    - https://adapt.to/2025/presentations/adaptto-2025-challenges-when-operating-1000-different-aem-applications.pdf
    - https://www.youtube.com/watch?v=nJ8QTNQEkD8

    ## Output Format

    The output is formatted as markdown text with:
    - Preserved headings and structure
    - Code blocks for examples
    - Lists and tables converted to markdown format
    - Navigation elements removed for clean content

    ## Handling Long Documents

    If the response indicates the document was truncated, you have several options:

    1. **Continue Reading**: Make another call with start_index set to the end of the previous response
    2. **Stop Early**: For very long documents (>30,000 characters), if you've already found the
       specific information needed, you can stop reading

    Args:
        ctx: MCP context for logging and error handling
        url: URL of the Adobe AEM documentation page to read
        max_length: Maximum number of characters to return
        start_index: On return output starting at this character index

    Returns:
        Markdown content of the Adobe AEM documentation
    """
    url_str = str(url)

    # Validate URL
    is_valid, error_msg = validate_adobe_url(url_str)
    if not is_valid:
        await ctx.error(error_msg)
        return error_msg

    return await read_documentation_impl(ctx, url_str, max_length, start_index, SESSION_UUID)


@mcp.tool()
async def search_experience_league(
    ctx: Context,
    query: str = Field(description='Search query string'),
    content_types: List[str] = Field(
        default=['Documentation'],
        description='Content types to search (Documentation, Tutorial, Troubleshooting, etc.)',
    ),
    products: List[str] = Field(
        default=None,
        description='Products to filter (e.g., Experience Manager, Experience Manager|as a Cloud Service)',
    ),
    roles: List[str] = Field(
        default=None,
        description='Roles to filter (Developer, Admin, User, etc.)',
    ),
    include_all_aem_products: bool = Field(
        default=False,
        description='If true, automatically includes all AEM product variants in the search',
    ),
) -> str:
    """Search Adobe Experience League documentation with filters.

    ## Usage

    This tool generates a search URL for Adobe Experience League and fetches the results.
    You can filter by content types, products, and roles to narrow down results.

    ## Parameters

    - **query**: The search term (e.g., 'sling models', 'component development')
    - **content_types**: Filter by content type (default: ['Documentation'])
      - Options: Documentation, Tutorial, Troubleshooting, API Reference, Release Notes, Best Practices
    - **products**: Filter by Adobe products (optional)
      - Examples: 'Experience Manager', 'Experience Manager|as a Cloud Service', 'Experience Manager|6.5'
    - **roles**: Filter by user role (optional)
      - Options: Developer, Admin, User, Leader, Architect, Business Practitioner
    - **include_all_aem_products**: Automatically include all AEM variants (Cloud Service, 6.5, Assets, Sites, etc.)

    ## Examples

    Search for documentation about 'sling models':
    ```
    search_experience_league(query='sling models', content_types=['Documentation'])
    ```

    Search for tutorials about components, for developers:
    ```
    search_experience_league(
        query='components',
        content_types=['Tutorial'],
        roles=['Developer']
    )
    ```

    Search across all AEM products:
    ```
    search_experience_league(
        query='authentication',
        include_all_aem_products=True
    )
    ```

    Args:
        ctx: MCP context for logging and error handling
        query: Search query string
        content_types: List of content types to filter
        products: List of products to filter
        roles: List of roles to filter
        include_all_aem_products: Include all AEM product variants automatically

    Returns:
        Search results in markdown format
    """
    await ctx.info(f'Searching Experience League for: {query}')
    
    # If include_all_aem_products is True, use predefined AEM product list
    if include_all_aem_products and not products:
        products = EXPERIENCE_MANAGER_PRODUCTS
        await ctx.info(f'Including all AEM products in search: {len(products)} products')
    
    # Build search URL
    search_url = build_experience_league_search_url(
        query=query,
        content_types=content_types if content_types else None,
        products=products,
        roles=roles,
    )
    
    await ctx.info(f'Search URL: {search_url}')
    
    # Fetch and return search results
    return await read_documentation_impl(ctx, search_url, 10000, 0, SESSION_UUID)


@mcp.tool()
async def get_available_services(
    ctx: Context,
) -> List[ServiceInfo]:
    """Get a list of available Adobe AEM services and documentation areas.

    ## Usage

    This tool provides a curated list of major Adobe Experience Manager services
    and their documentation URLs. Use this to discover what documentation is available
    and get direct links to key documentation areas.

    ## Categories

    - **cloud-service**: AEM as a Cloud Service documentation
    - **on-premise**: AEM 6.5 and on-premise documentation
    - **apis**: Developer APIs and integration guides
    - **tools**: AEM tools and utilities
    - **learning**: Tutorials and learning resources

    Args:
        ctx: MCP context for logging and error handling

    Returns:
        List of available AEM services with names, URLs, descriptions, and categories
    """
    await ctx.info('Retrieving available Adobe AEM services and documentation areas')

    # Curated list of major AEM services and documentation areas
    services = [
        ServiceInfo(
            name='AEM as a Cloud Service - Overview',
            url='https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/overview/introduction',
            description='Introduction and overview of Adobe Experience Manager as a Cloud Service',
            category='cloud-service',
        ),
        ServiceInfo(
            name='AEM Cloud Service - Release Notes',
            url='https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/release-notes/cloud-manager/current',
            description='Current release notes for AEM Cloud Manager',
            category='cloud-service',
        ),
        ServiceInfo(
            name='AEM Sites Optimizer',
            url='https://experienceleague.adobe.com/en/docs/experience-manager-sites-optimizer/content/home',
            description='Adobe Experience Manager Sites Optimizer documentation',
            category='cloud-service',
        ),
        ServiceInfo(
            name='AEM 6.5 LTS Documentation',
            url='https://experienceleague.adobe.com/en/docs/experience-manager-65-lts',
            description='Adobe Experience Manager 6.5 Long Term Support documentation',
            category='on-premise',
        ),
        ServiceInfo(
            name='AEM 6.5 Documentation',
            url='https://experienceleague.adobe.com/en/docs/experience-manager-65',
            description='Complete documentation for Adobe Experience Manager 6.5',
            category='on-premise',
        ),
        ServiceInfo(
            name='AEM APIs and Events',
            url='https://developer.adobe.com/experience-cloud/experience-manager-apis/guides/events/',
            description='Adobe Experience Manager APIs and event-driven architecture guides',
            category='apis',
        ),
        ServiceInfo(
            name='AEM Developer Documentation',
            url='https://developer.adobe.com/experience-cloud/experience-manager-apis/guides/',
            description='Complete developer guides for AEM APIs and integrations',
            category='apis',
        ),
        ServiceInfo(
            name='AEM Cloud Service Security Best Practices',
            url='https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/security/best-practices-for-sling-service-user-mapping-and-service-user-definition',
            description='Security best practices for Sling Service User mapping and definition',
            category='cloud-service',
        ),
        ServiceInfo(
            name='AEM Documentation Browse',
            url='https://experienceleague.adobe.com/en/browse/experience-manager',
            description='Browse all Adobe Experience Manager documentation',
            category='learning',
        ),
        ServiceInfo(
            name='Adobe AI Documentation',
            url='https://experienceleague.adobe.com/en/docs/ai',
            description='Adobe AI and machine learning documentation',
            category='tools',
        ),
        ServiceInfo(
            name='AEM Project Archetype (GitHub)',
            url='https://github.com/adobe/aem-project-archetype',
            description='Maven template for AEM projects with best practices',
            category='tools',
        ),
        ServiceInfo(
            name='AEM Core WCM Components (GitHub)',
            url='https://github.com/adobe/aem-core-wcm-components',
            description='Standardized Web Content Management components for AEM',
            category='tools',
        ),
        ServiceInfo(
            name='ACS AEM Commons (GitHub)',
            url='https://github.com/Adobe-Consulting-Services/acs-aem-commons',
            description='ACS AEM Commons - Collection of reusable AEM components and utilities',
            category='tools',
        ),
        ServiceInfo(
            name='ACS AEM Commons Documentation',
            url='https://adobe-consulting-services.github.io/acs-aem-commons/',
            description='Official documentation for ACS AEM Commons library',
            category='tools',
        ),
        ServiceInfo(
            name='Netcentric AEM Tools (GitHub)',
            url='https://github.com/Netcentric',
            description='Netcentric open source AEM tools and frameworks',
            category='tools',
        ),
        ServiceInfo(
            name='AEM Multi-Tenant Demo (GitHub)',
            url='https://github.com/Netcentric/aem-multitenant-demo',
            description='Multi-tenancy implementation example for AEM',
            category='tools',
        ),
        ServiceInfo(
            name='Coral UI 3 Reference (AEM 6.5)',
            url='https://developer.adobe.com/experience-manager/reference-materials/6-5/coral-ui/coralui3/index.html',
            description='Coral UI 3 component library reference for AEM 6.5',
            category='tools',
        ),
        ServiceInfo(
            name='Apache Sling Models',
            url='https://sling.apache.org/documentation/bundles/models.html',
            description='Apache Sling Models documentation - AEM foundation framework',
            category='apis',
        ),
        ServiceInfo(
            name='Apache Sling Servlets',
            url='https://sling.apache.org/documentation/the-sling-engine/servlets.html',
            description='Apache Sling Servlets documentation for AEM development',
            category='apis',
        ),
        ServiceInfo(
            name='Apache Sling Eventing and Job Handling',
            url='https://sling.apache.org/documentation/bundles/apache-sling-eventing-and-job-handling.html',
            description='Event-driven programming and job handling in Sling/AEM',
            category='apis',
        ),
        ServiceInfo(
            name='adaptTo() 2025 Conference',
            url='https://adapt.to/2025/',
            description='adaptTo() conference - AEM developer community event',
            category='learning',
        ),
        ServiceInfo(
            name='adaptTo() 2025 Schedule',
            url='https://adapt.to/2025/schedule',
            description='Full schedule of adaptTo() 2025 conference sessions',
            category='learning',
        ),
        ServiceInfo(
            name='adaptTo() 2024 Schedule',
            url='https://adapt.to/2024/schedule',
            description='adaptTo() 2024 conference sessions and schedule',
            category='learning',
        ),
        ServiceInfo(
            name='adaptTo() 2023 Schedule',
            url='https://adapt.to/2023/schedule',
            description='adaptTo() 2023 conference sessions and schedule',
            category='learning',
        ),
        ServiceInfo(
            name='adaptTo() Historical Archives',
            url='https://adapt.to/2012/schedule',
            description='Historical adaptTo() conferences (2011-2019) - community archives',
            category='learning',
        ),
        ServiceInfo(
            name='Adobe Summit',
            url='https://business.adobe.com/summit/adobe-summit.html',
            description='Adobe Summit - The Digital Experience Conference',
            category='learning',
        ),
        ServiceInfo(
            name='Adobe Developers YouTube Channel',
            url='https://www.youtube.com/@AdobeDevelopers',
            description='Official Adobe Developers YouTube channel with tutorials and talks',
            category='learning',
        ),
        ServiceInfo(
            name='AEM User Group YouTube Channel',
            url='https://www.youtube.com/@adobeexperiencemanageruser7261',
            description='Adobe Experience Manager User Group community channel',
            category='learning',
        ),
    ]

    logger.info(f'Returning {len(services)} available AEM services')
    return services


def main():
    """Run the MCP server with CLI argument support."""
    logger.info('Starting Adobe AEM Documentation MCP Server')
    logger.info(f'Session UUID: {SESSION_UUID}')
    logger.info(f'User-Agent: {DEFAULT_USER_AGENT}')

    mcp.run()


if __name__ == '__main__':
    main()
