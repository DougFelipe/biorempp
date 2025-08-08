"""
Modular Pipeline Command Implementation.

This module implements the ModularPipelineCommand for executing
modular BioRemPP processing with auto-discovery and DataFrame-based results.

SOLUTION for Risk: Pandas Import Conditionally
- pandas imported only in this module where it's actually used
- Registry auto-discovery moved to __init__ for proper lifecycle management
"""

from typing import Any, Dict

# Conditional pandas import - only used in modular pipeline
try:
    import pandas as pd
except ImportError:
    pd = None

from biorempp.analysis.module_registry import registry
from biorempp.commands.base_command import BaseCommand
from biorempp.pipelines.modular_processing import ModularProcessingPipeline


class ModularPipelineCommand(BaseCommand):
    """
    Command for executing modular BioRemPP processing pipelines.

    This command supports auto-discovery of analysis modules and processes
    data through a modular pipeline returning DataFrame results for external use.

    Features:
    - Auto-discovery of available analysis modules
    - CSV data loading with configurable separator
    - Modular processing with flexible processor selection
    - Detailed execution summary and metadata

    ARCHITECTURAL SOLUTIONS IMPLEMENTED:
    1. Pandas imported conditionally only where needed
    2. Registry auto-discovery in constructor for proper lifecycle
    3. Clean separation between data loading and processing
    4. Comprehensive error handling with context
    """

    def __init__(self):
        """
        Initialize modular pipeline command.

        SOLUTION for Risk: Registry Auto-Discovery Timing
        - Auto-discovery moved to initialization for better lifecycle management
        - Ensures modules are available before validation/execution
        """
        super().__init__()

        # Verify pandas is available for modular processing
        if pd is None:
            raise ImportError(
                "pandas is required for modular pipeline processing. "
                "Please install pandas: pip install pandas"
            )

        # Auto-discover modules at initialization for proper lifecycle
        self.logger.debug("Initializing module auto-discovery")
        registry.auto_discover_modules()
        available_processors = registry.list_processors()
        self.logger.info(f"Discovered {len(available_processors)} modules")

    def validate_specific_input(self, args) -> bool:
        """
        Validate modular pipeline specific inputs.

        Checks that processors are specified and that required arguments
        are present for modular pipeline execution.

        Parameters
        ----------
        args : argparse.Namespace
            Parsed command line arguments

        Returns
        -------
        bool
            True if validation passes, False otherwise
        """
        # Validate processors list is provided
        if not hasattr(args, "processors") or not args.processors:
            self.logger.error(
                "Processors list is required for modular pipeline processing. "
                "Use --processors to specify modules to run."
            )
            return False

        # Validate input file is provided
        if not hasattr(args, "input") or not args.input:
            self.logger.error("Input file is required for modular pipeline processing")
            return False

        # Validate that specified processors are available
        available_processors = registry.list_processors()
        for processor_name in args.processors:
            if processor_name not in available_processors:
                self.logger.error(
                    f"Processor '{processor_name}' not found in registry. "
                    f"Available: {available_processors}"
                )
                return False

        self.logger.debug(
            f"Modular pipeline validation passed for processors: {args.processors}"
        )
        return True

    def execute(self, args) -> Dict[str, Any]:
        """
        Execute the modular pipeline processing.

        Loads input data, runs specified processors through the modular pipeline,
        and returns comprehensive results with metadata.

        Parameters
        ----------
        args : argparse.Namespace
            Parsed command line arguments

        Returns
        -------
        Dict[str, Any]
            Dictionary containing:
            - processors_run: Number of processors executed
            - successful_processors: Number of successful processors
            - processing_results: DataFrame results from each processor
            - processor_details: Metadata about each processor execution
        """
        self.logger.info("Executing modular processing pipeline")

        # Load input data
        input_data = self._load_input_data(args.input)

        # Initialize and run modular pipeline
        pipeline = ModularProcessingPipeline()
        processing_results = pipeline.run_processing_pipeline(
            processor_names=args.processors, data_type="biorempp", input_data=input_data
        )

        # Build comprehensive results summary
        results_summary = self._build_results_summary(
            args.processors, processing_results
        )

        self.logger.info(
            f"Modular pipeline completed: {results_summary['successful_processors']}/"
            f"{results_summary['processors_run']} processors successful"
        )

        return results_summary

    def _load_input_data(self, input_path: str) -> pd.DataFrame:
        """
        Load input data from CSV file.

        SOLUTION for Risk: Error Handling Distribution
        - Centralized data loading with comprehensive error context
        - Proper exception chaining for debugging

        Parameters
        ----------
        input_path : str
            Path to input CSV file

        Returns
        -------
        pd.DataFrame
            Loaded input data

        Raises
        ------
        ValueError
            If data loading fails with context about the error
        """
        try:
            self.logger.info(f"Loading input data from: {input_path}")
            input_data = pd.read_csv(input_path, sep=";")
            self.logger.info(f"Loaded data shape: {input_data.shape}")

            # Validate data is not empty
            if input_data.empty:
                raise ValueError(
                    f"Input file is empty or contains no valid data: {input_path}"
                )

            return input_data

        except pd.errors.EmptyDataError as e:
            self.logger.error(f"Input file is empty: {input_path}")
            raise ValueError(f"Input file is empty: {input_path}") from e
        except pd.errors.ParserError as e:
            self.logger.error(f"Failed to parse CSV file: {input_path} - {e}")
            raise ValueError(f"Failed to parse CSV file: {input_path} - {e}") from e
        except Exception as e:
            self.logger.error(f"Failed to load input data from {input_path}: {e}")
            raise ValueError(f"Failed to load input data from {input_path}: {e}") from e

    def _build_results_summary(
        self, requested_processors: list, processing_results: Dict[str, pd.DataFrame]
    ) -> Dict[str, Any]:
        """
        Build comprehensive results summary with processor details.

        Parameters
        ----------
        requested_processors : list
            List of processors that were requested to run
        processing_results : Dict[str, pd.DataFrame]
            Results from successful processor executions

        Returns
        -------
        Dict[str, Any]
            Comprehensive results summary with metadata
        """
        results_summary = {
            "processors_run": len(requested_processors),
            "successful_processors": len(processing_results),
            "processing_results": processing_results,
            "processor_details": {},
        }

        # Add details for each requested processor
        for processor_name in requested_processors:
            if processor_name in processing_results:
                # Successful processor
                df_result = processing_results[processor_name]
                results_summary["processor_details"][processor_name] = {
                    "rows_processed": len(df_result),
                    "columns": list(df_result.columns),
                    "success": True,
                    "data_shape": df_result.shape,
                    "memory_usage_mb": round(
                        df_result.memory_usage(deep=True).sum() / 1024**2, 2
                    ),
                }
            else:
                # Failed processor
                results_summary["processor_details"][processor_name] = {
                    "rows_processed": 0,
                    "columns": [],
                    "success": False,
                    "error": "Processor execution failed",
                }

        return results_summary
