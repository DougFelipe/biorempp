# Configuration file for the Sphinx documentation builder.
# BioRemPP documentation configuration

import os
import sys
from pathlib import Path

# Add the project source to the path
docs_dir = Path(__file__).parent
project_dir = docs_dir.parent
src_dir = project_dir / "src"
sys.path.insert(0, str(src_dir))

# -- Project information -----------------------------------------------------
project = 'BioRemPP'
copyright = '2025, Douglas Felipe'
author = 'Douglas Felipe'

# Try to get version from package
try:
    from importlib.metadata import version
    release = version("biorempp")
except Exception:
    release = "0.1.0-dev"

version = release.split('+')[0]  # Short version

# -- General configuration ---------------------------------------------------
extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
]

# MyST configuration
myst_enable_extensions = [
    "colon_fence",
    "deflist", 
    "dollarmath",
    "html_image",
    "linkify",
    "smartquotes",
    "substitution",
    "tasklist",
]

# Source parsers
source_suffix = ['.rst', '.md']

# Master document
master_doc = 'index'
root_doc = 'index'

# Exclude patterns
exclude_patterns = [
    '_build', 
    'Thumbs.db', 
    '.DS_Store',
    '.venv',
    'temp_md',
    'outputs'
]

# Templates
templates_path = ['_templates']

# Internationalization
language = 'en'

# Mock imports for documentation
autodoc_mock_imports = [
    'numpy', 'pandas', 'scipy', 'matplotlib', 'sklearn',
    'tqdm', 'click', 'dash', 'plotly'
]

# Suppress specific warnings
suppress_warnings = [
    'myst.header',
    'myst.xref_missing',
    'myst.iref_ambiguous',
    'autodoc.import_object',
]

# Nitpicky mode configuration
nitpicky = False
nitpick_ignore = [
    ('py:class', 'optional'),
    ('py:class', 'callable'),
    ('py:class', 'pd.DataFrame'),
    ('py:class', 'default=None'),
    ('py:class', 'default "INFO"'),
    ('py:class', 'default True'),
    ('py:class', 'default "detailed"'),
]

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Theme options
html_theme_options = {
    'collapse_navigation': False,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

# -- Extension configuration -------------------------------------------------
# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False

# Autodoc settings
autodoc_typehints = 'description'
autodoc_typehints_description_target = 'documented'
autosummary_generate = True

# Intersphinx
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable', None),
    'pandas': ('https://pandas.pydata.org/docs', None),
    'matplotlib': ('https://matplotlib.org/stable', None),
}

# Print configuration loaded
print(f"Sphinx configuration loaded for {project} {version}", file=sys.stderr)
