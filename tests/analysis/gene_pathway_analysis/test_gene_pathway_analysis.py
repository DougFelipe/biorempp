"""
Unit tests for gene pathway analysis module.

This module contains comprehensive tests for the GenePathwayAnalyzer class,
including tests for valid data, malformed data, and missing column scenarios.
"""

import pandas as pd
import pytest

from biorempp.analysis.gene_pathway_analysis import GenePathwayAnalyzer


class TestGenePathwayAnalyzer:
    """Test suite for GenePathwayAnalyzer class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.analyzer = GenePathwayAnalyzer()

    def test_analyzer_initialization(self):
        """Test that analyzer initializes correctly."""
        assert self.analyzer is not None
        assert hasattr(self.analyzer, "logger")

    def test_validate_dataframe_valid_input(self, mock_merged_biorempp_basic):
        """Test DataFrame validation with valid input."""
        required_columns = ["sample", "ko"]

        # Should not raise any exception
        self.analyzer._validate_dataframe(mock_merged_biorempp_basic, required_columns)

    def test_validate_dataframe_missing_columns(
        self, mock_merged_biorempp_missing_columns
    ):
        """Test DataFrame validation with missing required columns."""
        required_columns = ["sample", "ko"]

        with pytest.raises(ValueError, match="Missing required columns"):
            self.analyzer._validate_dataframe(
                mock_merged_biorempp_missing_columns, required_columns
            )

    def test_validate_dataframe_empty_dataframe(self, mock_merged_biorempp_empty):
        """Test DataFrame validation with empty DataFrame."""
        required_columns = ["sample", "ko"]

        with pytest.raises(ValueError, match="DataFrame cannot be empty"):
            self.analyzer._validate_dataframe(
                mock_merged_biorempp_empty, required_columns
            )

    def test_validate_dataframe_wrong_type(self):
        """Test DataFrame validation with wrong input type."""
        not_a_dataframe = [{"sample": "Sample1", "ko": "K00001"}]
        required_columns = ["sample", "ko"]

        with pytest.raises(TypeError, match="Input must be a pandas DataFrame"):
            self.analyzer._validate_dataframe(not_a_dataframe, required_columns)

    def test_analyze_ko_counts_valid_data(self, mock_merged_biorempp_basic):
        """Test KO counting analysis with valid data."""
        result = self.analyzer.analyze_ko_counts_per_sample(mock_merged_biorempp_basic)

        # Check result structure
        assert isinstance(result, pd.DataFrame)
        assert list(result.columns) == ["sample", "ko_count"]
        assert len(result) == 3

        # Check sorting (should be descending by ko_count)
        assert result.iloc[0]["ko_count"] >= result.iloc[1]["ko_count"]
        assert result.iloc[1]["ko_count"] >= result.iloc[2]["ko_count"]

        # Check specific counts
        sample1_count = result[result["sample"] == "Sample1"]["ko_count"].iloc[0]
        sample2_count = result[result["sample"] == "Sample2"]["ko_count"].iloc[0]
        sample3_count = result[result["sample"] == "Sample3"]["ko_count"].iloc[0]

        assert sample1_count == 2  # K00001, K00002
        assert sample2_count == 2  # K00001, K00003
        assert sample3_count == 1  # K00001

    def test_analyze_ko_counts_single_sample(self, mock_merged_biorempp_single_sample):
        """Test KO counting analysis with single sample."""
        result = self.analyzer.analyze_ko_counts_per_sample(
            mock_merged_biorempp_single_sample
        )

        assert len(result) == 1
        assert result.iloc[0]["sample"] == "Sample1"
        assert result.iloc[0]["ko_count"] == 2  # Unique KOs: K00001, K00002

    def test_analyze_ko_counts_duplicate_kos(
        self, mock_merged_biorempp_with_duplicates
    ):
        """Test KO counting with duplicate KO identifiers."""
        result = self.analyzer.analyze_ko_counts_per_sample(
            mock_merged_biorempp_with_duplicates
        )

        assert len(result) == 1
        assert result.iloc[0]["ko_count"] == 3  # Unique KOs: K00001, K00002, K00003

    def test_analyze_ko_counts_missing_required_columns(
        self, mock_merged_biorempp_missing_columns
    ):
        """Test KO analysis with missing required columns."""
        with pytest.raises(ValueError, match="Missing required columns"):
            self.analyzer.analyze_ko_counts_per_sample(
                mock_merged_biorempp_missing_columns
            )

    def test_analyze_ko_counts_empty_dataframe(self, mock_merged_biorempp_empty):
        """Test KO analysis with empty DataFrame."""
        with pytest.raises(ValueError, match="DataFrame cannot be empty"):
            self.analyzer.analyze_ko_counts_per_sample(mock_merged_biorempp_empty)

    def test_analyze_ko_counts_wrong_input_type(self):
        """Test KO analysis with wrong input type."""
        wrong_input = "not a dataframe"

        with pytest.raises(TypeError, match="Input must be a pandas DataFrame"):
            self.analyzer.analyze_ko_counts_per_sample(wrong_input)

    def test_analyze_ko_counts_with_none_values(
        self, mock_merged_biorempp_with_missing_values
    ):
        """Test KO analysis with None/NaN values."""
        result = self.analyzer.analyze_ko_counts_per_sample(
            mock_merged_biorempp_with_missing_values
        )

        # pandas nunique() excludes NaN values by default
        sample1_count = result[result["sample"] == "Sample1"]["ko_count"].iloc[0]
        sample2_count = result[result["sample"] == "Sample2"]["ko_count"].iloc[0]

        assert sample1_count == 1  # Only K00001 (None is excluded)
        assert sample2_count == 2  # K00002, K00003

    def test_analyze_ko_counts_mixed_data_types(self, mock_merged_biorempp_mixed_types):
        """Test KO analysis with mixed data types in KO column."""
        result = self.analyzer.analyze_ko_counts_per_sample(
            mock_merged_biorempp_mixed_types
        )

        assert len(result) == 1
        assert result.iloc[0]["ko_count"] == 3  # All values are counted as unique

    def test_analyze_ko_counts_extra_columns(
        self, mock_merged_biorempp_with_extra_columns
    ):
        """Test KO analysis with extra columns in DataFrame."""
        result = self.analyzer.analyze_ko_counts_per_sample(
            mock_merged_biorempp_with_extra_columns
        )

        # Should work fine, only uses required columns
        assert isinstance(result, pd.DataFrame)
        assert list(result.columns) == ["sample", "ko_count"]
        assert len(result) == 2

    def test_analyze_ko_counts_large_dataset(self, mock_merged_biorempp_large_dataset):
        """Test KO analysis performance with larger dataset."""
        result = self.analyzer.analyze_ko_counts_per_sample(
            mock_merged_biorempp_large_dataset
        )

        # Basic checks
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 100  # 100 unique samples
        assert all(result["ko_count"] > 0)
        assert result["ko_count"].dtype in ["int64", "int32"]

        # Check sorting
        assert (result["ko_count"].diff().dropna() <= 0).all()


def test_legacy_process_ko_data_function(mock_merged_biorempp_basic):
    """Test the legacy process_ko_data function."""
    from biorempp.analysis.gene_pathway_analysis import process_ko_data

    # Use only first 3 rows to match expected result
    df = mock_merged_biorempp_basic.copy()

    result = process_ko_data(df)

    # Should work the same as the new method
    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ["sample", "ko_count"]
    assert len(result) == 3


def test_legacy_process_ko_data_with_list_input():
    """Test the legacy function with list of dicts input."""
    from biorempp.analysis.gene_pathway_analysis import process_ko_data

    data = [
        {"sample": "Sample1", "ko": "K00001"},
        {"sample": "Sample1", "ko": "K00002"},
        {"sample": "Sample2", "ko": "K00001"},
    ]

    result = process_ko_data(data)

    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ["sample", "ko_count"]
    assert len(result) == 2


def test_legacy_process_ko_data_invalid_input():
    """Test the legacy function with invalid input."""
    from biorempp.analysis.gene_pathway_analysis import process_ko_data

    with pytest.raises(ValueError, match="must be a pandas DataFrame or a list"):
        process_ko_data("invalid input")
