"""
Input processing and validation module for BioRemPP.

This sub-package contains functions and utilities for:
    - Loading FASTA-like files
    - Validating input format and content
    - Decoding base64 files
    - Preparing and optimizing DataFrames for analysis pipeline
    - Merging input data with functional reference databases

Main public functions:
    - validate_and_process_input: Validates and extracts samples and KOs from
      input to DataFrame
    - merge_input_with_biorempp: Merges validated input with BioRemPP
      database (CSV)
    - merge_input_with_kegg: Merges validated input with KEGG degradation
      pathways database (CSV)
    - merge_input_with_hadeg: Merges validated input with HADEG
      database (CSV)
    - optimize_dtypes_biorempp: Optimizes categorical columns for memory
      reduction
    - optimize_dtypes_kegg: Optimizes categorical columns for KEGG data
    - optimize_dtypes_hadeg: Optimizes categorical columns for HADEG data
    - load_and_merge_input: Validation and merge pipeline, ready for CLI or
      interface use
"""

from .biorempp_merge_processing import (
    merge_input_with_biorempp,
    optimize_dtypes_biorempp,
)
from .hadeg_merge_processing import merge_input_with_hadeg, optimize_dtypes_hadeg
from .input_loader import load_and_merge_input
from .input_validator import validate_and_process_input
from .kegg_merge_processing import merge_input_with_kegg, optimize_dtypes_kegg

__all__ = [
    "validate_and_process_input",
    "merge_input_with_biorempp",
    "merge_input_with_kegg",
    "merge_input_with_hadeg",
    "optimize_dtypes_biorempp",
    "optimize_dtypes_kegg",
    "optimize_dtypes_hadeg",
    "load_and_merge_input",
]
