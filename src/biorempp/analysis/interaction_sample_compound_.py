"""
Sample compound interaction processor for BioRemPP.

This module provides functionality to extract unique compound classes from
processed biological data, supporting integration with the modular pipeline system.
"""

import os
from typing import List

import pandas as pd

from biorempp.analysis.base_processor import BaseDataProcessor
from biorempp.utils.io_utils import save_dataframe_output


class SampleCompoundInteraction(BaseDataProcessor):
    """
    Processor for extracting sample-compound interactions from processed data.

    This processor extracts unique sample-compound interactions from biological
    data, providing a tidy DataFrame with sample, compound name, and compound class
    information. Results are saved to the entities_interactions directory for
    downstream analysis.
    """

    def __init__(
        self,
        output_dir: str = "outputs/entities_interactions",
        output_file: str = "sample_compound_interaction.txt",
    ):
        """
        Initialize the sample compound interaction processor.

        Parameters
        ----------
        output_dir : str, optional
            Directory to save interaction results.
            Default: "outputs/entities_interactions"
        output_file : str, optional
            Name of the output file. Default: "sample_compound_interaction.txt"
        """
        super().__init__(
            name="sample_compound_interaction_processor",
            description=(
                "Extract sample-compound interactions from processed biological data"
            ),
        )
        self.output_dir = output_dir
        self.output_file = output_file
        self._ensure_output_directory()

    @property
    def required_columns(self) -> List[str]:
        """Return the list of required columns for this processor."""
        return ["sample", "compoundname", "compoundclass"]

    @property
    def output_columns(self) -> List[str]:
        """Return the list of columns in the output DataFrame."""
        return ["sample", "compoundname", "compoundclass"]

    def _ensure_output_directory(self) -> None:
        """Ensure the output directory exists."""
        from biorempp.utils.io_utils import resolve_output_path

        resolved_output_dir = resolve_output_path(self.output_dir)
        os.makedirs(resolved_output_dir, exist_ok=True)
        self.logger.debug(f"Output directory ensured: {resolved_output_dir}")
        # Update the output_dir to use the resolved path
        self.output_dir = resolved_output_dir

    def _validate_input_data(self, data: pd.DataFrame) -> bool:
        """
        Validate that input data contains required columns.

        Parameters
        ----------
        data : pd.DataFrame
            Input data to validate

        Returns
        -------
        bool
            True if data is valid, False otherwise
        """
        if data.empty:
            self.logger.warning("Input data is empty")
            return False

        required_cols = ["sample", "compoundname", "compoundclass"]
        missing_cols = [col for col in required_cols if col not in data.columns]

        if missing_cols:
            self.logger.error(
                f"Required columns {missing_cols} not found in input data. "
                f"Available columns: {list(data.columns)}"
            )
            return False

        return True

    def _extract_sample_compound_interactions(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Extract sample-compound interactions from the data.

        Parameters
        ----------
        data : pd.DataFrame
            Input DataFrame containing sample, compound name and class information

        Returns
        -------
        pd.DataFrame
            DataFrame with sample, compoundname, and compoundclass columns
        """
        self.logger.debug("Extracting sample-compound interactions from data")

        # Select only the required columns and remove duplicates
        interactions_df = data[
            ["sample", "compoundname", "compoundclass"]
        ].drop_duplicates()

        # Remove rows where any of the key columns are NaN
        interactions_df = interactions_df.dropna(
            subset=["sample", "compoundname", "compoundclass"]
        )

        # Sort by sample, then by compound name for consistent output
        interactions_df = interactions_df.sort_values(
            ["sample", "compoundname", "compoundclass"]
        ).reset_index(drop=True)

        self.logger.info(
            f"Found {len(interactions_df)} unique sample-compound interactions"
        )
        return interactions_df

    def _save_results_to_file(self, results_df: pd.DataFrame) -> None:
        """
        Save compound interaction results to the output file.

        Parameters
        ----------
        results_df : pd.DataFrame
            DataFrame with sample-compound interactions to save
        """
        self.logger.info(
            f"Saving {len(results_df)} sample-compound interactions to: "
            f"{self.output_file}"
        )

        try:
            # Use save_dataframe_output to save the file
            output_path = save_dataframe_output(
                df=results_df,
                output_dir=self.output_dir,
                filename=self.output_file,
                sep=";",  # Use semicolon separator
                index=False,
                add_timestamp=False,
            )
            self.logger.info(f"Successfully saved results to: {output_path}")
        except Exception as e:
            self.logger.error(f"Failed to save results to file: {e}")
            raise

    def extract_compound_classes(self, biorempp_data):
        """
        Extracts unique compound classes from processed data (list[dict] or DataFrame).

        Parameters
        ----------
        biorempp_data : list[dict] | pd.DataFrame

        Returns
        -------
        list
        """
        if isinstance(biorempp_data, pd.DataFrame):
            if biorempp_data.empty or "compoundclass" not in biorempp_data.columns:
                return []
            values = biorempp_data["compoundclass"].dropna().unique()
            return sorted(values)

        if not biorempp_data:
            return []

        df = pd.DataFrame(biorempp_data)
        if "compoundclass" not in df.columns:
            return []

        values = df["compoundclass"].dropna().unique()
        return sorted(values)

    def process(self, data: pd.DataFrame, save_file: bool = True) -> pd.DataFrame:
        """
        Process the data and extract sample-compound interactions.

        Parameters
        ----------
        data : pd.DataFrame
            Input DataFrame containing biological data
        save_file : bool, optional
            Whether to save results to file. Default: True

        Returns
        -------
        pd.DataFrame
            DataFrame with sample, compoundname, and compoundclass columns
        """
        self.logger.info("Starting sample compound interaction processing")

        # Validate input data
        if not self._validate_input_data(data):
            self.logger.warning("Invalid input data, returning empty DataFrame")
            return pd.DataFrame(columns=self.output_columns)

        # Extract sample-compound interactions
        results_df = self._extract_sample_compound_interactions(data)

        if results_df.empty:
            self.logger.warning("No sample-compound interactions found in data")
            return pd.DataFrame(columns=self.output_columns)

        # Save to file if requested
        if save_file:
            self._save_results_to_file(results_df)

        self.logger.info("Sample compound interaction processing completed")
        return results_df
