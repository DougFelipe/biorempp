"""
Info Command Implementation.

This module implements the InfoCommand for displaying available modules
and system information without requiring input files.
"""

from typing import Any, Dict, List

from biorempp.analysis.module_registry import registry
from biorempp.commands.base_command import BaseCommand


class InfoCommand(BaseCommand):
    """
    Command for displaying system information and available modules.

    This command handles informational requests that don't require
    input file processing, such as listing available analysis modules.

    Features:
    - Auto-discovery and listing of available processors
    - Module descriptions and metadata
    - No input file validation required
    """

    def __init__(self):
        """Initialize info command with module discovery."""
        super().__init__()

        # Auto-discover modules for listing
        self.logger.debug("Initializing module auto-discovery for info command")
        registry.auto_discover_modules()

    def validate_specific_input(self, args) -> bool:
        """
        Validate info command specific inputs.

        Info commands generally don't require specific validation
        as they don't process input files.

        Parameters
        ----------
        args : argparse.Namespace
            Parsed command line arguments

        Returns
        -------
        bool
            Always True for info commands
        """
        self.logger.debug("Info command validation - no specific validation required")
        return True

    def execute(self, args) -> Dict[str, Any]:
        """
        Execute the info command logic.

        Currently supports listing available modules. Can be extended
        for other informational commands in the future.

        Parameters
        ----------
        args : argparse.Namespace
            Parsed command line arguments

        Returns
        -------
        Dict[str, Any]
            Dictionary containing available modules information
        """
        self.logger.info("Executing info command - listing available modules")

        # Get all available processors
        processor_names = registry.list_processors()

        # Build module information
        modules_info = {
            "total_modules": len(processor_names),
            "modules": self._build_modules_info(processor_names),
        }

        self.logger.info(f"Found {len(processor_names)} available modules")
        return modules_info

    def _build_modules_info(
        self, processor_names: List[str]
    ) -> Dict[str, Dict[str, str]]:
        """
        Build detailed information about available modules.

        Parameters
        ----------
        processor_names : List[str]
            List of available processor names

        Returns
        -------
        Dict[str, Dict[str, str]]
            Dictionary mapping processor names to their metadata
        """
        modules_info = {}

        for name in processor_names:
            try:
                processor_class = registry.processors[name]
                instance = processor_class()

                modules_info[name] = {
                    "description": getattr(
                        instance, "description", "No description available"
                    ),
                    "class_name": processor_class.__name__,
                    "module": processor_class.__module__,
                }

            except Exception as e:
                self.logger.warning(f"Failed to get info for processor {name}: {e}")
                modules_info[name] = {
                    "description": "Error loading module information",
                    "class_name": "Unknown",
                    "module": "Unknown",
                    "error": str(e),
                }

        return modules_info
