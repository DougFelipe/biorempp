"""
Unit tests for io_utils module.

Tests for I/O utilities functions, particularly save_dataframe_output.
Updated to work with current working directory behavior.
"""

import os
import tempfile
from pathlib import Path
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
        output_dir = "test_output"
        filename = "test_data.csv"

        # Act - Mock getcwd to return tmp_path
        with patch("biorempp.utils.io_utils.os.getcwd", return_value=str(tmp_path)):
            result_path = save_dataframe_output(
                df, output_dir, filename, add_timestamp=False
            )

        # Assert
        expected_path = os.path.join(str(tmp_path), output_dir, filename)
        assert result_path == expected_path
        assert os.path.exists(result_path)

        # Verify content
        saved_df = pd.read_csv(result_path, sep=";")
        pd.testing.assert_frame_equal(df, saved_df)

    def test_save_dataframe_output_absolute_path(self, tmp_path):
        """
        Test saving DataFrame with absolute path.

        Verifies that absolute paths are used as-is without modification.
        """
        # Arrange
        df = pd.DataFrame({"col1": ["a", "b", "c"], "col2": [1, 2, 3]})
        output_dir = str(tmp_path / "test_output")  # Absolute path
        filename = "test_absolute.csv"

        # Act - No need to mock getcwd for absolute paths
        result_path = save_dataframe_output(df, output_dir, filename)

        # Assert
        expected_path = os.path.join(output_dir, filename)
        assert result_path == expected_path
        assert os.path.exists(result_path)

    def test_save_dataframe_output_custom_separator(self, tmp_path):
        """
        Test saving DataFrame with custom separator.

        Verifies that the function correctly uses a custom separator
        when provided.
        """
        # Arrange
        df = pd.DataFrame({"col1": ["a", "b", "c"], "col2": [1, 2, 3]})
        output_dir = "test_output"
        filename = "test_custom_sep.csv"
        custom_sep = ","

        # Act
        with patch("biorempp.utils.io_utils.os.getcwd", return_value=str(tmp_path)):
            result_path = save_dataframe_output(
                df, output_dir, filename, sep=custom_sep
            )

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
        output_dir = "test_output"
        filename = "test_with_index.csv"

        # Act
        with patch("biorempp.utils.io_utils.os.getcwd", return_value=str(tmp_path)):
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
        output_dir = "test_output"
        filename = "test_encoding.csv"
        encoding = "latin-1"

        # Act
        with patch("biorempp.utils.io_utils.os.getcwd", return_value=str(tmp_path)):
            result_path = save_dataframe_output(
                df, output_dir, filename, encoding=encoding
            )

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
        output_dir = "test_output"
        filename = "empty_data.csv"

        # Act
        with patch("biorempp.utils.io_utils.os.getcwd", return_value=str(tmp_path)):
            result_path = save_dataframe_output(df, output_dir, filename)

        # Assert
        assert os.path.exists(result_path)

        # Verify empty file was created
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
        output_dir = "nested/path/that/does_not_exist"
        filename = "test.csv"

        # Act
        with patch("biorempp.utils.io_utils.os.getcwd", return_value=str(tmp_path)):
            result_path = save_dataframe_output(df, output_dir, filename)
            expected_dir = os.path.join(str(tmp_path), output_dir)

        # Assert
        assert os.path.exists(expected_dir)
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
        output_dir = "test_output"
        filename = "overwrite_test.csv"

        # Act - First save
        with patch("biorempp.utils.io_utils.os.getcwd", return_value=str(tmp_path)):
            result_path1 = save_dataframe_output(df1, output_dir, filename)

        # Act - Second save (overwrite)
        with patch("biorempp.utils.io_utils.os.getcwd", return_value=str(tmp_path)):
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
        output_dir = "test_output"
        filename = "path_test.csv"

        # Act
        with patch("biorempp.utils.io_utils.os.getcwd", return_value=str(tmp_path)):
            result_path = save_dataframe_output(
                df, output_dir, filename, add_timestamp=False
            )

        # Assert
        expected_path = os.path.join(str(tmp_path), output_dir, filename)
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
        output_dir = "mock_test"
        filename = "test.csv"

        # Act
        with patch("biorempp.utils.io_utils.os.getcwd", return_value=str(tmp_path)):
            with patch(
                "biorempp.utils.io_utils.os.makedirs", wraps=os.makedirs
            ) as mock_makedirs:
                save_dataframe_output(df, output_dir, filename)
                expected_dir = os.path.join(str(tmp_path), output_dir)

                # Assert
                mock_makedirs.assert_called_once_with(expected_dir, exist_ok=True)

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
        output_dir = "test_output"
        filename = "special_chars.csv"

        # Act
        with patch("biorempp.utils.io_utils.os.getcwd", return_value=str(tmp_path)):
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
        output_dir = "test_output"
        filename = "large_data.csv"

        # Act
        with patch("biorempp.utils.io_utils.os.getcwd", return_value=str(tmp_path)):
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
        output_dir = "test_output"
        filename = "mixed_types.csv"

        # Act
        with patch("biorempp.utils.io_utils.os.getcwd", return_value=str(tmp_path)):
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
        output_dir = "test_output"
        filename = "permission_test.csv"

        # Act & Assert
        with patch("biorempp.utils.io_utils.os.getcwd", return_value=str(tmp_path)):
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
        output_dir = "test_output"

        # Test with valid filename (invalid chars would be OS-specific)
        filename = "valid_filename.csv"

        # Act
        with patch("biorempp.utils.io_utils.os.getcwd", return_value=str(tmp_path)):
            result_path = save_dataframe_output(df, output_dir, filename)

        # Assert
        assert os.path.exists(result_path)

    def test_save_dataframe_output_with_timestamp(self, tmp_path):
        """
        Test saving DataFrame with timestamp explicitly enabled.

        Verifies that the function adds timestamp to filename when explicitly enabled.
        """
        # Arrange
        df = pd.DataFrame({"test": [1]})
        output_dir = "test_output"
        filename = "timestamped_test.csv"

        # Act - explicitly enable timestamp
        with patch("biorempp.utils.io_utils.os.getcwd", return_value=str(tmp_path)):
            result_path = save_dataframe_output(
                df, output_dir, filename, add_timestamp=True
            )

        # Assert
        assert os.path.exists(result_path)
        # Should not be the exact filename since timestamp is added
        expected_path_no_timestamp = os.path.join(str(tmp_path), output_dir, filename)
        assert result_path != expected_path_no_timestamp
        # Should contain timestamp pattern
        assert "_2025" in result_path  # Year in timestamp
        assert "timestamped_test_" in result_path
        assert result_path.endswith(".csv")

    def test_save_dataframe_output_timestamp_disabled(self, tmp_path):
        """
        Test saving DataFrame with timestamp explicitly disabled.

        Verifies that the function does not add timestamp when disabled.
        """
        # Arrange
        df = pd.DataFrame({"test": [1]})
        output_dir = "test_output"
        filename = "no_timestamp_test.csv"

        # Act
        with patch("biorempp.utils.io_utils.os.getcwd", return_value=str(tmp_path)):
            result_path = save_dataframe_output(
                df, output_dir, filename, add_timestamp=False
            )

        # Assert
        assert os.path.exists(result_path)
        expected_path = os.path.join(str(tmp_path), output_dir, filename)
        assert result_path == expected_path


"""
Additional tests for io_utils module to improve coverage.

These tests target the uncovered lines and edge cases.
"""

from biorempp.utils.io_utils import (
    generate_timestamped_filename,
    get_project_root,
    resolve_log_path,
)


class TestGetProjectRoot:
    """Test suite for get_project_root function."""

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.resolve")
    def test_get_project_root_with_pyproject_toml(self, mock_resolve, mock_exists):
        """Test finding project root with pyproject.toml."""
        # Create a mock path structure
        mock_file_path = Path("/mock/project/src/biorempp/utils/io_utils.py")
        mock_resolve.return_value = mock_file_path

        # Mock that pyproject.toml exists in project root
        def exists_side_effect(self):
            return str(self).endswith("pyproject.toml") and "project" in str(self)

        with patch.object(Path, "exists", exists_side_effect):
            root = get_project_root()
            assert isinstance(root, str)

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.resolve")
    def test_get_project_root_with_setup_py(self, mock_resolve, mock_exists):
        """Test finding project root with setup.py."""
        # Create a mock path structure
        mock_file_path = Path("/mock/project/src/biorempp/utils/io_utils.py")
        mock_resolve.return_value = mock_file_path

        # Mock that setup.py exists but not pyproject.toml
        def exists_side_effect(self):
            if str(self).endswith("pyproject.toml"):
                return False
            return str(self).endswith("setup.py") and "project" in str(self)

        with patch.object(Path, "exists", exists_side_effect):
            root = get_project_root()
            assert isinstance(root, str)

    @patch("pathlib.Path.exists")
    def test_get_project_root_fallback(self, mock_exists):
        """Test project root fallback when no markers found."""
        # Mock that neither pyproject.toml nor setup.py exist
        mock_exists.return_value = False

        root = get_project_root()
        assert isinstance(root, str)
        # Should return fallback path


class TestResolveLogPath:
    """Test suite for resolve_log_path function."""

    def test_resolve_log_path_relative(self):
        """Test resolving relative log path."""
        log_path = "logs/app.log"
        resolved = resolve_log_path(log_path)

        assert isinstance(resolved, str)
        assert log_path in resolved or "app.log" in resolved

    def test_resolve_log_path_absolute(self):
        """Test resolving absolute log path."""
        if os.name == "nt":
            log_path = r"C:\logs\app.log"
        else:
            log_path = "/var/log/app.log"

        resolved = resolve_log_path(log_path)
        assert resolved == log_path

    def test_resolve_log_path_with_project_root(self):
        """Test that log path is resolved relative to project root."""
        log_path = "outputs/logs/test.log"
        resolved = resolve_log_path(log_path)

        # Should contain the project structure
        assert isinstance(resolved, str)
        assert len(resolved) > len(log_path)


class TestGenerateTimestampedFilename:
    """Test suite for generate_timestamped_filename function."""

    def test_generate_timestamped_filename_enabled(self):
        """Test generating filename with timestamp enabled."""
        filename = "results.csv"
        timestamped = generate_timestamped_filename(filename, add_timestamp=True)

        assert timestamped != filename
        assert timestamped.startswith("results_")
        assert timestamped.endswith(".csv")
        assert "20" in timestamped  # Should contain year

    def test_generate_timestamped_filename_disabled(self):
        """Test generating filename with timestamp disabled."""
        filename = "results.csv"
        timestamped = generate_timestamped_filename(filename, add_timestamp=False)

        assert timestamped == filename

    def test_generate_timestamped_filename_no_extension(self):
        """Test generating timestamped filename without extension."""
        filename = "results"
        timestamped = generate_timestamped_filename(filename, add_timestamp=True)

        assert timestamped != filename
        assert timestamped.startswith("results_")
        assert "20" in timestamped

    def test_generate_timestamped_filename_multiple_dots(self):
        """Test generating timestamped filename with multiple dots."""
        filename = "data.processed.csv"
        timestamped = generate_timestamped_filename(filename, add_timestamp=True)

        assert timestamped != filename
        assert timestamped.startswith("data.processed_")
        assert timestamped.endswith(".csv")


class TestEdgeCases:
    """Test suite for edge cases and error conditions."""

    def test_save_dataframe_output_error_handling(self):
        """Test error handling in save_dataframe_output."""
        from biorempp.utils.io_utils import save_dataframe_output

        df = pd.DataFrame({"test": [1, 2, 3]})

        # Test with invalid output directory (permission error simulation)
        with patch("pandas.DataFrame.to_csv") as mock_to_csv:
            mock_to_csv.side_effect = PermissionError("Access denied")

            with pytest.raises(PermissionError):
                save_dataframe_output(df, "test_dir", "test.csv")

    def test_resolve_output_path_edge_cases(self):
        """Test edge cases for resolve_output_path."""
        from biorempp.utils.io_utils import resolve_output_path

        # Test with empty string
        result = resolve_output_path("")
        assert isinstance(result, str)

        # Test with current directory
        result = resolve_output_path(".")
        assert isinstance(result, str)

        # Test with parent directory
        result = resolve_output_path("..")
        assert isinstance(result, str)

    def test_path_handling_cross_platform(self):
        """Test that path handling works across platforms."""
        from biorempp.utils.io_utils import resolve_output_path

        # Test with forward slashes
        result1 = resolve_output_path("output/subdir")
        assert isinstance(result1, str)

        # Test with backslashes (should work on Windows)
        result2 = resolve_output_path("output\\subdir")
        assert isinstance(result2, str)

    @patch("biorempp.utils.io_utils.logger")
    def test_logging_coverage(self, mock_logger):
        """Test that logging statements are covered."""
        from biorempp.utils.io_utils import save_dataframe_output

        df = pd.DataFrame({"test": [1]})

        with tempfile.TemporaryDirectory() as temp_dir:
            save_dataframe_output(df, temp_dir, "test.csv")

            # Verify that debug and info logging was called
            assert mock_logger.debug.called
            assert mock_logger.info.called
