"""Data processing module for BioRemPP.

This module provides the core data processing functionality for BioRemPP,
focusing exclusively on data analysis. Visualization is handled externally
through the DataFrames returned by processors.
"""

from .base_processor import BaseDataProcessor
from .gene_pathway_analysis_processing import GenePathwayAnalyzer
from .module_registry import registry
from .sample_compound_interaction_processing import SampleCompoundInteraction

__all__ = [
    "GenePathwayAnalyzer",
    "BaseDataProcessor",
    "registry",
    "SampleCompoundInteraction",
]
