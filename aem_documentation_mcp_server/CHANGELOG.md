# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2025-01-23

### Added

- **PDF Document Support**: Automatic detection of PDF files with download guidance
  - Detects `.pdf` extensions in URLs
  - Provides download instructions and extraction tool recommendations
  - Special handling for adaptTo() conference presentations
  - Returns formatted markdown with PDF metadata
- **Expanded GitHub Support**: Now supports ANY GitHub organization (not limited to Adobe)
  - Supports all public GitHub repositories (Adobe, ACS, Netcentric, etc.)
  - Supports GitHub organization pages (e.g., `https://github.com/Netcentric`)
  - Added validation for GitHub Pages (*.github.io)
  - Support for community AEM projects and tools
- **New Services** (5 additions): Expanded catalog from 25 to 30 services
  - ACS AEM Commons (GitHub repository)
  - ACS AEM Commons Documentation (GitHub Pages)
  - Netcentric AEM Tools (GitHub organization)
  - AEM Multi-Tenant Demo (Netcentric)
  - Additional community resources
- **Enhanced Content Extraction**: Added selectors for GitHub Pages
  - `.post-content`, `.page-content` for Jekyll sites
  - Better support for static site generators (Hugo, Jekyll, etc.)
- **Test Coverage**: Added 4 new validation tests
  - GitHub ACS URL validation
  - GitHub Netcentric URL validation
  - GitHub Pages URL validation
  - adaptTo() PDF URL validation

### Changed

- **GitHub URL Validation**: Relaxed from `github.com/adobe/*` to `github.com/*`
  - Now accepts any public GitHub organization
  - Supports organization pages without repository path
  - Updated regex pattern from specific to general
- **URL Validation Messages**: Updated error messages to reflect broader GitHub support
- **Test Updates**: Modified test for non-Adobe GitHub URLs (now valid instead of invalid)

### Fixed

- GitHub organizations other than Adobe are now properly supported
- GitHub organization URLs (without repository) are now validated correctly
- GitHub Pages documentation sites now accessible

## [0.3.0] - 2025-11-23

### Added

- **New Tool: `search_experience_league`**: Search Adobe Experience League with advanced filters
  - Filter by content type (Documentation, Tutorial, Troubleshooting, etc.)
  - Filter by products (Experience Manager variants, Cloud Services, etc.)
  - Filter by roles (Developer, Admin, User, Leader, etc.)
  - Auto-include all AEM products option
  - 14 comprehensive tests for search functionality
- **Enhanced URL Support**:
  - Experience League search pages with hash fragments preserved
  - adaptTo() conference support for all years (2011-2025+)
  - Hash fragment preservation for adaptTo() day navigation (#day-1, #day-2, etc.)
- **Expanded Service Catalog**: Grew from 22 to 25 services
  - Added adaptTo() 2024 Schedule
  - Added adaptTo() 2023 Schedule  
  - Added adaptTo() Historical Archives (2011-2019)
- **New Module**: `search_utils.py` with search URL building utilities
  - Predefined product lists (EXPERIENCE_MANAGER_PRODUCTS, ALL_PRODUCTS)
  - Predefined content types (CONTENT_TYPES)
  - Predefined roles (ROLES)
- **Enhanced Content Extraction**: Added selectors for Experience League search results
  - `.search-results`, `.search-results-list`, `.search-result-item`
  - `dexter-SearchResults`, `.coveo-search-section`, `.coveo-result-list`
  - `.schedule-content`, `.conference-content` for adaptTo()
- **Comprehensive Test Coverage**: Increased from 61 to 75 tests (+14 tests, +23% growth)

### Changed

- **Hash Fragment Handling**: Improved logic to preserve fragments for search and adaptTo() pages
  - Regular docs: fragments removed (backward compatible)
  - Search pages: fragments preserved for filter parameters
  - adaptTo() pages: fragments preserved for day navigation
- **Server Instructions**: Updated to include search tool guidance
- **Documentation**: Enhanced README with search examples and updated feature list

### Fixed

- adaptTo() URLs with hash fragments now work correctly
- Search URLs maintain filter parameters in hash fragments

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
