"""
Enhanced User Feedback Manager for BioRemPP CLI Interface.

This module provides elegant feedback components for the beautiful CLI interface,
implementing the design specification from LOGGING_SYSTEM_DESIGN.md.
"""

from typing import Any, Dict


class EnhancedFeedbackManager:
    """
    Enhanced feedback manager for beautiful CLI interface.

    Provides structured, elegant output components following the design
    specification from LOGGING_SYSTEM_DESIGN.md.
    """

    def __init__(self):
        """Initialize feedback manager."""
        self.db_order = ["biorempp", "hadeg", "kegg", "toxcsm"]
        self.db_names = {
            "biorempp": "BioRemPP",
            "hadeg": "HAdeg",
            "kegg": "KEGG",
            "toxcsm": "ToxCSM",
        }

    def show_header(self) -> None:
        """Display the beautiful header."""
        print("\n🧬 BioRemPP - Processing with ALL Databases")
        print("═" * 67)
        print()

    def show_input_loaded(self, line_count: int) -> None:
        """Display input loading status."""
        if line_count > 0:
            print(
                f"📁 Loading input data...        "
                f"✅ {line_count:,} KO identifiers loaded"
            )
        else:
            print("📁 Loading input data...        ✅ Input loaded")
        print()

    def show_database_processing(self, result: Dict[str, Any]) -> None:
        """Display database processing steps with real data."""
        for i, db_key in enumerate(self.db_order, 1):
            if db_key in result:
                pipeline_result = result[db_key]
                if (
                    isinstance(pipeline_result, dict)
                    and "output_path" in pipeline_result
                ):
                    filename = pipeline_result.get("filename", "Unknown")
                    matches = pipeline_result.get("matches", 0)

                    print(f"🔄 Processing databases [{i}/4]:")
                    print(
                        f"   🧬 {self.db_names.get(db_key, db_key)} "
                        f"Database...      ✅ {matches:,} matches → "
                        f"{filename}"
                    )
                    print()

    def show_final_summary(self, result: Dict[str, Any], elapsed_time: float) -> None:
        """Display final summary with real data."""
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

        print("🎉 All databases processed successfully!")
        print(
            f"   📊 Total results: {total_matches:,} matches across "
            f"{database_count} databases"
        )
        print("   📁 Location: outputs/results_tables/")
        print(f"   ⏱️  Total time: {elapsed_time:.1f} seconds")
        print()
