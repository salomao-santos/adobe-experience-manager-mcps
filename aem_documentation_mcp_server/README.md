# Adobe Experience Manager (AEM) Documentation MCP Server

Model Context Protocol (MCP) server for Adobe Experience Manager (AEM) Documentation

This MCP server provides tools to access Adobe AEM documentation and related resources from the AEM ecosystem, converting them to markdown format.

## Features

- **Read Documentation**: Fetch and convert documentation pages to markdown format from:
  - Adobe Official Documentation (Experience League, Developer, HelpX, Docs)
  - GitHub repositories (adobe organization)
  - Apache Sling documentation
  - adaptTo() conference resources
  - YouTube videos (with transcript guidance)
  - Adobe Business sites (Summit, etc.)
- **Get Available Services**: Get a curated list of 22+ AEM services and documentation areas

## Prerequisites

### Installation Requirements

1. Install `uv` from [Astral](https://docs.astral.sh/uv/getting-started/installation/) or the [GitHub README](https://github.com/astral-sh/uv#installation)
2. Install Python 3.10 or newer using `uv python install 3.10` (or a more recent version)

## Installation

Configure the MCP server in your MCP client configuration:

```json
{
  "mcpServers": {
    "adobelabs.aem-documentation-mcp-server": {
      "command": "uvx",
      "args": ["adobelabs.aem-documentation-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

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

- "Get available AEM services"
- "Look up documentation on AEM Cloud Service introduction"
- "Read the AEM 6.5 documentation and explain key features"
- "Show me the AEM Project Archetype GitHub README"
- "Get documentation on Apache Sling Models"
- "What sessions are at adaptTo() 2025?"
- "Provide guidance on accessing YouTube transcript for video XYZ"

## Tools

### read_documentation

Fetches documentation pages from the AEM ecosystem and converts them to markdown format.

```python
read_documentation(url: str, max_length: int = 10000, start_index: int = 0) -> str
```

**Supported Domains**:
- **Adobe Official**: experienceleague.adobe.com, developer.adobe.com, helpx.adobe.com, docs.adobe.com, business.adobe.com
- **GitHub**: github.com/adobe/* (Adobe organization repositories)
- **Apache Sling**: sling.apache.org
- **Community Events**: adapt.to (adaptTo() conference)
- **Video Resources**: youtube.com, youtu.be (provides transcript access guidance)

**Special Features**:
- YouTube URLs: Provides video information and guidance on accessing transcripts
- Pagination support for long documents via `start_index` and `max_length`
- Automatic content extraction with platform-specific selectors
- Session tracking for analytics

### get_available_services

Gets a curated list of AEM ecosystem services and documentation areas.

```python
get_available_services() -> List[ServiceInfo]
```

Returns 22+ resources including:
- **Core AEM**: Cloud Service, 6.5, Developer APIs
- **GitHub Repos**: Project Archetype, Core WCM Components
- **Foundation**: Apache Sling Models, Servlets, Eventing
- **Community**: adaptTo() 2025 Conference, schedules
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
pytest --cov=adobelabs

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
