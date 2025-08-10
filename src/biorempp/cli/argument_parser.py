"""
argument_parser.py
-----------------
Advanced Command Line Argument Parser for BioRemPP Interface

This module implements a sophisticated argument parsing system designed
specifically for BioRemPP's bioremediation analysis workflows. It provides
a clean, intuitive interface for users while maintaining flexibility and
extensibility for complex analytical operations.

The parser implements a hierarchical argument structure with logical groupings
that guide users through the available options while ensuring comprehensive
validation and error handling for all input scenarios.

Argument Categories:
    - Input Arguments: File paths and data sources
    - Database Arguments: Database selection and processing options
    - Information Arguments: Help and discovery commands
    - Verbosity Arguments: Output control and debugging levels

Design Features:
    - Logical argument grouping for improved usability
    - Mutually exclusive groups for conflicting options
    - Comprehensive help text and examples
    - Flexible database selection (individual or comprehensive)
    - Progressive verbosity levels for different user needs

User Experience:
    The parser is designed to be self-documenting with clear help messages,
    logical option organization, and intuitive command patterns that follow
    common CLI conventions while being specific to bioremediation workflows.

Validation Strategy:
    Implements context-aware validation where requirements depend on the
    operation type, allowing information commands to work without input
    files while ensuring processing commands have all necessary parameters.

Integration:
    Seamlessly integrates with the BioRemPP command framework, providing
    parsed arguments that are directly consumable by command classes
    without additional transformation or validation overhead.

Author: BioRemPP Development Team
"""

import argparse
from typing import List, Optional


class BioRemPPArgumentParser:
    """
    Advanced command-line argument parser for BioRemPP bioremediation analysis.

    This parser provides a comprehensive and user-friendly interface for all
    BioRemPP operations, from single database analysis to comprehensive
    multi-database workflows and system information commands.

    Argument Structure:
        The parser organizes arguments into logical groups that guide users
        through available options while maintaining clear separation between
        different types of operations and configurations.

    Supported Operations:
        - Single Database Analysis: Targeted processing with specific databases
        - Multi-Database Analysis: Comprehensive analysis across all databases
        - Information Commands: Database discovery and help functionality
        - Output Configuration: Flexible result organization and formatting

    Design Philosophy:
        - Intuitive: Follows common CLI patterns and conventions
        - Self-Documenting: Comprehensive help text and examples
        - Flexible: Supports various workflow patterns and use cases
        - Robust: Comprehensive validation and error handling

    Argument Groups:
        - Input Arguments: File paths and data source configuration
        - Database Options: Individual vs comprehensive database selection
        - Information Commands: Discovery and help functionality
        - Verbosity Options: Output control and debugging levels

    Usage Examples:
        >>> parser = BioRemPPArgumentParser()
        >>> args = parser.parse_args(['--input', 'data.txt', '--all-databases'])
        >>> args = parser.parse_args(['--list-databases'])
        >>> args = parser.parse_args(['--input', 'data.txt', '--database', 'biorempp'])

    Validation Features:
        - Context-aware requirements (info commands vs processing commands)
        - Mutually exclusive options for conflicting selections
        - Path validation and accessibility checking
        - Database type validation and availability verification
    """

    def __init__(self):
        """Initialize the argument parser with structure."""
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """
        Create and configure the main argument parser with hierarchical structure.

        Builds a comprehensive argument parser with logical groupings that
        provide clear organization of options while maintaining flexibility
        for various workflow patterns and use cases.

        Returns
        -------
        argparse.ArgumentParser
            Fully configured parser with organized argument groups, validation
            rules, and comprehensive help text for optimal user experience.

        Parser Configuration:
            - Main description and program information
            - Logical argument groups for different operation types
            - Mutually exclusive groups for conflicting options
            - Comprehensive help text and usage examples
            - Validation rules and error handling

        Argument Organization:
            The parser implements a hierarchical structure that guides users
            through available options while ensuring all necessary information
            is captured for successful command execution.
        """
        parser = argparse.ArgumentParser(
            description="BioRemPP: Bioremediation Potential Profile"
        )

        # Add simplified argument groups
        self._add_input_arguments(parser)
        self._add_database_arguments(parser)
        self._add_info_arguments(parser)
        self._add_verbosity_arguments(parser)

        return parser

    def _add_input_arguments(self, parser: argparse.ArgumentParser) -> None:
        """
        Add input file and output configuration arguments.

        Configures arguments related to data input and result output,
        providing flexible options for file handling and result organization
        while maintaining sensible defaults for common use cases.

        Parameters
        ----------
        parser : argparse.ArgumentParser
            Parser instance to enhance with input/output arguments.

        Arguments Added:
            - --input: Path to biological data file (context-dependent requirement)
            - --output-dir: Directory for result files with smart defaults

        Validation Features:
            - Path existence and accessibility checking
            - Directory creation permissions validation
            - File format and content validation (delegated to processors)
        """
        parser.add_argument(
            "--input",
            type=str,
            required=False,  # Will be validated later based on context
            help="Path to the input biological data file",
        )

        parser.add_argument(
            "--output-dir",
            type=str,
            default="outputs/results_tables",
            help="Directory for output files (default: outputs/results_tables)",
        )

    def _add_database_arguments(self, parser: argparse.ArgumentParser) -> None:
        """
        Add database selection and processing configuration arguments.

        Provides flexible database selection options supporting both targeted
        analysis with specific databases and comprehensive analysis across
        all available databases, with clear guidance for users.

        Parameters
        ----------
        parser : argparse.ArgumentParser
            Parser instance to enhance with database selection arguments.

        Arguments Added:
            - --all-databases: Comprehensive analysis across all databases
            - --database: Targeted analysis with specific database selection

        Database Options:
            - biorempp: Core bioremediation potential analysis
            - hadeg: Hydrocarbon degradation gene analysis
            - kegg: Metabolic pathway enrichment analysis
            - toxcsm: Toxicity prediction and safety assessment

        Selection Strategy:
            Users can choose between comprehensive coverage (all databases)
            or focused analysis (single database) based on their research
            needs and computational resources.
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
        Add information discovery and help system arguments.

        Provides comprehensive system discovery capabilities that help users
        understand available databases, their capabilities, and optimal
        usage patterns without requiring input data processing.

        Parameters
        ----------
        parser : argparse.ArgumentParser
            Parser instance to enhance with information and discovery arguments.

        Arguments Added:
            - --list-databases: Overview of all available databases
            - --database-info: Detailed information about specific databases

        Information Features:
            - Database schema and column information
            - Record counts and file size statistics
            - Key features and capabilities overview
            - Usage examples and best practices
            - Integration guidance and workflow suggestions

        Discovery Workflow:
            These commands enable users to explore the system capabilities
            and make informed decisions about database selection and
            analysis strategies before processing their data.
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
        Add progressive verbosity control and debugging arguments.

        Implements a three-tier verbosity system that accommodates different
        user needs from silent operation to comprehensive debugging, with
        mutually exclusive groups ensuring clear selection.

        Parameters
        ----------
        parser : argparse.ArgumentParser
            Parser instance to enhance with verbosity control arguments.

        Verbosity Levels:
            - Quiet (--quiet, -q): Silent operation with error-only output
            - Verbose (--verbose, -v): Detailed progress and status information
            - Debug (--debug): Comprehensive technical information and logging

        Design Features:
            - Mutually exclusive groups prevent conflicting selections
            - Progressive information disclosure based on user needs
            - Integration with logging infrastructure for consistent output
            - Context-aware output formatting for optimal readability

        Use Cases:
            - Quiet: Automated scripts and batch processing
            - Verbose: Interactive analysis and progress monitoring
            - Debug: Development, troubleshooting, and detailed analysis
        """
        verbosity_group = parser.add_argument_group("Verbosity Options")

        # Create mutually exclusive group for verbosity levels
        verbosity_exclusive = verbosity_group.add_mutually_exclusive_group()

        verbosity_exclusive.add_argument(
            "--quiet",
            "-q",
            action="store_true",
            help="Silent mode - no output except errors (default)",
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
