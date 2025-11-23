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
"""Tests for utility functions."""

import pytest
from adobelabs.aem_documentation_mcp_server.util import (
    extract_content_from_html,
    extract_page_title,
    format_documentation_result,
    is_html_content,
)


class TestExtractContentFromHtml:
    """Tests for extract_content_from_html function."""

    def test_empty_html(self):
        """Test with empty HTML."""
        result = extract_content_from_html('')
        assert '<e>Empty HTML content</e>' in result

    def test_simple_html(self):
        """Test with simple HTML."""
        html = '<html><body><main><h1>Test</h1><p>Content</p></main></body></html>'
        result = extract_content_from_html(html)
        assert 'Test' in result
        assert 'Content' in result

    def test_html_with_navigation(self):
        """Test that navigation elements are removed."""
        html = '''
        <html><body>
            <nav>Navigation</nav>
            <header>Header</header>
            <main><h1>Main Content</h1></main>
            <footer>Footer</footer>
        </body></html>
        '''
        result = extract_content_from_html(html)
        assert 'Main Content' in result
        assert 'Navigation' not in result
        assert 'Header' not in result
        assert 'Footer' not in result

    def test_adobe_specific_selectors(self):
        """Test Adobe-specific content selectors."""
        html = '''
        <html><body>
            <div class="article-content">
                <h1>Article Title</h1>
                <p>Article content here</p>
            </div>
        </body></html>
        '''
        result = extract_content_from_html(html)
        assert 'Article Title' in result
        assert 'Article content here' in result

    def test_error_handling(self):
        """Test error handling for invalid HTML."""
        result = extract_content_from_html(None)
        assert '<e>Empty HTML content</e>' in result


class TestIsHtmlContent:
    """Tests for is_html_content function."""

    def test_html_content_with_html_tag(self):
        """Test HTML detection with <html> tag."""
        assert is_html_content('<html><body>test</body></html>', 'text/html')

    def test_html_content_with_content_type(self):
        """Test HTML detection with content-type header."""
        assert is_html_content('test content', 'text/html; charset=utf-8')

    def test_non_html_content(self):
        """Test non-HTML content."""
        assert is_html_content('plain text', 'text/plain') is False

    def test_empty_content_type(self):
        """Test with empty content-type (defaults to HTML)."""
        assert is_html_content('test', '')


class TestFormatDocumentationResult:
    """Tests for format_documentation_result function."""

    def test_basic_formatting(self):
        """Test basic formatting without truncation."""
        content = 'Short content'
        result, is_truncated = format_documentation_result(
            'https://example.com', content, 0, 1000
        )
        assert 'Adobe AEM Documentation from https://example.com' in result
        assert 'Short content' in result
        assert is_truncated is False

    def test_truncation(self):
        """Test content truncation."""
        content = 'a' * 10000
        result, is_truncated = format_documentation_result(
            'https://example.com', content, 0, 100
        )
        assert len(result) < len(content)
        assert 'start_index=100' in result
        assert is_truncated is True

    def test_start_index(self):
        """Test pagination with start_index."""
        content = 'abcdefghij' * 100
        result, is_truncated = format_documentation_result(
            'https://example.com', content, 50, 50
        )
        assert 'start_index=100' in result
        assert is_truncated is True

    def test_start_index_beyond_content(self):
        """Test start_index beyond content length."""
        content = 'Short'
        result, is_truncated = format_documentation_result(
            'https://example.com', content, 100, 100
        )
        assert 'No more content available' in result
        assert is_truncated is False


class TestExtractPageTitle:
    """Tests for extract_page_title function."""

    def test_extract_from_title_tag(self):
        """Test extracting title from <title> tag."""
        html = '<html><head><title>Page Title</title></head><body></body></html>'
        assert extract_page_title(html) == 'Page Title'

    def test_extract_from_h1(self):
        """Test extracting title from <h1> tag."""
        html = '<html><body><h1>Heading Title</h1></body></html>'
        assert extract_page_title(html) == 'Heading Title'

    def test_extract_from_og_title(self):
        """Test extracting title from og:title meta tag."""
        html = '''
        <html>
            <head><meta property="og:title" content="OG Title" /></head>
            <body></body>
        </html>
        '''
        assert extract_page_title(html) == 'OG Title'

    def test_no_title_found(self):
        """Test when no title is found."""
        html = '<html><body><p>No title here</p></body></html>'
        assert extract_page_title(html) is None

    def test_error_handling(self):
        """Test error handling for invalid HTML."""
        assert extract_page_title(None) is None
