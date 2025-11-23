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
"""Search utilities for Adobe Experience League."""

from typing import List, Optional
from urllib.parse import quote_plus


def build_experience_league_search_url(
    query: str,
    content_types: Optional[List[str]] = None,
    products: Optional[List[str]] = None,
    roles: Optional[List[str]] = None,
) -> str:
    """Build an Adobe Experience League search URL with filters.

    Args:
        query: Search query string
        content_types: List of content types to filter (e.g., ['Documentation', 'Tutorial'])
        products: List of products to filter (e.g., ['Experience Manager', 'Experience Cloud'])
        roles: List of roles to filter (e.g., ['Developer', 'Admin', 'User'])

    Returns:
        Complete search URL for Experience League

    Examples:
        >>> build_experience_league_search_url('test', content_types=['Documentation'])
        'https://experienceleague.adobe.com/en/search#q=test&f-el_contenttype=Documentation'

        >>> build_experience_league_search_url(
        ...     'models',
        ...     content_types=['Documentation'],
        ...     products=['Experience Manager'],
        ...     roles=['Developer']
        ... )
        'https://experienceleague.adobe.com/en/search#q=models&f-el_contenttype=Documentation&f-el_product=Experience%20Manager&f-el_role=Developer'
    """
    # Base URL
    base_url = 'https://experienceleague.adobe.com/en/search#'
    
    # Build hash parameters
    params = []
    
    # Add search query
    params.append(f'q={quote_plus(query)}')
    
    # Add content type filters
    if content_types:
        content_type_str = ','.join(content_types)
        params.append(f'f-el_contenttype={quote_plus(content_type_str)}')
    
    # Add product filters
    if products:
        product_str = ','.join(products)
        params.append(f'f-el_product={quote_plus(product_str)}')
    
    # Add role filters
    if roles:
        role_str = ','.join(roles)
        params.append(f'f-el_role={quote_plus(role_str)}')
    
    return base_url + '&'.join(params)


# Predefined product lists for common searches
EXPERIENCE_MANAGER_PRODUCTS = [
    'Experience Manager',
    'Experience Manager|6.5',
    'Experience Manager|6.5 LTS',
    'Experience Manager|as a Cloud Service',
    'Experience Manager|Assets',
    'Experience Manager|Forms',
    'Experience Manager|Screens',
    'Experience Manager|Sites',
]

ALL_PRODUCTS = [
    'Experience Cloud',
    'Experience Cloud Services',
] + EXPERIENCE_MANAGER_PRODUCTS


# Predefined content types
CONTENT_TYPES = [
    'Documentation',
    'Tutorial',
    'Troubleshooting',
    'API Reference',
    'Release Notes',
    'Best Practices',
]


# Predefined roles
ROLES = [
    'Developer',
    'Admin',
    'Leader',
    'User',
    'Architect',
    'Business Practitioner',
]
