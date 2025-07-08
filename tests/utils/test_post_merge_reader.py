"""
Tests for the PostMergeDataReader class.

This module contains comprehensive tests for the PostMergeDataReader,
including success cases, edge cases, and error handling.
"""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest

from biorempp.utils.post_merge_reader import PostMergeDataReader


class TestPostMergeDataReader:
    """Test suite for PostMergeDataReader class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Create a temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()
        self.reader = PostMergeDataReader(results_dir=self.temp_dir)

    def teardown_method(self):
        """Clean up after each test method."""
        # Clean up temporary files
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_test_file(self, filename: str, content: str):
        """Helper method to create test files."""
        filepath = Path(self.temp_dir) / filename
        with open(filepath, "w") as f:
            f.write(content)
        return filepath

    def _create_sample_dataframe_content(self, data_type: str = "biorempp"):
        """Helper method to create sample DataFrame content."""
        if data_type == "biorempp":
            return (
                "sample;ko;genesymbol;genename;cpd;compoundclass;"
                "referenceAG;compoundname;enzyme_activity\n"
                "Sample1;K00001;GST;glutathione S-transferase;C00001;"
                "Chlorinated;WFD;Test compound 1;transferase\n"
                "Sample1;K00002;OXD;oxidase enzyme;C00002;"
                "Aromatic;EPC;Test compound 2;oxidase\n"
                "Sample2;K00003;HYD;hydrolase enzyme;C00003;"
                "Alkane;CONAMA;Test compound 3;hydrolase\n"
            )
        elif data_type == "hadeg":
            return (
                "sample;ko;Gene;Pathway;compound_pathway\n"
                "Sample1;K00001;isoI;B_Isoprene_degradation;Alkenes\n"
                "Sample1;K00002;xamoF;B_Propene_degradation;Alkenes\n"
            )
        elif data_type == "kegg":
            return (
                "sample;ko;pathname;genesymbol\n"
                "Sample1;K00001;Cytochrome P450;GST\n"
                "Sample1;K00002;Toluene;E3.1.1.45\n"
            )
        elif data_type == "toxcsm":
            return (
                "sample;ko;genesymbol;genename;cpd;compoundclass;"
                "referenceAG;compoundname;enzyme_activity;SMILES;"
                "ChEBI;value_NR_AR;label_NR_AR\n"
                "Sample1;K00001;GST;glutathione S-transferase;C00001;"
                "Chlorinated;WFD;Achlor;transferase;CCc1cccc(CC)c1;"
                "2533;0.0;High Safety\n"
                "Sample1;K00002;OXD;oxidase enzyme;C00002;"
                "Aromatic;EPC;Benzene;oxidase;c1ccccc1;241;"
                "0.5;Low Toxicity\n"
            )

    def test_init_default_results_dir(self):
        """Test initialization with default results directory."""
        reader = PostMergeDataReader()
        assert reader.results_dir.name == "results_table"
        assert "outputs" in str(reader.results_dir)

    def test_init_custom_results_dir(self):
        """Test initialization with custom results directory."""
        custom_dir = "\\custom\\path"  # Windows path format
        reader = PostMergeDataReader(results_dir=custom_dir)
        assert str(reader.results_dir) == custom_dir

    def test_file_prefixes_mapping(self):
        """Test that file prefixes are correctly mapped."""
        expected_prefixes = {
            "biorempp": "BioRemPP_Results_",
            "hadeg": "HADEG_Results_",
            "kegg": "KEGG_Results_",
            "toxcsm": "ToxCSM_",
        }
        assert self.reader.file_prefixes == expected_prefixes

    def test_load_latest_biorempp_success(self):
        """Test successful loading of latest BioRemPP file."""
        # Create test files with different timestamps
        content = self._create_sample_dataframe_content("biorempp")
        self._create_test_file("BioRemPP_Results_20240101_120000.txt", content)
        self._create_test_file("BioRemPP_Results_20240102_120000.txt", content)

        # Load the latest file
        df = self.reader.load_latest("biorempp")

        # Verify DataFrame content
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert "ko" in df.columns
        assert "sample" in df.columns
        assert len(df) == 3

    def test_load_latest_hadeg_success(self):
        """Test successful loading of latest HADEG file."""
        content = self._create_sample_dataframe_content("hadeg")
        self._create_test_file("HADEG_Results_20240101_120000.txt", content)

        df = self.reader.load_latest("hadeg")

        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert "ko" in df.columns
        assert "sample" in df.columns

    def test_load_latest_kegg_success(self):
        """Test successful loading of latest KEGG file."""
        content = self._create_sample_dataframe_content("kegg")
        self._create_test_file("KEGG_Results_20240101_120000.txt", content)

        df = self.reader.load_latest("kegg")

        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert "ko" in df.columns
        assert "sample" in df.columns

    def test_load_latest_toxcsm_success(self):
        """Test successful loading of latest ToxCSM file."""
        content = self._create_sample_dataframe_content("toxcsm")
        self._create_test_file("ToxCSM_20240101_120000.txt", content)

        df = self.reader.load_latest("toxcsm")

        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert "ko" in df.columns
        assert "sample" in df.columns

    def test_load_latest_selects_most_recent(self):
        """Test that load_latest selects the most recent file."""
        content_old = self._create_sample_dataframe_content("biorempp")
        content_new = (
            "sample;ko;genesymbol;genename;cpd;compoundclass;"
            "referenceAG;compoundname;enzyme_activity\n"
            "Sample3;K00004;NEW;new enzyme;C00004;"
            "New_class;NEW_REF;Newest compound;new_activity\n"
        )

        # Create files with different timestamps
        self._create_test_file("BioRemPP_Results_20240101_120000.txt", content_old)
        self._create_test_file("BioRemPP_Results_20240103_120000.txt", content_new)

        df = self.reader.load_latest("biorempp")

        # Should load the newer file
        assert len(df) == 1
        assert df.iloc[0]["ko"] == "K00004"

    def test_load_latest_file_not_found(self):
        """Test error handling when no files are found."""
        with pytest.raises(FileNotFoundError) as exc_info:
            self.reader.load_latest("biorempp")

        assert "No biorempp files found" in str(exc_info.value)

    def test_load_latest_unsupported_data_type(self):
        """Test error handling for unsupported data types."""
        with pytest.raises(ValueError) as exc_info:
            self.reader.load_latest("unsupported")

        assert "Unsupported data_type: unsupported" in str(exc_info.value)

    def test_load_latest_empty_file(self):
        """Test error handling for empty files."""
        self._create_test_file("BioRemPP_Results_20240101_120000.txt", "")

        with pytest.raises(ValueError) as exc_info:
            self.reader.load_latest("biorempp")

        assert "empty or malformed" in str(exc_info.value)

    def test_load_latest_malformed_file(self):
        """Test error handling for malformed files."""
        malformed_content = "This is not a valid CSV file content"
        self._create_test_file(
            "BioRemPP_Results_20240101_120000.txt", malformed_content
        )

        with pytest.raises(ValueError) as exc_info:
            self.reader.load_latest("biorempp")

        # Should catch parsing errors or empty DataFrame errors
        error_message = str(exc_info.value)
        assert (
            "empty or malformed" in error_message
            or "Error parsing file" in error_message
            or "DataFrame for biorempp is empty" in error_message
        )

    def test_load_latest_file_without_expected_columns(self):
        """Test loading file without expected columns (should warn but not fail)."""
        content_no_expected_cols = "Custom_Column1;Custom_Column2\n" "Value1;Value2\n"
        self._create_test_file(
            "BioRemPP_Results_20240101_120000.txt", content_no_expected_cols
        )

        # Should still load successfully but log warning
        df = self.reader.load_latest("biorempp")

        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert "Custom_Column1" in df.columns

    def test_find_latest_file_method(self):
        """Test the _find_latest_file method directly."""
        content = self._create_sample_dataframe_content("biorempp")
        self._create_test_file("BioRemPP_Results_20240101_120000.txt", content)
        self._create_test_file("BioRemPP_Results_20240103_120000.txt", content)

        latest_file = self.reader._find_latest_file("biorempp")

        assert latest_file is not None
        assert "20240103_120000" in latest_file.name

    def test_find_latest_file_no_files(self):
        """Test _find_latest_file when no files exist."""
        latest_file = self.reader._find_latest_file("biorempp")
        assert latest_file is None

    def test_validate_dataframe_empty(self):
        """Test DataFrame validation with empty DataFrame."""
        empty_df = pd.DataFrame()

        with pytest.raises(ValueError) as exc_info:
            self.reader._validate_dataframe(empty_df, "biorempp")

        assert "DataFrame for biorempp is empty" in str(exc_info.value)

    def test_validate_dataframe_missing_columns(self):
        """Test DataFrame validation with missing expected columns."""
        df_missing_cols = pd.DataFrame({"Other_Column": ["value1", "value2"]})

        # Should not raise error, just log warning
        self.reader._validate_dataframe(df_missing_cols, "biorempp")

    def test_list_available_files_empty(self):
        """Test listing available files when directory is empty."""
        available_files = self.reader.list_available_files()

        expected_keys = ["biorempp", "hadeg", "kegg", "toxcsm"]
        assert all(key in available_files for key in expected_keys)
        assert all(len(files) == 0 for files in available_files.values())

    def test_list_available_files_with_files(self):
        """Test listing available files when files exist."""
        # Create test files
        content = self._create_sample_dataframe_content("biorempp")
        self._create_test_file("BioRemPP_Results_20240101_120000.txt", content)
        self._create_test_file("BioRemPP_Results_20240102_120000.txt", content)

        content_hadeg = self._create_sample_dataframe_content("hadeg")
        self._create_test_file("HADEG_Results_20240101_120000.txt", content_hadeg)

        available_files = self.reader.list_available_files()

        assert len(available_files["biorempp"]) == 2
        assert len(available_files["hadeg"]) == 1
        assert len(available_files["kegg"]) == 0
        assert len(available_files["toxcsm"]) == 0

        # Check that files are sorted by timestamp (most recent first)
        biorempp_files = available_files["biorempp"]
        assert biorempp_files[0] == "BioRemPP_Results_20240102_120000.txt"
        assert biorempp_files[1] == "BioRemPP_Results_20240101_120000.txt"

    def test_case_insensitive_data_type(self):
        """Test that data_type parameter is case-insensitive."""
        content = self._create_sample_dataframe_content("biorempp")
        self._create_test_file("BioRemPP_Results_20240101_120000.txt", content)

        # Test different cases
        df1 = self.reader.load_latest("BIOREMPP")
        df2 = self.reader.load_latest("BioRemPP")
        df3 = self.reader.load_latest("biorempp")

        assert len(df1) == len(df2) == len(df3) == 3

    @patch("biorempp.utils.post_merge_reader.logger")
    def test_logging_behavior(self, mock_logger):
        """Test that appropriate logging occurs."""
        content = self._create_sample_dataframe_content("biorempp")
        self._create_test_file("BioRemPP_Results_20240101_120000.txt", content)

        self.reader.load_latest("biorempp")

        # Verify that logging methods were called
        mock_logger.info.assert_called()
        mock_logger.debug.assert_called()

    def test_timestamp_extraction_edge_cases(self):
        """Test timestamp extraction with various filename patterns."""
        content = self._create_sample_dataframe_content("biorempp")

        # Create files with different timestamp patterns
        self._create_test_file("BioRemPP_Results_20240101_120000.txt", content)
        self._create_test_file("BioRemPP_Results_20240101_120001.txt", content)
        self._create_test_file("BioRemPP_Results_invalid_timestamp.txt", content)

        df = self.reader.load_latest("biorempp")

        # Should load the file with the latest valid timestamp
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    def test_file_permissions_error(self):
        """Test handling of file permission errors."""
        content = self._create_sample_dataframe_content("biorempp")
        self._create_test_file("BioRemPP_Results_20240101_120000.txt", content)

        # Mock file permission error
        with patch("pandas.read_csv") as mock_read_csv:
            mock_read_csv.side_effect = PermissionError("Permission denied")

            with pytest.raises(PermissionError):
                self.reader.load_latest("biorempp")

    def test_integration_with_real_project_structure(self):
        """Test integration with real project directory structure."""
        # This test uses the default constructor to test real project paths
        reader = PostMergeDataReader()

        # Check that the default path exists or can be created
        assert reader.results_dir.parent.name == "outputs"

        # Test that list_available_files works with real structure
        available_files = reader.list_available_files()
        assert isinstance(available_files, dict)
        assert all(isinstance(files, list) for files in available_files.values())


if __name__ == "__main__":
    pytest.main([__file__])
