# Release Notes - v0.4.0

## 🚀 Summary

Version 0.4.0 expands the AEM Documentation MCP Server to support PDF documents and unlimited GitHub organization access, completing the ecosystem coverage for Adobe Experience Manager community resources.

## ✨ Key Features

### 1. PDF Document Support

The server now automatically detects PDF files and provides intelligent guidance:

```python
# Example: adaptTo() conference presentations
url = "https://adapt.to/2025/presentations/adaptto-2025-challenges-when-operating-1000-different-aem-applications.pdf"

# Returns:
# - PDF metadata (filename, URL)
# - Download instructions
# - Extraction tool recommendations (PyPDF2, pdfplumber)
# - Special notes for adaptTo() presentations
```

**Supported PDF Sources:**
- adaptTo() conference presentations (2011-2025+)
- Any AEM-related documentation PDFs
- GitHub repository PDFs
- Community resource PDFs

### 2. Unlimited GitHub Organization Support

Previously limited to `github.com/adobe/*`, now supports **any** public GitHub organization:

**Previously Supported:**
- ✅ `https://github.com/adobe/aem-core-wcm-components`

**Now Also Supported:**
- ✅ `https://github.com/Adobe-Consulting-Services/acs-aem-commons`
- ✅ `https://github.com/Netcentric/aem-multitenant-demo`
- ✅ `https://github.com/Netcentric` (organization pages)
- ✅ Any other AEM-related GitHub repository

### 3. GitHub Pages Documentation

Full support for GitHub Pages static sites (*.github.io):

```python
url = "https://adobe-consulting-services.github.io/acs-aem-commons/"
# Extracts documentation from Jekyll/Hugo static sites
```

**Enhanced Content Extraction:**
- `.post-content`, `.page-content` selectors for Jekyll
- Support for Hugo, Gatsby, and other static site generators
- Proper navigation removal for clean documentation

### 4. Expanded Service Catalog

**New Services Added (5):**

1. **ACS AEM Commons** (GitHub)
   - `https://github.com/Adobe-Consulting-Services/acs-aem-commons`
   - Popular AEM component library

2. **ACS AEM Commons Docs** (GitHub Pages)
   - `https://adobe-consulting-services.github.io/acs-aem-commons/`
   - Comprehensive documentation site

3. **Netcentric AEM Tools** (GitHub Org)
   - `https://github.com/Netcentric`
   - Collection of AEM development tools

4. **AEM Multi-Tenant Demo** (Netcentric)
   - `https://github.com/Netcentric/aem-multitenant-demo`
   - Multi-tenant AEM implementation example

5. **More community resources...**

**Total Services: 30** (up from 25 in v0.3.0)

## 🔧 Technical Improvements

### URL Validation Enhancements

**Before (v0.3.0):**
```python
r'^https?://github\.com/adobe/'  # Only Adobe org
```

**After (v0.4.0):**
```python
r'^https?://github\.com/[^/]+'   # Any org, with or without repo
r'^https?://[^/]+\.github\.io/'  # GitHub Pages
```

### PDF Detection Logic

```python
# Intelligent PDF detection with special handling
is_pdf = url_str.lower().endswith('.pdf')

if is_pdf:
    filename = parsed_url.path.split('/')[-1]
    
    # Special handling for adaptTo() presentations
    if 'adapt.to' in url_str and '/presentations/' in url_str:
        # Extract year, event info
        # Provide presentation-specific guidance
```

### Content Extraction Improvements

**New Selectors Added:**
- GitHub Pages: `.post-content`, `.page-content`
- Jekyll/Hugo support
- Static site generator compatibility

## 📊 Test Coverage

- **Total Tests:** 79 (4 new in v0.4.0)
- **Pass Rate:** 100% ✅
- **Code Coverage:** 76%
- **New Test Cases:**
  - GitHub ACS URL validation
  - GitHub Netcentric URL validation
  - GitHub Pages URL validation
  - adaptTo() PDF URL validation

## 🎯 Use Cases

### Use Case 1: Access adaptTo() Presentations

```python
# Read a conference presentation PDF
read_documentation(
    url="https://adapt.to/2025/presentations/adaptto-2025-mastering-aem-authorization-best-practices-for-security-and-performance.pdf"
)
# Returns download instructions and metadata
```

### Use Case 2: Browse Community Tools

```python
# Explore ACS AEM Commons repository
read_documentation(
    url="https://github.com/Adobe-Consulting-Services/acs-aem-commons"
)
# Returns README and repository information

# Read detailed documentation
read_documentation(
    url="https://adobe-consulting-services.github.io/acs-aem-commons/features/adaptive-images.html"
)
# Returns feature documentation in Markdown
```

### Use Case 3: Discover Organization Tools

```python
# Browse Netcentric's AEM tools
read_documentation(
    url="https://github.com/Netcentric"
)
# Returns organization profile and repository list
```

## 📝 Breaking Changes

**None** - All v0.3.0 functionality remains intact. This is a purely additive release.

## 🔄 Migration from v0.3.0

No migration needed! All existing code continues to work. Simply update to v0.4.0 to gain new capabilities:

```bash
cd aem_documentation_mcp_server
git pull origin main
uv sync
```

## 🧪 Validation

All 6 user-requested URLs validated successfully:

✅ `https://adapt.to/2025/presentations/adaptto-2025-challenges-when-operating-1000-different-aem-applications.pdf`
✅ `https://adapt.to/2025/presentations/adaptto-2025-mastering-aem-authorization-best-practices-for-security-and-performance.pdf`
✅ `https://github.com/Adobe-Consulting-Services/acs-aem-commons`
✅ `https://adobe-consulting-services.github.io/acs-aem-commons/`
✅ `https://github.com/Netcentric/aem-multitenant-demo`
✅ `https://github.com/Netcentric`

## 📚 Documentation Updates

- ✅ README.md - Updated features and supported domains
- ✅ CHANGELOG.md - Comprehensive v0.4.0 notes
- ✅ IMPROVEMENTS_v0.4.0.md - Detailed technical documentation
- ✅ Test validation script - `test_new_features_v04.py`

## 🔮 Future Enhancements

Potential v0.5.0 features (not committed):
- Optional PyPDF2 integration for automatic PDF text extraction
- GitHub API integration for structured repository data
- Caching for frequently accessed GitHub Pages
- Private repository support (with token auth)

## 🙏 Acknowledgments

This release was driven by user requests for:
- adaptTo() conference presentation access
- ACS AEM Commons integration
- Netcentric community tools
- Broader GitHub organization support

## 📞 Support

For issues or questions:
- Check IMPROVEMENTS_v0.4.0.md for technical details
- Review test files for usage examples
- Submit issues with detailed error messages

---

**Version:** 0.4.0  
**Release Date:** 2025-01-23  
**Test Status:** ✅ 79/79 passing  
**Coverage:** 76%  
**Breaking Changes:** None
