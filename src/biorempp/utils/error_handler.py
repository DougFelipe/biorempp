"""Enhanced error handling with user-friendly messages and solutions."""

import logging
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
                    "Check if all required database files are present",
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
            }
        },
        "ValueError": {
            "invalid_database": {
                "message": "Invalid database name",
                "solutions": [
                    "Use one of the available databases: biorempp, hadeg, kegg, toxcsm",
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
                "example": "Check sample_data.txt for format reference",
            },
        },
    }

    def __init__(self):
        self.logger = logging.getLogger("biorempp.error_handler")

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

        # Log technical error details
        self.logger.error(
            f"Error occurred: {error_type}: {error_message}", exc_info=True
        )

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
        return f"An unexpected error occurred: {error_message}", fallback_solution

    def _determine_context(self, error_message: str, error_type: str) -> str:
        """Determine error context from error message and type."""
        error_lower = error_message.lower()

        if "input" in error_lower or "sample_data" in error_lower:
            return "input_file"
        elif any(db in error_lower for db in ["biorempp", "hadeg", "kegg", "toxcsm"]):
            if "database" in error_lower or ".csv" in error_lower:
                return "database_file"
            else:
                return "invalid_database"
        elif "output" in error_lower or "results" in error_lower:
            return "output_dir"
        elif "format" in error_lower or "invalid" in error_lower:
            return "invalid_format"

        return "general"

    def _get_solution_info(self, error_type: str, context: str) -> Optional[Dict]:
        """Get solution information for error type and context."""
        if error_type in self.ERROR_SOLUTIONS:
            # Use the general solution for the error type
            if "general" in self.ERROR_SOLUTIONS[error_type]:
                return self.ERROR_SOLUTIONS[error_type]["general"]
        return None

    def _format_solution(self, solutions: List[str], example: str = None) -> str:
        """Format solution text for display."""
        solution_lines = []
        for i, solution in enumerate(solutions, 1):
            solution_lines.append(f"   • {solution}")

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
        """Show error to user in a friendly format."""
        user_message, solution = self.handle_error(error, context)

        print(f"\n❌ Error: {user_message}")
        if solution:
            print("\n💡 Solutions:")
            print(solution)
        print()


# Global error handler instance
_global_error_handler = None


def get_error_handler() -> EnhancedErrorHandler:
    """Get enhanced error handler instance."""
    global _global_error_handler
    if _global_error_handler is None:
        _global_error_handler = EnhancedErrorHandler()
    return _global_error_handler
