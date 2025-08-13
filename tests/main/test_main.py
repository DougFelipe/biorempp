"""
Tests for main entry points of BioRemPP.

These tests verify that the main entry points work correctly
and provide appropriate CLI functionality.
"""

import sys
from unittest.mock import Mock, patch

import pytest


class TestMainModule:
    """Test suite for main module functionality."""

    def test_main_entry_point_import(self):
        """Test that main module can be imported without errors."""
        import biorempp.main

        assert hasattr(biorempp.main, "main")

    @patch("biorempp.main.BioRemPPApplication")
    def test_main_function_creates_application(self, mock_app_class):
        """Test that main function creates and runs BioRemPPApplication."""
        # Arrange
        mock_app = Mock()
        mock_app_class.return_value = mock_app

        # Import and run main
        from biorempp.main import main

        # Act
        main()

        # Assert
        mock_app_class.assert_called_once()
        mock_app.run.assert_called_once()

    @patch("biorempp.main.BioRemPPApplication")
    def test_main_function_no_return_value(self, mock_app_class):
        """Test that main function returns None to avoid CLI pollution."""
        from biorempp.main import main

        result = main()

        assert result is None

    def test_main_module_as_script(self):
        """Test running module as script (__main__.py)."""
        import subprocess
        import sys

        # Test that we can run the module
        result = subprocess.run(
            [sys.executable, "-m", "biorempp", "--help"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        # Should not crash (return code 0 or help exit code)
        assert result.returncode in [0, 2]  # 2 is typical for --help
