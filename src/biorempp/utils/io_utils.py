"""
I/O Utilities for BioRemPP

General functions for saving outputs to disk.
"""

import os


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
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)
    df.to_csv(output_path, sep=sep, index=index, encoding=encoding)
    return output_path
