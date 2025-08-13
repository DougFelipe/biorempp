"""
Tests for enhanced error handling system.

These tests verify that the enhanced error handling functionality works correctly.
"""

from unittest.mock import Mock, patch

from biorempp.utils.enhanced_errors import EnhancedErrorHandler, get_error_handler


class TestEnhancedErrorHandler:
    """Test suite for EnhancedErrorHandler class."""

    def test_error_handler_creation(self):
        """Test creating EnhancedErrorHandler instance."""
        handler = EnhancedErrorHandler()
        assert handler is not None

    def test_error_handler_with_feedback_manager(self):
        """Test creating handler with feedback manager."""
        mock_feedback = Mock()
        handler = EnhancedErrorHandler(feedback_manager=mock_feedback)
        assert handler.feedback_manager == mock_feedback

    def test_error_solutions_database_structure(self):
        """Test that ERROR_SOLUTIONS database has expected structure."""
        handler = EnhancedErrorHandler()
        solutions = handler.ERROR_SOLUTIONS

        # Should be a dictionary
        assert isinstance(solutions, dict)

        # Should have common error types
        expected_errors = ["FileNotFoundError", "PermissionError", "ValueError"]
        for error_type in expected_errors:
            assert error_type in solutions
            assert isinstance(solutions[error_type], dict)

    def test_handle_error_file_not_found(self):
        """Test handling FileNotFoundError."""
        handler = EnhancedErrorHandler()
        error = FileNotFoundError("sample_data.txt not found")

        message, solution = handler.handle_error(error, "input_file")

        assert isinstance(message, str)
        assert isinstance(solution, str)
        assert "Input file not found" in message
        assert "Check if the file path is correct" in solution

    def test_handle_error_permission_denied(self):
        """Test handling PermissionError."""
        handler = EnhancedErrorHandler()
        error = PermissionError("Permission denied: /output/dir")

        message, solution = handler.handle_error(error, "output_dir")

        assert isinstance(message, str)
        assert isinstance(solution, str)
        assert "Permission denied" in message
        assert "Choose a different output directory" in solution

    def test_handle_error_invalid_database(self):
        """Test handling ValueError for invalid database."""
        handler = EnhancedErrorHandler()
        error = ValueError("Invalid database name: wrong_db")

        message, solution = handler.handle_error(error, "invalid_database")

        assert isinstance(message, str)
        assert isinstance(solution, str)
        assert "Invalid database name" in message
        assert "biorempp, hadeg, kegg, toxcsm" in solution

    def test_handle_error_with_context_detection(self):
        """Test automatic context detection from error message."""
        handler = EnhancedErrorHandler()
        error = FileNotFoundError("input file not found: data.txt")

        # No context provided, should detect from message
        message, solution = handler.handle_error(error)

        assert isinstance(message, str)
        assert isinstance(solution, str)
        # Should detect input_file context
        assert "Input file not found" in message

    def test_handle_error_unknown_error_type(self):
        """Test handling unknown error type."""
        handler = EnhancedErrorHandler()
        error = RuntimeError("Some unknown error occurred")

        message, solution = handler.handle_error(error, "unknown_context")

        assert isinstance(message, str)
        assert isinstance(solution, str)
        assert "An unexpected error occurred" in message
        assert "Some unknown error occurred" in message

    def test_determine_context_input_file(self):
        """Test context determination for input file errors."""
        handler = EnhancedErrorHandler()

        context = handler._determine_context("input file missing", "FileNotFoundError")
        assert context == "input_file"

        context = handler._determine_context(
            "sample_data.txt not found", "FileNotFoundError"
        )
        assert context == "input_file"

    def test_determine_context_database_file(self):
        """Test context determination for database file errors."""
        handler = EnhancedErrorHandler()

        context = handler._determine_context(
            "biorempp.csv not found", "FileNotFoundError"
        )
        assert context == "database_file"

        context = handler._determine_context(
            "kegg database missing", "FileNotFoundError"
        )
        assert context == "database_file"

    def test_determine_context_invalid_database(self):
        """Test context determination for invalid database names."""
        handler = EnhancedErrorHandler()

        context = handler._determine_context("Invalid biorempp value", "ValueError")
        assert context == "invalid_database"

    def test_determine_context_output_directory(self):
        """Test context determination for output directory errors."""
        handler = EnhancedErrorHandler()

        context = handler._determine_context(
            "output directory error", "PermissionError"
        )
        assert context == "output_dir"

        context = handler._determine_context(
            "results folder permission", "PermissionError"
        )
        assert context == "output_dir"

    def test_determine_context_missing_column(self):
        """Test context determination for missing column errors."""
        handler = EnhancedErrorHandler()

        context = handler._determine_context("KeyError: 'column_name'", "KeyError")
        assert context == "missing_column"

    def test_determine_context_empty_input(self):
        """Test context determination for empty input errors."""
        handler = EnhancedErrorHandler()

        context = handler._determine_context("empty file or no data", "ValueError")
        assert context == "empty_input"

    def test_determine_context_missing_dependency(self):
        """Test context determination for import errors."""
        handler = EnhancedErrorHandler()

        context = handler._determine_context("No module named 'pandas'", "ImportError")
        assert context == "missing_dependency"

    def test_get_solution_info_existing(self):
        """Test getting solution info for existing error/context combination."""
        handler = EnhancedErrorHandler()

        solution_info = handler._get_solution_info("FileNotFoundError", "input_file")

        assert solution_info is not None
        assert "message" in solution_info
        assert "solutions" in solution_info
        assert "example" in solution_info

    def test_get_solution_info_nonexistent(self):
        """Test getting solution info for non-existent combination."""
        handler = EnhancedErrorHandler()

        solution_info = handler._get_solution_info("UnknownError", "unknown_context")
        assert solution_info is None

    def test_format_solution_with_example(self):
        """Test formatting solution with example."""
        handler = EnhancedErrorHandler()
        solutions = ["Solution 1", "Solution 2"]
        example = "biorempp --input data.txt"

        formatted = handler._format_solution(solutions, example)

        assert "1. Solution 1" in formatted
        assert "2. Solution 2" in formatted
        assert "📚 Example:" in formatted
        assert "biorempp --input data.txt" in formatted

    def test_format_solution_without_example(self):
        """Test formatting solution without example."""
        handler = EnhancedErrorHandler()
        solutions = ["Solution 1", "Solution 2"]

        formatted = handler._format_solution(solutions)

        assert "1. Solution 1" in formatted
        assert "2. Solution 2" in formatted
        assert "📚 Example:" not in formatted

    def test_get_generic_solution_known_error(self):
        """Test getting generic solution for known error type."""
        handler = EnhancedErrorHandler()

        solution = handler._get_generic_solution("FileNotFoundError")
        assert "Check file paths and ensure files exist" in solution

    def test_get_generic_solution_unknown_error(self):
        """Test getting generic solution for unknown error type."""
        handler = EnhancedErrorHandler()

        solution = handler._get_generic_solution("UnknownError")
        assert "Check error details and try again" in solution

    @patch("builtins.print")
    def test_show_error_to_user_without_feedback_manager(self, mock_print):
        """Test showing error to user without feedback manager."""
        handler = EnhancedErrorHandler()
        error = ValueError("Test error")

        handler.show_error_to_user(error, "invalid_format")

        # Should have called print
        mock_print.assert_called()

    def test_show_error_to_user_with_feedback_manager(self):
        """Test showing error to user with feedback manager."""
        mock_feedback = Mock()
        handler = EnhancedErrorHandler(feedback_manager=mock_feedback)
        error = ValueError("Test error")

        handler.show_error_to_user(error, "invalid_format")

        # Should have called feedback manager
        mock_feedback.show_error.assert_called_once()

    def test_create_error_context_simple(self):
        """Test creating simple error context."""
        handler = EnhancedErrorHandler()

        context = handler.create_error_context("file_processing")
        assert context == "file_processing"

    def test_create_error_context_with_details(self):
        """Test creating error context with details."""
        handler = EnhancedErrorHandler()
        details = {"filename": "data.txt", "line": 42}

        context = handler.create_error_context("validation", details)
        assert "validation" in context
        assert "filename=data.txt" in context
        assert "line=42" in context

    def test_error_handler_comprehensive_error_types(self):
        """Test handler with comprehensive set of error types."""
        handler = EnhancedErrorHandler()

        test_cases = [
            (FileNotFoundError("file.txt"), "input_file"),
            (PermissionError("access denied"), "output_dir"),
            (ValueError("invalid value"), "invalid_database"),
            (KeyError("missing_key"), "missing_column"),
            (ImportError("module not found"), "missing_dependency"),
        ]

        for error, context in test_cases:
            message, solution = handler.handle_error(error, context)
            assert isinstance(message, str)
            assert isinstance(solution, str)
            assert len(message) > 0
            assert len(solution) > 0


class TestErrorHandlerFactory:
    """Test suite for error handler factory function."""

    def test_get_error_handler_returns_instance(self):
        """Test that get_error_handler returns an instance."""
        handler = get_error_handler()
        assert isinstance(handler, EnhancedErrorHandler)

    def test_get_error_handler_singleton_behavior(self):
        """Test that get_error_handler returns the same instance."""
        handler1 = get_error_handler()
        handler2 = get_error_handler()
        assert handler1 is handler2

    def test_get_error_handler_with_feedback_manager(self):
        """Test get_error_handler with feedback manager."""
        mock_feedback = Mock()

        # Reset global handler for this test
        import biorempp.utils.enhanced_errors

        biorempp.utils.enhanced_errors._global_error_handler = None

        handler = get_error_handler(feedback_manager=mock_feedback)
        assert handler.feedback_manager == mock_feedback

    def test_get_error_handler_preserves_feedback_manager(self):
        """Test that subsequent calls preserve feedback manager."""
        mock_feedback = Mock()

        # Reset global handler for this test
        import biorempp.utils.enhanced_errors

        biorempp.utils.enhanced_errors._global_error_handler = None

        handler1 = get_error_handler(feedback_manager=mock_feedback)
        handler2 = get_error_handler()  # No feedback manager in second call

        assert handler1 is handler2
        assert handler2.feedback_manager == mock_feedback


class TestErrorHandlerIntegration:
    """Integration tests for error handler system."""

    def test_realistic_file_not_found_scenario(self):
        """Test realistic file not found scenario."""
        handler = EnhancedErrorHandler()

        # Simulate real file not found error
        try:
            with open("nonexistent_file.txt", "r"):
                pass
        except FileNotFoundError as e:
            message, solution = handler.handle_error(e)
            assert (
                "Input file not found" in message
                or "An unexpected error occurred" in message
            )
            assert isinstance(solution, str)

    def test_database_error_scenario(self):
        """Test database-related error scenario."""
        handler = EnhancedErrorHandler()
        error = FileNotFoundError("biorempp.csv not found")

        message, solution = handler.handle_error(error)

        assert "Database file not found" in message
        assert "Try reinstalling BioRemPP package" in solution

    def test_permission_error_scenario(self):
        """Test permission error scenario."""
        handler = EnhancedErrorHandler()
        error = PermissionError("Permission denied: /restricted/output")

        message, solution = handler.handle_error(error)

        assert "Permission denied" in message
        assert "Choose a different output directory" in solution

    def test_validation_error_scenario(self):
        """Test validation error scenario."""
        handler = EnhancedErrorHandler()
        error = ValueError("Invalid database: wrong_name")

        message, solution = handler.handle_error(error)

        assert "Invalid database name" in message
        assert "biorempp, hadeg, kegg, toxcsm" in solution

    def test_error_handler_with_complex_context(self):
        """Test error handler with complex operational context."""
        handler = EnhancedErrorHandler()

        # Create complex context
        context = handler.create_error_context(
            "data_processing",
            {
                "input_file": "large_dataset.txt",
                "database": "biorempp",
                "operation": "pathway_analysis",
            },
        )

        error = ValueError("Memory allocation failed")
        message, solution = handler.handle_error(error, context)

        assert isinstance(message, str)
        assert isinstance(solution, str)

    def test_error_cascading_and_recovery(self):
        """Test error handling in cascading failure scenarios."""
        handler = EnhancedErrorHandler()

        # Simulate cascading errors
        errors = [
            FileNotFoundError("config.yaml not found"),
            PermissionError("Cannot write to logs"),
            ValueError("Invalid configuration parameter"),
        ]

        for error in errors:
            message, solution = handler.handle_error(error)
            assert isinstance(message, str)
            assert isinstance(solution, str)
            assert len(message) > 0
            assert len(solution) > 0
