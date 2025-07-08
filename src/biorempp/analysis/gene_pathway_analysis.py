"""
Gene pathway analysis module for BioRemPP.

This module provides functionality for analyzing gene and pathway data
from post-merge BioRemPP results, including KO counting analysis.
"""

import pandas as pd

from biorempp.utils.logging_config import get_logger

logger = get_logger("analysis.gene_pathway_analysis")


class GenePathwayAnalyzer:
    """
    Analyzer for gene pathway data from BioRemPP pipeline results.

    This class provides methods for analyzing post-merge data including
    KO counting and other statistical analyses.

    Attributes
    ----------
    logger : logging.Logger
        Logger instance for this analyzer.
    """

    def __init__(self):
        """Initialize the GenePathwayAnalyzer."""
        self.logger = logger
        self.logger.info("GenePathwayAnalyzer initialized")

    def _validate_dataframe(self, df: pd.DataFrame, required_columns: list) -> None:
        """
        Validate that DataFrame has required columns.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame to validate.
        required_columns : list
            List of required column names.

        Raises
        ------
        ValueError
            If DataFrame is empty or missing required columns.
        TypeError
            If input is not a pandas DataFrame.
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame")

        if df.empty:
            raise ValueError("DataFrame cannot be empty")

        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        self.logger.debug(f"DataFrame validation passed: {df.shape}")

    def analyze_ko_counts_per_sample(self, merged_df: pd.DataFrame) -> pd.DataFrame:
        """
        Analyze KO counts per sample from post-merge BioRemPP data.

        This function processes the merged DataFrame from BioRemPP pipeline
        to count unique KO (KEGG Orthology) identifiers per sample, providing
        insights into the functional diversity of each sample.

        Parameters
        ----------
        merged_df : pd.DataFrame
            Post-merge DataFrame from BioRemPP pipeline containing at least
            'sample' and 'ko' columns.

        Returns
        -------
        pd.DataFrame
            DataFrame with columns ['sample', 'ko_count'] sorted in descending
            order by KO count. Each row represents a sample and its unique
            KO count.

        Raises
        ------
        TypeError
            If input is not a pandas DataFrame.
        ValueError
            If DataFrame is empty or missing required columns.

        Examples
        --------
        >>> analyzer = GenePathwayAnalyzer()
        >>> df = pd.DataFrame({
        ...     'sample': ['Sample1', 'Sample1', 'Sample2'],
        ...     'ko': ['K00001', 'K00002', 'K00001']
        ... })
        >>> result = analyzer.analyze_ko_counts_per_sample(df)
        >>> print(result)
           sample  ko_count
        0  Sample1         2
        1  Sample2         1
        """
        self.logger.info("Starting KO counts analysis per sample")

        # Validate input DataFrame
        required_columns = ["sample", "ko"]
        self._validate_dataframe(merged_df, required_columns)

        # Count unique KOs per sample
        self.logger.info("Counting unique KOs per sample...")
        ko_counts = (
            merged_df.groupby("sample")["ko"].nunique().reset_index(name="ko_count")
        )

        # Sort by KO count in descending order
        ko_counts_sorted = ko_counts.sort_values("ko_count", ascending=False)

        self.logger.info(
            f"KO analysis completed. Processed {len(ko_counts_sorted)} samples"
        )
        self.logger.debug(f"KO counts summary:\n{ko_counts_sorted.head()}")

        return ko_counts_sorted
