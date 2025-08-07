"""
Info Command Implementation.

This module implements the InfoCommand for displaying database information
and system help without requiring input files.
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

    def execute_specific_logic(self, args) -> Dict[str, Any]:
        """
        Execute info command specific logic.

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
                "name": "BioRemPP Database",
                "description": "Core BioRemPP biological compounds database",
                "file": "database_biorempp.csv",
            },
            "hadeg": {
                "name": "HAdeg Database",
                "description": "Human Metabolism Database for biodegradation pathways",
                "file": "database_hadegDB.csv",
            },
            "kegg": {
                "name": "KEGG Pathways",
                "description": "KEGG degradation pathways database",
                "file": "kegg_degradation_pathways.csv",
            },
            "toxcsm": {
                "name": "ToxCSM Database",
                "description": "Toxicity prediction and assessment database",
                "file": "database_toxcsm.csv",
            },
        }

        print("\n🗄️  Available Databases:")
        print("=" * 50)
        for db_key, db_info in databases.items():
            print(f"📊 {db_key.upper()}")
            print(f"   Name: {db_info['name']}")
            print(f"   Description: {db_info['description']}")
            print(f"   File: {db_info['file']}")
            print()

        print("💡 Usage Examples:")
        print("   biorempp --input data.txt --all-databases")
        print("   biorempp --input data.txt --database biorempp")
        print("   biorempp --database-info biorempp")
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
                "description": "Comprehensive biological compounds database for biodegradation research",
                "columns": [
                    "compound_id",
                    "compound_name",
                    "class",
                    "subclass",
                    "pathway",
                ],
                "size": "~5000 compounds",
                "format": "CSV with semicolon separator",
                "usage": "Primary database for compound identification and classification",
            },
            "hadeg": {
                "name": "Human Metabolism Database (HAdeg)",
                "description": "Specialized database for human metabolism biodegradation pathways",
                "columns": ["metabolite_id", "pathway", "enzyme", "reaction"],
                "size": "~2500 metabolites",
                "format": "CSV with semicolon separator",
                "usage": "Human-specific biodegradation pathway analysis",
            },
            "kegg": {
                "name": "KEGG Degradation Pathways",
                "description": "KEGG-derived biodegradation pathway information",
                "columns": ["pathway_id", "pathway_name", "compounds", "enzymes"],
                "size": "~800 pathways",
                "format": "CSV with semicolon separator",
                "usage": "Pathway enrichment and degradation route analysis",
            },
            "toxcsm": {
                "name": "ToxCSM Toxicity Database",
                "description": "Comprehensive toxicity prediction and assessment database",
                "columns": [
                    "compound_id",
                    "toxicity_endpoint",
                    "prediction",
                    "confidence",
                ],
                "size": "~3000 toxicity assessments",
                "format": "CSV with semicolon separator",
                "usage": "Toxicity evaluation and safety assessment",
            },
        }

        if database_name not in database_details:
            print(f"❌ Database '{database_name}' not found.")
            print(f"Available databases: {', '.join(database_details.keys())}")
            return {"error": f"Database '{database_name}' not found"}

        db_info = database_details[database_name]

        print(f"\n📊 {db_info['name']}")
        print("=" * 60)
        print(f"Description: {db_info['description']}")
        print(f"Size: {db_info['size']}")
        print(f"Format: {db_info['format']}")
        print(f"Columns: {', '.join(db_info['columns'])}")
        print(f"Usage: {db_info['usage']}")
        print()
        print("💡 Usage Examples:")
        print(f"   biorempp --input data.txt --database {database_name}")
        print("   biorempp --input data.txt --all-databases")
        print()

        return {"database_info": {database_name: db_info}}
