import argparse
import sys

from biorempp.pipelines.input_processing import run_input_processing_pipeline
from biorempp.utils.logging_config import get_logger, setup_logging

# Initialize centralized logging
setup_logging(level="INFO", console_output=True)
logger = get_logger("main")


def main():
    parser = argparse.ArgumentParser(
        description="BioRemPP - Input validation and database merging pipeline."
    )
    parser.add_argument(
        "--input", required=True, help="Path to the FASTA-like input file (.txt)"
    )
    parser.add_argument(
        "--database",
        default=None,
        help="Path to the BioRemPP database CSV file (default: auto-resolve)",
    )
    parser.add_argument(
        "--output-dir",
        default="outputs/merged_data",
        help="Directory to save merged result (default: outputs/merged_data/)",
    )
    parser.add_argument(
        "--output-filename",
        default="merged_input.txt",
        help="Filename for the merged DataFrame output (default: merged_input.txt)",
    )
    parser.add_argument(
        "--sep",
        default=";",
        help="Separator for the output file (default: ';')",
    )

    args = parser.parse_args()

    try:
        logger.info("Starting BioRemPP input processing pipeline")
        logger.debug(f"Input parameters: {vars(args)}")

        output_path = run_input_processing_pipeline(
            input_path=args.input,
            database_path=args.database,
            output_dir=args.output_dir,
            output_filename=args.output_filename,
            sep=args.sep,
        )

        logger.info(f"Pipeline completed successfully. Output saved to: {output_path}")
        print(f"[BioRemPP] Output processed and saved to: {output_path}")
    except Exception as e:
        logger.error(f"Pipeline failed with error: {e}", exc_info=True)
        print(f"[BioRemPP] Pipeline error: {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()
