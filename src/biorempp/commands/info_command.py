"""
info_command.py
--------------
Information Display Command Implementation

This module implements the InfoCommand class for displaying comprehensive
database information and system help without requiring input file processing.
It provides users with detailed insights into available databases, their
schemas, capabilities, and usage examples.

The InfoCommand serves as the primary interface for system discovery,
helping users understand the available resources and make informed decisions
about database selection and analysis workflows.

Information Types:
    - Database Listing: Complete overview of all available databases
    - Database Details: In-depth information about specific databases
    - Schema Information: Column structures and data types
    - Usage Examples: Practical command-line examples
    - Feature Summaries: Key capabilities and record counts

Database Coverage:
    - BioRemPP: Core bioremediation potential database
    - HADEG: Hydrocarbon degradation genes and pathways
    - KEGG: Degradation pathway information
    - ToxCSM: Toxicity prediction and chemical safety

Display Features:
    - Formatted console output with icons and sections
    - Comprehensive database statistics and metadata
    - Practical usage examples and command syntax
    - Schema visualization with column information
    - File size and record count information
"""

from typing import Any, Dict

from biorempp.commands.base_command import BaseCommand


class InfoCommand(BaseCommand):
    """
    Command for displaying database information and system help.

    This command handles informational requests that don't require
    input file processing, such as listing available databases or
    showing database-specific information.

    Supported info types:
    - databases: List all available databases
    - database_info: Show detailed information about a specific database
    """

    def __init__(self, info_type: str, target: str = None):
        """
        Initialize info command with type and target.

        Parameters
        ----------
        info_type : str
            Type of information to display ('databases', 'database_info')
        target : str, optional
            Target database name for database_info type
        """
        super().__init__()
        self.info_type = info_type
        self.target = target

    def execute(self, args) -> Dict[str, Any]:
        """
        Execute info command logic.

        Parameters
        ----------
        args : argparse.Namespace
            Parsed command line arguments

        Returns
        -------
        Dict[str, Any]
            Information results based on command type
        """
        self.logger.info(f"Executing info command: {self.info_type}")

        if self.info_type == "databases":
            return self._list_databases()
        elif self.info_type == "database_info":
            return self._show_database_info(self.target)
        else:
            raise ValueError(f"Unsupported info type: {self.info_type}")

    def validate_specific_input(self, args) -> bool:
        """
        Validate info command specific inputs.

        Info commands generally don't require specific validation
        as they are informational only.

        Parameters
        ----------
        args : argparse.Namespace
            Parsed command line arguments

        Returns
        -------
        bool
            Always True for info commands
        """
        self.logger.debug(f"Info command validation for type: {self.info_type}")
        return True

    def _list_databases(self) -> Dict[str, Any]:
        """
        List all available databases.

        Returns
        -------
        Dict[str, Any]
            Database listing information
        """
        databases = {
            "biorempp": {
                "name": "BioRemPP Core Database",
                "description": (
                    "Bioremediation Potential Profile Database " "(6,623 records)"
                ),
                "file": "database_biorempp.csv",
                "size": "0.69 MB",
            },
            "hadeg": {
                "name": "HADEG Database",
                "description": (
                    "Hydrocarbon Aerobic Degradation Enzymes and Genes "
                    "(1,168 records)"
                ),
                "file": "database_hadeg.csv",
                "size": "0.04 MB",
            },
            "kegg": {
                "name": "KEGG Pathways",
                "description": "20 KEGG for xenobiotic biodegradation "
                "pathways (871 records)",
                "file": "kegg_degradation_pathways.csv",
                "size": "0.02 MB",
            },
            "toxcsm": {
                "name": "ToxCSM Database",
                "description": (
                    "Comprehensive Prediction of Small Molecule Toxicity Profiles "
                    "(323 records, 66 endpoints)"
                ),
                "file": "database_toxcsm.csv",
                "size": "0.18 MB",
            },
        }

        print("\n[DATABASES] Available Databases:")
        print("=" * 70)

        for db_key, db_info in databases.items():
            print(f"\n[DB] {db_key.upper()}")
            print(f"   Name: {db_info['name']}")
            print(f"   Description: {db_info['description']}")
            print(f"   File: {db_info['file']} ({db_info['size']})")

        print("\n[SAMPLE] Example Input Data:")
        print("   File: sample_data.txt (0.18 MB)")
        print("   Content: 10 organisms with 23,663 KO identifiers")
        print("   Format: Organism headers (>) and KO entries")

        print("\n[USAGE] Usage Examples:")
        print("   biorempp --input sample_data.txt --all-databases")
        print("   biorempp --input sample_data.txt --database biorempp")
        print("   biorempp --database-info biorempp")
        print("   biorempp --list-databases")
        print()

        return {"databases": databases}

    def _show_database_info(self, database_name: str) -> Dict[str, Any]:
        """
        Show detailed information about a specific database.

        Parameters
        ----------
        database_name : str
            Name of the database to show info for

        Returns
        -------
        Dict[str, Any]
            Detailed database information
        """
        database_details = {
            "biorempp": {
                "name": "BioRemPP Core Database",
                "description": ("Bioremediation Potential Profile"),
                "columns": [
                    "ko",
                    "genesymbol",
                    "genename",
                    "cpd",
                    "compoundclass",
                    "referenceAG",
                    "compoundname",
                    "enzyme_activity",
                ],
                "size": "6,623 records",
                "file_size": "0.69 MB",
                "format": "CSV with semicolon separator",
                "key_features": [
                    "986 unique KEGG Orthology (KO) identifiers",
                    "323 unique compounds across 12 chemical classes",
                    "978 unique enzyme gene symbols",
                    "150 different enzyme activities",
                ],
                "usage": ("Primary database for" " bioremediation analysis"),
            },
            "hadeg": {
                "name": "Hydrocarbon Aerobic Degradation Enzymes and Genes",
                "description": (
                    "manually curated database containing "
                    "sequences of experimentally validated"
                ),
                "columns": ["Gene", "ko", "Pathway", "compound_pathway"],
                "size": "1,168 records",
                "file_size": "0.04 MB",
                "format": "CSV with semicolon separator",
                "key_features": [
                    "323 unique genes involved in degradation",
                    "339 unique KO identifiers",
                    "71 distinct metabolic pathways",
                    "5 major compound pathway categories (Alkanes, Aromatics, etc.)",
                ],
                "usage": (
                    "Specific biodegradation pathway analysis "
                    "and gene-pathway mapping"
                ),
            },
            "kegg": {
                "name": "KEGG Degradation Pathways",
                "description": ("KEGG-derived biodegradation pathway information"),
                "columns": ["ko", "pathname", "genesymbol"],
                "size": "871 records",
                "file_size": "0.02 MB",
                "format": "CSV with semicolon separator",
                "key_features": [
                    "517 unique KO identifiers",
                    "20 degradation pathways (Naphthalene, Aromatic, Toluene, etc.)",
                    "513 unique gene symbols",
                    "Focus on xenobiotic degradation",
                ],
                "usage": (
                    "Pathway enrichment analysis and degradation route "
                    "identification"
                ),
            },
            "toxcsm": {
                "name": "ToxCSM Toxicity Database",
                "description": ("Comprehensive toxicity prediction database"),
                "columns": [
                    "SMILES",
                    "cpd",
                    "ChEBI",
                    "compoundname",
                    "66 toxicity endpoints",
                    "Nuclear receptor (NR_*), Stress response (SR_*), "
                    "Genotoxicity (Gen_*)",
                    "Environmental (Env_*), Organ toxicity (Org_*) assessments",
                ],
                "size": "323 records",
                "file_size": "0.18 MB",
                "format": "CSV with semicolon separator",
                "key_features": [
                    "314 unique SMILES molecular structures",
                    "66 toxicity endpoints with value/label pairs",
                    (
                        "Multiple toxicity categories: Nuclear receptors, "
                        "Stress response, Genotoxicity, Environmental, "
                        "Organ-specific"
                    ),
                    "ChEBI identifiers for chemical standardization",
                ],
                "usage": "Comprehensive toxicity evaluation and safety assessment",
            },
        }

        if database_name not in database_details:
            print(f"[ERROR] Database '{database_name}' not found.")
            print(f"Available databases: {', '.join(database_details.keys())}")
            return {"error": f"Database '{database_name}' not found"}

        db_info = database_details[database_name]

        print(f"\n {db_info['name']}")
        print("=" * 70)
        print(f" Description: {db_info['description']}")
        print(f" Size: {db_info['size']} ({db_info['file_size']})")
        print(f"[FORMAT] Format: {db_info['format']}")

        print("\n🔍 Database Schema:")
        for i, col in enumerate(db_info["columns"][:8], 1):  # Show first 8 columns
            print(f"   {i:2d}. {col}")
        if len(db_info["columns"]) > 8:
            print(f"   ... and {len(db_info['columns']) - 8} more columns")

        if "key_features" in db_info:
            print("\n⭐ Key Features:")
            for feature in db_info["key_features"]:
                print(f"   • {feature}")

        print("\n🎯 Primary Usage:")
        print(f"   {db_info['usage']}")

        print("\n[USAGE] Usage Examples:")
        print(f"   biorempp --input sample_data.txt --database {database_name}")
        print("   biorempp --input sample_data.txt --all-databases")
        print("   biorempp --list-databases")
        print()

        return {"database_info": {database_name: db_info}}
