"""
Output Formatter for BioRemPP CLI Interface.

This module provides centralized output formatting for all command types,
separating presentation logic from business logic following SRP.
"""

import argparse
import os
import time
from typing import Any, Dict, Union

from biorempp.utils.enhanced_user_feedback import EnhancedFeedbackManager
from biorempp.utils.silent_logging import get_logger


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
        """Initialize output formatter with logger and enhanced feedback."""
        self.logger = get_logger(self.__class__.__name__)
        self.feedback_manager = EnhancedFeedbackManager()
        self.start_time = time.time()

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
        Format traditional pipeline output with enhanced design.

        Displays clean, user-friendly output following the
        LOGGING_SYSTEM_DESIGN.md specification for beautiful CLI interface.

        Parameters
        ----------
        result : Union[str, Dict[str, str]]
            Pipeline output path(s)
        args : argparse.Namespace
            Command arguments for context
        """
        self.logger.debug("Formatting traditional pipeline output")

        if isinstance(result, dict):
            # Check if it's a single database result or multiple databases
            if self._is_single_database_result(result):
                # Single database processing
                self._format_single_database_output(result, args)
            else:
                # Multiple databases processing
                self._format_multiple_databases_output(result, args)
        else:
            # Fallback for string results
            print(f"[BioRemPP] Output processed and saved to: {result}")

    def _is_single_database_result(self, result: Dict[str, Any]) -> bool:
        """
        Check if result is from a single database or multiple databases.

        Single database results have keys like: output_path, matches, filename
        Multiple database results have keys like: biorempp, hadeg, kegg, toxcsm
        """
        single_db_keys = {"output_path", "matches", "filename"}
        result_keys = set(result.keys())

        # If result has the typical single database keys, it's single
        if single_db_keys.issubset(result_keys):
            return True

        # If result has database names as keys, it's multiple
        database_names = {"biorempp", "hadeg", "kegg", "toxcsm"}
        if any(key in database_names for key in result_keys):
            return False

        # Default to single if uncertain
        return True

    def _format_single_database_output(
        self, result: Dict[str, Any], args: argparse.Namespace
    ) -> None:
        """Format output for single database processing."""
        # Determine which database was processed
        database = getattr(args, "database", "Unknown")
        db_display_name = {
            "biorempp": "BioRemPP",
            "hadeg": "HAdeg",
            "kegg": "KEGG",
            "toxcsm": "ToxCSM",
        }.get(database, database.upper())

        # Show header for single database
        print(f"\n🧬 BioRemPP - Processing with {db_display_name.upper()} Database")
        print("═" * 67)
        print()

        # Count identifiers from input
        input_file = getattr(args, "input", "")
        if input_file and os.path.exists(input_file):
            with open(input_file, "r", encoding="utf-8") as f:
                line_count = sum(1 for line in f if line.strip())
            print(
                f"📁 Loading input data...        "
                f"✅ {line_count:,} identifiers loaded"
            )
        else:
            print("📁 Loading input data...        ✅ Input loaded")
        print()

        # Show database processing
        matches = result.get("matches", 0)
        filename = result.get("filename", "Unknown")

        print(
            f"🔗 Connecting to {db_display_name.upper()}...    "
            f"✅ Database available"
        )
        print("⚙️  Processing data...          ████████████████████ 100%")
        print(f"💾 Saving results...            ✅ {filename}")
        print()

        # Show final summary
        elapsed_time = time.time() - self.start_time
        output_path = result.get("output_path", "")
        file_size = self._get_file_size(output_path) if output_path else "Unknown"

        print("🎉 Processing completed successfully!")
        print(f"   📊 Results: {matches:,} matches found")
        print(f"   📁 Output: {filename} ({file_size})")
        print(f"   ⏱️  Time: {elapsed_time:.1f} seconds")
        print()

    def _format_multiple_databases_output(
        self, result: Dict[str, Any], args: argparse.Namespace
    ) -> None:
        """Format output for multiple databases processing."""
        # Use enhanced feedback manager for multiple databases
        self.feedback_manager.show_header()

        # Count identifiers from input
        input_file = getattr(args, "input", "")
        if input_file and os.path.exists(input_file):
            with open(input_file, "r", encoding="utf-8") as f:
                line_count = sum(1 for line in f if line.strip())
            self.feedback_manager.show_input_loaded(line_count)
        else:
            self.feedback_manager.show_input_loaded(0)

        # Process databases with real data
        self.feedback_manager.show_database_processing(result)

        # Calculate actual time
        elapsed_time = time.time() - self.start_time

        # Show final summary with real data
        self.feedback_manager.show_final_summary(result, elapsed_time)

    def _get_file_size(self, file_path: str) -> str:
        """Get human-readable file size."""
        try:
            import os

            size_bytes = os.path.getsize(file_path)
            if size_bytes < 1024:
                return f"{size_bytes}B"
            elif size_bytes < 1024 * 1024:
                return f"{size_bytes // 1024}KB"
            else:
                return f"{size_bytes // (1024 * 1024)}MB"
        except (OSError, FileNotFoundError):
            return "Unknown"

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
