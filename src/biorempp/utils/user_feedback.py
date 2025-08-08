"""User-friendly feedback system for BioRemPP CLI."""

import os
import sys
import threading
import time
from typing import Any, Dict


class ProgressIndicator:
    """Handles progress indication with different styles."""

    def __init__(self):
        self.active = False
        self.thread = None
        self.current_message = ""
        self.progress_style = "spinner"  # spinner, dots, bar

    def start(self, message: str, style: str = "spinner"):
        """Start progress indicator."""
        self.current_message = message
        self.progress_style = style
        self.active = True

        if style == "spinner":
            self.thread = threading.Thread(target=self._spinner_animation)
        elif style == "dots":
            self.thread = threading.Thread(target=self._dots_animation)

        self.thread.daemon = True
        self.thread.start()

    def stop(self, success_message: str = None):
        """Stop progress indicator."""
        self.active = False
        if self.thread:
            self.thread.join(timeout=0.2)

        # Clear the line and show result
        sys.stdout.write("\r" + " " * (len(self.current_message) + 10) + "\r")
        if success_message:
            print(f"✅ {success_message}")
        sys.stdout.flush()

    def _spinner_animation(self):
        """Spinner animation."""
        spinner_chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        i = 0
        while self.active:
            sys.stdout.write(
                f"\r{spinner_chars[i % len(spinner_chars)]} {self.current_message}"
            )
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1

    def _dots_animation(self):
        """Dots animation."""
        dots = ""
        while self.active:
            for i in range(4):
                if not self.active:
                    break
                dots = "." * i
                sys.stdout.write(f"\r{self.current_message}{dots}   ")
                sys.stdout.flush()
                time.sleep(0.5)


class UserFeedbackManager:
    """Manages user-friendly feedback and progress indication."""

    def __init__(self, verbosity: str = "NORMAL"):
        self.verbosity = verbosity.upper()
        self.current_task = None
        self.task_start_time = None
        self.progress = ProgressIndicator()

    def show_header(self, title: str, subtitle: str = None):
        """Show application header."""
        if self.verbosity == "SILENT":
            return

        print(f"\n🧬 BioRemPP - {title}")
        print("═" * 67)
        if subtitle:
            print(f"{subtitle}\n")

    def show_database_list(self, databases: Dict[str, Dict[str, Any]]):
        """Show available databases in a user-friendly format."""
        if self.verbosity == "SILENT":
            return

        self.show_header("Available Databases")

        for db_key, db_info in databases.items():
            name = db_info.get("name", db_key.upper())
            description = db_info.get("description", "No description")
            size = db_info.get("size", "Unknown size")

            print(f"📊 {name:12} │ {size:15} │ {description}")

        print("\n💡 Usage: biorempp --input your_data.txt --database biorempp")
        print("💡 Or use all: biorempp --input your_data.txt --all-databases\n")

    def start_processing(self, input_file: str, database: str = None):
        """Start processing feedback."""
        if self.verbosity == "SILENT":
            return

        if database:
            title = f"Processing with {database.upper()} Database"
        else:
            title = "Processing with ALL Databases"

        self.show_header(title)

        # Loading input data step
        self.show_loading_step("Loading input data", show_progress=True)

    def show_loading_step(self, step_name: str, show_progress: bool = False):
        """Show loading step with optional progress indicator."""
        if self.verbosity == "SILENT":
            return

        if show_progress:
            self.progress.start(f"📁 {step_name}...")
        else:
            print(f"📁 {step_name}...")

    def complete_loading_step(self, details: str = None, count_info: str = None):
        """Complete loading step with details."""
        if self.verbosity == "SILENT":
            return

        if count_info:
            self.progress.stop(f"Loading input data...        ✅ {count_info}")
        else:
            self.progress.stop("Loading completed")

    def show_database_connection(
        self, db_name: str, record_count: int, show_progress: bool = False
    ):
        """Show database connection step."""
        if self.verbosity == "SILENT":
            return

        if show_progress:
            self.progress.start(f"🔗 Connecting to {db_name}...")
            time.sleep(0.5)  # Simulate connection time
            self.progress.stop(
                f"Connecting to {db_name}...    ✅ {record_count:,} records available"
            )
        else:
            print(f"🔗 {db_name}: {record_count:,} records available")

    def show_processing_progress(self, task_name: str, show_bar: bool = False):
        """Show processing progress."""
        if self.verbosity == "SILENT":
            return

        if show_bar:
            self.progress.start(f"⚙️  {task_name}...")
            time.sleep(1.0)  # Simulate processing time
            self.progress.stop(f"{task_name}...          ████████████████ 100%")
        else:
            print(f"⚙️  {task_name}...")

    def show_saving_results(self, filename: str, show_progress: bool = False):
        """Show saving results step."""
        if self.verbosity == "SILENT":
            return

        if show_progress:
            self.progress.start("💾 Saving results...")
            time.sleep(0.3)  # Simulate saving time
            self.progress.stop(f"Saving results...            ✅ {filename}")
        else:
            print(f"� Saved: {filename}")

    def show_all_databases_processing(self, total_count: int):
        """Show all databases processing header."""
        if self.verbosity == "SILENT":
            return

        self.show_header("Processing with ALL Databases")
        self.show_loading_step("Loading input data", show_progress=True)

    def show_database_processing_step(
        self, current: int, total: int, db_name: str, show_progress: bool = False
    ):
        """Show individual database processing step."""
        if self.verbosity == "SILENT":
            return

        print(f"\n🔄 Processing databases [{current}/{total}]:")

        if show_progress:
            self.progress.start(f"   🧬 {db_name} Database...")
            time.sleep(0.8)  # Simulate processing
        else:
            print(f"   🧬 {db_name} Database...")

    def show_processing_results(self, results: Dict[str, Any]):
        """Show final processing results with detailed stats."""
        if self.verbosity == "SILENT":
            return

        print("\n🎉 Processing completed successfully!")

        if isinstance(results, dict):
            if "output_file" in results:
                filename = os.path.basename(results["output_file"])

                # Calculate file size if file exists
                if os.path.exists(results["output_file"]):
                    file_size = os.path.getsize(results["output_file"])
                    if file_size > 1024 * 1024:  # > 1MB
                        size_str = f"{file_size/(1024*1024):.1f}MB"
                    else:
                        size_str = f"{file_size/1024:.0f}KB"
                    print(f"   📊 Results: {results.get('matches', 0):,} matches found")
                    print(f"   📁 Output: {filename} ({size_str})")
                else:
                    print(f"   📁 Output: {filename}")

            if "processing_time" in results:
                print(f"   ⏱️  Time: {results['processing_time']:.1f} seconds")

        print()

    def show_all_databases_results(self, all_results: Dict[str, Any]):
        """Show results from all databases processing with summary."""
        if self.verbosity == "SILENT":
            return

        print("\n🎉 All databases processed successfully!")

        total_matches = 0
        database_count = 0
        total_time = 0

        for db_name, result in all_results.items():
            if isinstance(result, dict) and "error" not in result:
                database_count += 1
                matches = result.get("matches", 0)
                total_matches += matches
                total_time += result.get("processing_time", 0)

                filename = os.path.basename(result.get("output_path", ""))
                print(f"   🧬 {db_name.upper():8} → {filename}")

        total_msg = (
            f"   📊 Total results: {total_matches:,} matches "
            f"across {database_count} databases"
        )
        print(total_msg)
        print("   📁 Location: outputs/results_tables/")
        if total_time > 0:
            print(f"   ⏱️  Total time: {total_time:.1f} seconds")
        print()

    def show_error(self, message: str, details: str = None):
        """Show error message to user."""
        print(f"\n❌ Error: {message}")
        if details:
            print(details)
        print()

    def show_warning(self, message: str, suggestion: str = None):
        """Show warning message to user."""
        print(f"⚠️  Warning: {message}")
        if suggestion:
            print(f"💡 {suggestion}")

    def show_info(self, message: str, icon: str = "ℹ️"):
        """Show info message to user."""
        if self.verbosity != "SILENT":
            print(f"{icon} {message}")

    def warning(self, message: str):
        """Display warning message."""
        if self.verbosity != "SILENT":
            print(f"⚠️  {message}")

    def error(self, message: str):
        """Display error message."""
        if self.verbosity != "SILENT":
            print(f"❌ {message}")

    def success(self, message: str):
        """Display success message."""
        if self.verbosity != "SILENT":
            print(f"✅ {message}")

    def info(self, message: str):
        """Display info message."""
        if self.verbosity != "SILENT":
            print(f"ℹ️  {message}")

    def debug(self, message: str):
        """Display debug message only in debug mode."""
        if self.verbosity == "DEBUG":
            print(f"🔧 {message}")

    def set_verbosity(self, level: str):
        """Set verbosity level: quiet, normal, verbose, debug."""
        level_map = {
            "quiet": "SILENT",
            "normal": "NORMAL",
            "verbose": "VERBOSE",
            "debug": "DEBUG",
        }
        self.verbosity = level_map.get(level, "NORMAL")


# Global feedback manager instance
_global_feedback = None


def get_user_feedback(verbosity: str = "NORMAL") -> UserFeedbackManager:
    """Get user feedback manager instance."""
    global _global_feedback
    if _global_feedback is None:
        _global_feedback = UserFeedbackManager(verbosity)
    return _global_feedback


def set_verbosity(verbosity: str):
    """Set verbosity level globally."""
    global _global_feedback
    if _global_feedback:
        _global_feedback.verbosity = verbosity.upper()
