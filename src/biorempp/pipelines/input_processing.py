"""
input_processing.py
------------------
BioRemPP Database-Specific Processing Pipelines

This module contains the complete processing pipelines for each supported
database in the BioRemPP ecosystem. Each pipeline handles the full workflow
from input validation to output generation, tailored to the specific
requirements and data structures of each database.

These pipelines serve as the primary interface for data processing operations,
integrating multiple processing components into cohesive, database-specific
workflows suitable for production use.

Supported Databases:
    1. BioRemPP: Core bioremediation database
    2. KEGG: Degradation pathway information from KEGG
    3. HADEG: Hydrocarbon degradation gene database
    4. ToxCSM: Toxicity prediction and chemical safety database

Pipeline Features:
    - Input validation and format checking
    - Database-specific merging strategies
    - Memory optimization through categorical types
    - Comprehensive error handling and logging
    - Structured output generation with metadata
    - Configurable output directories and file formats

Common Pipeline Flow:
    1. Input file existence validation
    2. Content reading and parsing
    3. Data validation and format checking
    4. Database-specific merging operations
    5. Type optimization for memory efficiency
    6. Output file generation and saving
    7. Structured result reporting

Return Format:
    All pipelines return a dictionary with:
    - 'output_path': Full path to the generated output file
    - 'matches': Number of successful database matches
    - 'filename': Base name of the output file

Error Handling:
    - FileNotFoundError: For missing input files
    - RuntimeError: For processing or merging errors
    - Comprehensive logging throughout the pipeline
"""

import os

from biorempp.input_processing.hadeg_merge_processing import merge_input_with_hadeg
from biorempp.input_processing.input_loader import load_and_merge_input
from biorempp.input_processing.kegg_merge_processing import merge_input_with_kegg
from biorempp.input_processing.toxcsm_merge_processing import merge_input_with_toxcsm
from biorempp.utils.io_utils import save_dataframe_output
from biorempp.utils.logging_config import get_logger

logger = get_logger("pipelines.input_processing")


def run_biorempp_processing_pipeline(
    input_path,
    database_path=None,
    output_dir="outputs/results_tables",
    output_filename="BioRemPP_Results.txt",
    sep=";",
    optimize_types=True,
    add_timestamp=False,
):
    """
    Run complete BioRemPP database processing pipeline.

    This pipeline performs comprehensive validation, processing, and merging
    of input with the BioRemPP reference database. It handles the
    complete workflow from raw input to analysis-ready output files.

    Parameters
    ----------
    input_path : str
        Path to the input .txt file containing biological data in
        format with sample IDs and KO entries.
    database_path : str, optional
        Path to the BioRemPP database CSV file. If None, uses default path
        '../data/database_biorempp.csv' relative to module location.
    output_dir : str, optional
        Directory where the merged DataFrame will be saved. Directory will
        be created if it doesn't exist. Default: 'outputs/results_tables'.
    output_filename : str, optional
        Name of the output file. Default: 'BioRemPP_Results.txt'.
    sep : str, optional
        Field separator for output file. Default: ';'.
    optimize_types : bool, optional
        Whether to optimize DataFrame dtypes using categorical conversions
        for memory efficiency. Default: True.
    add_timestamp : bool, optional
        Whether to add timestamp to output filename. Default: False.

    Returns
    -------
    dict
        Processing results containing:
        - 'output_path' (str): Full path to the generated output file
        - 'matches' (int): Number of successful database matches
        - 'filename' (str): Base name of the output file

    Raises
    ------
    FileNotFoundError
        If the input file does not exist.
    RuntimeError
        If there is an error in processing, validation, or merging operations.

    Examples
    --------
    >>> result = run_biorempp_processing_pipeline("sample_data.txt")
    >>> print(f"Processed {result['matches']} matches")
    >>> print(f"Output saved to: {result['output_path']}")

    >>> # Custom database and output settings
    >>> result = run_biorempp_processing_pipeline(
    ...     "input.txt",
    ...     database_path="custom_biorempp.csv",
    ...     output_dir="custom_output",
    ...     add_timestamp=True
    ... )

    Notes
    -----
    - Input file must be in format with > for sample IDs
    - Database file must use semicolon (;) as delimiter
    - UTF-8 encoding is expected for all files
    - Output includes all columns from both input and database
    - Processing time and memory usage scale with input size
    """
    logger.info(f"Starting input processing pipeline for: {input_path}")
    logger.debug(
        f"Pipeline parameters - database: {database_path}, "
        f"output_dir: {output_dir}, optimize_types: {optimize_types}"
    )

    if not os.path.exists(input_path):
        error_msg = f"Input file not found: {input_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    if database_path is None:
        this_dir = os.path.dirname(os.path.abspath(__file__))
        database_path = os.path.normpath(
            os.path.join(this_dir, "..", "data", "database_biorempp.csv")
        )
        logger.debug(f"Using default database path: {database_path}")

    logger.info(f"Reading input file: {input_path}")
    with open(input_path, "r", encoding="utf-8") as f:
        input_content = f.read()

    logger.info("Loading and merging input data")
    df, error = load_and_merge_input(
        input_content,
        os.path.basename(input_path),
        database_filepath=database_path,
        optimize_types=optimize_types,
    )

    if error:
        error_msg = f"Pipeline error: {error}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)

    logger.info(f"Saving merged DataFrame to: {output_dir}/{output_filename}")
    output_path = save_dataframe_output(
        df,
        output_dir=output_dir,
        filename=output_filename,
        sep=sep,
        add_timestamp=add_timestamp,
    )

    logger.info(f"Pipeline completed successfully. Output saved to: {output_path}")

    # Return structured data for user feedback
    return {
        "output_path": output_path,
        "matches": len(df) if df is not None else 0,
        "filename": os.path.basename(output_path),
    }


def run_kegg_processing_pipeline(
    input_path,
    kegg_database_path=None,
    output_dir="outputs/results_tables",
    output_filename="KEGG_Results.txt",
    sep=";",
    optimize_types=True,
    add_timestamp=False,
):
    """
    Run complete KEGG degradation pathway processing pipeline.

    This pipeline validates, processes, and merges input with the
    KEGG (Kyoto Encyclopedia of Genes and Genomes) degradation pathways
    database. It provides pathway context for environmental degradation
    processes and bioremediation analysis.

    Parameters
    ----------
    input_path : str
        Path to the input .txt file containing biological data in
        format with sample IDs and KO entries.
    kegg_database_path : str, optional
        Path to the KEGG degradation pathways CSV file. If None, uses default
        path '../data/kegg_degradation_pathways.csv' relative to module.
    output_dir : str, optional
        Directory where the merged DataFrame will be saved. Directory will
        be created if it doesn't exist. Default: 'outputs/results_tables'.
    output_filename : str, optional
        Name of the output file. Default: 'KEGG_Results.txt'.
    sep : str, optional
        Field separator for output file. Default: ';'.
    optimize_types : bool, optional
        Whether to optimize DataFrame dtypes using categorical conversions
        for memory efficiency. Default: True.
    add_timestamp : bool, optional
        Whether to add timestamp to output filename. Default: False.

    Returns
    -------
    dict
        Processing results containing:
        - 'output_path' (str): Full path to the generated output file
        - 'matches' (int): Number of successful KEGG pathway matches
        - 'filename' (str): Base name of the output file

    Raises
    ------
    FileNotFoundError
        If the input file does not exist.
    RuntimeError
        If there is an error in processing, validation, or merging operations.

    Examples
    --------
    >>> result = run_kegg_processing_pipeline("sample_data.txt")
    >>> print(f"Found {result['matches']} pathway matches")
    >>> print(f"KEGG results saved to: {result['output_path']}")

    >>> # Custom output settings
    >>> result = run_kegg_processing_pipeline(
    ...     "input.txt",
    ...     output_dir="kegg_analysis",
    ...     output_filename="pathways_2024.txt"
    ... )

    Notes
    -----
    - Input file must be in format with > for sample IDs
    - KEGG database file must use semicolon (;) as delimiter
    - UTF-8 encoding is expected for all files
    - Output includes pathway names in 'pathname' column
    - Gene symbols are available in 'genesymbol' column
    - Optimized for degradation pathway analysis
    """
    from biorempp.input_processing.input_validator import validate_and_process_input

    logger.info(f"Starting KEGG processing pipeline for: {input_path}")
    logger.debug(
        f"Pipeline parameters - kegg_database: {kegg_database_path}, "
        f"output_dir: {output_dir}, optimize_types: {optimize_types}"
    )

    if not os.path.exists(input_path):
        error_msg = f"Input file not found: {input_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    if kegg_database_path is None:
        this_dir = os.path.dirname(os.path.abspath(__file__))
        kegg_database_path = os.path.normpath(
            os.path.join(this_dir, "..", "data", "kegg_degradation_pathways.csv")
        )
        logger.debug(f"Using default KEGG database path: {kegg_database_path}")
        logger.debug(f"Using default KEGG database path: {kegg_database_path}")

    logger.info(f"Reading input file: {input_path}")
    with open(input_path, "r", encoding="utf-8") as f:
        input_content = f.read()

    # Validate and process input
    logger.info("Validating and processing input data")
    df, error = validate_and_process_input(input_content, os.path.basename(input_path))

    if error:
        error_msg = f"KEGG pipeline validation error: {error}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)

    # Merge with KEGG database
    logger.info("Merging with KEGG degradation pathways")
    kegg_merged_df = merge_input_with_kegg(
        df, kegg_filepath=kegg_database_path, optimize_types=optimize_types
    )

    logger.info(f"Saving KEGG merged DataFrame to: {output_dir}/{output_filename}")
    output_path = save_dataframe_output(
        kegg_merged_df,
        output_dir=output_dir,
        filename=output_filename,
        sep=sep,
        add_timestamp=add_timestamp,
    )

    logger.info(f"KEGG pipeline completed successfully. Output saved to: {output_path}")

    # Return structured data for user feedback
    return {
        "output_path": output_path,
        "matches": len(kegg_merged_df) if kegg_merged_df is not None else 0,
        "filename": os.path.basename(output_path),
    }


def run_hadeg_processing_pipeline(
    input_path,
    hadeg_database_path=None,
    output_dir="outputs/results_tables",
    output_filename="HADEG_Results.txt",
    sep=";",
    optimize_types=True,
    add_timestamp=False,
):
    """
    Run complete HADEG hydrocarbon degradation processing pipeline.

    This pipeline validates, processes, and merges input with the
    HADEG, specialized in genes and pathways involved in hydrocarbon
    degradation, plastics and biosurfactants.

    Parameters
    ----------
    input_path : str
        Path to the input .txt file containing biological data in
        format with sample IDs and KO entries.
    hadeg_database_path : str, optional
        Path to the HADEG database CSV file. If None, uses default path
        '../data/database_hadeg.csv' relative to module location.
    output_dir : str, optional
        Directory where the merged DataFrame will be saved. Directory will
        be created if it doesn't exist. Default: 'outputs/results_tables'.
    output_filename : str, optional
        Name of the output file. Default: 'HADEG_Results.txt'.
    sep : str, optional
        Field separator for output file. Default: ';'.
    optimize_types : bool, optional
        Whether to optimize DataFrame dtypes using categorical conversions
        for memory efficiency. Default: True.
    add_timestamp : bool, optional
        Whether to add timestamp to output filename. Default: False.

    Returns
    -------
    dict
        Processing results containing:
        - 'output_path' (str): Full path to the generated output file
        - 'matches' (int): Number of successful HADEG database matches
        - 'filename' (str): Base name of the output file

    Raises
    ------
    FileNotFoundError
        If the input file does not exist.
    RuntimeError
        If there is an error in processing, validation, or merging operations.

    Examples
    --------
    >>> result = run_hadeg_processing_pipeline("oil_sample.txt")
    >>> print(f"Found {result['matches']} hydrocarbon degradation genes")
    >>> print(f"HADEG results saved to: {result['output_path']}")

    >>> # Environmental cleanup analysis
    >>> result = run_hadeg_processing_pipeline(
    ...     "petroleum_site.txt",
    ...     output_dir="cleanup_analysis",
    ...     output_filename="hydrocarbon_degradation.txt"
    ... )

    Notes
    -----
    - Input file must be in format with > for sample IDs
    - HADEG database file must use semicolon (;) as delimiter
    - UTF-8 encoding is expected for all files
    - Output includes gene information in 'Gene' column
    - Pathway data available in 'Pathway' and 'compound_pathway' columns
    - Specialized for hydrocarbon contamination analysis
    - Ideal for petroleum spill and industrial contamination studies
    """
    logger.info(f"Starting HADEG processing pipeline for: {input_path}")
    logger.debug(
        f"Pipeline parameters - database: {hadeg_database_path}, "
        f"output_dir: {output_dir}, optimize_types: {optimize_types}"
    )

    if not os.path.exists(input_path):
        error_msg = f"Input file not found: {input_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    if hadeg_database_path is None:
        this_dir = os.path.dirname(os.path.abspath(__file__))
        hadeg_database_path = os.path.normpath(
            os.path.join(this_dir, "..", "data", "database_hadeg.csv")
        )
        logger.debug(f"Using default HADEG database path: {hadeg_database_path}")

    logger.info(f"Reading input file: {input_path}")
    with open(input_path, "r", encoding="utf-8") as f:
        input_content = f.read()

    logger.info("Loading and merging input data with HADEG database")
    df, error = load_and_merge_input(
        input_content,
        os.path.basename(input_path),
        database_filepath=hadeg_database_path,
        optimize_types=optimize_types,
        merge_function=merge_input_with_hadeg,
    )

    if error:
        error_msg = f"HADEG Pipeline error: {error}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)

    logger.info(f"Saving merged DataFrame to: {output_dir}/{output_filename}")
    output_path = save_dataframe_output(
        df,
        output_dir=output_dir,
        filename=output_filename,
        sep=sep,
        add_timestamp=add_timestamp,
    )

    logger.info(
        f"HADEG Pipeline completed successfully. Output saved to: {output_path}"
    )

    # Return structured data for user feedback
    return {
        "output_path": output_path,
        "matches": len(df) if df is not None else 0,
        "filename": os.path.basename(output_path),
    }


def run_toxcsm_processing_pipeline(
    input_path,
    toxcsm_database_path=None,
    output_dir="outputs/results_tables",
    output_filename="ToxCSM.txt",
    sep=";",
    optimize_types=True,
    add_timestamp=False,
):
    """
    Run complete ToxCSM toxicity prediction processing pipeline.

    This pipeline performs a two-stage process: first processing input through
    the BioRemPP database to obtain compound identifiers, then merging with
    the ToxCSM database for comprehensive toxicity predictions and chemical
    safety assessment.

    Parameters
    ----------
    input_path : str
        Path to the input .txt file containing biological data in
        format with sample IDs and KO entries.
    toxcsm_database_path : str, optional
        Path to the ToxCSM database CSV file. If None, uses default path
        '../data/database_toxcsm.csv' relative to module location.
    output_dir : str, optional
        Directory where the merged DataFrame will be saved. Directory will
        be created if it doesn't exist. Default: 'outputs/results_tables'.
    output_filename : str, optional
        Name of the output file. Default: 'ToxCSM.txt'.
    sep : str, optional
        Field separator for output file. Default: ';'.
    optimize_types : bool, optional
        Whether to optimize DataFrame dtypes using categorical conversions
        for memory efficiency. Default: True.
    add_timestamp : bool, optional
        Whether to add timestamp to output filename. Default: False.

    Returns
    -------
    dict
        Processing results containing:
        - 'output_path' (str): Full path to the generated output file
        - 'matches' (int): Number of successful ToxCSM database matches
        - 'filename' (str): Base name of the output file

    Raises
    ------
    FileNotFoundError
        If the input file does not exist.
    RuntimeError
        If there is an error in processing, validation, or merging operations.

    Examples
    --------
    >>> result = run_toxcsm_processing_pipeline("sample_data.txt")
    >>> print(f"Found {result['matches']} toxicity predictions")
    >>> print(f"ToxCSM results saved to: {result['output_path']}")

    >>> # Safety assessment analysis
    >>> result = run_toxcsm_processing_pipeline(
    ...     "compounds.txt",
    ...     output_dir="safety_assessment",
    ...     output_filename="toxicity_analysis.txt"
    ... )

    Notes
    -----
    - Input file must be in format with > for sample IDs
    - Two-stage processing: BioRemPP → ToxCSM integration
    - Database files must use semicolon (;) as delimiter
    - UTF-8 encoding is expected for all files
    - Output includes SMILES representations in 'SMILES' column
    - ChEBI identifiers available in 'ChEBI' column
    - Toxicity values in 'value_*' columns (float32 optimized)
    - Toxicity labels in 'label_*' columns (categorical)
    - Optimized for environmental safety assessment
    - Requires 'cpd' column from BioRemPP processing stage
    """
    logger.info(f"Starting ToxCSM processing pipeline for: {input_path}")
    logger.debug(
        f"Pipeline parameters - toxcsm_database: {toxcsm_database_path}, "
        f"output_dir: {output_dir}, optimize_types: {optimize_types}"
    )

    if not os.path.exists(input_path):
        error_msg = f"Input file not found: {input_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    if toxcsm_database_path is None:
        this_dir = os.path.dirname(os.path.abspath(__file__))
        toxcsm_database_path = os.path.normpath(
            os.path.join(this_dir, "..", "data", "database_toxcsm.csv")
        )
        logger.debug(f"Using default ToxCSM database path: {toxcsm_database_path}")

    logger.info(f"Reading input file: {input_path}")
    with open(input_path, "r", encoding="utf-8") as f:
        input_content = f.read()

    # Step 1: Process input through BioRemPP first to get 'cpd' column
    logger.info("Processing input data through BioRemPP pipeline")

    # Define BioRemPP database path for internal use
    biorempp_db_path = None
    if toxcsm_database_path:
        # Use the same directory structure
        biorempp_db_path = os.path.normpath(
            os.path.join(os.path.dirname(toxcsm_database_path), "database_biorempp.csv")
        )

    df_biorempp, error = load_and_merge_input(
        input_content,
        os.path.basename(input_path),
        optimize_types=optimize_types,
        database_filepath=biorempp_db_path,
    )

    if error:
        error_msg = f"BioRemPP processing error: {error}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)

    # Step 2: Merge BioRemPP result with ToxCSM database
    logger.info("Merging BioRemPP data with ToxCSM database")
    df = merge_input_with_toxcsm(
        df_biorempp,
        database_filepath=toxcsm_database_path,
        optimize_types=optimize_types,
    )

    logger.info(f"Saving merged DataFrame to: {output_dir}/{output_filename}")
    output_path = save_dataframe_output(
        df,
        output_dir=output_dir,
        filename=output_filename,
        sep=sep,
        add_timestamp=add_timestamp,
    )

    logger.info(
        f"ToxCSM Pipeline completed successfully. Output saved to: {output_path}"
    )

    # Return structured data for user feedback
    return {
        "output_path": output_path,
        "matches": len(df) if df is not None else 0,
        "filename": os.path.basename(output_path),
    }
