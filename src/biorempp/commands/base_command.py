"""
    base_command.py
---------------
--------------
Abstract Base Command Implementation for BioRemPP Command Pattern

This module implements the Template Method design pattern to provide a
standardized execution framework for all BioRemPP commands. It ensures
consistent validation, error handling, and execution flow while allowing
specific implementations for different command types.

The BaseCommand class serves as the foundation for all command implementations,
enforcing a structured approach to command execution that promotes reliability,
maintainability, and extensibility across the BioRemPP command ecosystem.

Template Method Pattern:
    The run() method defines the algorithmic skeleton that all commands follow:
    1. Common input validation (files, permissions, paths)
    2. Command-specific validation (database types, parameters)
    3. Command execution with comprehensive error handling
    4. Result processing and user feedback

Design Benefits:
    - Consistency: All commands follow the same execution pattern
    - Reliability: Centralized validation and error handling
    - Extensibility: Easy addition of new command types
    - Maintainability: Common functionality in one location
    - Testability: Clear separation between validation and execution

Command Hierarchy:
    BaseCommand (Abstract)
    ├── DatabaseMergerCommand (Single database operations)
    ├── AllDatabasesMergerCommand (Multi-database operations)
    └── InfoCommand (Information and help display)
"""

import os
from abc import ABC, abstractmethod
from typing import Any

from biorempp.utils.silent_logging import get_logger


class BaseCommand(ABC):
    """
    Abstract base class for all BioRemPP commands.

    Implements the Template Method pattern to ensure consistent execution flow:
    1. Common input validation (file existence, permissions)
    2. Command-specific validation (pipeline types, processors, etc.)
    3. Command execution

    This design ensures robustness and consistency across all command types
    while maintaining flexibility for specific implementations.
    """

    def __init__(self):
        """Initialize the command with logger."""
        self.logger = get_logger(self.__class__.__name__)

    def run(self, args) -> Any:
        """
        Template method implementing the standard command execution flow.

        This method enforces the execution sequence:
        1. Validate common inputs (file paths, permissions)
        2. Validate command-specific inputs (pipeline types, processors)
        3. Execute the command logic

        Parameters
        ----------
        args : argparse.Namespace
            Parsed command line arguments

        Returns
        -------
        Any
            Command execution results

        Raises
        ------
        ValueError
            If validation fails at any step
        FileNotFoundError
            If required input files don't exist
        PermissionError
            If file permissions are insufficient
        """
        self.logger.info(f"Starting {self.__class__.__name__} execution")

        # Step 1: Common validation (file existence, permissions)
        self.validate_common_input(args)

        # Step 2: Command-specific validation
        if not self.validate_specific_input(args):
            raise ValueError(
                f"Command-specific validation failed for {self.__class__.__name__}"
            )

        # Step 3: Execute command logic
        result = self.execute(args)

        self.logger.info(f"{self.__class__.__name__} execution completed successfully")
        return result

    def validate_common_input(self, args) -> None:
        """
        Validate common input requirements across all commands.

        Checks file existence, permissions, and basic path validation.
        This centralizes common validation logic to avoid duplication.

        Parameters
        ----------
        args : argparse.Namespace
            Parsed command line arguments

        Raises
        ------
        FileNotFoundError
            If required input file doesn't exist
        PermissionError
            If file permissions are insufficient
        ValueError
            If file path is invalid
        """
        # Skip file validation for info commands that don't require input files
        if hasattr(args, "input") and args.input:
            input_path = args.input

            # Validate file exists
            if not os.path.exists(input_path):
                self.logger.error(f"Input file not found: {input_path}")
                raise FileNotFoundError(f"Input file not found: {input_path}")

            # Validate file is readable
            if not os.access(input_path, os.R_OK):
                self.logger.error(f"Input file is not readable: {input_path}")
                raise PermissionError(f"Input file is not readable: {input_path}")

            # Validate file is not empty
            if os.path.getsize(input_path) == 0:
                self.logger.error(f"Input file is empty: {input_path}")
                raise ValueError(f"Input file is empty: {input_path}")

            self.logger.debug(f"Input file validation passed: {input_path}")

    @abstractmethod
    def validate_specific_input(self, args) -> bool:
        """
        Validate command-specific input requirements.

        Each command type implements its own specific validation logic:
        - InfoCommand: no specific validation needed

        Parameters
        ----------
        args : argparse.Namespace
            Parsed command line arguments

        Returns
        -------
        bool
            True if validation passes, False otherwise
        """
        pass

    @abstractmethod
    def execute(self, args) -> Any:
        """
        Execute the command-specific logic.

        This method contains the core business logic for each command type.
        It should focus purely on execution without validation or formatting concerns.

        Parameters
        ----------
        args : argparse.Namespace
            Parsed command line arguments

        Returns
        -------
        Any
            Command execution results (typically Dict or DataFrame)
        """
        pass
