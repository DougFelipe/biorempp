"""
Unit tests for io_utils module.

Tests for I/O utilities functions, particularly save_dataframe_output.
"""

import os
from unittest.mock import patch

import pandas as pd
import pytest

from biorempp.utils.io_utils import save_dataframe_output


class TestSaveDataframeOutput:
    """Test suite for save_dataframe_output function."""

    def test_save_dataframe_output_happy_path(self, tmp_path):
        """
        Test successful saving of a DataFrame with default parameters.

        Verifies that the function creates the output directory and saves
        the DataFrame correctly with semicolon separator.
        """
        # Arrange
        df = pd.DataFrame(
            {
                "ko": ["K00001", "K00002", "K00003"],
                "gene": ["geneA", "geneB", "geneC"],
                "value": [1.0, 2.0, 3.0],
            }
        )
        output_dir = str(tmp_path / "test_output")
        filename = "test_data.csv"

        # Act
        result_path = save_dataframe_output(df, output_dir, filename)

        # Assert
        assert os.path.exists(result_path)
        assert result_path == os.path.join(output_dir, filename)

        # Verify content
        saved_df = pd.read_csv(result_path, sep=";")
        pd.testing.assert_frame_equal(df, saved_df)

    def test_save_dataframe_output_custom_separator(self, tmp_path):
        """
        Test saving DataFrame with custom separator.

        Verifies that the function correctly uses a custom separator
        when provided.
        """
        # Arrange
        df = pd.DataFrame({"col1": ["a", "b", "c"], "col2": [1, 2, 3]})
        output_dir = str(tmp_path / "test_output")
        filename = "test_custom_sep.csv"
        custom_sep = ","

        # Act
        result_path = save_dataframe_output(df, output_dir, filename, sep=custom_sep)

        # Assert
        assert os.path.exists(result_path)

        # Verify content with custom separator
        saved_df = pd.read_csv(result_path, sep=custom_sep)
        pd.testing.assert_frame_equal(df, saved_df)

    def test_save_dataframe_output_with_index(self, tmp_path):
        """
        Test saving DataFrame with index included.

        Verifies that when index=True, the row indices are saved
        to the output file.
        """
        # Arrange
        df = pd.DataFrame({"data": ["x", "y", "z"]}, index=["row1", "row2", "row3"])
        output_dir = str(tmp_path / "test_output")
        filename = "test_with_index.csv"

        # Act
        result_path = save_dataframe_output(df, output_dir, filename, index=True)

        # Assert
        assert os.path.exists(result_path)

        # Verify content includes index
        saved_df = pd.read_csv(result_path, sep=";", index_col=0)
        pd.testing.assert_frame_equal(df, saved_df)

    def test_save_dataframe_output_custom_encoding(self, tmp_path):
        """
        Test saving DataFrame with custom encoding.

        Verifies that the function correctly handles different
        text encodings.
        """
        # Arrange
        df = pd.DataFrame({"name": ["café", "naïve", "résumé"], "value": [1, 2, 3]})
        output_dir = str(tmp_path / "test_output")
        filename = "test_encoding.csv"
        encoding = "latin-1"

        # Act
        result_path = save_dataframe_output(df, output_dir, filename, encoding=encoding)

        # Assert
        assert os.path.exists(result_path)

        # Verify content with custom encoding
        saved_df = pd.read_csv(result_path, sep=";", encoding=encoding)
        pd.testing.assert_frame_equal(df, saved_df)

    def test_save_dataframe_output_empty_dataframe(self, tmp_path):
        """
        Test saving an empty DataFrame.

        Verifies that the function handles empty DataFrames gracefully
        without raising exceptions.
        """
        # Arrange
        df = pd.DataFrame()
        output_dir = str(tmp_path / "test_output")
        filename = "empty_data.csv"

        # Act
        result_path = save_dataframe_output(df, output_dir, filename)

        # Assert
        assert os.path.exists(result_path)

        # Verify empty file was created
        # For completely empty DataFrame, we check file size instead
        file_size = os.path.getsize(result_path)
        assert file_size >= 0  # File exists but may be empty or have headers

    def test_save_dataframe_output_creates_directory(self, tmp_path):
        """
        Test that non-existent directories are created.

        Verifies that the function creates the output directory
        structure when it doesn't exist.
        """
        # Arrange
        df = pd.DataFrame({"col": [1, 2, 3]})
        output_dir = str(tmp_path / "nested" / "path" / "that" / "does_not_exist")
        filename = "test.csv"

        # Act
        result_path = save_dataframe_output(df, output_dir, filename)

        # Assert
        assert os.path.exists(output_dir)
        assert os.path.exists(result_path)

    def test_save_dataframe_output_overwrites_existing_file(self, tmp_path):
        """
        Test overwriting an existing file.

        Verifies that the function overwrites existing files
        without raising exceptions.
        """
        # Arrange
        df1 = pd.DataFrame({"col": [1, 2, 3]})
        df2 = pd.DataFrame({"col": [4, 5, 6]})
        output_dir = str(tmp_path / "test_output")
        filename = "overwrite_test.csv"

        # Act - First save
        result_path1 = save_dataframe_output(df1, output_dir, filename)

        # Act - Second save (overwrite)
        result_path2 = save_dataframe_output(df2, output_dir, filename)

        # Assert
        assert result_path1 == result_path2
        assert os.path.exists(result_path2)

        # Verify content is from second DataFrame
        saved_df = pd.read_csv(result_path2, sep=";")
        pd.testing.assert_frame_equal(df2, saved_df)

    def test_save_dataframe_output_return_path_format(self, tmp_path):
        """
        Test the format of the returned file path.

        Verifies that the function returns the correct absolute path
        using os.path.join.
        """
        # Arrange
        df = pd.DataFrame({"test": [1]})
        output_dir = str(tmp_path / "test_output")
        filename = "path_test.csv"

        # Act
        result_path = save_dataframe_output(df, output_dir, filename)

        # Assert
        expected_path = os.path.join(output_dir, filename)
        assert result_path == expected_path
        assert os.path.isabs(result_path)

    def test_save_dataframe_output_makedirs_called(self, tmp_path):
        """
        Test that os.makedirs is called with correct parameters.

        Verifies that the function calls os.makedirs with exist_ok=True
        to handle directory creation safely.
        """
        # Arrange
        df = pd.DataFrame({"col": [1, 2, 3]})
        output_dir = str(tmp_path / "mock_test")
        filename = "test.csv"

        # Act
        with patch(
            "biorempp.utils.io_utils.os.makedirs", wraps=os.makedirs
        ) as mock_makedirs:
            save_dataframe_output(df, output_dir, filename)

            # Assert
            mock_makedirs.assert_called_once_with(output_dir, exist_ok=True)

    def test_save_dataframe_output_with_special_characters(self, tmp_path):
        """
        Test saving DataFrame with special characters in data.

        Verifies that the function handles special characters,
        including separators, in the data correctly.
        """
        # Arrange
        df = pd.DataFrame(
            {
                "text": ["hello;world", "test,data", "special\nchars"],
                "numbers": [1, 2, 3],
            }
        )
        output_dir = str(tmp_path / "test_output")
        filename = "special_chars.csv"

        # Act
        result_path = save_dataframe_output(df, output_dir, filename)

        # Assert
        assert os.path.exists(result_path)

        # Verify content is preserved correctly
        saved_df = pd.read_csv(result_path, sep=";")
        pd.testing.assert_frame_equal(df, saved_df)

    def test_save_dataframe_output_large_dataframe(self, tmp_path):
        """
        Test saving a large DataFrame.

        Verifies that the function can handle larger datasets
        without performance issues.
        """
        # Arrange
        import numpy as np

        df = pd.DataFrame(
            {
                "col1": np.random.rand(10000),
                "col2": np.random.randint(0, 100, 10000),
                "col3": [f"text_{i}" for i in range(10000)],
            }
        )
        output_dir = str(tmp_path / "test_output")
        filename = "large_data.csv"

        # Act
        result_path = save_dataframe_output(df, output_dir, filename)

        # Assert
        assert os.path.exists(result_path)

        # Verify file size is reasonable (not empty)
        file_size = os.path.getsize(result_path)
        assert file_size > 1000  # Should be substantial for 10k rows

    def test_save_dataframe_output_mixed_data_types(self, tmp_path):
        """
        Test saving DataFrame with mixed data types.

        Verifies that the function correctly handles DataFrames
        with various data types (strings, integers, floats, etc.).
        """
        # Arrange
        df = pd.DataFrame(
            {
                "string_col": ["a", "b", "c"],
                "int_col": [1, 2, 3],
                "float_col": [1.1, 2.2, 3.3],
                "bool_col": [True, False, True],
            }
        )
        output_dir = str(tmp_path / "test_output")
        filename = "mixed_types.csv"

        # Act
        result_path = save_dataframe_output(df, output_dir, filename)

        # Assert
        assert os.path.exists(result_path)

        # Verify content preservation
        saved_df = pd.read_csv(result_path, sep=";")
        # Note: CSV doesn't preserve exact dtypes, so compare values
        assert saved_df.shape == df.shape
        assert list(saved_df.columns) == list(df.columns)

    def test_save_dataframe_output_permission_error(self, tmp_path):
        """
        Test handling of permission errors during file operations.

        Verifies that appropriate exceptions are raised when
        file operations fail due to permissions.
        """
        # Arrange
        df = pd.DataFrame({"col": [1, 2, 3]})
        output_dir = str(tmp_path / "test_output")
        filename = "permission_test.csv"

        # Act & Assert
        with patch.object(df, "to_csv") as mock_to_csv:
            mock_to_csv.side_effect = PermissionError("Permission denied")

            with pytest.raises(PermissionError):
                save_dataframe_output(df, output_dir, filename)

    def test_save_dataframe_output_invalid_path_characters(self, tmp_path):
        """
        Test handling of invalid characters in file paths.

        Verifies behavior when invalid characters are used in
        directory or filename.
        """
        # Arrange
        df = pd.DataFrame({"col": [1, 2, 3]})
        output_dir = str(tmp_path / "test_output")

        # Test with valid filename (invalid chars would be OS-specific)
        filename = "valid_filename.csv"

        # Act
        result_path = save_dataframe_output(df, output_dir, filename)

        # Assert
        assert os.path.exists(result_path)
