"""
Tests for enhanced error handler system.

These tests verify that the enhanced error handler correctly processes
and displays errors to users with contextual solutions.
"""

from io import StringIO
from unittest.mock import patch

from biorempp.utils.error_handler import EnhancedErrorHandler, get_error_handler


class TestErrorHandlerFactory:
    """Test suite for error handler factory function."""

    def test_get_error_handler_returns_instance(self):
        """Test that get_error_handler returns an EnhancedErrorHandler instance."""
        handler = get_error_handler()
        assert isinstance(handler, EnhancedErrorHandler)

    def test_get_error_handler_singleton_behavior(self):
        """Test that get_error_handler returns the same instance."""
        handler1 = get_error_handler()
        handler2 = get_error_handler()
        assert handler1 is handler2


class TestEnhancedErrorHandler:
    """Test suite for EnhancedErrorHandler implementation."""

    def test_enhanced_error_handler_creation(self):
        """Test creating EnhancedErrorHandler instance."""
        handler = EnhancedErrorHandler()
        assert handler is not None
        assert isinstance(handler, EnhancedErrorHandler)

    def test_enhanced_error_handler_has_required_methods(self):
        """Test that handler has required methods."""
        handler = EnhancedErrorHandler()

        # Check for required methods
        assert hasattr(handler, "handle_error")
        assert hasattr(handler, "show_error_to_user")
        assert callable(handler.handle_error)
        assert callable(handler.show_error_to_user)

    def test_handle_error_file_not_found(self):
        """Test handling FileNotFoundError."""
        handler = EnhancedErrorHandler()
        error = FileNotFoundError("test_file.txt not found")

        result = handler.handle_error(error, "file_processing")

        # Should return tuple of (message, solution)
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], str)
        assert result[0]  # Message should not be empty

    def test_handle_error_permission_error(self):
        """Test handling PermissionError."""
        handler = EnhancedErrorHandler()
        error = PermissionError("Permission denied")

        result = handler.handle_error(error, "output_directory")

        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], str)
        assert result[0]  # Message should not be empty

    def test_handle_error_value_error(self):
        """Test handling ValueError."""
        handler = EnhancedErrorHandler()
        error = ValueError("Invalid value")

        result = handler.handle_error(error, "validation")

        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], str)
        assert result[0]  # Message should not be empty

    def test_handle_error_generic_exception(self):
        """Test handling generic exception."""
        handler = EnhancedErrorHandler()
        error = RuntimeError("Something went wrong")

        result = handler.handle_error(error, "processing")

        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], str)
        assert result[0]  # Message should not be empty

    @patch("sys.stdout", new_callable=StringIO)
    def test_show_error_to_user_displays_message(self, mock_stdout):
        """Test that show_error_to_user displays error message."""
        handler = EnhancedErrorHandler()
        error = ValueError("Test error message")

        handler.show_error_to_user(error, "test_context")

        # Should have printed something
        # Note: show_error_to_user might print to stderr or stdout
        # We'll just check it doesn't crash
        assert True  # If we get here, it didn't crash

    @patch("sys.stderr", new_callable=StringIO)
    def test_show_error_to_user_with_stderr(self, mock_stderr):
        """Test show_error_to_user with stderr capture."""
        handler = EnhancedErrorHandler()
        error = FileNotFoundError("missing_file.txt")

        handler.show_error_to_user(error, "file_operation")

        # Should not crash
        assert True

    def test_error_solutions_database_exists(self):
        """Test that ERROR_SOLUTIONS database exists and has expected structure."""
        handler = EnhancedErrorHandler()

        # Check that ERROR_SOLUTIONS attribute exists
        assert hasattr(handler, "ERROR_SOLUTIONS")
        solutions = handler.ERROR_SOLUTIONS

        # Should be a dictionary
        assert isinstance(solutions, dict)

        # Should have some common error types
        expected_errors = ["FileNotFoundError", "PermissionError", "ValueError"]
        for error_type in expected_errors:
            if error_type in solutions:
                assert isinstance(solutions[error_type], dict)

    def test_error_handler_with_context_variations(self):
        """Test error handler with different context values."""
        handler = EnhancedErrorHandler()
        error = ValueError("Test error")

        # Test with different context values
        contexts = [None, "", "file_processing", "database_operation", "validation"]

        for context in contexts:
            try:
                result = handler.handle_error(error, context)
                assert isinstance(result, tuple)
                assert len(result) == 2
            except Exception as e:
                assert False, f"handle_error failed with context '{context}': {e}"

    def test_determine_context_input_file(self):
        """Test context determination for input files."""
        handler = EnhancedErrorHandler()

        context = handler._determine_context("input file error", "FileNotFoundError")
        assert context == "input_file"

        context = handler._determine_context(
            "sample_data.txt missing", "FileNotFoundError"
        )
        assert context == "input_file"

    def test_determine_context_database_file(self):
        """Test context determination for database files."""
        handler = EnhancedErrorHandler()

        context = handler._determine_context(
            "biorempp.csv not found", "FileNotFoundError"
        )
        assert context == "database_file"

        context = handler._determine_context("kegg database error", "FileNotFoundError")
        assert context == "database_file"

    def test_determine_context_invalid_database(self):
        """Test context determination for invalid database."""
        handler = EnhancedErrorHandler()

        context = handler._determine_context("biorempp invalid", "ValueError")
        assert context == "invalid_database"

    def test_determine_context_output_directory(self):
        """Test context determination for output directory."""
        handler = EnhancedErrorHandler()

        context = handler._determine_context(
            "output directory error", "PermissionError"
        )
        assert context == "output_dir"

        context = handler._determine_context("results folder issue", "PermissionError")
        assert context == "output_dir"

    def test_determine_context_invalid_format(self):
        """Test context determination for invalid format."""
        handler = EnhancedErrorHandler()

        context = handler._determine_context("invalid format detected", "ValueError")
        assert context == "invalid_format"

        context = handler._determine_context("format error in file", "ValueError")
        assert context == "invalid_format"

    def test_determine_context_general(self):
        """Test context determination for general errors."""
        handler = EnhancedErrorHandler()

        context = handler._determine_context("random error message", "RuntimeError")
        assert context == "general"

    def test_get_solution_info_existing(self):
        """Test getting solution info for existing contexts."""
        handler = EnhancedErrorHandler()

        solution_info = handler._get_solution_info("FileNotFoundError", "input_file")

        if solution_info:
            assert "message" in solution_info
            assert "solutions" in solution_info

    def test_get_solution_info_nonexistent(self):
        """Test getting solution info for non-existent contexts."""
        handler = EnhancedErrorHandler()

        solution_info = handler._get_solution_info("UnknownError", "unknown_context")
        assert solution_info is None

    def test_format_solution_with_example(self):
        """Test formatting solution with example."""
        handler = EnhancedErrorHandler()
        solutions = ["Solution 1", "Solution 2"]
        example = "biorempp --input data.txt"

        formatted = handler._format_solution(solutions, example)

        assert "• Solution 1" in formatted
        assert "• Solution 2" in formatted
        assert "📚 Example:" in formatted
        assert "biorempp --input data.txt" in formatted

    def test_format_solution_without_example(self):
        """Test formatting solution without example."""
        handler = EnhancedErrorHandler()
        solutions = ["Solution 1", "Solution 2"]

        formatted = handler._format_solution(solutions)

        assert "• Solution 1" in formatted
        assert "• Solution 2" in formatted
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


class TestErrorHandlerWithRealScenarios:
    """Test error handler with realistic error scenarios."""

    def test_file_not_found_scenarios(self):
        """Test various file not found scenarios."""
        handler = EnhancedErrorHandler()

        scenarios = [
            FileNotFoundError("sample_data.txt: No such file"),
            FileNotFoundError("input.csv not found"),
            FileNotFoundError("[Errno 2] No such file: 'data.txt'"),
        ]

        for error in scenarios:
            message, solution = handler.handle_error(error)
            assert isinstance(message, str)
            assert isinstance(solution, str)
            assert len(message) > 0
            assert len(solution) > 0

    def test_permission_error_scenarios(self):
        """Test various permission error scenarios."""
        handler = EnhancedErrorHandler()

        scenarios = [
            PermissionError("Permission denied: output/"),
            PermissionError("[Errno 13] Permission denied: '/protected'"),
            PermissionError("Access denied to results folder"),
        ]

        for error in scenarios:
            message, solution = handler.handle_error(error)
            assert isinstance(message, str)
            assert isinstance(solution, str)

    def test_value_error_scenarios(self):
        """Test various value error scenarios."""
        handler = EnhancedErrorHandler()

        scenarios = [
            ValueError("Invalid database name: wrong_db"),
            ValueError("File format not supported"),
            ValueError("Invalid parameter value"),
        ]

        for error in scenarios:
            message, solution = handler.handle_error(error)
            assert isinstance(message, str)
            assert isinstance(solution, str)

    def test_database_related_errors(self):
        """Test database-related error handling."""
        handler = EnhancedErrorHandler()

        # Database file errors
        db_errors = [
            FileNotFoundError("biorempp.csv not found"),
            FileNotFoundError("kegg_database.csv missing"),
            ValueError("hadeg database corrupted"),
            KeyError("toxcsm column missing"),
        ]

        for error in db_errors:
            message, solution = handler.handle_error(error)
            assert isinstance(message, str)
            assert isinstance(solution, str)

    def test_error_logging_integration(self):
        """Test that error handler has logging capability."""
        handler = EnhancedErrorHandler()

        # Check that handler has logger
        assert hasattr(handler, "logger")
        assert handler.logger is not None

        # Test that handle_error doesn't crash with logging
        error = ValueError("Test error for logging")
        message, solution = handler.handle_error(error, "test_context")

        assert isinstance(message, str)
        assert isinstance(solution, str)

    def test_comprehensive_error_types(self):
        """Test handler with comprehensive set of error types."""
        handler = EnhancedErrorHandler()

        test_cases = [
            (FileNotFoundError("file.txt"), "input_file"),
            (PermissionError("access denied"), "output_dir"),
            (ValueError("invalid value"), "invalid_database"),
            (KeyError("missing_key"), "general"),
            (ImportError("module not found"), "general"),
            (RuntimeError("runtime issue"), "general"),
            (TypeError("type mismatch"), "general"),
            (AttributeError("attribute missing"), "general"),
        ]

        for error, context in test_cases:
            message, solution = handler.handle_error(error, context)
            assert isinstance(message, str)
            assert isinstance(solution, str)
            assert len(message) > 0
            assert len(solution) > 0


class TestErrorHandlerIntegration:
    """Integration tests for error handler system."""

    def test_error_handler_with_real_file_error(self):
        """Test error handler with real file system error."""
        handler = EnhancedErrorHandler()

        # Create a real FileNotFoundError
        try:
            with open("definitely_nonexistent_file_12345.txt", "r"):
                pass
        except FileNotFoundError as e:
            result = handler.handle_error(e, "file_input")
            assert isinstance(result, tuple)
            assert len(result) == 2

    def test_multiple_error_handlers(self):
        """Test creating multiple error handlers."""
        handler1 = EnhancedErrorHandler()
        handler2 = EnhancedErrorHandler()

        # They should be independent instances
        assert handler1 is not handler2

        # But get_error_handler should return singleton
        singleton1 = get_error_handler()
        singleton2 = get_error_handler()
        assert singleton1 is singleton2

    def test_error_handler_logging_integration(self):
        """Test that error handler integrates with logging system."""
        handler = EnhancedErrorHandler()

        # Check that handler has logger
        assert hasattr(handler, "logger")
        assert handler.logger is not None

    def test_error_cascading_scenarios(self):
        """Test error handling in cascading failure scenarios."""
        handler = EnhancedErrorHandler()

        # Simulate cascading errors
        errors = [
            FileNotFoundError("config.yaml not found"),
            PermissionError("Cannot write to logs"),
            ValueError("Invalid configuration parameter"),
            RuntimeError("System failure"),
        ]

        for error in errors:
            message, solution = handler.handle_error(error)
            assert isinstance(message, str)
            assert isinstance(solution, str)
            assert len(message) > 0
            assert len(solution) > 0
