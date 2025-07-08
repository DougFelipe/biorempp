"""
Post-merge processing pipeline for BioRemPP.

This module provides pipeline functionality for processing post-merge
data from BioRemPP, focusing on KO counting analysis.
"""

import os

from biorempp.analysis.gene_pathway_analysis import GenePathwayAnalyzer
from biorempp.utils.io_utils import save_dataframe_output
from biorempp.utils.logging_config import get_logger
from biorempp.utils.post_merge_reader import PostMergeDataReader

logger = get_logger("pipelines.processing_post_merge")


def run_post_merge_processing_pipeline(
    data_type: str = "biorempp",
    output_dir: str = "outputs/analysis_results",
    output_filename: str = None,
    results_dir: str = None,
) -> str:
    """
    Run the post-merge processing pipeline for KO analysis.

    This function loads post-merge data using PostMergeDataReader,
    performs KO counting analysis using GenePathwayAnalyzer, and saves
    the results to the specified location.

    Parameters
    ----------
    data_type : str, optional
        Type of post-merge data to process ('biorempp', 'hadeg', 'kegg', 'toxcsm').
        Default: 'biorempp'.
    output_dir : str, optional
        Directory to save analysis results. Default: 'outputs/analysis_results'.
    output_filename : str, optional
        Name of output file. If None, uses 'ko_counts.txt'.
    results_dir : str, optional
        Directory containing post-merge result files.
        If None, uses default from PostMergeDataReader.

    Returns
    -------
    str
        Path to the saved analysis file.

    Raises
    ------
    FileNotFoundError
        If no post-merge files found for the specified data type.
    ValueError
        If data_type is not supported.

    Examples
    --------
    >>> # Process BioRemPP data
    >>> output_path = run_post_merge_processing_pipeline('biorempp')
    >>> print(f"Results saved to: {output_path}")
    """
    logger.info(f"Starting post-merge processing pipeline for {data_type}")

    # Initialize components
    data_reader = PostMergeDataReader(results_dir=results_dir)
    analyzer = GenePathwayAnalyzer()

    # Load post-merge data
    logger.info(f"Loading latest {data_type} data...")
    merged_df = data_reader.load_latest(data_type)
    logger.info(f"Loaded {data_type} data: shape={merged_df.shape}")

    # Perform KO analysis
    logger.info("Performing KO counts analysis...")
    ko_results = analyzer.analyze_ko_counts_per_sample(merged_df)

    # Prepare output
    if output_filename is None:
        output_filename = "ko_counts.txt"

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save results
    output_path = save_dataframe_output(
        df=ko_results,
        output_dir=output_dir,
        filename=output_filename,
        add_timestamp=True,
    )

    logger.info(
        f"Post-merge processing pipeline completed for {data_type}. "
        f"Results saved to: {output_path}"
    )

    return output_path
