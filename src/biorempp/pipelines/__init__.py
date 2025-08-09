"""
BioRemPP Analysis Pipelines Package
==================================

This package provides high-level pipeline orchestrators for the main BioRemPP
analysis workflows. Each pipeline handles the complete data processing flow
from input validation to database integration and output generation.

The pipelines are designed to be the primary interface for data processing,
combining multiple processing steps into streamlined workflows suitable for
both CLI and programmatic use.

Pipeline Functions:
    - run_biorempp_processing_pipeline: Complete BioRemPP database analysis
    - run_kegg_processing_pipeline: KEGG degradation pathways analysis
    - run_hadeg_processing_pipeline: Hydrocarbon degradation analysis
    - run_toxcsm_processing_pipeline: Toxicity prediction analysis

Pipeline Architecture:
    Each pipeline follows a consistent structure:
    1. Input validation and file reading
    2. Data parsing and format checking
    3. Database-specific merging operations
    4. Type optimization for memory efficiency
    5. Output generation and file saving
    6. Structured result reporting

Common Features:
    - Input format support
    - Comprehensive error handling and logging
    - Configurable output directories and filenames
    - Memory optimization through categorical types
    - Consistent return format with match counts and file paths

Usage Examples:
    >>> from biorempp.pipelines import run_biorempp_processing_pipeline
    >>> result = run_biorempp_processing_pipeline("input.txt")
    >>> print(f"Processed {result['matches']} matches")
"""

from .input_processing import (
    run_biorempp_processing_pipeline,
    run_hadeg_processing_pipeline,
    run_kegg_processing_pipeline,
    run_toxcsm_processing_pipeline,
)

__all__ = [
    "run_biorempp_processing_pipeline",
    "run_kegg_processing_pipeline",
    "run_hadeg_processing_pipeline",
    "run_toxcsm_processing_pipeline",
]
