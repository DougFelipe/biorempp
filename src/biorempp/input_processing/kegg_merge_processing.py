import os

import pandas as pd

from biorempp.utils.logging_config import get_logger

logger = get_logger("input_processing.kegg_merge_processing")


def merge_input_with_kegg(
    input_data: pd.DataFrame, kegg_filepath: str = None, optimize_types: bool = True
) -> pd.DataFrame:
    """
    Merge input data with KEGG degradation pathway information from a CSV file.

    Parameters
    ----------
    input_data : pd.DataFrame
        DataFrame containing at least a 'ko' column.
    kegg_filepath : str, optional
        Path to the KEGG degradation pathways CSV file.
        Defaults to 'data/kegg_degradation_pathways.csv'.
    optimize_types : bool, optional
        If True, optimize dtypes using categorical columns.

    Returns
    -------
    pd.DataFrame
        DataFrame merged on the 'ko' column with optimized dtypes.

    Raises
    ------
    FileNotFoundError
        If the KEGG file does not exist.
    ValueError
        If the file extension is not .csv.
    KeyError
        If the 'ko' column is missing in either input.
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
    Optimize column types for KEGG degradation pathways data (converts to categorical).

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
