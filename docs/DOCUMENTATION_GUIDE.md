# BioRemPP Documentation Guide

## Overview

This guide provides comprehensive instructions for creating, maintaining, and updating the BioRemPP documentation system. The documentation uses **Sphinx** with **MyST-Parser** for Markdown support, enabling professional documentation generation with automatic API reference creation.

## Documentation Architecture

### Technology Stack

- **Sphinx**: Primary documentation generator
- **MyST-Parser**: Markdown support for Sphinx
- **sphinx-apidoc**: Automatic API documentation generation
- **Alabaster Theme**: Clean, professional theme
- **ReadTheDocs**: Deployment platform

### Directory Structure

```
docs/
├── Makefile                 # Build automation for documentation
├── conf.py                  # Sphinx configuration file
├── requirements.txt         # Documentation dependencies
├── index.md                 # Main documentation homepage
├── readme.md               # Project overview (symlinked from root)
├── contributing.md         # Contribution guidelines
├── changelog.md            # Version history and changes
├── authors.md              # Project contributors
├── license.md              # License information
├── api/                    # Auto-generated API documentation
│   ├── modules.rst         # Main API modules index
│   ├── biorempp.rst        # Main package documentation
│   ├── biorempp.*.rst      # Individual module documentation
│   └── ...
├── _build/                 # Generated documentation output
│   └── html/               # HTML documentation files
├── _static/                # Static assets (images, CSS, JS)
└── _templates/             # Custom Sphinx templates
```

## Getting Started

### Prerequisites

1. **Python Environment**: Ensure you have the BioRemPP conda environment activated
2. **Documentation Dependencies**: Install required packages

```bash
# Navigate to docs directory
cd docs/

# Install documentation requirements
pip install -r requirements.txt
```

### Building Documentation

#### Direct build

```bash
# From docs/ directory
python -m sphinx -M html . _build
```

python -m sphinx -M html . _build

#### Quick Build (HTML)

```bash
# From docs/ directory
make html
```

#### Clean Build (Remove previous builds)

```bash
# Clean previous builds
make clean

# Build fresh documentation
make html
```

#### View Documentation

```bash
# Open in browser (Windows)
start _build/html/index.html

# Open in browser (Linux/Mac)
open _build/html/index.html
```

## Documentation Configuration

### Main Configuration (conf.py)

The `conf.py` file contains all Sphinx configuration:

#### Key Settings

```python
# Project information
project = "biorempp"
copyright = "2025, Douglas"

# Extensions for enhanced functionality
extensions = [
    "sphinx.ext.autodoc",        # Automatic documentation from docstrings
    "sphinx.ext.autosummary",    # Generate summary tables
    "sphinx.ext.viewcode",       # Add source code links
    "sphinx.ext.napoleon",       # Google/NumPy style docstrings
    "myst_parser",               # Markdown support
]

# MyST-Parser configuration for advanced Markdown
myst_enable_extensions = [
    "amsmath",          # Math expressions
    "colon_fence",      # ::: fenced blocks
    "deflist",          # Definition lists
    "dollarmath",       # $ math expressions
    "html_image",       # HTML image support
    "linkify",          # Auto-link URLs
    "replacements",     # Text replacements
    "smartquotes",      # Smart quotes
    "substitution",     # Variable substitution
    "tasklist",         # Task lists with checkboxes
]
```

#### Automatic API Generation

The configuration automatically runs `sphinx-apidoc` to generate API documentation:

```python
# Automatic API documentation generation
output_dir = os.path.join(__location__, "api")
module_dir = os.path.join(__location__, "../src/biorempp")

# Clean and regenerate API docs
shutil.rmtree(output_dir)
apidoc.main(args)
```

## Content Creation

### Writing Documentation Pages

#### Markdown Format

Use MyST-flavored Markdown for documentation pages:

```markdown
# Page Title

## Section Heading

This is regular text with **bold** and *italic* formatting.

### Code Examples

```python
from biorempp.pipelines import run_biorempp_processing_pipeline

result = run_biorempp_processing_pipeline(
    input_file="samples.txt",
    output_dir="results"
)
```

### Cross-References

Link to other documentation:
- {doc}`readme` - Link to readme page
- {ref}`genindex` - Link to general index
- {mod}`biorempp.pipelines` - Link to module

### Admonitions

```{note}
This is an informational note.
```

```{warning}
This is a warning message.
```

```{important}
This is important information.
```
```

#### Table of Contents

Add pages to the main table of contents in `index.md`:

```markdown
```{toctree}
:maxdepth: 2

Overview <readme>
Installation <installation>
User Guide <user_guide>
API Reference <api/modules>
Contributing <contributing>
```
```

### API Documentation

#### Docstring Standards

Follow NumPy/Google style docstrings for automatic API generation:

```python
def process_biological_data(input_file: str, database: str) -> Dict[str, Any]:
    """
    Process biological data using specified database.

    This function performs comprehensive biological data analysis by merging
    input sequences with the specified database and generating analysis results.

    Parameters
    ----------
    input_file : str
        Path to the input biological data file containing sequences.
    database : str
        Database name for analysis ('biorempp', 'hadeg', 'kegg', 'toxcsm').

    Returns
    -------
    Dict[str, Any]
        Processing results containing:
        - 'output_path': Path to generated results file
        - 'matches': Number of successful matches found
        - 'processing_time': Time taken for analysis

    Raises
    ------
    FileNotFoundError
        If the input file cannot be found or accessed.
    ValueError
        If the database name is not supported.

    Examples
    --------
    >>> result = process_biological_data("samples.txt", "biorempp")
    >>> print(f"Found {result['matches']} matches")
    Found 7613 matches

    Notes
    -----
    This function requires the input file to be in the correct format with
    organism headers (>) followed by KO identifiers.
    """
```

#### Module Documentation

Each module should have a comprehensive docstring:

```python
"""
BioRemPP Data Processing Pipeline Module.

This module implements the core data processing pipelines for bioremediation
analysis, providing comprehensive workflows for biological data analysis
across multiple databases and processing strategies.

Key Features
-----------
- Multi-database processing support
- Standardized output formatting
- Error handling and validation
- Performance optimization

Examples
--------
    from biorempp.pipelines import run_biorempp_processing_pipeline

    result = run_biorempp_processing_pipeline(
        input_file="biological_data.txt",
        output_dir="analysis_results"
    )
"""
```

## Advanced Features

### Custom Directives

#### Code Blocks with Line Numbers

```python
:linenos:
:emphasize-lines: 2, 3

def example_function():
    important_line = "This line is highlighted"
    another_important_line = "This too"
    return important_line
```

#### Cross-References

```markdown
See the {func}`biorempp.pipelines.run_biorempp_processing_pipeline` function
for more details about processing workflows.

Refer to the {class}`biorempp.utils.EnhancedErrorHandler` class for
error handling capabilities.
```

#### Mathematical Expressions

```markdown
The biodegradation efficiency can be calculated using:

$$E = \frac{N_{matches}}{N_{total}} \times 100$$

Where $N_{matches}$ is the number of successful matches and $N_{total}$
is the total number of input sequences.
```

### Custom Styling

#### CSS Customization

Add custom styles in `_static/custom.css`:

```css
/* Custom styling for BioRemPP documentation */
.biorempp-highlight {
    background-color: #e8f4fd;
    border-left: 4px solid #2196F3;
    padding: 10px;
    margin: 10px 0;
}

.code-example {
    background-color: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 4px;
    padding: 15px;
}
```

## Updating Documentation

### When to Update Documentation

1. **New Features**: Document any new functionality or modules
2. **API Changes**: Update docstrings and examples for modified functions
3. **Configuration Changes**: Update installation or setup instructions
4. **Bug Fixes**: Document resolved issues and their solutions
5. **Performance Improvements**: Document optimization changes

### Documentation Update Workflow

#### 1. Update Source Code Documentation

```bash
# Ensure docstrings are complete and accurate
# Follow NumPy/Google docstring conventions
# Include examples and type hints
```

#### 2. Update Markdown Content

```bash
# Edit relevant .md files in docs/
# Update examples and usage instructions
# Add new sections as needed
```

#### 3. Regenerate API Documentation

```bash
# Clean previous builds
make clean

# Generate fresh API documentation
make html
```

#### 4. Review and Test

```bash
# Open documentation in browser
start _build/html/index.html

# Check for:
# - Broken links
# - Missing sections
# - Formatting issues
# - Incorrect examples
```

#### 5. Version Control

```bash
# Commit documentation changes
git add docs/
git commit -m "docs: Update documentation for v0.5.0"
```

### Automated Documentation Updates

#### CI/CD Integration

Consider adding documentation builds to your CI/CD pipeline:

```yaml
# .github/workflows/docs.yml
name: Documentation

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build-docs:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        pip install -r docs/requirements.txt
        pip install -e .
    - name: Build documentation
      run: |
        cd docs
        make html
    - name: Deploy to GitHub Pages
      if: github.ref == 'refs/heads/main'
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./docs/_build/html
```

## Troubleshooting

### Common Issues

#### 1. Import Errors During Build

**Problem**: ModuleNotFoundError when building documentation

**Solution**:
```bash
# Ensure BioRemPP is installed in development mode
pip install -e .

# Check Python path in conf.py
sys.path.insert(0, os.path.join(__location__, "../src"))
```

#### 2. Missing API Documentation

**Problem**: API pages not generating or updating

**Solution**:
```bash
# Clean and rebuild
make clean
rm -rf api/
make html
```

#### 3. Markdown Not Rendering

**Problem**: MyST-Parser not processing Markdown correctly

**Solution**:
```python
# Check conf.py for proper MyST configuration
extensions.append("myst_parser")
source_suffix = [".rst", ".md"]
```

#### 4. Cross-References Broken

**Problem**: Links between documentation pages not working

**Solution**:
```markdown
# Use proper MyST syntax
{doc}`readme`           # Link to document
{ref}`section-label`    # Link to section
{func}`module.function` # Link to function
```

### Build Errors

#### Sphinx Warnings

Monitor build output for warnings:

```bash
# Build with verbose output
make html SPHINXOPTS="-v"

# Build treating warnings as errors
make html SPHINXOPTS="-W"
```

#### Missing Dependencies

Ensure all documentation dependencies are installed:

```bash
# Install/update documentation requirements
pip install -r docs/requirements.txt

# Install BioRemPP in development mode
pip install -e .
```

## Best Practices

### 1. Documentation Standards

- **Consistency**: Use consistent formatting and style throughout
- **Completeness**: Document all public functions, classes, and modules
- **Clarity**: Write clear, concise explanations with examples
- **Maintenance**: Keep documentation synchronized with code changes

### 2. Content Organization

- **Logical Structure**: Organize content in a logical hierarchy
- **Progressive Disclosure**: Start with overview, then dive into details
- **Cross-Linking**: Use appropriate cross-references between sections
- **Search Optimization**: Use descriptive headings and keywords

### 3. Code Examples

- **Realistic Examples**: Provide practical, working examples
- **Complete Context**: Include necessary imports and setup
- **Expected Output**: Show what users should expect to see
- **Error Handling**: Include examples of error handling

### 4. Version Management

- **Changelog**: Maintain detailed changelog for documentation updates
- **Version Tags**: Tag documentation versions with releases
- **Backward Compatibility**: Note any breaking changes clearly
- **Migration Guides**: Provide guidance for major version changes

## Deployment

### Local Development

```bash
# Serve documentation locally for development
cd docs
make html
python -m http.server 8000 -d _build/html
# Visit http://localhost:8000
```

### ReadTheDocs Deployment

1. **Connect Repository**: Link GitHub repository to ReadTheDocs
2. **Configuration**: Ensure `.readthedocs.yml` is properly configured
3. **Dependencies**: Verify `docs/requirements.txt` includes all dependencies
4. **Build Settings**: Configure Python version and build environment

### GitHub Pages Deployment

```bash
# Manual deployment to GitHub Pages
git checkout gh-pages
git merge main
cd docs
make html
cp -r _build/html/* ../
git add .
git commit -m "Update documentation"
git push origin gh-pages
```

## Conclusion

This guide provides the foundation for maintaining high-quality documentation for BioRemPP. Regular updates, consistent formatting, and thorough testing ensure that users have access to accurate, helpful documentation that enhances their experience with the software.

For questions or suggestions about documentation, please refer to the contributing guidelines or open an issue in the project repository.
