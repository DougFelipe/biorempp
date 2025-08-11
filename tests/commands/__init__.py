"""
BioRemPP Commands Test Package
=============================

This package provides comprehensive automated testing for the BioRemPP
commands module, ensuring reliability, functionality, and compliance
with the Command Pattern architecture implementation.

The test suite covers all command types and their execution workflows,
including validation logic, error handling, pipeline integration,
and result processing capabilities.

Test Coverage:
    - BaseCommand: Abstract foundation and template method validation
    - InfoCommand: Database information display and help functionality
    - DatabaseMergerCommand: Single database processing operations
    - AllDatabasesMergerCommand: Multi-database comprehensive analysis

Testing Strategy:
    - Unit Testing: Individual component validation and behavior
    - Integration Testing: Command-pipeline coordination verification
    - Error Handling: Exception scenarios and edge cases
    - Mock Testing: Isolated testing with dependency injection
    - Parametrized Testing: Data-driven validation across scenarios

Test Organization:
    Each command type has dedicated test modules with comprehensive
    test classes covering initialization, validation, execution,
    error handling, and integration scenarios.

Quality Standards:
    - PEP 8 compliance with line length < 88 characters
    - English documentation and comprehensive docstrings
    - Mocking for external dependencies and file operations
    - Parametrized tests for multiple scenario validation
    - Clear test organization and descriptive naming

Test Files:
    - test_base_command.py: Abstract base class testing
    - test_info_command.py: Information command testing
    - test_single_merger_command.py: Single database command testing
    - test_all_merger_command.py: Multi-database command testing

Usage:
    Run all command tests:
    >>> pytest tests/commands/ -v

    Run specific command tests:
    >>> pytest tests/commands/test_info_command.py -v

Author: BioRemPP Development Team
"""

__all__ = [
    "test_base_command",
    "test_info_command", 
    "test_single_merger_command",
    "test_all_merger_command",
]
