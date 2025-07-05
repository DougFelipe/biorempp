"""
Unit tests for input_validator module.

Tests for input validation and processing functions,
particularly validate_and_process_input.
"""

import base64

import pandas as pd

from biorempp.input_processing.input_validator import validate_and_process_input


class TestValidateAndProcessInput:
    """Test suite for validate_and_process_input function."""

    def extract_ko_records(self, txt):
        """
        Extract (sample, ko) tuples from FASTA-like input.

        Used for comparing with DataFrame output to verify
        correct parsing of input format.

        Parameters
        ----------
        txt : str
            FASTA-like input text to parse.

        Returns
        -------
        list
            List of (sample, ko) tuples.
        """
        records = []
        current_sample = None
        for line in txt.splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                current_sample = line[1:].strip()
            elif line.startswith("K") and current_sample:
                records.append((current_sample, line))
        return records

    def test_validate_and_process_input_valid_txt_format(self, fasta_like_input_txt):
        """
        Test successful validation of valid FASTA-like txt input.

        Verifies that the function correctly processes valid input
        and returns a DataFrame with expected structure and content.
        """
        # Act
        df, error = validate_and_process_input(fasta_like_input_txt, "input.txt")

        # Assert
        assert error is None
        assert isinstance(df, pd.DataFrame)

        # Verify content matches expected records
        expected_records = self.extract_ko_records(fasta_like_input_txt)
        assert len(df) == len(expected_records)

        tuples_in_df = set(zip(df["sample"], df["ko"]))
        tuples_expected = set(expected_records)
        assert tuples_in_df == tuples_expected

    def test_validate_and_process_input_valid_base64_format(self, fasta_like_input_txt):
        """
        Test successful validation of valid base64 encoded input.

        Verifies that the function correctly processes base64
        encoded input and returns expected DataFrame structure.
        """
        # Arrange
        base64_bytes = base64.b64encode(fasta_like_input_txt.encode()).decode()
        encoded = f"data:text/plain;base64,{base64_bytes}"

        # Act
        df, error = validate_and_process_input(encoded, "input.txt")

        # Assert
        assert error is None
        assert isinstance(df, pd.DataFrame)

        # Verify content matches expected records
        expected_records = self.extract_ko_records(fasta_like_input_txt)
        assert len(df) == len(expected_records)

        tuples_in_df = set(zip(df["sample"], df["ko"]))
        tuples_expected = set(expected_records)
        assert tuples_in_df == tuples_expected

    def test_validate_and_process_input_invalid_extension_error(
        self, fasta_like_input_txt
    ):
        """
        Test error handling for invalid file extensions.

        Verifies that the function rejects files with unsupported
        extensions and returns appropriate error messages.
        """
        # Act
        df, error = validate_and_process_input(fasta_like_input_txt, "input.csv")

        # Assert
        assert df is None
        assert error is not None
        assert "invalid file type" in error.lower()

    def test_validate_and_process_input_bad_base64_error(self):
        """
        Test error handling for malformed base64 input.

        Verifies that the function handles invalid base64 encoding
        gracefully and returns appropriate error messages.
        """
        # Arrange
        bad = "data:text/plain;base64,@@@"

        # Act
        df, error = validate_and_process_input(bad, "input.txt")

        # Assert
        assert df is None
        assert error is not None

        # Accept any relevant error message
        error_l = error.lower()
        assert (
            "decode" in error_l
            or "could not decode" in error_l
            or "no valid sample" in error_l
            or "error" in error_l
        )

    def test_validate_and_process_input_invalid_line_format_error(self):
        """
        Test error handling for invalid line format.

        Verifies that the function rejects input with KO entries
        before any sample declaration.
        """
        # Arrange - KO before any sample
        bad_content = "K00001\n>SampleX\nK00002"

        # Act
        df, error = validate_and_process_input(bad_content, "input.txt")

        # Assert
        assert df is None
        assert error is not None
        assert "invalid format" in error.lower()

    def test_validate_and_process_input_empty_file_error(self):
        """
        Test error handling for empty input files.

        Verifies that the function handles empty input gracefully
        and returns appropriate error messages.
        """
        # Act
        df, error = validate_and_process_input("", "input.txt")

        # Assert
        assert df is None
        assert error is not None
        assert "no valid sample" in error.lower() or "no valid" in error.lower()

    def test_validate_and_process_input_sample_without_ko(self):
        """
        Test handling of samples without KO entries.

        Verifies that the function correctly processes input where
        some samples have no KO entries while others do.
        """
        # Arrange
        content = ">Sample1\n>Sample2\nK00005"

        # Act
        df, error = validate_and_process_input(content, "input.txt")

        # Assert
        assert error is None
        assert len(df) == 1
        assert df.iloc[0]["sample"] == "Sample2"
        assert df.iloc[0]["ko"] == "K00005"

    def test_validate_and_process_input_multiple_kos_per_sample(
        self, fasta_like_input_txt
    ):
        """
        Test handling of multiple KOs per sample.

        Verifies that the function correctly processes samples
        with multiple KO entries.
        """
        # Act
        df, error = validate_and_process_input(fasta_like_input_txt, "input.txt")

        # Assert
        assert error is None
        assert not df.empty

        # Verify that samples can have multiple KOs
        sample_counts = df["sample"].value_counts()
        assert any(count > 1 for count in sample_counts.values)

    def test_validate_and_process_input_whitespace_handling(self):
        """
        Test handling of whitespace in input.

        Verifies that the function correctly handles leading/trailing
        whitespace and empty lines.
        """
        # Arrange
        content_with_whitespace = (
            "  \n"
            "  >Sample1  \n"
            "  K00001  \n"
            "  \n"
            "  >Sample2  \n"
            "  K00002  \n"
            "  \n"
        )

        # Act
        df, error = validate_and_process_input(content_with_whitespace, "input.txt")

        # Assert
        assert error is None
        assert len(df) == 2
        assert "Sample1" in df["sample"].values
        assert "Sample2" in df["sample"].values
        assert "K00001" in df["ko"].values
        assert "K00002" in df["ko"].values

    def test_validate_and_process_input_special_characters_in_sample(self):
        """
        Test handling of special characters in sample names.

        Verifies that the function correctly handles sample names
        with special characters and numbers.
        """
        # Arrange
        content = ">Sample_123-A\nK00001\n>Sample@2\nK00002"

        # Act
        df, error = validate_and_process_input(content, "input.txt")

        # Assert
        assert error is None
        assert len(df) == 2
        assert "Sample_123-A" in df["sample"].values
        assert "Sample@2" in df["sample"].values

    def test_validate_and_process_input_case_sensitivity(self):
        """
        Test case sensitivity in KO identifiers.

        Verifies that the function enforces uppercase 'K' for
        KO identifiers and rejects lowercase variants.
        """
        # Arrange
        content = ">Sample1\nK00001\nk00002\n>Sample2\nK00003"

        # Act
        df, error = validate_and_process_input(content, "input.txt")

        # Assert
        # Function should reject lowercase 'k' in KO identifiers
        assert df is None
        assert error is not None
        assert "invalid format" in error.lower()

    def test_validate_and_process_input_large_dataset(self):
        """
        Test processing of large input datasets.

        Verifies that the function can handle larger datasets
        without performance issues.
        """
        # Arrange
        large_content = []
        for i in range(100):
            large_content.append(f">Sample{i}")
            for j in range(10):
                large_content.append(f"K{i:05d}{j:02d}")

        content = "\n".join(large_content)

        # Act
        df, error = validate_and_process_input(content, "input.txt")

        # Assert
        assert error is None
        assert len(df) == 1000  # 100 samples * 10 KOs each
        assert len(df["sample"].unique()) == 100

    def test_validate_and_process_input_duplicate_kos_in_sample(self):
        """
        Test handling of duplicate KOs within same sample.

        Verifies that the function correctly handles cases where
        the same KO appears multiple times in one sample.
        """
        # Arrange
        content = ">Sample1\nK00001\nK00001\nK00002"

        # Act
        df, error = validate_and_process_input(content, "input.txt")

        # Assert
        assert error is None
        # Should include duplicate KOs
        assert len(df) == 3
        ko_counts = df[df["sample"] == "Sample1"]["ko"].value_counts()
        assert ko_counts["K00001"] == 2
        assert ko_counts["K00002"] == 1
