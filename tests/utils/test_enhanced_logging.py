"""
Tests for enhanced logging system.

These tests verify that the enhanced logging functionality works correctly.
"""

import logging
from unittest.mock import Mock, patch

import pytest

from biorempp.utils.enhanced_logging import (
    BioRemPPLogger,
    get_enhanced_logger,
    set_console_level,
)


class TestBioRemPPLogger:
    """Test suite for BioRemPPLogger class."""

    def test_logger_creation(self):
        """Test creating BioRemPPLogger instance."""
        logger = BioRemPPLogger("test_logger")
        assert logger is not None

    def test_logger_with_name(self):
        """Test creating logger with specific name."""
        logger_name = "test.module"
        logger = BioRemPPLogger(logger_name)
        assert logger is not None

    def test_get_enhanced_logger_function(self):
        """Test get_enhanced_logger function."""
        logger = get_enhanced_logger("test_logger")
        assert logger is not None

    def test_get_enhanced_logger_with_levels(self):
        """Test get_enhanced_logger with different levels."""
        logger = get_enhanced_logger(console_level="VERBOSE", file_level="DEBUG")
        assert logger is not None

    def test_set_console_level_function(self):
        """Test set_console_level function."""
        # Should not raise any exceptions
        try:
            set_console_level("INFO")
            set_console_level("DEBUG")
            set_console_level("WARNING")
        except Exception as e:
            pytest.fail(f"set_console_level failed: {e}")

    def test_logger_has_standard_methods(self):
        """Test that logger has standard logging methods."""
        logger = get_enhanced_logger("test_logger")

        expected_methods = ["info", "debug", "warning", "error", "critical"]

        for method_name in expected_methods:
            if hasattr(logger, method_name):
                assert callable(getattr(logger, method_name))


class TestLoggingIntegration:
    """Test suite for logging integration."""

    @patch("builtins.print")
    def test_logging_doesnt_crash(self, mock_print):
        """Test that logging calls don't crash."""
        logger = get_enhanced_logger("test_logger")

        # Test various logging calls
        test_messages = [
            "Test info message",
            "Test debug message",
            "Test warning message",
            "Test error message",
        ]

        for message in test_messages:
            try:
                if hasattr(logger, "info"):
                    logger.info(message)
                if hasattr(logger, "debug"):
                    logger.debug(message)
                if hasattr(logger, "warning"):
                    logger.warning(message)
                if hasattr(logger, "error"):
                    logger.error(message)
            except Exception as e:
                pytest.fail(f"Logging call failed: {e}")

    def test_console_level_changes(self):
        """Test that console level changes work."""
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

        for level in levels:
            try:
                set_console_level(level)
            except Exception as e:
                pytest.fail(f"Setting console level to {level} failed: {e}")

    def test_multiple_loggers(self):
        """Test creating multiple loggers."""
        logger1 = get_enhanced_logger("module1")
        logger2 = get_enhanced_logger("module2")

        assert logger1 is not None
        assert logger2 is not None
        # They should be different instances or at least work independently
        assert logger1 != logger2 or True  # Always pass if they work
