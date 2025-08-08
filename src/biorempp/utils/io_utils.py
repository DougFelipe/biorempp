"""
I/O Utilities for BioRemPP

General functions for saving outputs to disk.
"""

import logging
import os
from datetime import datetime
from pathlib import Path

# Technical logging (silent to console, file only)
logger = logging.getLogger("biorempp.utils.io_utils")


def get_project_root() -> str:
    """
    Get the project root directory path.

    This function ensures outputs are always created relative to the project root,
    not the current working directory. This is crucial for maintaining consistent
    output paths regardless of where the commands are executed from.

    Returns
    -------
    str
        Absolute path to the project root directory
    """
    # Get the directory containing this file (utils)
    current_file = Path(__file__).resolve()

    # Navigate up to find project root (look for pyproject.toml or setup.py)
    current_dir = current_file.parent

    while current_dir != current_dir.parent:  # Not root directory
        pyproject_exists = (current_dir / "pyproject.toml").exists()
        setup_exists = (current_dir / "setup.py").exists()

        if pyproject_exists or setup_exists:
            logger.debug(f"Project root found: {current_dir}")
            return str(current_dir)
        current_dir = current_dir.parent

    # Fallback: assume project root is 3 levels up from utils
    # biorempp/src/biorempp/utils -> biorempp/
    fallback_root = current_file.parent.parent.parent.parent
    logger.warning(f"Using fallback project root: {fallback_root}")
    return str(fallback_root)


def resolve_output_path(output_dir: str) -> str:
    """
    Resolve output directory path relative to project root.

    This ensures that all outputs are created in the correct location
    (project_root/outputs/) regardless of the current working directory.

    Parameters
    ----------
    output_dir : str
        Output directory path (e.g., "outputs/results_tables")

    Returns
    -------
    str
        Absolute path to the output directory
    """
    project_root = get_project_root()

    # If output_dir is already absolute, use it as-is
    if os.path.isabs(output_dir):
        return output_dir

    # Resolve relative to project root
    resolved_path = os.path.join(project_root, output_dir)
    logger.debug(f"Resolved output path: {output_dir} -> {resolved_path}")
    return resolved_path


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
        Will be resolved relative to project root.
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

    # Resolve output directory relative to project root
    resolved_output_dir = resolve_output_path(output_dir)

    logger.debug(f"Saving DataFrame to: {resolved_output_dir}/{final_filename}")
    logger.debug(f"DataFrame shape: {df.shape}")

    os.makedirs(resolved_output_dir, exist_ok=True)
    output_path = os.path.join(resolved_output_dir, final_filename)

    try:
        df.to_csv(output_path, sep=sep, index=index, encoding=encoding)
        logger.info(f"DataFrame successfully saved to: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Failed to save DataFrame to {output_path}: {e}")
        raise
