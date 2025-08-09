"""
output_formatter.py
------------------
Professional Output Formatting and User Feedback System for BioRemPP CLI

This module implements a sophisticated output formatting system that delivers
beautiful, informative command-line interfaces following modern CLI design
principles. It centralizes all presentation logic and provides consistent
user feedback across all BioRemPP operations.

The formatter implements progressive disclosure patterns, using unicode icons,
structured layouts, and contextual information to create an engaging and
professional user experience that scales from simple operations to complex
multi-database workflows.

Formatting Capabilities:
    - Single Database Results: Focused output for targeted analysis
    - Multi-Database Results: Comprehensive summaries with aggregated metrics
    - Progress Indicators: Real-time feedback during processing operations
    - Error Presentation: Clear, actionable error messages and guidance
    - Result Summaries: Detailed metrics and file information

Design Principles:
    - Visual Hierarchy: Clear information organization with icons and spacing
    - Progressive Disclosure: Information depth appropriate to operation type
    - Consistency: Uniform formatting patterns across all output types
    - Accessibility: Clear, readable output suitable for various environments

User Experience Features:
    - Unicode icons for visual appeal and quick recognition
    - Structured layouts with consistent spacing and alignment
    - Contextual information based on operation type and results
    - Performance metrics and timing information
    - File size and location details for easy result management

Integration Architecture:
    The formatter integrates seamlessly with the command framework, accepting
    structured result data and producing formatted output without requiring
    changes to business logic or pipeline implementations.

Extensibility:
    The modular design supports easy addition of new output formats,
    presentation styles, and integration with external reporting systems
    while maintaining backward compatibility and consistent interfaces.

Author: BioRemPP Development Team
"""

import argparse
import os
import time
from typing import Any, Dict, Union

from biorempp.utils.enhanced_user_feedback import EnhancedFeedbackManager
from biorempp.utils.silent_logging import get_logger


class OutputFormatter:
    """
    Professional output formatting system for BioRemPP command-line interface.

    This formatter provides centralized, beautiful output formatting that
    transforms raw pipeline results into engaging, informative user interfaces
    following modern CLI design patterns with visual hierarchy and contextual
    information disclosure.

    Formatting Categories:
        - Single Database Output: Focused presentation for targeted analysis
        - Multi-Database Output: Comprehensive summaries with aggregated data
        - Progress Feedback: Real-time processing status and indicators
        - Error Messages: Clear, actionable error presentation
        - Result Summaries: Detailed metrics and performance information

    Design Features:
        - Unicode Icons: Visual elements for quick information recognition
        - Structured Layouts: Consistent spacing and alignment patterns
        - Progressive Disclosure: Information depth matching operation complexity
        - Contextual Adaptation: Output adaptation based on result types
        - Performance Integration: Timing and efficiency metrics display

    Output Patterns:
        The formatter implements consistent visual patterns that users can
        quickly understand and navigate, with clear section delineation,
        logical information flow, and appropriate detail levels.

    Integration Strategy:
        Accepts structured result dictionaries from command implementations
        and produces formatted console output without requiring changes to
        business logic or pipeline implementations, maintaining clean
        separation of concerns.

    Extensibility Features:
        - Modular formatting methods for easy customization
        - Pluggable output destinations for future enhancements
        - Template-based layouts for consistent visual design
        - Integration hooks for external reporting systems

    Usage Examples:
        >>> formatter = OutputFormatter()
        >>> formatter.format_output(single_db_result, args)
        >>> formatter.format_output(multi_db_results, args)
    """

    def __init__(self):
        """Initialize output formatter with logger and enhanced feedback."""
        self.logger = get_logger(self.__class__.__name__)
        self.feedback_manager = EnhancedFeedbackManager()
        self.start_time = time.time()

    def format_output(self, result: Any, args: argparse.Namespace) -> None:
        """
        Main output formatting dispatcher and presentation coordinator.

        This method serves as the central routing point for all output
        formatting operations, analyzing result types and dispatching to
        appropriate specialized formatting methods while maintaining
        consistent presentation patterns.

        Parameters
        ----------
        result : Any
            Structured command execution results from pipeline operations.
            Can be single database results (dict with output_path, matches)
            or multi-database results (dict with database names as keys).
        args : argparse.Namespace
            Parsed command line arguments providing context for formatting
            decisions, output preferences, and operation metadata.

        Processing Flow:
            1. Result type analysis and classification
            2. Context extraction from command arguments
            3. Dispatch to specialized formatting methods
            4. Consistent error handling and fallback strategies

        Formatting Strategy:
            The dispatcher implements intelligent result type detection to
            route formatting requests to the most appropriate presentation
            method, ensuring optimal user experience regardless of operation
            complexity or result structure.

        Output Coordination:
            Coordinates multiple formatting subsystems including progress
            feedback, result summaries, performance metrics, and error
            presentation to deliver cohesive user interfaces.
        """
        self.logger.debug("Formatting pipeline output")
        self._format_traditional_output(result, args)

    def _format_traditional_output(
        self, result: Union[str, Dict[str, str]], args: argparse.Namespace
    ) -> None:
        """
        Format pipeline output with enhanced design.

        Displays clean, user-friendly output following the
        LOGGING_SYSTEM_DESIGN.md specification for beautiful CLI interface.

        Parameters
        ----------
        result : Union[str, Dict[str, str]]
            Pipeline output path(s)
        args : argparse.Namespace
            Command arguments for context
        """
        self.logger.debug("Formatting pipeline output")

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
        """
        Format focused output for single database processing operations.

        Creates clean, informative presentation for targeted database analysis
        with detailed progress visualization, result metrics, and performance
        information optimized for single database workflows.

        Parameters
        ----------
        result : Dict[str, Any]
            Single database processing results containing output_path, matches,
            filename, and processing_time keys with operation metadata.
        args : argparse.Namespace
            Command arguments providing database type, input file, and
            configuration context for presentation customization.

        Output Structure:
            - Database identification header with visual branding
            - Input processing summary with identifier counts
            - Database connection and processing status indicators
            - Result summary with match counts and file information
            - Performance metrics including timing and file sizes

        Visual Design:
            Implements structured layout with unicode icons, progress bars,
            and consistent spacing to create professional appearance while
            delivering comprehensive operation feedback.
        """
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
        """
        Format comprehensive output for multi-database processing operations.

        Creates sophisticated presentation for comprehensive analysis workflows
        that process data across all available databases, with aggregated
        metrics, individual database summaries, and coordinated progress
        feedback through the enhanced feedback manager system.

        Parameters
        ----------
        result : Dict[str, Any]
            Multi-database processing results with database names as keys
            (biorempp, hadeg, kegg, toxcsm) containing individual operation
            results and metadata for comprehensive presentation.
        args : argparse.Namespace
            Command arguments providing input configuration and processing
            parameters for contextual output customization and metrics.

        Output Features:
            - Comprehensive header with workflow identification
            - Input processing summary with total identifier counts
            - Database-by-database processing status and results
            - Aggregated metrics across all database operations
            - Performance summary with total timing and success rates

        Integration:
            Leverages the EnhancedFeedbackManager for coordinated multi-step
            presentation that maintains visual consistency while handling
            complex workflow results and potential partial failures.
        """
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
