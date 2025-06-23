import argparse
import os
import sys

# Ensure 'src' is in sys.path for local development
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(THIS_DIR, ".."))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from biorempp.input_processing.input_loader import load_and_merge_input  # noqa: E402

# ... resto do main.py ...


def main():
    parser = argparse.ArgumentParser(
        description="BioRemPP - Input validation and database merging pipeline."
    )
    parser.add_argument(
        "--input", required=True, help="Path to the FASTA-like input file (.txt)"
    )
    parser.add_argument(
        "--database",
        default=None,  # <---- ALTERADO para None por padrão!
        help="Path to the BioRemPP database CSV file (default: auto-resolve)",
    )
    parser.add_argument(
        "--preview-rows",
        type=int,
        default=5,
        help="Number of DataFrame rows to preview (default: 5)",
    )

    args = parser.parse_args()

    # Resolva automaticamente o caminho do banco SE não for passado via --database
    if args.database is None:
        args.database = os.path.join(THIS_DIR, "data", "database_biorempp.csv")

    # Read input file
    if not os.path.exists(args.input):
        print(f"Input file not found: {args.input}")
        sys.exit(1)
    with open(args.input, "r", encoding="utf-8") as f:
        input_content = f.read()

    # Run the pipeline
    df, error = load_and_merge_input(
        input_content,
        os.path.basename(args.input),
        database_filepath=args.database,
        optimize_types=True,
    )

    if error:
        print(f"[BioRemPP] Pipeline error: {error}")
        sys.exit(2)
    else:
        print("[BioRemPP] Merged DataFrame preview:")
        print(df.head(args.preview_rows))
        print(f"[BioRemPP] DataFrame shape: {df.shape}")


if __name__ == "__main__":
    main()
