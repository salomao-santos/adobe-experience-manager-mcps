"""Tests for AEM MCP Server."""

import pytest
from bs4 import BeautifulSoup
from aem_mcp.server import extract_main_content, html_to_markdown


def test_extract_main_content_removes_nav():
    """Test that navigation elements are removed."""
    html = """
    <html>
        <body>
            <nav>Navigation menu</nav>
            <header>Header</header>
            <main>
                <h1>Main Content</h1>
                <p>This is the main content.</p>
            </main>
            <footer>Footer</footer>
        </body>
    </html>
    """
    soup = BeautifulSoup(html, 'lxml')
    result = extract_main_content(soup)
    
    # Check that main content is present
    assert 'Main Content' in str(result)
    assert 'This is the main content' in str(result)
    
    # Check that navigation elements are removed
    assert 'Navigation menu' not in str(result)
    assert '<nav>' not in str(result)
    assert '<header>' not in str(result)
    assert '<footer>' not in str(result)


def test_extract_main_content_finds_article():
    """Test that article element is found as main content."""
    html = """
    <html>
        <body>
            <nav>Nav</nav>
            <article>
                <h1>Article Title</h1>
                <p>Article content.</p>
            </article>
            <footer>Footer</footer>
        </body>
    </html>
    """
    soup = BeautifulSoup(html, 'lxml')
    result = extract_main_content(soup)
    
    assert 'Article Title' in str(result)
    assert 'Article content' in str(result)
    assert 'Nav' not in str(result)


def test_html_to_markdown_basic():
    """Test basic HTML to Markdown conversion."""
    html = """
    <h1>Title</h1>
    <p>A paragraph with <strong>bold</strong> and <em>italic</em> text.</p>
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
    </ul>
    """
    markdown = html_to_markdown(html)
    
    # Check for expected Markdown elements
    assert '# Title' in markdown
    assert '**bold**' in markdown or 'bold' in markdown
    assert '*italic*' in markdown or 'italic' in markdown
    assert '* Item 1' in markdown or '- Item 1' in markdown


def test_html_to_markdown_preserves_code():
    """Test that code blocks are preserved."""
    html = """
    <p>Here is some code:</p>
    <pre><code>function test() {
        return true;
    }</code></pre>
    """
    markdown = html_to_markdown(html)
    
    assert 'function test()' in markdown
    assert 'return true' in markdown


def test_html_to_markdown_handles_links():
    """Test that links are converted properly."""
    html = '<p>Check out <a href="https://example.com">this link</a>.</p>'
    markdown = html_to_markdown(html)
    
    assert 'this link' in markdown
    assert 'https://example.com' in markdown


def test_html_to_markdown_cleans_whitespace():
    """Test that excessive whitespace is cleaned up."""
    html = """
    <h1>Title</h1>
    
    
    
    <p>Paragraph</p>
    """
    markdown = html_to_markdown(html)
    
    # Should not have more than 2 consecutive newlines
    assert '\n\n\n' not in markdown
