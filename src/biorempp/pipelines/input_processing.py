"""
Input Processing Pipeline for BioRemPP

Pipeline to validate, process, and merge FASTA-like input with the BioRemPP
database. The merged result is saved using a generic output function.
"""

import os

from biorempp.input_processing.input_loader import load_and_merge_input
from biorempp.utils.io_utils import save_dataframe_output


def run_input_processing_pipeline(
    input_path,
    database_path=None,
    output_dir="outputs/merged_data",
    output_filename="merged_input.txt",
    sep=";",
    optimize_types=True,
):
    """
    Run the input validation, merging, and save output as .txt.

    Parameters
    ----------
    input_path : str
        Path to the input .txt file (FASTA-like format).
    database_path : str or None
        Path to the BioRemPP database CSV file. If None, uses default path.
    output_dir : str
        Directory where the merged DataFrame will be saved.
    output_filename : str
        Name of the output file.
    sep : str
        Separator for output (default: ';').
    optimize_types : bool
        Whether to optimize DataFrame dtypes (default: True).

    Returns
    -------
    str
        Path to the saved output file.

    Raises
    ------
    FileNotFoundError
        If the input file does not exist.
    RuntimeError
        If there is an error in processing or merging.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if database_path is None:
        this_dir = os.path.dirname(os.path.abspath(__file__))
        database_path = os.path.join(this_dir, "..", "data", "database_biorempp.csv")

    with open(input_path, "r", encoding="utf-8") as f:
        input_content = f.read()

    df, error = load_and_merge_input(
        input_content,
        os.path.basename(input_path),
        database_filepath=database_path,
        optimize_types=optimize_types,
    )

    if error:
        raise RuntimeError(f"Pipeline error: {error}")

    output_path = save_dataframe_output(
        df,
        output_dir=output_dir,
        filename=output_filename,
        sep=sep,
    )
    return output_path
