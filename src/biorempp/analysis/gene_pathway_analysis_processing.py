"""
Gene pathway analysis module for BioRemPP.

This module provides functionality for analyzing gene and pathway data
from post-merge BioRemPP results, including KO counting analysis.
"""

import pandas as pd

from biorempp.analysis.base_processor import BaseDataProcessor
from biorempp.utils.logging_config import get_logger

logger = get_logger("analysis.gene_pathway_analysis")


class GenePathwayAnalyzer(BaseDataProcessor):
    """
    Analyzer for gene pathway data from BioRemPP pipeline results.

    This class provides methods for analyzing post-merge data including
    KO counting and other statistical analyses, following the modular
    architecture pattern.

    Attributes
    ----------
    logger : logging.Logger
        Logger instance for this analyzer.
    """

    def __init__(self):
        """Initialize the GenePathwayAnalyzer."""
        super().__init__(
            name="gene_pathway_analyzer",
            description="Analyzes KO counts per sample from BioRemPP data",
        )

    @property
    def required_columns(self) -> list:
        """Return required columns for gene pathway analysis."""
        return ["sample", "ko"]

    @property
    def output_columns(self) -> list:
        """Return output columns from gene pathway analysis."""
        return ["sample", "ko_count"]

    def process(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """
        Process gene pathway data and return KO counts per sample.

        This is the main processing method that wraps the existing
        analyze_ko_counts_per_sample functionality.

        Parameters
        ----------
        data : pd.DataFrame
            Input DataFrame with BioRemPP post-merge data
        **kwargs
            Additional parameters (unused for this processor)

        Returns
        -------
        pd.DataFrame
            DataFrame with KO counts per sample
        """
        self.validate_input(data)
        return self.analyze_ko_counts_per_sample(data)

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
        self.validate_input(merged_df)

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

    def analyze_ko_per_pathway_per_sample(
        self, merged_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Count unique KOs for each pathway in each sample.

        This method processes the merged DataFrame from BioRemPP pipeline
        to count unique KO (KEGG Orthology) identifiers per pathway in each sample,
        providing insights into pathway diversity across samples.

        Parameters
        ----------
        merged_df : pd.DataFrame
            DataFrame resultante da fusão com os dados KEGG, contendo colunas
            'sample', 'pathname' e 'ko'.

        Returns
        -------
        pd.DataFrame
            DataFrame with columns ['sample', 'pathname', 'unique_ko_count']
            containing unique KO counts per pathway for each sample.

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
        ...     'pathname': ['Pathway1', 'Pathway2', 'Pathway1'],
        ...     'ko': ['K00001', 'K00002', 'K00001']
        ... })
        >>> result = analyzer.analyze_ko_per_pathway_per_sample(df)
        """
        self.logger.info("Starting KO counts analysis per pathway per sample")

        # Validate required columns for pathway analysis
        required_columns = ["sample", "pathname", "ko"]
        if not all(col in merged_df.columns for col in required_columns):
            missing_cols = [
                col for col in required_columns if col not in merged_df.columns
            ]
            raise ValueError(f"Missing required columns: {missing_cols}")

        if merged_df.empty:
            raise ValueError("Input DataFrame is empty")

        try:
            self.logger.info("Counting unique KOs per pathway and per sample...")
            pathway_count = (
                merged_df.groupby(["sample", "pathname"])["ko"]
                .nunique()
                .reset_index(name="unique_ko_count")
            )

            self.logger.info(
                f"Pathway analysis completed. "
                f"Processed {len(pathway_count)} sample-pathway combinations"
            )
            self.logger.debug(f"Pathway counts summary:\n{pathway_count.head()}")

            return pathway_count

        except Exception as e:
            self.logger.error(f"Error during pathway analysis: {e}")
            raise RuntimeError("Error processing KO counts per pathway") from e

    def analyze_ko_per_sample_for_pathway(
        self, merged_df: pd.DataFrame, selected_pathway: str
    ) -> pd.DataFrame:
        """
        Count unique KOs for a specific pathway across all samples.

        This method filters the merged DataFrame for a specific pathway and counts
        unique KO identifiers per sample, useful for comparing pathway presence
        across different samples.

        Parameters
        ----------
        merged_df : pd.DataFrame
            DataFrame contendo dados da fusão com KEGG, com colunas
            'sample', 'pathname' e 'ko'.
        selected_pathway : str
            Identificador da via metabólica selecionada para a filtragem.

        Returns
        -------
        pd.DataFrame
            DataFrame with columns ['sample', 'unique_ko_count'] for the selected
            pathway, sorted in descending order by KO count.

        Raises
        ------
        TypeError
            If input is not a pandas DataFrame.
        ValueError
            If DataFrame is empty, missing required columns, or selected pathway
            is not found.

        Examples
        --------
        >>> analyzer = GenePathwayAnalyzer()
        >>> df = pd.DataFrame({
        ...     'sample': ['Sample1', 'Sample1', 'Sample2'],
        ...     'pathname': ['Pathway1', 'Pathway1', 'Pathway1'],
        ...     'ko': ['K00001', 'K00002', 'K00001']
        ... })
        >>> result = analyzer.analyze_ko_per_sample_for_pathway(df, 'Pathway1')
        """
        self.logger.info(f"Starting KO counts analysis for pathway: {selected_pathway}")

        # Validate required columns for pathway-specific analysis
        required_columns = ["sample", "pathname", "ko"]
        if not all(col in merged_df.columns for col in required_columns):
            missing_cols = [
                col for col in required_columns if col not in merged_df.columns
            ]
            raise ValueError(f"Missing required columns: {missing_cols}")

        if merged_df.empty:
            raise ValueError("Input DataFrame is empty")

        # Check if selected pathway exists
        if selected_pathway not in merged_df["pathname"].unique():
            available_pathways = merged_df["pathname"].unique()
            self.logger.warning(f"Pathway '{selected_pathway}' not found in DataFrame")
            raise ValueError(
                f"Pathway '{selected_pathway}' not found. "
                f"Available pathways: {list(available_pathways)}"
            )

        try:
            self.logger.info(f"Filtering data for pathway: {selected_pathway}")
            filtered_df = merged_df[merged_df["pathname"] == selected_pathway]

            self.logger.info("Counting unique KOs per sample for selected pathway...")
            sample_count = (
                filtered_df.groupby("sample")["ko"]
                .nunique()
                .reset_index(name="unique_ko_count")
            )

            # Sort by KO count in descending order
            result = sample_count.sort_values("unique_ko_count", ascending=False)

            self.logger.info(
                f"Pathway-specific analysis completed. "
                f"Processed {len(result)} samples for pathway '{selected_pathway}'"
            )
            self.logger.debug(f"Sample counts for pathway:\n{result.head()}")

            return result

        except Exception as e:
            self.logger.error(f"Error during pathway-specific analysis: {e}")
            raise RuntimeError(
                f"Error processing KO counts per sample for pathway "
                f"'{selected_pathway}'"
            ) from e
