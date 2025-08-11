"""
InfoCommand Test Suite
=====================

Comprehensive testing suite for the InfoCommand class, validating
database information display functionality and help system capabilities
without requiring input file processing.

This test suite ensures the robustness of the information command
system, including database listing, detailed information display,
validation logic, and output formatting.

Test Coverage:
    - Command initialization with different info types
    - Database listing functionality and output formatting
    - Database-specific information display and content validation
    - Input validation for informational commands
    - Error handling for unsupported operations
    - Output structure and content verification

Testing Strategy:
    - Unit testing for individual information methods
    - Output content validation and structure verification
    - Error scenario simulation and handling verification
    - Mock-based testing for isolated functionality
    - Parametrized testing for multiple database types

Quality Standards:
    - PEP 8 compliance with line length < 88 characters
    - Comprehensive English documentation
    - Clear test organization and descriptive naming
    - Proper mocking and dependency isolation
    - Comprehensive assertion coverage

Author: BioRemPP Development Team
"""

from io import StringIO
from unittest.mock import Mock, patch

import pytest

from biorempp.commands.info_command import InfoCommand


class TestInfoCommandInitialization:
    """Test InfoCommand initialization and configuration."""

    def test_info_command_databases_initialization(self):
        """Test initialization for database listing command."""
        command = InfoCommand("databases")
        
        # Assert
        assert command.info_type == "databases"
        assert command.target is None
        assert hasattr(command, 'logger')

    def test_info_command_database_info_initialization(self):
        """Test initialization for specific database info command."""
        command = InfoCommand("database_info", "biorempp")
        
        # Assert
        assert command.info_type == "database_info"
        assert command.target == "biorempp"
        assert hasattr(command, 'logger')

    def test_info_command_initialization_with_none_target(self):
        """Test initialization with explicit None target."""
        command = InfoCommand("databases", None)
        
        # Assert
        assert command.info_type == "databases"
        assert command.target is None

    def test_info_command_logger_configuration(self):
        """Test that logger is properly configured."""
        command = InfoCommand("databases")
        
        # Assert
        assert command.logger.name.endswith("InfoCommand")


class TestInfoCommandValidation:
    """Test InfoCommand input validation functionality."""

    def test_validate_specific_input_always_returns_true(self):
        """Test that info commands always pass specific validation."""
        command = InfoCommand("databases")
        args = Mock()
        
        # Act
        result = command.validate_specific_input(args)
        
        # Assert
        assert result is True

    def test_validate_specific_input_with_database_info(self):
        """Test validation for database info command."""
        command = InfoCommand("database_info", "biorempp")
        args = Mock()
        
        # Act
        result = command.validate_specific_input(args)
        
        # Assert
        assert result is True

    def test_validate_specific_input_logging(self):
        """Test that validation logs debug information."""
        command = InfoCommand("databases")
        args = Mock()
        
        with patch.object(command.logger, 'debug') as mock_debug:
            # Act
            command.validate_specific_input(args)
            
            # Assert
            mock_debug.assert_called_once_with(
                "Info command validation for type: databases"
            )


class TestInfoCommandDatabaseListing:
    """Test InfoCommand database listing functionality."""

    @patch('builtins.print')
    def test_list_databases_output_structure(self, mock_print):
        """Test that database listing produces correct output structure."""
        command = InfoCommand("databases")
        
        # Act
        result = command._list_databases()
        
        # Assert result structure
        assert "databases" in result
        assert isinstance(result["databases"], dict)
        
        # Check database entries
        expected_databases = ["biorempp", "hadeg", "kegg", "toxcsm"]
        for db_name in expected_databases:
            assert db_name in result["databases"]

    @patch('builtins.print')
    def test_list_databases_content_validation(self, mock_print):
        """Test database listing content for correctness."""
        command = InfoCommand("databases")
        
        # Act
        result = command._list_databases()
        databases = result["databases"]
        
        # Assert BioRemPP database info
        biorempp = databases["biorempp"]
        assert biorempp["name"] == "BioRemPP Core Database"
        assert "6,623 records" in biorempp["description"]
        assert biorempp["file"] == "database_biorempp.csv"
        
        # Assert HADEG database info
        hadeg = databases["hadeg"]
        assert hadeg["name"] == "HADEG Database"
        assert "1,168 records" in hadeg["description"]
        assert hadeg["file"] == "database_hadeg.csv"
        
        # Assert KEGG database info
        kegg = databases["kegg"]
        assert kegg["name"] == "KEGG Pathways"
        assert "871 records" in kegg["description"]
        assert kegg["file"] == "kegg_degradation_pathways.csv"
        
        # Assert ToxCSM database info
        toxcsm = databases["toxcsm"]
        assert toxcsm["name"] == "ToxCSM Database"
        assert "323 records" in toxcsm["description"]
        assert toxcsm["file"] == "database_toxcsm.csv"

    @patch('builtins.print')
    def test_list_databases_print_calls(self, mock_print):
        """Test that database listing prints expected content."""
        command = InfoCommand("databases")
        
        # Act
        command._list_databases()
        
        # Assert print was called multiple times
        assert mock_print.call_count > 0
        
        # Check for key headers in print calls
        print_args = [call[0][0] for call in mock_print.call_args_list 
                     if call[0]]
        
        header_found = any("[DATABASES] Available Databases:" in arg 
                          for arg in print_args)
        assert header_found

    @patch('builtins.print')
    def test_list_databases_usage_examples(self, mock_print):
        """Test that database listing includes usage examples."""
        command = InfoCommand("databases")
        
        # Act
        command._list_databases()
        
        # Check that usage examples are printed
        print_args = [call[0][0] for call in mock_print.call_args_list 
                     if call[0]]
        
        usage_found = any("[USAGE] Usage Examples:" in arg 
                         for arg in print_args)
        assert usage_found


class TestInfoCommandDatabaseInfo:
    """Test InfoCommand specific database information functionality."""

    @patch('builtins.print')
    def test_show_database_info_biorempp(self, mock_print):
        """Test showing BioRemPP database information."""
        command = InfoCommand("database_info", "biorempp")
        
        # Act
        result = command._show_database_info("biorempp")
        
        # Assert result structure
        assert "database_info" in result
        assert "biorempp" in result["database_info"]
        
        # Assert content
        biorempp_info = result["database_info"]["biorempp"]
        assert biorempp_info["name"] == "BioRemPP Core Database"
        assert biorempp_info["size"] == "6,623 records"
        assert "ko" in biorempp_info["columns"]
        assert "genesymbol" in biorempp_info["columns"]

    @patch('builtins.print')
    def test_show_database_info_hadeg(self, mock_print):
        """Test showing HADEG database information."""
        command = InfoCommand("database_info", "hadeg")
        
        # Act
        result = command._show_database_info("hadeg")
        
        # Assert
        hadeg_info = result["database_info"]["hadeg"]
        assert "Hydrocarbon Aerobic Degradation" in hadeg_info["name"]
        assert hadeg_info["size"] == "1,168 records"
        assert "Gene" in hadeg_info["columns"]
        assert "Pathway" in hadeg_info["columns"]

    @patch('builtins.print')
    def test_show_database_info_kegg(self, mock_print):
        """Test showing KEGG database information."""
        command = InfoCommand("database_info", "kegg")
        
        # Act
        result = command._show_database_info("kegg")
        
        # Assert
        kegg_info = result["database_info"]["kegg"]
        assert "KEGG Degradation Pathways" in kegg_info["name"]
        assert kegg_info["size"] == "871 records"
        assert "ko" in kegg_info["columns"]
        assert "pathname" in kegg_info["columns"]

    @patch('builtins.print')
    def test_show_database_info_toxcsm(self, mock_print):
        """Test showing ToxCSM database information."""
        command = InfoCommand("database_info", "toxcsm")
        
        # Act
        result = command._show_database_info("toxcsm")
        
        # Assert
        toxcsm_info = result["database_info"]["toxcsm"]
        assert "ToxCSM Toxicity Database" in toxcsm_info["name"]
        assert toxcsm_info["size"] == "323 records"
        assert "SMILES" in toxcsm_info["columns"]
        assert "cpd" in toxcsm_info["columns"]

    @patch('builtins.print')
    def test_show_database_info_unknown_database(self, mock_print):
        """Test handling of unknown database request."""
        command = InfoCommand("database_info", "unknown")
        
        # Act
        result = command._show_database_info("unknown")
        
        # Assert error handling
        assert "error" in result
        assert "Database 'unknown' not found" in result["error"]

    @patch('builtins.print')
    def test_show_database_info_print_structure(self, mock_print):
        """Test that database info prints with correct structure."""
        command = InfoCommand("database_info", "biorempp")
        
        # Act
        command._show_database_info("biorempp")
        
        # Assert print structure
        print_args = [call[0][0] for call in mock_print.call_args_list 
                     if call[0]]
        
        # Check for key sections
        sections = ["Database Schema:", "Key Features:", "Primary Usage:"]
        for section in sections:
            section_found = any(section in arg for arg in print_args)
            assert section_found


class TestInfoCommandExecution:
    """Test InfoCommand execution logic and workflow."""

    def test_execute_databases_command(self):
        """Test execution of database listing command."""
        command = InfoCommand("databases")
        args = Mock()
        
        with patch.object(command, '_list_databases', 
                         return_value={"databases": {}}) as mock_list:
            # Act
            result = command.execute(args)
            
            # Assert
            mock_list.assert_called_once()
            assert result == {"databases": {}}

    def test_execute_database_info_command(self):
        """Test execution of specific database info command."""
        command = InfoCommand("database_info", "biorempp")
        args = Mock()
        
        with patch.object(command, '_show_database_info', 
                         return_value={"database_info": {"biorempp": {}}}) \
                         as mock_show:
            # Act
            result = command.execute(args)
            
            # Assert
            mock_show.assert_called_once_with("biorempp")
            assert result == {"database_info": {"biorempp": {}}}

    def test_execute_unsupported_info_type(self):
        """Test execution with unsupported info type."""
        command = InfoCommand("unsupported_type")
        args = Mock()
        
        # Act & Assert
        with pytest.raises(ValueError, 
                          match="Unsupported info type: unsupported_type"):
            command.execute(args)

    def test_execute_logging(self):
        """Test that execution logs info command type."""
        command = InfoCommand("databases")
        args = Mock()
        
        with patch.object(command.logger, 'info') as mock_log, \
             patch.object(command, '_list_databases', 
                         return_value={"databases": {}}):
            # Act
            command.execute(args)
            
            # Assert
            mock_log.assert_called_once_with(
                "Executing info command: databases"
            )


class TestInfoCommandParametrized:
    """Parametrized tests for InfoCommand functionality."""

    @pytest.mark.parametrize("info_type,target", [
        ("databases", None),
        ("database_info", "biorempp"),
        ("database_info", "hadeg"),
        ("database_info", "kegg"),
        ("database_info", "toxcsm"),
    ])
    def test_info_command_initialization_parametrized(self, info_type, target):
        """Test InfoCommand initialization with various parameters."""
        command = InfoCommand(info_type, target)
        
        assert command.info_type == info_type
        assert command.target == target

    @pytest.mark.parametrize("database_name", [
        "biorempp", "hadeg", "kegg", "toxcsm"
    ])
    @patch('builtins.print')
    def test_database_info_all_databases(self, mock_print, database_name):
        """Test database info for all supported databases."""
        command = InfoCommand("database_info", database_name)
        
        # Act
        result = command._show_database_info(database_name)
        
        # Assert
        assert "database_info" in result
        assert database_name in result["database_info"]
        assert "name" in result["database_info"][database_name]
        assert "size" in result["database_info"][database_name]


class TestInfoCommandIntegration:
    """Test InfoCommand integration scenarios."""

    def test_full_databases_listing_workflow(self):
        """Test complete database listing workflow."""
        command = InfoCommand("databases")
        args = Mock()
        
        # Mock common validation (should pass for info commands)
        with patch.object(command, 'validate_common_input'):
            # Act
            result = command.run(args)
            
            # Assert
            assert "databases" in result
            assert len(result["databases"]) == 4

    def test_full_database_info_workflow(self):
        """Test complete database info workflow."""
        command = InfoCommand("database_info", "biorempp")
        args = Mock()
        
        # Mock common validation
        with patch.object(command, 'validate_common_input'):
            # Act
            result = command.run(args)
            
            # Assert
            assert "database_info" in result
            assert "biorempp" in result["database_info"]

    def test_command_reusability(self):
        """Test that InfoCommand instances can be reused."""
        command = InfoCommand("databases")
        args = Mock()
        
        with patch.object(command, 'validate_common_input'):
            # Execute multiple times
            result1 = command.run(args)
            result2 = command.run(args)
            
            # Both should succeed and return same structure
            assert "databases" in result1
            assert "databases" in result2
