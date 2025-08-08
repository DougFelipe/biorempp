"""
BioRemPP Application Orchestrator.

This module implements the main application orchestrator that coordinates
all components using dependency injection and centralized error handling.
"""

import sys
from typing import Any, Dict, List, Optional

from biorempp.app.command_factory import CommandFactory
from biorempp.cli.argument_parser import BioRemPPArgumentParser
from biorempp.cli.output_formatter import OutputFormatter
from biorempp.utils.logging_config import get_logger


class BioRemPPApplication:
    """
    Main application orchestrator for BioRemPP.

    Coordinates all components using dependency injection:
    - Argument parsing via BioRemPPArgumentParser
    - Command creation via CommandFactory
    - Output formatting via OutputFormatter
    - Centralized error handling and logging

    This design implements clean separation of concerns and makes
    the entire application easily testable through dependency injection.

    SOLUTION for Risk: Error Handling Distribution
    - All exceptions handled at application level
    - Commands focus on business logic, not error presentation
    - Consistent error formatting and exit codes
    """

    def __init__(
        self,
        parser: Optional[BioRemPPArgumentParser] = None,
        command_factory: Optional[CommandFactory] = None,
        output_formatter: Optional[OutputFormatter] = None,
    ):
        """
        Initialize application with dependency injection.

        Parameters
        ----------
        parser : Optional[BioRemPPArgumentParser]
            Argument parser instance. Creates default if None.
        command_factory : Optional[CommandFactory]
            Command factory instance. Creates default if None.
        output_formatter : Optional[OutputFormatter]
            Output formatter instance. Creates default if None.
        """
        self.parser = parser or BioRemPPArgumentParser()
        self.command_factory = command_factory or CommandFactory()
        self.output_formatter = output_formatter or OutputFormatter()
        self.logger = get_logger(self.__class__.__name__)

    def run(self, args: Optional[List[str]] = None) -> Any:
        """
        Main application entry point.

        Orchestrates the complete execution flow:
        1. Parse command line arguments
        2. Create appropriate command via factory
        3. Execute command and capture results
        4. Format output via formatter
        5. Handle all exceptions with proper exit codes

        Parameters
        ----------
        args : Optional[List[str]]
            Command line arguments. Uses sys.argv if None.

        Returns
        -------
        Any
            Command execution results

        Raises
        ------
        SystemExit
            On errors or user interruption with appropriate exit codes
        """
        try:
            self.logger.info("Starting BioRemPP application")

            # Step 1: Parse arguments
            parsed_args = self.parser.parse_args(args)
            self.logger.debug(f"Parsed arguments: {vars(parsed_args)}")

            # Step 2: Create appropriate command
            command = self.command_factory.create_command(parsed_args)
            command_type = self.command_factory.get_command_type(parsed_args)
            self.logger.info(
                f"Created {command_type} command: {command.__class__.__name__}"
            )

            # Step 3: Execute command
            result = command.run(parsed_args)

            # Step 4: Format output
            self.output_formatter.format_output(result, parsed_args)

            self.logger.info("BioRemPP application completed successfully")
            return result

        except KeyboardInterrupt:
            self.logger.info("Process interrupted by user")
            self.output_formatter.print_interruption_message()
            sys.exit(130)  # Standard exit code for Ctrl+C

        except ValueError as e:
            self.logger.error(f"Validation error: {e}")
            self.output_formatter.print_error_message(e)
            sys.exit(1)

        except FileNotFoundError as e:
            self.logger.error(f"File not found: {e}")
            self.output_formatter.print_error_message(e)
            sys.exit(2)

        except PermissionError as e:
            self.logger.error(f"Permission error: {e}")
            self.output_formatter.print_error_message(e)
            sys.exit(3)

        except Exception as e:
            self.logger.error(f"Unexpected error: {e}", exc_info=True)
            self.output_formatter.print_error_message(e)
            sys.exit(1)

    def get_version_info(self) -> Dict[str, str]:
        """
        Get application version information.

        Returns
        -------
        Dict[str, str]
            Version information dictionary
        """
        # Import version from metadata if available
        try:
            from biorempp.metadata.version import __version__

            return {
                "version": __version__,
                "application": "BioRemPP",
                "description": "Modular Bioinformatics Data Processing Tool",
            }
        except ImportError:
            return {
                "version": "development",
                "application": "BioRemPP",
                "description": "Modular Bioinformatics Data Processing Tool",
            }
