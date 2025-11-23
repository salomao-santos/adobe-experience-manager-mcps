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
"""Tests for server utilities."""

import httpx
import pytest
from adobelabs.aem_documentation_mcp_server.server_utils import (
    read_documentation_impl,
    validate_adobe_url,
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


class TestValidateAdobeUrl:
    """Tests for validate_adobe_url function."""

    def test_valid_experienceleague_url(self):
        """Test valid experienceleague.adobe.com URL."""
        url = 'https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service'
        is_valid, error_msg = validate_adobe_url(url)
        assert is_valid is True
        assert error_msg is None

    def test_valid_developer_url(self):
        """Test valid developer.adobe.com URL."""
        url = 'https://developer.adobe.com/experience-cloud/experience-manager-apis/'
        is_valid, error_msg = validate_adobe_url(url)
        assert is_valid is True
        assert error_msg is None

    def test_valid_helpx_url(self):
        """Test valid helpx.adobe.com URL."""
        url = 'https://helpx.adobe.com/experience-manager/kb/index.html'
        is_valid, error_msg = validate_adobe_url(url)
        assert is_valid is True
        assert error_msg is None

    def test_valid_docs_url(self):
        """Test valid docs.adobe.com URL."""
        url = 'https://docs.adobe.com/content/help/en/experience-manager.html'
        is_valid, error_msg = validate_adobe_url(url)
        assert is_valid is True
        assert error_msg is None

    def test_valid_github_adobe_url(self):
        """Test valid github.com/adobe URL."""
        url = 'https://github.com/adobe/aem-project-archetype'
        is_valid, error_msg = validate_adobe_url(url)
        assert is_valid is True
        assert error_msg is None

    def test_valid_sling_url(self):
        """Test valid sling.apache.org URL."""
        url = 'https://sling.apache.org/documentation/bundles/models.html'
        is_valid, error_msg = validate_adobe_url(url)
        assert is_valid is True
        assert error_msg is None

    def test_valid_adaptto_url(self):
        """Test valid adapt.to URL."""
        url = 'https://adapt.to/2025/schedule'
        is_valid, error_msg = validate_adobe_url(url)
        assert is_valid is True
        assert error_msg is None

    def test_valid_youtube_url(self):
        """Test valid youtube.com URL."""
        url = 'https://www.youtube.com/watch?v=nJ8QTNQEkD8'
        is_valid, error_msg = validate_adobe_url(url)
        assert is_valid is True
        assert error_msg is None

    def test_valid_youtu_be_url(self):
        """Test valid youtu.be URL."""
        url = 'https://youtu.be/nJ8QTNQEkD8'
        is_valid, error_msg = validate_adobe_url(url)
        assert is_valid is True
        assert error_msg is None

    def test_valid_business_adobe_url(self):
        """Test valid business.adobe.com URL."""
        url = 'https://business.adobe.com/summit/2025.html'
        is_valid, error_msg = validate_adobe_url(url)
        assert is_valid is True
        assert error_msg is None

    def test_invalid_github_non_adobe_url(self):
        """Test invalid github.com URL (not adobe org)."""
        url = 'https://github.com/other-org/some-repo'
        is_valid, error_msg = validate_adobe_url(url)
        assert is_valid is False
        assert 'Invalid URL' in error_msg

    def test_invalid_domain(self):
        """Test invalid domain."""
        url = 'https://example.com/docs'
        is_valid, error_msg = validate_adobe_url(url)
        assert is_valid is False
        assert 'Invalid URL' in error_msg
        assert 'supported domains' in error_msg

    def test_http_protocol(self):
        """Test HTTP protocol (should work)."""
        url = 'http://experienceleague.adobe.com/docs'
        is_valid, error_msg = validate_adobe_url(url)
        assert is_valid is True
        assert error_msg is None


class TestReadDocumentationImpl:
    """Tests for read_documentation_impl function."""

    @pytest.mark.asyncio
    async def test_successful_fetch(self):
        """Test successful document fetch."""
        url = 'https://experienceleague.adobe.com/test.html'
        ctx = MockContext()

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><body><main><h1>Test</h1><p>Content</p></main></body></html>'
        mock_response.headers = {'content-type': 'text/html'}

        with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response

            result = await read_documentation_impl(ctx, url, 10000, 0, 'test-session')

            assert 'Adobe AEM Documentation from' in result
            assert 'Test' in result
            assert 'Content' in result
            mock_get.assert_called_once()

    @pytest.mark.asyncio
    async def test_http_error(self):
        """Test HTTP error handling."""
        url = 'https://experienceleague.adobe.com/test.html'
        ctx = MockContext()

        with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
            mock_get.side_effect = httpx.HTTPError('Connection error')

            result = await read_documentation_impl(ctx, url, 10000, 0, 'test-session')

            assert 'Failed to fetch' in result
            assert 'Connection error' in result

    @pytest.mark.asyncio
    async def test_404_error(self):
        """Test 404 status code."""
        url = 'https://experienceleague.adobe.com/test.html'
        ctx = MockContext()

        mock_response = MagicMock()
        mock_response.status_code = 404

        with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response

            result = await read_documentation_impl(ctx, url, 10000, 0, 'test-session')

            assert 'Failed to fetch' in result
            assert 'status code 404' in result

    @pytest.mark.asyncio
    async def test_url_with_hash_fragment(self):
        """Test URL with hash fragment (should be removed)."""
        url = 'https://experienceleague.adobe.com/test.html#section'
        ctx = MockContext()

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><body><main>Content</main></body></html>'
        mock_response.headers = {'content-type': 'text/html'}

        with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response

            await read_documentation_impl(ctx, url, 10000, 0, 'test-session')

            # Verify that the hash was removed from the request
            called_url = mock_get.call_args[0][0]
            assert '#section' not in called_url
            assert 'test.html' in called_url

    @pytest.mark.asyncio
    async def test_pagination(self):
        """Test content pagination."""
        url = 'https://experienceleague.adobe.com/test.html'
        ctx = MockContext()

        long_content = '<html><body><main>' + 'a' * 10000 + '</main></body></html>'
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = long_content
        mock_response.headers = {'content-type': 'text/html'}

        with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response

            result = await read_documentation_impl(ctx, url, 100, 0, 'test-session')

            assert 'Content truncated' in result
            assert 'start_index=100' in result
