# Adobe Experience Manager MCP Server

Model Context Protocol (MCP) server for Adobe Experience Manager (AEM) that extracts documentation from Experience League and transforms HTML into clean Markdown for LLM consumption.

## Overview

This MCP server provides tools to scrape and process Adobe Experience Manager documentation from Experience League, converting it into clean, structured Markdown format suitable for use by Large Language Models.

## Features

- **Web Scraping**: Uses Playwright to handle dynamic content and JavaScript-rendered pages
- **Content Extraction**: Intelligently identifies and extracts main documentation content
- **Noise Filtering**: Removes navigation menus, headers, footers, and other non-content elements
- **HTML to Markdown**: Converts extracted HTML to clean, readable Markdown format
- **LLM-Ready**: Outputs structured content optimized for LLM consumption

## Installation

```bash
# Clone the repository
git clone https://github.com/salomao-santos/adobe-experience-manager-mcps.git
cd adobe-experience-manager-mcps

# Install dependencies
pip install -e .

# Install Playwright browsers
playwright install chromium
```

## Usage

### As an MCP Server

The server can be used with any MCP client. Add it to your MCP client configuration:

```json
{
  "mcpServers": {
    "adobe-aem": {
      "command": "python",
      "args": ["-m", "adobe_experience_manager_mcps.server"]
    }
  }
}
```

### Available Tools

#### `read_aem_doc`

Extracts documentation from an Experience League URL and converts it to Markdown.

**Parameters:**
- `url` (string, required): The Experience League documentation URL

**Example:**
```json
{
  "name": "read_aem_doc",
  "arguments": {
    "url": "https://experienceleague.adobe.com/docs/experience-manager-cloud-service/content/release-notes/release-notes/release-notes-current.html"
  }
}
```

**Returns:**
Clean Markdown content with:
- Main documentation text
- Code snippets
- Tables and lists
- Relevant links and images
- No navigation or UI elements

## Use Cases

- Extract AEM Cloud Service release notes
- Retrieve code quality rules and best practices
- Access API documentation and guides
- Process migration guides and tutorials
- Gather troubleshooting information

## Technical Details

### Content Extraction Strategy

1. **Page Loading**: Uses Playwright to load the page and wait for dynamic content
2. **Content Identification**: Searches for main content using common selectors (`main`, `article`, `[role="main"]`, etc.)
3. **Noise Removal**: Removes `nav`, `header`, `footer`, `sidebar`, and other non-content elements
4. **HTML to Markdown**: Converts cleaned HTML using `html2text` with optimized settings
5. **Post-processing**: Removes excessive whitespace and normalizes formatting

### Dependencies

- **mcp**: Model Context Protocol SDK
- **playwright**: Browser automation for handling dynamic content
- **beautifulsoup4**: HTML parsing and manipulation
- **html2text**: HTML to Markdown conversion
- **lxml**: Fast XML/HTML parsing

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run the server directly
python -m adobe_experience_manager_mcps.server
```

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.