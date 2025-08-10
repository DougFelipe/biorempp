"""
BioRemPP Application Orchestrator Module.

This module serves as the central application orchestrator for BioRemPP,
implementing the main entry point and execution flow coordination.
It provides comprehensive dependency injection, error handling,
and component orchestration following clean architecture principles.

Key Features
-----------
- Dependency injection architecture for all major components
- Centralized error handling with detailed logging and user feedback
- Clean separation of concerns between parsing, execution, and output
- Comprehensive exception handling with appropriate exit codes
- Professional logging system with file-based technical logs

Architecture
-----------
The application follows the orchestrator pattern:
1. BioRemPPArgumentParser: CLI argument parsing and validation
2. CommandFactory: Command pattern implementation for operations
3. OutputFormatter: Consistent output formatting and presentation
4. EnhancedErrorHandler: Professional error handling and recovery
5. UserFeedbackManager: User-friendly feedback and progress indication

Components Integration
---------------------
- Main orchestrator coordinates all BioRemPP components
- Implements clean dependency injection for testability
- Provides centralized exception handling with proper exit codes
- Manages application lifecycle from initialization to completion

Example Usage
------------
    from biorempp.app.application import BioRemPPApplication

    # Create and run application
    app = BioRemPPApplication()
    result = app.run([
        '--all-databases',
        '--input', 'samples.txt',
        '--output-dir', 'results'
    ])

    # Custom dependency injection
    custom_parser = BioRemPPArgumentParser()
    custom_factory = CommandFactory()
    app = BioRemPPApplication(
        parser=custom_parser,
        command_factory=custom_factory
    )

Error Handling Strategy
----------------------
- KeyboardInterrupt: Exit code 130 (standard Ctrl+C)
- ValueError: Exit code 1 (validation and input errors)
- FileNotFoundError: Exit code 2 (missing files and paths)
- PermissionError: Exit code 3 (access and permission issues)
- Exception: Exit code 1 (unexpected errors with full logging)

Technical Notes
--------------
- Uses file-based logging for technical details
- Implements comprehensive exception handling
- Supports verbosity control through CLI arguments
- Provides version information and metadata access
"""

import sys
from typing import Any, Dict, List, Optional

from biorempp.app.command_factory import CommandFactory
from biorempp.cli.argument_parser import BioRemPPArgumentParser
from biorempp.cli.output_formatter import OutputFormatter


class BioRemPPApplication:
    """
    Main application orchestrator for BioRemPP.

    Coordinates all components using dependency injection architecture.
    Implements clean separation of concerns and comprehensive error handling
    for professional bioinformatics data processing workflows.

    This class serves as the central coordinator that manages:
    - Argument parsing via BioRemPPArgumentParser
    - Command creation and execution via CommandFactory
    - Output formatting via OutputFormatter
    - Centralized error handling and professional logging
    - User feedback management with appropriate verbosity levels

    The design implements clean architecture principles making
    the entire application easily testable through dependency injection
    and modular component design.

    Attributes
    ----------
    parser : BioRemPPArgumentParser
        CLI argument parser for command validation and processing
    command_factory : CommandFactory
        Factory for creating appropriate command instances
    output_formatter : OutputFormatter
        Consistent output formatting and presentation
    logger : logging.Logger
        File-based technical logging for debugging and monitoring
    error_handler : EnhancedErrorHandler
        Professional error handling with user-friendly messages
    feedback_manager : UserFeedbackManager
        User feedback system with verbosity control

    Error Handling Distribution
    --------------------------
    - All exceptions handled at application level
    - Consistent error formatting and exit codes
    - Technical details logged to files
    - User-friendly messages displayed to console
    - Proper exit codes for different error types

    Exit Codes
    ----------
    - 0: Successful execution
    - 1: General errors (validation, unexpected exceptions)
    - 2: File not found errors
    - 3: Permission errors
    - 130: User interruption (Ctrl+C)

    Example
    -------
    >>> app = BioRemPPApplication()
    >>> result = app.run(['--all-databases', '--input', 'data.txt'])
    """

    def __init__(
        self,
        parser: Optional[BioRemPPArgumentParser] = None,
        command_factory: Optional[CommandFactory] = None,
        output_formatter: Optional[OutputFormatter] = None,
    ):
        """
        Initialize application with dependency injection support.

        Sets up all major components using dependency injection pattern
        for enhanced testability and modularity. Creates default instances
        if none provided, enabling both production and testing scenarios.

        The initialization process:
        1. Sets up core components (parser, factory, formatter)
        2. Configures file-based technical logging system
        3. Initializes enhanced error handling components
        4. Prepares user feedback management system

        Parameters
        ----------
        parser : Optional[BioRemPPArgumentParser], default=None
            CLI argument parser instance. Creates default if None.
            Handles command line argument parsing and validation.
        command_factory : Optional[CommandFactory], default=None
            Command factory instance. Creates default if None.
            Manages command pattern implementation for operations.
        output_formatter : Optional[OutputFormatter], default=None
            Output formatter instance. Creates default if None.
            Handles consistent output formatting and presentation.

        Technical Setup
        ---------------
        - Configures file-based logging with daily rotation
        - Sets up enhanced error handling with user-friendly messages
        - Initializes feedback manager with verbosity control
        - Creates output directory structure for logs

        Logging Configuration
        --------------------
        - File path: outputs/logs/biorempp_YYYYMMDD.log
        - Format: timestamp | level | logger | function | message
        - Level: DEBUG for comprehensive technical details
        - Encoding: UTF-8 for international character support
        - No console propagation to avoid duplicate output

        Example
        -------
        >>> # Default initialization
        >>> app = BioRemPPApplication()

        >>> # Custom dependency injection
        >>> parser = BioRemPPArgumentParser()
        >>> factory = CommandFactory()
        >>> app = BioRemPPApplication(parser=parser, command_factory=factory)
        """
        self.parser = parser or BioRemPPArgumentParser()
        self.command_factory = command_factory or CommandFactory()
        self.output_formatter = output_formatter or OutputFormatter()

        # Technical logging (file only)
        import logging

        self.logger = logging.getLogger("biorempp.application")

        # Setup file-only handler
        if not self.logger.handlers:
            from datetime import datetime
            from pathlib import Path

            # Create logs directory
            log_dir = Path("outputs/logs")
            log_dir.mkdir(parents=True, exist_ok=True)

            # Setup file logging only
            log_file = log_dir / f"biorempp_{datetime.now().strftime('%Y%m%d')}.log"

            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_formatter = logging.Formatter(
                "%(asctime)s | %(levelname)-8s | %(name)-25s | "
                "%(funcName)-15s | %(message)s"
            )
            file_handler.setFormatter(file_formatter)
            file_handler.setLevel(logging.DEBUG)

            self.logger.addHandler(file_handler)
            self.logger.setLevel(logging.DEBUG)
            self.logger.propagate = False  # Prevent console output

        # Initialize enhanced components
        from ..utils.error_handler import EnhancedErrorHandler
        from ..utils.user_feedback import UserFeedbackManager

        self.error_handler = EnhancedErrorHandler()
        self.feedback_manager = UserFeedbackManager()

    def run(self, args: Optional[List[str]] = None) -> Any:
        """
        Main application entry point and execution orchestrator.

        Orchestrates the complete BioRemPP execution flow with comprehensive
        error handling and user feedback. Implements the main application
        lifecycle from argument parsing to result presentation.

        The execution flow follows these steps:
        1. Parse and validate command line arguments
        2. Configure verbosity levels for user feedback
        3. Create appropriate command instance via factory pattern
        4. Execute command with proper error handling
        5. Format and present results to user
        6. Handle all exceptions with appropriate exit codes

        Parameters
        ----------
        args : Optional[List[str]], default=None
            Command line arguments list. Uses sys.argv if None.
            Should contain valid BioRemPP command arguments.

        Returns
        -------
        Any
            Command execution results. Type depends on executed command:
            - InfoCommand: Database information dictionaries
            - DatabaseMergerCommand: Processing results and file paths
            - AllDatabasesMergerCommand: Comprehensive analysis results

        Raises
        ------
        SystemExit
            On errors or user interruption with appropriate exit codes:
            - 1: General errors (validation, unexpected exceptions)
            - 2: File not found errors
            - 3: Permission errors
            - 130: User interruption (Ctrl+C)

        Error Handling Strategy
        ----------------------
        - KeyboardInterrupt: Graceful handling of user interruption
        - ValueError: Input validation and argument errors
        - FileNotFoundError: Missing input files or database issues
        - PermissionError: File access and directory permission issues
        - Exception: Unexpected errors with full stack trace logging

        Verbosity Configuration
        ----------------------
        - verbose flag: Detailed progress information
        - debug flag: Comprehensive technical details
        - default: Quiet mode with essential information only

        Example
        -------
        >>> app = BioRemPPApplication()
        >>> # Process all databases
        >>> result = app.run([
        ...     '--all-databases',
        ...     '--input', 'samples.txt',
        ...     '--output-dir', 'results',
        ...     '--verbose'
        ... ])

        >>> # Process single database
        >>> result = app.run([
        ...     '--database', 'biorempp',
        ...     '--input', 'samples.txt'
        ... ])

        Technical Notes
        ---------------
        - All exceptions logged to file with full stack traces
        - User feedback provided through UserFeedbackManager
        - Exit codes follow UNIX conventions
        - Supports both interactive and batch execution modes
        """
        try:
            self.logger.info("Starting BioRemPP application")

            # Step 1: Parse arguments
            parsed_args = self.parser.parse_args(args)
            self.logger.debug(f"Parsed arguments: {vars(parsed_args)}")

            # Configure verbosity level for feedback manager
            if hasattr(parsed_args, "verbose") and parsed_args.verbose:
                self.feedback_manager.set_verbosity("verbose")
            elif hasattr(parsed_args, "debug") and parsed_args.debug:
                self.feedback_manager.set_verbosity("debug")
            else:
                # Default to quiet mode
                self.feedback_manager.set_verbosity("quiet")

            # Step 2: Create appropriate command
            command = self.command_factory.create_command(parsed_args)
            command_type = self.command_factory.get_command_type(parsed_args)
            self.logger.info(
                f"Created {command_type} command: {command.__class__.__name__}"
            )

            # Step 3: Execute command
            result = command.run(parsed_args)

            # Step 4: Format output (only for processing commands, not info commands)
            if command_type != "info":
                self.output_formatter.format_output(result, parsed_args)

            self.logger.info("BioRemPP application completed successfully")
            return result

        except KeyboardInterrupt:
            self.logger.info("Process interrupted by user")
            self.feedback_manager.error("[ERROR] Processo interrompido pelo usuário")
            sys.exit(130)  # Standard exit code for Ctrl+C

        except ValueError as e:
            self.logger.error(f"Validation error: {e}")
            args_context = parsed_args if "parsed_args" in locals() else None
            error_msg, solution_text = self.error_handler.handle_error(e, args_context)
            self.feedback_manager.error(f"[ERROR] {error_msg}")
            if solution_text:
                self.feedback_manager.info(f"[INFO] {solution_text}")
            sys.exit(1)

        except FileNotFoundError as e:
            self.logger.error(f"File not found: {e}")
            args_context = parsed_args if "parsed_args" in locals() else None
            error_msg, solution_text = self.error_handler.handle_error(e, args_context)
            self.feedback_manager.error(f"[ERROR] {error_msg}")
            if solution_text:
                self.feedback_manager.info(f"[INFO] {solution_text}")
            sys.exit(2)

        except PermissionError as e:
            self.logger.error(f"Permission error: {e}")
            args_context = parsed_args if "parsed_args" in locals() else None
            error_msg, solution_text = self.error_handler.handle_error(e, args_context)
            self.feedback_manager.error(f"[ERROR] {error_msg}")
            if solution_text:
                self.feedback_manager.info(f"[INFO] {solution_text}")
            sys.exit(3)

        except Exception as e:
            self.logger.error(f"Unexpected error: {e}", exc_info=True)
            args_context = parsed_args if "parsed_args" in locals() else None
            error_msg, solution_text = self.error_handler.handle_error(e, args_context)
            self.feedback_manager.error(f"[ERROR] {error_msg}")
            if solution_text:
                self.feedback_manager.info(f"[INFO] {solution_text}")
            sys.exit(1)

    def get_version_info(self) -> Dict[str, str]:
        """
        Get comprehensive application version and metadata information.

        Retrieves version information from the metadata module and provides
        comprehensive application details for version reporting, debugging,
        and user information purposes.

        The version information includes:
        - Application version number (from metadata or 'development')
        - Application name and description
        - Build and release information when available

        Returns
        -------
        Dict[str, str]
            Version information dictionary with keys:
            - 'version': Version string (e.g., '1.0.0' or 'development')
            - 'application': Application name ('BioRemPP')
            - 'description': Brief application description

        Fallback Behavior
        -----------------
        If version metadata is not available (development mode):
        - Returns 'development' as version
        - Maintains consistent structure for all environments
        - Enables version checking in both production and development

        Example
        -------
        >>> app = BioRemPPApplication()
        >>> version_info = app.get_version_info()
        >>> print(f"BioRemPP v{version_info['version']}")
        BioRemPP v1.0.0

        >>> # Access full information
        >>> for key, value in version_info.items():
        ...     print(f"{key}: {value}")
        version: 1.0.0
        application: BioRemPP
        description: Bioremediation Potential Profile

        Technical Notes
        ---------------
        - Attempts import from biorempp.metadata.version module
        - Graceful fallback for development environments
        - Consistent return structure regardless of environment
        - Supports version checking and debugging workflows
        """
        # Import version from metadata if available
        try:
            from biorempp.metadata.version import __version__

            return {
                "version": __version__,
                "application": "BioRemPP",
                "description": "Bioremediation Potential Profile",
            }
        except ImportError:
            return {
                "version": "development",
                "application": "BioRemPP",
                "description": "Bioremediation Potential Profile",
            }
