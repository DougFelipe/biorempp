import argparse
import sys

from biorempp.pipelines.input_processing import run_input_processing_pipeline


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
        output_path = run_input_processing_pipeline(
            input_path=args.input,
            database_path=args.database,
            output_dir=args.output_dir,
            output_filename=args.output_filename,
            sep=args.sep,
        )
        print(f"[BioRemPP] Output processed and saved to: {output_path}")
    except Exception as e:
        print(f"[BioRemPP] Pipeline error: {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()
