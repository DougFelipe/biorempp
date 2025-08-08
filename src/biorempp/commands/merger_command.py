"""
Database Merger Command Implementation.

This module implements the DatabaseMergerCommand for executing
database merging operations (biorempp, kegg, hadeg, toxcsm, all).
"""

import time
from typing import Any, Dict, Union

from biorempp.commands.base_command import BaseCommand
from biorempp.pipelines.input_processing import (
    run_biorempp_processing_pipeline,
    run_hadeg_processing_pipeline,
    run_kegg_processing_pipeline,
    run_toxcsm_processing_pipeline,
)
from biorempp.utils.error_handler import get_error_handler


class DatabaseMergerCommand(BaseCommand):
    """
    Command for executing database merging operations.

    Supports individual database merger types:
    - biorempp: Merge with BioRemPP database only
    - kegg: Merge with KEGG pathway database only
    - hadeg: Merge with HAdeg database only
    - toxcsm: Merge with ToxCSM toxicity database only

    For merging with ALL databases, use AllDatabasesMergerCommand instead.

    This command handles input validation and database merging execution
    maintaining the same robust functionality as the original implementation.
    """

    # Pipeline mapping for type validation and execution
    PIPELINE_MAP = {
        "biorempp": run_biorempp_processing_pipeline,
        "kegg": run_kegg_processing_pipeline,
        "hadeg": run_hadeg_processing_pipeline,
        "toxcsm": run_toxcsm_processing_pipeline,
    }

    def validate_specific_input(self, args) -> bool:
        """
        Validate traditional pipeline specific inputs.

        Checks that the pipeline type is supported and that required
        arguments are present for traditional pipeline execution.

        Parameters
        ----------
        args : argparse.Namespace
            Parsed command line arguments

        Returns
        -------
        bool
            True if validation passes, False otherwise
        """
        # Validate pipeline type is supported
        if args.pipeline_type not in self.PIPELINE_MAP:
            available_types = list(self.PIPELINE_MAP.keys())
            self.logger.error(
                f"Unsupported pipeline type: '{args.pipeline_type}'. "
                f"Available types: {available_types}"
            )
            return False

        # Validate input file is provided for processing pipelines
        if not hasattr(args, "input") or not args.input:
            self.logger.error(
                "Input file is required for traditional pipeline processing"
            )
            return False

        self.logger.debug(
            f"Traditional pipeline validation passed for type: {args.pipeline_type}"
        )
        return True

    def execute(self, args) -> Union[str, Dict[str, str]]:
        """
        Execute the traditional pipeline processing with enhanced user feedback.

        Builds pipeline arguments dynamically and executes the appropriate
        pipeline function based on the pipeline type specified.

        Parameters
        ----------
        args : argparse.Namespace
            Parsed command line arguments

        Returns
        -------
        Union[str, Dict[str, str]]
            Path to output file (single pipeline) or dictionary of
            pipeline names to output paths (all pipelines)
        """
        # Initialize error handler for exception handling
        error_handler = get_error_handler()

        try:
            self.logger.info(f"Executing traditional pipeline: {args.pipeline_type}")

            # Execute pipeline logic without display
            # (display handled by OutputFormatter)

            # Validate input file silently
            import os

            if not os.path.exists(args.input):
                raise FileNotFoundError(f"Input file not found: {args.input}")

            # Execute single database processing - no feedback display here

            # Get the appropriate pipeline function
            pipeline_function = self.PIPELINE_MAP[args.pipeline_type]

            # Build pipeline arguments dynamically
            pipeline_kwargs = self._build_pipeline_kwargs(args)

            # Execute the pipeline
            start_time = time.time()
            self.logger.debug(f"Pipeline kwargs: {list(pipeline_kwargs.keys())}")
            result = pipeline_function(**pipeline_kwargs)
            processing_time = time.time() - start_time

            # Return result for OutputFormatter to handle display
            if isinstance(result, dict) and "output_path" in result:
                # Add processing time to result for display
                result["processing_time"] = processing_time
                return result
            elif isinstance(result, str):
                # Fallback for old format
                return {
                    "output_path": result,
                    "filename": os.path.basename(result),
                    "matches": 0,  # Unknown for old format
                    "processing_time": processing_time,
                }

            self.logger.info(
                f"Traditional pipeline {args.pipeline_type} completed successfully"
            )
            return result

        except Exception as e:
            # Enhanced error handling
            pipeline_type = args.pipeline_type if args.pipeline_type else "processing"
            context = f"processing_{pipeline_type}"
            error_handler.show_error_to_user(e, context)
            raise

    def _get_database_path(self, database_name):
        """
        Get the full path to the database file based on the database name.

        Parameters
        ----------
        database_name : str
            Name of the database ('biorempp', 'hadeg', 'kegg', 'toxcsm')

        Returns
        -------
        str or None
            Full path to the database file, or None if not specified
        """
        if database_name is None:
            return None

        # Map database names to file names
        database_files = {
            "biorempp": "database_biorempp.csv",
            "hadeg": "database_hadeg.csv",
            "kegg": "kegg_degradation_pathways.csv",
            "toxcsm": "database_toxcsm.csv",
        }

        if database_name not in database_files:
            return None

        # Get the current directory and build path to data folder
        import os

        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.normpath(os.path.join(current_dir, "..", "data"))
        database_path = os.path.join(data_dir, database_files[database_name])

        return database_path

    def _build_pipeline_kwargs(self, args) -> Dict[str, Any]:
        """
        Build pipeline keyword arguments from parsed command line arguments.

        This method maps CLI arguments to pipeline function parameters,
        including only non-None values to avoid overriding pipeline defaults.

        Parameters
        ----------
        args : argparse.Namespace
            Parsed command line arguments

        Returns
        -------
        Dict[str, Any]
            Dictionary of keyword arguments for pipeline execution
        """
        # Required arguments for all pipelines
        pipeline_kwargs = {
            "input_path": args.input,
            "output_dir": getattr(args, "output_dir", "outputs/results_tables"),
            "add_timestamp": getattr(args, "add_timestamp", False),
        }

        # Map database-specific parameters based on pipeline
        database_name = getattr(args, "database", None)
        if database_name:
            database_path = self._get_database_path(database_name)
            if database_name == "biorempp":
                pipeline_kwargs["database_path"] = database_path
            elif database_name == "kegg":
                pipeline_kwargs["kegg_database_path"] = database_path
            elif database_name == "hadeg":
                pipeline_kwargs["hadeg_database_path"] = database_path
            elif database_name == "toxcsm":
                pipeline_kwargs["toxcsm_database_path"] = database_path

        # Optional arguments - only add if not None
        optional_args = {
            "biorempp_database": getattr(args, "biorempp_database", None),
            "kegg_database": getattr(args, "kegg_database", None),
            "hadeg_database": getattr(args, "hadeg_database", None),
            "toxcsm_database": getattr(args, "toxcsm_database", None),
            "output_filename": getattr(args, "output_filename", None),
            "biorempp_output_filename": getattr(args, "biorempp_output_filename", None),
            "kegg_output_filename": getattr(args, "kegg_output_filename", None),
            "hadeg_output_filename": getattr(args, "hadeg_output_filename", None),
            "toxcsm_output_filename": getattr(args, "toxcsm_output_filename", None),
            "sep": getattr(args, "sep", None),
        }

        # Only add arguments that are not None
        for key, value in optional_args.items():
            if value is not None:
                pipeline_kwargs[key] = value

        return pipeline_kwargs
