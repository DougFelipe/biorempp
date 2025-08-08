"""
Input Processing Pipeline for BioRemPP

Pipeline to validate, process, and merge FASTA-like input with the BioRemPP
database. The merged result is saved using a generic output function.
"""

import os

from biorempp.input_processing.hadeg_merge_processing import merge_input_with_hadeg
from biorempp.input_processing.input_loader import load_and_merge_input
from biorempp.input_processing.kegg_merge_processing import merge_input_with_kegg
from biorempp.input_processing.toxcsm_merge_processing import merge_input_with_toxcsm
from biorempp.utils.io_utils import save_dataframe_output
from biorempp.utils.logging_config import get_logger

logger = get_logger("pipelines.input_processing")


def run_biorempp_processing_pipeline(
    input_path,
    database_path=None,
    output_dir="outputs/results_tables",
    output_filename="BioRemPP_Results.txt",
    sep=";",
    optimize_types=True,
    add_timestamp=False,
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
    add_timestamp : bool
        Whether to add timestamp to filename (default: True).

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
        database_path = os.path.normpath(
            os.path.join(this_dir, "..", "data", "database_biorempp.csv")
        )
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
        add_timestamp=add_timestamp,
    )

    logger.info(f"Pipeline completed successfully. Output saved to: {output_path}")

    # Return structured data for user feedback
    return {
        "output_path": output_path,
        "matches": len(df) if df is not None else 0,
        "filename": os.path.basename(output_path),
    }


def run_kegg_processing_pipeline(
    input_path,
    kegg_database_path=None,
    output_dir="outputs/results_tables",
    output_filename="KEGG_Results.txt",
    sep=";",
    optimize_types=True,
    add_timestamp=False,
):
    """
    Run the KEGG degradation pathway processing pipeline.

    This pipeline validates, processes, and merges FASTA-like input with the KEGG
    degradation pathways database. The merged result is saved as a txt file.

    Parameters
    ----------
    input_path : str
        Path to the input .txt file (FASTA-like format).
    kegg_database_path : str or None
        Path to the KEGG degradation pathways CSV file. If None, uses default path.
    output_dir : str
        Directory where the merged DataFrame will be saved.
    output_filename : str
        Name of the output file.
    sep : str
        Separator for output (default: ';').
    optimize_types : bool
        Whether to optimize DataFrame dtypes (default: True).
    add_timestamp : bool
        Whether to add timestamp to filename (default: True).

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
    from biorempp.input_processing.input_validator import validate_and_process_input

    logger.info(f"Starting KEGG processing pipeline for: {input_path}")
    logger.debug(
        f"Pipeline parameters - kegg_database: {kegg_database_path}, "
        f"output_dir: {output_dir}, optimize_types: {optimize_types}"
    )

    if not os.path.exists(input_path):
        error_msg = f"Input file not found: {input_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    if kegg_database_path is None:
        this_dir = os.path.dirname(os.path.abspath(__file__))
        kegg_database_path = os.path.normpath(
            os.path.join(this_dir, "..", "data", "kegg_degradation_pathways.csv")
        )
        logger.debug(f"Using default KEGG database path: {kegg_database_path}")
        logger.debug(f"Using default KEGG database path: {kegg_database_path}")

    logger.info(f"Reading input file: {input_path}")
    with open(input_path, "r", encoding="utf-8") as f:
        input_content = f.read()

    # Validate and process input
    logger.info("Validating and processing input data")
    df, error = validate_and_process_input(input_content, os.path.basename(input_path))

    if error:
        error_msg = f"KEGG pipeline validation error: {error}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)

    # Merge with KEGG database
    logger.info("Merging with KEGG degradation pathways")
    kegg_merged_df = merge_input_with_kegg(
        df, kegg_filepath=kegg_database_path, optimize_types=optimize_types
    )

    logger.info(f"Saving KEGG merged DataFrame to: {output_dir}/{output_filename}")
    output_path = save_dataframe_output(
        kegg_merged_df,
        output_dir=output_dir,
        filename=output_filename,
        sep=sep,
        add_timestamp=add_timestamp,
    )

    logger.info(f"KEGG pipeline completed successfully. Output saved to: {output_path}")

    # Return structured data for user feedback
    return {
        "output_path": output_path,
        "matches": len(kegg_merged_df) if kegg_merged_df is not None else 0,
        "filename": os.path.basename(output_path),
    }


def run_hadeg_processing_pipeline(
    input_path,
    hadeg_database_path=None,
    output_dir="outputs/results_tables",
    output_filename="HADEG_Results.txt",
    sep=";",
    optimize_types=True,
    add_timestamp=False,
):
    """
    Run the HADEG (Hydrocarbon Degradation Database) processing pipeline.

    This pipeline validates, processes, and merges FASTA-like input with the
    HADEG database. The merged result is saved as a txt file.

    Parameters
    ----------
    input_path : str
        Path to the input .txt file (FASTA-like format).
    hadeg_database_path : str or None
        Path to the HADEG database CSV file. If None, uses default path.
    output_dir : str
        Directory where the merged DataFrame will be saved.
    output_filename : str
        Name of the output file.
    sep : str
        Separator for output (default: ';').
    optimize_types : bool
        Whether to optimize DataFrame dtypes (default: True).
    add_timestamp : bool
        Whether to add timestamp to filename (default: True).

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
    logger.info(f"Starting HADEG processing pipeline for: {input_path}")
    logger.debug(
        f"Pipeline parameters - database: {hadeg_database_path}, "
        f"output_dir: {output_dir}, optimize_types: {optimize_types}"
    )

    if not os.path.exists(input_path):
        error_msg = f"Input file not found: {input_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    if hadeg_database_path is None:
        this_dir = os.path.dirname(os.path.abspath(__file__))
        hadeg_database_path = os.path.normpath(
            os.path.join(this_dir, "..", "data", "database_hadeg.csv")
        )
        logger.debug(f"Using default HADEG database path: {hadeg_database_path}")

    logger.info(f"Reading input file: {input_path}")
    with open(input_path, "r", encoding="utf-8") as f:
        input_content = f.read()

    logger.info("Loading and merging input data with HADEG database")
    df, error = load_and_merge_input(
        input_content,
        os.path.basename(input_path),
        database_filepath=hadeg_database_path,
        optimize_types=optimize_types,
        merge_function=merge_input_with_hadeg,
    )

    if error:
        error_msg = f"HADEG Pipeline error: {error}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)

    logger.info(f"Saving merged DataFrame to: {output_dir}/{output_filename}")
    output_path = save_dataframe_output(
        df,
        output_dir=output_dir,
        filename=output_filename,
        sep=sep,
        add_timestamp=add_timestamp,
    )

    logger.info(
        f"HADEG Pipeline completed successfully. Output saved to: {output_path}"
    )

    # Return structured data for user feedback
    return {
        "output_path": output_path,
        "matches": len(df) if df is not None else 0,
        "filename": os.path.basename(output_path),
    }


def run_toxcsm_processing_pipeline(
    input_path,
    toxcsm_database_path=None,
    output_dir="outputs/results_tables",
    output_filename="ToxCSM.txt",
    sep=";",
    optimize_types=True,
    add_timestamp=False,
):
    """
    Run the ToxCSM toxicity prediction processing pipeline.

    This pipeline validates, processes, and merges FASTA-like input with the
    ToxCSM database. The merged result is saved as a txt file.

    Parameters
    ----------
    input_path : str
        Path to the input .txt file (FASTA-like format).
    toxcsm_database_path : str or None
        Path to the ToxCSM database CSV file. If None, uses default path.
    output_dir : str
        Directory where the merged DataFrame will be saved.
    output_filename : str
        Name of the output file.
    sep : str
        Separator for output (default: ';').
    optimize_types : bool
        Whether to optimize DataFrame dtypes (default: True).
    add_timestamp : bool
        Whether to add timestamp to filename (default: True).

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
    logger.info(f"Starting ToxCSM processing pipeline for: {input_path}")
    logger.debug(
        f"Pipeline parameters - toxcsm_database: {toxcsm_database_path}, "
        f"output_dir: {output_dir}, optimize_types: {optimize_types}"
    )

    if not os.path.exists(input_path):
        error_msg = f"Input file not found: {input_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    if toxcsm_database_path is None:
        this_dir = os.path.dirname(os.path.abspath(__file__))
        toxcsm_database_path = os.path.normpath(
            os.path.join(this_dir, "..", "data", "database_toxcsm.csv")
        )
        logger.debug(f"Using default ToxCSM database path: {toxcsm_database_path}")

    logger.info(f"Reading input file: {input_path}")
    with open(input_path, "r", encoding="utf-8") as f:
        input_content = f.read()

    # Step 1: Process input through BioRemPP first to get 'cpd' column
    logger.info("Processing input data through BioRemPP pipeline")

    # Define BioRemPP database path for internal use
    biorempp_db_path = None
    if toxcsm_database_path:
        # Use the same directory structure
        biorempp_db_path = os.path.normpath(
            os.path.join(os.path.dirname(toxcsm_database_path), "database_biorempp.csv")
        )

    df_biorempp, error = load_and_merge_input(
        input_content,
        os.path.basename(input_path),
        optimize_types=optimize_types,
        database_filepath=biorempp_db_path,
    )

    if error:
        error_msg = f"BioRemPP processing error: {error}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)

    # Step 2: Merge BioRemPP result with ToxCSM database
    logger.info("Merging BioRemPP data with ToxCSM database")
    df = merge_input_with_toxcsm(
        df_biorempp,
        database_filepath=toxcsm_database_path,
        optimize_types=optimize_types,
    )

    logger.info(f"Saving merged DataFrame to: {output_dir}/{output_filename}")
    output_path = save_dataframe_output(
        df,
        output_dir=output_dir,
        filename=output_filename,
        sep=sep,
        add_timestamp=add_timestamp,
    )

    logger.info(
        f"ToxCSM Pipeline completed successfully. Output saved to: {output_path}"
    )

    # Return structured data for user feedback
    return {
        "output_path": output_path,
        "matches": len(df) if df is not None else 0,
        "filename": os.path.basename(output_path),
    }
