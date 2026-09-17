# Contributing to Motus

Thank you for your interest in contributing to Motus. This document provides guidelines and instructions for contributing to this project.

## Development Setup

### Prerequisites

- Python 3.10 or higher
- macOS (for full functionality) or Linux (limited functionality)
- Webcam
- Git

### Local Development Environment

1. **Clone the repository:**

```bash
git clone https://github.com/JaKuba23/gesture-volume-control.git
cd gesture-volume-control
```

2. **Create and activate virtual environment:**

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
```

3. **Install dependencies:**

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -e .
```

4. **Install pre-commit hooks:**

```bash
pre-commit install
```

5. **Run tests to verify setup:**

```bash
pytest
```

## Coding Standards

### Python Style Guide

This project follows strict Python coding standards:

- **PEP 8** compliance enforced by `flake8`
- **Black** for code formatting (line length: 88)
- **isort** for import sorting
- **Type hints** required for all functions (mypy strict mode)
- **Docstrings** required for all public modules, classes, and functions (Google style)

### Code Formatting

Before committing, ensure your code is properly formatted:

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Check formatting
black --check src/ tests/
isort --check-only src/ tests/
```

### Linting

Run linters to check code quality:

```bash
# Run flake8
flake8 src/ tests/

# Run mypy type checking
mypy src/motus --strict
```

### Security

Run security scans before submitting:

```bash
# Check for security issues
bandit -r src/motus

# Check for vulnerable dependencies
safety check
```

## Testing Requirements

### Test Coverage

- **Minimum coverage:** 80% (enforced by CI)
- All new features must include tests
- Bug fixes should include regression tests

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=motus --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_gestures.py

# Run specific test
pytest tests/unit/test_gestures.py::TestCountOpenFingers::test_open_hand_returns_five
```

### Test Organization

- **Unit tests:** `tests/unit/` - Test individual functions and classes
- **Integration tests:** `tests/integration/` - Test component interactions
- **Markers:** Use `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.slow`

### Writing Tests

```python
"""Test module docstring."""

import pytest
from motus.module import function


class TestFeature:
    """Test class for specific feature."""
    
    def test_specific_behavior(self):
        """Test description."""
        # Arrange
        input_data = ...
        
        # Act
        result = function(input_data)
        
        # Assert
        assert result == expected
```

## Pull Request Process

### Before Submitting

1. **Create a feature branch:**

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

2. **Make your changes** following coding standards

3. **Add tests** for your changes

4. **Run the full test suite:**

```bash
# Format and lint
black src/ tests/
isort src/ tests/
flake8 src/ tests/
mypy src/motus --strict

# Run tests
pytest --cov=motus --cov-report=term-missing

# Security scan
bandit -r src/motus
```

5. **Commit with clear messages:**

```bash
git commit -m "feat: add new gesture detection algorithm"
git commit -m "fix: resolve camera initialization error on M1 Macs"
git commit -m "docs: update README with troubleshooting section"
```

### Commit Message Format

Use conventional commits:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks
- `perf:` - Performance improvements

### Pull Request Guidelines

1. **Title:** Clear, descriptive title following conventional commits
2. **Description:** Use the PR template, fill all sections
3. **Tests:** Include test results and coverage report
4. **Documentation:** Update docs if your PR changes functionality
5. **Breaking changes:** Clearly document any breaking changes

### Review Process

- All PRs require review by @JaKuba23
- CI checks must pass (lint, type check, tests, security)
- Coverage must remain above 80%
- Address all review comments before merge

## Branch Strategy

- `main` - Production-ready code, protected
- `develop` - Integration branch for features
- `feature/*` - New features
- `fix/*` - Bug fixes
- `docs/*` - Documentation improvements

## Issue Guidelines

### Reporting Bugs

Use the bug report template and include:

- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Relevant logs or error messages

### Suggesting Features

Use the feature request template and include:

- Problem statement
- Proposed solution
- Alternatives considered
- Use cases and benefits

## Development Commands

### Makefile Targets

```bash
make run           # Run application
make test          # Run tests
make coverage      # Generate coverage report
make lint          # Run linters
make format        # Format code
make type-check    # Run type checking
make security-scan # Run security scans
make clean         # Clean build artifacts
make install-dev   # Install development dependencies
```

## Architecture Guidelines

### Module Organization

```
src/motus/
├── __init__.py         # Package initialization
├── main.py             # Application entry point
├── config.py           # Configuration management
├── hand_tracking.py    # Hand detection logic
├── gestures.py         # Gesture recognition
└── mac_controls.py     # Platform-specific controls
```

### Adding New Features

1. Design the feature with clear interfaces
2. Add configuration options to `config.py` if needed
3. Implement with proper type hints and docstrings
4. Write comprehensive tests
5. Update documentation
6. Add examples to README if user-facing

## Performance Considerations

- Minimize camera processing overhead
- Use efficient NumPy operations

## Documentation Standards

- All public APIs must have docstrings
- Use Google-style docstrings
- Include type hints in function signatures
- Provide usage examples for complex features
- Keep README up to date

## Getting Help

- Check existing issues and documentation
- Ask questions using the question issue template
- Contact @JaKuba23 for maintainer-specific questions

## License

By contributing to Motus, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Motus!

