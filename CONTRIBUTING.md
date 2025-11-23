# Contributing to AEM MCP Server

Thank you for your interest in contributing! This document provides guidelines for contributing to the Adobe Experience Manager MCP Server project.

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/salomao-santos/adobe-experience-manager-mcps.git
   cd adobe-experience-manager-mcps
   ```

2. **Install dependencies**
   ```bash
   pip install -e .
   pip install pytest pytest-asyncio
   playwright install chromium
   ```

3. **Run tests**
   ```bash
   pytest tests/ -v
   ```

## Code Style

- Follow PEP 8 guidelines
- Use type hints for function parameters and return values
- Write descriptive docstrings for all public functions
- Keep functions focused and single-purpose

## Testing

- Add tests for all new features
- Ensure all tests pass before submitting PR
- Test with real AEM documentation URLs when possible
- Include both positive and negative test cases

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes with clear, descriptive commits
3. Add/update tests as needed
4. Update documentation (README, EXAMPLES, etc.)
5. Ensure all tests pass
6. Submit PR with clear description of changes

## Areas for Contribution

### High Priority
- Add support for more Adobe documentation sites
- Improve content extraction accuracy
- Add caching mechanism for repeated requests
- Add retry logic for failed requests

### Documentation
- Add more usage examples
- Improve API documentation
- Add troubleshooting guide
- Create video tutorials

### Testing
- Add integration tests with real AEM docs
- Add performance benchmarks
- Add error handling tests
- Add tests for edge cases

### Features
- Support for batch documentation extraction
- Export to different markdown flavors
- Configuration file support
- CLI tool for standalone use
- Support for authenticated documentation

## Code Review

All contributions will be reviewed for:
- Code quality and style
- Test coverage
- Documentation completeness
- Security considerations
- Performance impact

## Questions?

Open an issue on GitHub for questions or discussions.

Thank you for contributing!
