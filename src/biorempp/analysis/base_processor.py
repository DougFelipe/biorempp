"""
Base abstract class for modular data processing in BioRemPP.

This module defines the abstract base class that all data processors
must inherit from to ensure a consistent, extensible architecture.
The focus is exclusively on data processing - visualization is handled
externally through returned DataFrames.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List

import pandas as pd

from biorempp.utils.logging_config import get_logger


class BaseDataProcessor(ABC):
    """
    Abstract base class for all data processors in BioRemPP.

    This class defines the interface that all analysis modules must implement,
    ensuring consistency and enabling dynamic module discovery and execution.

    The processor is responsible for:
    1. Processing input data and returning results as DataFrames
    2. Saving processed results to files for persistence
    3. Providing data in a format ready for external visualization

    Attributes
    ----------
    name : str
        Unique identifier for this processor
    description : str
        Human-readable description of what this processor does
    required_columns : List[str]
        List of column names required in input DataFrames
    output_columns : List[str]
        List of column names that will be present in output DataFrames
    logger : logging.Logger
        Logger instance for this processor
    """

    def __init__(self, name: str, description: str):
        """
        Initialize the base data processor.

        Parameters
        ----------
        name : str
            Unique identifier for this processor
        description : str
            Human-readable description of what this processor does
        """
        self.name = name
        self.description = description
        self.logger = get_logger(f"analysis.{name}")
        self.logger.info(f"{self.__class__.__name__} initialized: {description}")

    @property
    @abstractmethod
    def required_columns(self) -> List[str]:
        """
        Return the list of required columns for this processor.

        Returns
        -------
        List[str]
            List of column names required in input DataFrames
        """
        pass

    @property
    @abstractmethod
    def output_columns(self) -> List[str]:
        """
        Return the list of columns that will be present in output DataFrames.

        Returns
        -------
        List[str]
            List of column names in output DataFrames
        """
        pass

    @abstractmethod
    def process(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """
        Process the input data and return analysis results.

        Parameters
        ----------
        data : pd.DataFrame
            Input DataFrame to process
        **kwargs
            Additional parameters specific to this processor

        Returns
        -------
        pd.DataFrame
            Processed data with analysis results

        Raises
        ------
        ValueError
            If input data is invalid or missing required columns
        """
        pass

    def validate_input(self, data: pd.DataFrame) -> None:
        """
        Validate that the input DataFrame has the required structure.

        Parameters
        ----------
        data : pd.DataFrame
            DataFrame to validate

        Raises
        ------
        TypeError
            If input is not a pandas DataFrame
        ValueError
            If DataFrame is empty or missing required columns
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError(f"{self.name}: Input must be a pandas DataFrame")

        if data.empty:
            raise ValueError(f"{self.name}: DataFrame cannot be empty")

        missing_columns = [
            col for col in self.required_columns if col not in data.columns
        ]
        if missing_columns:
            raise ValueError(
                f"{self.name}: Missing required columns: {missing_columns}. "
                f"Required: {self.required_columns}, Found: {list(data.columns)}"
            )

        self.logger.debug(f"Input validation passed: {data.shape}")

    def get_info(self) -> Dict[str, Any]:
        """
        Return information about this processor.

        Returns
        -------
        Dict[str, Any]
            Dictionary containing processor metadata
        """
        return {
            "name": self.name,
            "description": self.description,
            "class": self.__class__.__name__,
            "required_columns": self.required_columns,
            "output_columns": self.output_columns,
        }
