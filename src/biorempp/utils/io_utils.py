"""
I/O Utilities for BioRemPP

General functions for saving outputs to disk.
"""

import os

from biorempp.utils.logging_config import get_logger

logger = get_logger("utils.io_utils")


def save_dataframe_output(
    df,
    output_dir,
    filename,
    sep=";",
    index=False,
    encoding="utf-8",
):
    """
    Save a DataFrame to a txt/csv file in the given directory.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to save.
    output_dir : str
        Directory to save the file (created if it doesn't exist).
    filename : str
        Name of the output file.
    sep : str
        Separator for the output file (default: ';').
    index : bool
        Whether to write row indices (default: False).
    encoding : str
        File encoding (default: 'utf-8').

    Returns
    -------
    str
        Path to the saved file.
    """
    logger.debug(f"Saving DataFrame to: {output_dir}/{filename}")
    logger.debug(f"DataFrame shape: {df.shape}")

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)

    try:
        df.to_csv(output_path, sep=sep, index=index, encoding=encoding)
        logger.info(f"DataFrame successfully saved to: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Failed to save DataFrame to {output_path}: {e}")
        raise
