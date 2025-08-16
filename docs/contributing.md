# Contributing to BioRemPP

## Overview

We welcome contributions to BioRemPP! This document provides comprehensive guidelines for contributing to the project, including development setup, coding standards, testing procedures, and submission processes.

## Table of Contents

1. [Development Environment Setup](#development-environment-setup)
2. [Project Structure](#project-structure)
3. [Contribution Areas](#contribution-areas)
4. [Development Workflow](#development-workflow)
5. [Code Quality Standards](#code-quality-standards)
6. [Testing Guidelines](#testing-guidelines)
7. [Documentation Requirements](#documentation-requirements)
8. [Continuous Integration](#continuous-integration)
9. [Release Process](#release-process)
10. [Community Guidelines](#community-guidelines)

---

## Development Environment Setup

### Prerequisites

- Python 3.8+ (recommended: 3.10+)
- Git version control system
- Code editor with Python support (recommended: VS Code, PyCharm)

### Initial Setup

```bash
# 1. Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/biorempp.git
cd biorempp

# 2. Create development environment
python -m venv biorempp-dev
source biorempp-dev/bin/activate  # Linux/macOS
# or
biorempp-dev\Scripts\activate     # Windows

# 3. Install development dependencies
pip install --upgrade pip setuptools wheel
pip install -e .[dev,testing]

# 4. Install pre-commit hooks
pre-commit install

# 5. Verify installation
biorempp --help
pytest tests/ -v
```

### Environment Configuration

Create a `.env` file for development settings:

```bash
# Development environment variables
BIOREMPP_DEBUG=true
BIOREMPP_LOG_LEVEL=DEBUG
BIOREMPP_TEST_DATA_PATH=src/biorempp/data/
```

---

## Project Structure

### Core Architecture

```
biorempp/
├── 📁 src/biorempp/          # Main package source code
│   ├── 📁 pipelines/         # Processing pipeline implementations
│   ├── 📁 input_processing/  # Data validation and parsing
│   ├── 📁 cli/              # Command-line interface
│   ├── 📁 commands/         # Command pattern implementations
│   ├── 📁 app/              # Application core and factories
│   ├── 📁 utils/            # Utility functions and helpers
│   └── 📁 data/             # Embedded database files
├── 📁 tests/                # Comprehensive test suite
├── 📁 docs/                 # Documentation source files
├── 📁 examples/             # Usage examples and tutorials
├── 📁 scripts/              # Build and deployment scripts
├── 📁 configs/              # Configuration files
└── 📁 .github/workflows/    # CI/CD pipeline definitions
```

### Key Configuration Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | Python package configuration and dependencies |
| `environment.yml` | Conda environment specification |
| `.pre-commit-config.yaml` | Code quality automation hooks |
| `release.config.js` | Semantic release configuration |
| `tox.ini` | Multi-environment testing configuration |

---

## Contribution Areas

### 1. Database Extensions

**Adding New Databases:**
- Must use KEGG Orthology (KO) identifiers as primary keys
- Include comprehensive metadata and annotations
- Provide source documentation and citation information
- Follow established CSV format with semicolon separators

**Database Integration Requirements:**
```python
# Example new database integration
def create_new_database_pipeline():
    """
    Template for new database pipeline implementation.
    Must follow established patterns for consistency.
    """
    # 1. Data validation and loading
    # 2. KO identifier mapping
    # 3. Result formatting and output
    # 4. Error handling and logging
    pass
```

### 2. CLI Enhancements

**Command Extensions:**
- New analysis options and parameters
- Enhanced output formatting capabilities
- Improved user experience features
- Advanced filtering and selection options

**Example CLI Enhancement:**
```python
# Add new command-line option
parser.add_argument(
    '--filter-pathways',
    choices=['all', 'degradation', 'synthesis'],
    help='Filter results by pathway type'
)
```

### 3. Performance Optimizations

**Focus Areas:**
- Memory usage optimization for large datasets
- Processing speed improvements
- Parallel processing implementation
- Database query optimization

**Performance Testing:**
```python
import time
import psutil

def benchmark_processing_pipeline(input_size):
    """Benchmark processing performance for optimization."""
    start_time = time.time()
    memory_before = psutil.Process().memory_info().rss

    # Run processing pipeline
    result = process_data(input_size)

    end_time = time.time()
    memory_after = psutil.Process().memory_info().rss

    return {
        'processing_time': end_time - start_time,
        'memory_delta': memory_after - memory_before,
        'throughput': input_size / (end_time - start_time)
    }
```

### 4. Feature Development

**Statistical Analysis Modules:**
- Result interpretation and visualization
- Pathway enrichment analysis
- Comparative analysis between samples
- Statistical significance testing

**Integration Modules:**
- Workflow management system integration
- API endpoints for web service deployment
- Database connectivity for external data sources

---

## Development Workflow

### 1. Issue Creation and Assignment

Before starting development:
- Check existing issues for similar work
- Create detailed issue with clear requirements
- Discuss approach with maintainers if significant
- Get assignment confirmation for large features

### 2. Branch Management

```bash
# Create feature branch
git checkout -b feature/database-extension-uniprot
git checkout -b fix/memory-optimization-large-files
git checkout -b docs/api-reference-update

# Keep branch updated
git fetch origin
git rebase origin/main
```

### 3. Development Process

```bash
# 1. Make incremental commits
git add -A
git commit -m "feat: add UniProt database integration

- Implement KO mapping for UniProt entries
- Add database loading and validation
- Include comprehensive test coverage
- Update documentation"

# 2. Run quality checks
pre-commit run --all-files
pytest tests/ --cov=biorempp
tox

# 3. Push and create pull request
git push origin feature/database-extension-uniprot
```

### 4. Pull Request Requirements

**PR Description Template:**
```markdown
## Description
Brief description of changes and motivation.

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed
- [ ] Performance testing completed (if applicable)

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests pass locally
- [ ] Changes are backwards compatible
```

---

## Code Quality Standards

### Python Style Guide

**Black Formatting:**
```bash
# Automatic code formatting
black src/ tests/ --line-length 88
```

**Import Organization:**
```python
# Standard library imports
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Union

# Third-party imports
import pandas as pd
import numpy as np
from tqdm import tqdm

# Local imports
from biorempp.utils import logger
from biorempp.pipelines.base import BasePipeline
```

**Type Annotations:**
```python
from typing import Dict, List, Optional, Union
import pandas as pd

def process_database_results(
    input_data: List[str],
    database_path: str,
    output_dir: Optional[str] = None,
    optimize_types: bool = True
) -> Dict[str, Union[int, str, float]]:
    """
    Process biological data against specified database.

    Args:
        input_data: List of KO identifiers to process
        database_path: Path to database file
        output_dir: Optional output directory
        optimize_types: Enable memory optimization

    Returns:
        Dictionary containing processing results and metadata

    Raises:
        FileNotFoundError: If database file not found
        ValueError: If input data format invalid
    """
    pass
```

### Error Handling Standards

```python
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class BioRemPPError(Exception):
    """Base exception for BioRemPP-specific errors."""
    pass

class DatabaseError(BioRemPPError):
    """Raised when database operations fail."""
    pass

class InputValidationError(BioRemPPError):
    """Raised when input validation fails."""
    pass

def safe_file_operation(file_path: str) -> Optional[str]:
    """
    Safely perform file operations with comprehensive error handling.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise InputValidationError(f"Input file not found: {file_path}")
    except PermissionError:
        logger.error(f"Permission denied: {file_path}")
        raise BioRemPPError(f"Permission denied for file: {file_path}")
    except UnicodeDecodeError:
        logger.error(f"Encoding error: {file_path}")
        raise InputValidationError(f"File encoding error: {file_path}")
```

---

## Testing Guidelines

### Test Structure

```
tests/
├── 📁 unit/              # Unit tests for individual components
│   ├── test_pipelines.py
│   ├── test_cli.py
│   ├── test_utils.py
│   └── test_databases.py
├── 📁 integration/       # Integration tests for workflows
│   ├── test_full_pipeline.py
│   └── test_cli_integration.py
├── 📁 fixtures/          # Test data and fixtures
│   ├── sample_data.txt
│   └── expected_outputs/
└── conftest.py           # Shared test configuration
```

### Testing Requirements

**Minimum Coverage:** 90% code coverage required
**Test Categories:**
- Unit tests for all public functions
- Integration tests for complete workflows
- Performance tests for optimization validation
- Error handling tests for edge cases

### Test Implementation Examples

```python
import pytest
import pandas as pd
from pathlib import Path
from biorempp.pipelines import run_biorempp_processing_pipeline

class TestBioRemPPPipeline:
    """Comprehensive test suite for BioRemPP processing pipeline."""

    @pytest.fixture
    def sample_input_data(self, tmp_path):
        """Create sample input data for testing."""
        input_file = tmp_path / "test_input.txt"
        input_file.write_text(
            ">Sample1\nK00001\nK00002\nK00003\n"
            ">Sample2\nK00004\nK00005\nK00006\n"
        )
        return str(input_file)

    def test_successful_processing(self, sample_input_data, tmp_path):
        """Test successful pipeline execution."""
        result = run_biorempp_processing_pipeline(
            input_path=sample_input_data,
            output_dir=str(tmp_path),
            optimize_types=True
        )

        assert result['status'] == 'success'
        assert result['matches'] >= 0
        assert Path(result['output_path']).exists()

    def test_invalid_input_handling(self, tmp_path):
        """Test handling of invalid input files."""
        invalid_file = tmp_path / "invalid.txt"
        invalid_file.write_text("Invalid content without proper format")

        with pytest.raises(InputValidationError):
            run_biorempp_processing_pipeline(
                input_path=str(invalid_file),
                output_dir=str(tmp_path)
            )

    @pytest.mark.performance
    def test_large_dataset_performance(self, large_dataset_fixture):
        """Test performance with large datasets."""
        start_time = time.time()
        result = run_biorempp_processing_pipeline(
            input_path=large_dataset_fixture,
            output_dir="/tmp/performance_test"
        )
        processing_time = time.time() - start_time

        # Performance assertions
        assert processing_time < 60  # Should complete within 1 minute
        assert result['throughput'] > 1000  # KO identifiers per second
```

### Running Tests

```bash
# Run all tests with coverage
pytest tests/ --cov=biorempp --cov-report=html --cov-report=term

# Run specific test categories
pytest tests/unit/ -v
pytest tests/integration/ -v
pytest -m performance tests/

# Run tests in parallel
pytest tests/ -n auto

# Generate coverage report
coverage html
open htmlcov/index.html  # View coverage report
```

---

## Documentation Requirements

### Code Documentation

**Function Documentation:**
```python
def process_biological_data(
    input_identifiers: List[str],
    database_name: str,
    output_options: Optional[Dict[str, Any]] = None
) -> ProcessingResult:
    """
    Process biological identifiers against specified database.

    This function validates input data, loads the appropriate database,
    performs matching operations, and generates structured output files
    with comprehensive metadata and statistics.

    Args:
        input_identifiers: List of KEGG Orthology identifiers (K##### format)
        database_name: Target database ('biorempp', 'kegg', 'hadeg', 'toxcsm')
        output_options: Optional configuration for output formatting
            - 'directory': Output directory path
            - 'separator': Field separator character
            - 'include_timestamp': Boolean for timestamp inclusion

    Returns:
        ProcessingResult object containing:
            - matches: Number of successful matches
            - output_path: Path to generated output file
            - processing_time: Execution time in seconds
            - statistics: Detailed matching statistics

    Raises:
        InputValidationError: If input identifiers format is invalid
        DatabaseError: If database loading or querying fails
        FileSystemError: If output generation fails

    Example:
        >>> identifiers = ['K00001', 'K00002', 'K00003']
        >>> result = process_biological_data(
        ...     input_identifiers=identifiers,
        ...     database_name='biorempp',
        ...     output_options={'directory': '/tmp/results'}
        ... )
        >>> print(f"Found {result.matches} matches")
        Found 2 matches

    Note:
        For large datasets (>10,000 identifiers), consider using
        batch processing or enabling memory optimization.
    """
    pass
```

### README and Documentation Updates

All significant changes require documentation updates:
- Update relevant sections in README.md
- Add examples for new features
- Update CLI reference documentation
- Include performance impact notes

---

## Continuous Integration

### GitHub Actions Workflows

**Continuous Integration (`.github/workflows/ci.yml`):**
- Multi-Python version testing (3.8, 3.9, 3.10, 3.11)
- Code quality checks (black, flake8, mypy)
- Test execution with coverage reporting
- Documentation building verification

**Release Management (`.github/workflows/release.yml`):**
- Automated semantic versioning
- Package building and distribution
- GitHub release creation
- PyPI publication

### Pre-commit Hooks

Automated quality checks before each commit:
```yaml
repos:
- repo: https://github.com/pre-commit/pre-commit-hooks
  rev: v4.6.0
  hooks:
  - id: trailing-whitespace
  - id: check-added-large-files
  - id: check-ast
  - id: check-json
  - id: check-yaml
  - id: end-of-file-fixer

- repo: https://github.com/psf/black
  rev: stable
  hooks:
  - id: black
    language_version: python3

- repo: https://github.com/PyCQA/flake8
  rev: 7.1.1
  hooks:
  - id: flake8

- repo: https://github.com/PyCQA/isort
  rev: 5.13.2
  hooks:
  - id: isort
```

---

## Release Process

### Semantic Versioning

BioRemPP follows [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes affecting API compatibility
- **MINOR**: New features with backward compatibility
- **PATCH**: Bug fixes and minor improvements

### Conventional Commits

Use standardized commit message format:
```bash
feat: add support for UniProt database integration
fix: resolve memory leak in large dataset processing
docs: update API reference documentation
test: add comprehensive integration tests
perf: optimize KO identifier matching algorithm
refactor: restructure database loading logic
style: apply black formatting to all modules
chore: update development dependencies

# Breaking changes
feat!: redesign CLI interface for improved usability
```

### Release Checklist

Before creating a release:
- [ ] All tests pass on supported Python versions
- [ ] Documentation is updated and complete
- [ ] CHANGELOG.md is updated with new features
- [ ] Version numbers are updated consistently
- [ ] Performance regression testing completed
- [ ] Security vulnerability scanning passed

---

## Community Guidelines

### Code of Conduct

We are committed to providing a welcoming and inclusive environment:
- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

### Communication Channels

- **GitHub Issues**: Bug reports, feature requests, technical discussions
- **GitHub Discussions**: General questions, usage help, community interaction
- **Email**: Direct contact for sensitive issues or private inquiries

### Review Process

**Pull Request Reviews:**
- All PRs require at least one maintainer approval
- Automated CI checks must pass
- Code coverage cannot decrease
- Documentation must be updated for new features

**Review Timeline:**
- Initial response within 48 hours
- Complete review within 1 week for standard PRs
- Complex features may require additional review time

### Recognition

Contributors will be recognized through:
- GitHub contributor acknowledgments
- CHANGELOG.md attribution
- Annual contributor appreciation posts
- Conference presentation acknowledgments (when applicable)

---

## Getting Help

### Documentation Resources

- Main README: Comprehensive usage guide
- CLI Reference: Complete command-line documentation
- [API Documentation](https://biorempp.readthedocs.io): Detailed API reference

### Support Channels

- **GitHub Issues**: Technical problems and bug reports
- **GitHub Discussions**: General questions and community support
- **Email Contact**: [biorempp@gmail.com](mailto:biorempp@gmail.com)

### Development Questions

For development-specific questions:
1. Check existing GitHub issues and discussions
2. Review this CONTRIBUTING.md document
3. Examine existing code for similar implementations
4. Create a new issue with detailed context

---

**Thank you for contributing to BioRemPP! Your efforts help advance computational biology and environmental bioremediation research.**
