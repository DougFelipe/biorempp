import logging
import os

import pandas as pd

# Technical logging (silent to console, file only)
logger = logging.getLogger("biorempp.input_processing.biorempp_merge_processing")


def merge_input_with_biorempp(
    input_data: pd.DataFrame, database_filepath: str = None, optimize_types: bool = True
) -> pd.DataFrame:
    """
    Merge input data with BioRemPP reference database in CSV format.

    Parameters
    ----------
    input_data : pd.DataFrame
        Input DataFrame containing at least the 'ko' column.
    database_filepath : str, optional
        Path to database file (.csv). Default: 'data/database.csv'
    optimize_types : bool, optional
        Optimize types with optimize_dtypes_biorempp. Default: True

    Returns
    -------
    pd.DataFrame
        DataFrame with merge by 'ko' field, ready for analysis.

    Raises
    ------
    FileNotFoundError
        If database file does not exist.
    ValueError
        If file is not .csv format.
    KeyError
        If 'ko' column is missing in input or database.
    """
    if database_filepath is None:
        database_filepath = os.path.join("data", "database.csv")
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
    Optimize column types for recurring project columns (convert to categorical).

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.

    Returns
    -------
    pd.DataFrame
        DataFrame with optimized types.
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
