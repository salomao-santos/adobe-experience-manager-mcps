"""Tests for the AEM MCP server."""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from adobe_experience_manager_mcps.server import read_aem_doc


@pytest.mark.asyncio
async def test_read_aem_doc_extracts_main_content():
    """Test that read_aem_doc extracts main content and converts to markdown."""
    
    # Mock HTML content similar to Experience League
    mock_html = """
    <html>
        <head><title>Test Page</title></head>
        <body>
            <nav class="navigation">
                <ul><li>Menu 1</li><li>Menu 2</li></ul>
            </nav>
            <header>
                <h1>Header content</h1>
            </header>
            <main>
                <h1>Introduction to AEM Cloud Service</h1>
                <p>Adobe Experience Manager as a Cloud Service provides the latest capabilities.</p>
                <h2>Key Features</h2>
                <ul>
                    <li>Scalable architecture</li>
                    <li>Continuous updates</li>
                    <li>Cloud-native</li>
                </ul>
                <pre><code>// Example code
aem.service.init();</code></pre>
            </main>
            <footer>
                <p>Footer content</p>
            </footer>
        </body>
    </html>
    """
    
    # Mock Playwright browser and page
    mock_page = AsyncMock()
    mock_page.goto = AsyncMock()
    mock_page.wait_for_selector = AsyncMock()
    mock_page.content = AsyncMock(return_value=mock_html)
    mock_page.close = AsyncMock()
    
    mock_browser = AsyncMock()
    mock_browser.new_page = AsyncMock(return_value=mock_page)
    
    # Patch the get_browser function
    with patch('adobe_experience_manager_mcps.server.get_browser', return_value=mock_browser):
        result = await read_aem_doc("https://experienceleague.adobe.com/docs/test")
        
        # Verify the result contains main content
        assert "Introduction to AEM Cloud Service" in result
        assert "Adobe Experience Manager as a Cloud Service" in result
        assert "Key Features" in result
        assert "Scalable architecture" in result
        
        # Verify navigation and footer are not included
        assert "Menu 1" not in result
        assert "Footer content" not in result
        
        # Verify markdown formatting
        assert "#" in result  # Headers should be converted
        assert "*" in result or "-" in result  # List items
        
        # Verify page was closed
        mock_page.close.assert_called_once()


@pytest.mark.asyncio
async def test_read_aem_doc_handles_missing_main_content():
    """Test that read_aem_doc handles pages without explicit main content."""
    
    mock_html = """
    <html>
        <body>
            <div class="content">
                <h1>Documentation</h1>
                <p>This is some documentation content.</p>
            </div>
        </body>
    </html>
    """
    
    mock_page = AsyncMock()
    mock_page.goto = AsyncMock()
    mock_page.wait_for_selector = AsyncMock(side_effect=Exception("Selector not found"))
    mock_page.content = AsyncMock(return_value=mock_html)
    mock_page.close = AsyncMock()
    
    mock_browser = AsyncMock()
    mock_browser.new_page = AsyncMock(return_value=mock_page)
    
    with patch('adobe_experience_manager_mcps.server.get_browser', return_value=mock_browser):
        result = await read_aem_doc("https://experienceleague.adobe.com/docs/test")
        
        # Should still extract content from body
        assert "Documentation" in result
        assert "some documentation content" in result


@pytest.mark.asyncio
async def test_read_aem_doc_validates_url():
    """Test that read_aem_doc warns for non-Adobe URLs."""
    
    mock_html = "<html><body><main><p>Content</p></main></body></html>"
    
    mock_page = AsyncMock()
    mock_page.goto = AsyncMock()
    mock_page.wait_for_selector = AsyncMock()
    mock_page.content = AsyncMock(return_value=mock_html)
    mock_page.close = AsyncMock()
    
    mock_browser = AsyncMock()
    mock_browser.new_page = AsyncMock(return_value=mock_page)
    
    with patch('adobe_experience_manager_mcps.server.get_browser', return_value=mock_browser):
        # Should not raise an error, just log a warning
        result = await read_aem_doc("https://example.com/docs/test")
        assert "Content" in result


@pytest.mark.asyncio  
async def test_read_aem_doc_cleans_whitespace():
    """Test that read_aem_doc removes excessive whitespace."""
    
    mock_html = """
    <html>
        <body>
            <main>
                <p>Line 1</p>
                
                
                
                <p>Line 2</p>
            </main>
        </body>
    </html>
    """
    
    mock_page = AsyncMock()
    mock_page.goto = AsyncMock()
    mock_page.wait_for_selector = AsyncMock()
    mock_page.content = AsyncMock(return_value=mock_html)
    mock_page.close = AsyncMock()
    
    mock_browser = AsyncMock()
    mock_browser.new_page = AsyncMock(return_value=mock_page)
    
    with patch('adobe_experience_manager_mcps.server.get_browser', return_value=mock_browser):
        result = await read_aem_doc("https://experienceleague.adobe.com/docs/test")
        
        # Should not have more than 2 consecutive newlines
        assert "\n\n\n" not in result
