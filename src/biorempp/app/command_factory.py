"""
Command Factory Module for BioRemPP Command Pattern Implementation.

This module implements the Factory Pattern for creating appropriate
command instances based on parsed CLI arguments. It serves as the
central command creation and routing system for BioRemPP operations.

Key Features
-----------
- Factory Pattern implementation for command creation
- Intelligent command routing based on CLI arguments
- Comprehensive argument validation and conflict detection
- Support for info, merger, and processing commands
- Clean separation between command creation and execution

Supported Commands
-----------------
1. InfoCommand: Database information and listing operations
   - --list-databases: List all available databases
   - --database-info: Get specific database information

2. AllDatabasesMergerCommand: Process all available databases
   - --all-databases: Comprehensive multi-database processing

3. DatabaseMergerCommand: Process single database
   - --database <name>: Single database processing and analysis

Architecture
-----------
The factory implements a clean routing system:
- Command type detection based on CLI arguments
- Validation of required parameters for each command type
- Proper error handling for invalid configurations
- Support for command type inspection without instantiation

Command Routing Logic
--------------------
1. Info commands (highest priority): --list-databases, --database-info
2. All databases merger: --all-databases with required --input
3. Single database merger: --database with required --input
4. Error handling: Invalid configurations raise ValueError

Technical Notes
--------------
- Uses silent logging for technical details
- Implements static methods for stateless operation
- Provides both command creation and type inspection
- Supports testing and debugging through type detection
"""

import argparse

from biorempp.commands.all_merger_command import AllDatabasesMergerCommand
from biorempp.commands.base_command import BaseCommand
from biorempp.commands.info_command import InfoCommand
from biorempp.commands.single_merger_command import DatabaseMergerCommand
from biorempp.utils.silent_logging import get_logger


class CommandFactory:
    """
    Factory class for creating appropriate command instances.

    Implements the Factory Pattern for the BioRemPP command architecture,
    providing intelligent command creation and routing based on parsed
    CLI arguments. Focuses on the core BioRemPP functionality:
    database information, merging, and processing operations.

    The factory maintains a clean separation between command creation
    logic and command execution, enabling better testability and
    maintainability of the overall application architecture.

    Supported Command Types
    ----------------------
    1. InfoCommand: Information and listing operations
       - Database listing (--list-databases)
       - Database details (--database-info <name>)

    2. AllDatabasesMergerCommand: Multi-database processing
       - All databases analysis (--all-databases)
       - Requires input file specification

    3. DatabaseMergerCommand: Single database processing
       - Specific database analysis (--database <name>)
       - Requires input file specification

    Command Priority
    ---------------
    1. Info commands (highest priority)
    2. All databases merger commands
    3. Single database merger commands
    4. Error handling for invalid configurations

    Validation Rules
    ---------------
    - Info commands: No additional requirements
    - Merger commands: Must specify --input file
    - Conflicting arguments: Proper error messages
    - Missing requirements: Clear validation feedback

    Attributes
    ----------
    logger : logging.Logger
        Silent logger for technical debugging and monitoring
    """

    def __init__(self):
        """
        Initialize command factory with logger configuration.

        Sets up the factory with a silent logger for technical debugging
        and monitoring purposes. The logger provides detailed information
        about command creation processes without interfering with user
        output or application feedback.

        Technical Setup
        ---------------
        - Configures silent logger for debugging purposes
        - Enables technical monitoring of command creation
        - Supports debugging and troubleshooting workflows
        - Maintains clean separation from user-facing output
        """
        self.logger = get_logger(self.__class__.__name__)

    @classmethod
    def create_command(cls, args: argparse.Namespace) -> BaseCommand:
        """
        Create appropriate command instance based on parsed arguments.

        Implements intelligent command routing and creation based on CLI
        arguments. Uses priority-based routing to determine the most
        appropriate command type and validates all requirements before
        instantiation.

        The routing logic follows this priority order:
        1. Info commands (--list-databases, --database-info)
        2. All databases merger (--all-databases)
        3. Single database merger (--database)
        4. Error handling for invalid configurations

        Parameters
        ----------
        args : argparse.Namespace
            Parsed command line arguments from BioRemPPArgumentParser.
            Must contain valid command configuration.

        Returns
        -------
        BaseCommand
            Appropriate command instance ready for execution:
            - InfoCommand: For database information operations
            - AllDatabasesMergerCommand: For multi-database processing
            - DatabaseMergerCommand: For single database processing

        Raises
        ------
        ValueError
            If command configuration is invalid, conflicting, or missing
            required parameters. Error messages provide clear guidance
            for correction.

        Command Routing Details
        ----------------------
        Info Commands:
            - --list-databases: Creates InfoCommand for database listing
            - --database-info <name>: Creates InfoCommand for specific info
            - No additional requirements or validation needed

        All Databases Merger:
            - --all-databases: Creates AllDatabasesMergerCommand
            - Requires: --input file specification
            - Validates: Input file parameter presence

        Single Database Merger:
            - --database <name>: Creates DatabaseMergerCommand
            - Requires: --input file specification
            - Sets: pipeline_type attribute for execution
            - Validates: Database name and input file parameters

        Technical Notes
        ---------------
        - Uses classmethod for stateless operation
        - Provides comprehensive argument validation
        - Sets required attributes for command execution
        - Enables testing without factory instantiation
        """
        factory = cls()
        factory.logger.debug("Creating command based on arguments")

        # Route 1: Info commands (highest priority)
        if getattr(args, "list_databases", False):
            factory.logger.info("Creating InfoCommand for database listing")
            return InfoCommand("databases")

        if getattr(args, "database_info", None):
            db_info = args.database_info
            factory.logger.info(f"Creating InfoCommand for database info: {db_info}")
            return InfoCommand("database_info", args.database_info)

        # Route 2: All databases merger
        if getattr(args, "all_databases", False):
            # Validate input file requirement
            if not getattr(args, "input", None):
                raise ValueError(
                    "All databases merger requires --input file to be specified."
                )

            factory.logger.info("Creating AllDatabasesMergerCommand")
            return AllDatabasesMergerCommand()

        # Route 3: Single database merger (--database only)
        database_name = getattr(args, "database", None)

        if database_name:
            # Validate input file requirement
            if not getattr(args, "input", None):
                raise ValueError(
                    "Database merger requires --input file to be specified."
                )

            # Set pipeline_type for the underlying pipeline execution
            args.pipeline_type = args.database

            factory.logger.info(
                f"Creating DatabaseMergerCommand for database: {database_name}"
            )
            return DatabaseMergerCommand()

        # Default: Show help or error
        raise ValueError(
            "No valid command specified. Use --help to see available options, "
            "or try: --all-databases, --database <name>, --list-databases"
        )

    @classmethod
    def get_command_type(cls, args: argparse.Namespace) -> str:
        """
        Get the command type that would be created for given arguments.

        Performs command type detection without creating actual command
        instances. Useful for testing, debugging, and validation workflows
        where command type information is needed without full instantiation.

        This method implements the same routing logic as create_command
        but returns only the command type identifier for inspection
        purposes.

        Parameters
        ----------
        args : argparse.Namespace
            Parsed command line arguments from BioRemPPArgumentParser.
            Used for command type detection only.

        Returns
        -------
        str
            Command type identifier:
            - 'info': For InfoCommand instances (--list-databases,
              --database-info)
            - 'all_databases': For AllDatabasesMergerCommand instances
              (--all-databases)
            - 'single_database': For DatabaseMergerCommand instances
              (--database)
            - 'unknown': For invalid or unrecognized configurations

        Command Type Detection
        ---------------------
        The detection follows the same priority as create_command:
        1. Info commands: Returns 'info'
        2. All databases commands: Returns 'all_databases'
        3. Single database commands: Returns 'single_database'
        4. Invalid configurations: Returns 'unknown'

        Use Cases
        ---------
        - Testing command routing logic without full instantiation
        - Debugging argument parsing and command selection
        - Validation workflows in development environments
        - Pre-execution command type verification

        Technical Notes
        ---------------
        - Stateless operation using classmethod
        - No validation of required parameters (unlike create_command)
        - Safe for use with incomplete argument configurations
        - Enables testing scenarios without full command setup
        """
        list_dbs = getattr(args, "list_databases", False)
        db_info = getattr(args, "database_info", None)
        if list_dbs or db_info:
            return "info"
        elif getattr(args, "all_databases", False):
            return "all_databases"
        elif getattr(args, "database", None):
            return "single_database"
        else:
            return "unknown"
