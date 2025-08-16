"""
    biorempp_merge_processing.py
----------------------------
---------------------------
BioRemPP Database Merge Processing Module

This module provides functionality to merge input biological data with the
BioRemPP reference database. It handles data validation, type optimization,
and efficient merging operations for bioremediation analysis.

The module supports CSV-format databases with semicolon delimiters and
includes memory optimization features through categorical data types.

Main Functions:
    - merge_input_with_biorempp: Core merge function for BioRemPP database
    - optimize_dtypes_biorempp: Memory optimization for BioRemPP DataFrames

Database Schema:
    The BioRemPP database contains columns including 'ko', 'genesymbol',
    'genename', 'cpd', 'compoundclass', 'referenceAG', 'compoundname',
    and 'enzyme_activity' among others.
"""

import logging
import os

import pandas as pd

# Technical logging (silent to console, file only)
logger = logging.getLogger("biorempp.input_processing.biorempp_merge_processing")


def merge_input_with_biorempp(
    input_data: pd.DataFrame,
    database_filepath: str = None,
    optimize_types: bool = True,
) -> pd.DataFrame:
    """
    Merge input data with BioRemPP reference database in CSV format.

    This function performs an inner join between the input biological data
    and the BioRemPP reference database using the 'ko' (KEGG Orthology)
    column as the merge key. The BioRemPP database contains comprehensive
    information about genes, compounds, and enzymes for bioremediation.

    Parameters
    ----------
    input_data : pd.DataFrame
        Input DataFrame containing at least the 'ko' column with KEGG
        orthology identifiers.
    database_filepath : str, optional
        Path to BioRemPP database file (.csv). If None, defaults to
        'data/database_biorempp.csv' in the current working directory.
    optimize_types : bool, optional
        If True, applies dtype optimization using optimize_dtypes_biorempp
        to reduce memory usage through categorical conversions. Default: True.

    Returns
    -------
    pd.DataFrame
        Merged DataFrame containing all columns from both input and database
        DataFrames. Only rows with matching 'ko' values are included
        (inner join).

    Raises
    ------
    FileNotFoundError
        If the specified database file does not exist.
    ValueError
        If the database file is not in .csv format.
    KeyError
        If the 'ko' column is missing in either input_data or database.
    TypeError
        If input_data is not a pandas DataFrame.
    Exception
        If there are issues reading the CSV file (encoding, format, etc.).

    Examples
    --------
    >>> import pandas as pd
    >>> input_df = pd.DataFrame({'ko': ['K00001', 'K00002'], 'sample': ['S1', 'S2']})
    >>> result = merge_input_with_biorempp(input_df)
    >>> print(result.shape)
    (2, 5)
    Notes
    -----
    - The database file must use semicolon (;) as the delimiter
    - UTF-8 encoding is expected for proper character handling
    - Memory optimization converts repetitive columns to categorical types
    - The merge operation preserves all columns from both DataFrames
    """
    if database_filepath is None:
        database_filepath = os.path.join("data", "database_biorempp.csv")
    logger.info(f"Using database file: {database_filepath}")

    # Check file existence
    if not os.path.exists(database_filepath):
        logger.error(f"Database file not found: {database_filepath}")
        raise FileNotFoundError(f"Database file not found: {database_filepath}")

    # Only .csv accepted
    if not database_filepath.lower().endswith(".csv"):
        logger.error("Unsupported file format. Use .csv")
        raise ValueError("Unsupported file format. Use .csv")

    # Load database

    try:
        database_df = pd.read_csv(database_filepath, encoding="utf-8", sep=";")
        logger.info(
            "Database loaded (%d rows, %d columns)",
            database_df.shape[0],
            database_df.shape[1],
        )
    except Exception:
        logger.exception("Error loading database CSV.")
        raise

    # Optimize types if requested
    if optimize_types:
        database_df = optimize_dtypes_biorempp(database_df)
        input_data = optimize_dtypes_biorempp(input_data.copy())
        logger.info("Types optimized with optimize_dtypes_biorempp.")

    # Validate presence of 'ko' column
    for df_name, df in {"input_data": input_data, "database_df": database_df}.items():
        if "ko" not in df.columns:
            logger.error(f"Missing 'ko' column in {df_name}.")
            raise KeyError(
                "Column 'ko' must be present in both input and database DataFrames."
            )

    # Perform merge by 'ko' field
    merged_df = pd.merge(input_data, database_df, on="ko", how="inner")

    if optimize_types:
        merged_df = optimize_dtypes_biorempp(merged_df)

    logger.info(f"Merge completed. Final shape: {merged_df.shape}")
    return merged_df


def optimize_dtypes_biorempp(df: pd.DataFrame) -> pd.DataFrame:
    """
    Optimize column types for BioRemPP DataFrames to reduce memory usage.

    This function converts frequently repeated string columns to categorical
    data types, which significantly reduces memory consumption for large
    datasets. It targets columns commonly found in BioRemPP biological data.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame with BioRemPP data columns.

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
    - 'ko': KEGG Orthology identifiers
    - 'genesymbol': Gene symbols
    - 'genename': Full gene names
    - 'cpd': Compound identifiers
    - 'compoundclass': Chemical compound classifications
    - 'referenceAG': Reference agencies information
    - 'compoundname': Compound names
    - 'enzyme_activity': Enzyme activity descriptions
    - 'sample': Sample identifiers

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     'ko': ['K00001', 'K00001', 'K00002'],
    ...     'genesymbol': ['geneA', 'geneA', 'geneB']
    ... })
    >>> optimized_df = optimize_dtypes_biorempp(df)
    >>> print(optimized_df.dtypes)
    ko           category
    genesymbol   category
    dtype: object
    """
    if not isinstance(df, pd.DataFrame):
        logger.error("Input must be a pandas DataFrame.")
        raise TypeError("Input must be a pandas DataFrame.")

    categorical_columns = [
        "ko",
        "genesymbol",
        "genename",
        "cpd",
        "compoundclass",
        "referenceAG",
        "compoundname",
        "enzyme_activity",
        "sample",
    ]

    for col in categorical_columns:
        if col in df.columns:
            logger.debug(f"Converting column '{col}' to categorical.")
            df[col] = df[col].astype("category")
    logger.info("Dtype optimization completed.")
    return df
