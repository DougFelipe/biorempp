"""
Unit tests for the biorempp.cli.output_formatter module.

This module contains comprehensive tests for the BioRemPP CLI output formatting
system, including single and multiple result formatting, error handling,
and integration with the feedback system.

The tests cover:
- Single database output formatting
- Multiple database output formatting
- Result type detection
- File size calculation
- Error message handling
- Feedback manager integration
- Performance metrics
"""

import argparse
import time
from unittest.mock import Mock, patch

import pytest

from biorempp.cli.output_formatter import OutputFormatter


class TestOutputFormatter:
    """Test suite for the OutputFormatter class."""

    def test_formatter_initialization(self):
        """
        Test basic formatter initialization.
        
        Verifies that the formatter is created correctly and
        contains the necessary components.
        """
        # Act
        formatter = OutputFormatter()
        
        # Assert
        assert formatter is not None
        assert formatter.logger is not None
        assert formatter.feedback_manager is not None
        assert hasattr(formatter, 'start_time')

    def test_format_output_single_database_dispatch(self):
        """
        Test routing for single database formatting.
        
        Verifies that single database results are routed
        para o método correto de formatação.
        """
        # Arrange
        formatter = OutputFormatter()
        single_db_result = {
            "output_path": "/path/to/output.txt",
            "matches": 42,
            "filename": "results.txt"
        }
        args = argparse.Namespace(database="biorempp", input="test.txt")
        
        # Act
        with patch.object(
            formatter, '_format_single_database_output'
        ) as mock_single:
            formatter.format_output(single_db_result, args)
        
        # Assert
        mock_single.assert_called_once_with(single_db_result, args)

    def test_format_output_multiple_databases_dispatch(self):
        """
        Test routing for multiple database formatting.
        
        Verifies that multiple database results are routed
        para o método correto de formatação.
        """
        # Arrange
        formatter = OutputFormatter()
        multi_db_result = {
            "biorempp": {"output_path": "/path/1.txt", "matches": 10},
            "hadeg": {"output_path": "/path/2.txt", "matches": 20},
        }
        args = argparse.Namespace(all_databases=True, input="test.txt")
        
        # Act
        with patch.object(
            formatter, '_format_multiple_databases_output'
        ) as mock_multi:
            formatter.format_output(multi_db_result, args)
        
        # Assert
        mock_multi.assert_called_once_with(multi_db_result, args)

    def test_is_single_database_result_true(self):
        """
        Test detection of single database result.
        
        Verifies that results with single database structure
        são identificados corretamente.
        """
        # Arrange
        formatter = OutputFormatter()
        single_db_result = {
            "output_path": "/path/to/output.txt",
            "matches": 42,
            "filename": "results.txt",
            "extra_field": "value"
        }
        
        # Act
        is_single = formatter._is_single_database_result(single_db_result)
        
        # Assert
        assert is_single is True

    def test_is_single_database_result_false(self):
        """
        Test detection of multiple database results.
        
        Verifies that results with multiple database structure
        são identificados corretamente.
        """
        # Arrange
        formatter = OutputFormatter()
        multi_db_result = {
            "biorempp": {"output_path": "/path/1.txt", "matches": 10},
            "hadeg": {"output_path": "/path/2.txt", "matches": 20},
        }
        
        # Act
        is_single = formatter._is_single_database_result(multi_db_result)
        
        # Assert
        assert is_single is False

    def test_format_single_database_output_biorempp(self, capsys):
        """
        Test output formatting for BioRemPP database.
        
        Verifies that formatted output contains the information
        corretas para processamento BioRemPP.
        """
        # Arrange
        formatter = OutputFormatter()
        result = {
            "output_path": "/fake/path/biorempp_results.txt",
            "matches": 150,
            "filename": "biorempp_results.txt"
        }
        args = argparse.Namespace(database="biorempp", input=None)
        
        # Act
        with patch.object(formatter, '_get_file_size', return_value="2.5KB"):
            formatter._format_single_database_output(result, args)
        
        # Assert
        captured = capsys.readouterr()
        assert "BIOREMPP" in captured.out
        assert "150" in captured.out
        assert "biorempp_results.txt" in captured.out
        assert "2.5KB" in captured.out

    def test_format_single_database_output_with_input_file(
        self, capsys, tmp_path
    ):
        """
        Test formatting with existing input file.
        
        Verifies that input file information is
        exibidas corretamente.
        """
        # Arrange
        formatter = OutputFormatter()
        input_file = tmp_path / "test_input.txt"
        input_file.write_text("line1\nline2\nline3\n")
        
        result = {
            "output_path": "/fake/path/results.txt",
            "matches": 50,
            "filename": "results.txt"
        }
        args = argparse.Namespace(
            database="hadeg",
            input=str(input_file)
        )
        
        # Act
        with patch.object(formatter, '_get_file_size', return_value="1KB"):
            formatter._format_single_database_output(result, args)
        
        # Assert
        captured = capsys.readouterr()
        assert "HADEG" in captured.out
        assert "3 identifiers loaded" in captured.out

    def test_format_multiple_databases_output(self):
        """
        Test output formatting for multiple databases.
        
        Verifies that feedback manager is called correctly
        para múltiplos bancos.
        """
        # Arrange
        formatter = OutputFormatter()
        result = {
            "biorempp": {"output_path": "/path/1.txt", "matches": 10},
            "hadeg": {"output_path": "/path/2.txt", "matches": 20},
        }
        args = argparse.Namespace(all_databases=True, input=None)
        
        # Mock do feedback manager
        formatter.feedback_manager = Mock()
        
        # Act
        formatter._format_multiple_databases_output(result, args)
        
        # Assert
        formatter.feedback_manager.show_header.assert_called_once()
        formatter.feedback_manager.show_input_loaded.assert_called_once()
        formatter.feedback_manager.show_database_processing.assert_called_once_with(
            result
        )
        formatter.feedback_manager.show_final_summary.assert_called_once()

    def test_format_multiple_databases_with_input_file(self, tmp_path):
        """
        Test multiple formatting with input file.
        
        Verifies that file line count is
        calculada corretamente.
        """
        # Arrange
        formatter = OutputFormatter()
        input_file = tmp_path / "test_input.txt"
        input_file.write_text("line1\nline2\nline3\nline4\nline5\n")
        
        result = {
            "biorempp": {"output_path": "/path/1.txt", "matches": 10}
        }
        args = argparse.Namespace(
            all_databases=True,
            input=str(input_file)
        )
        
        # Mock do feedback manager
        formatter.feedback_manager = Mock()
        
        # Act
        formatter._format_multiple_databases_output(result, args)
        
        # Assert
        formatter.feedback_manager.show_input_loaded.assert_called_once_with(5)

    def test_get_file_size_bytes(self):
        """
        Test file size calculation in bytes.
        
        Verifies that small files are formatted
        corretamente em bytes.
        """
        # Arrange
        formatter = OutputFormatter()
        
        # Act
        with patch('os.path.getsize', return_value=512):
            size = formatter._get_file_size("/fake/path")
        
        # Assert
        assert size == "512B"

    def test_get_file_size_kilobytes(self):
        """
        Test file size calculation in kilobytes.
        
        Verifies that medium files are formatted
        corretamente em KB.
        """
        # Arrange
        formatter = OutputFormatter()
        
        # Act
        with patch('os.path.getsize', return_value=2048):  # 2KB
            size = formatter._get_file_size("/fake/path")
        
        # Assert
        assert size == "2KB"

    def test_get_file_size_megabytes(self):
        """
        Test file size calculation in megabytes.
        
        Verifies that large files are formatted
        corretamente em MB.
        """
        # Arrange
        formatter = OutputFormatter()
        
        # Act
        with patch('os.path.getsize', return_value=2097152):  # 2MB
            size = formatter._get_file_size("/fake/path")
        
        # Assert
        assert size == "2MB"

    def test_get_file_size_file_not_found(self):
        """
        Test error handling for file not found.
        
        Verifies that non-existent files return
        "Unknown" adequadamente.
        """
        # Arrange
        formatter = OutputFormatter()
        
        # Act
        with patch('os.path.getsize', side_effect=FileNotFoundError):
            size = formatter._get_file_size("/nonexistent/path")
        
        # Assert
        assert size == "Unknown"

    def test_get_file_size_os_error(self):
        """
        Test operating system error handling.
        
        Verifies that OS errors are handled
        adequadamente.
        """
        # Arrange
        formatter = OutputFormatter()
        
        # Act
        with patch('os.path.getsize', side_effect=OSError):
            size = formatter._get_file_size("/error/path")
        
        # Assert
        assert size == "Unknown"

    def test_print_error_message(self, capsys):
        """
        Test error message formatting.
        
        Verifies that errors are formatted and displayed
        corretamente.
        """
        # Arrange
        formatter = OutputFormatter()
        error = ValueError("Teste de erro")
        
        # Act
        formatter.print_error_message(error)
        
        # Assert
        captured = capsys.readouterr()
        assert "[ERROR]" in captured.out
        assert "Teste de erro" in captured.out

    def test_print_interruption_message(self, capsys):
        """
        Test interruption message formatting.
        
        Verifies that user interruptions are
        formatadas corretamente.
        """
        # Arrange
        formatter = OutputFormatter()
        
        # Act
        formatter.print_interruption_message()
        
        # Assert
        captured = capsys.readouterr()
        assert "[BioRemPP]" in captured.out
        assert "interrupted" in captured.out

    def test_format_output_string_fallback(self, capsys):
        """
        Test fallback for string results.
        
        Verifies that string format results are
        tratados adequadamente.
        """
        # Arrange
        formatter = OutputFormatter()
        string_result = "/path/to/output.txt"
        args = argparse.Namespace()
        
        # Act
        formatter.format_output(string_result, args)
        
        # Assert
        captured = capsys.readouterr()
        assert "[BioRemPP]" in captured.out
        assert "/path/to/output.txt" in captured.out

    @pytest.mark.parametrize("db_name,expected_display", [
        ("biorempp", "BioRemPP"),
        ("hadeg", "HAdeg"),
        ("kegg", "KEGG"),
        ("toxcsm", "ToxCSM"),
        ("unknown", "UNKNOWN"),
    ])
    def test_database_display_names(
        self, db_name, expected_display, capsys
    ):
        """
        Test database name mapping for display.
        
        Verifies that database names are formatted
        corretamente para exibição.
        """
        # Arrange
        formatter = OutputFormatter()
        result = {
            "output_path": "/path/to/output.txt",
            "matches": 10,
            "filename": "results.txt"
        }
        args = argparse.Namespace(database=db_name, input=None)
        
        # Act
        with patch.object(formatter, '_get_file_size', return_value="1KB"):
            formatter._format_single_database_output(result, args)
        
        # Assert
        captured = capsys.readouterr()
        assert expected_display.upper() in captured.out

    def test_timing_calculation(self):
        """
        Test processing time calculation.
        
        Verifies that elapsed time is calculated
        corretamente.
        """
        # Arrange
        formatter = OutputFormatter()
        start_time = time.time()
        formatter.start_time = start_time - 2.5  # Simula 2.5 segundos
        
        result = {
            "biorempp": {"output_path": "/path/1.txt", "matches": 10}
        }
        args = argparse.Namespace(all_databases=True, input=None)
        
        # Mock do feedback manager
        formatter.feedback_manager = Mock()
        
        # Act
        formatter._format_multiple_databases_output(result, args)
        
        # Assert
        # Verifies that show_final_summary was called with approximate time
        call_args = formatter.feedback_manager.show_final_summary.call_args
        elapsed_time = call_args[0][1]  # segundo argumento
        assert elapsed_time >= 2.0  # Pelo menos 2 segundos

    def test_empty_result_handling(self):
        """
        Test empty results handling.
        
        Verifies that empty results are handled
        sem erros.
        """
        # Arrange
        formatter = OutputFormatter()
        empty_result = {}
        args = argparse.Namespace()
        
        # Act & Assert - não deve gerar exceção
        formatter.format_output(empty_result, args)

    def test_missing_file_path_in_result(self, capsys):
        """
        Test result handling without file path.
        
        Verifies that results without output_path are
        tratados adequadamente.
        """
        # Arrange
        formatter = OutputFormatter()
        result = {
            "matches": 42,
            "filename": "results.txt"
            # Sem output_path
        }
        args = argparse.Namespace(database="biorempp", input=None)
        
        # Act
        formatter._format_single_database_output(result, args)
        
        # Assert
        captured = capsys.readouterr()
        assert "42" in captured.out  # Verifies that matches appear
        assert "results.txt" in captured.out

    def test_input_file_line_counting_with_empty_lines(self, tmp_path):
        """
        Test line counting ignoring empty lines.
        
        Verifica se apenas linhas com conteúdo são
        contadas.
        """
        # Arrange
        formatter = OutputFormatter()
        input_file = tmp_path / "test_input.txt"
        input_file.write_text("line1\n\nline2\n   \nline3\n")
        
        result = {
            "biorempp": {"output_path": "/path/1.txt", "matches": 10}
        }
        args = argparse.Namespace(
            all_databases=True, 
            input=str(input_file)
        )
        
        # Mock do feedback manager
        formatter.feedback_manager = Mock()
        
        # Act
        formatter._format_multiple_databases_output(result, args)
        
        # Assert
        # Deve contar apenas linhas não vazias: line1, line2, line3 = 3
        formatter.feedback_manager.show_input_loaded.assert_called_once_with(3)

    def test_logger_debug_calls(self):
        """
        Test that debug messages are logged.
        
        Verifica se o logger é chamado adequadamente
        durante a formatação.
        """
        # Arrange
        formatter = OutputFormatter()
        formatter.logger = Mock()
        
        result = {"output_path": "/path", "matches": 1, "filename": "test.txt"}
        args = argparse.Namespace(database="biorempp", input=None)
        
        # Act
        with patch.object(formatter, '_get_file_size', return_value="1KB"):
            formatter.format_output(result, args)
        
        # Assert
        assert formatter.logger.debug.called
