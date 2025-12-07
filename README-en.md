# AEM Documentation MCP Server

Model Context Protocol (MCP) server for Adobe Experience Manager (AEM) Documentation

This MCP server provides tools to access Adobe AEM documentation and related resources from the AEM ecosystem, converting them to markdown format for easy consumption by AI assistants.

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

1. **Python**: Version 3.10 or newer
   - Install using `uv python install 3.10` (or 3.11, 3.12, 3.13)
   
2. **uv**: Latest version from [Astral](https://docs.astral.sh/uv/getting-started/installation/)
   - Install via: `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - Or via pip: `pip install uv`
   - Or via homebrew: `brew install uv`

3. **Docker** (optional): For containerized deployment
   - Install from [Docker Desktop](https://www.docker.com/products/docker-desktop/)

## Installation

> **⚠️ Important**: The `aemlabs.aem-documentation-mcp-server` package is **not yet published to PyPI**. Use Docker for local development until official publication.

You can run the MCP server using either **Docker** (recommended for local development) or **UVX** (when published to PyPI). Choose the method that best fits your environment.

### Option 1: Using Docker (Recommended for local development)

First, build the Docker image:

```bash
cd aem_documentation_mcp_server
docker build -t aem-docs-mcp-server:latest .
```

Then configure the MCP server:

```json
{
  "mcpServers": {
    "aem-documentation-mcp-server": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "aem-docs-mcp-server:latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": [
        "search_experience_league",
        "read_documentation",
        "get_available_services"
      ]
    }
  }
}
```

### Option 2: Using UVX (When published to PyPI)

**Note**: The package is not yet published to PyPI. This option will be available soon.

Configure the MCP server in your MCP client configuration:

```json
{
  "mcpServers": {
    "aemlabs.aem-documentation-mcp-server": {
      "command": "uvx",
      "args": ["aemlabs.aem-documentation-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": [
        "search_experience_league",
        "read_documentation",
        "get_available_services"
      ]
    }
  }
}
```

### About Auto-Approval (autoApprove)

Tools listed in `autoApprove` don't require manual confirmation for each use:
- `search_experience_league` - Search documentation
- `read_documentation` - Read documentation pages
- `get_available_services` - List available services

You can add or remove tools from this list based on your security preferences.

### Switching Between Docker and UVX

To switch between modes, set `"disabled": true` on the mode you don't want to use and `"disabled": false` on the one you want to activate.

### Development Installation

Clone the repository and install in development mode:

```bash
git clone https://github.com/salomao-santos/adobe-experience-manager-mcps.git
cd adobe-experience-manager-mcps/aem_documentation_mcp_server
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

The server is built using FastMCP and follows best practices for MCP server development:

- `server.py` - Main FastMCP server with tool definitions
- `server_utils.py` - Shared utilities for HTTP requests and URL validation
- `util.py` - HTML extraction and Markdown conversion utilities
- `models.py` - Pydantic data models
- `search_utils.py` - Experience League search functionality
- `youtube_utils.py` - YouTube video handling

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

## Docker Image

The Docker image is optimized for production use:
- **Base Image**: Python 3.13 Alpine
- **Size**: ~112MB
- **Multi-stage build**: Separates build and runtime dependencies
- **Non-root user**: Runs as unprivileged user for security
- **Optimizations**: Bytecode compilation, minimal dependencies

## License

Apache License 2.0 - See [LICENSE](aem_documentation_mcp_server/LICENSE) file for details

## Author

**Salomão Santos**
- Email: salomaosantos777@gmail.com
- GitHub: [@salomao-santos](https://github.com/salomao-santos)

## Repository

This project is publicly available at:
- **Homepage**: https://github.com/salomao-santos/adobe-experience-manager-mcps
- **Documentation**: https://github.com/salomao-santos/adobe-experience-manager-mcps/blob/main/README.md
- **Source Code**: https://github.com/salomao-santos/adobe-experience-manager-mcps.git
- **Bug Tracker**: https://github.com/salomao-santos/adobe-experience-manager-mcps/issues

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on the [GitHub repository](https://github.com/salomao-santos/adobe-experience-manager-mcps/issues).
