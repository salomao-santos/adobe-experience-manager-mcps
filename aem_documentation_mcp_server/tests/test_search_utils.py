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
"""Tests for search utilities."""

import pytest
from aemlabs.aem_documentation_mcp_server.search_utils import (
    build_experience_league_search_url,
    EXPERIENCE_MANAGER_PRODUCTS,
    ALL_PRODUCTS,
    CONTENT_TYPES,
    ROLES,
)


class TestBuildExperienceLeagueSearchUrl:
    """Tests for build_experience_league_search_url function."""

    def test_simple_search(self):
        """Test building a simple search URL."""
        url = build_experience_league_search_url('test')
        assert url == 'https://experienceleague.adobe.com/en/search#q=test'

    def test_search_with_content_type(self):
        """Test building search URL with content type filter."""
        url = build_experience_league_search_url('test', content_types=['Documentation'])
        assert url == 'https://experienceleague.adobe.com/en/search#q=test&f-el_contenttype=Documentation'

    def test_search_with_multiple_content_types(self):
        """Test building search URL with multiple content type filters."""
        url = build_experience_league_search_url('test', content_types=['Documentation', 'Tutorial'])
        assert 'q=test' in url
        assert 'f-el_contenttype=Documentation%2CTutorial' in url

    def test_search_with_product(self):
        """Test building search URL with product filter."""
        url = build_experience_league_search_url('test', products=['Experience Manager'])
        assert 'q=test' in url
        assert 'f-el_product=Experience+Manager' in url

    def test_search_with_multiple_products(self):
        """Test building search URL with multiple product filters."""
        url = build_experience_league_search_url(
            'test',
            products=['Experience Manager', 'Experience Manager|as a Cloud Service']
        )
        assert 'q=test' in url
        assert 'Experience+Manager' in url
        assert 'as+a+Cloud+Service' in url

    def test_search_with_role(self):
        """Test building search URL with role filter."""
        url = build_experience_league_search_url('test', roles=['Developer'])
        assert 'q=test' in url
        assert 'f-el_role=Developer' in url

    def test_search_with_multiple_roles(self):
        """Test building search URL with multiple role filters."""
        url = build_experience_league_search_url('test', roles=['Developer', 'Admin'])
        assert 'q=test' in url
        assert 'f-el_role=Developer%2CAdmin' in url

    def test_search_with_all_filters(self):
        """Test building search URL with all filters."""
        url = build_experience_league_search_url(
            query='models',
            content_types=['Documentation'],
            products=['Experience Manager'],
            roles=['Developer']
        )
        assert 'q=models' in url
        assert 'f-el_contenttype=Documentation' in url
        assert 'f-el_product=Experience+Manager' in url
        assert 'f-el_role=Developer' in url

    def test_search_with_special_characters(self):
        """Test building search URL with special characters in query."""
        url = build_experience_league_search_url('sling & models')
        assert 'sling+%26+models' in url

    def test_search_with_empty_filters(self):
        """Test building search URL with empty filter lists."""
        url = build_experience_league_search_url('test', content_types=[], products=[], roles=[])
        assert url == 'https://experienceleague.adobe.com/en/search#q=test'


class TestPredefinedLists:
    """Tests for predefined constants."""

    def test_experience_manager_products_list(self):
        """Test EXPERIENCE_MANAGER_PRODUCTS contains expected items."""
        assert 'Experience Manager' in EXPERIENCE_MANAGER_PRODUCTS
        assert 'Experience Manager|6.5' in EXPERIENCE_MANAGER_PRODUCTS
        assert 'Experience Manager|as a Cloud Service' in EXPERIENCE_MANAGER_PRODUCTS
        assert len(EXPERIENCE_MANAGER_PRODUCTS) >= 8

    def test_all_products_list(self):
        """Test ALL_PRODUCTS includes Experience Cloud."""
        assert 'Experience Cloud' in ALL_PRODUCTS
        assert 'Experience Manager' in ALL_PRODUCTS
        assert len(ALL_PRODUCTS) > len(EXPERIENCE_MANAGER_PRODUCTS)

    def test_content_types_list(self):
        """Test CONTENT_TYPES contains expected items."""
        assert 'Documentation' in CONTENT_TYPES
        assert 'Tutorial' in CONTENT_TYPES
        assert 'Troubleshooting' in CONTENT_TYPES
        assert len(CONTENT_TYPES) >= 6

    def test_roles_list(self):
        """Test ROLES contains expected items."""
        assert 'Developer' in ROLES
        assert 'Admin' in ROLES
        assert 'User' in ROLES
        assert len(ROLES) >= 6
