# -----------------------------------------------------------------------------
# Sphinx configuration for BioRemPP
# - Read the Docs theme
# - Version derived from installed package (importlib.metadata)
# - Mocks heavy runtime deps to keep builds fast/stable
# - Compatible with src/ layout and MSYS2/Windows
# -----------------------------------------------------------------------------

import os
import sys
from importlib.metadata import version as pkg_version, PackageNotFoundError

# --- Paths -------------------------------------------------------------------
# Add ../src to sys.path for local builds (RTD typically installs the package)
__location__ = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(__location__, "../src"))

# --- Project info ------------------------------------------------------------
project = "biorempp"
author = "Douglas Felipe"
language = "en"  # keep docs in English

# Derive release/version from the installed package; fall back if not installed
try:
    release = pkg_version("biorempp")
except PackageNotFoundError:
    release = "0+unknown"
version = release  # If you want X.Y only, slice here.

# --- General configuration ----------------------------------------------------
extensions = [
    # Content & authoring
    "myst_parser",                # Markdown via MyST

    # API & code docs
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",        # Google/NumPy docstring styles
    "sphinx.ext.viewcode",

    # Utility & quality gates
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.ifconfig",
    "sphinx.ext.mathjax",
]

# MyST: enable useful Markdown features
myst_enable_extensions = [
    "amsmath", "colon_fence", "deflist", "dollarmath",
    "html_image", "linkify", "replacements", "smartquotes",
    "substitution", "tasklist",
]

# Accepted source file types
source_suffix = [".rst", ".md"]

# Root document (replaces deprecated `master_doc`)
root_doc = "index"

# Templates and excludes
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", ".venv"]

# Autodoc / Napoleon / Autosummary for cleaner API docs
autodoc_typehints = "description"
autoclass_content = "class"         # only class docstring (not __init__)
autosummary_generate = True
autosummary_imported_members = True
todo_emit_warnings = True

# --- Mock heavy dependencies --------------------------------------------------
# Keep this aligned with your install_requires / optional extras.
# This avoids importing heavy C extensions on RTD or local minimal envs.
autodoc_mock_imports = [
    "numpy", "pandas", "scipy", "matplotlib", "sklearn",
    "tqdm", "click", "dash", "dash_bootstrap_components",
]

# --- HTML output --------------------------------------------------------------
html_theme = "sphinx_rtd_theme"   # make sure it's in requirements.txt
html_static_path = ["_static"]
html_theme_options = {
    # Example options (uncomment/tune as needed):
    # "collapse_navigation": False,
    # "navigation_depth": 3,
}
htmlhelp_basename = "biorempp-doc"

# --- LaTeX (PDF) output -------------------------------------------------------
latex_elements = {}
latex_documents = [
    ("index", "user_guide.tex", "biorempp Documentation", author, "manual")
]

# --- Intersphinx mappings -----------------------------------------------------
python_version = ".".join(map(str, sys.version_info[0:2]))
intersphinx_mapping = {
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
    "python": (f"https://docs.python.org/{python_version}", None),
    "matplotlib": ("https://matplotlib.org/stable", None),
    "numpy": ("https://numpy.org/doc/stable", None),
    "sklearn": ("https://scikit-learn.org/stable", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/reference", None),
    "setuptools": ("https://setuptools.pypa.io/en/stable/", None),
}

# --- Optional: auto-generate API stubs on config load -------------------------
# Prefer Makefile target `api`, but this is handy on RTD/CI if you set env var.
# Set RUN_SPHINX_APIDOC=1 to enable (default on).
if os.environ.get("RUN_SPHINX_APIDOC", "1") == "1":
    try:
        from sphinx.ext.apidoc import main as apidoc_main
    except Exception:
        try:
            from sphinx.apidoc import main as apidoc_main  # type: ignore[assignment]
        except Exception:
            apidoc_main = None

    if apidoc_main:
        import shutil
        out = os.path.join(__location__, "api")
        # Source path for src layout:
        src = os.path.join(__location__, "../src/biorempp")
        try:
            shutil.rmtree(out)
        except FileNotFoundError:
            pass
        apidoc_main(["-f", "-o", out, src, "--implicit-namespaces"])

# Log to stderr to confirm config loaded (useful to debug RTD/CI)
print(f"loading configurations for {project} {version} ...", file=sys.stderr)
