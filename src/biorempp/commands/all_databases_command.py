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

    def execute(self, args) -> Dict[str, Any]:
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

                # Build pipeline kwargs for this database
                pipeline_kwargs = self._build_pipeline_kwargs(args, db_name)

                # Execute merge function
                result = merge_func(**pipeline_kwargs)
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

    def _build_pipeline_kwargs(self, args, database_name: str) -> Dict[str, Any]:
        """
        Build pipeline keyword arguments for specific database.

        Parameters
        ----------
        args : argparse.Namespace
            Parsed command line arguments
        database_name : str
            Name of the database to merge with

        Returns
        -------
        Dict[str, Any]
            Dictionary of keyword arguments for pipeline execution
        """
        # Required arguments for all pipelines
        pipeline_kwargs = {
            "input_path": args.input,
            "output_dir": getattr(args, "output_dir", "outputs/results_tables"),
            "add_timestamp": getattr(args, "add_timestamp", True),
        }

        # Map database-specific parameters
        database_path = self._get_database_path(database_name)
        if database_name == "biorempp":
            pipeline_kwargs["database_path"] = database_path
        elif database_name == "kegg":
            pipeline_kwargs["kegg_database_path"] = database_path
        elif database_name == "hadeg":
            pipeline_kwargs["hadeg_database_path"] = database_path
        elif database_name == "toxcsm":
            pipeline_kwargs["toxcsm_database_path"] = database_path

        return pipeline_kwargs

    def _get_database_path(self, database_name: str) -> str:
        """
        Get the full path to a database file.

        Parameters
        ----------
        database_name : str
            Name of the database (biorempp, hadeg, kegg, toxcsm)

        Returns
        -------
        str
            Full path to the database file
        """
        import os

        # Map database names to file names
        database_files = {
            "biorempp": "database_biorempp.csv",
            "hadeg": "database_hadeg.csv",
            "kegg": "kegg_degradation_pathways.csv",
            "toxcsm": "database_toxcsm.csv",
        }

        if database_name not in database_files:
            raise ValueError(f"Unknown database: {database_name}")

        # Get the current directory and build path to data folder
        this_dir = os.path.dirname(os.path.abspath(__file__))
        database_path = os.path.normpath(
            os.path.join(this_dir, "..", "data", database_files[database_name])
        )

        return database_path
