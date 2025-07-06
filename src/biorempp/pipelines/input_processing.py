"""
Input Processing Pipeline for BioRemPP

Pipeline to validate, process, and merge FASTA-like input with the BioRemPP
database. The merged result is saved using a generic output function.
"""

import os

from biorempp.input_processing.input_loader import load_and_merge_input
from biorempp.utils.io_utils import save_dataframe_output
from biorempp.utils.logging_config import get_logger

logger = get_logger("pipelines.input_processing")


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
    logger.info(f"Starting input processing pipeline for: {input_path}")
    logger.debug(
        f"Pipeline parameters - database: {database_path}, "
        f"output_dir: {output_dir}, optimize_types: {optimize_types}"
    )

    if not os.path.exists(input_path):
        error_msg = f"Input file not found: {input_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    if database_path is None:
        this_dir = os.path.dirname(os.path.abspath(__file__))
        database_path = os.path.join(this_dir, "..", "data", "database_biorempp.csv")
        logger.debug(f"Using default database path: {database_path}")

    logger.info(f"Reading input file: {input_path}")
    with open(input_path, "r", encoding="utf-8") as f:
        input_content = f.read()

    logger.info("Loading and merging input data")
    df, error = load_and_merge_input(
        input_content,
        os.path.basename(input_path),
        database_filepath=database_path,
        optimize_types=optimize_types,
    )

    if error:
        error_msg = f"Pipeline error: {error}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)

    logger.info(f"Saving merged DataFrame to: {output_dir}/{output_filename}")
    output_path = save_dataframe_output(
        df,
        output_dir=output_dir,
        filename=output_filename,
        sep=sep,
    )

    logger.info(f"Pipeline completed successfully. Output saved to: {output_path}")
    return output_path
