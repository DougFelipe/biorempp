"""
input_loader.py
---------------
Central Input Processing and Database Merging Orchestration Module

This module provides the main orchestration function for the complete
BioRemPP input processing pipeline. It coordinates input validation,
format processing, and database merging operations into a single,
streamlined workflow.

The module acts as the primary entry point for CLI and programmatic
interfaces, handling the complete data flow from raw input files to
merged biological datasets ready for downstream analysis.

Main Functions:
    - load_and_merge_input: Complete pipeline orchestration function

Pipeline Flow:
    1. Input validation and format checking
    2. Data parsing and structure validation
    3. Database merging with specified reference database
    4. Type optimization for memory efficiency
    5. Error handling and logging throughout
"""

import logging

from biorempp.input_processing.biorempp_merge_processing import (
    merge_input_with_biorempp,
)
from biorempp.input_processing.input_validator import validate_and_process_input

# Technical logging (silent to console, file only)
logger = logging.getLogger("biorempp.input_processing.input_loader")


def load_and_merge_input(
    contents: str,
    filename: str,
    database_filepath: str = "src/biorempp/data/database_biorempp.csv",
    optimize_types: bool = True,
    merge_function=None,
) -> tuple:
    """
    Complete pipeline: validates, processes, and merges input with database.

    This function orchestrates the entire input processing workflow, from
    raw file contents to merged biological datasets. It handles validation,
    format processing, database integration, and error management in a
    unified pipeline suitable for both CLI and programmatic use.

    Parameters
    ----------
    contents : str
        Contents of the input file. Can be plain text or base64-encoded
        data URI format (data:text/plain;base64,<encoded_content>).
    filename : str
        Name of the input file, used for format validation and logging.
        Must have .txt extension.
    database_filepath : str, optional
        Path to the reference database CSV file. Default points to the
        BioRemPP database. Can be customized for different database types.
    optimize_types : bool, optional
        If True, applies DataFrame dtype optimization to reduce memory
        usage through categorical conversions. Default: True.
    merge_function : callable, optional
        Custom merge function to use for database integration. If None,
        uses merge_input_with_biorempp as default. Function should accept
        (df_input, database_filepath, optimize_types) parameters.

    Returns
    -------
    tuple[pd.DataFrame | None, str | None]
        A tuple containing:
        - DataFrame: Successfully merged data, or None if error occurred
        - str: Error message if processing failed, or None if successful

    Examples
    --------
    >>> contents = ">Sample1\\nK00001\\nK00002\\n>Sample2\\nK00003"
    >>> result_df, error = load_and_merge_input(contents, "input.txt")
    >>> if error is None:
    ...     print(f"Success: {result_df.shape[0]} rows merged")
    ... else:
    ...     print(f"Error: {error}")

    Notes
    -----
    - Input format expects structure with sample IDs and KO entries
    - Base64 decoding is automatically handled for web uploads
    - All errors are logged and returned as descriptive messages
    - The function maintains transaction-like behavior: all or nothing
    """
    logger.info("Starting input validation and merging pipeline.")

    # Use default merge function if none provided
    if merge_function is None:
        merge_function = merge_input_with_biorempp

    # 1. Validate and parse input
    df_input, error = validate_and_process_input(contents, filename)
    if error:
        logger.error(f"Input validation/processing error: {error}")
        return None, f"Input processing error: {error}"

    # 2. Merge with reference database
    try:
        df_merged = merge_function(
            df_input,
            database_filepath=database_filepath,
            optimize_types=optimize_types,
        )
        logger.info("Database merge completed successfully.")
        return df_merged, None
    except Exception as e:
        logger.exception("Database merge failed.")
        return None, f"Database merge error: {e}"
