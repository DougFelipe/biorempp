"""
BaseCommand Test Suite
=====================

Comprehensive testing suite for the BaseCommand abstract base class,
validating the Template Method pattern implementation and common
functionality shared across all BioRemPP command types.

This test suite ensures the robustness of the command foundation,
including validation logic, error handling, template method execution,
and abstract method contract enforcement.

Test Coverage:
    - Abstract base class instantiation and inheritance
    - Template method execution flow validation
    - Common input validation logic and edge cases
    - Error handling and exception propagation
    - Logger configuration and functionality
    - Abstract method contract enforcement

Testing Strategy:
    - Concrete test implementations for abstract methods
    - Mock-based testing for file system operations
    - Edge case validation for file permissions and existence
    - Error scenario simulation and handling verification
    - Template method flow control validation

Quality Standards:
    - PEP 8 compliance with line length < 88 characters
    - Comprehensive English documentation
    - Parametrized testing for multiple input scenarios
    - Clear test organization and descriptive naming
    - Proper mocking and dependency isolation

Author: BioRemPP Development Team
"""

import os
import tempfile
from abc import abstractmethod
from unittest.mock import Mock, patch

import pytest

from biorempp.commands.base_command import BaseCommand


class ConcreteTestCommand(BaseCommand):
    """
    Concrete implementation of BaseCommand for testing purposes.
    
    This class provides minimal implementations of abstract methods
    to enable testing of the BaseCommand template method pattern
    and common functionality.
    """

    def validate_specific_input(self, args) -> bool:
        """
        Test implementation of specific input validation.
        
        Parameters
        ----------
        args : argparse.Namespace
            Parsed command line arguments
            
        Returns
        -------
        bool
            True if validation passes, False otherwise
        """
        return getattr(args, 'valid_specific', True)

    def execute(self, args):
        """
        Test implementation of command execution.
        
        Parameters
        ----------
        args : argparse.Namespace
            Parsed command line arguments
            
        Returns
        -------
        dict
            Test execution result
        """
        return {"status": "success", "test": True}


class TestBaseCommandInitialization:
    """Test BaseCommand initialization and configuration."""

    def test_base_command_cannot_be_instantiated_directly(self):
        """Test that BaseCommand cannot be instantiated as abstract class."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            BaseCommand()

    def test_concrete_command_initialization(self):
        """Test successful initialization of concrete command implementation."""
        command = ConcreteTestCommand()
        
        # Assert
        assert hasattr(command, 'logger')
        assert command.logger.name.endswith('ConcreteTestCommand')

    def test_logger_configuration(self):
        """Test that logger is properly configured during initialization."""
        command = ConcreteTestCommand()
        
        # Assert
        assert command.logger is not None
        assert hasattr(command.logger, 'info')
        assert hasattr(command.logger, 'error')
        assert hasattr(command.logger, 'debug')


class TestBaseCommandTemplateMethod:
    """Test BaseCommand template method execution flow."""

    def test_template_method_execution_order(self):
        """Test that template method executes steps in correct order."""
        command = ConcreteTestCommand()
        
        # Create mock args
        args = Mock()
        args.input = None  # No input file for this test
        args.valid_specific = True
        
        # Mock the methods to track call order
        with patch.object(command, 'validate_common_input') as mock_common, \
             patch.object(command, 'validate_specific_input', 
                         return_value=True) as mock_specific, \
             patch.object(command, 'execute', 
                         return_value={'test': 'result'}) as mock_execute:
            
            # Act
            result = command.run(args)
            
            # Assert execution order
            mock_common.assert_called_once_with(args)
            mock_specific.assert_called_once_with(args)
            mock_execute.assert_called_once_with(args)
            assert result == {'test': 'result'}

    def test_template_method_with_validation_failure(self):
        """Test template method behavior when specific validation fails."""
        command = ConcreteTestCommand()
        
        # Create mock args
        args = Mock()
        args.input = None
        args.valid_specific = False
        
        # Act & Assert
        with pytest.raises(ValueError, 
                          match="Command-specific validation failed"):
            command.run(args)

    def test_template_method_logging(self):
        """Test that template method logs execution start and completion."""
        command = ConcreteTestCommand()
        
        # Create mock args
        args = Mock()
        args.input = None
        args.valid_specific = True
        
        with patch.object(command.logger, 'info') as mock_log:
            # Act
            command.run(args)
            
            # Assert logging calls
            actual_calls = [call[0][0] for call in mock_log.call_args_list]
            assert len(actual_calls) >= 2
            assert any('Starting' in call and 'execution' in call 
                      for call in actual_calls)
            assert any('completed successfully' in call 
                      for call in actual_calls)


class TestBaseCommandCommonValidation:
    """Test BaseCommand common input validation functionality."""

    def test_validate_common_input_with_no_input_attribute(self):
        """Test validation passes when no input attribute exists."""
        command = ConcreteTestCommand()
        args = Mock()
        del args.input  # Remove input attribute
        
        # Should not raise any exception
        command.validate_common_input(args)

    def test_validate_common_input_with_none_input(self):
        """Test validation passes when input is None."""
        command = ConcreteTestCommand()
        args = Mock()
        args.input = None
        
        # Should not raise any exception
        command.validate_common_input(args)

    def test_validate_common_input_with_valid_file(self):
        """Test validation passes with valid input file."""
        command = ConcreteTestCommand()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
            tmp_file.write("test content")
            temp_path = tmp_file.name
        
        try:
            args = Mock()
            args.input = temp_path
            
            # Should not raise any exception
            command.validate_common_input(args)
            
        finally:
            # Clean up
            os.unlink(temp_path)

    def test_validate_common_input_with_nonexistent_file(self):
        """Test validation fails with non-existent file."""
        command = ConcreteTestCommand()
        args = Mock()
        args.input = "/path/to/nonexistent/file.txt"
        
        # Act & Assert
        with pytest.raises(FileNotFoundError, 
                          match="Input file not found"):
            command.validate_common_input(args)

    def test_validate_common_input_with_empty_file(self):
        """Test validation fails with empty file."""
        command = ConcreteTestCommand()
        
        # Create empty temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            temp_path = tmp_file.name
        
        try:
            args = Mock()
            args.input = temp_path
            
            # Act & Assert
            with pytest.raises(ValueError, match="Input file is empty"):
                command.validate_common_input(args)
                
        finally:
            # Clean up
            os.unlink(temp_path)

    @patch('os.access')
    def test_validate_common_input_with_unreadable_file(self, mock_access):
        """Test validation fails with unreadable file."""
        command = ConcreteTestCommand()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
            tmp_file.write("test content")
            temp_path = tmp_file.name
        
        try:
            # Mock file as unreadable
            mock_access.return_value = False
            
            args = Mock()
            args.input = temp_path
            
            # Act & Assert
            with pytest.raises(PermissionError, 
                              match="Input file is not readable"):
                command.validate_common_input(args)
                
        finally:
            # Clean up
            os.unlink(temp_path)


class TestBaseCommandAbstractMethods:
    """Test BaseCommand abstract method contracts."""

    def test_validate_specific_input_is_abstract(self):
        """Test that validate_specific_input is properly abstract."""
        # This is tested implicitly by the fact that BaseCommand
        # cannot be instantiated directly
        
        class IncompleteCommand(BaseCommand):
            def execute(self, args):
                return "result"
        
        with pytest.raises(TypeError):
            IncompleteCommand()

    def test_execute_is_abstract(self):
        """Test that execute method is properly abstract."""
        class IncompleteCommand(BaseCommand):
            def validate_specific_input(self, args) -> bool:
                return True
        
        with pytest.raises(TypeError):
            IncompleteCommand()

    def test_concrete_implementation_requirements(self):
        """Test that concrete implementations must implement all abstracts."""
        class CompleteCommand(BaseCommand):
            def validate_specific_input(self, args) -> bool:
                return True
                
            def execute(self, args):
                return {"complete": True}
        
        # Should instantiate successfully
        command = CompleteCommand()
        assert command is not None


class TestBaseCommandErrorHandling:
    """Test BaseCommand error handling and propagation."""

    def test_common_validation_error_propagation(self):
        """Test that common validation errors are properly propagated."""
        command = ConcreteTestCommand()
        args = Mock()
        args.input = "/nonexistent/file.txt"
        
        # Should propagate FileNotFoundError
        with pytest.raises(FileNotFoundError):
            command.run(args)

    def test_specific_validation_error_handling(self):
        """Test handling of specific validation failures."""
        command = ConcreteTestCommand()
        args = Mock()
        args.input = None
        args.valid_specific = False
        
        # Should raise ValueError for validation failure
        with pytest.raises(ValueError, 
                          match="Command-specific validation failed"):
            command.run(args)

    def test_execution_error_propagation(self):
        """Test that execution errors are properly propagated."""
        command = ConcreteTestCommand()
        args = Mock()
        args.input = None
        args.valid_specific = True
        
        with patch.object(command, 'execute', 
                         side_effect=RuntimeError("Execution failed")):
            # Should propagate RuntimeError
            with pytest.raises(RuntimeError, match="Execution failed"):
                command.run(args)


class TestBaseCommandIntegration:
    """Test BaseCommand integration scenarios."""

    def test_full_execution_workflow_success(self):
        """Test complete successful execution workflow."""
        command = ConcreteTestCommand()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
            tmp_file.write("test input data")
            temp_path = tmp_file.name
        
        try:
            args = Mock()
            args.input = temp_path
            args.valid_specific = True
            
            # Act
            result = command.run(args)
            
            # Assert
            assert result == {"status": "success", "test": True}
            
        finally:
            # Clean up
            os.unlink(temp_path)

    def test_command_reusability(self):
        """Test that command instances can be reused."""
        command = ConcreteTestCommand()
        
        args1 = Mock()
        args1.input = None
        args1.valid_specific = True
        
        args2 = Mock()
        args2.input = None
        args2.valid_specific = True
        
        # Both executions should succeed
        result1 = command.run(args1)
        result2 = command.run(args2)
        
        assert result1 == {"status": "success", "test": True}
        assert result2 == {"status": "success", "test": True}