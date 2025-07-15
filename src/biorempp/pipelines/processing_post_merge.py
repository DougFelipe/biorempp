"""
Post-merge processing pipeline for BioRemPP.

This module provides pipeline functionality for processing post-merge
data from BioRemPP, focusing on KO counting analysis.
"""

import os
from typing import Union

from biorempp.analysis.gene_pathway_analysis_processing import GenePathwayAnalyzer
from biorempp.utils.io_utils import save_dataframe_output
from biorempp.utils.logging_config import get_logger
from biorempp.utils.post_merge_reader import PostMergeDataReader

logger = get_logger("pipelines.processing_post_merge")


def run_post_merge_processing_pipeline(
    data_type: str = "biorempp",
    output_dir: str = "outputs/analysis_results",
    output_filename: str = None,
    results_dir: str = None,
    return_dataframes: bool = False,
) -> Union[str, tuple]:
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
    return_dataframes : bool, optional
        If True, returns (output_path, merged_df, ko_results).
        If False, returns only output_path. Default: False.

    Returns
    -------
    str or tuple
        If return_dataframes=False: Path to the saved analysis file.
        If return_dataframes=True: (output_path, merged_df, ko_results).

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
    >>>
    >>> # Get DataFrames for further processing
    >>> output_path, merged_df, ko_results = run_post_merge_processing_pipeline(
    ...     'biorempp', return_dataframes=True
    ... )
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

    # Prepare output for basic KO analysis
    if output_filename is None:
        output_filename = "ko_counts.txt"

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save basic KO counts results
    output_path = save_dataframe_output(
        df=ko_results,
        output_dir=output_dir,
        filename=output_filename,
        add_timestamp=True,
    )

    # Additional analyses for KEGG data
    additional_outputs = []
    if data_type.lower() == "kegg":
        logger.info("Performing additional KEGG-specific analyses...")

        # Check if required columns for KEGG analysis are present
        required_kegg_columns = ["sample", "pathname", "ko"]
        if all(col in merged_df.columns for col in required_kegg_columns):

            # Analysis 1: KO per pathway per sample
            logger.info("Performing KO per pathway per sample analysis...")
            try:
                pathway_results = analyzer.analyze_ko_per_pathway_per_sample(merged_df)
                pathway_output_path = save_dataframe_output(
                    df=pathway_results,
                    output_dir=output_dir,
                    filename="ko_per_pathway_per_sample.txt",
                    add_timestamp=True,
                )
                additional_outputs.append(pathway_output_path)
                logger.info(f"Pathway analysis saved to: {pathway_output_path}")
            except Exception as e:
                logger.error(f"Error in pathway analysis: {e}")

            # Additional pathway-specific analyses for representative pathways
            if "pathname" in merged_df.columns:
                try:
                    # Get top 3 most frequent pathways for detailed analysis
                    top_pathways = (
                        merged_df["pathname"].value_counts().head(3).index.tolist()
                    )

                    for pathway in top_pathways:
                        logger.info(f"Performing analysis for pathway: {pathway}")
                        pathway_specific_results = (
                            analyzer.analyze_ko_per_sample_for_pathway(
                                merged_df, pathway
                            )
                        )
                        # Clean pathway name for filename
                        clean_pathway = (
                            pathway.replace(" ", "_")
                            .replace("/", "_")
                            .replace("\\", "_")
                        )
                        pathway_specific_filename = (
                            f"ko_per_sample_for_{clean_pathway}.txt"
                        )
                        pathway_specific_output_path = save_dataframe_output(
                            df=pathway_specific_results,
                            output_dir=output_dir,
                            filename=pathway_specific_filename,
                            add_timestamp=True,
                        )
                        additional_outputs.append(pathway_specific_output_path)
                        logger.info(
                            f"Pathway-specific analysis saved to: "
                            f"{pathway_specific_output_path}"
                        )
                except Exception as e:
                    logger.error(f"Error in pathway-specific analyses: {e}")
            else:
                logger.info(
                    "No specific pathway provided. "
                    "Skipping pathway-specific analysis."
                )

        else:
            missing_cols = [
                col for col in required_kegg_columns if col not in merged_df.columns
            ]
            logger.warning(f"KEGG analysis skipped. Missing columns: {missing_cols}")

    logger.info(
        f"Post-merge processing pipeline completed for {data_type}. "
        f"Results saved to: {output_path}"
    )
    if additional_outputs:
        logger.info(f"Additional outputs: {additional_outputs}")

    if return_dataframes:
        return output_path, merged_df, ko_results
    else:
        return output_path
