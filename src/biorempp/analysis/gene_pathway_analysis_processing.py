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
        automatically detects data source (BioRemPP vs KEGG) and executes
        appropriate analyses with proper file naming.

        Parameters
        ----------
        data : pd.DataFrame
            Post-merge DataFrame from pipeline containing required columns
            for analysis.
        **kwargs
            Additional parameters:
            - data_source (str): Override automatic detection with 'biorempp'
              or 'kegg'

        Returns
        -------
        pd.DataFrame
            Comprehensive analysis results with KO counts per sample.
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
        3. Most abundant pathway analysis (logged, if pathways)

        Data source is automatically detected by column presence:
        - BioRemPP data: has 'sample', 'ko' columns
        - KEGG data: has 'sample', 'ko', 'pathname' columns
        """
        self.logger.info("Starting comprehensive gene pathway analysis processing")

        # Validate basic requirements for all analyses
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame")

        if data.empty:
            raise ValueError("DataFrame cannot be empty")

        # Detect data source automatically or use provided override
        data_source = kwargs.get("data_source")
        if data_source is None:
            if "pathname" in data.columns:
                data_source = "kegg"
            else:
                data_source = "biorempp"

        self.logger.info(f"Processing {data_source} data")

        # Analysis 1: KO counts per sample (primary analysis)
        try:
            ko_per_sample = self.analyze_ko_counts_per_sample(
                data, data_source=data_source
            )
            self.logger.info(
                f"Analysis 1 completed: KO counts per sample "
                f"({len(ko_per_sample)} samples) for {data_source} data"
            )
        except Exception as e:
            self.logger.error(f"KO counts per sample analysis failed: {e}")
            raise

        # Analysis 2: KO counts per pathway per sample (KEGG data only)
        try:
            if data_source == "kegg" and "pathname" in data.columns:
                ko_per_pathway = self.analyze_ko_per_pathway_per_sample(data)
                self.logger.info(
                    f"Analysis 2 completed: KO counts per pathway per sample "
                    f"({len(ko_per_pathway)} pathway-sample combinations)"
                )

                # Save pathway analysis to separate output directory
                from biorempp.utils.io_utils import save_dataframe_output

                pathway_output_path = save_dataframe_output(
                    ko_per_pathway,
                    output_dir="outputs/gene_pathways_analysis",
                    filename="ko_per_pathway_per_sample.txt",
                    sep=";",
                )
                self.logger.info(f"Pathway analysis saved to: {pathway_output_path}")

                # Analysis 3: Find most abundant pathway
                if len(ko_per_pathway) > 0:
                    most_abundant_idx = ko_per_pathway["unique_ko_count"].idxmax()
                    most_abundant_pathway = ko_per_pathway.loc[most_abundant_idx]
                    self.logger.info(
                        f"Most abundant pathway: "
                        f"{most_abundant_pathway['pathname']} "
                        f"(Sample: {most_abundant_pathway['sample']}, "
                        f"KO count: {most_abundant_pathway['unique_ko_count']})"
                    )
            else:
                self.logger.info(
                    f"Analysis 2 skipped: pathway analysis not applicable "
                    f"for {data_source} data"
                )

        except Exception as e:
            self.logger.warning(f"Pathway analysis failed (non-critical): {e}")

        self.logger.info(
            f"Comprehensive gene pathway analysis processing completed "
            f"for {data_source} data"
        )

        # Return primary analysis result (KO counts per sample)
        return ko_per_sample

    def analyze_ko_counts_per_sample(
        self, merged_df: pd.DataFrame, data_source: str = "biorempp"
    ) -> pd.DataFrame:
        """
        Analyze KO counts per sample from post-merge BioRemPP or KEGG data.

        This function processes the merged DataFrame from BioRemPP pipeline
        to count unique KO (KEGG Orthology) identifiers per sample, providing
        insights into the functional diversity of each sample. Results are
        automatically saved with appropriate suffixes based on data source.

        Parameters
        ----------
        merged_df : pd.DataFrame
            Post-merge DataFrame from BioRemPP pipeline containing at least
            'sample' and 'ko' columns.
        data_source : str, optional
            Source of the data for naming output files. Can be 'biorempp'
            or 'kegg' (default: 'biorempp').

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
        valid_sources = ["biorempp", "kegg"]
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
        self, merged_df: pd.DataFrame, selected_pathway: str = None
    ) -> pd.DataFrame:
        """
        Count unique KOs for pathways across all samples.

        This method analyzes KO counts per sample for either a specific pathway
        (if selected_pathway is provided) or for all pathways (if selected_pathway
        is None). When analyzing all pathways, results are saved to a single file
        for comprehensive pathway comparison.

        Parameters
        ----------
        merged_df : pd.DataFrame
            DataFrame contendo dados da fusão com KEGG, com colunas
            'sample', 'pathname' e 'ko'.
        selected_pathway : str, optional
            Identificador da via metabólica específica para filtragem.
            Se None (padrão), analisa todas as vias disponíveis.

        Returns
        -------
        pd.DataFrame
            DataFrame with columns ['sample', 'pathname', 'unique_ko_count']
            containing KO counts per sample for all pathways, or columns
            ['sample', 'unique_ko_count'] for a specific pathway.
            Results are sorted by pathway and then by KO count (descending).

        Raises
        ------
        TypeError
            If input is not a pandas DataFrame.
        ValueError
            If DataFrame is empty, missing required columns, or selected pathway
            is not found (when specified).

        Examples
        --------
        >>> analyzer = GenePathwayAnalyzer()
        >>> df = pd.DataFrame({
        ...     'sample': ['Sample1', 'Sample1', 'Sample2'],
        ...     'pathname': ['Pathway1', 'Pathway2', 'Pathway1'],
        ...     'ko': ['K00001', 'K00002', 'K00001']
        ... })
        >>> # Análise de todas as vias
        >>> result = analyzer.analyze_ko_per_sample_for_pathway(df)
        >>> # Análise de via específica
        >>> result = analyzer.analyze_ko_per_sample_for_pathway(df, 'Pathway1')
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
                # Analisar todas as vias disponíveis
                self.logger.info(
                    "Starting comprehensive KO counts analysis for all pathways"
                )

                available_pathways = merged_df["pathname"].unique()
                self.logger.info(
                    f"Found {len(available_pathways)} unique pathways to analyze"
                )

                # Contar KOs únicos por amostra por via
                all_pathways_result = (
                    merged_df.groupby(["pathname", "sample"])["ko"]
                    .nunique()
                    .reset_index(name="unique_ko_count")
                )

                # Reorganizar colunas e ordenar
                all_pathways_result = all_pathways_result[
                    ["sample", "pathname", "unique_ko_count"]
                ]
                result = all_pathways_result.sort_values(
                    ["pathname", "unique_ko_count"], ascending=[True, False]
                )

                self.logger.info(
                    f"All pathways analysis completed. "
                    f"Processed {len(result)} sample-pathway combinations"
                )

                # Salvar resultados em arquivo específico
                from biorempp.utils.io_utils import save_dataframe_output

                output_path = save_dataframe_output(
                    result,
                    output_dir="outputs/gene_pathways_analysis",
                    filename="ko_per_sample_all_pathways.txt",
                    sep=";",
                )
                self.logger.info(f"All pathways analysis saved to: {output_path}")

                # Log estatísticas resumidas
                pathway_stats = (
                    result.groupby("pathname")["unique_ko_count"]
                    .agg(["count", "mean", "max", "min"])
                    .round(2)
                )
                self.logger.info(f"Pathway statistics:\n{pathway_stats}")

                return result

            else:
                # Analisar via específica (comportamento original)
                self.logger.info(
                    f"Starting KO counts analysis for specific pathway: "
                    f"{selected_pathway}"
                )

                # Check if selected pathway exists
                if selected_pathway not in merged_df["pathname"].unique():
                    available_pathways = merged_df["pathname"].unique()
                    self.logger.warning(
                        f"Pathway '{selected_pathway}' not found in DataFrame"
                    )
                    raise ValueError(
                        f"Pathway '{selected_pathway}' not found. "
                        f"Available pathways: {list(available_pathways)}"
                    )

                self.logger.info(f"Filtering data for pathway: {selected_pathway}")
                filtered_df = merged_df[merged_df["pathname"] == selected_pathway]

                self.logger.info(
                    "Counting unique KOs per sample for selected pathway..."
                )
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
            pathway_info = (
                f"pathway '{selected_pathway}'" if selected_pathway else "all pathways"
            )
            self.logger.error(f"Error during pathway analysis for {pathway_info}: {e}")
            raise RuntimeError(
                f"Error processing KO counts per sample for {pathway_info}"
            ) from e
