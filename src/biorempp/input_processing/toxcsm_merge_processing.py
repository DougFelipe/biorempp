"""
toxcsm_merge_processing.py
-------------------------
ToxCSM Database Merge Processing Module

This module provides functionality to merge input biological data with the
ToxCSM (Toxicity Computational Screening and Modeling) database. It
specializes in connecting compound identifiers (cpd) with toxicity predictions
and chemical properties for environmental safety assessment.

The module handles CSV-format ToxCSM databases with semicolon delimiters and
includes advanced memory optimization through categorical data types and
float32 conversion for numerical toxicity values.

Main Functions:
    - merge_input_with_toxcsm: Core merge function for ToxCSM database
    - optimize_dtypes_toxcsm: Memory optimization for ToxCSM DataFrames

Database Schema:
    The ToxCSM database contains columns including 'cpd', 'SMILES', 'ChEBI',
    'compoundname', and various 'value_*' and 'label_*' columns for toxicity
    predictions and chemical properties.

Merge Strategy:
    Uses 'cpd' column as merge key and handles column conflicts by prioritizing
    input data while preserving ToxCSM-specific toxicity columns.

Available at: https://biosig.lab.uq.edu.au/toxcsm/
"""

import logging
import os

import pandas as pd

# Technical logging (silent to console, file only)
logger = logging.getLogger("biorempp.input_processing.toxcsm_merge_processing")


def merge_input_with_toxcsm(
    input_data: pd.DataFrame, database_filepath: str = None, optimize_types: bool = True
) -> pd.DataFrame:
    """
    Merge input data with ToxCSM database based on 'cpd' column.

    This function performs an inner join between the input data and the ToxCSM
    database using the 'cpd' column as the merge key. The ToxCSM database
    contains toxicity predictions for chemical compounds.

    Parameters
    ----------
    input_data : pd.DataFrame
        Input DataFrame containing at least the 'cpd' column.
    database_filepath : str, optional
        Path to the ToxCSM database CSV file.
        Default: 'data/database_toxcsm.csv'
    optimize_types : bool, optional
        Whether to optimize DataFrame dtypes. Default: True

    Returns
    -------
    pd.DataFrame
        Merged DataFrame with ToxCSM annotations for matched compounds.

    Raises
    ------
    FileNotFoundError
        If the ToxCSM database file does not exist.
    ValueError
        If the file format is not CSV.
    KeyError
        If the 'cpd' column is missing in input or database.

    Examples
    --------
    >>> import pandas as pd
    >>> input_df = pd.DataFrame({'cpd': ['C00001', 'C00002']})
    >>> result = merge_input_with_toxcsm(input_df)
    >>> print(result.columns)
    """
    if database_filepath is None:
        database_filepath = os.path.join("data", "database_toxcsm.csv")
    logger.info(f"Using ToxCSM database file: {database_filepath}")

    # Check file existence
    if not os.path.exists(database_filepath):
        logger.error(f"ToxCSM database file not found: {database_filepath}")
        raise FileNotFoundError(f"ToxCSM database file not found: {database_filepath}")

    # Only .csv format accepted
    if not database_filepath.lower().endswith(".csv"):
        logger.error("Unsupported file format. Use .csv")
        raise ValueError("Unsupported file format. Use .csv")

    # Load ToxCSM database
    try:
        database_df = pd.read_csv(database_filepath, encoding="utf-8", sep=";")
        logger.info(
            "ToxCSM database loaded (%d rows, %d columns)",
            database_df.shape[0],
            database_df.shape[1],
        )
    except Exception:
        logger.exception("Error loading ToxCSM database CSV.")
        raise

    # Optimize types if requested
    if optimize_types:
        database_df = optimize_dtypes_toxcsm(database_df)
        input_data = optimize_dtypes_toxcsm(input_data.copy())
        logger.info("Types optimized with optimize_dtypes_toxcsm.")

    # Validate presence of 'cpd' column
    for df_name, df in {"input_data": input_data, "database_df": database_df}.items():
        if "cpd" not in df.columns:
            logger.error(f"Missing 'cpd' column in {df_name}.")
            raise KeyError(
                "Column 'cpd' must be present in both input and ToxCSM DataFrames."
            )

    # Handle potential column conflicts before merge
    # Check for overlapping columns (excluding merge key)
    input_cols = set(input_data.columns)
    db_cols = set(database_df.columns)
    overlap_cols = input_cols.intersection(db_cols) - {"cpd"}

    if overlap_cols:
        logger.info(f"Found overlapping columns: {overlap_cols}")
        # For overlapping columns, prioritize input data and drop from database
        # except for ToxCSM-specific columns which should be kept
        toxcsm_specific_cols = {"SMILES", "ChEBI"} | {
            col for col in database_df.columns if col.startswith(("value_", "label_"))
        }

        cols_to_drop = overlap_cols - toxcsm_specific_cols
        if cols_to_drop:
            logger.info(f"Dropping overlapping columns from database: {cols_to_drop}")
            database_df = database_df.drop(columns=list(cols_to_drop))

    # Perform merge on 'cpd' column
    merged_df = pd.merge(input_data, database_df, on="cpd", how="inner")

    if optimize_types:
        merged_df = optimize_dtypes_toxcsm(merged_df)

    logger.info(f"ToxCSM merge completed. Final shape: {merged_df.shape}")
    return merged_df


def optimize_dtypes_toxcsm(df: pd.DataFrame) -> pd.DataFrame:
    """
    Optimize ToxCSM DataFrame dtypes for memory efficiency.

    Converts repetitive columns to categorical and numeric columns to float32.
    This function handles the specific column patterns found in ToxCSM data.

    Parameters
    ----------
    df : pd.DataFrame
        Input ToxCSM DataFrame.

    Returns
    -------
    pd.DataFrame
        DataFrame with optimized dtypes.

    Raises
    ------
    TypeError
        If input is not a pandas DataFrame.
    """
    if not isinstance(df, pd.DataFrame):
        logger.error("Input must be a pandas DataFrame.")
        raise TypeError("Input must be a pandas DataFrame.")

    # Categorical columns commonly found in ToxCSM data
    categorical_columns = [
        "SMILES",
        "cpd",
        "ChEBI",
        "compoundname",
        "sample",
        "ko",
        "genesymbol",
        "genename",
        "compoundclass",
        "referenceAG",
        "enzyme_activity",
    ]

    for col in categorical_columns:
        if col in df.columns:
            logger.debug(f"Converting column '{col}' to categorical.")
            df[col] = df[col].astype("category")

    # Handle label_* columns (toxicity labels)
    label_columns = [col for col in df.columns if col.startswith("label_")]
    for col in label_columns:
        logger.debug(f"Converting label column '{col}' to categorical.")
        df[col] = df[col].astype("category")

    # Handle value_* columns (numeric toxicity values)
    value_columns = [col for col in df.columns if col.startswith("value_")]
    for col in value_columns:
        try:
            logger.debug(f"Converting value column '{col}' to float32.")
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("float32")
        except Exception as e:
            logger.warning(f"Failed to convert column '{col}' to float32: {e}")

    logger.info("ToxCSM DataFrame dtype optimization completed.")
    return df
