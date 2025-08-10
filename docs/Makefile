# -----------------------------------------------------------------------------
# Cross-platform Makefile for Sphinx docs (works well on Windows/MSYS2)
# - Calls Sphinx via `python -m sphinx` to avoid PATH issues
# - Generates API stubs with sphinx-apidoc before building HTML
# - Tweak PACKAGE if your import root differs
# -----------------------------------------------------------------------------

# Python/Sphinx entry points (overridable via env)
PY            ?= python
SPHINXBUILD   ?= $(PY) -m sphinx
SPHINXAPIDOC  ?= $(PY) -m sphinx.ext.apidoc

# Paths
SOURCEDIR     := .
BUILDDIR      := _build
AUTODOCDIR    := api

# Package import root (adjust to your project)
# For src layout, docs live in:   biorempp/ docs/
# Code lives in:                  biorempp/ src/biorempp/
PACKAGE       ?= biorempp

# Sphinx options:
#  -n nitpicky (stricter ref checking)
#  -T full tracebacks on errors
# Tip: add -W to fail on warnings (great for CI)
SPHINXOPTS    ?= -n -T
#SPHINXOPTS   ?= -n -T -W

.PHONY: help clean clean-api api html linkcheck doctest dirhtml latexpdf

# Default target: show Sphinx make-mode help
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

# Clean build artifacts (HTML, doctrees) and API stubs
clean:
	rm -rf "$(BUILDDIR)"/* "$(AUTODOCDIR)"

# Clean only API stubs
clean-api:
	rm -rf "$(AUTODOCDIR)"

# Generate API stubs from package source
# -f: overwrite
# -e: separate pages per module
# -M: include module __all__ members in autosummary
api: clean-api
	$(SPHINXAPIDOC) -o "$(AUTODOCDIR)" ../src/$(PACKAGE) -f -e -M --implicit-namespaces

# Build HTML (ensures API stubs are up-to-date first)
html: api
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

# Useful extras
linkcheck:
	@$(SPHINXBUILD) -M linkcheck "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

doctest:
	@$(SPHINXBUILD) -M doctest "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

dirhtml:
	@$(SPHINXBUILD) -M dirhtml "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

latexpdf:
	@$(SPHINXBUILD) -M latexpdf "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

# Catch-all: route unknown targets to Sphinx make-mode
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)
