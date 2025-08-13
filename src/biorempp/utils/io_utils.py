"""
BioRemPP I/O Utilities Module.

This module provides comprehensive file input/output operations and path
management utilities. It implements file handling patterns with
standardized output formats, project-relative path resolution, and
timestamped file generation for organized result management.

Key Features
-----------
- Current working directory path resolution for command execution context
- Project-relative path resolution for consistency when needed
- Timestamped file generation for chronological result tracking
- DataFrame export with standardized formatting and encoding
- Robust error handling for file system operations
- Cross-platform path management with proper encoding support

Technical Implementation
-----------------------
- UTF-8 encoding for international character support
- Thread-safe operations for concurrent processing environments
- Efficient file I/O with proper resource management
- Comprehensive error handling with informative messages
- Cross-platform path operations using pathlib

File Management Capabilities
---------------------------
The module handles various file operations:
- Output directory creation with proper permissions
- Timestamped filename generation for result organization
- DataFrame serialization with consistent formatting
- Path resolution relative to project structure
- Error-resilient file operations with detailed logging

Output Organization
------------------
Implements flexible output directory structure:
- outputs/results_tables/: Main results and analysis outputs
- Timestamped files: Chronological organization of processing results
- Current working directory paths: Output files in execution context (default)
- Standardized formats: CSV with UTF-8 encoding and consistent separators

Path Resolution Strategy
-----------------------
The module implements current working directory path resolution:
1. Current working directory (default): Output files where command is executed
2. Relative path construction: Consistent paths from current directory
3. Cross-platform compatibility: Proper handling of Windows/Unix path formats

Example Usage
------------
    from biorempp.utils.io_utils import (
        save_dataframe_output,
        get_project_root,
        resolve_output_path,
        generate_timestamped_filename
    )

    # Save analysis results
    output_path = save_dataframe_output(
        dataframe=results_df,
        base_filename="analysis_results",
        subdirectory="pathway_analysis"
    )

    # Generate timestamped files
    filename = generate_timestamped_filename("experiment", "csv")

    # Resolve project-relative paths
    project_root = get_project_root()
    output_dir = resolve_output_path("custom_results")
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
    Resolve output directory path relative to current working directory.

    This function creates outputs in the current working directory where
    the command is executed, providing intuitive behavior for users.

    Parameters
    ----------
    output_dir : str
        Output directory path (e.g., "outputs/results_tables")

    Returns
    -------
    str
        Absolute path to the output directory
    """
    # If output_dir is already absolute, use it as-is
    if os.path.isabs(output_dir):
        return output_dir

    # Resolve relative to current working directory
    resolved_path = os.path.join(os.getcwd(), output_dir)
    logger.debug(f"Resolved output path (CWD): {output_dir} -> {resolved_path}")

    return resolved_path


def resolve_log_path(log_path: str) -> str:
    """
    Resolve log file path relative to project root.

    This ensures that log files are created in the correct location
    (project_root/outputs/logs/) regardless of the current working directory.

    Parameters
    ----------
    log_path : str
        Log file path (e.g., "outputs/logs/biorempp.log")

    Returns
    -------
    str
        Absolute path to the log file
    """
    project_root = get_project_root()

    # If log_path is already absolute, use it as-is
    if os.path.isabs(log_path):
        return log_path

    # Resolve relative to project root
    resolved_path = os.path.join(project_root, log_path)
    logger.debug(f"Resolved log path: {log_path} -> {resolved_path}")
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
        Will be resolved relative to current working directory.
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

    # Resolve output directory relative to current working directory
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
