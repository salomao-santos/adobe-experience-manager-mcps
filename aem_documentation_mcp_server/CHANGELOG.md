# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-01-XX

### Added

- **Expanded Domain Support**: Now supports 10 domain patterns beyond Adobe official documentation
  - GitHub repositories from Adobe organization (github.com/adobe/*)
  - Apache Sling documentation (sling.apache.org)
  - adaptTo() conference resources (adapt.to)
  - YouTube videos with transcript guidance (youtube.com, youtu.be)
  - Adobe Business sites (business.adobe.com)
- **YouTube Integration**: New youtube_utils module for video handling
  - Video ID extraction from multiple URL formats
  - YouTube URL detection
  - Transcript access guidance for video content
- **Enhanced Service Catalog**: Expanded from 10 to 22 curated services
  - GitHub: AEM Project Archetype, Core WCM Components
  - Sling: Models, Servlets, Eventing, Context-Aware Configuration
  - Events: adaptTo() 2025 Conference and Schedule
  - Media: YouTube channels (Adobe Developers, AEM User Group)
  - Business: Adobe Summit
- **Platform-Specific Content Extraction**: Added specialized selectors for:
  - GitHub markdown rendering (article.markdown-body)
  - Apache Sling documentation (.content)
  - adaptTo() conference pages (.content-wrapper)
- **Comprehensive Test Coverage**: Increased from 37 to 61 tests
  - 24 new tests for YouTube utilities
  - 7 new tests for expanded domain validation
  - All tests passing (100% success rate)

### Changed

- Updated `validate_adobe_url()` to support comprehensive AEM ecosystem domains
- Enhanced `extract_content_from_html()` with platform-specific selectors
- Improved error messages to reference "supported domains" instead of "Adobe domains"
- Updated README with expanded feature documentation
- Updated server tool descriptions and examples

## [0.1.0] - 2025-11-23

### Added

- Initial release of Adobe AEM Documentation MCP Server
- `read_documentation` tool to fetch and convert AEM documentation pages to markdown
- `get_available_services` tool to list available AEM services and documentation areas
- Support for multiple Adobe domains:
  - experienceleague.adobe.com
  - developer.adobe.com
  - helpx.adobe.com
  - docs.adobe.com
- HTML to Markdown conversion with content extraction
- Pagination support for long documents
- Session tracking for analytics
- Hash fragment handling in URLs
- Comprehensive test suite (37 tests)
- Docker support
- Complete documentation in README.md
