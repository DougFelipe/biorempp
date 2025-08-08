"""
Database Merger Command Implementation.

This module implements the DatabaseMergerCommand for executing
database merging operations (biorempp, kegg, hadeg, toxcsm, all).
"""

import time
from typing import Any, Dict, Union

from biorempp.commands.base_command import BaseCommand
from biorempp.pipelines.input_processing import (
    run_all_processing_pipelines,
    run_biorempp_processing_pipeline,
    run_hadeg_processing_pipeline,
    run_kegg_processing_pipeline,
    run_toxcsm_processing_pipeline,
)
from biorempp.utils.error_handler import get_error_handler
from biorempp.utils.user_feedback import get_user_feedback


class DatabaseMergerCommand(BaseCommand):
    """
    Command for executing database merging operations.

    Supports all database merger types:
    - all: Merge with ALL databases (biorempp, kegg, hadeg, toxcsm)
    - biorempp: Merge with BioRemPP database only
    - kegg: Merge with KEGG pathway database only
    - hadeg: Merge with HAdeg database only
    - toxcsm: Merge with ToxCSM toxicity database only

    This command handles input validation and database merging execution
    maintaining the same robust functionality as the original implementation.
    """

    # Pipeline mapping for type validation and execution
    PIPELINE_MAP = {
        "all": run_all_processing_pipelines,
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
        # Initialize feedback system based on verbosity
        verbosity = self._get_verbosity_level(args)
        feedback = get_user_feedback(verbosity)
        error_handler = get_error_handler()

        try:
            self.logger.info(f"Executing traditional pipeline: {args.pipeline_type}")

            # Start processing feedback
            database_name = args.pipeline_type if args.pipeline_type != "all" else None
            feedback.start_processing(args.input, database_name)

            # Show loading step with progress
            feedback.show_loading_step("Loading input data", show_progress=True)
            time.sleep(0.5)  # Simulate loading time

            # Validate input file and show feedback
            import os

            if os.path.exists(args.input):
                # Count lines for feedback (simplified)
                with open(args.input, "r", encoding="utf-8") as f:
                    line_count = sum(1 for line in f if line.strip())
                feedback.complete_loading_step("", f"{line_count:,} identifiers loaded")
            else:
                raise FileNotFoundError(f"Input file not found: {args.input}")

            # Show database connection step
            if args.pipeline_type != "all":
                # Single database processing
                db_name = args.pipeline_type.upper()
                # TODO: Get actual database size - using placeholder for now
                feedback.show_database_connection(db_name, 6623, show_progress=True)

                # Show processing progress
                feedback.show_processing_progress("Processing data", show_bar=True)

                # Get the appropriate pipeline function
                pipeline_function = self.PIPELINE_MAP[args.pipeline_type]

                # Build pipeline arguments dynamically
                pipeline_kwargs = self._build_pipeline_kwargs(args)

                # Execute the pipeline
                start_time = time.time()
                self.logger.debug(f"Pipeline kwargs: {list(pipeline_kwargs.keys())}")
                result = pipeline_function(**pipeline_kwargs)
                processing_time = time.time() - start_time

                # Show saving step
                if isinstance(result, dict) and "output_path" in result:
                    feedback.show_saving_results(result["filename"], show_progress=True)

                    # Show final results with correct values
                    feedback.show_processing_results(
                        {
                            "output_file": result["output_path"],
                            "matches": result.get("matches", 0),
                            "processing_time": processing_time,
                        }
                    )
                elif isinstance(result, str):
                    # Fallback for old format
                    feedback.show_saving_results(result, show_progress=True)

                    # Show final results
                    feedback.show_processing_results(
                        {
                            "output_file": result,
                            "matches": 0,  # Unknown for old format
                            "processing_time": processing_time,
                        }
                    )
            else:
                # All databases processing
                feedback.show_all_databases_processing(4)

                # Get the appropriate pipeline function
                pipeline_function = self.PIPELINE_MAP[args.pipeline_type]

                # Build pipeline arguments dynamically
                pipeline_kwargs = self._build_pipeline_kwargs(args)

                # Execute the pipeline with step-by-step feedback
                start_time = time.time()
                self.logger.debug(f"Pipeline kwargs: {list(pipeline_kwargs.keys())}")

                # Simulate processing each database
                databases = ["biorempp", "hadeg", "kegg", "toxcsm"]
                for i, db_name in enumerate(databases, 1):
                    db_upper = db_name.upper()
                    feedback.show_database_processing_step(
                        i, 4, db_upper, show_progress=True
                    )

                result = pipeline_function(**pipeline_kwargs)
                processing_time = time.time() - start_time

                # Show all databases results
                if isinstance(result, dict):
                    # Add processing time to results
                    for db_name in result:
                        if isinstance(result[db_name], dict):
                            avg_time = processing_time / len(result)
                            result[db_name]["processing_time"] = avg_time

                    feedback.show_all_databases_results(result)

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

    def _get_verbosity_level(self, args) -> str:
        """Get verbosity level from arguments."""
        if hasattr(args, "quiet") and args.quiet:
            return "SILENT"
        elif hasattr(args, "verbose") and args.verbose:
            return "VERBOSE"
        elif hasattr(args, "debug") and args.debug:
            return "DEBUG"
        else:
            return "NORMAL"

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
