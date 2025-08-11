"""
Unit tests for the biorempp.app.command_factory module.

This module contains comprehensive tests for the CommandFactory class,
covering command creation, routing logic, argument validation, and
factory pattern implementation for the BioRemPP command architecture.

Test Categories
--------------
- Factory initialization and configuration
- Command creation and routing logic
- Argument validation and error handling
- Command type detection and inspection
- Factory pattern implementation validation
- Integration with different command types

The tests ensure proper factory behavior across all supported command
types, validation scenarios, and error conditions while maintaining
clean factory pattern implementation and comprehensive validation.
"""

import argparse
from unittest.mock import Mock, patch

import pytest

from biorempp.app.command_factory import CommandFactory
from biorempp.commands.all_merger_command import AllDatabasesMergerCommand
from biorempp.commands.info_command import InfoCommand
from biorempp.commands.single_merger_command import DatabaseMergerCommand


class TestCommandFactoryInitialization:
    """Test suite for CommandFactory initialization and setup."""

    def test_factory_default_initialization(self):
        """
        Test factory initialization with default configuration.

        Verifies that the factory initializes properly with default
        logger configuration and required components.
        """
        # Act
        factory = CommandFactory()

        # Assert
        assert hasattr(factory, 'logger')
        assert factory.logger is not None

    @patch('biorempp.app.command_factory.get_logger')
    def test_factory_logger_configuration(self, mock_get_logger):
        """
        Test factory logger configuration during initialization.

        Verifies that the factory properly configures its logger
        with appropriate settings for debugging and monitoring.
        """
        # Arrange
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger

        # Act
        factory = CommandFactory()

        # Assert
        mock_get_logger.assert_called_once_with('CommandFactory')
        assert factory.logger == mock_logger


class TestCommandFactoryCreation:
    """Test suite for CommandFactory command creation logic."""

    def test_create_info_command_list_databases(self):
        """
        Test creation of InfoCommand for database listing.

        Verifies that the factory creates appropriate InfoCommand
        when list_databases flag is specified.
        """
        # Arrange
        args = argparse.Namespace(
            list_databases=True,
            database_info=None,
            all_databases=False,
            database=None
        )

        # Act
        command = CommandFactory.create_command(args)

        # Assert
        assert isinstance(command, InfoCommand)

    def test_create_info_command_database_info(self):
        """
        Test creation of InfoCommand for specific database information.

        Verifies that the factory creates appropriate InfoCommand
        when database_info parameter is specified.
        """
        # Arrange
        args = argparse.Namespace(
            list_databases=False,
            database_info='biorempp',
            all_databases=False,
            database=None
        )

        # Act
        command = CommandFactory.create_command(args)

        # Assert
        assert isinstance(command, InfoCommand)

    def test_create_all_databases_merger_command(self):
        """
        Test creation of AllDatabasesMergerCommand.

        Verifies that the factory creates appropriate AllDatabasesMergerCommand
        when all_databases flag is specified with required input.
        """
        # Arrange
        args = argparse.Namespace(
            list_databases=False,
            database_info=None,
            all_databases=True,
            database=None,
            input='test.txt'
        )

        # Act
        command = CommandFactory.create_command(args)

        # Assert
        assert isinstance(command, AllDatabasesMergerCommand)

    def test_create_single_database_merger_command(self):
        """
        Test creation of DatabaseMergerCommand for single database.

        Verifies that the factory creates appropriate DatabaseMergerCommand
        when database parameter is specified with required input.
        """
        # Arrange
        args = argparse.Namespace(
            list_databases=False,
            database_info=None,
            all_databases=False,
            database='biorempp',
            input='test.txt'
        )

        # Act
        command = CommandFactory.create_command(args)

        # Assert
        assert isinstance(command, DatabaseMergerCommand)
        assert hasattr(args, 'pipeline_type')
        assert args.pipeline_type == 'biorempp'

    def test_create_command_priority_info_over_merger(self):
        """
        Test command creation priority with info commands over merger.

        Verifies that info commands take priority over merger commands
        when multiple flags are specified.
        """
        # Arrange
        args = argparse.Namespace(
            list_databases=True,
            database_info=None,
            all_databases=True,
            database='biorempp',
            input='test.txt'
        )

        # Act
        command = CommandFactory.create_command(args)

        # Assert
        assert isinstance(command, InfoCommand)

    def test_create_command_priority_all_over_single(self):
        """
        Test command creation priority with all databases over single.

        Verifies that all databases commands take priority over single
        database commands when both are specified.
        """
        # Arrange
        args = argparse.Namespace(
            list_databases=False,
            database_info=None,
            all_databases=True,
            database='biorempp',
            input='test.txt'
        )

        # Act
        command = CommandFactory.create_command(args)

        # Assert
        assert isinstance(command, AllDatabasesMergerCommand)


class TestCommandFactoryValidation:
    """Test suite for CommandFactory argument validation."""

    def test_all_databases_merger_requires_input(self):
        """
        Test validation for all databases merger requiring input file.

        Verifies that the factory raises appropriate error when
        all_databases is specified without input file.
        """
        # Arrange
        args = argparse.Namespace(
            list_databases=False,
            database_info=None,
            all_databases=True,
            database=None,
            input=None
        )

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            CommandFactory.create_command(args)

        assert "All databases merger requires --input file" in str(exc_info.value)

    def test_single_database_merger_requires_input(self):
        """
        Test validation for single database merger requiring input file.

        Verifies that the factory raises appropriate error when
        database is specified without input file.
        """
        # Arrange
        args = argparse.Namespace(
            list_databases=False,
            database_info=None,
            all_databases=False,
            database='biorempp',
            input=None
        )

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            CommandFactory.create_command(args)

        assert "Database merger requires --input file" in str(exc_info.value)

    def test_no_valid_command_specified(self):
        """
        Test validation when no valid command is specified.

        Verifies that the factory raises appropriate error with
        helpful message when no valid command configuration is provided.
        """
        # Arrange
        args = argparse.Namespace(
            list_databases=False,
            database_info=None,
            all_databases=False,
            database=None
        )

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            CommandFactory.create_command(args)

        assert "No valid command specified" in str(exc_info.value)
        assert "--help" in str(exc_info.value)

    def test_info_commands_no_input_required(self):
        """
        Test that info commands do not require input file validation.

        Verifies that info commands can be created without input
        file specification, unlike merger commands.
        """
        # Arrange
        args_list = argparse.Namespace(
            list_databases=True,
            database_info=None,
            all_databases=False,
            database=None,
            input=None
        )
        
        args_info = argparse.Namespace(
            list_databases=False,
            database_info='biorempp',
            all_databases=False,
            database=None,
            input=None
        )

        # Act & Assert
        # Both should succeed without input file
        command_list = CommandFactory.create_command(args_list)
        command_info = CommandFactory.create_command(args_info)

        assert isinstance(command_list, InfoCommand)
        assert isinstance(command_info, InfoCommand)


class TestCommandFactoryTypeDetection:
    """Test suite for CommandFactory command type detection."""

    def test_get_command_type_info_list_databases(self):
        """
        Test command type detection for info list databases.

        Verifies that the factory correctly identifies info command
        type for database listing operations.
        """
        # Arrange
        args = argparse.Namespace(
            list_databases=True,
            database_info=None,
            all_databases=False,
            database=None
        )

        # Act
        command_type = CommandFactory.get_command_type(args)

        # Assert
        assert command_type == "info"

    def test_get_command_type_info_database_info(self):
        """
        Test command type detection for info database information.

        Verifies that the factory correctly identifies info command
        type for specific database information operations.
        """
        # Arrange
        args = argparse.Namespace(
            list_databases=False,
            database_info='biorempp',
            all_databases=False,
            database=None
        )

        # Act
        command_type = CommandFactory.get_command_type(args)

        # Assert
        assert command_type == "info"

    def test_get_command_type_all_databases(self):
        """
        Test command type detection for all databases merger.

        Verifies that the factory correctly identifies all databases
        command type for multi-database processing.
        """
        # Arrange
        args = argparse.Namespace(
            list_databases=False,
            database_info=None,
            all_databases=True,
            database=None
        )

        # Act
        command_type = CommandFactory.get_command_type(args)

        # Assert
        assert command_type == "all_databases"

    def test_get_command_type_single_database(self):
        """
        Test command type detection for single database merger.

        Verifies that the factory correctly identifies single database
        command type for specific database processing.
        """
        # Arrange
        args = argparse.Namespace(
            list_databases=False,
            database_info=None,
            all_databases=False,
            database='biorempp'
        )

        # Act
        command_type = CommandFactory.get_command_type(args)

        # Assert
        assert command_type == "single_database"

    def test_get_command_type_unknown(self):
        """
        Test command type detection for unknown/invalid configuration.

        Verifies that the factory correctly identifies unknown command
        type for invalid or unrecognized configurations.
        """
        # Arrange
        args = argparse.Namespace(
            list_databases=False,
            database_info=None,
            all_databases=False,
            database=None
        )

        # Act
        command_type = CommandFactory.get_command_type(args)

        # Assert
        assert command_type == "unknown"

    def test_get_command_type_priority_consistency(self):
        """
        Test command type detection priority consistency.

        Verifies that command type detection follows the same priority
        rules as command creation for consistent behavior.
        """
        # Arrange - Multiple flags set to test priority
        args = argparse.Namespace(
            list_databases=True,
            database_info='test',
            all_databases=True,
            database='biorempp'
        )

        # Act
        command_type = CommandFactory.get_command_type(args)

        # Assert
        # Should prioritize info commands
        assert command_type == "info"


class TestCommandFactoryParametrizedTests:
    """Test suite for CommandFactory with parametrized test scenarios."""

    @pytest.mark.parametrize("database_name", [
        "biorempp", "kegg", "hadeg", "toxcsm"
    ])
    def test_create_single_database_commands_parametrized(self, database_name):
        """
        Test creation of single database commands for all supported databases.

        Verifies that the factory can create DatabaseMergerCommand for
        all supported database types with proper configuration.
        """
        # Arrange
        args = argparse.Namespace(
            list_databases=False,
            database_info=None,
            all_databases=False,
            database=database_name,
            input='test.txt'
        )

        # Act
        command = CommandFactory.create_command(args)

        # Assert
        assert isinstance(command, DatabaseMergerCommand)
        assert args.pipeline_type == database_name

    @pytest.mark.parametrize("info_type,expected_args", [
        ("list_databases", {"list_databases": True, "database_info": None}),
        ("database_info", {"list_databases": False, "database_info": "biorempp"}),
    ])
    def test_create_info_commands_parametrized(self, info_type, expected_args):
        """
        Test creation of info commands for different information types.

        Verifies that the factory can create InfoCommand for all
        supported information request types.
        """
        # Arrange
        args = argparse.Namespace(
            all_databases=False,
            database=None,
            **expected_args
        )

        # Act
        command = CommandFactory.create_command(args)

        # Assert
        assert isinstance(command, InfoCommand)

    @pytest.mark.parametrize("command_config,expected_type", [
        ({"list_databases": True}, "info"),
        ({"database_info": "test"}, "info"),
        ({"all_databases": True}, "all_databases"),
        ({"database": "biorempp"}, "single_database"),
        ({}, "unknown"),
    ])
    def test_command_type_detection_parametrized(
        self, command_config, expected_type
    ):
        """
        Test command type detection for various argument configurations.

        Verifies that command type detection works correctly across
        all supported command configuration scenarios.
        """
        # Arrange
        default_args = {
            "list_databases": False,
            "database_info": None,
            "all_databases": False,
            "database": None
        }
        default_args.update(command_config)
        args = argparse.Namespace(**default_args)

        # Act
        command_type = CommandFactory.get_command_type(args)

        # Assert
        assert command_type == expected_type


class TestCommandFactoryIntegration:
    """Test suite for CommandFactory integration and lifecycle testing."""

    @patch('biorempp.app.command_factory.get_logger')
    def test_factory_logging_integration(self, mock_get_logger):
        """
        Test factory integration with logging system.

        Verifies that the factory properly integrates with the logging
        system for debugging and monitoring capabilities.
        """
        # Arrange
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        
        args = argparse.Namespace(
            list_databases=True,
            database_info=None,
            all_databases=False,
            database=None
        )

        # Act
        factory = CommandFactory()
        with patch.object(factory.logger, 'debug'):
            with patch.object(factory.logger, 'info'):
                command = factory.create_command(args)

                # Assert
                assert isinstance(command, InfoCommand)
                # Verify logging was called during factory initialization
                assert mock_get_logger.call_count >= 1

    def test_factory_stateless_operation(self):
        """
        Test factory stateless operation and thread safety.

        Verifies that the factory operates in a stateless manner
        and can be used safely across multiple command creations.
        """
        # Arrange
        args1 = argparse.Namespace(
            list_databases=True,
            database_info=None,
            all_databases=False,
            database=None
        )
        
        args2 = argparse.Namespace(
            list_databases=False,
            database_info=None,
            all_databases=False,
            database='biorempp',
            input='test.txt'
        )

        # Act
        command1 = CommandFactory.create_command(args1)
        command2 = CommandFactory.create_command(args2)

        # Assert
        assert isinstance(command1, InfoCommand)
        assert isinstance(command2, DatabaseMergerCommand)
        # Verify that commands are independent instances
        assert command1 is not command2

    def test_factory_classmethod_accessibility(self):
        """
        Test factory classmethod accessibility and usage.

        Verifies that factory methods can be used as classmethods
        without requiring factory instance creation.
        """
        # Arrange
        args = argparse.Namespace(
            list_databases=True,
            database_info=None,
            all_databases=False,
            database=None
        )

        # Act
        # Test both classmethod and instance method access
        command_from_class = CommandFactory.create_command(args)
        command_type_from_class = CommandFactory.get_command_type(args)
        
        factory_instance = CommandFactory()
        command_from_instance = factory_instance.create_command(args)
        command_type_from_instance = factory_instance.get_command_type(args)

        # Assert
        assert isinstance(command_from_class, InfoCommand)
        assert isinstance(command_from_instance, InfoCommand)
        assert command_type_from_class == "info"
        assert command_type_from_instance == "info"

    def test_factory_argument_mutation_handling(self):
        """
        Test factory handling of argument namespace mutations.

        Verifies that the factory properly handles modifications
        to argument namespaces during command creation.
        """
        # Arrange
        args = argparse.Namespace(
            list_databases=False,
            database_info=None,
            all_databases=False,
            database='biorempp',
            input='test.txt'
        )
        original_database = args.database

        # Act
        command = CommandFactory.create_command(args)

        # Assert
        assert isinstance(command, DatabaseMergerCommand)
        # Verify that factory added pipeline_type attribute
        assert hasattr(args, 'pipeline_type')
        assert args.pipeline_type == original_database
        # Verify original attributes remain unchanged
        assert args.database == original_database

    def test_factory_error_handling_integration(self):
        """
        Test factory error handling integration with validation.

        Verifies that the factory provides comprehensive error
        handling with detailed error messages for invalid configurations.
        """
        # Arrange
        invalid_configs = [
            # All databases without input
            argparse.Namespace(
                list_databases=False,
                database_info=None,
                all_databases=True,
                database=None,
                input=None
            ),
            # Single database without input
            argparse.Namespace(
                list_databases=False,
                database_info=None,
                all_databases=False,
                database='biorempp',
                input=None
            ),
            # No command specified
            argparse.Namespace(
                list_databases=False,
                database_info=None,
                all_databases=False,
                database=None
            )
        ]

        # Act & Assert
        for config in invalid_configs:
            with pytest.raises(ValueError) as exc_info:
                CommandFactory.create_command(config)
            
            # Verify that error messages are helpful
            error_msg = str(exc_info.value)
            assert len(error_msg) > 0
            assert any(keyword in error_msg.lower() for keyword in [
                "requires", "specified", "help", "input", "command"
            ])
