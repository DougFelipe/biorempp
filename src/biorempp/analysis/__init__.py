"""Data processing module for BioRemPP.

This module provides the core data processing functionality for BioRemPP,
focusing exclusively on data analysis. Visualization is handled externally
through the DataFrames returned by processors.
"""

from .base_processor import BaseDataProcessor
from .gene_pathway_analysis_processing import GenePathwayAnalyzer
from .interaction_sample_compound_ import SampleCompoundInteraction
from .module_registry import registry

__all__ = [
    "GenePathwayAnalyzer",
    "BaseDataProcessor",
    "registry",
    "SampleCompoundInteraction",
]
