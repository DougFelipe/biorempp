"""Enhanced error handling with user-friendly messages and solutions."""

from typing import Dict, List, Optional, Tuple


class EnhancedErrorHandler:
    """Enhanced error handling with contextual solutions."""

    ERROR_SOLUTIONS = {
        "FileNotFoundError": {
            "input_file": {
                "message": "Input file not found",
                "solutions": [
                    "Check if the file path is correct",
                    "Ensure the file exists in the specified location",
                    "Use absolute path if necessary",
                    "Verify file permissions",
                ],
                "example": (
                    "biorempp --input /full/path/to/your_data.txt "
                    "--database biorempp"
                ),
            },
            "database_file": {
                "message": "Database file not found",
                "solutions": [
                    "Database files may be missing or corrupted",
                    "Try reinstalling BioRemPP package",
                    (
                        "Check if all required database files are present "
                        "in src/biorempp/data/"
                    ),
                    "Verify package installation integrity",
                ],
                "example": "biorempp --list-databases",
            },
        },
        "PermissionError": {
            "output_dir": {
                "message": "Permission denied for output directory",
                "solutions": [
                    "Choose a different output directory",
                    "Check write permissions for the directory",
                    "Try running with administrator privileges",
                    "Create the directory manually first",
                ],
                "example": (
                    "biorempp --input data.txt --database biorempp "
                    "--output-dir ~/my_results"
                ),
            },
            "log_dir": {
                "message": "Permission denied for log directory",
                "solutions": [
                    "Create logs directory manually: mkdir outputs/logs",
                    "Check write permissions for outputs/ directory",
                    "Try running with administrator privileges",
                ],
                "example": "mkdir -p outputs/logs",
            },
        },
        "ValueError": {
            "invalid_database": {
                "message": "Invalid database name",
                "solutions": [
                    (
                        "Use one of the available databases: "
                        "biorempp, hadeg, kegg, toxcsm"
                    ),
                    "Check spelling of database name (case-sensitive)",
                    "Use --list-databases to see all available options",
                ],
                "example": "biorempp --input data.txt --database biorempp",
            },
            "invalid_format": {
                "message": "Invalid file format",
                "solutions": [
                    "Ensure input file contains valid identifiers",
                    "Check if file contains KO identifiers (one per line)",
                    "Verify file encoding is UTF-8",
                    "Remove any special characters or formatting",
                ],
                "example": (
                    "Check sample_data.txt in src/biorempp/data/ "
                    "for format reference"
                ),
            },
            "empty_input": {
                "message": "Input file is empty or contains no valid data",
                "solutions": [
                    "Verify the input file contains data",
                    "Check file format and content",
                    "Ensure identifiers are properly formatted",
                ],
                "example": "Input file should contain one identifier per line",
            },
        },
        "KeyError": {
            "missing_column": {
                "message": "Required column missing from database",
                "solutions": [
                    "Database file may be corrupted",
                    "Try reinstalling BioRemPP package",
                    "Check database file integrity",
                ],
                "example": "biorempp --database-info biorempp",
            }
        },
        "pd.errors.EmptyDataError": {
            "empty_database": {
                "message": "Database file is empty or corrupted",
                "solutions": [
                    "Database file may be corrupted",
                    "Try reinstalling BioRemPP package",
                    "Check if database file exists and has content",
                ],
                "example": "biorempp --list-databases",
            }
        },
        "ImportError": {
            "missing_dependency": {
                "message": "Required dependency not found",
                "solutions": [
                    (
                        "Install missing dependencies with: "
                        "pip install -r requirements.txt"
                    ),
                    "Check if pandas is installed: pip install pandas",
                    "Verify Python environment is properly configured",
                ],
                "example": "pip install biorempp[all]",
            }
        },
    }

    def __init__(self, feedback_manager=None):
        self.feedback_manager = feedback_manager

    def handle_error(
        self, error: Exception, context: str = None
    ) -> Tuple[str, Optional[str]]:
        """
        Convert technical error to user-friendly message with solution.

        Parameters
        ----------
        error : Exception
            The exception that occurred
        context : str, optional
            Additional context about where the error occurred

        Returns
        -------
        Tuple[str, str]
            Tuple of (user_message, solution_text)
        """
        error_type = type(error).__name__
        error_message = str(error)

        # Try to determine context from error message if not provided
        if not context:
            context = self._determine_context(error_message, error_type)

        # Get predefined solution
        solution_info = self._get_solution_info(error_type, context)

        if solution_info:
            user_message = solution_info["message"]
            solutions = solution_info["solutions"]
            example = solution_info.get("example")

            solution_text = self._format_solution(solutions, example)
            return user_message, solution_text

        # Fallback for unknown errors
        fallback_solution = self._get_generic_solution(error_type)
        return (f"An unexpected error occurred: {error_message}", fallback_solution)

    def _determine_context(self, error_message: str, error_type: str) -> str:
        """Determine error context from error message and type."""
        error_lower = error_message.lower()

        # File-related contexts
        if "input" in error_lower or "sample_data" in error_lower:
            return "input_file"
        elif any(db in error_lower for db in ["biorempp", "hadeg", "kegg", "toxcsm"]):
            if "database" in error_lower or ".csv" in error_lower:
                return "database_file"
            else:
                return "invalid_database"
        elif "output" in error_lower or "results" in error_lower:
            return "output_dir"
        elif "log" in error_lower:
            return "log_dir"

        # Data-related contexts
        elif "column" in error_lower or "key" in error_lower:
            return "missing_column"
        elif "empty" in error_lower or "no data" in error_lower:
            if error_type == "ValueError":
                return "empty_input"
            else:
                return "empty_database"

        # Import-related contexts
        elif "import" in error_lower or "module" in error_lower:
            return "missing_dependency"

        # Format-related contexts
        elif "format" in error_lower or "invalid" in error_lower:
            return "invalid_format"

        return "general"

    def _get_solution_info(self, error_type: str, context: str) -> Optional[Dict]:
        """Get solution information for error type and context."""
        if error_type in self.ERROR_SOLUTIONS:
            if context in self.ERROR_SOLUTIONS[error_type]:
                return self.ERROR_SOLUTIONS[error_type][context]

        return None

    def _format_solution(self, solutions: List[str], example: str = None) -> str:
        """Format solution text for display."""
        solution_lines = []
        for i, solution in enumerate(solutions, 1):
            solution_lines.append(f"   {i}. {solution}")

        solution_text = "\n".join(solution_lines)

        if example:
            solution_text += f"\n\n📚 Example:\n   {example}"

        return solution_text

    def _get_generic_solution(self, error_type: str) -> str:
        """Get generic solution for unknown error types."""
        generic_solutions = {
            "FileNotFoundError": "Check file paths and ensure files exist",
            "PermissionError": "Check file and directory permissions",
            "ValueError": "Verify input data format and values",
            "KeyError": "Check data structure and required fields",
            "ImportError": "Install missing dependencies",
            "TypeError": "Check data types and function parameters",
            "AttributeError": "Check object attributes and method calls",
        }

        solution = generic_solutions.get(
            error_type, "Check error details and try again"
        )
        return (
            f"   • {solution}\n"
            f"   • Check the log file for more details\n"
            f"   • Report issue if problem persists"
        )

    def show_error_to_user(self, error: Exception, context: str = None):
        """Show error to user using feedback manager."""
        user_message, solution = self.handle_error(error, context)

        if self.feedback_manager:
            self.feedback_manager.show_error(user_message, solution)
        else:
            print(f"❌ Error: {user_message}")
            if solution:
                print("\n💡 Solutions:")
                print(solution)

    def create_error_context(
        self, operation: str, details: Dict[str, any] = None
    ) -> str:
        """Create error context string for better error handling."""
        context_parts = [operation]

        if details:
            for key, value in details.items():
                context_parts.append(f"{key}={value}")

        return " | ".join(context_parts)


# Global error handler instance
_global_error_handler = None


def get_error_handler(feedback_manager=None) -> EnhancedErrorHandler:
    """Get enhanced error handler instance."""
    global _global_error_handler
    if _global_error_handler is None:
        _global_error_handler = EnhancedErrorHandler(feedback_manager)
    return _global_error_handler
