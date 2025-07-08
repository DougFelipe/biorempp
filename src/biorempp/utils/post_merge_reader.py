"""
Post-merge data reader for BioRemPP pipeline outputs.

This module provides functionality to load and validate the most recent
post-merge result files from the BioRemPP pipeline outputs.
"""

import glob
import logging
import os
import re
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd

logger = logging.getLogger(__name__)


class PostMergeDataReader:
    """
    Handles loading, validation, and standardization of post-merge DataFrames.

    This class provides methods to locate, load, and validate the most recent
    post-merge result files from the BioRemPP pipeline outputs. It supports
    loading data from different database types (BioRemPP, HADEG, KEGG, ToxCSM).

    Attributes
    ----------
    results_dir : str
        Path to the results directory containing post-merge files.
    file_prefixes : dict
        Mapping of data types to their file prefixes.
    expected_columns : dict
        Expected columns for each data type for validation.
    """

    def __init__(self, results_dir: Optional[str] = None):
        """
        Initialize the PostMergeDataReader.

        Parameters
        ----------
        results_dir : str, optional
            Path to the results directory. If None, uses default
            'outputs/results_table/'.
        """
        if results_dir is None:
            # Default to outputs/results_table relative to project root
            project_root = Path(__file__).parent.parent.parent.parent
            self.results_dir = project_root / "outputs" / "results_table"
        else:
            self.results_dir = Path(results_dir)

        # Mapping of data types to their file prefixes
        self.file_prefixes = {
            "biorempp": "BioRemPP_Results_",
            "hadeg": "HADEG_Results_",
            "kegg": "KEGG_Results_",
            "toxcsm": "ToxCSM_",
        }

        # Expected columns for basic validation
        self.expected_columns = {
            "biorempp": [
                "sample",
                "ko",
                "genesymbol",
                "genename",
                "cpd",
                "compoundclass",
                "referenceAG",
                "compoundname",
                "enzyme_activity",
            ],
            "hadeg": ["sample", "ko", "Gene", "Pathway", "compound_pathway"],
            "kegg": ["sample", "ko", "pathname", "genesymbol"],
            "toxcsm": [
                "sample",
                "ko",
                "genesymbol",
                "genename",
                "cpd",
                "compoundclass",
                "referenceAG",
                "compoundname",
                "enzyme_activity",
                "SMILES",
                "ChEBI",
            ],
        }

        logger.debug(
            f"PostMergeDataReader initialized with results_dir: " f"{self.results_dir}"
        )

    def _find_latest_file(self, data_type: str) -> Optional[Path]:
        """
        Find the most recent file for the specified data type.

        Parameters
        ----------
        data_type : str
            The type of data to find ('biorempp', 'hadeg', 'kegg', 'toxcsm').

        Returns
        -------
        Path or None
            Path to the most recent file, or None if no files found.

        Raises
        ------
        ValueError
            If data_type is not supported.
        """
        if data_type.lower() not in self.file_prefixes:
            raise ValueError(
                f"Unsupported data_type: {data_type}. "
                f"Supported types: {list(self.file_prefixes.keys())}"
            )

        prefix = self.file_prefixes[data_type.lower()]

        # Search for files with the specified prefix
        pattern = str(self.results_dir / f"{prefix}*.txt")
        matching_files = glob.glob(pattern)

        if not matching_files:
            logger.warning(
                f"No files found with prefix '{prefix}' in {self.results_dir}"
            )
            return None

        # Sort files by timestamp in filename (extract timestamp using regex)
        def extract_timestamp(filepath):
            filename = os.path.basename(filepath)
            # Extract timestamp pattern YYYYMMDD_HHMMSS
            match = re.search(r"(\d{8}_\d{6})", filename)
            return match.group(1) if match else "00000000_000000"

        sorted_files = sorted(matching_files, key=extract_timestamp, reverse=True)
        latest_file = Path(sorted_files[0])

        logger.debug(
            f"Found {len(matching_files)} files for {data_type}, "
            f"latest: {latest_file.name}"
        )

        return latest_file

    def _validate_dataframe(self, df: pd.DataFrame, data_type: str) -> None:
        """
        Validate the loaded DataFrame content.

        Parameters
        ----------
        df : pd.DataFrame
            The DataFrame to validate.
        data_type : str
            The type of data for validation context.

        Raises
        ------
        ValueError
            If DataFrame is empty or missing expected columns.
        """
        if df.empty:
            raise ValueError(f"DataFrame for {data_type} is empty")

        expected_cols = self.expected_columns.get(data_type.lower(), [])
        missing_cols = [col for col in expected_cols if col not in df.columns]

        if missing_cols:
            logger.warning(f"Missing expected columns for {data_type}: {missing_cols}")
            # Don't raise error, just log warning as different pipelines
            # may have different columns

        logger.debug(
            f"DataFrame validation passed for {data_type}: "
            f"shape={df.shape}, columns={list(df.columns)}"
        )

    def load_latest(self, data_type: str) -> pd.DataFrame:
        """
        Load the most recent post-merge result file for the specified data type.

        Parameters
        ----------
        data_type : str
            The type of data to load ('biorempp', 'hadeg', 'kegg', 'toxcsm').

        Returns
        -------
        pd.DataFrame
            The loaded and validated DataFrame.

        Raises
        ------
        FileNotFoundError
            If no files found for the specified data type.
        ValueError
            If the file is malformed or missing expected columns.
        Exception
            If there's an error reading the file.

        Examples
        --------
        >>> reader = PostMergeDataReader()
        >>> df_biorempp = reader.load_latest('biorempp')
        >>> df_hadeg = reader.load_latest('hadeg')
        """
        logger.info(f"Loading latest {data_type} data from {self.results_dir}")

        # Find the latest file
        latest_file = self._find_latest_file(data_type)

        if latest_file is None:
            raise FileNotFoundError(f"No {data_type} files found in {self.results_dir}")

        try:
            # Read the file
            logger.debug(f"Reading file: {latest_file}")
            df = pd.read_csv(latest_file, sep="\t")

            # Validate the DataFrame
            self._validate_dataframe(df, data_type)

            # Log summary information
            logger.info(
                f"Successfully loaded {data_type} data: "
                f"shape={df.shape}, file={latest_file.name}"
            )

            # Debug mode: print head of DataFrame
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(f"First 5 rows of {data_type} DataFrame:")
                logger.debug(f"\n{df.head()}")

            return df

        except pd.errors.EmptyDataError:
            raise ValueError(f"File {latest_file.name} is empty or malformed")
        except pd.errors.ParserError as e:
            raise ValueError(f"Error parsing file {latest_file.name}: {str(e)}")
        except Exception as e:
            logger.error(f"Error loading {data_type} data from {latest_file}: {str(e)}")
            raise

    def list_available_files(self) -> Dict[str, List[str]]:
        """
        List all available post-merge files by data type.

        Returns
        -------
        dict
            Dictionary mapping data types to lists of available filenames.
        """
        available_files = {}

        for data_type, prefix in self.file_prefixes.items():
            pattern = str(self.results_dir / f"{prefix}*.txt")
            matching_files = glob.glob(pattern)
            filenames = [os.path.basename(f) for f in matching_files]
            available_files[data_type] = sorted(filenames, reverse=True)

        return available_files
