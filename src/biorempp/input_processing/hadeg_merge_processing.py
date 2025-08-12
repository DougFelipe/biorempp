"""
hadeg_merge_processing.py
-------------------------
HADEG Database Merge Processing Module

This module provides functionality to merge input biological data with the
HADEG (Hydrocarbon Degradation Database). HADEG specializes in genes and
pathways involved in hydrocarbon degradation processes, making it essential
for environmental bioremediation analysis and contamination studies.

The module handles CSV-format HADEG databases with semicolon delimiters and
includes memory optimization through categorical data types for gene and
pathway information commonly found in hydrocarbon degradation research.

Main Functions:
    - merge_input_with_hadeg: Core merge function for HADEG database
    - optimize_dtypes_hadeg: Memory optimization for HADEG DataFrames

Database Schema:
    The HADEG database contains columns including 'ko', 'Gene', 'Pathway',
    'compound_pathway', and 'sample' for hydrocarbon degradation gene-pathway
    relationships and compound degradation information.

Use Cases:
    - Hydrocarbon contamination bioremediation analysis
    - Petroleum degradation pathway identification
    - Environmental cleanup gene expression studies
    - Oil spill remediation potential assessment

Available at: https://github.com/jarojasva/HADEG
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
    Merge input data with HADEG database using 'ko' column.

    This function performs an inner join between input biological data and
    the HADEG (Hydrocarbon Degradation Database) using 'ko' identifiers.
    HADEG provides comprehensive information about genes and pathways involved
    in hydrocarbon degradation, essential for environmental bioremediation.

    Parameters
    ----------
    input_data : pd.DataFrame
        Input DataFrame containing at least the 'ko' column with KEGG
        orthology identifiers.
    database_filepath : str, optional
        Path to the HADEG database CSV file. If None, uses default path
        '../data/database_hadeg.csv' relative to module location.
    optimize_types : bool, optional
        Whether to optimize DataFrame types using categorical conversions
        for memory efficiency. Default: True.

    Returns
    -------
    pd.DataFrame
        Merged DataFrame containing input data enriched with HADEG hydrocarbon
        degradation information. Only rows with matching 'ko' values are
        included (inner join).

    Raises
    ------
    FileNotFoundError
        If the specified HADEG database file is not found.
    ValueError
        If the database file is not in .csv format.
    KeyError
        If the 'ko' column is missing in either input_data or HADEG database.
    TypeError
        If input_data is not a pandas DataFrame.
    Exception
        If there are issues reading the CSV file (encoding, format, etc.).

    Examples
    --------
    >>> import pandas as pd
    >>> input_df = pd.DataFrame({
    ...     'ko': ['K00001', 'K00002'],
    ...     'sample': ['Oil_Sample_1', 'Oil_Sample_2']
    ... })
    >>> result = merge_input_with_hadeg(input_df)
    >>> print('Pathway' in result.columns)
    True

    Notes
    -----
    - HADEG database file must use semicolon (;) as delimiter
    - UTF-8 encoding is expected for proper character handling
    - Gene information is stored in the 'Gene' column
    - Pathway data is available in 'Pathway' and 'compound_pathway' columns
    - Optimized for hydrocarbon degradation pathway analysis
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
    Optimize HADEG DataFrame types for memory efficiency and performance.

    This function converts repetitive string columns to categorical data types
    to reduce memory consumption. It targets columns commonly found in HADEG
    hydrocarbon degradation databases for environmental analysis.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame with HADEG hydrocarbon degradation data.

    Returns
    -------
    pd.DataFrame
        DataFrame with optimized categorical data types for memory efficiency.

    Raises
    ------
    TypeError
        If the input is not a pandas DataFrame.

    Notes
    -----
    Optimized columns include:
    - 'Gene': Gene identifiers involved in hydrocarbon degradation
    - 'ko': KEGG Orthology identifiers
    - 'Pathway': Degradation pathway names and classifications
    - 'compound_pathway': Specific compound degradation pathways
    - 'sample': Sample identifiers from environmental studies

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     'ko': ['K00001', 'K00001', 'K00002'],
    ...     'Gene': ['alkB', 'alkB', 'catA'],
    ...     'Pathway': ['alkane_degradation', 'alkane_degradation', 'aromatic']
    ... })
    >>> optimized_df = optimize_dtypes_hadeg(df)
    >>> print(optimized_df['Gene'].dtype)
    category
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
