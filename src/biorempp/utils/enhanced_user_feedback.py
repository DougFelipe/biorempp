"""
    BioRemPP Enhanced User Feedback Manager Module.

This module implements an user feedback system specifically designed
for command-line interface.
It provides sophisticated visual feedback, progress tracking, and status
presentation following CLI design principles with,
informative user interfaces.

Key Features
------------
------------
-----------
- CLI Interface: design with visual hierarchy
- Multi-Database Support: Specialized feedback for complex workflow coordination
- Progressive Disclosure: Information depth appropriate to operation complexity

Multi-Database Workflow Support
-------------------------------
-------------------------------
------------------------------
Specialized feedback for complex processing scenarios:
- Database Processing: Individual database progress and status tracking
- Workflow Coordination: Multi-step operation progress visualization
- Result Aggregation: Summary presentation with comprehensive metrics
- Error Handling: Error presentation with recovery guidance
- Performance Metrics: Timing and efficiency information display

Visual Design Elements
----------------------
----------------------
---------------------
Visual design components:
- Structured Headers: Clear section delineation with visual appeal
- Progress Indicators: Real-time progress visualization and status updates
- Result Summaries: Comprehensive result presentation with key metrics
- Status Messages:  Status communication with clear messaging

Interface Architecture
----------------------
----------------------
---------------------
Design for flexible interface composition:
- Header Components: Headers with branding and context
- Progress Components: Sophisticated progress tracking and visualization
- Summary Components: Comprehensive result and metrics presentation
- Status Components: Real-time status updates and notifications
- Error Components: Error presentation and guidance


Example Usage
-------------
-------------
------------
    from biorempp.utils.enhanced_user_feedback import EnhancedFeedbackManager

    # Initialize enhanced feedback
    feedback = EnhancedFeedbackManager()

    # Show professional header
    feedback.show_header()

    # Display input processing status
    feedback.show_input_loaded(23653)

    # Show database processing with results
    results = {
        'biorempp': {'matches': 7613, 'filename': 'BioRemPP_Results.txt'},
        'hadeg': {'matches': 1737, 'filename': 'HADEG_Results.txt'}
    }
    feedback.show_database_processing(results)

    # Display final summary
    feedback.show_final_summary(results, elapsed_time=1.2)
"""

from typing import Any, Dict


class EnhancedFeedbackManager:
    """
    Enhanced feedback manager for CLI interface.

    Provides structured, elegant output components following the design
    specification from LOGGING_SYSTEM_DESIGN.md.
    """

    def __init__(self, verbosity: str = "NORMAL"):
        """Initialize feedback manager."""
        self.verbosity = verbosity.upper()
        self.db_order = ["biorempp", "hadeg", "kegg", "toxcsm"]
        self.db_names = {
            "biorempp": "BioRemPP",
            "hadeg": "HAdeg",
            "kegg": "KEGG",
            "toxcsm": "ToxCSM",
        }

    def show_header(self) -> None:
        """Display the header."""
        if self.verbosity == "SILENT":
            return

        print("\n[BIOREMPP] Processing with ALL Databases")
        print("=" * 67)

        # Debug mode shows technical details
        if self.verbosity == "DEBUG":
            print(f"🔧 [DEBUG] Verbosity level: {self.verbosity}")
            print(f"🔧 [DEBUG] Available databases: {list(self.db_names.keys())}")
            print(f"🔧 [DEBUG] Processing order: {self.db_order}")

        print()

    def show_input_loaded(self, line_count: int) -> None:
        """Display input loading status."""
        if self.verbosity == "SILENT":
            return

        if line_count > 0:
            print(
                f"[LOAD] Loading input data...        "
                f"OK {line_count:,} KO identifiers loaded"
            )

            # Debug mode shows technical details
            if self.verbosity == "DEBUG":
                print("🔧 [DEBUG] Input file processing completed")
                print(f"🔧 [DEBUG] Total KO identifiers parsed: {line_count:,}")

        else:
            print("[LOAD] Loading input data...        OK Input loaded")

            if self.verbosity == "DEBUG":
                print("🔧 [DEBUG] Empty or minimal input detected")

        print()

    def show_database_processing(self, result: Dict[str, Any]) -> None:
        """Display database processing steps with real data."""
        if self.verbosity == "SILENT":
            return

        for i, db_key in enumerate(self.db_order, 1):
            if db_key in result:
                pipeline_result = result[db_key]
                if (
                    isinstance(pipeline_result, dict)
                    and "output_path" in pipeline_result
                ):
                    filename = pipeline_result.get("filename", "Unknown")
                    matches = pipeline_result.get("matches", 0)

                    print(f"[PROCESS] Processing databases [{i}/4]:")
                    print(
                        f"   [DB] {self.db_names.get(db_key, db_key)} "
                        f"Database...      OK {matches:,} matches -> "
                        f"{filename}"
                    )

                    # Debug mode shows technical details
                    if self.verbosity == "DEBUG":
                        output_path = pipeline_result.get("output_path", "Unknown")
                        print(f"🔧 [DEBUG] Database: {db_key}")
                        print(f"🔧 [DEBUG] Output path: {output_path}")
                        print(
                            f"🔧 [DEBUG] Result type: {type(pipeline_result).__name__}"
                        )
                        if "processing_time" in pipeline_result:
                            time_val = pipeline_result["processing_time"]
                            print(f"🔧 [DEBUG] Processing time: {time_val:.2f}s")

                    print()

    def show_final_summary(self, result: Dict[str, Any], elapsed_time: float) -> None:
        """Display final summary with real data."""
        if self.verbosity == "SILENT":
            return

        # Calculate total matches
        total_matches = 0
        database_count = 0

        for db_key in self.db_order:
            if db_key in result:
                pipeline_result = result[db_key]
                if (
                    isinstance(pipeline_result, dict)
                    and "output_path" in pipeline_result
                ):
                    matches = pipeline_result.get("matches", 0)
                    total_matches += matches
                    database_count += 1

        print("[SUCCESS] All databases processed successfully!")
        print(
            f"   [RESULTS] Total results: {total_matches:,} matches across "
            f"{database_count} databases"
        )
        print("   [OUTPUT] Location: outputs/results_tables/")
        print(f"   [TIME] Total time: {elapsed_time:.1f} seconds")

        # Debug mode shows technical summary
        if self.verbosity == "DEBUG":
            print("🔧 [DEBUG] ===== TECHNICAL SUMMARY =====")
            db_count = len(self.db_order)
            print(f"🔧 [DEBUG] Processed databases: {database_count}/{db_count}")
            print(f"🔧 [DEBUG] Total processing time: {elapsed_time:.3f} seconds")
            avg_time = elapsed_time / max(database_count, 1)
            print(f"🔧 [DEBUG] Average time per database: {avg_time:.3f}s")
            matches_per_sec = total_matches / max(elapsed_time, 0.001)
            print(f"🔧 [DEBUG] Matches per second: {matches_per_sec:.1f}")
            for db_key in self.db_order:
                if db_key in result:
                    pipeline_result = result[db_key]
                    if isinstance(pipeline_result, dict):
                        matches = pipeline_result.get("matches", 0)
                        print(f"🔧 [DEBUG] {db_key}: {matches:,} matches")

        print()
