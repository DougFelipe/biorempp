"""
input_loader.py
---------------
Central orchestration function for loading, validating,
and merging FASTA-like input with the BioRemPP database.
"""

from biorempp.input_processing.biorempp_merge_processing import (
    merge_input_with_biorempp,
)
from biorempp.input_processing.input_validator import validate_and_process_input
from biorempp.utils.logging_config import get_logger

logger = get_logger("input_processing.input_loader")


def load_and_merge_input(
    contents: str,
    filename: str,
    database_filepath: str = "src/biorempp/data/database_biorempp.csv",
    optimize_types: bool = True,
    merge_function=None,
) -> tuple:
    """
    Complete pipeline: validates, processes, and merges the input .txt
    with the specified database.

    Parameters
    ----------
    contents : str
        Contents of the input .txt file (plain text or base64).
    filename : str
        Name of the input file.
    database_filepath : str, optional
        Path to the database .csv file
        (default: src/biorempp/data/database_biorempp.csv).
    optimize_types : bool, optional
        If True, applies dtype optimization to the DataFrames.
    merge_function : callable, optional
        Function to use for merging. If None, uses merge_input_with_biorempp.

    Returns
    -------
    tuple
        (final DataFrame, error message or None)
        DataFrame will be None if there is any error in processing or merging.
        Error message will be detailed for UI/logging purposes.

    Example
    -------
    >>> df, err = load_and_merge_input(txt_contents, "input.txt")
    >>> if err: print(err)
    >>> else: print(df.head())
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
