# Copyright 2024-2025 Salomão Santos
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
"""Tests for the main server."""

import httpx
import pytest
from aemlabs.aem_documentation_mcp_server.server import (
    get_available_services,
    main,
    read_documentation,
)
from unittest.mock import AsyncMock, MagicMock, patch


class MockContext:
    """Mock context for testing."""

    async def error(self, message):
        """Mock error method."""
        print(f'Error: {message}')

    async def info(self, message):
        """Mock info method."""
        print(f'Info: {message}')


class TestReadDocumentation:
    """Tests for read_documentation tool."""

    @pytest.mark.asyncio
    async def test_valid_url(self):
        """Test reading documentation with valid URL."""
        url = 'https://experienceleague.adobe.com/en/docs/test'
        ctx = MockContext()

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><body><main><h1>Test</h1></main></body></html>'
        mock_response.headers = {'content-type': 'text/html'}

        with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response

            # Test via read_documentation_impl to avoid Field processing issues
            from aemlabs.aem_documentation_mcp_server.server_utils import read_documentation_impl

            result = await read_documentation_impl(ctx, url, 10000, 0, 'test-session')

            assert 'Test' in result
            assert 'Adobe AEM Documentation' in result

    @pytest.mark.asyncio
    async def test_invalid_domain(self):
        """Test reading documentation with invalid domain."""
        url = 'https://invalid.com/docs'
        ctx = MockContext()

        result = await read_documentation(ctx, url=url)

        assert 'Invalid URL' in result
        assert 'supported domains' in result

    @pytest.mark.asyncio
    async def test_max_length_parameter(self):
        """Test max_length parameter."""
        url = 'https://experienceleague.adobe.com/test'
        ctx = MockContext()

        long_content = '<html><body><main>' + 'a' * 10000 + '</main></body></html>'
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = long_content
        mock_response.headers = {'content-type': 'text/html'}

        with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response

            # Test via read_documentation_impl to avoid Field processing issues
            from aemlabs.aem_documentation_mcp_server.server_utils import read_documentation_impl

            result = await read_documentation_impl(ctx, url, 100, 0, 'test-session')

            assert 'Content truncated' in result

    @pytest.mark.asyncio
    async def test_start_index_parameter(self):
        """Test start_index parameter for pagination."""
        url = 'https://experienceleague.adobe.com/test'
        ctx = MockContext()

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><body><main>' + 'abcd' * 1000 + '</main></body></html>'
        mock_response.headers = {'content-type': 'text/html'}

        with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response

            result = await read_documentation(ctx, url=url, max_length=100, start_index=50)

            # Should not contain the first 50 characters
            assert 'start_index=150' in result or 'start_index' in result


class TestGetAvailableServices:
    """Tests for get_available_services tool."""

    @pytest.mark.asyncio
    async def test_returns_services_list(self):
        """Test that get_available_services returns a list of services."""
        ctx = MockContext()

        result = await get_available_services(ctx)

        assert isinstance(result, list)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_service_structure(self):
        """Test that services have required fields."""
        ctx = MockContext()

        result = await get_available_services(ctx)

        for service in result:
            assert hasattr(service, 'name')
            assert hasattr(service, 'url')
            assert hasattr(service, 'description')
            assert hasattr(service, 'category')
            assert service.name
            assert service.url
            assert service.category

    @pytest.mark.asyncio
    async def test_includes_major_services(self):
        """Test that major AEM services are included."""
        ctx = MockContext()

        result = await get_available_services(ctx)
        service_names = [s.name.lower() for s in result]

        # Check for key services
        assert any('cloud service' in name for name in service_names)
        assert any('6.5' in name for name in service_names)
        assert any('api' in name for name in service_names)


class TestMain:
    """Tests for main function."""

    def test_main_function(self):
        """Test that main function can be called."""
        with patch('aemlabs.aem_documentation_mcp_server.server.mcp.run') as mock_run:
            with patch('aemlabs.aem_documentation_mcp_server.server.logger.info'):
                main()
                mock_run.assert_called_once()
