"""
    Input Processing and Database Integration Module for BioRemPP
=============================================================
============================================================

This package provides comprehensive functionality for processing biological
input data and integrating it with multiple reference databases for
bioremediation analysis. It handles the complete data pipeline from raw
input validation to database-merged datasets ready for downstream analysis.

Core Functionality
------------------
- Input file validation and format checking
- Data parsing
- Base64 decoding for web upload support
- Multi-database integration (BioRemPP, KEGG, HADEG, ToxCSM)
- Memory optimization through categorical data types
- Comprehensive error handling and logging

Supported Databases
-------------------
1. **BioRemPP Database**: Comprehensive bioremediation database
2. **KEGG Database**: Degradation pathway information from KEGG
3. **HADEG Database**: Hydrocarbon degradation gene information
4. **ToxCSM Database**: Toxicity predictions and chemical properties

Input Format
------------
Expected input follows structure:
    >Sample_ID_1
    K00001
    K00002
    >Sample_ID_2
    K00003

Public Interface
----------------
---------------
Main pipeline functions:
    - load_and_merge_input: Complete validation and merge pipeline
    - validate_and_process_input: Input validation and parsing

Database-specific merge functions:
    - merge_input_with_biorempp: BioRemPP database integration
    - merge_input_with_kegg: KEGG pathway database integration
    - merge_input_with_hadeg: HADEG database integration
    - merge_input_with_toxcsm: ToxCSM toxicity database integration

Memory optimization functions:
    - optimize_dtypes_biorempp: BioRemPP data optimization
    - optimize_dtypes_kegg: KEGG data optimization
    - optimize_dtypes_hadeg: HADEG data optimization
    - optimize_dtypes_toxcsm: ToxCSM data optimization

Usage Examples
--------------
Basic pipeline usage:
    >>> from biorempp.input_processing import load_and_merge_input
    >>> content = ">Sample1\\nK00001\\nK00002"
    >>> df, error = load_and_merge_input(content, "input.txt")

Direct database merging:
    >>> from biorempp.input_processing import merge_input_with_kegg
    >>> result_df = merge_input_with_kegg(input_df)
"""

from .biorempp_merge_processing import (
    merge_input_with_biorempp,
    optimize_dtypes_biorempp,
)
from .hadeg_merge_processing import merge_input_with_hadeg, optimize_dtypes_hadeg
from .input_loader import load_and_merge_input
from .input_validator import validate_and_process_input
from .kegg_merge_processing import merge_input_with_kegg, optimize_dtypes_kegg
from .toxcsm_merge_processing import merge_input_with_toxcsm, optimize_dtypes_toxcsm

__all__ = [
    "validate_and_process_input",
    "merge_input_with_biorempp",
    "merge_input_with_kegg",
    "merge_input_with_hadeg",
    "merge_input_with_toxcsm",
    "optimize_dtypes_biorempp",
    "optimize_dtypes_kegg",
    "optimize_dtypes_hadeg",
    "optimize_dtypes_toxcsm",
    "load_and_merge_input",
]
