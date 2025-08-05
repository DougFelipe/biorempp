"""
I/O Utilities for BioRemPP

General functions for saving outputs to disk.
"""

import os
from datetime import datetime

from biorempp.utils.logging_config import get_logger

logger = get_logger("utils.io_utils")


def generate_timestamped_filename(filename, add_timestamp=False):
    """
    Generate a filename with timestamp if requested.

    Parameters
    ----------
    filename : str
        Original filename.
    add_timestamp : bool
        Whether to add timestamp to filename.

    Returns
    -------
    str
        Filename with or without timestamp.

    Examples
    --------
    >>> generate_timestamped_filename("results.txt", True)
    'results_20250707_194530.txt'
    >>> generate_timestamped_filename("results.txt", False)
    'results.txt'
    """
    if not add_timestamp:
        return filename

    # Split filename and extension
    name, ext = os.path.splitext(filename)

    # Generate timestamp (YYYYMMDD_HHMMSS)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Return timestamped filename
    return f"{name}_{timestamp}{ext}"


def save_dataframe_output(
    df,
    output_dir,
    filename,
    sep=";",
    index=False,
    encoding="utf-8",
    add_timestamp=False,
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
    add_timestamp : bool
        Whether to add timestamp to filename (default: False).

    Returns
    -------
    str
        Path to the saved file.
    """
    # Generate timestamped filename if requested
    final_filename = generate_timestamped_filename(filename, add_timestamp)

    logger.debug(f"Saving DataFrame to: {output_dir}/{final_filename}")
    logger.debug(f"DataFrame shape: {df.shape}")

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, final_filename)

    try:
        df.to_csv(output_path, sep=sep, index=index, encoding=encoding)
        logger.info(f"DataFrame successfully saved to: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Failed to save DataFrame to {output_path}: {e}")
        raise
