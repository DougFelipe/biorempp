"""
Command Factory for BioRemPP Simplified Command Pattern Implementation.

This module implements the Factory Pattern for creating appropriate
command instances based on parsed CLI arguments for the simplified architecture.
"""

import argparse

from biorempp.commands.all_databases_command import AllDatabasesMergerCommand
from biorempp.commands.base_command import BaseCommand
from biorempp.commands.info_command import InfoCommand
from biorempp.commands.merger_command import DatabaseMergerCommand
from biorempp.utils.silent_logging import get_logger


class CommandFactory:
    """
    Factory class for creating appropriate command instances.

    Implements the Factory Pattern for the simplified BioRemPP architecture,
    focusing on database merging functionality:
    - Info commands (--list-databases, --database-info)
    - All databases merger (--all-databases)
    - Single database merger (--database)

    This simplified design maintains the robust Factory Pattern while
    removing unnecessary complexity.
    """

    def __init__(self):
        """Initialize command factory with logger."""
        self.logger = get_logger(self.__class__.__name__)

    @classmethod
    def create_command(cls, args: argparse.Namespace) -> BaseCommand:
        """
        Create appropriate command instance based on arguments.

        Routes command creation based on simplified CLI arguments:
        1. Info commands (--list-databases, --database-info) -> InfoCommand
        2. All databases merger (--all-databases) -> AllDatabasesMergerCommand
        3. Single database merger (--database) -> DatabaseMergerCommand

        Parameters
        ----------
        args : argparse.Namespace
            Parsed command line arguments

        Returns
        -------
        BaseCommand
            Appropriate command instance for execution

        Raises
        ------
        ValueError
            If command configuration is invalid or conflicting
        """
        factory = cls()
        factory.logger.debug("Creating command based on simplified arguments")

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

        Useful for testing and debugging without creating actual instances.

        Parameters
        ----------
        args : argparse.Namespace
            Parsed command line arguments

        Returns
        -------
        str
            Command type name ('info', 'all_databases', 'single_database')
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
