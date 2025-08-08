"""
BioRemPP Argument Parser for Command Line Interface.

This module provides a clean, modular approach to CLI argument parsing,
organized by functional groups for better maintainability and testing.
"""

import argparse
from typing import List, Optional


class BioRemPPArgumentParser:
    """
    Modular argument parser for BioRemPP CLI interface.

    Organizes CLI arguments into logical groups for better maintainability:
    - Input arguments: file paths and data sources
    - Pipeline arguments: processing type selection
    - Database arguments: database file configurations
    - Output arguments: output directory and file configurations
    - Modular arguments: modular processing options
    - Info arguments: help and information commands

    This design allows for easy extension and modification of CLI interface
    without affecting other components.
    """

    def __init__(self):
        """Initialize the argument parser with modular structure."""
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """
        Create and configure the main argument parser.

        Returns
        -------
        argparse.ArgumentParser
            Configured parser with all argument groups
        """
        parser = argparse.ArgumentParser(
            description="BioRemPP: Modular Bioinformatics Data Processing Tool"
        )

        # Add all argument groups
        self._add_input_arguments(parser)
        self._add_pipeline_arguments(parser)
        self._add_database_arguments(parser)
        self._add_output_arguments(parser)
        self._add_modular_arguments(parser)
        self._add_info_arguments(parser)

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
            help="Path to the input file containing the data to be processed",
        )

    def _add_pipeline_arguments(self, parser: argparse.ArgumentParser) -> None:
        """
        Add pipeline type selection arguments.

        Parameters
        ----------
        parser : argparse.ArgumentParser
            Parser to add arguments to
        """
        parser.add_argument(
            "--pipeline-type",
            type=str,
            choices=["all", "biorempp", "kegg", "hadeg", "toxcsm"],
            default="all",
            help="Type of processing pipeline to run (default: all)",
        )

    def _add_database_arguments(self, parser: argparse.ArgumentParser) -> None:
        """
        Add database configuration arguments.

        Parameters
        ----------
        parser : argparse.ArgumentParser
            Parser to add arguments to
        """
        parser.add_argument(
            "--database",
            type=str,
            help="Path to the main database file (overrides specific database paths)",
        )

        parser.add_argument(
            "--biorempp-database", type=str, help="Path to the BioRemPP database file"
        )

        parser.add_argument(
            "--kegg-database", type=str, help="Path to the KEGG database file"
        )

        parser.add_argument(
            "--hadeg-database", type=str, help="Path to the HAdeg database file"
        )

        parser.add_argument(
            "--toxcsm-database", type=str, help="Path to the ToxCSM database file"
        )

    def _add_output_arguments(self, parser: argparse.ArgumentParser) -> None:
        """
        Add output configuration arguments.

        Parameters
        ----------
        parser : argparse.ArgumentParser
            Parser to add arguments to
        """
        parser.add_argument(
            "--output-dir",
            type=str,
            default="outputs/results_tables",
            help="Directory to save output files (default: outputs/results_tables)",
        )

        parser.add_argument(
            "--output-filename",
            type=str,
            help="Custom filename for the main output file",
        )

        parser.add_argument(
            "--biorempp-output-filename",
            type=str,
            help="Custom filename for BioRemPP output",
        )

        parser.add_argument(
            "--kegg-output-filename", type=str, help="Custom filename for KEGG output"
        )

        parser.add_argument(
            "--hadeg-output-filename", type=str, help="Custom filename for HAdeg output"
        )

        parser.add_argument(
            "--toxcsm-output-filename",
            type=str,
            help="Custom filename for ToxCSM output",
        )

        # File format options
        parser.add_argument(
            "--sep",
            type=str,
            default=";",
            help="Separator character for output files (default: ;)",
        )

        # Timestamp options
        timestamp_group = parser.add_mutually_exclusive_group()
        timestamp_group.add_argument(
            "--add-timestamp",
            action="store_true",
            default=False,
            help="Add timestamp to output filenames",
        )

        timestamp_group.add_argument(
            "--no-timestamp",
            action="store_false",
            dest="add_timestamp",
            help="Do not add timestamp to output filenames (default)",
        )

    def _add_modular_arguments(self, parser: argparse.ArgumentParser) -> None:
        """
        Add modular processing arguments.

        Parameters
        ----------
        parser : argparse.ArgumentParser
            Parser to add arguments to
        """
        parser.add_argument(
            "--enable-modular",
            action="store_true",
            help=(
                "Enable modular processing pipeline "
                "(returns DataFrames for external use)"
            ),
        )

        parser.add_argument(
            "--processors",
            nargs="+",
            help="List of data processors to run in modular mode "
            "(e.g., gene_pathway_analyzer compound_class_analyzer)",
        )

    def _add_info_arguments(self, parser: argparse.ArgumentParser) -> None:
        """
        Add information and help arguments.

        Parameters
        ----------
        parser : argparse.ArgumentParser
            Parser to add arguments to
        """
        parser.add_argument(
            "--list-modules",
            action="store_true",
            help="List all available processing modules and exit",
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
