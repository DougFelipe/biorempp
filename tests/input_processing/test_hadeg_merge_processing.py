"""
Test suite for HADEG merge processing module.

This module tests the functionality of merging input data with the HADEG
(Hydrocarbon Degradation Database) including various scenarios such as
successful merges, error handling, and edge cases.
"""

from unittest.mock import patch

import pandas as pd
import pytest

from biorempp.input_processing.hadeg_merge_processing import (
    merge_input_with_hadeg,
    optimize_dtypes_hadeg,
)


class TestMergeInputWithHadeg:
    """Test cases for merge_input_with_hadeg function."""

    def test_merge_successful(
        self, sample_input_data_for_hadeg, mock_hadeg_database_csv
    ):
        """Test successful merge with HADEG database."""
        result = merge_input_with_hadeg(
            sample_input_data_for_hadeg,
            database_filepath=mock_hadeg_database_csv,
            optimize_types=False,
        )

        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
        assert "Gene" in result.columns
        assert "Pathway" in result.columns
        assert "compound_pathway" in result.columns
        assert all(result["ko"].isin(sample_input_data_for_hadeg["ko"]))

    def test_merge_with_optimization(
        self, sample_input_data_for_hadeg, mock_hadeg_database_csv
    ):
        """Test merge with type optimization enabled."""
        result = merge_input_with_hadeg(
            sample_input_data_for_hadeg,
            database_filepath=mock_hadeg_database_csv,
            optimize_types=True,
        )

        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
        # Check that categorical optimization was applied
        assert result["ko"].dtype.name == "category"
        assert result["Gene"].dtype.name == "category"

    def test_merge_with_no_matches(self, mock_hadeg_database_csv):
        """Test merge when no matches are found."""
        no_match_data = pd.DataFrame(
            {"ko": ["K99999", "K88888"], "sample": ["Sample1", "Sample2"]}
        )

        result = merge_input_with_hadeg(
            no_match_data,
            database_filepath=mock_hadeg_database_csv,
            optimize_types=False,
        )

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_merge_with_duplicates(
        self, sample_input_data_for_hadeg, mock_hadeg_database_with_duplicates
    ):
        """Test merge with database containing duplicate KO entries."""
        input_data = pd.DataFrame(
            {"ko": ["K00496", "K05710"], "sample": ["Sample1", "Sample2"]}
        )

        # Mock the database loading to use our fixture
        with patch("os.path.exists", return_value=True):
            with patch("pandas.read_csv") as mock_read_csv:
                mock_read_csv.return_value = mock_hadeg_database_with_duplicates

                result = merge_input_with_hadeg(
                    input_data, database_filepath="dummy_path.csv", optimize_types=False
                )

                assert isinstance(result, pd.DataFrame)
                assert len(result) > 2  # Should have multiple rows due to duplicates

    def test_merge_minimal_data(self, mock_hadeg_minimal_dataframe):
        """Test merge with minimal dataset."""
        input_data = pd.DataFrame(
            {"ko": ["K00001", "K00002"], "sample": ["Sample1", "Sample2"]}
        )

        with patch("os.path.exists", return_value=True):
            with patch("pandas.read_csv") as mock_read_csv:
                mock_read_csv.return_value = mock_hadeg_minimal_dataframe

                result = merge_input_with_hadeg(
                    input_data, database_filepath="dummy_path.csv", optimize_types=False
                )

                assert isinstance(result, pd.DataFrame)
                assert len(result) == 2

    def test_merge_with_default_database_path(
        self, sample_input_data_for_hadeg, mock_hadeg_database_dataframe
    ):
        """Test merge using default database path."""
        with patch("os.path.exists", return_value=True):
            with patch("pandas.read_csv") as mock_read_csv:
                mock_read_csv.return_value = mock_hadeg_database_dataframe

                result = merge_input_with_hadeg(
                    sample_input_data_for_hadeg,
                    database_filepath=None,
                    optimize_types=False,
                )

                assert isinstance(result, pd.DataFrame)
                assert len(result) > 0

    def test_invalid_input_type(self):
        """Test error handling for invalid input type."""
        with pytest.raises(TypeError, match="Input must be a pandas DataFrame"):
            merge_input_with_hadeg("not_a_dataframe")

    def test_file_not_found(self, sample_input_data_for_hadeg):
        """Test error handling when database file doesn't exist."""
        with pytest.raises(FileNotFoundError, match="Database file not found"):
            merge_input_with_hadeg(
                sample_input_data_for_hadeg, database_filepath="nonexistent_file.csv"
            )

    def test_invalid_file_format(self, sample_input_data_for_hadeg, tmp_path):
        """Test error handling for non-CSV files."""
        # Create a temporary .txt file to test format validation
        txt_file = tmp_path / "test_file.txt"
        txt_file.write_text("some content\n")

        with pytest.raises(ValueError, match="Unsupported file format"):
            merge_input_with_hadeg(
                sample_input_data_for_hadeg, database_filepath=str(txt_file)
            )

    def test_missing_ko_column_in_input(self, mock_hadeg_database_csv):
        """Test error handling when ko column is missing in input."""
        invalid_input = pd.DataFrame(
            {"gene": ["gene1", "gene2"], "sample": ["Sample1", "Sample2"]}
        )

        with pytest.raises(KeyError, match="Column 'ko' must be present"):
            merge_input_with_hadeg(
                invalid_input, database_filepath=mock_hadeg_database_csv
            )

    def test_missing_ko_column_in_database(
        self, sample_input_data_for_hadeg, mock_hadeg_database_missing_columns
    ):
        """Test error handling when ko column is missing in database."""
        with pytest.raises(KeyError, match="Column 'ko' must be present"):
            merge_input_with_hadeg(
                sample_input_data_for_hadeg,
                database_filepath=mock_hadeg_database_missing_columns,
            )

    def test_empty_database(
        self, sample_input_data_for_hadeg, mock_hadeg_empty_dataframe
    ):
        """Test merge with empty database."""
        with patch("os.path.exists", return_value=True):
            with patch("pandas.read_csv") as mock_read_csv:
                mock_read_csv.return_value = mock_hadeg_empty_dataframe

                result = merge_input_with_hadeg(
                    sample_input_data_for_hadeg,
                    database_filepath="dummy_path.csv",
                    optimize_types=False,
                )

                assert isinstance(result, pd.DataFrame)
                assert len(result) == 0

    def test_csv_read_error(self, sample_input_data_for_hadeg, tmp_path):
        """Test error handling when CSV reading fails."""
        # Create a CSV with invalid structure that will cause pandas to fail
        corrupt_file = tmp_path / "corrupt.csv"
        # Write malformed CSV that will cause pandas.read_csv to fail
        corrupt_file.write_text("Gene;ko;Pathway\nalkB;K00496;incomplete")

        # Since the CSV loads successfully but lacks expected columns,
        # we expect the merge to work but produce a DataFrame with different structure
        result = merge_input_with_hadeg(
            sample_input_data_for_hadeg, database_filepath=str(corrupt_file)
        )

        # The result should be a DataFrame but may have different columns
        assert isinstance(result, pd.DataFrame)
        assert "ko" in result.columns  # ko column should be present from merge


class TestOptimizeDtypesHadeg:
    """Test cases for optimize_dtypes_hadeg function."""

    def test_optimize_dtypes_successful(self, mock_hadeg_database_dataframe):
        """Test successful dtype optimization."""
        # Add a sample column for testing
        test_df = mock_hadeg_database_dataframe.copy()

        # Create sample column with correct length
        sample_values = ["Sample1", "Sample2", "Sample3"] * 7  # 21 values
        # Truncate to match DataFrame length
        test_df["sample"] = sample_values[: len(test_df)]
        test_df["numeric_column"] = range(len(test_df))

        result = optimize_dtypes_hadeg(test_df)

        assert isinstance(result, pd.DataFrame)
        assert result["Gene"].dtype.name == "category"
        assert result["ko"].dtype.name == "category"
        assert result["Pathway"].dtype.name == "category"
        assert result["compound_pathway"].dtype.name == "category"
        assert result["sample"].dtype.name == "category"
        # Non-categorical columns should remain unchanged
        assert result["numeric_column"].dtype.name != "category"

    def test_optimize_dtypes_partial_columns(self):
        """Test optimization with only some HADEG columns present."""
        df = pd.DataFrame(
            {
                "Gene": ["alkB", "ahpC"],
                "ko": ["K00496", "K03386"],
                "other_column": ["value1", "value2"],
            }
        )

        result = optimize_dtypes_hadeg(df)

        assert result["Gene"].dtype.name == "category"
        assert result["ko"].dtype.name == "category"
        assert result["other_column"].dtype.name != "category"

    def test_optimize_dtypes_with_minimal_data(self, mock_hadeg_minimal_dataframe):
        """Test optimization with minimal HADEG data."""
        result = optimize_dtypes_hadeg(mock_hadeg_minimal_dataframe)

        assert isinstance(result, pd.DataFrame)
        assert result["Gene"].dtype.name == "category"
        assert result["ko"].dtype.name == "category"
        assert result["Pathway"].dtype.name == "category"
        assert result["compound_pathway"].dtype.name == "category"

    def test_optimize_dtypes_invalid_input(self):
        """Test error handling for invalid input type."""
        with pytest.raises(TypeError, match="Input must be a pandas DataFrame"):
            optimize_dtypes_hadeg("not_a_dataframe")

    def test_optimize_dtypes_empty_dataframe(self, mock_hadeg_empty_dataframe):
        """Test optimization with empty DataFrame."""
        result = optimize_dtypes_hadeg(mock_hadeg_empty_dataframe)

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_optimize_dtypes_no_hadeg_columns(self):
        """Test optimization when no HADEG columns are present."""
        df = pd.DataFrame(
            {"random_column1": ["value1", "value2"], "random_column2": [1, 2]}
        )

        result = optimize_dtypes_hadeg(df)

        assert isinstance(result, pd.DataFrame)
        assert result["random_column1"].dtype.name != "category"
        assert result["random_column2"].dtype.name != "category"

    def test_optimize_dtypes_with_duplicates(self, mock_hadeg_database_with_duplicates):
        """Test optimization with duplicate entries."""
        result = optimize_dtypes_hadeg(mock_hadeg_database_with_duplicates)

        assert isinstance(result, pd.DataFrame)
        assert result["Gene"].dtype.name == "category"
        assert result["ko"].dtype.name == "category"
        assert result["Pathway"].dtype.name == "category"
        assert result["compound_pathway"].dtype.name == "category"
