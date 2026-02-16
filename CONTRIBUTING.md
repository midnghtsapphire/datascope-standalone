# Contributing to DataScope Enhanced

Thank you for your interest in contributing to DataScope Enhanced! This document provides guidelines and information for contributors.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Contributing Guidelines](#contributing-guidelines)
5. [Pull Request Process](#pull-request-process)
6. [Coding Standards](#coding-standards)
7. [Testing](#testing)
8. [Documentation](#documentation)
9. [Community](#community)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

### Ways to Contribute

- **Bug Reports**: Report bugs and issues
- **Feature Requests**: Suggest new features or improvements
- **Code Contributions**: Submit bug fixes, new features, or improvements
- **Documentation**: Improve documentation, tutorials, or examples
- **Testing**: Help with testing and quality assurance
- **Community Support**: Help other users in discussions and issues

### Before You Start

1. **Check existing issues**: Look for existing issues or discussions about your idea
2. **Create an issue**: For significant changes, create an issue to discuss your proposal
3. **Fork the repository**: Create your own fork to work on
4. **Read the documentation**: Familiarize yourself with the codebase and architecture

## Development Setup

### Prerequisites

- Python 3.11 or higher
- Git
- Chrome browser (for browser automation features)
- Docker (optional, for containerized development)

### Local Development Setup

1. **Fork and clone the repository**:
```bash
git clone https://github.com/your-username/datascope-enhanced.git
cd datascope-enhanced
```

2. **Create a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install development dependencies**:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

4. **Install pre-commit hooks**:
```bash
pre-commit install
```

5. **Set up environment**:
```bash
cp .env.example .env
# Edit .env with your development settings
```

6. **Run tests**:
```bash
pytest
```

### Docker Development Setup

```bash
# Build development image
docker-compose -f docker-compose.dev.yml build

# Start development environment
docker-compose -f docker-compose.dev.yml up -d

# Run tests in container
docker-compose -f docker-compose.dev.yml exec datascope pytest
```

## Contributing Guidelines

### Issue Guidelines

#### Bug Reports

When reporting bugs, please include:

- **Clear title**: Descriptive title summarizing the issue
- **Environment**: OS, Python version, browser version
- **Steps to reproduce**: Detailed steps to reproduce the issue
- **Expected behavior**: What you expected to happen
- **Actual behavior**: What actually happened
- **Error messages**: Full error messages and stack traces
- **Screenshots**: If applicable, add screenshots

**Bug Report Template**:
```markdown
**Environment:**
- OS: [e.g., Ubuntu 20.04]
- Python: [e.g., 3.11.5]
- Chrome: [e.g., 118.0.5993.70]
- DataScope Version: [e.g., 1.0.0]

**Steps to Reproduce:**
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected Behavior:**
A clear description of what you expected to happen.

**Actual Behavior:**
A clear description of what actually happened.

**Error Messages:**
```
Paste full error messages here
```

**Additional Context:**
Add any other context about the problem here.
```

#### Feature Requests

When requesting features, please include:

- **Clear title**: Descriptive title for the feature
- **Problem statement**: What problem does this solve?
- **Proposed solution**: Detailed description of the proposed feature
- **Alternatives considered**: Other solutions you've considered
- **Use cases**: How would this feature be used?
- **Priority**: How important is this feature?

### Code Contribution Guidelines

#### Branch Naming

Use descriptive branch names:
- `feature/add-new-domain-support`
- `bugfix/fix-browser-automation-timeout`
- `docs/update-installation-guide`
- `refactor/improve-prompt-engine`

#### Commit Messages

Follow conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(browser): add support for Firefox automation
fix(prompt-engine): resolve timeout issues with large datasets
docs(api): update authentication documentation
test(cybersecurity): add unit tests for threat analysis
```

#### Code Style

- **Follow PEP 8**: Use Python's official style guide
- **Use Black**: Code formatting with Black
- **Type hints**: Include type hints for all functions
- **Docstrings**: Document all classes and functions
- **Comments**: Add comments for complex logic

Example:
```python
def collect_domain_data(
    self, 
    domain: str, 
    location: Optional[str] = None,
    filters: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Collect data for a specific domain using intelligent prompts.
    
    Args:
        domain: The domain to collect data for (e.g., 'cybersecurity')
        location: Optional geographic location filter
        filters: Optional dictionary of filters to apply
        
    Returns:
        Dictionary containing collected data and metadata
        
    Raises:
        ValueError: If domain is not supported
        ConnectionError: If data collection fails
    """
    # Implementation here
    pass
```

## Pull Request Process

### Before Submitting

1. **Update your fork**: Sync with the latest upstream changes
2. **Run tests**: Ensure all tests pass
3. **Run linting**: Fix any linting issues
4. **Update documentation**: Update relevant documentation
5. **Add tests**: Add tests for new functionality

### Pull Request Template

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added tests for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows the project's style guidelines
- [ ] Self-review of code completed
- [ ] Code is commented, particularly in hard-to-understand areas
- [ ] Corresponding changes to documentation made
- [ ] Changes generate no new warnings
- [ ] Added tests that prove the fix is effective or that the feature works
- [ ] New and existing unit tests pass locally

## Screenshots (if applicable)
Add screenshots to help explain your changes.

## Additional Notes
Any additional information or context.
```

### Review Process

1. **Automated checks**: CI/CD pipeline runs tests and checks
2. **Code review**: Maintainers review the code
3. **Feedback**: Address any feedback or requested changes
4. **Approval**: Once approved, the PR will be merged

## Coding Standards

### Python Code Style

- **PEP 8 compliance**: Follow Python's style guide
- **Line length**: Maximum 88 characters (Black default)
- **Imports**: Use absolute imports, group imports properly
- **Naming**: Use descriptive names for variables and functions

### Documentation Style

- **Docstrings**: Use Google-style docstrings
- **Comments**: Write clear, concise comments
- **README**: Keep README up to date
- **API docs**: Document all API endpoints

### Testing Standards

- **Unit tests**: Write unit tests for all new functions
- **Integration tests**: Add integration tests for new features
- **Test coverage**: Maintain high test coverage (>80%)
- **Test naming**: Use descriptive test names

Example test:
```python
def test_collect_cybersecurity_data_with_valid_location():
    """Test that cybersecurity data collection works with valid location."""
    datascope = DataScopeEnhanced()
    result = datascope.collect_domain_data('cybersecurity', location='federal')
    
    assert result['success'] is True
    assert result['total_items_collected'] > 0
    assert 'cybersecurity' in result['domain']
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_prompt_engine.py

# Run specific test
pytest tests/test_prompt_engine.py::test_generate_collection_prompt

# Run tests with verbose output
pytest -v

# Run tests in parallel
pytest -n auto
```

### Test Categories

- **Unit tests**: Test individual functions and classes
- **Integration tests**: Test component interactions
- **End-to-end tests**: Test complete workflows
- **Performance tests**: Test performance and scalability

### Writing Tests

1. **Test structure**: Use Arrange-Act-Assert pattern
2. **Test isolation**: Each test should be independent
3. **Mock external dependencies**: Use mocks for external services
4. **Test edge cases**: Include tests for error conditions

## Documentation

### Types of Documentation

- **Code documentation**: Docstrings and comments
- **API documentation**: REST API endpoints
- **User guides**: How-to guides and tutorials
- **Developer documentation**: Architecture and design docs

### Documentation Standards

- **Clear and concise**: Write for your audience
- **Examples**: Include code examples
- **Up to date**: Keep documentation current
- **Accessible**: Use clear language and structure

### Building Documentation

```bash
# Install documentation dependencies
pip install sphinx sphinx-rtd-theme

# Build documentation
cd docs
make html

# View documentation
open _build/html/index.html
```

## Community

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General discussions and questions
- **Discord**: Real-time chat and community support
- **Email**: team@datascope-enhanced.com

### Getting Help

1. **Search existing issues**: Check if your question has been answered
2. **Read documentation**: Check the docs and guides
3. **Ask in discussions**: Use GitHub Discussions for questions
4. **Join Discord**: Get real-time help from the community

### Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please:

- **Be respectful**: Treat everyone with respect and kindness
- **Be inclusive**: Welcome newcomers and different perspectives
- **Be constructive**: Provide helpful feedback and suggestions
- **Be patient**: Remember that everyone is learning

## Recognition

Contributors will be recognized in:

- **CONTRIBUTORS.md**: List of all contributors
- **Release notes**: Major contributions mentioned in releases
- **GitHub**: Contributor badges and statistics
- **Community**: Shout-outs in community channels

## Questions?

If you have questions about contributing, please:

1. Check this document and other documentation
2. Search existing issues and discussions
3. Create a new discussion or issue
4. Contact the maintainers directly

Thank you for contributing to DataScope Enhanced! 🚀

