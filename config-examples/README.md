# MCP Client Configuration Examples

This directory contains example configurations for various MCP clients.

## Claude Desktop

### Using Python directly

Copy the contents of `claude-desktop-config.json` to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Make sure you have installed the package:
```bash
pip install -e /path/to/adobe-experience-manager-mcps
playwright install chromium
```

### Using uv (recommended)

If you're using `uv` for Python package management, use `claude-desktop-config-uv.json` instead:

1. Update the `--directory` path to point to your clone of the repository
2. Install uv if you haven't already: `pip install uv`
3. Copy the configuration to Claude Desktop config file

## Other MCP Clients

For other MCP clients, use similar configuration with:
- **Command**: `python`
- **Arguments**: `["-m", "adobe_experience_manager_mcps.server"]`

Or with the full path to the Python interpreter:
```json
{
  "command": "/path/to/python",
  "args": ["-m", "adobe_experience_manager_mcps.server"]
}
```

## Testing the Configuration

After adding the configuration, restart your MCP client. You should see the `read_aem_doc` tool available.

Test it with a URL like:
```
https://experienceleague.adobe.com/docs/experience-manager-cloud-service/content/overview/introduction.html
```

## Troubleshooting

### Playwright not found
Make sure to install Playwright browsers:
```bash
playwright install chromium
```

### Module not found
Ensure the package is installed:
```bash
pip install -e /path/to/adobe-experience-manager-mcps
```

### Network issues
The tool requires internet access to fetch documentation from Adobe Experience League. Ensure your network allows connections to `experienceleague.adobe.com`.
