"""
Module registry system for BioRemPP.

This module provides a registry system for dynamically discovering and managing
data processors, enabling a truly modular architecture focused on data processing.
Visualization is handled externally through returned DataFrames.
"""

import importlib
import importlib.util
import inspect
from pathlib import Path
from typing import Any, Dict, List, Type

from biorempp.analysis.base_processor import BaseDataProcessor
from biorempp.utils.logging_config import get_logger

logger = get_logger("analysis.module_registry")


class ModuleRegistry:
    """
    Registry for managing data processors.

    This class provides functionality to discover, register, and manage
    all available analysis modules in the BioRemPP system. The focus is
    exclusively on data processing - visualization is handled externally.

    Attributes
    ----------
    processors : Dict[str, Type[BaseDataProcessor]]
        Registry of available data processors
    """

    def __init__(self):
        """Initialize the module registry."""
        self.processors: Dict[str, Type[BaseDataProcessor]] = {}
        self.logger = logger
        self.logger.info("ModuleRegistry initialized")

    def register_processor(
        self, processor_class: Type[BaseDataProcessor], name: str = None
    ) -> None:
        """
        Register a data processor class.

        Parameters
        ----------
        processor_class : Type[BaseDataProcessor]
            The processor class to register
        name : str, optional
            Custom name for the processor. If None, uses class name
        """
        if not issubclass(processor_class, BaseDataProcessor):
            raise ValueError(
                f"Processor must inherit from BaseDataProcessor, "
                f"got {processor_class}"
            )

        processor_name = name or processor_class.__name__.lower()
        self.processors[processor_name] = processor_class
        self.logger.info(f"Registered data processor: {processor_name}")

    def get_processor(self, name: str) -> Type[BaseDataProcessor]:
        """
        Get a processor class by name.

        Parameters
        ----------
        name : str
            Name of the processor

        Returns
        -------
        Type[BaseDataProcessor]
            Processor class

        Raises
        ------
        KeyError
            If processor not found
        """
        if name not in self.processors:
            raise KeyError(f"Processor '{name}' not found")
        return self.processors[name]

    def list_processors(self) -> List[str]:
        """
        List all registered processor names.

        Returns
        -------
        List[str]
            List of processor names
        """
        return list(self.processors.keys())

    def create_processor_instance(self, name: str, **kwargs) -> BaseDataProcessor:
        """
        Create an instance of a processor.

        Parameters
        ----------
        name : str
            Name of the processor
        **kwargs
            Additional arguments for processor initialization

        Returns
        -------
        BaseDataProcessor
            Processor instance
        """
        processor_class = self.get_processor(name)
        return processor_class(**kwargs)

    def get_processor_info(self, name: str) -> Dict[str, Any]:
        """
        Get information about a processor.

        Parameters
        ----------
        name : str
            Name of the processor

        Returns
        -------
        Dict[str, Any]
            Processor information
        """
        processor_class = self.get_processor(name)
        instance = processor_class()
        return instance.get_info()

    def auto_discover_modules(self, modules_dir: str = None) -> None:
        """
        Automatically discover and register all processors in the analysis directory.

        Parameters
        ----------
        modules_dir : str, optional
            Directory to search for modules. If None, uses default analysis directory
        """
        if modules_dir is None:
            # Get the directory containing this file (analysis directory)
            current_dir = Path(__file__).parent
            modules_dir = str(current_dir)

        self.logger.info(f"Auto-discovering modules in: {modules_dir}")

        modules_path = Path(modules_dir)

        # Find all Python files in the directory
        for py_file in modules_path.glob("*.py"):
            # Skip __init__.py, base_processor.py, and this registry file
            if py_file.name in [
                "__init__.py",
                "base_processor.py",
                "module_registry.py",
            ]:
                continue

            try:
                # Import the module
                module_name = py_file.stem
                spec = importlib.util.spec_from_file_location(module_name, py_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Find all classes in the module
                for name, obj in inspect.getmembers(module, inspect.isclass):

                    # (obj.__module__ != module.__name__)
                    if obj.__module__ != module.__name__:
                        continue

                    # Register processors
                    if (
                        issubclass(obj, BaseDataProcessor)
                        and obj != BaseDataProcessor
                        and not inspect.isabstract(obj)
                    ):
                        self.register_processor(obj)

            except Exception as e:
                self.logger.warning(f"Failed to load module {py_file}: {e}")

    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all registered modules.

        Returns
        -------
        Dict[str, Any]
            Summary of registered modules
        """
        return {
            "processors": {
                name: self.get_processor_info(name) for name in self.processors.keys()
            },
            "total_processors": len(self.processors),
        }


# Global registry instance
registry = ModuleRegistry()
