"""
kegg_merge_processing.py
-----------------------
KEGG Degradation Pathways Database Merge Processing Module

This module provides functionality to merge input biological data with the
KEGG (Kyoto Encyclopedia of Genes and Genomes) degradation pathways database.
It specializes in connecting KO (KEGG Orthology) identifiers with degradation
pathway information for environmental bioremediation analysis.

The module handles CSV-format KEGG databases with semicolon delimiters and
includes memory optimization through categorical data types for pathway
and gene information.

Main Functions:
    - merge_input_with_kegg: Core merge function for KEGG pathway database
    - optimize_dtypes_kegg: Memory optimization for KEGG DataFrames

Database Schema:
    The KEGG database contains columns including 'ko', 'pathname',
    'genesymbol', and 'sample' for pathway-gene relationships.

Available at: https://www.genome.jp/kegg/pathway.html#xenobiotics
"""

import logging
import os

import pandas as pd

# Technical logging (silent to console, file only)
logger = logging.getLogger("biorempp.input_processing.kegg_merge_processing")


def merge_input_with_kegg(
    input_data: pd.DataFrame,
    kegg_filepath: str = None,
    optimize_types: bool = True,
) -> pd.DataFrame:
    """
    Merge input data with KEGG degradation pathway information from CSV file.

    This function performs an inner join between input biological data and
    the KEGG (Kyoto Encyclopedia of Genes and Genomes) degradation pathways
    database using 'ko' identifiers. It provides pathway context for
    environmental degradation processes.

    Parameters
    ----------
    input_data : pd.DataFrame
        Input DataFrame containing at least a 'ko' column with KEGG
        orthology identifiers.
    kegg_filepath : str, optional
        Path to the KEGG degradation pathways CSV file. If None, defaults
        to 'data/kegg_degradation_pathways.csv'.
    optimize_types : bool, optional
        If True, optimizes DataFrame dtypes using categorical columns for
        memory efficiency. Default: True.

    Returns
    -------
    pd.DataFrame
        Merged DataFrame containing input data enriched with KEGG pathway
        information. Only rows with matching 'ko' values are included.

    Raises
    ------
    FileNotFoundError
        If the specified KEGG file does not exist.
    ValueError
        If the file extension is not .csv.
    KeyError
        If the 'ko' column is missing in either input DataFrame or KEGG
        database.
    TypeError
        If input_data is not a pandas DataFrame.
    Exception
        If there are issues reading the CSV file.

    Examples
    --------
    >>> import pandas as pd
    >>> input_df = pd.DataFrame({
    ...     'ko': ['K00001', 'K00002'],
    ...     'sample': ['Sample1', 'Sample2']
    ... })
    >>> result = merge_input_with_kegg(input_df)
    >>> print('pathname' in result.columns)
    True

    Notes
    -----
    - KEGG database file must use semicolon (;) as delimiter
    - UTF-8 encoding is expected for proper character handling
    - Pathway names are stored in the 'pathname' column
    - Gene symbols are available in the 'genesymbol' column
    """
    if kegg_filepath is None:
        kegg_filepath = os.path.join("data", "kegg_degradation_pathways.csv")
    logger.info(f"Using KEGG file: {kegg_filepath}")

    # Check file existence
    if not os.path.exists(kegg_filepath):
        logger.error(f"KEGG file not found: {kegg_filepath}")
        raise FileNotFoundError(f"KEGG file not found: {kegg_filepath}")

    # Only .csv files are supported
    if not kegg_filepath.lower().endswith(".csv"):
        logger.error("Unsupported file format. Use .csv")
        raise ValueError("Unsupported file format. Use .csv")

    # Load KEGG database
    try:
        kegg_df = pd.read_csv(kegg_filepath, encoding="utf-8", sep=";")
        logger.info(
            "KEGG database loaded (%d rows, %d columns)",
            kegg_df.shape[0],
            kegg_df.shape[1],
        )
    except Exception:
        logger.exception("Error loading KEGG CSV.")
        raise

    # Optimize types if requested
    if optimize_types:
        kegg_df = optimize_dtypes_kegg(kegg_df)
        input_data = optimize_dtypes_kegg(input_data.copy())
        logger.info("Types optimized with optimize_dtypes_kegg.")

    # Validate presence of 'ko' column
    for df_name, df in {"input_data": input_data, "kegg_df": kegg_df}.items():
        if "ko" not in df.columns:
            logger.error(f"Missing 'ko' column in {df_name}.")
            raise KeyError(
                "Column 'ko' must be present in both input and KEGG DataFrames."
            )

    # Perform merge on 'ko' field
    merged_df = pd.merge(input_data, kegg_df, on="ko", how="inner")

    if optimize_types:
        merged_df = optimize_dtypes_kegg(merged_df)

    logger.info(f"Merge completed. Final shape: {merged_df.shape}")
    return merged_df


def optimize_dtypes_kegg(df: pd.DataFrame) -> pd.DataFrame:
    """
    Optimize column types for KEGG degradation pathways data.

    This function converts repetitive string columns to categorical data types
    to reduce memory consumption. It targets columns commonly found in KEGG
    pathway databases for environmental degradation analysis.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame with KEGG pathway data.

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
    - 'pathname': Degradation pathway names
    - 'genesymbol': Gene symbols associated with pathways
    - 'sample': Sample identifiers

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     'ko': ['K00001', 'K00001', 'K00002'],
    ...     'pathname': ['pathway1', 'pathway1', 'pathway2']
    ... })
    >>> optimized_df = optimize_dtypes_kegg(df)
    >>> print(optimized_df['ko'].dtype)
    category
    """
    if not isinstance(df, pd.DataFrame):
        logger.error("Input must be a pandas DataFrame.")
        raise TypeError("Input must be a pandas DataFrame.")

    categorical_columns = [
        "ko",
        "pathname",
        "genesymbol",
        "sample",
    ]

    for col in categorical_columns:
        if col in df.columns:
            logger.debug(f"Converting column '{col}' to categorical.")
            df[col] = df[col].astype("category")
    logger.info("KEGG dtypes optimization completed.")
    return df
