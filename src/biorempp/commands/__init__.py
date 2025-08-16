"""
    BioRemPP Commands Package

This package implements the Command Pattern architecture for BioRemPP,
providing a structured and extensible approach to handling different types
of operations. The command pattern encapsulates requests as objects,
allowing for parameterization, queuing, and decoupling of request handling.

Command Architecture:
    The package follows a hierarchical structure with BaseCommand as the
    abstract foundation implementing the Template Method pattern for
    consistent execution flow across all command types.

Available Commands:
    - BaseCommand: Abstract foundation with common validation and execution flow
    - DatabaseMergerCommand: Single database processing operations
    - AllDatabasesMergerCommand: Multi-database processing operations
    - InfoCommand: Information display and help functionality

Design Patterns:
    - Command Pattern: Encapsulates operations as executable objects
    - Template Method: Standardizes execution flow while allowing customization
    - Factory Method: Dynamic command creation based on CLI arguments

Execution Flow:
    1. Common input validation (file existence, permissions)
    2. Command-specific validation (database types, parameters)
    3. Command execution with error handling
    4. Result formatting and user feedback

Benefits:
    - Extensibility: Easy addition of new command types
    - Consistency: Standardized validation and error handling
    - Maintainability: Clear separation of concerns
    - Testability: Isolated command logic for unit testing

Usage Examples:
    >>> from biorempp.commands import DatabaseMergerCommand
    >>> command = DatabaseMergerCommand()
    >>> result = command.run(parsed_args)
"""

from .all_merger_command import AllDatabasesMergerCommand
from .base_command import BaseCommand
from .info_command import InfoCommand
from .single_merger_command import DatabaseMergerCommand

__all__ = [
    "BaseCommand",
    "DatabaseMergerCommand",
    "AllDatabasesMergerCommand",
    "InfoCommand",
]
