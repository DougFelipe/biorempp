"""
Single Merger Command Test Suite
===============================

Comprehensive testing suite for the DatabaseMergerCommand class,
validating single database processing operations, pipeline integration,
and targeted analytical workflows.

This test suite ensures the robustness of single database merger
functionality, including validation logic, pipeline execution,
parameter mapping, error handling, and result processing.

Test Coverage:
    - Command initialization and configuration
    - Pipeline type validation and parameter mapping
    - Database-specific execution workflows
    - Error handling and exception scenarios
    - Performance monitoring and result formatting
    - Integration with pipeline functions

Testing Strategy:
    - Unit testing for individual command methods
    - Mock-based testing for pipeline integration
    - Parametrized testing for multiple database types
    - Error scenario simulation and handling verification
    - Performance monitoring validation

Quality Standards:
    - PEP 8 compliance with line length < 88 characters
    - Comprehensive English documentation
    - Clear test organization and descriptive naming
    - Proper mocking and dependency isolation
    - Comprehensive assertion coverage

Author: BioRemPP Development Team
"""

import os
import tempfile
import time
from unittest.mock import Mock, patch

import pytest

from biorempp.commands.single_merger_command import DatabaseMergerCommand


class TestDatabaseMergerCommandInitialization:
    """Test DatabaseMergerCommand initialization and configuration."""

    def test_command_initialization(self):
        """Test successful command initialization."""
        command = DatabaseMergerCommand()
        
        # Assert
        assert hasattr(command, 'logger')
        assert command.logger.name.endswith('DatabaseMergerCommand')
        assert hasattr(command, 'PIPELINE_MAP')

    def test_pipeline_map_configuration(self):
        """Test that pipeline map contains all supported databases."""
        command = DatabaseMergerCommand()
        
        # Assert
        expected_pipelines = ['biorempp', 'kegg', 'hadeg', 'toxcsm']
        for pipeline in expected_pipelines:
            assert pipeline in command.PIPELINE_MAP
            assert callable(command.PIPELINE_MAP[pipeline])

    def test_logger_configuration(self):
        """Test that logger is properly configured."""
        command = DatabaseMergerCommand()
        
        # Assert
        assert command.logger is not None
        assert hasattr(command.logger, 'info')
        assert hasattr(command.logger, 'error')
        assert hasattr(command.logger, 'debug')


class TestDatabaseMergerCommandValidation:
    """Test DatabaseMergerCommand input validation functionality."""

    def test_validate_specific_input_valid_pipeline(self):
        """Test validation passes with supported pipeline type."""
        command = DatabaseMergerCommand()
        args = Mock()
        args.pipeline_type = "biorempp"
        args.input = "test_input.txt"
        
        # Act
        result = command.validate_specific_input(args)
        
        # Assert
        assert result is True

    def test_validate_specific_input_unsupported_pipeline(self):
        """Test validation fails with unsupported pipeline type."""
        command = DatabaseMergerCommand()
        args = Mock()
        args.pipeline_type = "unsupported"
        args.input = "test_input.txt"
        
        # Act
        result = command.validate_specific_input(args)
        
        # Assert
        assert result is False

    def test_validate_specific_input_missing_input_file(self):
        """Test validation fails when input file is missing."""
        command = DatabaseMergerCommand()
        args = Mock()
        args.pipeline_type = "biorempp"
        # No input attribute
        del args.input
        
        # Act
        result = command.validate_specific_input(args)
        
        # Assert
        assert result is False

    def test_validate_specific_input_none_input_file(self):
        """Test validation fails when input file is None."""
        command = DatabaseMergerCommand()
        args = Mock()
        args.pipeline_type = "biorempp"
        args.input = None
        
        # Act
        result = command.validate_specific_input(args)
        
        # Assert
        assert result is False

    def test_validate_specific_input_logging(self):
        """Test that validation logs appropriate messages."""
        command = DatabaseMergerCommand()
        args = Mock()
        args.pipeline_type = "biorempp"
        args.input = "test_input.txt"
        
        with patch.object(command.logger, 'debug') as mock_debug:
            # Act
            command.validate_specific_input(args)
            
            # Assert
            mock_debug.assert_called_once_with(
                "Pipeline validation passed for type: biorempp"
            )

    def test_validate_specific_input_error_logging(self):
        """Test that validation errors are logged."""
        command = DatabaseMergerCommand()
        args = Mock()
        args.pipeline_type = "unsupported"
        args.input = "test_input.txt"
        
        with patch.object(command.logger, 'error') as mock_error:
            # Act
            command.validate_specific_input(args)
            
            # Assert
            assert mock_error.called
            error_msg = mock_error.call_args[0][0]
            assert "Unsupported pipeline type" in error_msg


class TestDatabaseMergerCommandExecution:
    """Test DatabaseMergerCommand execution logic and workflow."""

    @patch('biorempp.commands.single_merger_command.get_error_handler')
    @patch('os.path.exists')
    def test_execute_successful_pipeline(self, mock_exists, mock_error_handler):
        """Test successful pipeline execution."""
        command = DatabaseMergerCommand()
        args = Mock()
        args.pipeline_type = "biorempp"
        args.input = "test_input.txt"
        
        # Mock file existence
        mock_exists.return_value = True
        
        # Mock pipeline function
        mock_pipeline = Mock(return_value={
            "output_path": "/path/to/output.txt",
            "matches": 100,
            "filename": "output.txt"
        })
        
        with patch.object(command, '_build_pipeline_kwargs', 
                         return_value={"input_path": "test_input.txt"}), \
             patch.dict(command.PIPELINE_MAP, 
                       {"biorempp": mock_pipeline}):
            
            # Act
            result = command.execute(args)
            
            # Assert
            assert "output_path" in result
            assert "processing_time" in result
            assert result["matches"] == 100
            mock_pipeline.assert_called_once()

    @patch('biorempp.commands.single_merger_command.get_error_handler')
    @patch('os.path.exists')
    def test_execute_file_not_found(self, mock_exists, mock_error_handler):
        """Test execution with non-existent input file."""
        command = DatabaseMergerCommand()
        args = Mock()
        args.pipeline_type = "biorempp"
        args.input = "nonexistent.txt"
        
        # Mock file does not exist
        mock_exists.return_value = False
        
        # Act & Assert
        with pytest.raises(FileNotFoundError):
            command.execute(args)

    @patch('biorempp.commands.single_merger_command.get_error_handler')
    @patch('os.path.exists')
    def test_execute_pipeline_exception(self, mock_exists, mock_error_handler):
        """Test execution with pipeline exception."""
        command = DatabaseMergerCommand()
        args = Mock()
        args.pipeline_type = "biorempp"
        args.input = "test_input.txt"
        
        # Mock file existence
        mock_exists.return_value = True
        
        # Mock pipeline function that raises exception
        mock_pipeline = Mock(side_effect=RuntimeError("Pipeline failed"))
        
        with patch.object(command, '_build_pipeline_kwargs', 
                         return_value={"input_path": "test_input.txt"}), \
             patch.dict(command.PIPELINE_MAP, 
                       {"biorempp": mock_pipeline}):
            
            # Act & Assert
            with pytest.raises(RuntimeError):
                command.execute(args)

    @patch('biorempp.commands.single_merger_command.get_error_handler')
    @patch('os.path.exists')
    def test_execute_string_result_handling(self, mock_exists, 
                                           mock_error_handler):
        """Test execution with string result (fallback format)."""
        command = DatabaseMergerCommand()
        args = Mock()
        args.pipeline_type = "biorempp"
        args.input = "test_input.txt"
        
        # Mock file existence
        mock_exists.return_value = True
        
        # Mock pipeline function returning string
        mock_pipeline = Mock(return_value="/path/to/output.txt")
        
        with patch.object(command, '_build_pipeline_kwargs', 
                         return_value={"input_path": "test_input.txt"}), \
             patch.dict(command.PIPELINE_MAP, 
                       {"biorempp": mock_pipeline}):
            
            # Act
            result = command.execute(args)
            
            # Assert
            assert result["output_path"] == "/path/to/output.txt"
            assert result["filename"] == "output.txt"
            assert "processing_time" in result

    @patch('biorempp.commands.single_merger_command.get_error_handler')
    @patch('os.path.exists')
    def test_execute_logging(self, mock_exists, mock_error_handler):
        """Test that execution logs appropriate messages."""
        command = DatabaseMergerCommand()
        args = Mock()
        args.pipeline_type = "biorempp"
        args.input = "test_input.txt"
        
        # Mock file existence
        mock_exists.return_value = True
        
        # Mock pipeline function
        mock_pipeline = Mock(return_value={"output_path": "/path/to/output.txt"})
        
        with patch.object(command.logger, 'info') as mock_info, \
             patch.object(command, '_build_pipeline_kwargs', 
                         return_value={"input_path": "test_input.txt"}), \
             patch.dict(command.PIPELINE_MAP, 
                       {"biorempp": mock_pipeline}):
            
            # Act
            command.execute(args)
            
            # Assert
            info_calls = [call[0][0] for call in mock_info.call_args_list]
            assert any("Executing pipeline: biorempp" in call 
                      for call in info_calls)


class TestDatabaseMergerCommandDatabasePath:
    """Test DatabaseMergerCommand database path resolution."""

    def test_get_database_path_biorempp(self):
        """Test database path resolution for BioRemPP."""
        command = DatabaseMergerCommand()
        
        # Act
        path = command._get_database_path("biorempp")
        
        # Assert
        assert path is not None
        assert "database_biorempp.csv" in path

    def test_get_database_path_hadeg(self):
        """Test database path resolution for HADEG."""
        command = DatabaseMergerCommand()
        
        # Act
        path = command._get_database_path("hadeg")
        
        # Assert
        assert path is not None
        assert "database_hadeg.csv" in path

    def test_get_database_path_kegg(self):
        """Test database path resolution for KEGG."""
        command = DatabaseMergerCommand()
        
        # Act
        path = command._get_database_path("kegg")
        
        # Assert
        assert path is not None
        assert "kegg_degradation_pathways.csv" in path

    def test_get_database_path_toxcsm(self):
        """Test database path resolution for ToxCSM."""
        command = DatabaseMergerCommand()
        
        # Act
        path = command._get_database_path("toxcsm")
        
        # Assert
        assert path is not None
        assert "database_toxcsm.csv" in path

    def test_get_database_path_none(self):
        """Test database path resolution with None input."""
        command = DatabaseMergerCommand()
        
        # Act
        path = command._get_database_path(None)
        
        # Assert
        assert path is None

    def test_get_database_path_unknown(self):
        """Test database path resolution with unknown database."""
        command = DatabaseMergerCommand()
        
        # Act
        path = command._get_database_path("unknown")
        
        # Assert
        assert path is None


class TestDatabaseMergerCommandPipelineKwargs:
    """Test DatabaseMergerCommand pipeline kwargs building."""

    def test_build_pipeline_kwargs_basic(self):
        """Test basic pipeline kwargs building."""
        command = DatabaseMergerCommand()
        args = Mock()
        args.input = "test_input.txt"
        args.output_dir = "outputs/test"
        args.add_timestamp = True
        
        # Act
        kwargs = command._build_pipeline_kwargs(args)
        
        # Assert
        assert kwargs["input_path"] == "test_input.txt"
        assert kwargs["output_dir"] == "outputs/test"
        assert kwargs["add_timestamp"] is True

    def test_build_pipeline_kwargs_with_database(self):
        """Test pipeline kwargs building with database specification."""
        command = DatabaseMergerCommand()
        args = Mock()
        args.input = "test_input.txt"
        args.database = "biorempp"
        
        with patch.object(command, '_get_database_path', 
                         return_value="/path/to/database.csv"):
            # Act
            kwargs = command._build_pipeline_kwargs(args)
            
            # Assert
            assert "database_path" in kwargs
            assert kwargs["database_path"] == "/path/to/database.csv"

    def test_build_pipeline_kwargs_kegg_database(self):
        """Test pipeline kwargs building for KEGG database."""
        command = DatabaseMergerCommand()
        args = Mock()
        args.input = "test_input.txt"
        args.database = "kegg"
        
        with patch.object(command, '_get_database_path', 
                         return_value="/path/to/kegg.csv"):
            # Act
            kwargs = command._build_pipeline_kwargs(args)
            
            # Assert
            assert "kegg_database_path" in kwargs
            assert kwargs["kegg_database_path"] == "/path/to/kegg.csv"

    def test_build_pipeline_kwargs_optional_parameters(self):
        """Test pipeline kwargs building with optional parameters."""
        command = DatabaseMergerCommand()
        args = Mock()
        args.input = "test_input.txt"
        args.output_filename = "custom_output.txt"
        args.sep = ";"
        
        # Set other optional args to None
        args.biorempp_database = None
        args.kegg_database = None
        
        # Act
        kwargs = command._build_pipeline_kwargs(args)
        
        # Assert
        assert kwargs["output_filename"] == "custom_output.txt"
        assert kwargs["sep"] == ";"
        assert "biorempp_database" not in kwargs  # None values excluded

    def test_build_pipeline_kwargs_defaults(self):
        """Test pipeline kwargs building with default values."""
        command = DatabaseMergerCommand()
        args = Mock()
        args.input = "test_input.txt"
        
        # Remove optional attributes
        for attr in ['output_dir', 'add_timestamp', 'database']:
            if hasattr(args, attr):
                delattr(args, attr)
        
        # Act
        kwargs = command._build_pipeline_kwargs(args)
        
        # Assert
        assert kwargs["input_path"] == "test_input.txt"
        assert kwargs["output_dir"] == "outputs/results_tables"
        assert kwargs["add_timestamp"] is False


class TestDatabaseMergerCommandParametrized:
    """Parametrized tests for DatabaseMergerCommand functionality."""

    @pytest.mark.parametrize("pipeline_type", [
        "biorempp", "kegg", "hadeg", "toxcsm"
    ])
    def test_validate_all_supported_pipelines(self, pipeline_type):
        """Test validation for all supported pipeline types."""
        command = DatabaseMergerCommand()
        args = Mock()
        args.pipeline_type = pipeline_type
        args.input = "test_input.txt"
        
        # Act
        result = command.validate_specific_input(args)
        
        # Assert
        assert result is True

    @pytest.mark.parametrize("database_name,expected_file", [
        ("biorempp", "database_biorempp.csv"),
        ("hadeg", "database_hadeg.csv"),
        ("kegg", "kegg_degradation_pathways.csv"),
        ("toxcsm", "database_toxcsm.csv"),
    ])
    def test_database_path_mapping(self, database_name, expected_file):
        """Test database path mapping for all databases."""
        command = DatabaseMergerCommand()
        
        # Act
        path = command._get_database_path(database_name)
        
        # Assert
        assert path is not None
        assert expected_file in path

    @pytest.mark.parametrize("database_name,expected_key", [
        ("biorempp", "database_path"),
        ("kegg", "kegg_database_path"),
        ("hadeg", "hadeg_database_path"),
        ("toxcsm", "toxcsm_database_path"),
    ])
    def test_pipeline_kwargs_database_mapping(self, database_name, 
                                             expected_key):
        """Test pipeline kwargs database parameter mapping."""
        command = DatabaseMergerCommand()
        args = Mock()
        args.input = "test_input.txt"
        args.database = database_name
        
        with patch.object(command, '_get_database_path', 
                         return_value="/path/to/db.csv"):
            # Act
            kwargs = command._build_pipeline_kwargs(args)
            
            # Assert
            assert expected_key in kwargs
            assert kwargs[expected_key] == "/path/to/db.csv"


class TestDatabaseMergerCommandIntegration:
    """Test DatabaseMergerCommand integration scenarios."""

    def test_full_execution_workflow_success(self):
        """Test complete successful execution workflow."""
        command = DatabaseMergerCommand()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
            tmp_file.write("test input data")
            temp_path = tmp_file.name
        
        try:
            args = Mock()
            args.pipeline_type = "biorempp"
            args.input = temp_path
            
            # Mock pipeline execution
            with patch.dict(command.PIPELINE_MAP, {
                "biorempp": Mock(return_value={
                    "output_path": "/path/to/output.txt",
                    "matches": 50
                })
            }), patch.object(command, '_build_pipeline_kwargs', 
                           return_value={"input_path": temp_path}):
                
                # Act
                result = command.run(args)
                
                # Assert
                assert "output_path" in result
                assert "processing_time" in result
                
        finally:
            # Clean up
            os.unlink(temp_path)

    def test_command_reusability(self):
        """Test that command instances can be reused."""
        command = DatabaseMergerCommand()
        
        args1 = Mock()
        args1.pipeline_type = "biorempp"
        args1.input = "test1.txt"
        
        args2 = Mock()
        args2.pipeline_type = "kegg"
        args2.input = "test2.txt"
        
        # Mock pipeline executions
        mock_biorempp = Mock(return_value={"output_path": "/path1.txt"})
        mock_kegg = Mock(return_value={"output_path": "/path2.txt"})
        
        with patch('os.path.exists', return_value=True), \
             patch.dict(command.PIPELINE_MAP, {
                 "biorempp": mock_biorempp,
                 "kegg": mock_kegg
             }), \
             patch.object(command, '_build_pipeline_kwargs', 
                         return_value={}):
            
            # Both executions should succeed
            result1 = command.execute(args1)
            result2 = command.execute(args2)
            
            assert "output_path" in result1
            assert "output_path" in result2
            mock_biorempp.assert_called_once()
            mock_kegg.assert_called_once()
