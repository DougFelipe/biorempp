"""
Unit tests for the biorempp.app.application module.

This module contains comprehensive tests for the BioRemPPApplication class,
covering application orchestration, dependency injection, error handling,
and the complete execution lifecycle.

Test Categories
--------------
- Application initialization and dependency injection
- Main execution flow and argument processing
- Error handling and exception management
- Verbosity configuration and user feedback
- Version information and metadata retrieval
- Integration with CLI components and command factory

The tests ensure proper application behavior across different scenarios,
error conditions, and configuration options while maintaining clean
architecture principles and comprehensive error handling.
"""

import argparse
from unittest.mock import Mock, patch

import pytest

from biorempp.app.application import BioRemPPApplication
from biorempp.app.command_factory import CommandFactory
from biorempp.cli.argument_parser import BioRemPPArgumentParser
from biorempp.cli.output_formatter import OutputFormatter


class TestBioRemPPApplicationInitialization:
    """Test suite for BioRemPP application initialization and setup."""

    def test_application_default_initialization(self):
        """
        Test application initialization with default dependencies.

        Verifies that the application creates appropriate default instances
        for all required components when no dependencies are injected.
        """
        # Act
        app = BioRemPPApplication()

        # Assert
        assert isinstance(app.parser, BioRemPPArgumentParser)
        assert isinstance(app.command_factory, CommandFactory)
        assert isinstance(app.output_formatter, OutputFormatter)
        assert app.logger.name == "biorempp.application"

    def test_application_dependency_injection(self):
        """
        Test application initialization with custom dependency injection.

        Verifies that the application properly accepts and uses custom
        instances for all injectable dependencies.
        """
        # Arrange
        custom_parser = Mock(spec=BioRemPPArgumentParser)
        custom_factory = Mock(spec=CommandFactory)
        custom_formatter = Mock(spec=OutputFormatter)

        # Act
        app = BioRemPPApplication(
            parser=custom_parser,
            command_factory=custom_factory,
            output_formatter=custom_formatter
        )

        # Assert
        assert app.parser is custom_parser
        assert app.command_factory is custom_factory
        assert app.output_formatter is custom_formatter

    def test_application_partial_dependency_injection(self):
        """
        Test application initialization with partial dependency injection.

        Verifies that the application creates defaults for missing
        dependencies while using provided custom instances.
        """
        # Arrange
        custom_parser = Mock(spec=BioRemPPArgumentParser)

        # Act
        app = BioRemPPApplication(parser=custom_parser)

        # Assert
        assert app.parser is custom_parser
        assert isinstance(app.command_factory, CommandFactory)
        assert isinstance(app.output_formatter, OutputFormatter)

    @patch('pathlib.Path.mkdir')
    @patch('logging.FileHandler')
    def test_application_logging_setup(self, mock_file_handler, mock_mkdir):
        """
        Test application logging configuration during initialization.

        Verifies that the logging system is properly configured with
        file-based handlers and appropriate formatting.
        """
        # Arrange
        mock_handler = Mock()
        mock_file_handler.return_value = mock_handler

        # Act
        app = BioRemPPApplication()

        # Assert
        # Verify logger is created and configured
        assert hasattr(app, 'logger')
        assert app.logger.name == "biorempp.application"
        
        # Verify directory creation was called
        assert mock_mkdir.call_count >= 1
        mock_mkdir.assert_called_with(parents=True, exist_ok=True)

    def test_application_enhanced_components_initialization(self):
        """
        Test initialization of enhanced components.

        Verifies that error handler and feedback manager are properly
        initialized as part of the application setup.
        """
        # Act
        app = BioRemPPApplication()

        # Assert
        assert hasattr(app, 'error_handler')
        assert hasattr(app, 'feedback_manager')
        assert app.error_handler is not None
        assert app.feedback_manager is not None


class TestBioRemPPApplicationExecution:
    """Test suite for BioRemPP application main execution flow."""

    def test_successful_execution_with_info_command(self):
        """
        Test successful application execution with info command.

        Verifies that the application properly handles info commands
        and returns results without formatting.
        """
        # Arrange
        app = BioRemPPApplication()
        mock_args = argparse.Namespace(
            list_databases=True,
            verbose=False,
            debug=False
        )

        with patch.object(app.parser, 'parse_args', return_value=mock_args):
            with patch.object(
                app.command_factory, 'create_command'
            ) as mock_create:
                with patch.object(
                    app.command_factory,
                    'get_command_type',
                    return_value='info'
                ):
                    mock_command = Mock()
                    mock_command.run.return_value = {"databases": ["biorempp"]}
                    mock_create.return_value = mock_command

                    # Act
                    result = app.run(['--list-databases'])

                    # Assert
                    assert result == {"databases": ["biorempp"]}
                    mock_command.run.assert_called_once_with(mock_args)

    def test_successful_execution_with_merger_command(self):
        """
        Test successful application execution with merger command.

        Verifies that the application properly handles merger commands,
        executes them, and formats the output.
        """
        # Arrange
        app = BioRemPPApplication()
        mock_args = argparse.Namespace(
            database='biorempp',
            input='test.txt',
            verbose=False,
            debug=False
        )

        with patch.object(app.parser, 'parse_args', return_value=mock_args):
            with patch.object(
                app.command_factory, 'create_command'
            ) as mock_create:
                with patch.object(
                    app.command_factory,
                    'get_command_type',
                    return_value='single_database'
                ):
                    with patch.object(
                        app.output_formatter, 'format_output'
                    ) as mock_format:
                        mock_command = Mock()
                        mock_command.run.return_value = {"result": "processed"}
                        mock_create.return_value = mock_command

                        # Act
                        result = app.run([
                            '--database', 'biorempp', '--input', 'test.txt'
                        ])

                        # Assert
                        assert result == {"result": "processed"}
                        mock_command.run.assert_called_once_with(mock_args)
                        mock_format.assert_called_once_with(
                            {"result": "processed"}, mock_args
                        )

    def test_verbosity_configuration_verbose(self):
        """
        Test verbosity configuration for verbose mode.

        Verifies that the application properly configures the feedback
        manager for verbose output mode.
        """
        # Arrange
        app = BioRemPPApplication()
        mock_args = argparse.Namespace(
            list_databases=True,
            verbose=True,
            debug=False
        )

        with patch.object(app.parser, 'parse_args', return_value=mock_args):
            with patch.object(
                app.command_factory, 'create_command'
            ) as mock_create:
                with patch.object(
                    app.command_factory,
                    'get_command_type',
                    return_value='info'
                ):
                    with patch.object(
                        app.feedback_manager, 'set_verbosity'
                    ) as mock_verbosity:
                        mock_command = Mock()
                        mock_command.run.return_value = {}
                        mock_create.return_value = mock_command

                        # Act
                        app.run(['--list-databases', '--verbose'])

                        # Assert
                        mock_verbosity.assert_called_once_with("verbose")

    def test_verbosity_configuration_debug(self):
        """
        Test verbosity configuration for debug mode.

        Verifies that the application properly configures the feedback
        manager for debug output mode.
        """
        # Arrange
        app = BioRemPPApplication()
        mock_args = argparse.Namespace(
            list_databases=True,
            verbose=False,
            debug=True
        )

        with patch.object(app.parser, 'parse_args', return_value=mock_args):
            with patch.object(
                app.command_factory, 'create_command'
            ) as mock_create:
                with patch.object(
                    app.command_factory,
                    'get_command_type',
                    return_value='info'
                ):
                    with patch.object(
                        app.feedback_manager, 'set_verbosity'
                    ) as mock_verbosity:
                        mock_command = Mock()
                        mock_command.run.return_value = {}
                        mock_create.return_value = mock_command

                        # Act
                        app.run(['--list-databases', '--debug'])

                        # Assert
                        mock_verbosity.assert_called_once_with("debug")

    def test_verbosity_configuration_quiet_default(self):
        """
        Test verbosity configuration for quiet (default) mode.

        Verifies that the application defaults to quiet mode when no
        verbosity flags are specified.
        """
        # Arrange
        app = BioRemPPApplication()
        mock_args = argparse.Namespace(
            list_databases=True,
            verbose=False,
            debug=False
        )

        with patch.object(app.parser, 'parse_args', return_value=mock_args):
            with patch.object(
                app.command_factory, 'create_command'
            ) as mock_create:
                with patch.object(
                    app.command_factory,
                    'get_command_type',
                    return_value='info'
                ):
                    with patch.object(
                        app.feedback_manager, 'set_verbosity'
                    ) as mock_verbosity:
                        mock_command = Mock()
                        mock_command.run.return_value = {}
                        mock_create.return_value = mock_command

                        # Act
                        app.run(['--list-databases'])

                        # Assert
                        mock_verbosity.assert_called_once_with("quiet")


class TestBioRemPPApplicationErrorHandling:
    """Test suite for BioRemPP application error handling and exceptions."""

    def test_keyboard_interrupt_handling(self):
        """
        Test handling of keyboard interrupt (Ctrl+C).

        Verifies that the application properly handles user interruption
        with appropriate exit code and user feedback.
        """
        # Arrange
        app = BioRemPPApplication()
        
        with patch.object(
            app.parser, 'parse_args', side_effect=KeyboardInterrupt
        ):
            with patch.object(app.feedback_manager, 'error') as mock_error:
                with pytest.raises(SystemExit) as exc_info:
                    # Act
                    app.run(['--list-databases'])

                # Assert
                assert exc_info.value.code == 130
                mock_error.assert_called_once()

    def test_value_error_handling(self):
        """
        Test handling of ValueError exceptions.

        Verifies that the application properly handles validation errors
        with appropriate exit code and error messaging.
        """
        # Arrange
        app = BioRemPPApplication()
        error_msg = "Invalid input value"
        
        with patch.object(
            app.parser, 'parse_args', side_effect=ValueError(error_msg)
        ):
            with patch.object(
                app.error_handler,
                'handle_error',
                return_value=("Error", "Solution")
            ):
                with patch.object(
                    app.feedback_manager, 'error'
                ) as mock_error:
                    with patch.object(
                        app.feedback_manager, 'info'
                    ) as mock_info:
                        with pytest.raises(SystemExit) as exc_info:
                            # Act
                            app.run(['--invalid'])

                        # Assert
                        assert exc_info.value.code == 1
                        mock_error.assert_called_once_with("[ERROR] Error")
                        mock_info.assert_called_once_with("[INFO] Solution")

    def test_file_not_found_error_handling(self):
        """
        Test handling of FileNotFoundError exceptions.

        Verifies that the application properly handles missing file errors
        with appropriate exit code and error messaging.
        """
        # Arrange
        app = BioRemPPApplication()
        error_msg = "File not found"
        
        with patch.object(
            app.parser,
            'parse_args',
            side_effect=FileNotFoundError(error_msg)
        ):
            with patch.object(
                app.error_handler,
                'handle_error',
                return_value=("File Error", "Check path")
            ):
                with patch.object(
                    app.feedback_manager, 'error'
                ) as mock_error:
                    with patch.object(
                        app.feedback_manager, 'info'
                    ) as mock_info:
                        with pytest.raises(SystemExit) as exc_info:
                            # Act
                            app.run(['--input', 'missing.txt'])

                        # Assert
                        assert exc_info.value.code == 2
                        mock_error.assert_called_once_with("[ERROR] File Error")
                        mock_info.assert_called_once_with("[INFO] Check path")

    def test_permission_error_handling(self):
        """
        Test handling of PermissionError exceptions.

        Verifies that the application properly handles permission errors
        with appropriate exit code and error messaging.
        """
        # Arrange
        app = BioRemPPApplication()
        error_msg = "Permission denied"
        
        with patch.object(
            app.parser,
            'parse_args',
            side_effect=PermissionError(error_msg)
        ):
            with patch.object(
                app.error_handler,
                'handle_error',
                return_value=("Permission Error", "Check access")
            ):
                with patch.object(
                    app.feedback_manager, 'error'
                ) as mock_error:
                    with patch.object(
                        app.feedback_manager, 'info'
                    ) as mock_info:
                        with pytest.raises(SystemExit) as exc_info:
                            # Act
                            app.run(['--output-dir', '/protected'])

                        # Assert
                        assert exc_info.value.code == 3
                        mock_error.assert_called_once_with(
                            "[ERROR] Permission Error"
                        )
                        mock_info.assert_called_once_with(
                            "[INFO] Check access"
                        )

    def test_unexpected_exception_handling(self):
        """
        Test handling of unexpected exceptions.

        Verifies that the application properly handles unexpected errors
        with appropriate exit code and comprehensive logging.
        """
        # Arrange
        app = BioRemPPApplication()
        error_msg = "Unexpected error"
        
        with patch.object(
            app.parser, 'parse_args', side_effect=RuntimeError(error_msg)
        ):
            with patch.object(
                app.error_handler,
                'handle_error',
                return_value=("Runtime Error", "Try again")
            ):
                with patch.object(
                    app.feedback_manager, 'error'
                ) as mock_error:
                    with patch.object(
                        app.feedback_manager, 'info'
                    ) as mock_info:
                        with pytest.raises(SystemExit) as exc_info:
                            # Act
                            app.run(['--list-databases'])

                        # Assert
                        assert exc_info.value.code == 1
                        mock_error.assert_called_once_with(
                            "[ERROR] Runtime Error"
                        )
                        mock_info.assert_called_once_with("[INFO] Try again")

    def test_error_handling_with_parsed_args_context(self):
        """
        Test error handling with parsed arguments context.

        Verifies that error handling properly provides parsed arguments
        context when available for better error reporting.
        """
        # Arrange
        app = BioRemPPApplication()
        mock_args = argparse.Namespace(database='biorempp', input='test.txt')
        
        with patch.object(app.parser, 'parse_args', return_value=mock_args):
            with patch.object(
                app.command_factory,
                'create_command',
                side_effect=ValueError("Command error")
            ):
                with patch.object(
                    app.error_handler,
                    'handle_error',
                    return_value=("Error message", "Solution text")
                ) as mock_handle:
                    with patch.object(app.feedback_manager, 'error'):
                        with pytest.raises(SystemExit):
                            # Act
                            app.run([
                                '--database', 'biorempp', '--input', 'test.txt'
                            ])

                        # Assert
                        # Verify that handle_error was called with parsed args
                        call_args = mock_handle.call_args
                        assert call_args[0][1] == mock_args


class TestBioRemPPApplicationVersionInfo:
    """Test suite for BioRemPP application version information."""

    def test_get_version_info_with_metadata(self):
        """
        Test version information retrieval with available metadata.

        Verifies that the application properly retrieves version information
        from the metadata module when available.
        """
        # Arrange
        app = BioRemPPApplication()

        with patch.object(
            app, 'get_version_info'
        ) as mock_version:
            mock_version.return_value = {
                "version": "1.0.0",
                "application": "BioRemPP",
                "description": "Bioremediation Potential Profile"
            }

            # Act
            version_info = app.get_version_info()

            # Assert
            assert version_info["version"] == "1.0.0"
            assert version_info["application"] == "BioRemPP"
            expected_desc = "Bioremediation Potential Profile"
            assert version_info["description"] == expected_desc

    def test_get_version_info_without_metadata(self):
        """
        Test version information retrieval without metadata (development).

        Verifies that the application provides fallback version information
        when metadata module is not available.
        """
        # Arrange
        app = BioRemPPApplication()

        with patch.object(
            app, 'get_version_info'
        ) as mock_version:
            mock_version.return_value = {
                "version": "development",
                "application": "BioRemPP",
                "description": "Bioremediation Potential Profile"
            }

            # Act
            version_info = app.get_version_info()

            # Assert
            assert version_info["version"] == "development"
            assert version_info["application"] == "BioRemPP"
            expected_desc = "Bioremediation Potential Profile"
            assert version_info["description"] == expected_desc

    def test_version_info_structure_consistency(self):
        """
        Test consistency of version information structure.

        Verifies that version information always contains the expected
        keys regardless of metadata availability.
        """
        # Arrange
        app = BioRemPPApplication()

        # Act
        version_info = app.get_version_info()

        # Assert
        required_keys = {"version", "application", "description"}
        assert set(version_info.keys()) == required_keys
        assert all(isinstance(value, str) for value in version_info.values())


class TestBioRemPPApplicationIntegration:
    """Test suite for BioRemPP application component integration."""

    def test_complete_execution_flow_integration(self):
        """
        Test complete application execution flow integration.

        Verifies that all application components work together properly
        in a realistic execution scenario.
        """
        # Arrange
        app = BioRemPPApplication()
        test_args = [
            '--database', 'biorempp', '--input', 'test.txt', '--verbose'
        ]
        
        mock_parsed_args = argparse.Namespace(
            database='biorempp',
            input='test.txt',
            verbose=True,
            debug=False
        )
        
        mock_result = {
            "database": "biorempp",
            "processed_samples": 10,
            "output_file": "results.csv"
        }

        with patch.object(
            app.parser, 'parse_args', return_value=mock_parsed_args
        ):
            with patch.object(
                app.command_factory, 'create_command'
            ) as mock_create:
                with patch.object(
                    app.command_factory,
                    'get_command_type',
                    return_value='single_database'
                ):
                    with patch.object(
                        app.output_formatter, 'format_output'
                    ) as mock_format:
                        with patch.object(
                            app.feedback_manager, 'set_verbosity'
                        ) as mock_verbosity:
                            mock_command = Mock()
                            mock_command.run.return_value = mock_result
                            mock_create.return_value = mock_command

                            # Act
                            result = app.run(test_args)

                            # Assert
                            # Verify complete integration
                            app.parser.parse_args.assert_called_once_with(
                                test_args
                            )
                            mock_verbosity.assert_called_once_with("verbose")
                            mock_create.assert_called_once_with(
                                mock_parsed_args
                            )
                            mock_command.run.assert_called_once_with(
                                mock_parsed_args
                            )
                            mock_format.assert_called_once_with(
                                mock_result, mock_parsed_args
                            )
                            assert result == mock_result

    def test_application_with_custom_dependencies_integration(self):
        """
        Test application integration with custom injected dependencies.

        Verifies that the application properly integrates with custom
        dependencies and maintains proper execution flow.
        """
        # Arrange
        custom_parser = Mock(spec=BioRemPPArgumentParser)
        custom_factory = Mock(spec=CommandFactory)
        custom_formatter = Mock(spec=OutputFormatter)
        
        app = BioRemPPApplication(
            parser=custom_parser,
            command_factory=custom_factory,
            output_formatter=custom_formatter
        )
        
        mock_args = argparse.Namespace(
            list_databases=True, verbose=False, debug=False
        )
        mock_command = Mock()
        mock_command.run.return_value = {"databases": ["biorempp", "kegg"]}
        
        custom_parser.parse_args.return_value = mock_args
        custom_factory.create_command.return_value = mock_command
        custom_factory.get_command_type.return_value = 'info'

        # Act
        result = app.run(['--list-databases'])

        # Assert
        custom_parser.parse_args.assert_called_once_with(['--list-databases'])
        custom_factory.create_command.assert_called_once_with(mock_args)
        custom_factory.get_command_type.assert_called_once_with(mock_args)
        mock_command.run.assert_called_once_with(mock_args)
        assert result == {"databases": ["biorempp", "kegg"]}

    def test_logging_integration_during_execution(self):
        """
        Test logging integration during application execution.

        Verifies that logging properly captures execution flow information
        and technical details during application runtime.
        """
        # Arrange
        app = BioRemPPApplication()
        mock_args = argparse.Namespace(
            list_databases=True, verbose=False, debug=False
        )
        
        with patch.object(app.parser, 'parse_args', return_value=mock_args):
            with patch.object(
                app.command_factory, 'create_command'
            ) as mock_create:
                with patch.object(
                    app.command_factory,
                    'get_command_type',
                    return_value='info'
                ):
                    with patch.object(
                        app.logger, 'info'
                    ) as mock_log_info:
                        with patch.object(
                            app.logger, 'debug'
                        ) as mock_log_debug:
                            mock_command = Mock()
                            mock_command.run.return_value = {}
                            mock_create.return_value = mock_command

                            # Act
                            app.run(['--list-databases'])

                            # Assert
                            # Verify logging calls
                            mock_log_info.assert_any_call(
                                "Starting BioRemPP application"
                            )
                            mock_log_debug.assert_called_with(
                                f"Parsed arguments: {vars(mock_args)}"
                            )
                            mock_log_info.assert_any_call(
                                "BioRemPP application completed successfully"
                            )
