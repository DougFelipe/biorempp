"""
Output Formatter for BioRemPP CLI Interface.

This module provides centralized output formatting for all command types,
separating presentation logic from business logic following SRP.
"""

import argparse
from typing import Any, Dict, Union

from biorempp.utils.logging_config import get_logger


class OutputFormatter:
    """
    Centralized output formatter for BioRemPP CLI interface.

    Handles formatting and display of results from all command types:
    - Traditional pipeline results (single/multiple outputs)
    - Modular pipeline results (DataFrame summaries)
    - Info command results (module listings)

    This design centralizes all presentation logic and makes it easy
    to add new output formats (JSON, XML, etc.) in the future.

    SOLUTION for Risk: Template Method vs Application Responsibility
    - Commands return raw data without formatting concerns
    - Application uses OutputFormatter to handle all presentation
    - Clean separation between data processing and presentation
    """

    def __init__(self):
        """Initialize output formatter with logger."""
        self.logger = get_logger(self.__class__.__name__)

    def format_output(self, result: Any, args: argparse.Namespace) -> None:
        """
        Main output formatting dispatcher.

        Routes output formatting based on argument type and command results.

        Parameters
        ----------
        result : Any
            Command execution results
        args : argparse.Namespace
            Parsed command line arguments for context
        """
        self.logger.debug("Formatting output based on command type")

        # Route to appropriate formatter based on command type
        if getattr(args, "list_modules", False):
            self._format_modules_list(result)
        elif getattr(args, "enable_modular", False):
            self._format_modular_output(result)
        else:
            self._format_traditional_output(result, args)

    def _format_traditional_output(
        self, result: Union[str, Dict[str, str]], args: argparse.Namespace
    ) -> None:
        """
        Format traditional pipeline output.

        Handles both single pipeline outputs (string path) and
        multiple pipeline outputs (dictionary of paths).

        Parameters
        ----------
        result : Union[str, Dict[str, str]]
            Pipeline output path(s)
        args : argparse.Namespace
            Command arguments for context
        """
        self.logger.debug("Formatting traditional pipeline output")

        if isinstance(result, dict):
            # Multiple pipelines (e.g., from 'all' pipeline type)
            print("[BioRemPP] All processing pipelines completed successfully:")
            for pipeline_name, output_path in result.items():
                print(f"  [{pipeline_name.upper()}] Output: {output_path}")
        else:
            # Single pipeline
            print(f"[BioRemPP] Output processed and saved to: {result}")

    def _format_modular_output(self, result: Dict[str, Any]) -> None:
        """
        Format modular pipeline output.

        Displays summary information and details for each processor
        executed in the modular pipeline.

        Parameters
        ----------
        result : Dict[str, Any]
            Modular pipeline results summary
        """
        self.logger.debug("Formatting modular pipeline output")

        print("[BioRemPP] Modular Pipeline Results:")
        print(f"  Processors run: {result['processors_run']}")
        print(f"  Successful: {result['successful_processors']}")

        # Print details for each processor
        for processor_name, details in result["processor_details"].items():
            if details["success"]:
                processor_name_upper = processor_name.upper()
                print(
                    f"  [{processor_name_upper}] Processing completed - "
                    f"{details['rows_processed']} rows processed"
                )
                print("    Columns: {}".format(", ".join(details["columns"])))
                if "data_shape" in details:
                    print(f"    Data shape: {details['data_shape']}")
                if "memory_usage_mb" in details:
                    print(f"    Memory usage: {details['memory_usage_mb']} MB")
                print("    DataFrame available for external analysis and visualization")
            else:
                processor_name_upper = processor_name.upper()
                print(f"  [{processor_name_upper}] Processing failed")
                if "error" in details:
                    print(f"    Error: {details['error']}")

    def _format_modules_list(self, result: Dict[str, Any]) -> None:
        """
        Format available modules list output.

        Displays all available analysis modules with descriptions.

        Parameters
        ----------
        result : Dict[str, Any]
            Modules information from InfoCommand
        """
        self.logger.debug("Formatting modules list output")

        total_modules = result.get("total_modules", 0)
        modules = result.get("modules", {})

        print("[BioRemPP] Available Modules:")
        print(f"Data Processors ({total_modules}):")

        for name, info in modules.items():
            description = info.get("description", "No description available")
            print(f"  - {name}: {description}")

            # Show error if module failed to load
            if "error" in info:
                print(f"    Warning: {info['error']}")

    def print_error_message(self, error: Exception) -> None:
        """
        Format and print error messages.

        Parameters
        ----------
        error : Exception
            Exception that occurred during execution
        """
        self.logger.debug("Formatting error message")
        print(f"[ERROR] {error}")

    def print_interruption_message(self) -> None:
        """Format and print interruption message."""
        self.logger.debug("Formatting interruption message")
        print("\n[BioRemPP] Process interrupted by user")
