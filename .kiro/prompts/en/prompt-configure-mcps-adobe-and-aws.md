# Adobe and AWS MCP Servers Configuration for Kiro

## Summary

This guide configures **6 MCP servers** in Kiro for accessing Adobe AEM documentation, AWS documentation, document processing, and repository research.

**Total MCPs configured**: 6 servers
- **1 Adobe server**: AEM Documentation
- **5 AWS servers**: Documentation, Core, Knowledge, Document Loader, and Git Repo Research

---

## Installation Requirements

### Required Prerequisites

1. **uv** - Fast Python package manager
   - Installation: [Astral](https://docs.astral.sh/uv/getting-started/installation/) or [GitHub](https://github.com/astral-sh/uv#installation)
   - Installation command: `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - Or via pip: `pip install uv`
   - Or via homebrew: `brew install uv`
   - Verify installation: `uv --version`

2. **Python 3.10 or higher** (recommended: 3.10, 3.11, 3.12, or 3.13)
   - **For AEM Documentation MCP**: Python 3.10+ is required
   - **For AWS MCPs**: Python 3.12+ is recommended
   - Installation via uv: `uv python install 3.10` (or higher version)
   - Verify version: `python3 --version`

3. **Docker** (optional - for containerized execution)
   - Installation: [Docker Desktop](https://www.docker.com/products/docker-desktop/)
   - Verify installation: `docker --version`
   - **Note**: Docker is an alternative to uvx for running MCP servers

### AWS Requirements (Optional - only for some servers)

1. **AWS CLI configured** with credentials that have access to Amazon Bedrock
2. **Amazon Bedrock access** for embedding models like Titan Embeddings
3. **AWS environment variables**:
   - `AWS_REGION` (example: `us-west-2`)
   - `AWS_PROFILE` (your AWS profile name)

### Optional Requirements

1. **GitHub Token** - For higher rate limits when searching repositories
   - Environment variable: `GITHUB_TOKEN`

---

## Configured MCP Servers

> **⚠️ Important**: The AEM Documentation MCP server is **not yet published to PyPI**. Use Docker for local development as instructed below.

## Adobe Servers

### 1. AEM Documentation MCP Server
**Purpose**: Access to official Adobe Experience Manager (AEM) documentation

**Specific Requirements**:
- **Python**: 3.10 or higher (supports 3.10, 3.11, 3.12, 3.13)
- **uv**: Latest version
- **Docker** (optional): For containerized execution

**Features**:
- **Experience League Search**: Search Adobe documentation with advanced filters (content type, products, roles)
- **Documentation Reading**: Fetch and convert documentation pages to markdown format from:
  - Official Adobe documentation (Experience League, Developer, HelpX, Docs)
  - GitHub repositories (any organization: Adobe, ACS, Netcentric, etc.)
  - GitHub Pages (*.github.io documentation sites)
  - Apache Sling documentation
  - adaptTo() conference resources (all years: 2011-2025+, including PDFs)
  - YouTube videos (with transcript guidance)
  - Adobe Business sites (Summit, etc.)
- **Available Services**: Curated list of 30+ AEM services and documentation areas
- **Hash Fragment Support**: Preserves URL fragments for search pages and adaptTo() schedules (#day-1, #day-2, etc.)
- **PDF Detection**: Identifies PDF documents and provides download guidance

**Available Tools**:
1. `search_experience_league` - Search with advanced filters
2. `read_documentation` - Convert documentation to markdown
3. `get_available_services` - List 30+ AEM resources

**Configuration via Docker (Recommended for local development)**:
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

**Docker Note**: To use Docker, first build the image:
```bash
cd aem_documentation_mcp_server
docker build -t aem-docs-mcp-server:latest .
```

**Configuration via UVX (When published to PyPI)**:
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

**Note**: The package is not yet published to PyPI. Use Docker for local development.

**Optional Environment Variables**:
- `FASTMCP_LOG_LEVEL`: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL) - Default: WARNING
- `MCP_USER_AGENT`: Custom User-Agent for corporate networks

**Repository**: [adobe-experience-manager-mcps](https://github.com/salomao-santos/adobe-experience-manager-mcps)
**Author**: Salomão Santos (salomaosantos777@gmail.com)

---

## AWS Servers

### 2. AWS Documentation MCP Server
**Purpose**: Access to official AWS documentation

**Features**:
- Search AWS documentation
- Read documentation pages
- Related content recommendations

**Configuration**:
```json
{
  "mcpServers": {
    "awslabs.aws-documentation-mcp-server": {
      "command": "uvx",
      "args": ["awslabs.aws-documentation-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR",
        "AWS_DOCUMENTATION_PARTITION": "aws",
        "MCP_USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

---

### 3. Core MCP Server
**Purpose**: Core AWS functionalities

**Features**:
- Basic AWS operations
- AWS services integration

**Configuration**:
```json
{
  "mcpServers": {
    "awslabs.core-mcp-server": {
      "command": "uvx",
      "args": ["awslabs.core-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

---

### 4. AWS Knowledge MCP Server
**Purpose**: AWS knowledge base via HTTP

**Features**:
- Access to AWS knowledge
- Queries about AWS services and resources

**Configuration (Recommended for Kiro)**:
```json
{
  "mcpServers": {
    "aws-knowledge-mcp-server": {
      "url": "https://knowledge-mcp.global.api.aws",
      "type": "http",
      "disabled": false
    }
  }
}
```

---

### 5. Document Loader MCP Server
**Purpose**: Processing various document types

**Features**:
- **PDF text extraction**: Using pdfplumber
- **Word processing**: Convert DOCX/DOC to markdown
- **Excel reading**: Parse XLSX/XLS and convert to markdown
- **PowerPoint processing**: Extract content from PPTX/PPT
- **Image loading**: Supports PNG, JPG, GIF, BMP, TIFF, WEBP

**Configuration**:
```json
{
  "mcpServers": {
    "awslabs.document-loader-mcp-server": {
      "command": "uvx",
      "args": ["awslabs.document-loader-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

---

### 6. Git Repo Research MCP Server (Optional)
**Purpose**: Git repository research and analysis using Amazon Bedrock embeddings

**Additional requirements**:
- AWS credentials with Bedrock access
- GitHub token (optional, but recommended)

**Features**:
- Semantic search in repositories
- Code analysis using AI
- Embeddings with Amazon Bedrock

**Configuration**:
```json
{
  "mcpServers": {
    "awslabs.git-repo-research-mcp-server": {
      "command": "uvx",
      "args": ["awslabs.git-repo-research-mcp-server@latest"],
      "env": {
        "AWS_PROFILE": "your-aws-profile",
        "AWS_REGION": "us-west-2",
        "FASTMCP_LOG_LEVEL": "ERROR",
        "GITHUB_TOKEN": "your-github-token"
      },
      "disabled": true,
      "autoApprove": []
    }
  }
}
```

**Important**: This server is **disabled by default** because it requires:
- AWS credentials configured with Bedrock access
- Optional GitHub token for higher rate limits
- Set `"disabled": false` only after configuring your AWS credentials

**Note**: Replace `your-aws-profile` and `your-github-token` with your actual values.

---

## Complete Kiro Configuration

### Complete Configuration (Recommended)

File: `.kiro/settings/mcp.json`

**Note**: The AEM server uses Docker because the package is not yet published to PyPI.

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
    },
    "awslabs.aws-documentation-mcp-server": {
      "command": "uvx",
      "args": ["awslabs.aws-documentation-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR",
        "AWS_DOCUMENTATION_PARTITION": "aws",
        "MCP_USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
      },
      "disabled": false,
      "autoApprove": [
        "read_documentation",
        "search_documentation",
        "recommend"
      ]
    },
    "awslabs.core-mcp-server": {
      "command": "uvx",
      "args": ["awslabs.core-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": []
    },
    "aws-knowledge-mcp-server": {
      "url": "https://knowledge-mcp.global.api.aws",
      "type": "http",
      "disabled": false
    },
    "awslabs.document-loader-mcp-server": {
      "command": "uvx",
      "args": ["awslabs.document-loader-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": [
        "read_document",
        "read_image"
      ]
    },
    "awslabs.git-repo-research-mcp-server": {
      "command": "uvx",
      "args": ["awslabs.git-repo-research-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": true,
      "autoApprove": []
    }
  }
}
```

**Important**: Before using, build the AEM Docker image:
```bash
cd aem_documentation_mcp_server
docker build -t aem-docs-mcp-server:latest .
```

### About Auto-Approval (autoApprove)

Tools listed in `autoApprove` don't require manual confirmation for each use:
- **AEM**: `search_experience_league`, `read_documentation`, `get_available_services`
- **AWS Docs**: `read_documentation`, `search_documentation`, `recommend`
- **Document Loader**: `read_document`, `read_image`

You can add or remove tools from this list based on your security preferences.

---

## Installation Verification

### 1. Verify installed requirements

```bash
# Verify uv
uv --version

# Verify Python (should be 3.10+ for AEM, 3.12+ for AWS)
python3 --version

# Verify uvx
uvx --help

# Verify Docker (if using)
docker --version
```

### 2. Validate configuration file

```bash
# Check if JSON is valid
cat .kiro/settings/mcp.json | python3 -m json.tool
```

### 3. Test MCP servers individually

```bash
# Test AEM Documentation
uvx aemlabs.aem-documentation-mcp-server@latest

# Test AWS Documentation
uvx awslabs.aws-documentation-mcp-server@latest

# Test Document Loader
uvx awslabs.document-loader-mcp-server@latest

# Test AEM via Docker (if you built the image)
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' | docker run --rm -i aem-docs-mcp-server:latest
```

### 4. Verify in Kiro

1. Open the MCP servers panel in Kiro
2. Verify that 5-6 servers are connected (1 Adobe + 4-5 AWS)
3. Test available tools:
   - AEM: `search_experience_league`, `read_documentation`, `get_available_services`
   - AWS: Server-specific tools
4. Check logs if there are issues
5. Use Kiro's command palette: "MCP: Reconnect Servers" if needed

---

## Important Notes

1. **Versions**: Always use `@latest` to get the most recent server versions
2. **Log Level**: Configured as `ERROR` to reduce verbosity. Use `DEBUG` for troubleshooting
3. **Auto Approve**: Empty list by default. Add specific tools for automatic approval
4. **Reconnection**: Servers automatically reconnect after configuration changes
5. **Git Repo Research**: Optional server that requires additional AWS configuration
6. **AEM Documentation**: Accesses Adobe documentation, GitHub, Apache Sling, adaptTo(), and YouTube related to AEM

---

## Troubleshooting

### Server won't connect
- Verify that `uv` and `uvx` are installed
- Confirm that Python 3.12+ is available
- Validate the JSON format of the configuration file

### AWS credentials error
- Configure AWS CLI: `aws configure`
- Check environment variables: `AWS_PROFILE` and `AWS_REGION`
- Confirm Bedrock access (if using Git Repo Research)

### Timeout or slowness
- Check internet connection
- Test connectivity: `curl https://knowledge-mcp.global.api.aws`
- Increase timeout if necessary

### AEM Documentation issues
- Verify that `uvx` is installed and working: `uvx --help`
- Confirm Python 3.10+: `python3 --version`
- Test connectivity with Experience League: `curl https://experienceleague.adobe.com`
- For Docker: Check if the image was built: `docker images | grep aem-docs-mcp-server`
- Test the server manually: `uvx aemlabs.aem-documentation-mcp-server@latest`
- Check the repository: [adobe-experience-manager-mcps](https://github.com/salomao-santos/adobe-experience-manager-mcps)
- Open an issue: [Bug Tracker](https://github.com/salomao-santos/adobe-experience-manager-mcps/issues)

---

## Additional Resources

### Adobe AEM Documentation
- [Experience League - AEM](https://experienceleague.adobe.com/docs/experience-manager.html)
- [AEM Developer Documentation](https://developer.adobe.com/experience-manager/)
- [adaptTo() Conference](https://adapt.to/)
- [Apache Sling](https://sling.apache.org/)

### AWS Documentation
- [AWS Documentation](https://docs.aws.amazon.com/)
- [AWS Developer Center](https://aws.amazon.com/developer/)
- [Amazon Bedrock](https://aws.amazon.com/bedrock/)

### MCP Repositories
- [Adobe Experience Manager MCPs](https://github.com/salomao-santos/adobe-experience-manager-mcps)
- [AWS Labs MCP Servers](https://github.com/awslabs)
