"""
Database Merger Command Implementation.

This module implements the DatabaseMergerCommand for executing
database merging operations (biorempp, kegg, hadeg, toxcsm, all).
"""

from typing import Any, Dict, Union

from biorempp.commands.base_command import BaseCommand
from biorempp.pipelines.input_processing import (
    run_all_processing_pipelines,
    run_biorempp_processing_pipeline,
    run_hadeg_processing_pipeline,
    run_kegg_processing_pipeline,
    run_toxcsm_processing_pipeline,
)


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
        Execute the traditional pipeline processing.

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
        self.logger.info(f"Executing traditional pipeline: {args.pipeline_type}")

        # Get the appropriate pipeline function
        pipeline_function = self.PIPELINE_MAP[args.pipeline_type]

        # Build pipeline arguments dynamically
        pipeline_kwargs = self._build_pipeline_kwargs(args)

        # Execute the pipeline
        self.logger.debug(f"Pipeline kwargs: {list(pipeline_kwargs.keys())}")
        result = pipeline_function(**pipeline_kwargs)

        self.logger.info(
            f"Traditional pipeline {args.pipeline_type} completed successfully"
        )
        return result

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
            "output_dir": args.output_dir,
            "add_timestamp": args.add_timestamp,
        }

        # Optional arguments - only add if not None
        optional_args = {
            "database": getattr(args, "database", None),
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
