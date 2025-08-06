"""
Unit tests for SampleCompoundInteractionProcessor.

This module contains comprehensive tests for the sample compound interaction
processing functionality in BioRemPP, using fixtures from conftest.py.
"""

import os
import tempfile
from unittest.mock import patch

import pandas as pd
import pytest

from biorempp.analysis.sample_compound_interaction_processing import (
    SampleCompoundInteraction,
)


class TestSampleCompoundInteractionProcessor:
    """Test cases for SampleCompoundInteractionProcessor using pytest fixtures."""

    def test_init(self):
        """Test proper initialization of the processor."""
        processor = SampleCompoundInteraction()

        assert processor.name == "sample_compound_interaction_processor"
        assert processor.description is not None
        assert processor.output_dir == "outputs/entities_interactions"
        assert processor.output_file == "sample_compound_interaction.txt"

        # Check if output directory was created
        assert os.path.exists(processor.output_dir)

    def test_required_columns(self):
        """Test that required columns are correctly specified."""
        processor = SampleCompoundInteraction()
        expected_columns = ["sample", "compoundname", "compoundclass"]
        assert processor.required_columns == expected_columns

    def test_output_columns(self):
        """Test that output columns are correctly specified."""
        processor = SampleCompoundInteraction()
        expected_columns = ["sample", "compoundname", "compoundclass"]
        assert processor.output_columns == expected_columns

    def test_create_sample_compound_data_fixture(self):
        """Test creating sample data fixture for validation."""
        # Create test data that mimics merged BioRemPP data with compound info
        data = [
            # Sample1 interactions
            ["Sample1", "Thioacetamide", "Nitrogen-containing"],
            ["Sample1", "Lead", "Metal"],
            ["Sample1", "Methyl tert-butyl ether", "Aliphatic"],
            ["Sample1", "Acetaldehyde", "Aliphatic"],
            ["Sample1", "Phenobarbital", "Nitrogen-containing"],
            # Sample2 interactions
            ["Sample2", "Zinc cation", "Metal"],
            ["Sample2", "Some Compound", "Aliphatic"],
            ["Sample2", "alpha-Chlorohydrin", "Aliphatic"],
            # Sample3 interactions
            ["Sample3", "Phenytoin", "Nitrogen-containing"],
            ["Sample3", "Mercuric chloride", "Metal"],
            # Duplicates to test deduplication
            ["Sample1", "Thioacetamide", "Nitrogen-containing"],  # Duplicate
            ["Sample2", "Zinc cation", "Metal"],  # Duplicate
        ]

        columns = ["sample", "compoundname", "compoundclass"]
        test_df = pd.DataFrame(data, columns=columns)

        # Verify the fixture has expected structure
        assert not test_df.empty
        assert list(test_df.columns) == columns
        assert len(test_df) == 12  # 10 unique + 2 duplicates

    def test_validate_input_data_valid(self):
        """Test validation with valid input data."""
        processor = SampleCompoundInteraction()
        test_data = self.test_create_sample_compound_data_fixture()

        assert processor._validate_input_data(test_data) is True

    def test_validate_input_data_empty(self):
        """Test validation with empty DataFrame."""
        processor = SampleCompoundInteraction()
        empty_df = pd.DataFrame()

        with patch.object(processor.logger, "warning") as mock_warning:
            result = processor._validate_input_data(empty_df)
            assert result is False
            mock_warning.assert_called_once_with("Input data is empty")

    def test_validate_input_data_missing_columns(self):
        """Test validation with missing required columns."""
        processor = SampleCompoundInteraction()
        invalid_data = pd.DataFrame(
            {
                "sample": ["Sample1", "Sample2"],
                "ko": ["K00001", "K00002"],  # Missing compoundname and compoundclass
            }
        )

        with patch.object(processor.logger, "error") as mock_error:
            result = processor._validate_input_data(invalid_data)
            assert result is False
            mock_error.assert_called_once()

    def test_extract_sample_compound_interactions(self):
        """Test extraction of sample-compound interactions."""
        processor = SampleCompoundInteraction()
        test_data = self.test_create_sample_compound_data_fixture()

        result = processor._extract_sample_compound_interactions(test_data)

        # Check that duplicates are removed
        assert len(result) == 10  # 12 original rows - 2 duplicates

        # Check that all required columns are present
        expected_columns = ["sample", "compoundname", "compoundclass"]
        assert list(result.columns) == expected_columns

        # Check that Sample1 has unique interactions (should be 5, not 4)
        sample1_interactions = result[result["sample"] == "Sample1"]
        assert len(sample1_interactions) == 5

        # Check that compounds are correctly preserved
        thioacetamide_rows = result[result["compoundname"] == "Thioacetamide"]
        assert len(thioacetamide_rows) == 1
        assert thioacetamide_rows.iloc[0]["compoundclass"] == "Nitrogen-containing"

    def test_extract_sample_compound_interactions_with_nan(self):
        """Test extraction with NaN values."""
        processor = SampleCompoundInteraction()
        data_with_nan = pd.DataFrame(
            {
                "sample": ["Sample1", "Sample2", "Sample3"],
                "compoundname": ["Compound1", None, "Compound3"],
                "compoundclass": ["Metal", "Aliphatic", None],
            }
        )

        result = processor._extract_sample_compound_interactions(data_with_nan)

        # Should only return Sample1 (complete data)
        assert len(result) == 1
        assert result.iloc[0]["sample"] == "Sample1"
        assert result.iloc[0]["compoundname"] == "Compound1"
        assert result.iloc[0]["compoundclass"] == "Metal"

    def test_save_results_to_file(self):
        """Test saving results to file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            processor = SampleCompoundInteraction(
                output_dir=temp_dir, output_file="test_interactions.txt"
            )
            test_data = self.test_create_sample_compound_data_fixture()
            interactions = processor._extract_sample_compound_interactions(test_data)

            processor._save_results_to_file(interactions)

            output_path = os.path.join(temp_dir, "test_interactions.txt")
            assert os.path.exists(output_path)

            # Verify file contents
            saved_df = pd.read_csv(output_path, sep=";")
            assert len(saved_df) == len(interactions)
            assert list(saved_df.columns) == ["sample", "compoundname", "compoundclass"]

    def test_process_success(self):
        """Test successful processing with file saving."""
        with tempfile.TemporaryDirectory() as temp_dir:
            processor = SampleCompoundInteraction(
                output_dir=temp_dir, output_file="test_interactions.txt"
            )
            test_data = self.test_create_sample_compound_data_fixture()

            result = processor.process(test_data, save_file=True)

            # Check DataFrame structure
            expected_columns = ["sample", "compoundname", "compoundclass"]
            assert list(result.columns) == expected_columns

            # Check content - should remove duplicates
            assert len(result) == 10

            # Check that file was saved
            output_path = os.path.join(temp_dir, "test_interactions.txt")
            assert os.path.exists(output_path)

    def test_process_no_save(self):
        """Test processing without saving to file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            processor = SampleCompoundInteraction(
                output_dir=temp_dir, output_file="test_interactions.txt"
            )
            test_data = self.test_create_sample_compound_data_fixture()

            result = processor.process(test_data, save_file=False)

            # Check DataFrame structure
            expected_columns = ["sample", "compoundname", "compoundclass"]
            assert list(result.columns) == expected_columns

            # Check that file was not saved
            output_path = os.path.join(temp_dir, "test_interactions.txt")
            assert not os.path.exists(output_path)

    def test_process_invalid_data(self):
        """Test processing with invalid data."""
        processor = SampleCompoundInteraction()
        invalid_data = pd.DataFrame(
            {
                "sample": ["Sample1", "Sample2"],
                "ko": ["K00001", "K00002"],  # Missing required columns
            }
        )

        with patch.object(processor.logger, "warning") as mock_warning:
            result = processor.process(invalid_data)

            # Should return empty DataFrame with correct columns
            expected_columns = ["sample", "compoundname", "compoundclass"]
            assert list(result.columns) == expected_columns
            assert len(result) == 0

            mock_warning.assert_called_with(
                "Invalid input data, returning empty DataFrame"
            )

    def test_process_empty_data(self):
        """Test processing with empty DataFrame."""
        processor = SampleCompoundInteraction()
        empty_df = pd.DataFrame()

        with patch.object(processor.logger, "warning") as mock_warning:
            result = processor.process(empty_df)

            # Should return empty DataFrame with correct columns
            expected_columns = ["sample", "compoundname", "compoundclass"]
            assert list(result.columns) == expected_columns
            assert len(result) == 0

            mock_warning.assert_called_with(
                "Invalid input data, returning empty DataFrame"
            )

    def test_process_no_interactions_found(self):
        """Test processing when no valid interactions are found."""
        processor = SampleCompoundInteraction()
        data_no_interactions = pd.DataFrame(
            {
                "sample": ["Sample1", "Sample2", "Sample3"],
                "compoundname": [None, None, None],
                "compoundclass": [None, None, None],
            }
        )

        with patch.object(processor.logger, "warning") as mock_warning:
            result = processor.process(data_no_interactions)

            # Should return empty DataFrame with correct columns
            expected_columns = ["sample", "compoundname", "compoundclass"]
            assert list(result.columns) == expected_columns
            assert len(result) == 0

            mock_warning.assert_called_with(
                "No sample-compound interactions found in data"
            )

    @patch(
        "biorempp.analysis.sample_compound_interaction_processing.save_dataframe_output"
    )
    def test_save_results_error_handling(self, mock_save):
        """Test error handling in save_results_to_file."""
        mock_save.side_effect = Exception("File save error")

        processor = SampleCompoundInteraction()
        test_data = self.test_create_sample_compound_data_fixture()
        interactions = processor._extract_sample_compound_interactions(test_data)

        with patch.object(processor.logger, "error") as mock_error:
            with pytest.raises(Exception):
                processor._save_results_to_file(interactions)

            mock_error.assert_called_with(
                "Failed to save results to file: File save error"
            )

    def test_legacy_extract_compound_classes_compatibility(self):
        """Test that legacy extract_compound_classes method still works."""
        processor = SampleCompoundInteraction()
        test_data = self.test_create_sample_compound_data_fixture()

        # Test with DataFrame
        result = processor.extract_compound_classes(test_data)
        expected_classes = ["Aliphatic", "Metal", "Nitrogen-containing"]
        assert sorted(result) == expected_classes

        # Test with list of dicts
        list_data = test_data.to_dict("records")
        result_list = processor.extract_compound_classes(list_data)
        assert sorted(result_list) == expected_classes

        # Test with empty data
        assert processor.extract_compound_classes([]) == []
        assert processor.extract_compound_classes(None) == []

        # Test with missing column
        invalid_df = pd.DataFrame({"sample": ["S1"], "ko": ["K1"]})
        assert processor.extract_compound_classes(invalid_df) == []


# Integration test with CLI
def test_cli_integration():
    """Test CLI integration for the sample compound interaction processor."""
    import subprocess
    import tempfile

    # Create a test input file
    test_input = ">Sample1\n" "K00001\nK00002\n" ">Sample2\n" "K00003\nK00004\n"

    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write(test_input)
        input_file = f.name

    try:
        # Test listing modules (should include our processor)
        result = subprocess.run(
            ["python", "-m", "biorempp.main", "--list-modules"],
            capture_output=True,
            text=True,
            cwd=".",
        )

        assert result.returncode == 0
        assert "samplecompoundinteractionprocessor" in result.stdout.lower()

        # Test running the traditional pipeline (should generate data for our processor)
        with tempfile.TemporaryDirectory() as output_dir:
            result = subprocess.run(
                [
                    "python",
                    "-m",
                    "biorempp.main",
                    "--input",
                    input_file,
                    "--pipeline-type",
                    "biorempp",
                    "--output-dir",
                    output_dir,
                    "--no-timestamp",
                ],
                capture_output=True,
                text=True,
                cwd=".",
            )

            if result.returncode == 0:
                # Check if BioRemPP results were generated
                biorempp_file = os.path.join(output_dir, "BioRemPP_Results.txt")
                if os.path.exists(biorempp_file):
                    # Test modular pipeline with compound interaction processor
                    result = subprocess.run(
                        [
                            "python",
                            "-m",
                            "biorempp.main",
                            "--input",
                            biorempp_file,
                            "--enable-modular",
                            "--processors",
                            "samplecompoundinteractionprocessor",
                        ],
                        capture_output=True,
                        text=True,
                        cwd=".",
                    )

                    # Check that the processor ran (even if no compound data available)
                    assert "samplecompoundinteractionprocessor" in result.stdout.lower()

    finally:
        # Clean up
        try:
            os.unlink(input_file)
        except OSError:
            pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
