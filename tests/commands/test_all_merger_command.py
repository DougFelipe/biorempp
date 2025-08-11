"""
All Databases Merger Command Test Suite
======================================

Comprehensive testing suite for the AllDatabasesMergerCommand class,
validating multi-database processing operations, sequential execution,
and comprehensive analytical workflows.

This test suite ensures the robustness of the all databases merger
functionality, including validation logic, multi-pipeline orchestration,
fault tolerance, error handling, and result aggregation.

Test Coverage:
    - Command initialization and configuration
    - Multi-database validation and processing
    - Sequential execution workflow and fault tolerance
    - Error handling and recovery mechanisms
    - Result aggregation and reporting
    - Integration with multiple pipeline functions

Testing Strategy:
    - Unit testing for individual command methods
    - Mock-based testing for multi-pipeline integration
    - Fault tolerance testing with simulated failures
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
from unittest.mock import Mock, patch

import pytest

from biorempp.commands.all_merger_command import AllDatabasesMergerCommand


class TestAllDatabasesMergerCommandInitialization:
    """Test AllDatabasesMergerCommand initialization and configuration."""

    def test_command_initialization(self):
        """Test successful command initialization."""
        command = AllDatabasesMergerCommand()
        
        # Assert
        assert hasattr(command, 'logger')
        assert command.logger.name.endswith('AllDatabasesMergerCommand')
        assert hasattr(command, 'MERGE_FUNCTIONS')

    def test_merge_functions_configuration(self):
        """Test that merge functions map contains all supported databases."""
        command = AllDatabasesMergerCommand()
        
        # Assert
        expected_databases = ['biorempp', 'hadeg', 'kegg', 'toxcsm']
        for database in expected_databases:
            assert database in command.MERGE_FUNCTIONS
            assert callable(command.MERGE_FUNCTIONS[database])

    def test_logger_configuration(self):
        """Test that logger is properly configured."""
        command = AllDatabasesMergerCommand()
        
        # Assert
        assert command.logger is not None
        assert hasattr(command.logger, 'info')
        assert hasattr(command.logger, 'error')
        assert hasattr(command.logger, 'debug')


class TestAllDatabasesMergerCommandValidation:
    """Test AllDatabasesMergerCommand input validation functionality."""

    def test_validate_specific_input_with_input_file(self):
        """Test validation passes with valid input file."""
        command = AllDatabasesMergerCommand()
        args = Mock()
        args.input = "test_input.txt"
        
        # Act
        result = command.validate_specific_input(args)
        
        # Assert
        assert result is True

    def test_validate_specific_input_missing_input_file(self):
        """Test validation fails when input file is missing."""
        command = AllDatabasesMergerCommand()
        args = Mock()
        # No input attribute
        del args.input
        
        # Act
        result = command.validate_specific_input(args)
        
        # Assert
        assert result is False

    def test_validate_specific_input_none_input_file(self):
        """Test validation fails when input file is None."""
        command = AllDatabasesMergerCommand()
        args = Mock()
        args.input = None
        
        # Act
        result = command.validate_specific_input(args)
        
        # Assert
        assert result is False

    def test_validate_specific_input_empty_input_file(self):
        """Test validation fails when input file is empty string."""
        command = AllDatabasesMergerCommand()
        args = Mock()
        args.input = ""
        
        # Act
        result = command.validate_specific_input(args)
        
        # Assert
        assert result is False

    def test_validate_specific_input_logging(self):
        """Test that validation logs appropriate messages."""
        command = AllDatabasesMergerCommand()
        args = Mock()
        args.input = "test_input.txt"
        
        with patch.object(command.logger, 'debug') as mock_debug:
            # Act
            command.validate_specific_input(args)
            
            # Assert
            mock_debug.assert_called_once_with(
                "All databases merger validation passed"
            )

    def test_validate_specific_input_error_logging(self):
        """Test that validation errors are logged."""
        command = AllDatabasesMergerCommand()
        args = Mock()
        args.input = None
        
        with patch.object(command.logger, 'error') as mock_error:
            # Act
            command.validate_specific_input(args)
            
            # Assert
            mock_error.assert_called_once_with(
                "Input file is required for database merging"
            )


class TestAllDatabasesMergerCommandExecution:
    """Test AllDatabasesMergerCommand execution logic and workflow."""

    def test_execute_all_databases_success(self):
        """Test successful execution with all databases."""
        command = AllDatabasesMergerCommand()
        args = Mock()
        args.input = "test_input.txt"
        
        # Mock all merge functions to succeed
        mock_results = {
            "biorempp": {"output_path": "/path/biorempp.txt", "matches": 100},
            "hadeg": {"output_path": "/path/hadeg.txt", "matches": 50},
            "kegg": {"output_path": "/path/kegg.txt", "matches": 75},
            "toxcsm": {"output_path": "/path/toxcsm.txt", "matches": 25}
        }
        
        mock_functions = {}
        for db_name, result in mock_results.items():
            mock_functions[db_name] = Mock(return_value=result)
        
        with patch.dict(command.MERGE_FUNCTIONS, mock_functions), \
             patch.object(command, '_build_pipeline_kwargs', 
                         return_value={"input_path": "test_input.txt"}):
            
            # Act
            result = command.execute(args)
            
            # Assert
            assert len(result) == 4
            for db_name in mock_results.keys():
                assert db_name in result
                assert result[db_name] == mock_results[db_name]
                mock_functions[db_name].assert_called_once()

    def test_execute_with_partial_failures(self):
        """Test execution with some database failures."""
        command = AllDatabasesMergerCommand()
        args = Mock()
        args.input = "test_input.txt"
        
        # Mock some functions to succeed, others to fail
        mock_functions = {
            "biorempp": Mock(return_value={"output_path": "/path/biorempp.txt"}),
            "hadeg": Mock(side_effect=RuntimeError("HADEG failed")),
            "kegg": Mock(return_value={"output_path": "/path/kegg.txt"}),
            "toxcsm": Mock(side_effect=ValueError("ToxCSM failed"))
        }
        
        with patch.dict(command.MERGE_FUNCTIONS, mock_functions), \
             patch.object(command, '_build_pipeline_kwargs', 
                         return_value={"input_path": "test_input.txt"}):
            
            # Act
            result = command.execute(args)
            
            # Assert
            assert len(result) == 4
            
            # Check successful results
            assert "output_path" in result["biorempp"]
            assert "output_path" in result["kegg"]
            
            # Check failed results
            assert "error" in result["hadeg"]
            assert "HADEG failed" in result["hadeg"]["error"]
            assert "error" in result["toxcsm"]
            assert "ToxCSM failed" in result["toxcsm"]["error"]

    def test_execute_all_failures(self):
        """Test execution when all databases fail."""
        command = AllDatabasesMergerCommand()
        args = Mock()
        args.input = "test_input.txt"
        
        # Mock all functions to fail
        mock_functions = {
            "biorempp": Mock(side_effect=RuntimeError("BioRemPP failed")),
            "hadeg": Mock(side_effect=RuntimeError("HADEG failed")),
            "kegg": Mock(side_effect=RuntimeError("KEGG failed")),
            "toxcsm": Mock(side_effect=RuntimeError("ToxCSM failed"))
        }
        
        with patch.dict(command.MERGE_FUNCTIONS, mock_functions), \
             patch.object(command, '_build_pipeline_kwargs', 
                         return_value={"input_path": "test_input.txt"}):
            
            # Act
            result = command.execute(args)
            
            # Assert
            assert len(result) == 4
            for db_name in mock_functions.keys():
                assert "error" in result[db_name]
                assert "failed" in result[db_name]["error"]

    def test_execute_logging_summary(self):
        """Test that execution logs summary information."""
        command = AllDatabasesMergerCommand()
        args = Mock()
        args.input = "test_input.txt"
        
        # Mock mixed success/failure
        mock_functions = {
            "biorempp": Mock(return_value={"output_path": "/path/biorempp.txt"}),
            "hadeg": Mock(side_effect=RuntimeError("HADEG failed")),
            "kegg": Mock(return_value={"output_path": "/path/kegg.txt"}),
            "toxcsm": Mock(side_effect=RuntimeError("ToxCSM failed"))
        }
        
        with patch.dict(command.MERGE_FUNCTIONS, mock_functions), \
             patch.object(command, '_build_pipeline_kwargs', 
                         return_value={}), \
             patch.object(command.logger, 'info') as mock_info, \
             patch.object(command.logger, 'warning') as mock_warning:
            
            # Act
            command.execute(args)
            
            # Assert logging calls
            info_calls = [call[0][0] for call in mock_info.call_args_list]
            
            # Check for summary log
            summary_found = any("All databases merge completed" in call 
                               for call in info_calls)
            assert summary_found
            
            # Check for successful count
            success_found = any("Successful: 2/4" in call 
                               for call in info_calls)
            assert success_found
            
            # Check for failed databases warning
            warning_calls = [call[0][0] for call in mock_warning.call_args_list]
            failed_found = any("Failed merges:" in call 
                              for call in warning_calls)
            assert failed_found


class TestAllDatabasesMergerCommandDatabasePath:
    """Test AllDatabasesMergerCommand database path resolution."""

    def test_get_database_path_biorempp(self):
        """Test database path resolution for BioRemPP."""
        command = AllDatabasesMergerCommand()
        
        # Act
        path = command._get_database_path("biorempp")
        
        # Assert
        assert path is not None
        assert "database_biorempp.csv" in path

    def test_get_database_path_hadeg(self):
        """Test database path resolution for HADEG."""
        command = AllDatabasesMergerCommand()
        
        # Act
        path = command._get_database_path("hadeg")
        
        # Assert
        assert path is not None
        assert "database_hadeg.csv" in path

    def test_get_database_path_kegg(self):
        """Test database path resolution for KEGG."""
        command = AllDatabasesMergerCommand()
        
        # Act
        path = command._get_database_path("kegg")
        
        # Assert
        assert path is not None
        assert "kegg_degradation_pathways.csv" in path

    def test_get_database_path_toxcsm(self):
        """Test database path resolution for ToxCSM."""
        command = AllDatabasesMergerCommand()
        
        # Act
        path = command._get_database_path("toxcsm")
        
        # Assert
        assert path is not None
        assert "database_toxcsm.csv" in path

    def test_get_database_path_unknown(self):
        """Test database path resolution with unknown database."""
        command = AllDatabasesMergerCommand()
        
        # Act & Assert
        with pytest.raises(ValueError, match="Unknown database: unknown"):
            command._get_database_path("unknown")

    def test_get_database_path_structure(self):
        """Test that database paths have correct structure."""
        command = AllDatabasesMergerCommand()
        
        # Act
        path = command._get_database_path("biorempp")
        
        # Assert
        assert os.path.isabs(path) or ".." in path  # Absolute or relative path
        assert path.endswith("database_biorempp.csv")


class TestAllDatabasesMergerCommandPipelineKwargs:
    """Test AllDatabasesMergerCommand pipeline kwargs building."""

    def test_build_pipeline_kwargs_basic(self):
        """Test basic pipeline kwargs building."""
        command = AllDatabasesMergerCommand()
        args = Mock()
        args.input = "test_input.txt"
        args.output_dir = "outputs/test"
        args.add_timestamp = True
        
        # Act
        kwargs = command._build_pipeline_kwargs(args, "biorempp")
        
        # Assert
        assert kwargs["input_path"] == "test_input.txt"
        assert kwargs["output_dir"] == "outputs/test"
        assert kwargs["add_timestamp"] is True

    def test_build_pipeline_kwargs_biorempp(self):
        """Test pipeline kwargs building for BioRemPP database."""
        command = AllDatabasesMergerCommand()
        args = Mock()
        args.input = "test_input.txt"
        
        with patch.object(command, '_get_database_path', 
                         return_value="/path/to/biorempp.csv"):
            # Act
            kwargs = command._build_pipeline_kwargs(args, "biorempp")
            
            # Assert
            assert "database_path" in kwargs
            assert kwargs["database_path"] == "/path/to/biorempp.csv"

    def test_build_pipeline_kwargs_kegg(self):
        """Test pipeline kwargs building for KEGG database."""
        command = AllDatabasesMergerCommand()
        args = Mock()
        args.input = "test_input.txt"
        
        with patch.object(command, '_get_database_path', 
                         return_value="/path/to/kegg.csv"):
            # Act
            kwargs = command._build_pipeline_kwargs(args, "kegg")
            
            # Assert
            assert "kegg_database_path" in kwargs
            assert kwargs["kegg_database_path"] == "/path/to/kegg.csv"

    def test_build_pipeline_kwargs_hadeg(self):
        """Test pipeline kwargs building for HADEG database."""
        command = AllDatabasesMergerCommand()
        args = Mock()
        args.input = "test_input.txt"
        
        with patch.object(command, '_get_database_path', 
                         return_value="/path/to/hadeg.csv"):
            # Act
            kwargs = command._build_pipeline_kwargs(args, "hadeg")
            
            # Assert
            assert "hadeg_database_path" in kwargs
            assert kwargs["hadeg_database_path"] == "/path/to/hadeg.csv"

    def test_build_pipeline_kwargs_toxcsm(self):
        """Test pipeline kwargs building for ToxCSM database."""
        command = AllDatabasesMergerCommand()
        args = Mock()
        args.input = "test_input.txt"
        
        with patch.object(command, '_get_database_path', 
                         return_value="/path/to/toxcsm.csv"):
            # Act
            kwargs = command._build_pipeline_kwargs(args, "toxcsm")
            
            # Assert
            assert "toxcsm_database_path" in kwargs
            assert kwargs["toxcsm_database_path"] == "/path/to/toxcsm.csv"

    def test_build_pipeline_kwargs_defaults(self):
        """Test pipeline kwargs building with default values."""
        command = AllDatabasesMergerCommand()
        args = Mock()
        args.input = "test_input.txt"
        
        # Remove optional attributes
        for attr in ['output_dir', 'add_timestamp']:
            if hasattr(args, attr):
                delattr(args, attr)
        
        # Act
        kwargs = command._build_pipeline_kwargs(args, "biorempp")
        
        # Assert
        assert kwargs["input_path"] == "test_input.txt"
        assert kwargs["output_dir"] == "outputs/results_tables"
        assert kwargs["add_timestamp"] is False


class TestAllDatabasesMergerCommandParametrized:
    """Parametrized tests for AllDatabasesMergerCommand functionality."""

    @pytest.mark.parametrize("database_name,expected_file", [
        ("biorempp", "database_biorempp.csv"),
        ("hadeg", "database_hadeg.csv"),
        ("kegg", "kegg_degradation_pathways.csv"),
        ("toxcsm", "database_toxcsm.csv"),
    ])
    def test_database_path_mapping(self, database_name, expected_file):
        """Test database path mapping for all databases."""
        command = AllDatabasesMergerCommand()
        
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
        command = AllDatabasesMergerCommand()
        args = Mock()
        args.input = "test_input.txt"
        
        with patch.object(command, '_get_database_path', 
                         return_value="/path/to/db.csv"):
            # Act
            kwargs = command._build_pipeline_kwargs(args, database_name)
            
            # Assert
            assert expected_key in kwargs
            assert kwargs[expected_key] == "/path/to/db.csv"

    @pytest.mark.parametrize("num_failures", [0, 1, 2, 3, 4])
    def test_fault_tolerance_scenarios(self, num_failures):
        """Test fault tolerance with varying numbers of failures."""
        command = AllDatabasesMergerCommand()
        args = Mock()
        args.input = "test_input.txt"
        
        databases = ["biorempp", "hadeg", "kegg", "toxcsm"]
        mock_functions = {}
        
        # Set up mixed success/failure based on num_failures
        for i, db_name in enumerate(databases):
            if i < num_failures:
                mock_functions[db_name] = Mock(
                    side_effect=RuntimeError(f"{db_name} failed")
                )
            else:
                mock_functions[db_name] = Mock(
                    return_value={"output_path": f"/path/{db_name}.txt"}
                )
        
        with patch.dict(command.MERGE_FUNCTIONS, mock_functions), \
             patch.object(command, '_build_pipeline_kwargs', 
                         return_value={}):
            
            # Act
            result = command.execute(args)
            
            # Assert
            assert len(result) == 4
            
            # Count successful and failed results
            successful = sum(1 for r in result.values() if "error" not in r)
            failed = sum(1 for r in result.values() if "error" in r)
            
            assert successful == (4 - num_failures)
            assert failed == num_failures


class TestAllDatabasesMergerCommandIntegration:
    """Test AllDatabasesMergerCommand integration scenarios."""

    def test_full_execution_workflow_success(self):
        """Test complete successful execution workflow."""
        command = AllDatabasesMergerCommand()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
            tmp_file.write("test input data")
            temp_path = tmp_file.name
        
        try:
            args = Mock()
            args.input = temp_path
            
            # Mock all merge functions to succeed
            mock_functions = {
                "biorempp": Mock(return_value={"output_path": "/biorempp.txt"}),
                "hadeg": Mock(return_value={"output_path": "/hadeg.txt"}),
                "kegg": Mock(return_value={"output_path": "/kegg.txt"}),
                "toxcsm": Mock(return_value={"output_path": "/toxcsm.txt"})
            }
            
            with patch.dict(command.MERGE_FUNCTIONS, mock_functions), \
                 patch.object(command, '_build_pipeline_kwargs', 
                             return_value={}):
                
                # Act
                result = command.run(args)
                
                # Assert
                assert len(result) == 4
                for db_name in mock_functions.keys():
                    assert db_name in result
                    assert "output_path" in result[db_name]
                
        finally:
            # Clean up
            os.unlink(temp_path)

    def test_command_reusability(self):
        """Test that command instances can be reused."""
        command = AllDatabasesMergerCommand()
        
        args1 = Mock()
        args1.input = "test1.txt"
        
        args2 = Mock()
        args2.input = "test2.txt"
        
        # Mock merge functions
        mock_functions = {
            "biorempp": Mock(return_value={"output_path": "/biorempp.txt"}),
            "hadeg": Mock(return_value={"output_path": "/hadeg.txt"}),
            "kegg": Mock(return_value={"output_path": "/kegg.txt"}),
            "toxcsm": Mock(return_value={"output_path": "/toxcsm.txt"})
        }
        
        with patch.dict(command.MERGE_FUNCTIONS, mock_functions), \
             patch.object(command, '_build_pipeline_kwargs', return_value={}):
            
            # Both executions should succeed
            result1 = command.execute(args1)
            result2 = command.execute(args2)
            
            assert len(result1) == 4
            assert len(result2) == 4
            
            # Each function should be called twice (once per execution)
            for mock_func in mock_functions.values():
                assert mock_func.call_count == 2

    def test_execution_with_real_validation(self):
        """Test execution with actual validation workflow."""
        command = AllDatabasesMergerCommand()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
            tmp_file.write("test content")
            temp_path = tmp_file.name
        
        try:
            args = Mock()
            args.input = temp_path
            
            # Mock merge functions
            mock_functions = {
                "biorempp": Mock(return_value={"output_path": "/biorempp.txt"}),
                "hadeg": Mock(return_value={"output_path": "/hadeg.txt"}),
                "kegg": Mock(return_value={"output_path": "/kegg.txt"}),
                "toxcsm": Mock(return_value={"output_path": "/toxcsm.txt"})
            }
            
            with patch.dict(command.MERGE_FUNCTIONS, mock_functions), \
                 patch.object(command, '_build_pipeline_kwargs', 
                             return_value={}):
                
                # Act - use run() to include validation
                result = command.run(args)
                
                # Assert
                assert len(result) == 4
                for db_name in ["biorempp", "hadeg", "kegg", "toxcsm"]:
                    assert db_name in result
                
        finally:
            # Clean up
            os.unlink(temp_path)
