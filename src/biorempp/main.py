import argparse
import sys

from biorempp.pipelines.input_processing import (
    run_all_processing_pipelines,
    run_biorempp_processing_pipeline,
    run_hadeg_processing_pipeline,
    run_kegg_processing_pipeline,
    run_toxcsm_processing_pipeline,
)
from biorempp.utils.logging_config import get_logger, setup_logging

# Initialize centralized logging
setup_logging(level="INFO", console_output=True)
logger = get_logger("main")


def get_pipeline_function(pipeline_type):
    """
    Return the appropriate pipeline function based on the pipeline type.

    This function acts as a dispatcher/router for different pipeline types,
    making it easy to add new pipeline types in the future.

    Parameters
    ----------
    pipeline_type : str
        The type of pipeline to run ('all', 'biorempp', 'kegg', 'hadeg', or 'toxcsm')

    Returns
    -------
    callable
        The pipeline function to execute

    Raises
    ------
    ValueError
        If pipeline_type is not supported
    """
    pipeline_map = {
        "all": run_all_processing_pipelines,
        "biorempp": run_biorempp_processing_pipeline,
        "kegg": run_kegg_processing_pipeline,
        "hadeg": run_hadeg_processing_pipeline,
        "toxcsm": run_toxcsm_processing_pipeline,
    }

    if pipeline_type not in pipeline_map:
        available_types = ", ".join(pipeline_map.keys())
        raise ValueError(
            f"Unsupported pipeline type: {pipeline_type}. "
            f"Available types: {available_types}"
        )

    return pipeline_map[pipeline_type]


def run_pipeline(pipeline_type, args):
    """
    Execute the specified pipeline with the given arguments.

    Parameters
    ----------
    pipeline_type : str
        The type of pipeline to run
    args : argparse.Namespace
        Parsed command line arguments

    Returns
    -------
    str or dict
        Path to the output file (for single pipelines) or dictionary with
        paths (for 'all' pipeline)
    """
    pipeline_function = get_pipeline_function(pipeline_type)

    # Common parameters for all pipelines
    common_params = {
        "input_path": args.input,
        "output_dir": args.output_dir,
        "sep": args.sep,
        "optimize_types": True,
        "add_timestamp": args.add_timestamp and not args.no_timestamp,
    }

    # Add pipeline-specific parameters
    if pipeline_type == "biorempp":
        common_params["database_path"] = args.database
        common_params["output_filename"] = (
            args.output_filename or "BioRemPP_Results.txt"
        )
    elif pipeline_type == "kegg":
        common_params["kegg_database_path"] = args.database
        common_params["output_filename"] = args.output_filename or "KEGG_Results.txt"
    elif pipeline_type == "hadeg":
        common_params["hadeg_database_path"] = args.database
        common_params["output_filename"] = args.output_filename or "HADEG_Results.txt"
    elif pipeline_type == "toxcsm":
        common_params["toxcsm_database_path"] = args.database
        common_params["output_filename"] = args.output_filename or "ToxCSM.txt"
    elif pipeline_type == "all":
        common_params["biorempp_database_path"] = args.biorempp_database
        common_params["kegg_database_path"] = args.kegg_database
        common_params["hadeg_database_path"] = args.hadeg_database
        common_params["toxcsm_database_path"] = args.toxcsm_database
        common_params["biorempp_output_filename"] = args.biorempp_output_filename
        common_params["kegg_output_filename"] = args.kegg_output_filename
        common_params["hadeg_output_filename"] = args.hadeg_output_filename
        common_params["toxcsm_output_filename"] = args.toxcsm_output_filename

    logger.info(f"Running {pipeline_type} pipeline")
    logger.debug(f"Pipeline parameters: {common_params}")

    return pipeline_function(**common_params)


def main():
    parser = argparse.ArgumentParser(
        description="BioRemPP - Input validation and database merging pipeline."
    )
    parser.add_argument(
        "--input", required=True, help="Path to the FASTA-like input file (.txt)"
    )
    parser.add_argument(
        "--pipeline-type",
        choices=["all", "biorempp", "kegg", "hadeg", "toxcsm"],
        default="all",
        help="Type of pipeline to run (default: all - runs all pipelines)",
    )
    parser.add_argument(
        "--database",
        default=None,
        help="Path to database CSV file for single pipeline modes "
        "(default: auto-resolve based on pipeline type)",
    )
    parser.add_argument(
        "--biorempp-database",
        default=None,
        help="Path to BioRemPP database CSV file for 'all' mode "
        "(default: auto-resolve)",
    )
    parser.add_argument(
        "--kegg-database",
        default=None,
        help="Path to KEGG degradation pathways CSV file for 'all' mode "
        "(default: auto-resolve)",
    )
    parser.add_argument(
        "--hadeg-database",
        default=None,
        help="Path to HADEG database CSV file for 'all' mode "
        "(default: auto-resolve)",
    )
    parser.add_argument(
        "--toxcsm-database",
        default=None,
        help="Path to ToxCSM database CSV file for 'all' mode "
        "(default: auto-resolve)",
    )
    parser.add_argument(
        "--output-dir",
        default="outputs/results_table",
        help="Directory to save results (default: outputs/results_table/)",
    )
    parser.add_argument(
        "--output-filename",
        default=None,
        help="Filename for single pipeline output "
        "(auto-resolved by pipeline type if not provided)",
    )
    parser.add_argument(
        "--biorempp-output-filename",
        default="BioRemPP_Results.txt",
        help="Filename for BioRemPP output in 'all' mode "
        "(default: BioRemPP_Results.txt)",
    )
    parser.add_argument(
        "--kegg-output-filename",
        default="KEGG_Results.txt",
        help="Filename for KEGG output in 'all' mode (default: KEGG_Results.txt)",
    )
    parser.add_argument(
        "--hadeg-output-filename",
        default="HADEG_Results.txt",
        help="Filename for HADEG output in 'all' mode (default: HADEG_Results.txt)",
    )
    parser.add_argument(
        "--toxcsm-output-filename",
        default="ToxCSM.txt",
        help="Filename for ToxCSM output in 'all' mode (default: ToxCSM.txt)",
    )
    parser.add_argument(
        "--sep",
        default=";",
        help="Separator for the output file (default: ';')",
    )
    parser.add_argument(
        "--add-timestamp",
        action="store_true",
        default=True,
        help="Add timestamp to output filenames (default: True)",
    )
    parser.add_argument(
        "--no-timestamp",
        action="store_true",
        help="Disable timestamp in output filenames",
    )

    args = parser.parse_args()

    try:
        logger.info("Starting BioRemPP processing pipeline")
        logger.debug(f"Input parameters: {vars(args)}")

        output_path = run_pipeline(args.pipeline_type, args)

        if isinstance(output_path, dict):
            # Multiple outputs from 'all' pipeline
            logger.info("All pipelines completed successfully")
            print("[BioRemPP] All processing pipelines completed successfully:")
            for pipeline_name, path in output_path.items():
                logger.info(f"{pipeline_name.upper()} output saved to: {path}")
                print(f"  [{pipeline_name.upper()}] Output: {path}")
        else:
            # Single output from individual pipeline
            logger.info(
                f"Pipeline completed successfully. Output saved to: {output_path}"
            )
            print(f"[BioRemPP] Output processed and saved to: {output_path}")
    except Exception as e:
        logger.error(f"Pipeline failed with error: {e}", exc_info=True)
        print(f"[BioRemPP] Pipeline error: {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()
