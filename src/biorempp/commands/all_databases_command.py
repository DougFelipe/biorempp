"""
All Databases Merger Command Implementation.

This module implements the AllDatabasesMergerCommand for executing
database merging with ALL available databases in sequence.
"""

from typing import Any, Dict

from biorempp.commands.base_command import BaseCommand
from biorempp.pipelines.input_processing import (
    run_biorempp_processing_pipeline,
    run_hadeg_processing_pipeline,
    run_kegg_processing_pipeline,
    run_toxcsm_processing_pipeline,
)


class AllDatabasesMergerCommand(BaseCommand):
    """
    Command for merging input with ALL databases in sequence.

    Executes merging with all 4 databases individually:
    - biorempp: BioRemPP database
    - hadeg: HAdeg database
    - kegg: KEGG pathway database
    - toxcsm: ToxCSM toxicity database

    Creates individual output files for each database, providing
    comprehensive coverage of all available data sources.
    """

    # Database merge functions mapping
    MERGE_FUNCTIONS = {
        "biorempp": run_biorempp_processing_pipeline,
        "hadeg": run_hadeg_processing_pipeline,
        "kegg": run_kegg_processing_pipeline,
        "toxcsm": run_toxcsm_processing_pipeline,
    }

    def validate_specific_input(self, args) -> bool:
        """
        Validate all databases merger specific inputs.

        Parameters
        ----------
        args : argparse.Namespace
            Parsed command line arguments

        Returns
        -------
        bool
            True if validation passes, False otherwise
        """
        # Validate input file is provided
        if not hasattr(args, "input") or not args.input:
            self.logger.error("Input file is required for database merging")
            return False

        self.logger.debug("All databases merger validation passed")
        return True

    def execute_implementation(self, args) -> Dict[str, Any]:
        """
        Execute merging with all databases in sequence.

        Creates individual output files for each database merger,
        providing comprehensive data coverage.

        Parameters
        ----------
        args : argparse.Namespace
            Parsed command line arguments

        Returns
        -------
        Dict[str, Any]
            Results from all database mergers
        """
        self.logger.info("Starting merge with ALL databases")
        results = {}

        # Execute merge with each database individually
        for db_name, merge_func in self.MERGE_FUNCTIONS.items():
            try:
                self.logger.info(f"Merging with {db_name} database...")

                # Create modified args for individual database
                individual_args = self._create_individual_args(args, db_name)

                # Execute merge function
                result = merge_func(individual_args)
                results[db_name] = result

                self.logger.info(f"Successfully merged with {db_name} database")

            except Exception as e:
                self.logger.error(f"Failed to merge with {db_name} database: {e}")
                results[db_name] = {"error": str(e)}
                # Continue with other databases even if one fails

        # Log summary
        successful_merges = [
            db for db, result in results.items() if "error" not in result
        ]
        failed_merges = [db for db, result in results.items() if "error" in result]

        self.logger.info(
            f"All databases merge completed. "
            f"Successful: {len(successful_merges)}/{len(self.MERGE_FUNCTIONS)} "
            f"({', '.join(successful_merges)})"
        )

        if failed_merges:
            self.logger.warning(f"Failed merges: {', '.join(failed_merges)}")

        return results

    def _create_individual_args(self, args, database_name: str):
        """
        Create modified args for individual database merger.

        Parameters
        ----------
        args : argparse.Namespace
            Original parsed arguments
        database_name : str
            Name of the database to merge with

        Returns
        -------
        argparse.Namespace
            Modified arguments for individual database merger
        """
        # Create a copy of args
        import copy

        individual_args = copy.deepcopy(args)

        # Set pipeline type for individual merger
        individual_args.pipeline_type = database_name

        return individual_args
