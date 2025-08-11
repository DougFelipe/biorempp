"""
all_merger_command.py
--------------------
Comprehensive Multi-Database Merger Command Implementation

This module implements the AllDatabasesMergerCommand for executing
comprehensive data integration across all available BioRemPP databases
in a coordinated sequence. It provides complete analytical coverage by
processing input data against every database type.

The command orchestrates multiple database integrations to deliver
comprehensive bioremediation analysis, combining insights from gene
function, pathway information, degradation capabilities, and toxicity
assessments into a complete analytical workflow.

Multi-Database Integration:
    The command processes data sequentially against all four databases,
    creating individual output files for each database while maintaining
    data integrity and providing comprehensive error handling throughout
    the entire workflow.

Database Sequence:
    1. BioRemPP: Core bioremediation potential analysis
    2. HADEG: Hydrocarbon degradation gene identification
    3. KEGG: Degradation pathway enrichment analysis
    4. ToxCSM: Toxicity prediction and safety assessment

Processing Strategy:
    - Sequential execution with individual error handling
    - Continuation strategy: failures in one database don't stop others
    - Individual result tracking and reporting
    - Comprehensive logging and progress monitoring

Output Generation:
    Creates separate output files for each database, allowing users to
    analyze results independently or in combination based on their
    analytical needs and research questions.

Performance Considerations:
    - Memory management across multiple database operations
    - Error isolation to prevent cascade failures
    - Progress tracking for long-running operations
    - Resource optimization for comprehensive analysis
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
    Command for comprehensive multi-database integration operations.

    This command orchestrates complete bioremediation analysis by processing
    input data against all four available databases sequentially, providing
    comprehensive coverage of gene function, pathway information, degradation
    capabilities, and toxicity assessments.

    Database Coverage:
        - biorempp: Core bioremediation potential and gene-compound mapping
        - hadeg: Hydrocarbon degradation genes and pathway specialization
        - kegg: Metabolic pathway enrichment and degradation routes
        - toxcsm: Toxicity prediction and chemical safety evaluation

    Processing Strategy:
        Sequential execution with fault tolerance - failures in individual
        databases do not prevent processing of remaining databases, ensuring
        maximum data recovery and analytical completeness.

    Output Generation:
        Creates individual output files for each database:
        - BioRemPP_Results.txt: Core bioremediation analysis
        - HADEG_Results.txt: Hydrocarbon degradation analysis
        - KEGG_Results.txt: Pathway enrichment analysis
        - ToxCSM_Results.txt: Toxicity assessment analysis

    Command Benefits:
        - Complete analytical coverage in single execution
        - Fault tolerance prevents partial failures
        - Individual result files for focused analysis
        - Comprehensive logging and progress tracking
        - Optimized parameter handling for each database

    Performance Characteristics:
        - Memory management across multiple operations
        - Error isolation and recovery mechanisms
        - Progress monitoring for long-running workflows
        - Resource optimization for comprehensive analysis

    Use Cases:
        - Complete bioremediation potential assessment
        - Comprehensive environmental analysis workflows
        - Multi-database comparative studies
        - Complete organism characterization projects
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
        Execute comprehensive multi-database integration workflow.

        This method orchestrates sequential processing across all available
        databases, implementing a fault-tolerant strategy that continues
        processing even if individual databases encounter errors, ensuring
        maximum data recovery and analytical completeness.

        Parameters
        ----------
        args : argparse.Namespace
            Parsed command line arguments containing input file path,
            output directory specifications, and processing parameters.

        Returns
        -------
        Dict[str, Any]
            Comprehensive results from all database integration operations:
            {
                'biorempp': {result_dict or error_info},
                'hadeg': {result_dict or error_info},
                'kegg': {result_dict or error_info},
                'toxcsm': {result_dict or error_info}
            }

        Processing Strategy:
            - Sequential execution through all databases
            - Individual error handling and isolation
            - Continuation despite individual failures
            - Comprehensive logging and progress tracking
            - Result aggregation with success/failure reporting

        Error Handling:
            Individual database failures are captured and logged but do not
            prevent processing of remaining databases. This ensures maximum
            data recovery even in partial failure scenarios.

        Output Files Generated:
            - BioRemPP_Results.txt: Core bioremediation analysis
            - HADEG_Results.txt: Hydrocarbon degradation analysis
            - KEGG_Results.txt: Pathway enrichment analysis
            - ToxCSM_Results.txt: Toxicity assessment analysis

        Performance Monitoring:
            The method tracks processing statistics including successful
            and failed operations, providing comprehensive execution
            summaries for workflow assessment and optimization.
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
            "add_timestamp": getattr(args, "add_timestamp", False),
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
