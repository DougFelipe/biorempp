"""
HADEG Database Merge Processing Module

This module provides functionality to merge input data with the HADEG
(Hydrocarbon Degradation Database) using KEGG Ortholog identifiers.
"""

import logging
import os

import pandas as pd

# Technical logging (silent to console, file only)
logger = logging.getLogger("biorempp.input_processing.hadeg_merge_processing")


def merge_input_with_hadeg(
    input_data: pd.DataFrame,
    database_filepath: str = None,
    optimize_types: bool = True,
) -> pd.DataFrame:
    """
    Merge input data with the HADEG database using 'ko' column.

    Parameters
    ----------
    input_data : pd.DataFrame
        DataFrame containing at least the 'ko' column.
    database_filepath : str, optional
        Path to the HADEG database CSV file. If None, uses default path.
    optimize_types : bool, optional
        Whether to optimize DataFrame types using categoricals. Default: True.

    Returns
    -------
    pd.DataFrame
        Merged DataFrame containing rows with matching 'ko' values.

    Raises
    ------
    FileNotFoundError
        If the database file is not found.
    ValueError
        If the file is not a .csv.
    KeyError
        If 'ko' column is missing in either DataFrame.
    TypeError
        If input_data is not a pandas DataFrame.

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({'ko': ['K00001', 'K00002']})
    >>> merged_df = merge_input_with_hadeg(df)
    >>> print(merged_df.shape)
    """
    if not isinstance(input_data, pd.DataFrame):
        logger.error("Input must be a pandas DataFrame.")
        raise TypeError("Input must be a pandas DataFrame.")

    if database_filepath is None:
        this_dir = os.path.dirname(os.path.abspath(__file__))
        database_filepath = os.path.join(this_dir, "..", "data", "database_hadeg.csv")
    logger.info(f"Using HADEG database file: {database_filepath}")

    # Check file existence
    if not os.path.exists(database_filepath):
        logger.error(f"Database file not found: {database_filepath}")
        raise FileNotFoundError(f"Database file not found: {database_filepath}")

    # Only CSV files are supported
    if not database_filepath.lower().endswith(".csv"):
        logger.error("Unsupported file format. Use .csv")
        raise ValueError("Unsupported file format. Use .csv")

    # Load database
    try:
        database_df = pd.read_csv(database_filepath, encoding="utf-8", sep=";")
        logger.info(
            "HADEG database loaded (%d rows, %d columns)",
            database_df.shape[0],
            database_df.shape[1],
        )
    except Exception:
        logger.exception("Error loading HADEG database CSV.")
        raise

    # Optimize types if requested
    if optimize_types:
        database_df = optimize_dtypes_hadeg(database_df)
        input_data = optimize_dtypes_hadeg(input_data.copy())
        logger.info("Types optimized with optimize_dtypes_hadeg.")

    # Validate presence of 'ko' column
    for df_name, df in {"input_data": input_data, "database_df": database_df}.items():
        if "ko" not in df.columns:
            logger.error(f"Missing 'ko' column in {df_name}.")
            raise KeyError(
                "Column 'ko' must be present in both input and database DataFrames."
            )

    # Perform merge on 'ko' field
    merged_df = pd.merge(input_data, database_df, on="ko", how="inner")

    if optimize_types:
        merged_df = optimize_dtypes_hadeg(merged_df)

    logger.info(f"Merge completed. Final shape: {merged_df.shape}")
    return merged_df


def optimize_dtypes_hadeg(df: pd.DataFrame) -> pd.DataFrame:
    """
    Optimize HADEG DataFrame types by converting repetitive columns to categorical.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.

    Returns
    -------
    pd.DataFrame
        DataFrame with optimized types.

    Raises
    ------
    TypeError
        If input is not a pandas DataFrame.
    """
    if not isinstance(df, pd.DataFrame):
        logger.error("Input must be a pandas DataFrame.")
        raise TypeError("Input must be a pandas DataFrame.")

    categorical_columns = [
        "Gene",
        "ko",
        "Pathway",
        "compound_pathway",
        "sample",
    ]

    for col in categorical_columns:
        if col in df.columns:
            logger.debug(f"Converting column '{col}' to categorical.")
            df[col] = df[col].astype("category")

    logger.info("HADEG DataFrame type optimization completed.")
    return df
