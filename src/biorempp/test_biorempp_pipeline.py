import os
import sys

from biorempp.input_processing.input_loader import load_and_merge_input

# Add 'src' directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
src_path = os.path.join(project_root, "src")
sys.path.insert(0, src_path)


SAMPLE_TXT_PATH = os.path.join(src_path, "biorempp", "data", "sample_data.txt")
BIOREMPP_DB_PATH = os.path.join(src_path, "biorempp", "data", "database_biorempp.csv")

with open(SAMPLE_TXT_PATH, "r", encoding="utf-8") as f:
    txt_contents = f.read()

df, error = load_and_merge_input(
    txt_contents,
    "sample_data.txt",
    database_filepath=BIOREMPP_DB_PATH,
    optimize_types=True,
)

if error:
    print(f"Pipeline error: {error}")
else:
    print("Merged DataFrame preview:")
    print(df.head())
    print(f"Shape: {df.shape}")
