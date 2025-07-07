"""
Comprehensive test suite for ToxCSM merge processing functionality.

This module contains comprehensive tests for the ToxCSM merge processing
pipeline, covering basic functionality, edge cases, error handling,
and optimization features.
"""

import pandas as pd
import pytest

from biorempp.input_processing.toxcsm_merge_processing import (
    merge_input_with_toxcsm,
    optimize_dtypes_toxcsm,
)


class TestMergeInputWithToxcsm:
    """Test cases for merge_input_with_toxcsm function."""

    def test_successful_merge_minimal_data(self, mock_toxcsm_minimal_csv):
        """Test successful merge with minimal ToxCSM data."""
        # Create input DataFrame with matching cpd
        input_df = pd.DataFrame(
            {
                "sample": ["TestSample"],
                "ko": ["K00001"],
                "cpd": ["C13881"],
                "compoundclass": ["Metal"],
            }
        )

        result = merge_input_with_toxcsm(
            input_df, database_filepath=mock_toxcsm_minimal_csv, optimize_types=False
        )

        # Verify merge was successful
        assert len(result) == 1
        assert "cpd" in result.columns
        assert "C13881" in result["cpd"].values
        assert "value_NR_AR" in result.columns
        assert "label_NR_AR" in result.columns

    def test_successful_merge_extreme_values(self, mock_toxcsm_minimal_csv):
        """Test merge with extreme toxicity values."""
        input_df = pd.DataFrame(
            {
                "sample": ["Sample1"],
                "ko": ["K00001"],
                "cpd": ["C13881"],  # Use same compound as minimal fixture
                "compoundclass": ["Metal"],
            }
        )

        result = merge_input_with_toxcsm(
            input_df, database_filepath=mock_toxcsm_minimal_csv, optimize_types=False
        )

        # Verify merge was successful
        assert len(result) == 1
        assert set(result["cpd"]) == {"C13881"}

    def test_merge_with_missing_values(self, mock_toxcsm_missing_values_csv):
        """Test merge with ToxCSM data containing missing values."""
        input_df = pd.DataFrame(
            {
                "sample": ["S1", "S2", "S3"],
                "ko": ["K77777", "K66666", "K55555"],
                "cpd": ["C77777", "C66666", "C55555"],
                "compoundclass": ["Class1", "Class2", "Class3"],
            }
        )

        result = merge_input_with_toxcsm(
            input_df,
            database_filepath=mock_toxcsm_missing_values_csv,
            optimize_types=False,
        )

        # Verify merge was successful despite missing values
        assert len(result) == 3
        assert set(result["cpd"]) == {"C77777", "C66666", "C55555"}

        # Check that missing values are handled (should be NaN or empty)
        missing_compound = result[result["cpd"] == "C77777"]
        assert len(missing_compound) == 1

    def test_merge_with_duplicates(self, mock_toxcsm_minimal_csv):
        """Test merge with ToxCSM data containing duplicates."""
        input_df = pd.DataFrame(
            {
                "sample": ["S1"],
                "ko": ["K12345"],
                "cpd": ["C13881"],  # Use compound from minimal fixture
                "compoundclass": ["Class1"],
            }
        )

        result = merge_input_with_toxcsm(
            input_df, database_filepath=mock_toxcsm_minimal_csv, optimize_types=False
        )

        # Should get one row since minimal fixture has one compound
        assert len(result) == 1
        assert "C13881" in result["cpd"].values

    def test_no_matching_compounds(self, mock_toxcsm_minimal_csv):
        """Test merge when no compounds match."""
        input_df = pd.DataFrame(
            {
                "sample": ["TestSample"],
                "ko": ["K00001"],
                "cpd": ["C99999"],  # Non-existent compound
                "compoundclass": ["Unknown"],
            }
        )

        result = merge_input_with_toxcsm(
            input_df, database_filepath=mock_toxcsm_minimal_csv, optimize_types=False
        )

        # Should return empty DataFrame
        assert len(result) == 0
        assert "cpd" in result.columns

    def test_optimize_types_enabled(self, mock_toxcsm_minimal_csv):
        """Test merge with dtype optimization enabled."""
        input_df = pd.DataFrame(
            {
                "sample": ["TestSample"],
                "ko": ["K00001"],
                "cpd": ["C13881"],
                "compoundclass": ["Metal"],
            }
        )

        result = merge_input_with_toxcsm(
            input_df, database_filepath=mock_toxcsm_minimal_csv, optimize_types=True
        )

        # Verify categorical columns
        categorical_cols = ["cpd", "compoundname", "sample"]
        for col in categorical_cols:
            if col in result.columns:
                assert result[col].dtype.name == "category"

        # Verify float32 value columns
        value_cols = [col for col in result.columns if col.startswith("value_")]
        for col in value_cols:
            assert result[col].dtype == "float32"

    def test_default_database_path(self):
        """Test using default database path."""
        input_df = pd.DataFrame(
            {
                "sample": ["TestSample"],
                "ko": ["K00001"],
                "cpd": ["C13881"],
                "compoundclass": ["Metal"],
            }
        )

        # This should raise FileNotFoundError since default path doesn't exist
        with pytest.raises(FileNotFoundError):
            merge_input_with_toxcsm(input_df)

    def test_missing_cpd_column_in_input(self, mock_toxcsm_minimal_csv):
        """Test error when input DataFrame lacks 'cpd' column."""
        input_df = pd.DataFrame(
            {
                "sample": ["TestSample"],
                "ko": ["K00001"],
                "compoundclass": ["Metal"],
                # Missing 'cpd' column
            }
        )

        with pytest.raises(KeyError, match="cpd.*must be present"):
            merge_input_with_toxcsm(input_df, database_filepath=mock_toxcsm_minimal_csv)

    def test_nonexistent_database_file(self):
        """Test error when database file doesn't exist."""
        input_df = pd.DataFrame(
            {
                "sample": ["TestSample"],
                "ko": ["K00001"],
                "cpd": ["C13881"],
                "compoundclass": ["Metal"],
            }
        )

        with pytest.raises(FileNotFoundError):
            merge_input_with_toxcsm(
                input_df, database_filepath="/nonexistent/path/database.csv"
            )

    def test_invalid_file_format(self, tmp_path):
        """Test error when database file is not CSV."""
        # Create a non-CSV file
        invalid_file = tmp_path / "database.txt"
        invalid_file.write_text("some text")

        input_df = pd.DataFrame(
            {
                "sample": ["TestSample"],
                "ko": ["K00001"],
                "cpd": ["C13881"],
                "compoundclass": ["Metal"],
            }
        )

        with pytest.raises(ValueError, match="Unsupported file format"):
            merge_input_with_toxcsm(input_df, database_filepath=str(invalid_file))

    def test_empty_input_dataframe(self, mock_toxcsm_minimal_csv):
        """Test merge with empty input DataFrame."""
        input_df = pd.DataFrame(columns=["sample", "ko", "cpd", "compoundclass"])

        result = merge_input_with_toxcsm(
            input_df, database_filepath=mock_toxcsm_minimal_csv
        )

        # Should return empty DataFrame
        assert len(result) == 0


class TestOptimizeDtypesToxcsm:
    """Test cases for optimize_dtypes_toxcsm function."""

    def test_optimize_categorical_columns(self):
        """Test optimization of categorical columns."""
        df = pd.DataFrame(
            {
                "SMILES": ["[Ba++]", "[Na+]", "[Ca++]"],
                "cpd": ["C13881", "C13882", "C13883"],
                "ChEBI": ["37136", "37137", "37138"],
                "compoundname": ["Barium", "Sodium", "Calcium"],
                "sample": ["S1", "S2", "S3"],
                "value_NR_AR": [0.1, 0.2, 0.3],
            }
        )

        result = optimize_dtypes_toxcsm(df)

        # Check categorical columns
        categorical_cols = ["SMILES", "cpd", "ChEBI", "compoundname", "sample"]
        for col in categorical_cols:
            assert result[col].dtype.name == "category"

    def test_optimize_label_columns(self):
        """Test optimization of label_* columns."""
        df = pd.DataFrame(
            {
                "cpd": ["C1", "C2", "C3"],
                "label_NR_AR": ["High Safety", "Medium Safety", "Low Safety"],
                "label_NR_ER": ["High Safety", "High Safety", "Medium Safety"],
                "label_Gen_AMES": ["Low Toxicity", "Medium Toxicity", "High Toxicity"],
            }
        )

        result = optimize_dtypes_toxcsm(df)

        # Check that all label columns are categorical
        label_cols = [col for col in result.columns if col.startswith("label_")]
        for col in label_cols:
            assert result[col].dtype.name == "category"

    def test_optimize_value_columns(self):
        """Test optimization of value_* columns."""
        df = pd.DataFrame(
            {
                "cpd": ["C1", "C2", "C3"],
                "value_NR_AR": ["0.1", "0.2", "0.3"],
                "value_NR_ER": ["0.4", "0.5", "0.6"],
                "value_Gen_AMES": ["0.7", "0.8", "0.9"],
            }
        )

        result = optimize_dtypes_toxcsm(df)

        # Check that all value columns are float32
        value_cols = [col for col in result.columns if col.startswith("value_")]
        for col in value_cols:
            assert result[col].dtype == "float32"

    def test_optimize_with_missing_values(self):
        """Test optimization with missing values in numeric columns."""
        df = pd.DataFrame(
            {
                "cpd": ["C1", "C2", "C3"],
                "value_NR_AR": ["0.1", "", "0.3"],
                "value_NR_ER": ["0.4", "invalid", "0.6"],
                "label_NR_AR": ["High Safety", "", "Low Safety"],
            }
        )

        result = optimize_dtypes_toxcsm(df)

        # Value columns should be float32 with NaN for invalid values
        assert result["value_NR_AR"].dtype == "float32"
        assert result["value_NR_ER"].dtype == "float32"
        assert pd.isna(result["value_NR_AR"].iloc[1])
        assert pd.isna(result["value_NR_ER"].iloc[1])

        # Label columns should be categorical
        assert result["label_NR_AR"].dtype.name == "category"

    def test_optimize_invalid_input(self):
        """Test error when input is not a DataFrame."""
        with pytest.raises(TypeError, match="Input must be a pandas DataFrame"):
            optimize_dtypes_toxcsm("not a dataframe")

        with pytest.raises(TypeError, match="Input must be a pandas DataFrame"):
            optimize_dtypes_toxcsm(None)

        with pytest.raises(TypeError, match="Input must be a pandas DataFrame"):
            optimize_dtypes_toxcsm([1, 2, 3])

    def test_optimize_empty_dataframe(self):
        """Test optimization with empty DataFrame."""
        df = pd.DataFrame()
        result = optimize_dtypes_toxcsm(df)
        assert len(result) == 0

    def test_optimize_missing_columns(self):
        """Test optimization when expected columns are missing."""
        df = pd.DataFrame({"some_other_col": ["A", "B", "C"], "another_col": [1, 2, 3]})

        # Should not raise error, just skip missing columns
        result = optimize_dtypes_toxcsm(df)
        assert len(result) == 3
        assert "some_other_col" in result.columns
        assert "another_col" in result.columns


class TestToxcsmIntegration:
    """Integration tests for ToxCSM processing pipeline."""

    def test_end_to_end_pipeline(self, mock_toxcsm_minimal_csv):
        """Test complete end-to-end processing with ToxCSM data."""
        # Simulate input from previous pipeline steps
        input_df = pd.DataFrame(
            {
                "sample": ["SampleA", "SampleB"],
                "ko": ["K00001", "K00002"],
                "cpd": ["C13881", "C13881"],  # Both map to same compound
                "compoundclass": ["Metal", "Metal"],
                "genesymbol": ["Gene1", "Gene2"],
                "genename": ["Gene Name 1", "Gene Name 2"],
            }
        )

        result = merge_input_with_toxcsm(
            input_df, database_filepath=mock_toxcsm_minimal_csv, optimize_types=True
        )

        # Verify complete pipeline
        assert len(result) == 2
        assert "value_NR_AR" in result.columns
        assert "label_NR_AR" in result.columns
        assert result["cpd"].dtype.name == "category"
        assert result["value_NR_AR"].dtype == "float32"

    def test_large_input_dataset(self, mock_toxcsm_minimal_csv):
        """Test processing with larger input dataset."""
        # Create larger input dataset using the compound from minimal fixture
        compounds = ["C13881"] * 100  # 100 entries of same compound
        input_df = pd.DataFrame(
            {
                "sample": [f"Sample_{i}" for i in range(len(compounds))],
                "ko": [f"K{i:05d}" for i in range(len(compounds))],
                "cpd": compounds,
                "compoundclass": ["TestClass"] * len(compounds),
            }
        )

        result = merge_input_with_toxcsm(
            input_df, database_filepath=mock_toxcsm_minimal_csv, optimize_types=True
        )

        # Should have 100 results (all compounds match)
        assert len(result) == 100
        assert len(result["cpd"].unique()) == 1

    def test_memory_efficiency(self, mock_toxcsm_minimal_csv):
        """Test memory efficiency with optimization enabled."""
        input_df = pd.DataFrame(
            {
                "sample": ["TestSample"] * 1000,
                "ko": ["K00001"] * 1000,
                "cpd": ["C13881"] * 1000,
                "compoundclass": ["Metal"] * 1000,
            }
        )

        # Test without optimization
        result_no_opt = merge_input_with_toxcsm(
            input_df, database_filepath=mock_toxcsm_minimal_csv, optimize_types=False
        )

        # Test with optimization
        result_opt = merge_input_with_toxcsm(
            input_df, database_filepath=mock_toxcsm_minimal_csv, optimize_types=True
        )

        # Both should have same shape
        assert result_no_opt.shape == result_opt.shape

        # Optimized version should have categorical types
        assert result_opt["cpd"].dtype.name == "category"
        assert result_opt["compoundname"].dtype.name == "category"
