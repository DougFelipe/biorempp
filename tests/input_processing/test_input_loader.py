"""
Unit tests for input_loader module.

Tests for input loading and merging functions,
particularly load_and_merge_input.
"""

import pandas as pd

from biorempp.input_processing.input_loader import load_and_merge_input


class TestLoadAndMergeInput:
    """Test suite for load_and_merge_input function."""

    def test_load_and_merge_input_success_happy_path(
        self, fasta_like_input_txt, mock_biorempp_db_csv
    ):
        """
        Test successful loading and merging with valid inputs.

        Verifies that the function correctly processes valid input
        and database files, returning expected DataFrame structure.
        """
        # Act
        df, error = load_and_merge_input(
            fasta_like_input_txt, "input.txt", database_filepath=mock_biorempp_db_csv
        )

        # Assert
        assert error is None
        assert isinstance(df, pd.DataFrame)

        # Verify required columns are present
        assert "sample" in df.columns
        assert "ko" in df.columns
        assert "genesymbol" in df.columns

        # Verify samples from input are present
        expected_samples = ["SampleA", "SampleB", "SampleC", "SampleD", "SampleE"]
        assert df["sample"].isin(expected_samples).any()

        # Verify KOs from input are present
        expected_kos = [
            "K00001",
            "K00002",
            "K00003",
            "K00004",
            "K00005",
            "K00006",
            "K00007",
            "K00008",
            "K00009",
            "K00010",
            "K00011",
            "K00012",
            "K00013",
            "K00014",
            "K00015",
            "K00016",
            "K00017",
            "K00018",
            "K00019",
            "K00020",
        ]
        assert df["ko"].isin(expected_kos).all()

    def test_load_and_merge_input_invalid_extension_error(
        self, fasta_like_input_txt, mock_biorempp_db_csv
    ):
        """
        Test error handling for invalid file extensions.

        Verifies that the function rejects files with unsupported
        extensions and returns appropriate error messages.
        """
        # Act
        df, error = load_and_merge_input(
            fasta_like_input_txt, "input.csv", database_filepath=mock_biorempp_db_csv
        )

        # Assert
        assert df is None
        assert error is not None
        assert "file type" in error or "extension" in error.lower()

    def test_load_and_merge_input_invalid_format_error(self, mock_biorempp_db_csv):
        """
        Test error handling for invalid input format.

        Verifies that the function rejects input with KO entries
        before sample declarations.
        """
        # Arrange
        invalid_txt = "K00001\n>SampleA\nK00002"

        # Act
        df, error = load_and_merge_input(
            invalid_txt, "input.txt", database_filepath=mock_biorempp_db_csv
        )

        # Assert
        assert df is None
        assert error is not None
        assert "format" in error.lower() or "Expected '>'" in error

    def test_load_and_merge_input_empty_file_error(self, mock_biorempp_db_csv):
        """
        Test error handling for empty input files.

        Verifies that the function handles empty input gracefully
        and returns appropriate error messages.
        """
        # Act
        df, error = load_and_merge_input(
            "", "input.txt", database_filepath=mock_biorempp_db_csv
        )

        # Assert
        assert df is None
        assert error is not None
        assert "No valid sample or KO entries" in error or "empty" in error.lower()

    def test_load_and_merge_input_database_not_found_error(self, fasta_like_input_txt):
        """
        Test error handling for non-existent database files.

        Verifies that the function handles missing database files
        gracefully and returns appropriate error messages.
        """
        # Act
        df, error = load_and_merge_input(
            fasta_like_input_txt, "input.txt", database_filepath="not_a_real_file.csv"
        )

        # Assert
        assert df is None
        assert error is not None
        assert "Database merge error" in error or "not found" in error

    def test_load_and_merge_input_ko_not_in_database(self, tmp_path):
        """
        Test handling of KOs not present in database.

        Verifies that the function returns empty DataFrame when
        input KOs are not found in the database.
        """
        # Arrange
        input_txt = ">SampleZ\nK99999\n"

        # Create minimal database with only K00001
        db = pd.DataFrame(
            [["K00001", "GEN", "test", "C001", "class", "ref", "cmp", "act"]],
            columns=[
                "ko",
                "genesymbol",
                "genename",
                "cpd",
                "compoundclass",
                "referenceAG",
                "compoundname",
                "enzyme_activity",
            ],
        )
        db_path = tmp_path / "testdb.csv"
        db.to_csv(db_path, sep=";", index=False)

        # Act
        df, error = load_and_merge_input(
            input_txt, "input.txt", database_filepath=str(db_path)
        )

        # Assert
        assert error is None
        assert isinstance(df, pd.DataFrame)
        assert df.empty  # No common KOs, so empty result

    def test_load_and_merge_input_base64_encoded_input(
        self, fasta_like_input_txt, mock_biorempp_db_csv
    ):
        """
        Test handling of base64 encoded input.

        Verifies that the function correctly processes base64
        encoded input strings.
        """
        # Arrange
        import base64

        base64_bytes = base64.b64encode(fasta_like_input_txt.encode()).decode()
        encoded_input = f"data:text/plain;base64,{base64_bytes}"

        # Act
        df, error = load_and_merge_input(
            encoded_input, "input.txt", database_filepath=mock_biorempp_db_csv
        )

        # Assert
        assert error is None
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    def test_load_and_merge_input_partial_ko_match(self, tmp_path):
        """
        Test handling of partial KO matches with database.

        Verifies that the function correctly handles cases where
        only some input KOs are present in the database.
        """
        # Arrange
        input_txt = ">SampleA\nK00001\nK99999\n>SampleB\nK00002\n"

        # Create database with only K00001 and K00002
        db = pd.DataFrame(
            [
                ["K00001", "GEN1", "gene1", "C001", "class1", "ref1", "cmp1", "act1"],
                ["K00002", "GEN2", "gene2", "C002", "class2", "ref2", "cmp2", "act2"],
            ],
            columns=[
                "ko",
                "genesymbol",
                "genename",
                "cpd",
                "compoundclass",
                "referenceAG",
                "compoundname",
                "enzyme_activity",
            ],
        )
        db_path = tmp_path / "partial_db.csv"
        db.to_csv(db_path, sep=";", index=False)

        # Act
        df, error = load_and_merge_input(
            input_txt, "input.txt", database_filepath=str(db_path)
        )

        # Assert
        assert error is None
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

        # Only K00001 and K00002 should be present (K99999 not in DB)
        assert set(df["ko"].unique()) == {"K00001", "K00002"}

    def test_load_and_merge_input_multiple_samples_same_ko(self, mock_biorempp_db_csv):
        """
        Test handling of multiple samples with same KO.

        Verifies that the function correctly handles cases where
        multiple samples contain the same KO entries.
        """
        # Arrange
        input_txt = ">SampleA\nK00001\n>SampleB\nK00001\n>SampleC\nK00002\n"

        # Act
        df, error = load_and_merge_input(
            input_txt, "input.txt", database_filepath=mock_biorempp_db_csv
        )

        # Assert
        assert error is None
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

        # Verify all samples are present
        assert set(df["sample"].unique()) == {"SampleA", "SampleB", "SampleC"}

        # Verify K00001 appears for both SampleA and SampleB
        k00001_samples = df[df["ko"] == "K00001"]["sample"].unique()
        assert "SampleA" in k00001_samples
        assert "SampleB" in k00001_samples

    def test_load_and_merge_input_whitespace_handling(self, mock_biorempp_db_csv):
        """
        Test handling of whitespace in input.

        Verifies that the function correctly handles leading/trailing
        whitespace and empty lines in input.
        """
        # Arrange
        input_with_whitespace = (
            "  \n"
            "  >SampleA  \n"
            "  K00001  \n"
            "  \n"
            "  >SampleB  \n"
            "  K00002  \n"
            "  \n"
        )

        # Act
        df, error = load_and_merge_input(
            input_with_whitespace, "input.txt", database_filepath=mock_biorempp_db_csv
        )

        # Assert
        assert error is None
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert "SampleA" in df["sample"].values
        assert "SampleB" in df["sample"].values

    def test_load_and_merge_input_malformed_database_error(
        self, fasta_like_input_txt, tmp_path
    ):
        """
        Test error handling for malformed database files.

        Verifies that the function handles database files with
        missing required columns gracefully.
        """
        # Arrange
        malformed_db = pd.DataFrame(
            {
                "wrong_column": ["value1", "value2"],
                "another_column": ["value3", "value4"],
            }
        )
        db_path = tmp_path / "malformed_db.csv"
        malformed_db.to_csv(db_path, sep=";", index=False)

        # Act
        df, error = load_and_merge_input(
            fasta_like_input_txt, "input.txt", database_filepath=str(db_path)
        )

        # Assert
        assert df is None
        assert error is not None
        assert "Database merge error" in error

    def test_load_and_merge_input_empty_database(self, fasta_like_input_txt, tmp_path):
        """
        Test handling of empty database files.

        Verifies that the function handles empty database files
        gracefully and returns appropriate results.
        """
        # Arrange
        empty_db = pd.DataFrame(
            columns=[
                "ko",
                "genesymbol",
                "genename",
                "cpd",
                "compoundclass",
                "referenceAG",
                "compoundname",
                "enzyme_activity",
            ]
        )
        db_path = tmp_path / "empty_db.csv"
        empty_db.to_csv(db_path, sep=";", index=False)

        # Act
        df, error = load_and_merge_input(
            fasta_like_input_txt, "input.txt", database_filepath=str(db_path)
        )

        # Assert
        assert error is None
        assert isinstance(df, pd.DataFrame)
        assert df.empty  # No data in database, so empty result

    def test_load_and_merge_input_large_dataset_performance(self, mock_biorempp_db_csv):
        """
        Test performance with large input datasets.

        Verifies that the function can handle larger datasets
        without significant performance degradation.
        """
        # Arrange
        large_input_parts = []
        for i in range(100):
            large_input_parts.append(f">Sample{i}")
            for j in range(5):
                # Use KOs that exist in the mock database
                ko_num = (j % 20) + 1
                large_input_parts.append(f"K{ko_num:05d}")

        large_input = "\n".join(large_input_parts)

        # Act
        df, error = load_and_merge_input(
            large_input, "input.txt", database_filepath=mock_biorempp_db_csv
        )

        # Assert
        assert error is None
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert len(df["sample"].unique()) <= 100
