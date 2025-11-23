# Quick Reference: Supported URLs and Examples

## Supported Domain Patterns

### Adobe Official Documentation
✅ `https://experienceleague.adobe.com/...`  
✅ `https://developer.adobe.com/...`  
✅ `https://helpx.adobe.com/...`  
✅ `https://docs.adobe.com/...`  
✅ `https://business.adobe.com/...`

### GitHub (Adobe Organization)
✅ `https://github.com/adobe/...`  
❌ `https://github.com/other-org/...` (must be adobe org)

### Apache Sling
✅ `https://sling.apache.org/...`

### Community Events
✅ `https://adapt.to/...`

### YouTube
✅ `https://www.youtube.com/watch?v=...`  
✅ `https://www.youtube.com/embed/...`  
✅ `https://youtu.be/...`

## Example Queries

### Basic Documentation
```
"Read the AEM Cloud Service introduction documentation"
→ Fetches from experienceleague.adobe.com
```

### GitHub Repositories
```
"Show me the AEM Project Archetype README"
→ Fetches https://github.com/adobe/aem-project-archetype

"Get the Core WCM Components documentation"
→ Fetches https://github.com/adobe/aem-core-wcm-components
```

### Apache Sling
```
"Explain Apache Sling Models"
→ Fetches https://sling.apache.org/documentation/bundles/models.html

"How do Sling Servlets work?"
→ Fetches https://sling.apache.org/documentation/the-sling-engine/servlets.html
```

### Community Events
```
"What's the schedule for adaptTo() 2025?"
→ Fetches https://adapt.to/2025/schedule

"Show me adaptTo() conference details"
→ Fetches https://adapt.to/2025/conference.html
```

### YouTube Videos
```
"Get transcript guidance for YouTube video nJ8QTNQEkD8"
→ Provides video info and transcript access instructions

"Access the Adobe Developers YouTube channel"
→ Returns channel information and guidance
```

### Business Content
```
"Tell me about Adobe Summit 2025"
→ Fetches business.adobe.com/summit/2025.html
```

## Available Services (22 Total)

### Core AEM (9 services)
1. AEM as a Cloud Service
2. AEM 6.5 (On-Premise)
3. AEM 6.5 (LTS)
4. AEM 6.5 Service Pack Notes
5. Developer APIs & Events
6. Sites Optimizer
7. Screens as a Cloud Service
8. Edge Delivery Services
9. Headless CMS

### GitHub Repositories (2 services)
10. AEM Project Archetype
11. AEM Core WCM Components

### Apache Sling Foundation (4 services)
12. Sling Models
13. Sling Servlets
14. Sling Eventing
15. Sling Context-Aware Configuration

### UI Components (2 services)
16. Coral UI 3 Reference
17. Spectrum Design System

### Community Events (2 services)
18. adaptTo() 2025 Conference
19. adaptTo() 2025 Schedule

### Business (1 service)
20. Adobe Summit

### Video Resources (2 services)
21. Adobe Developers YouTube Channel
22. AEM User Group YouTube Channel

## Content Extraction Features

### Automatic Platform Detection
- Detects platform from URL
- Uses platform-specific content selectors
- Removes platform-specific navigation

### Supported Content Types
- HTML documentation pages
- GitHub Markdown (README.md, etc.)
- Apache Sling documentation
- Conference/event pages
- YouTube video pages (guidance only)

### Pagination Support
```python
# Get first 5000 characters
read_documentation(url, max_length=5000, start_index=0)

# Get next 5000 characters
read_documentation(url, max_length=5000, start_index=5000)
```

### Special Features

#### YouTube Videos
- Video ID extraction
- Manual transcript access instructions
- Notes about YouTube API requirements
- Direct link to video page

#### GitHub Repositories
- README.md content
- Documentation files
- Badge preservation
- Link preservation

#### Apache Sling
- Main content extraction
- Code example preservation
- Navigation removal
- Table of contents handling

## Tool Signatures

### read_documentation
```python
read_documentation(
    url: str,              # Required: URL to fetch
    max_length: int = 10000,   # Optional: max chars (default 10000)
    start_index: int = 0       # Optional: start position (default 0)
) -> str                       # Returns: Markdown content
```

### get_available_services
```python
get_available_services() -> List[ServiceInfo]

# ServiceInfo structure:
{
    "name": "Service Name",
    "url": "https://...",
    "description": "Description text",
    "category": "Category name"
}
```

## Common Use Cases

### 1. Learning AEM Concepts
"Read the AEM Cloud Service architecture documentation"

### 2. Setting Up Projects
"Show me the AEM Project Archetype documentation"

### 3. Understanding Sling
"Explain Apache Sling Models with examples"

### 4. Finding Conference Sessions
"What sessions are at adaptTo() 2025?"

### 5. Accessing Video Content
"Provide guidance for accessing transcript of YouTube video XYZ"

### 6. Component Development
"Get the Core WCM Components documentation"

### 7. API Integration
"Read the AEM Developer APIs documentation"

### 8. Event Information
"Tell me about Adobe Summit schedule"

## Limitations

### YouTube Transcripts
- **Manual Access Required**: Transcripts are not automatically extracted
- **API Integration**: Requires additional dependencies (youtube-transcript-api)
- **Availability**: Not all videos have transcripts
- **Languages**: Transcript language depends on video settings

### GitHub Limitations
- **Adobe Organization Only**: Only github.com/adobe/* repositories supported
- **Rate Limiting**: Subject to GitHub's rate limits
- **Public Only**: Private repositories not accessible

### General Limitations
- **No Authentication**: All resources must be publicly accessible
- **No File Downloads**: Only HTML/text content, no binary files
- **No Interactive Content**: JavaScript-heavy pages may not render fully
- **Pagination Required**: Long documents require multiple requests

## Troubleshooting

### "Invalid URL" Error
- Verify URL matches supported domain patterns
- For GitHub, ensure URL is from adobe organization
- Check URL is publicly accessible

### Empty Content
- Some pages may use client-side rendering
- Try adding selectors for platform-specific elements
- Check page loads correctly in browser

### Truncated Content
- Use pagination with `start_index` parameter
- Increase `max_length` if needed
- Content is limited to prevent context overflow

## Version Information

- **Current Version**: 0.2.0
- **Python**: 3.10+
- **FastMCP**: 1.11.0+
- **Dependencies**: httpx, BeautifulSoup4, markdownify, pydantic
