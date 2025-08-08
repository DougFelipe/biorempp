"""
BioRemPP Simplified Argument Parser for Command Line Interface.

This module provides a simplified, focused approach to CLI argument parsing,
designed for the core database merging functionality.
"""

import argparse
from typing import List, Optional


class BioRemPPArgumentParser:
    """
    Simplified argument parser for BioRemPP CLI interface.

    Focuses on core database merging functionality:
    - Input arguments: biological data file paths
    - Database arguments: database selection (individual or all)
    - Info arguments: database information and help commands

    This simplified design provides a cleaner user experience while
    maintaining the robust architecture underneath.
    """

    def __init__(self):
        """Initialize the argument parser with simplified structure."""
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """
        Create and configure the main argument parser.

        Returns
        -------
        argparse.ArgumentParser
            Configured parser with simplified argument groups
        """
        parser = argparse.ArgumentParser(
            description="BioRemPP: Biological Data & Database Merger Engine"
        )

        # Add simplified argument groups
        self._add_input_arguments(parser)
        self._add_database_arguments(parser)
        self._add_info_arguments(parser)
        self._add_verbosity_arguments(parser)

        return parser

    def _add_input_arguments(self, parser: argparse.ArgumentParser) -> None:
        """
        Add input-related arguments.

        Parameters
        ----------
        parser : argparse.ArgumentParser
            Parser to add arguments to
        """
        parser.add_argument(
            "--input",
            type=str,
            required=False,  # Will be validated later based on context
            help="Path to the input biological data file (FASTA format)",
        )

        parser.add_argument(
            "--output-dir",
            type=str,
            default="outputs/results_tables",
            help="Directory for output files (default: outputs/results_tables)",
        )

    def _add_database_arguments(self, parser: argparse.ArgumentParser) -> None:
        """
        Add database selection arguments.

        Parameters
        ----------
        parser : argparse.ArgumentParser
            Parser to add arguments to
        """
        db_group = parser.add_argument_group("Database Options")

        # Option 1: All databases (novo padrão recomendado)
        db_group.add_argument(
            "--all-databases",
            action="store_true",
            help="Merge input with ALL databases (biorempp, hadeg, kegg, toxcsm)",
        )

        # Option 2: Specific database
        db_group.add_argument(
            "--database",
            choices=["biorempp", "hadeg", "kegg", "toxcsm"],
            help="Merge with specific database only",
        )

    def _add_info_arguments(self, parser: argparse.ArgumentParser) -> None:
        """
        Add information and help arguments.

        Parameters
        ----------
        parser : argparse.ArgumentParser
            Parser to add arguments to
        """
        info_group = parser.add_argument_group("Information Commands")

        # Info commands
        info_group.add_argument(
            "--list-databases", action="store_true", help="List all available databases"
        )

        info_group.add_argument(
            "--database-info",
            choices=["biorempp", "hadeg", "kegg", "toxcsm"],
            help="Show detailed information about a specific database",
        )

    def _add_verbosity_arguments(self, parser: argparse.ArgumentParser) -> None:
        """
        Add verbosity control arguments.

        Parameters
        ----------
        parser : argparse.ArgumentParser
            Parser to add arguments to
        """
        verbosity_group = parser.add_argument_group("Verbosity Options")

        # Create mutually exclusive group for verbosity levels
        verbosity_exclusive = verbosity_group.add_mutually_exclusive_group()

        verbosity_exclusive.add_argument(
            "--quiet",
            "-q",
            action="store_true",
            help="Silent mode - no output except errors (this is now default)",
        )

        verbosity_exclusive.add_argument(
            "--verbose",
            "-v",
            action="store_true",
            help="Verbose mode - detailed progress information",
        )

        verbosity_exclusive.add_argument(
            "--debug",
            action="store_true",
            help="Debug mode - technical information and file logging",
        )

    def parse_args(self, args: Optional[List[str]] = None) -> argparse.Namespace:
        """
        Parse command line arguments.

        Parameters
        ----------
        args : Optional[List[str]]
            List of arguments to parse. If None, uses sys.argv

        Returns
        -------
        argparse.Namespace
            Parsed arguments
        """
        return self.parser.parse_args(args)

    def get_parser(self) -> argparse.ArgumentParser:
        """
        Get the underlying ArgumentParser instance.

        Returns
        -------
        argparse.ArgumentParser
            The configured parser
        """
        return self.parser
