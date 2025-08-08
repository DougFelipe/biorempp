"""
Command Factory for BioRemPP Command Pattern Implementation.

This module implements the Factory Pattern for creating appropriate
command instances based on parsed CLI arguments.
"""

import argparse

from biorempp.commands.base_command import BaseCommand
from biorempp.commands.info_command import InfoCommand
from biorempp.commands.modular_command import ModularPipelineCommand
from biorempp.commands.traditional_command import TraditionalPipelineCommand
from biorempp.utils.logging_config import get_logger


class CommandFactory:
    """
    Factory class for creating appropriate command instances.

    Implements the Factory Pattern to centralize command creation logic
    and routing based on CLI arguments. This eliminates conditional
    logic in the main application and makes it easy to add new commands.

    SOLUTION for Risk: Template Method vs Application Responsibility
    - Commands focus on execution and return data
    - Application (not commands) handles formatting via OutputFormatter
    - Clean separation of concerns maintained
    """

    def __init__(self):
        """Initialize command factory with logger."""
        self.logger = get_logger(self.__class__.__name__)

    @classmethod
    def create_command(cls, args: argparse.Namespace) -> BaseCommand:
        """
        Create appropriate command instance based on arguments.

        Routes command creation based on CLI flags and arguments:
        1. Info commands (--list-modules) -> InfoCommand
        2. Modular processing (--enable-modular) -> ModularPipelineCommand
        3. Traditional processing (default) -> TraditionalPipelineCommand

        Parameters
        ----------
        args : argparse.Namespace
            Parsed command line arguments

        Returns
        -------
        BaseCommand
            Appropriate command instance for execution

        Raises
        ------
        ValueError
            If command configuration is invalid or conflicting
        """
        factory = cls()
        factory.logger.debug("Creating command based on arguments")

        # Route 1: Info commands (highest priority)
        if getattr(args, "list_modules", False):
            factory.logger.info("Creating InfoCommand for module listing")
            return InfoCommand()

        # Route 2: Modular processing
        if getattr(args, "enable_modular", False):
            # Validate modular processing requirements
            if not getattr(args, "processors", None):
                raise ValueError(
                    "Modular processing requires --processors to be specified. "
                    "Use --list-modules to see available processors."
                )

            if not getattr(args, "input", None):
                raise ValueError(
                    "Modular processing requires --input file to be specified."
                )

            factory.logger.info("Creating ModularPipelineCommand")
            return ModularPipelineCommand()

        # Route 3: Traditional processing (default)
        # Validate traditional processing requirements
        if not getattr(args, "input", None):
            raise ValueError(
                "Traditional processing requires --input file to be specified."
            )

        factory.logger.info(
            f"Creating TraditionalPipelineCommand for pipeline: {args.pipeline_type}"
        )
        return TraditionalPipelineCommand()

    @classmethod
    def get_command_type(cls, args: argparse.Namespace) -> str:
        """
        Get the command type that would be created for given arguments.

        Useful for testing and debugging without creating actual instances.

        Parameters
        ----------
        args : argparse.Namespace
            Parsed command line arguments

        Returns
        -------
        str
            Command type name ('info', 'modular', 'traditional')
        """
        if getattr(args, "list_modules", False):
            return "info"
        elif getattr(args, "enable_modular", False):
            return "modular"
        else:
            return "traditional"
