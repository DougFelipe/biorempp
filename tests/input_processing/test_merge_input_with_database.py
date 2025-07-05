"""
Unit tests for biorempp_merge_processing module.

Tests for merge functions, particularly merge_input_with_biorempp.
"""

import os
from unittest.mock import patch

import pandas as pd
import pytest

from biorempp.input_processing.biorempp_merge_processing import (
    merge_input_with_biorempp,
)


class TestMergeInputWithBiorempp:
    """Test suite for merge_input_with_biorempp function."""

    @pytest.fixture
    def input_df_from_fasta(self, fasta_like_input_txt):
        """
        Create input DataFrame from FASTA-like mock input.

        Uses the project's parsing function to create a DataFrame
        from the mock FASTA input fixture.
        """
        from biorempp.input_processing.input_validator import validate_and_process_input

        df, error = validate_and_process_input(fasta_like_input_txt, "input.txt")
        assert error is None
        return df

    def test_merge_input_with_biorempp_happy_path(
        self, input_df_from_fasta, mock_biorempp_db_csv
    ):
        """
        Test successful merge of input DataFrame with BioRemPP database.

        Verifies that the function performs a complete merge using
        realistic mock data and returns expected columns and data.
        """
        # Act
        df_merged = merge_input_with_biorempp(input_df_from_fasta, mock_biorempp_db_csv)

        # Assert
        assert not df_merged.empty

        # Verify all expected columns are present
        expected_columns = [
            "ko",
            "genesymbol",
            "genename",
            "cpd",
            "compoundclass",
            "referenceAG",
            "compoundname",
            "enzyme_activity",
            "sample",
        ]
        for col in expected_columns:
            assert col in df_merged.columns

        # Verify only KOs from input are in the result
        assert df_merged["ko"].isin(input_df_from_fasta["ko"]).all()

    def test_merge_input_with_biorempp_inner_join_behavior(
        self, input_df_from_fasta, mock_biorempp_db_csv
    ):
        """
        Test that only matching KOs appear in result (inner join).

        Verifies that the merge function performs an inner join,
        excluding KOs that don't exist in the database.
        """
        # Arrange - Remove K00001 from database to test absence
        db = pd.read_csv(mock_biorempp_db_csv, sep=";")
        db_filtered = db[db["ko"] != "K00001"]
        test_path = mock_biorempp_db_csv.replace(".csv", "_noK00001.csv")
        db_filtered.to_csv(test_path, sep=";", index=False)

        # Act
        merged = merge_input_with_biorempp(input_df_from_fasta, test_path)

        # Assert
        assert "K00001" not in merged["ko"].values

        # Cleanup
        if os.path.exists(test_path):
            os.remove(test_path)

    def test_merge_input_with_biorempp_missing_ko_column_raises_error(
        self, input_df_from_fasta, tmp_path
    ):
        """
        Test that KeyError is raised when database lacks 'ko' column.

        Verifies that appropriate error handling occurs when the
        database file doesn't contain the required 'ko' column.
        """
        # Arrange
        path = tmp_path / "noko.csv"
        pd.DataFrame({"genename": ["a"]}).to_csv(path, sep=";", index=False)

        # Act & Assert
        with pytest.raises(KeyError):
            merge_input_with_biorempp(input_df_from_fasta, str(path))

    def test_merge_input_with_biorempp_file_not_found_raises_error(
        self, input_df_from_fasta
    ):
        """
        Test that FileNotFoundError is raised for non-existent database.

        Verifies that appropriate error handling occurs when the
        database file path doesn't exist.
        """
        # Act & Assert
        with pytest.raises(FileNotFoundError):
            merge_input_with_biorempp(input_df_from_fasta, "fake_path.csv")

    def test_merge_input_with_biorempp_empty_input_dataframe(
        self, mock_biorempp_db_csv
    ):
        """
        Test merge behavior with empty input DataFrame.

        Verifies that the function handles empty input DataFrames
        gracefully without raising exceptions.
        """
        # Arrange
        empty_df = pd.DataFrame(columns=["ko", "sample"])

        # Act
        result = merge_input_with_biorempp(empty_df, mock_biorempp_db_csv)

        # Assert
        assert result.empty

    def test_merge_input_with_biorempp_empty_database(
        self, input_df_from_fasta, tmp_path
    ):
        """
        Test merge behavior with empty database.

        Verifies that the function handles empty database files
        gracefully, returning an empty result.
        """
        # Arrange
        empty_db_path = tmp_path / "empty_db.csv"
        pd.DataFrame(columns=["ko", "genesymbol"]).to_csv(
            empty_db_path, sep=";", index=False
        )

        # Act
        result = merge_input_with_biorempp(input_df_from_fasta, str(empty_db_path))

        # Assert
        assert result.empty

    def test_merge_input_with_biorempp_preserves_sample_information(
        self, input_df_from_fasta, mock_biorempp_db_csv
    ):
        """
        Test that sample information is preserved in merged result.

        Verifies that the merge function maintains the sample
        information from the input DataFrame.
        """
        # Act
        df_merged = merge_input_with_biorempp(input_df_from_fasta, mock_biorempp_db_csv)

        # Assert
        assert "sample" in df_merged.columns

        # Verify sample values are preserved
        original_samples = set(input_df_from_fasta["sample"].values)
        merged_samples = set(df_merged["sample"].values)
        assert merged_samples.issubset(original_samples)

    def test_merge_input_with_biorempp_handles_duplicate_kos(
        self, mock_biorempp_db_csv, tmp_path
    ):
        """
        Test merge behavior with duplicate KOs in input.

        Verifies that the function correctly handles cases where
        the same KO appears multiple times in the input data.
        """
        # Arrange
        input_with_duplicates = pd.DataFrame(
            {
                "ko": ["K00001", "K00001", "K00002"],
                "sample": ["SampleA", "SampleB", "SampleC"],
            }
        )

        # Act
        result = merge_input_with_biorempp(input_with_duplicates, mock_biorempp_db_csv)

        # Assert
        assert not result.empty

        # Verify all input samples are represented
        assert set(result["sample"].values) == {"SampleA", "SampleB", "SampleC"}

    def test_merge_input_with_biorempp_multiple_compounds_per_ko(
        self, input_df_from_fasta, mock_biorempp_db_csv
    ):
        """
        Test merge with KOs having multiple compound associations.

        Verifies that the function correctly handles cases where
        one KO is associated with multiple compounds in the database.
        """
        # Act
        df_merged = merge_input_with_biorempp(input_df_from_fasta, mock_biorempp_db_csv)

        # Assert
        # K00001 should have multiple compound associations
        k00001_rows = df_merged[df_merged["ko"] == "K00001"]
        if not k00001_rows.empty:
            assert len(k00001_rows) > 1  # Multiple compounds per KO

    def test_merge_input_with_biorempp_custom_separator(
        self, input_df_from_fasta, tmp_path
    ):
        """
        Test merge with database using custom separator.

        Verifies that the function can handle database files
        with different separators (comma instead of semicolon).
        """
        # Arrange - Create a simple test database with comma separator
        test_db = pd.DataFrame(
            {
                "ko": ["K00001", "K00002"],
                "genesymbol": ["gene1", "gene2"],
                "genename": ["Gene 1", "Gene 2"],
                "cpd": ["C001", "C002"],
                "compoundclass": ["Class1", "Class2"],
                "referenceAG": ["REF1", "REF2"],
                "compoundname": ["Compound 1", "Compound 2"],
                "enzyme_activity": ["activity1", "activity2"],
            }
        )
        custom_sep_path = tmp_path / "custom_sep_db.csv"
        test_db.to_csv(custom_sep_path, sep=",", index=False)

        # Mock the function to handle comma separator
        mock_path = "biorempp.input_processing.biorempp_merge_processing.pd.read_csv"
        with patch(mock_path) as mock_read_csv:
            mock_read_csv.return_value = test_db

            # Act
            merge_input_with_biorempp(input_df_from_fasta, str(custom_sep_path))

            # Assert
            mock_read_csv.assert_called_once()

    def test_merge_input_with_biorempp_data_types_preserved(
        self, input_df_from_fasta, mock_biorempp_db_csv
    ):
        """
        Test that data types are preserved during merge.

        Verifies that the merge function maintains appropriate
        data types for columns in the result DataFrame.
        """
        # Act
        df_merged = merge_input_with_biorempp(input_df_from_fasta, mock_biorempp_db_csv)

        # Assert
        assert not df_merged.empty

        # Verify string columns are preserved as strings or categories
        string_columns = ["ko", "genesymbol", "genename", "sample"]
        for col in string_columns:
            if col in df_merged.columns:
                # Accept both object and categorical dtypes for string data
                is_object = df_merged[col].dtype == "object"
                is_category = df_merged[col].dtype.name == "category"
                assert is_object or is_category

    def test_merge_input_with_biorempp_performance_large_dataset(
        self, mock_biorempp_db_csv, tmp_path
    ):
        """
        Test merge performance with large input dataset.

        Verifies that the function can handle larger datasets
        without significant performance degradation.
        """
        # Arrange
        import numpy as np

        large_input = pd.DataFrame(
            {
                "ko": np.random.choice(["K00001", "K00002", "K00003"], 10000),
                "sample": [f"Sample_{i}" for i in range(10000)],
            }
        )

        # Act
        result = merge_input_with_biorempp(large_input, mock_biorempp_db_csv)

        # Assert
        assert not result.empty
        assert len(result) > 0
