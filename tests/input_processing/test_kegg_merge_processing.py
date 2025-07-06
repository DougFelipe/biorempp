"""
Test suite for KEGG merge processing functionality.

This module contains comprehensive tests for the KEGG degradation pathway
merging functionality including validation, error handling, and optimization.
"""

from unittest.mock import patch

import pandas as pd
import pytest

from biorempp.input_processing.kegg_merge_processing import (
    merge_input_with_kegg,
    optimize_dtypes_kegg,
)


class TestMergeInputWithKegg:
    """Test class for merge_input_with_kegg function."""

    def test_merge_input_with_kegg_success_happy_path(
        self, mock_kegg_degradation_pathways_dataframe
    ):
        """Test successful merge with KEGG database."""
        input_data = pd.DataFrame(
            {"ko": ["K00001", "K00002"], "sample": ["sample1", "sample2"]}
        )

        with patch("os.path.exists", return_value=True), patch(
            "pandas.read_csv", return_value=mock_kegg_degradation_pathways_dataframe
        ):

            result = merge_input_with_kegg(input_data, "dummy_path.csv")

            # Check that merge was successful
            assert isinstance(result, pd.DataFrame)
            assert len(result) > 0
            assert "ko" in result.columns
            assert "pathname" in result.columns
            assert "genesymbol" in result.columns

    def test_merge_input_with_kegg_file_not_found_error(self):
        """Test FileNotFoundError when KEGG file does not exist."""
        input_data = pd.DataFrame(
            {"ko": ["K00001", "K00002"], "sample": ["sample1", "sample2"]}
        )

        with pytest.raises(FileNotFoundError, match="KEGG file not found"):
            merge_input_with_kegg(input_data, "non_existent_file.csv")

    def test_merge_input_with_kegg_invalid_extension_error(self):
        """Test ValueError when file extension is not .csv."""
        input_data = pd.DataFrame(
            {"ko": ["K00001", "K00002"], "sample": ["sample1", "sample2"]}
        )

        with patch("os.path.exists", return_value=True):
            with pytest.raises(ValueError, match="Unsupported file format"):
                merge_input_with_kegg(input_data, "dummy_file.txt")

    def test_merge_input_with_kegg_missing_ko_column_in_input(self):
        """Test KeyError when 'ko' column is missing from input."""
        input_data = pd.DataFrame({"sample": ["sample1", "sample2"]})

        mock_kegg_data = pd.DataFrame(
            {
                "ko": ["K00001", "K00002"],
                "pathname": ["Pathway1", "Pathway2"],
                "genesymbol": ["Gene1", "Gene2"],
            }
        )

        with patch("os.path.exists", return_value=True), patch(
            "pandas.read_csv", return_value=mock_kegg_data
        ):

            with pytest.raises(KeyError, match="Column 'ko' must be present"):
                merge_input_with_kegg(input_data, "dummy_path.csv")

    def test_merge_input_with_kegg_missing_ko_column_in_kegg(self):
        """Test KeyError when 'ko' column is missing from KEGG data."""
        input_data = pd.DataFrame(
            {"ko": ["K00001", "K00002"], "sample": ["sample1", "sample2"]}
        )

        mock_kegg_data = pd.DataFrame(
            {"pathname": ["Pathway1", "Pathway2"], "genesymbol": ["Gene1", "Gene2"]}
        )

        with patch("os.path.exists", return_value=True), patch(
            "pandas.read_csv", return_value=mock_kegg_data
        ):

            with pytest.raises(KeyError, match="Column 'ko' must be present"):
                merge_input_with_kegg(input_data, "dummy_path.csv")

    def test_merge_input_with_kegg_default_path(
        self, mock_kegg_degradation_pathways_dataframe
    ):
        """Test that default path is used when none is provided."""
        input_data = pd.DataFrame(
            {"ko": ["K00001", "K00002"], "sample": ["sample1", "sample2"]}
        )

        with patch("os.path.exists", return_value=True), patch(
            "pandas.read_csv", return_value=mock_kegg_degradation_pathways_dataframe
        ):

            result = merge_input_with_kegg(input_data)

            assert isinstance(result, pd.DataFrame)
            assert len(result) > 0

    def test_merge_input_with_kegg_no_matches(self):
        """Test behavior when no KO matches are found."""
        input_data = pd.DataFrame(
            {"ko": ["K99999", "K88888"], "sample": ["sample1", "sample2"]}
        )

        mock_kegg_data = pd.DataFrame(
            {
                "ko": ["K00001", "K00002"],
                "pathname": ["Pathway1", "Pathway2"],
                "genesymbol": ["Gene1", "Gene2"],
            }
        )

        with patch("os.path.exists", return_value=True), patch(
            "pandas.read_csv", return_value=mock_kegg_data
        ):

            result = merge_input_with_kegg(input_data, "dummy_path.csv")

            assert isinstance(result, pd.DataFrame)
            assert len(result) == 0  # No matches found

    def test_merge_input_with_kegg_optimize_types_disabled(
        self, mock_kegg_degradation_pathways_dataframe
    ):
        """Test merge with type optimization disabled."""
        input_data = pd.DataFrame(
            {"ko": ["K00001", "K00002"], "sample": ["sample1", "sample2"]}
        )

        with patch("os.path.exists", return_value=True), patch(
            "pandas.read_csv", return_value=mock_kegg_degradation_pathways_dataframe
        ):

            result = merge_input_with_kegg(
                input_data, "dummy_path.csv", optimize_types=False
            )

            assert isinstance(result, pd.DataFrame)
            assert len(result) > 0
            # Check that columns are not categorical when optimization is disabled
            assert not pd.api.types.is_categorical_dtype(result["ko"])

    def test_merge_input_with_kegg_csv_read_error(self):
        """Test handling of CSV read errors."""
        input_data = pd.DataFrame(
            {"ko": ["K00001", "K00002"], "sample": ["sample1", "sample2"]}
        )

        with patch("os.path.exists", return_value=True), patch(
            "pandas.read_csv", side_effect=pd.errors.EmptyDataError("Empty CSV")
        ):

            with pytest.raises(pd.errors.EmptyDataError):
                merge_input_with_kegg(input_data, "dummy_path.csv")


class TestOptimizeDtypesKegg:
    """Test class for optimize_dtypes_kegg function."""

    def test_optimize_dtypes_kegg_success(self):
        """Test successful dtype optimization for KEGG data."""
        df = pd.DataFrame(
            {
                "ko": ["K00001", "K00002", "K00003"],
                "pathname": ["Path1", "Path2", "Path3"],
                "genesymbol": ["Gene1", "Gene2", "Gene3"],
                "sample": ["sample1", "sample2", "sample3"],
                "other_col": [1, 2, 3],
            }
        )

        result = optimize_dtypes_kegg(df)

        assert isinstance(result, pd.DataFrame)
        assert pd.api.types.is_categorical_dtype(result["ko"])
        assert pd.api.types.is_categorical_dtype(result["pathname"])
        assert pd.api.types.is_categorical_dtype(result["genesymbol"])
        assert pd.api.types.is_categorical_dtype(result["sample"])
        assert not pd.api.types.is_categorical_dtype(result["other_col"])

    def test_optimize_dtypes_kegg_missing_columns(self):
        """Test optimization when some categorical columns are missing."""
        df = pd.DataFrame(
            {"ko": ["K00001", "K00002", "K00003"], "other_col": [1, 2, 3]}
        )

        result = optimize_dtypes_kegg(df)

        assert isinstance(result, pd.DataFrame)
        assert pd.api.types.is_categorical_dtype(result["ko"])
        assert not pd.api.types.is_categorical_dtype(result["other_col"])

    def test_optimize_dtypes_kegg_invalid_input(self):
        """Test TypeError when input is not a DataFrame."""
        with pytest.raises(TypeError, match="Input must be a pandas DataFrame"):
            optimize_dtypes_kegg("not_a_dataframe")

    def test_optimize_dtypes_kegg_empty_dataframe(self):
        """Test optimization with empty DataFrame."""
        df = pd.DataFrame()

        result = optimize_dtypes_kegg(df)

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_optimize_dtypes_kegg_preserves_original_data(self):
        """Test that optimization preserves original data values."""
        df = pd.DataFrame(
            {
                "ko": ["K00001", "K00002", "K00003"],
                "pathname": ["Path1", "Path2", "Path3"],
                "genesymbol": ["Gene1", "Gene2", "Gene3"],
            }
        )

        original_ko_values = df["ko"].tolist()
        original_pathname_values = df["pathname"].tolist()
        original_genesymbol_values = df["genesymbol"].tolist()

        result = optimize_dtypes_kegg(df)

        assert result["ko"].tolist() == original_ko_values
        assert result["pathname"].tolist() == original_pathname_values
        assert result["genesymbol"].tolist() == original_genesymbol_values
