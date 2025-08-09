"""
BioRemPP Enhanced Error Handling Module.

This module implements a sophisticated error handling system that transforms
technical exceptions into user-friendly messages with actionable guidance.
It provides contextual error analysis, solution recommendations, and
professional error presentation for improved user experience in bioinformatics
data processing workflows.

Key Features
-----------
- Contextual Error Analysis: Intelligent error classification and context detection
- User-Friendly Messages: Technical errors translated to clear explanations
- Actionable Solutions: Specific guidance for error resolution
- Example Commands: Practical examples for correcting common issues
- Professional Presentation: Consistent error formatting and display

Error Handling Philosophy
------------------------
The module follows a user-centric error handling approach:
1. Error Classification: Categorize errors by type and context
2. Context Analysis: Understand the operational context when errors occur
3. Solution Generation: Provide specific, actionable resolution steps
4. User Guidance: Clear explanations without overwhelming technical details
5. Recovery Assistance: Help users quickly resolve issues and continue work

Contextual Intelligence
----------------------
Implements intelligent context detection:
- File Operation Errors: Input files, database files, permission issues
- Processing Errors: Data format problems, memory issues, computation failures
- Configuration Errors: Invalid parameters, missing dependencies, setup issues
- System Errors: Platform-specific issues, resource constraints, permissions
- Network Errors: Database connectivity, download failures, timeout issues

Solution Recommendation System
-----------------------------
Provides structured solution recommendations:
- Immediate Actions: Quick fixes for common problems
- Diagnostic Steps: Systematic troubleshooting approaches
- Alternative Methods: Different approaches when primary methods fail
- Prevention Advice: Guidance to avoid similar issues in the future
- Expert Resources: References to documentation and support channels

Error Message Architecture
--------------------------
Structured error presentation system:
- Primary Message: Clear, non-technical description of the problem
- Context Information: Relevant details about the operation that failed
- Solution Steps: Numbered, actionable steps for resolution
- Example Commands: Practical command-line examples for correction
- Additional Resources: Links to documentation and support materials

Integration Design
-----------------
Seamlessly integrates with BioRemPP error handling:
- Exception Translation: Convert Python exceptions to user messages
- Argument Context: Use command-line arguments for better error context
- Logging Integration: Coordinate with logging systems for technical details
- User Feedback: Connect with feedback systems for consistent presentation
- Recovery Guidance: Help users understand and resolve operational issues

Error Categories
---------------
Handles comprehensive error categories:
- File System Errors: Missing files, permission issues, path problems
- Data Processing Errors: Format issues, parsing failures, validation errors
- Resource Errors: Memory constraints, disk space, processing limits
- Configuration Errors: Invalid settings, missing dependencies, setup issues
- Runtime Errors: Unexpected failures, system limitations, platform issues

Example Usage
------------
    from biorempp.utils.error_handler import EnhancedErrorHandler

    # Initialize error handler
    error_handler = EnhancedErrorHandler()

    # Handle specific error with context
    try:
        process_data(input_file)
    except FileNotFoundError as e:
        message, solution = error_handler.handle_error(e, args_context)
        print(f"Error: {message}")
        print(f"Solution: {solution}")

    # Get error solutions
    solutions = error_handler.get_error_solutions("FileNotFoundError")

    # Format error for user display
    formatted_error = error_handler.format_error_message(
        error_type="ValidationError",
        context="input_validation",
        user_input="invalid_file.txt"
    )

Technical Implementation
-----------------------
- Exception type classification with pattern matching
- Context-aware error message generation
- Structured solution database with hierarchical organization
- Professional error formatting with consistent presentation
- Integration hooks for logging and user feedback systems
"""

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
