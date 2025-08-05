"""
Gene pathway analysis module for BioRemPP.

This module provides functionality for analyzing gene and pathway data
from post-merge BioRemPP results, including KO coun    def analyze_ko_counts_per_sample(
        self,
        merged_df: pd.DataFrame,
        data_source: str = "biorempp"
    ) -> pd.DataFrame:analysis.
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
        Comprehensive gene pathway analysis processing method.

        This method runs all available analysis methods on the input data,
        providing a complete analysis suite for gene pathway data. It
        automatically detects data source and orchestrates the execution
        of all analyses.

        Parameters
        ----------
        data : pd.DataFrame
            Post-merge DataFrame from pipeline containing required columns
            for analysis.
        **kwargs
            Additional parameters:
            - data_source (str): Override automatic detection with 'biorempp',
              'kegg', or 'hadeg'

        Returns
        -------
        pd.DataFrame
            Primary analysis results with KO counts per sample.
            Additional analysis results are logged and saved to files.

        Raises
        ------
        TypeError
            If input is not a pandas DataFrame.
        ValueError
            If DataFrame is empty or missing required columns.

        Notes
        -----
        This method performs the following analyses:
        1. KO counts per sample analysis (returned as primary result)
        2. KO counts per pathway per sample (logged and saved, if pathways)
        3. KO pathway statistics (with most abundant pathway identification,
           logged and saved, if pathways)

        Data source is automatically detected by column presence:
        - BioRemPP data: has 'sample', 'ko' columns
        - KEGG data: has 'sample', 'ko', 'pathname' columns
        - HADEG data: has 'sample', 'ko', 'Pathway', 'compound_pathway' columns
        """
        self.logger.info("Starting comprehensive gene pathway analysis processing")

        # Validate basic requirements
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame")

        if data.empty:
            raise ValueError("DataFrame cannot be empty")

        # Detect data source automatically or use provided override
        data_source = kwargs.get("data_source")
        if data_source is None:
            data_source = self._detect_data_source(data)

        self.logger.info(f"Processing {data_source} data")

        # Analysis 1: KO counts per sample (primary analysis)
        ko_per_sample = self.analyze_ko_counts_per_sample(data, data_source=data_source)
        self.logger.info(
            f"Analysis 1 completed: KO counts per sample "
            f"({len(ko_per_sample)} samples) for {data_source} data"
        )

        # Analysis 2 & 3: Pathway analyses (if applicable)
        if data_source in ["kegg", "hadeg"]:
            try:
                self._execute_pathway_analyses(data, data_source)
            except Exception as e:
                self.logger.warning(f"Pathway analysis failed (non-critical): {e}")
        else:
            self.logger.info(
                f"Pathway analysis skipped: not applicable for {data_source} data"
            )

        self.logger.info(
            f"Comprehensive gene pathway analysis processing completed "
            f"for {data_source} data"
        )

        return ko_per_sample

    def _detect_data_source(self, data: pd.DataFrame) -> str:
        """
        Automatically detect data source based on column presence.

        Parameters
        ----------
        data : pd.DataFrame
            Input DataFrame to analyze.

        Returns
        -------
        str
            Detected data source: 'kegg', 'hadeg', or 'biorempp'.
        """
        if "pathname" in data.columns:
            return "kegg"
        elif "Pathway" in data.columns and "compound_pathway" in data.columns:
            return "hadeg"
        else:
            return "biorempp"

    def _execute_pathway_analyses(self, data: pd.DataFrame, data_source: str) -> None:
        """
        Execute pathway analyses for KEGG or HADEG data sources.

        Parameters
        ----------
        data : pd.DataFrame
            Input data with pathway information.
        data_source : str
            Data source type ('kegg' or 'hadeg').
        """
        if data_source == "kegg":
            self._execute_kegg_pathway_analyses(data)
        elif data_source == "hadeg":
            self._execute_hadeg_pathway_analyses(data)

    def _execute_kegg_pathway_analyses(self, data: pd.DataFrame) -> None:
        """Execute KEGG-specific pathway analyses."""
        # Analysis 2: KO per pathway per sample
        ko_per_pathway = self.analyze_ko_per_pathway_per_sample(
            data, save_file=True, suffix="kegg"
        )
        self.logger.info(
            f"Analysis 2 completed: KO counts per KEGG pathway per sample "
            f"({len(ko_per_pathway)} pathway-sample combinations)"
        )

        # Analysis 3: Pathway statistics
        self.analyze_ko_per_sample_for_pathway(data, save_file=True, suffix="kegg")
        self.logger.info("Analysis 3 completed: KEGG pathway statistics analysis")

    def _execute_hadeg_pathway_analyses(self, data: pd.DataFrame) -> None:
        """Execute HADEG-specific pathway analyses."""
        # Prepare HADEG data (rename columns for compatibility)
        data_hadeg = data.copy()
        data_hadeg = data_hadeg.rename(columns={"Pathway": "pathname"})

        # Analysis 2: KO per pathway per sample
        self.analyze_ko_per_pathway_per_sample(
            data_hadeg, save_file=True, suffix="hadeg"
        )
        self.logger.info("Analysis 2 completed: KO counts per HADEG pathway per sample")

        # Analysis 3: Pathway statistics
        self.analyze_ko_per_sample_for_pathway(
            data_hadeg, save_file=True, suffix="hadeg"
        )
        self.logger.info("Analysis 3 completed: HADEG pathway statistics analysis")

    def analyze_ko_counts_per_sample(
        self, merged_df: pd.DataFrame, data_source: str = "biorempp"
    ) -> pd.DataFrame:
        """
        Analyze KO counts per sample from post-merge BioRemPP, KEGG, or HADEG data.

        This function processes the merged DataFrame from BioRemPP pipeline
        to count unique KO (KEGG Orthology) identifiers per sample, providing
        insights into the functional diversity of each sample. Results are
        automatically saved with appropriate suffixes based on data source.

        Parameters
        ----------
        merged_df : pd.DataFrame
            Post-merge DataFrame from BioRemPP pipeline containing at least
            'sample' and 'ko' columns. Additional columns depend on data source:
            - BioRemPP: basic columns
            - KEGG: includes 'pathname' column
            - HADEG: includes 'Pathway' and 'compound_pathway' columns
        data_source : str, optional
            Source of the data for naming output files. Can be 'biorempp',
            'kegg', or 'hadeg' (default: 'biorempp').

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
            If DataFrame is empty or missing required columns, or if
            data_source is invalid.

        Examples
        --------
        >>> analyzer = GenePathwayAnalyzer()
        >>> df = pd.DataFrame({
        ...     'sample': ['Sample1', 'Sample1', 'Sample2'],
        ...     'ko': ['K00001', 'K00002', 'K00001']
        ... })
        >>> result = analyzer.analyze_ko_counts_per_sample(df, 'biorempp')
        >>> print(result)
           sample  ko_count
        0  Sample1         2
        1  Sample2         1
        """
        # Validate data_source parameter
        valid_sources = ["biorempp", "kegg", "hadeg"]
        if data_source not in valid_sources:
            raise ValueError(
                f"Invalid data_source '{data_source}'. "
                f"Must be one of {valid_sources}"
            )

        self.logger.info(
            f"Starting KO counts analysis per sample for {data_source} data"
        )

        # Validate input DataFrame
        self.validate_input(merged_df)

        # Count unique KOs per sample
        self.logger.info("Counting unique KOs per sample...")
        ko_counts = (
            merged_df.groupby("sample")["ko"].nunique().reset_index(name="ko_count")
        )

        # Sort by KO count in descending order
        ko_counts_sorted = ko_counts.sort_values("ko_count", ascending=False)

        # Save results with appropriate suffix
        try:
            from biorempp.utils.io_utils import save_dataframe_output

            filename = f"ko_counts_per_sample_{data_source}.txt"
            output_path = save_dataframe_output(
                ko_counts_sorted,
                output_dir="outputs/gene_pathways_analysis",
                filename=filename,
                sep=";",
            )
            self.logger.info(f"KO counts analysis saved to: {output_path}")

        except Exception as e:
            self.logger.warning(
                f"Failed to save KO counts analysis: {e}. " "Continuing with analysis."
            )

        self.logger.info(
            f"KO analysis completed. Processed {len(ko_counts_sorted)} samples "
            f"from {data_source} data"
        )
        self.logger.debug(f"KO counts summary:\n{ko_counts_sorted.head()}")

        return ko_counts_sorted

    def analyze_ko_per_pathway_per_sample(
        self, merged_df: pd.DataFrame, save_file: bool = False, suffix: str = ""
    ) -> pd.DataFrame:
        """
        Count unique KOs for each pathway in each sample.

        This method processes the merged DataFrame from BioRemPP pipeline
        to count unique KO (KEGG Orthology) identifiers per pathway in each
        sample, providing insights into pathway diversity across samples.

        Parameters
        ----------
        merged_df : pd.DataFrame
            DataFrame with columns 'sample', 'pathname' and 'ko'.
        save_file : bool, optional
            Whether to save results to file (default: False).
        suffix : str, optional
            Suffix for output filename when saving (default: "").

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

            # Save to file if requested
            if save_file and suffix:
                self._save_pathway_per_sample_results(pathway_count, suffix)

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
        self,
        merged_df: pd.DataFrame,
        selected_pathway: str = None,
        save_file: bool = False,
        suffix: str = "",
    ) -> pd.DataFrame:
        """
        Analyze KO counts for pathways across samples.

        This method analyzes KO counts per sample for either a specific pathway
        (if selected_pathway is provided) or generates pathway statistics for
        all pathways (if selected_pathway is None).

        Parameters
        ----------
        merged_df : pd.DataFrame
            DataFrame with columns 'sample', 'pathname' and 'ko'.
        selected_pathway : str, optional
            Specific pathway identifier for filtering. If None (default),
            generates statistics for all pathways.
        save_file : bool, optional
            Whether to save results to file (default: False).
        suffix : str, optional
            Suffix for output filename when saving (default: "").

        Returns
        -------
        pd.DataFrame
            For all pathways: DataFrame with pathway statistics (count, mean, max, min).
            For specific pathway: DataFrame with sample-specific results.

        Raises
        ------
        TypeError
            If input is not a pandas DataFrame.
        ValueError
            If DataFrame is empty, missing required columns, or selected pathway
            is not found (when specified).
        """
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
            if selected_pathway is None:
                return self._analyze_all_pathways_statistics(
                    merged_df, save_file, suffix
                )
            else:
                return self._analyze_specific_pathway(merged_df, selected_pathway)

        except Exception as e:
            pathway_info = (
                f"pathway '{selected_pathway}'" if selected_pathway else "all pathways"
            )
            self.logger.error(f"Error during pathway analysis for {pathway_info}: {e}")
            raise RuntimeError(
                f"Error processing KO counts per sample for {pathway_info}"
            ) from e

    def _analyze_all_pathways_statistics(
        self, merged_df: pd.DataFrame, save_file: bool, suffix: str
    ) -> pd.DataFrame:
        """
        Generate statistics for all pathways.

        Parameters
        ----------
        merged_df : pd.DataFrame
            Input DataFrame with pathway data.
        save_file : bool
            Whether to save results to file.
        suffix : str
            Suffix for output filename.

        Returns
        -------
        pd.DataFrame
            DataFrame with pathway statistics.
        """
        self.logger.info("Starting comprehensive KO counts analysis for all pathways")

        available_pathways = merged_df["pathname"].unique()
        self.logger.info(f"Found {len(available_pathways)} unique pathways to analyze")

        # Count unique KOs per sample per pathway
        all_pathways_result = (
            merged_df.groupby(["pathname", "sample"])["ko"]
            .nunique()
            .reset_index(name="unique_ko_count")
        )

        # Generate pathway statistics (count, mean, max, min)
        pathway_stats = (
            all_pathways_result.groupby("pathname")["unique_ko_count"]
            .agg(["count", "mean", "max", "min"])
            .round(2)
            .reset_index()
        )

        # Find and log most abundant pathway
        self._log_most_abundant_pathway(all_pathways_result, suffix)

        # Save to file if requested
        if save_file and suffix:
            self._save_pathway_statistics_results(pathway_stats, suffix)

        self.logger.info(f"Pathway statistics:\n{pathway_stats}")
        self.logger.info(
            f"All pathways analysis completed. "
            f"Processed {len(pathway_stats)} unique pathways"
        )

        return pathway_stats

    def _analyze_specific_pathway(
        self, merged_df: pd.DataFrame, selected_pathway: str
    ) -> pd.DataFrame:
        """
        Analyze a specific pathway.

        Parameters
        ----------
        merged_df : pd.DataFrame
            Input DataFrame with pathway data.
        selected_pathway : str
            Specific pathway to analyze.

        Returns
        -------
        pd.DataFrame
            DataFrame with sample-specific results for the pathway.
        """
        self.logger.info(
            f"Starting KO counts analysis for specific pathway: " f"{selected_pathway}"
        )

        # Check if selected pathway exists
        if selected_pathway not in merged_df["pathname"].unique():
            available_pathways = merged_df["pathname"].unique()
            self.logger.warning(f"Pathway '{selected_pathway}' not found in DataFrame")
            raise ValueError(
                f"Pathway '{selected_pathway}' not found. "
                f"Available pathways: {list(available_pathways)}"
            )

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

    def _save_pathway_per_sample_results(
        self, results: pd.DataFrame, suffix: str
    ) -> None:
        """Save pathway per sample results to file."""
        try:
            from biorempp.utils.io_utils import save_dataframe_output

            # Handle HADEG column naming
            if suffix == "hadeg" and "pathname" in results.columns:
                results = results.rename(columns={"pathname": "Pathway"})

            filename = f"ko_per_pathway_per_sample_{suffix}.txt"
            output_path = save_dataframe_output(
                results,
                output_dir="outputs/gene_pathways_analysis",
                filename=filename,
                sep=";",
            )
            self.logger.info(f"Pathway analysis saved to: {output_path}")

        except Exception as e:
            self.logger.warning(f"Failed to save pathway analysis: {e}")

    def _save_pathway_statistics_results(
        self, results: pd.DataFrame, suffix: str
    ) -> None:
        """Save pathway statistics results to file."""
        try:
            from biorempp.utils.io_utils import save_dataframe_output

            # Handle HADEG column naming
            if suffix == "hadeg" and "pathname" in results.columns:
                results = results.rename(columns={"pathname": "Pathway"})

            filename = f"ko_per_sample_all_pathways_{suffix}.txt"
            output_path = save_dataframe_output(
                results,
                output_dir="outputs/gene_pathways_analysis",
                filename=filename,
                sep=";",
            )
            self.logger.info(
                f"All {suffix.upper()} pathways statistics saved to: {output_path}"
            )

        except Exception as e:
            self.logger.warning(f"Failed to save pathway statistics: {e}")

    def _log_most_abundant_pathway(
        self, all_pathways_result: pd.DataFrame, suffix: str
    ) -> None:
        """Log information about the most abundant pathway."""
        if len(all_pathways_result) > 0:
            most_abundant_idx = all_pathways_result["unique_ko_count"].idxmax()
            most_abundant_pathway = all_pathways_result.loc[most_abundant_idx]

            pathway_name = most_abundant_pathway["pathname"]

            self.logger.info(
                f"Most abundant {suffix.upper()} pathway: {pathway_name} "
                f"(Sample: {most_abundant_pathway['sample']}, "
                f"KO count: {most_abundant_pathway['unique_ko_count']})"
            )
