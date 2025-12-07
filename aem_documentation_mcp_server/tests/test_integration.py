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

"""Additional integration tests for coverage."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from aemlabs.aem_documentation_mcp_server.server import (
    search_experience_league,
)
from aemlabs.aem_documentation_mcp_server.server_utils import (
    read_documentation_impl,
)


class MockContext:
    """Mock context for testing."""
    
    async def info(self, message: str):
        """Mock info logging."""
        print(f'Info: {message}')
    
    async def debug(self, message: str):
        """Mock debug logging."""
        print(f'Debug: {message}')
    
    async def error(self, message: str):
        """Mock error logging."""
        print(f'Error: {message}')


class TestYouTubeIntegration:
    """Integration tests for YouTube URL handling."""

    @pytest.mark.asyncio
    async def test_youtube_url_full_flow(self):
        """Test complete YouTube URL handling flow."""
        ctx = MockContext()
        url = 'https://www.youtube.com/watch?v=TEST123'
        
        result = await read_documentation_impl(ctx, url, 10000, 0, 'session-1')
        
        assert 'YouTube Video' in result
        assert 'TEST123' in result
        assert 'transcript' in result.lower()


class TestPDFIntegration:
    """Integration tests for PDF handling."""

    @pytest.mark.asyncio
    async def test_regular_pdf_handling(self):
        """Test regular PDF file handling."""
        ctx = MockContext()
        url = 'https://example.com/document.pdf'
        
        result = await read_documentation_impl(ctx, url, 10000, 0, 'session-1')
        
        assert 'PDF Document' in result
        assert 'document.pdf' in result
        assert 'Download' in result or 'download' in result

    @pytest.mark.asyncio
    async def test_adaptto_pdf_handling(self):
        """Test adaptTo() presentation PDF handling."""
        ctx = MockContext()
        url = 'https://adapt.to/2025/presentations/my-talk.pdf'
        
        result = await read_documentation_impl(ctx, url, 10000, 0, 'session-1')
        
        assert 'PDF Document' in result
        assert 'adaptTo() Presentation' in result
        assert 'my-talk.pdf' in result


class TestSearchIntegration:
    """Integration tests for search functionality."""

    @pytest.mark.asyncio
    async def test_search_with_all_parameters(self):
        """Test search with all filter parameters."""
        ctx = MockContext()
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><body><div class="search-results">Results</div></body></html>'
        mock_response.headers = {'content-type': 'text/html'}
        
        with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response
            
            result = await search_experience_league(
                ctx,
                query='components',
                content_types=['Documentation', 'Tutorial'],
                products=['Experience Manager'],
                roles=['Developer']
            )
            
            assert mock_get.called
            called_url = mock_get.call_args[0][0]
            assert 'components' in called_url.lower()


class TestErrorHandling:
    """Integration tests for error handling."""

    @pytest.mark.asyncio
    async def test_network_timeout(self):
        """Test handling of network timeout."""
        ctx = MockContext()
        url = 'https://experienceleague.adobe.com/test.html'
        
        with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
            import httpx
            mock_get.side_effect = httpx.TimeoutException('Request timeout')
            
            result = await read_documentation_impl(ctx, url, 10000, 0, 'session-1')
            
            assert 'Failed to fetch' in result or 'error' in result.lower()

    @pytest.mark.asyncio
    async def test_connection_error(self):
        """Test handling of connection errors."""
        ctx = MockContext()
        url = 'https://experienceleague.adobe.com/test.html'
        
        with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
            import httpx
            mock_get.side_effect = httpx.ConnectError('Connection refused')
            
            result = await read_documentation_impl(ctx, url, 10000, 0, 'session-1')
            
            assert 'Failed to fetch' in result or 'error' in result.lower()
