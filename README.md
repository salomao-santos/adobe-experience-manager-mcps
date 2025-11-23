# Adobe Experience Manager MCP Server

MCP (Model Context Protocol) server for extracting and converting Adobe Experience Manager (AEM) documentation to clean Markdown format for use by Large Language Models (LLMs).

## Overview

This MCP server provides a `read_aem_doc` tool that:

- Fetches AEM documentation pages using Playwright
- Extracts main content while filtering out navigation, headers, footers, and menus
- Converts HTML to clean, well-structured Markdown
- Returns content optimized for LLM consumption

## Features

- **Smart Content Extraction**: Automatically identifies and extracts main documentation content
- **Clean Markdown Output**: Converts HTML to readable Markdown format
- **Navigation Filtering**: Removes menus, footers, headers, and other non-content elements
- **AEM-Optimized**: Designed specifically for Adobe Experience Manager Cloud Service documentation
- **Async Support**: Built with async/await for efficient operation

## Installation

### Prerequisites

- Python 3.10 or higher
- pip or uv package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/salomao-santos/adobe-experience-manager-mcps.git
cd adobe-experience-manager-mcps
```

2. Install dependencies:
```bash
pip install -e .
```

3. Install Playwright browsers:
```bash
playwright install chromium
```

## Usage

### As an MCP Server

Configure your MCP client to use this server. Example configuration for Claude Desktop:

```json
{
  "mcpServers": {
    "aem-docs": {
      "command": "python",
      "args": ["-m", "aem_mcp.server"],
      "cwd": "/path/to/adobe-experience-manager-mcps/src"
    }
  }
}
```

### Standalone Usage

You can also run the server directly:

```bash
python -m aem_mcp.server
```

## Tool: read_aem_doc

Extract and convert AEM documentation to Markdown.

### Parameters

- `url` (string, required): The URL of the AEM documentation page to extract

### Example Usage

```python
# Via MCP protocol
{
  "tool": "read_aem_doc",
  "arguments": {
    "url": "https://experienceleague.adobe.com/docs/experience-manager-cloud-service/content/implementing/developing/full-stack/overview.html"
  }
}
```

### Supported Documentation Types

- Code quality rules
- Release notes
- Technical documentation
- API references
- Best practices guides
- Tutorial pages

## Examples

### Extract Release Notes

```python
read_aem_doc(url="https://experienceleague.adobe.com/docs/experience-manager-cloud-service/content/release-notes/release-notes/release-notes-current.html")
```

### Extract Code Quality Rules

```python
read_aem_doc(url="https://experienceleague.adobe.com/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/test-results/overview-test-results.html")
```

## How It Works

1. **Fetch**: Uses Playwright to navigate to the documentation URL and wait for content to load
2. **Parse**: BeautifulSoup parses the HTML content
3. **Extract**: Identifies and extracts main content area while removing:
   - Navigation menus
   - Headers and footers
   - Sidebars
   - Breadcrumbs
   - Scripts and styles
4. **Convert**: html2text converts clean HTML to well-formatted Markdown
5. **Clean**: Post-processes Markdown to remove excessive whitespace

## Development

### Running Tests

```bash
pytest
```

### Project Structure

```
adobe-experience-manager-mcps/
├── src/
│   └── aem_mcp/
│       ├── __init__.py
│       └── server.py          # Main MCP server implementation
├── tests/                      # Test files
├── pyproject.toml             # Project configuration
└── README.md
```

## Inspiration

This project is inspired by:
- Web scraping examples for documentation extraction
- AWS documentation MCP servers
- BeautifulSoup content extraction patterns

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub.