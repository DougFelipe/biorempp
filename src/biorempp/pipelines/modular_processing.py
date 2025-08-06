"""
Modular data processing pipeline for BioRemPP.

This module provides a flexible pipeline system that can dynamically
execute any combination of registered data processors, focusing exclusively
on data processing. Results are returned as DataFrames for external use.
"""

from typing import Any, Dict, List

import pandas as pd

from biorempp.analysis.module_registry import registry
from biorempp.utils.logging_config import get_logger

logger = get_logger("pipelines.modular_processing")


class ModularProcessingPipeline:
    """
    Pipeline for executing modular data processing.

    This class provides a single interface that can work with any combination
    of registered processors. Each processor handles its own file saving logic,
    and results are returned as DataFrames for external consumption
    (e.g., visualization in notebooks).

    Attributes
    ----------
    registry : ModuleRegistry
        The module registry containing available processors
    logger : logging.Logger
        Logger instance for this pipeline
    """

    def __init__(self):
        """Initialize the modular processing pipeline."""
        self.registry = registry
        self.logger = logger
        self.logger.info("ModularProcessingPipeline initialized")

    def run_processing_pipeline(
        self,
        processor_names: List[str],
        data_type: str = "biorempp",
        input_data: pd.DataFrame = None,
    ) -> Dict[str, pd.DataFrame]:
        """
        Run multiple data processors on input data.

        This method processes data using the specified processors and returns
        DataFrames for external use. Each processor handles its own file saving
        logic as defined in their individual classes.

        Parameters
        ----------
        processor_names : List[str]
            List of processor names to execute
        data_type : str, optional
            Type of data being processed. Default is "biorempp"
        input_data : pd.DataFrame, optional
            Input data to process. If None, raises ValueError

        Returns
        -------
        Dict[str, pd.DataFrame]
            Dictionary mapping processor names to their result DataFrames

        Raises
        ------
        ValueError
            If no processors specified or input_data is None
        """
        if not processor_names:
            raise ValueError("At least one processor must be specified")

        self.logger.info(f"Running processing pipeline with: {processor_names}")

        # Load input data if not provided
        if input_data is None:
            raise ValueError(
                "input_data is required. The traditional pipeline functionality "
                "for auto-loading timestamped files has been deprecated. "
                "Please provide input_data explicitly."
            )

        results = {}

        # Execute each processor
        for processor_name in processor_names:
            try:
                self.logger.info(f"Running processor: {processor_name}")

                # Create processor instance
                processor = self.registry.create_processor_instance(processor_name)

                # Process the data (each processor handles its own file saving)
                processed_data = processor.process(input_data)

                # Store results in memory
                results[processor_name] = processed_data

                self.logger.info(
                    f"Processor {processor_name} completed. "
                    f"Results available in memory."
                )

            except Exception as e:
                self.logger.error(f"Error running processor {processor_name}: {e}")
                # Continue with other processors even if one fails
                continue

        self.logger.info("Processing pipeline completed")
        return results

    def run_single_processor(
        self,
        processor_name: str,
        input_data: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Run a single processor on input data.

        Each processor handles its own file saving logic as defined in their
        individual classes.

        Parameters
        ----------
        processor_name : str
            Name of the processor to execute
        input_data : pd.DataFrame
            Input data to process

        Returns
        -------
        pd.DataFrame
            Processed data
        """
        result = self.run_processing_pipeline(
            processor_names=[processor_name],
            input_data=input_data,
        )
        return result[processor_name]

    def get_available_processors(self) -> List[str]:
        """
        Get list of all available processors.

        Returns
        -------
        List[str]
            List of available processor names
        """
        return self.registry.list_processors()

    def get_processor_info(self, processor_name: str) -> Dict[str, Any]:
        """
        Get information about a specific processor.

        Parameters
        ----------
        processor_name : str
            Name of the processor

        Returns
        -------
        Dict[str, Any]
            Processor information including description, required columns, etc.
        """
        return self.registry.get_processor_info(processor_name)

    def validate_processors(self, processor_names: List[str]) -> Dict[str, bool]:
        """
        Validate that all specified processors are available.

        Parameters
        ----------
        processor_names : List[str]
            List of processor names to validate

        Returns
        -------
        Dict[str, bool]
            Dictionary mapping processor names to availability status
        """
        available = self.get_available_processors()
        return {name: name in available for name in processor_names}

    def get_pipeline_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the pipeline capabilities.

        Returns
        -------
        Dict[str, Any]
            Summary of available processors and pipeline information
        """
        summary = self.registry.get_summary()
        summary["pipeline_info"] = {
            "class": self.__class__.__name__,
            "description": "Modular data processing pipeline for BioRemPP",
            "focus": "Data processing with individual processor file management",
            "output_formats": [
                "DataFrame (in-memory)",
                "Processor-specific output files",
            ],
        }
        return summary
