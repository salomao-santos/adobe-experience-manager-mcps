# AEM MCP Server Usage Examples

## Example 1: Extract Release Notes

Extract the latest AEM Cloud Service release notes:

```python
# Via MCP protocol
{
  "tool": "read_aem_doc",
  "arguments": {
    "url": "https://experienceleague.adobe.com/docs/experience-manager-cloud-service/content/release-notes/release-notes/release-notes-current.html"
  }
}
```

**Result**: Clean Markdown containing:
- Release highlights
- New features
- Known issues
- Deprecated features

---

## Example 2: Extract Code Quality Rules

Get documentation about AEM code quality and testing:

```python
{
  "tool": "read_aem_doc",
  "arguments": {
    "url": "https://experienceleague.adobe.com/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/test-results/overview-test-results.html"
  }
}
```

**Result**: Markdown with:
- Code quality metrics
- Testing requirements
- Best practices
- Examples

---

## Example 3: Extract Development Guidelines

Extract full-stack development guidelines:

```python
{
  "tool": "read_aem_doc",
  "arguments": {
    "url": "https://experienceleague.adobe.com/docs/experience-manager-cloud-service/content/implementing/developing/full-stack/overview.html"
  }
}
```

**Result**: Structured Markdown with:
- Development patterns
- Architecture guidelines
- Code examples
- Integration best practices

---

## Example 4: Extract Component Development Docs

Get documentation for AEM component development:

```python
{
  "tool": "read_aem_doc",
  "arguments": {
    "url": "https://experienceleague.adobe.com/docs/experience-manager-cloud-service/content/implementing/developing/components/overview.html"
  }
}
```

---

## Example 5: Extract Dispatcher Configuration

Get Dispatcher configuration documentation:

```python
{
  "tool": "read_aem_doc",
  "arguments": {
    "url": "https://experienceleague.adobe.com/docs/experience-manager-dispatcher/using/configuring/dispatcher-configuration.html"
  }
}
```

---

## Using with Claude Desktop

1. Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

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

2. Restart Claude Desktop

3. Use in conversation:
```
Can you read the AEM release notes from 
https://experienceleague.adobe.com/docs/... 
and summarize the key changes?
```

---

## Using Programmatically

```python
import asyncio
from aem_mcp.server import fetch_aem_doc

async def main():
    url = "https://experienceleague.adobe.com/docs/..."
    markdown = await fetch_aem_doc(url)
    print(markdown)

asyncio.run(main())
```

---

## Tips for Best Results

1. **Use Direct Documentation URLs**: Point to specific documentation pages, not landing pages
2. **Check Content Quality**: The tool works best with well-structured Adobe documentation
3. **Handle Errors**: Network issues or page structure changes may affect extraction
4. **Review Output**: Always review the extracted Markdown for completeness

---

## Common Use Cases

### For Developers
- Extract API documentation
- Get code examples
- Review best practices
- Check component specifications

### For DevOps
- Get deployment guidelines
- Review configuration options
- Extract troubleshooting guides
- Check system requirements

### For Architects
- Review architecture patterns
- Get integration guidelines
- Extract security best practices
- Study scalability recommendations

### For Content Authors
- Get authoring guidelines
- Review component usage
- Extract workflow documentation
- Check accessibility requirements
