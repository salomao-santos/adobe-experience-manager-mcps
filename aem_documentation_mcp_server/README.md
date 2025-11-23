# Adobe Experience Manager (AEM) Documentation MCP Server

Model Context Protocol (MCP) server for Adobe Experience Manager (AEM) Documentation

This MCP server provides tools to access Adobe AEM documentation and related resources from the AEM ecosystem, converting them to markdown format.

## Features

- **Search Experience League**: Search Adobe documentation with advanced filters (content type, products, roles)
- **Read Documentation**: Fetch and convert documentation pages to markdown format from:
  - Adobe Official Documentation (Experience League, Developer, HelpX, Docs)
  - GitHub repositories (any organization: Adobe, ACS, Netcentric, etc.)
  - GitHub Pages (*.github.io documentation sites)
  - Apache Sling documentation
  - adaptTo() conference resources (all years: 2011-2025+, including PDFs)
  - YouTube videos (with transcript guidance)
  - Adobe Business sites (Summit, etc.)
- **Get Available Services**: Get a curated list of 30+ AEM services and documentation areas
- **Hash Fragment Support**: Preserves URL fragments for search pages and adaptTo() schedules (#day-1, #day-2, etc.)
- **PDF Detection**: Identifies PDF documents and provides download guidance

## Prerequisites

### Installation Requirements

1. Install `uv` from [Astral](https://docs.astral.sh/uv/getting-started/installation/) or the [GitHub README](https://github.com/astral-sh/uv#installation)
2. Install Python 3.10 or newer using `uv python install 3.10` (or a more recent version)

## Installation

You can run the MCP server using either **UVX** (recommended) or **Docker**. Choose the method that best fits your environment.

### Option 1: Using UVX (Recommended)

Configure the MCP server in your MCP client configuration:

```json
{
  "mcpServers": {
    "aem-documentation-uvx": {
      "command": "uvx",
      "args": ["aemlabs.aem-documentation-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

**Prerequisites for UVX:**
- Install `uv` from [Astral](https://docs.astral.sh/uv/getting-started/installation/)
- Python 3.10+ (installed via `uv python install 3.10`)

### Option 2: Using Docker

First, build the Docker image:

```bash
cd aem_documentation_mcp_server
docker build -t aem-docs-mcp-server:latest .
```

Then configure the MCP server:

```json
{
  "mcpServers": {
    "aem-documentation-docker": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "aem-docs-mcp-server:latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

**Prerequisites for Docker:**
- Docker installed and running

### Switching Between UVX and Docker

To switch between modes, set `"disabled": true` on the mode you don't want to use and `"disabled": false` on the one you want to activate.

### Development Installation

Clone the repository and install in development mode:

```bash
cd aem_documentation_mcp_server
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FASTMCP_LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) | `WARNING` |
| `MCP_USER_AGENT` | Custom User-Agent string for HTTP requests | Chrome-based default |

### Corporate Network Support

For corporate environments with proxy servers or firewalls that block certain User-Agent strings:

```json
{
  "env": {
    "MCP_USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
  }
}
```

## Basic Usage

Examples:

- "Search Experience League for 'sling models' documentation"
- "Search for AEM component tutorials for developers"
- "Get available AEM services"
- "Look up documentation on AEM Cloud Service introduction"
- "Read the AEM 6.5 documentation and explain key features"
- "Show me the AEM Project Archetype GitHub README"
- "Get documentation on Apache Sling Models"
- "What sessions are at adaptTo() 2024 on day 1?"
- "What were the sessions at adaptTo() 2012?"
- "Provide guidance on accessing YouTube transcript for video XYZ"

## Tools

### search_experience_league

Search Adobe Experience League documentation with advanced filters.

```python
search_experience_league(
    query: str,
    content_types: List[str] = ['Documentation'],
    products: List[str] = None,
    roles: List[str] = None,
    include_all_aem_products: bool = False
) -> str
```

**Parameters**:
- `query`: Search term (e.g., 'sling models', 'component development')
- `content_types`: Filter by type (Documentation, Tutorial, Troubleshooting, API Reference, etc.)
- `products`: Filter by Adobe products (e.g., 'Experience Manager', 'Experience Manager|as a Cloud Service')
- `roles`: Filter by user role (Developer, Admin, User, Leader, etc.)
- `include_all_aem_products`: Auto-include all AEM variants (Cloud Service, 6.5, Assets, Sites, etc.)

**Examples**:
```python
# Search for documentation about sling models
search_experience_league(query='sling models', content_types=['Documentation'])

# Search for component tutorials for developers
search_experience_league(
    query='components',
    content_types=['Tutorial'],
    roles=['Developer']
)

# Search across all AEM products
search_experience_league(
    query='authentication',
    include_all_aem_products=True
)
```

### read_documentation

Fetches documentation pages from the AEM ecosystem and converts them to markdown format.

```python
read_documentation(url: str, max_length: int = 10000, start_index: int = 0) -> str
```

**Supported Domains**:
- **Adobe Official**: experienceleague.adobe.com (including /search pages), developer.adobe.com, helpx.adobe.com, docs.adobe.com, business.adobe.com
- **GitHub**: github.com/* (any organization), *.github.io (GitHub Pages)
- **Apache Sling**: sling.apache.org
- **Community Events**: adapt.to (all years: 2011-2025+, including hash fragments like #day-1 and PDFs)
- **Video Resources**: youtube.com, youtu.be (provides transcript access guidance)

**Special Features**:
- YouTube URLs: Provides video information and guidance on accessing transcripts
- PDF files: Detects PDF documents (e.g., adaptTo() presentations) and provides download instructions
- Search pages: Preserves hash fragments with search parameters
- adaptTo() pages: Preserves hash fragments for day navigation (#day-1, #day-2, etc.)
- Pagination support for long documents via `start_index` and `max_length`
- Automatic content extraction with platform-specific selectors
- Session tracking for analytics

### get_available_services

Gets a curated list of AEM ecosystem services and documentation areas.

```python
get_available_services() -> List[ServiceInfo]
```

Returns 30+ resources including:
- **Core AEM**: Cloud Service, 6.5, Developer APIs
- **GitHub Repos**: Project Archetype, Core WCM Components, ACS AEM Commons, Netcentric Tools
- **Foundation**: Apache Sling Models, Servlets, Eventing
- **Community**: adaptTo() 2025, 2024, 2023, Historical archives (2011-2019)
- **Business**: Adobe Summit
- **Video**: YouTube channels (Adobe Developers, AEM User Group)

## Architecture

The server is built following the AWS Documentation MCP Server pattern:

- `server.py` - Main FastMCP server with tool definitions
- `server_utils.py` - Shared utilities for HTTP requests and URL validation
- `util.py` - HTML extraction and Markdown conversion utilities
- `models.py` - Pydantic data models

## Development

### Running Tests

```bash
# Install development dependencies
uv pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=aemlabs

# Run live tests (makes real HTTP requests)
pytest --run-live
```

### Code Quality

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Type checking
pyright
```

## License

Apache License 2.0 - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on the GitHub repository.
