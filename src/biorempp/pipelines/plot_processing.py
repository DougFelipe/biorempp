"""
Plot processing pipeline for BioRemPP.

This module provides functionality for generating and saving plots from
post-merge analysis results, specifically for gene pathway analysis.
"""

from datetime import datetime
from pathlib import Path
from typing import Optional

from biorempp.analysis.gene_pathway_analysis_plotter import GenePathwayPlotter
from biorempp.analysis.gene_pathway_analysis_processing import GenePathwayAnalyzer
from biorempp.utils.logging_config import get_logger
from biorempp.utils.post_merge_reader import PostMergeDataReader

logger = get_logger("pipelines.plot_processing")


def run_gene_pathway_plotting_pipeline(
    data_type: str = "biorempp",
    output_dir: Optional[str] = None,
    plot_format: str = "png",
    use_plotly: bool = True,
) -> str:
    """
    Run the gene pathway plotting pipeline.

    This pipeline loads the latest post-merge data, performs KO analysis,
    and generates plots saving them to the outputs/plots directory.

    Parameters
    ----------
    data_type : str, optional
        Type of data to load ('biorempp', 'hadeg', 'kegg', 'toxcsm').
        Default is 'biorempp'.
    output_dir : str, optional
        Output directory for plots. If None, uses 'outputs/plots/'.
    plot_format : str, optional
        Format for saving plots ('png', 'pdf', 'svg', 'html').
        Default is 'png'.
    use_plotly : bool, optional
        Whether to use Plotly (True) or matplotlib (False) for plotting.
        Default is True.

    Returns
    -------
    str
        Path to the saved plot file.

    Raises
    ------
    FileNotFoundError
        If no data files are found for the specified data type.
    ValueError
        If the data is invalid or plotting fails.

    Examples
    --------
    >>> plot_path = run_gene_pathway_plotting_pipeline()
    >>> print(f"Plot saved to: {plot_path}")
    """
    logger.info(f"Starting gene pathway plotting pipeline for {data_type}")

    try:
        # Initialize components
        data_reader = PostMergeDataReader()
        analyzer = GenePathwayAnalyzer()
        plotter = GenePathwayPlotter()

        logger.info("Loading latest post-merge data...")
        # Load the latest data
        merged_df = data_reader.load_latest(data_type)
        logger.info(f"Loaded data with shape: {merged_df.shape}")

        # Perform KO analysis
        logger.info("Performing KO counts analysis...")
        ko_counts_df = analyzer.analyze_ko_counts_per_sample(merged_df)
        logger.info(f"KO analysis completed. Found {len(ko_counts_df)} samples")

        # Generate timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Set output directory
        if output_dir is None:
            # Navigate from this file to project root:
            # src/biorempp/pipelines/plot_processing.py -> ../../../../
            current_file = Path(__file__).resolve()
            project_root = current_file.parent.parent.parent.parent
            output_dir = project_root / "outputs" / "plots"
        else:
            # If custom output_dir provided, ensure it's absolute or relative
            # to project root
            if not Path(output_dir).is_absolute():
                current_file = Path(__file__).resolve()
                project_root = current_file.parent.parent.parent.parent
                output_dir = project_root / output_dir
            else:
                output_dir = Path(output_dir)

        # Ensure output directory exists
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename
        filename = f"ko_counts_per_sample_{data_type}_{timestamp}"
        filepath = output_dir / filename

        plot_type = "Plotly" if use_plotly else "matplotlib"
        logger.info(f"Generating plot using {plot_type}...")

        # Generate plot
        if use_plotly:
            fig = plotter.plot_ko_counts_per_sample_plotly(ko_counts_df)
        else:
            fig = plotter.plot_ko_counts_per_sample_matplotlib(ko_counts_df)

        # Save plot
        logger.info(f"Saving plot to: {filepath}")
        saved_path = plotter.save_plot(fig, filepath, format=plot_format)

        logger.info("Gene pathway plotting pipeline completed successfully")
        logger.info(f"Plot saved to: {saved_path}")

        return saved_path

    except Exception as e:
        logger.error(f"Error in gene pathway plotting pipeline: {str(e)}")
        raise


def run_multiple_plots_pipeline(
    data_types: list = None,
    output_dir: Optional[str] = None,
    plot_formats: list = None,
    use_plotly: bool = True,
) -> dict:
    """
    Run plotting pipeline for multiple data types and formats.

    Parameters
    ----------
    data_types : list, optional
        List of data types to process. If None, uses ['biorempp'].
    output_dir : str, optional
        Output directory for plots. If None, uses 'outputs/plots/'.
    plot_formats : list, optional
        List of formats for saving plots. If None, uses ['png'].
    use_plotly : bool, optional
        Whether to use Plotly (True) or matplotlib (False) for plotting.

    Returns
    -------
    dict
        Dictionary with data_type as keys and saved plot paths as values.

    Examples
    --------
    >>> results = run_multiple_plots_pipeline(
    ...     data_types=['biorempp', 'kegg'],
    ...     plot_formats=['png', 'html']
    ... )
    """
    if data_types is None:
        data_types = ["biorempp"]
    if plot_formats is None:
        plot_formats = ["png"]

    logger.info(f"Starting multiple plots pipeline for data types: {data_types}")

    results = {}

    for data_type in data_types:
        try:
            logger.info(f"Processing plots for {data_type}")
            data_type_results = []

            for plot_format in plot_formats:
                try:
                    saved_path = run_gene_pathway_plotting_pipeline(
                        data_type=data_type,
                        output_dir=output_dir,
                        plot_format=plot_format,
                        use_plotly=use_plotly,
                    )
                    data_type_results.append(saved_path)
                    logger.info(
                        f"Successfully created {plot_format} plot for {data_type}"
                    )

                except Exception as e:
                    logger.warning(
                        f"Failed to create {plot_format} plot for {data_type}: "
                        f"{str(e)}"
                    )
                    continue

            results[data_type] = data_type_results

        except Exception as e:
            logger.error(f"Failed to process {data_type}: {str(e)}")
            results[data_type] = []
            continue

    logger.info("Multiple plots pipeline completed")
    return results
