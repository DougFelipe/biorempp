"""
Unit tests for the biorempp.cli.argument_parser module.

This module contains comprehensive tests for the BioRemPP command line
argument parsing system, including parameter validation, mutually exclusive
argument groups, and various usage scenarios.

The tests cover:
- Basic argument parsing
- Required argument validation
- Mutually exclusive groups
- Database selection
- Information commands
- Verbosity configurations
- Error and validation scenarios
"""

import argparse
import os
import platform

import pytest

from biorempp.cli.argument_parser import BioRemPPArgumentParser


class TestBioRemPPArgumentParser:
    """Test suite for the BioRemPPArgumentParser class."""

    def test_parser_initialization(self):
        """
        Test basic parser initialization.

        Verifies that the parser is created correctly and contains
        the expected basic argument structure.
        """
        # Act
        parser = BioRemPPArgumentParser()

        # Assert
        assert parser is not None
        assert parser.parser is not None
        assert isinstance(parser.parser, argparse.ArgumentParser)

    def test_input_argument_parsing(self, tmp_path):
        """
        Test parsing of the --input argument.

        Verifies that the input file argument is
        parsed correctly.
        """
        # Arrange
        input_file = tmp_path / "test_input.txt"
        input_file.write_text("sample data")
        parser = BioRemPPArgumentParser()

        # Act
        args = parser.parse_args(["--input", str(input_file), "--database", "biorempp"])

        # Assert
        assert args.input == str(input_file)

    def test_output_dir_argument_parsing(self, tmp_path):
        """
        Test parsing of the --output-dir argument.

        Verifies that the output directory argument is
        parsed correctly and paths are resolved to absolute paths.
        """
        # Arrange
        parser = BioRemPPArgumentParser()

        # Act - test with default value
        args_default = parser.parse_args(
            ["--input", "test.txt", "--database", "biorempp"]
        )

        # Act - test with custom value (absolute path for Windows)
        if platform.system() == "Windows":
            custom_path = "C:/custom/output"
        else:
            custom_path = "/custom/output"

        args_custom = parser.parse_args(
            [
                "--input",
                "test.txt",
                "--database",
                "biorempp",
                "--output-dir",
                custom_path,
            ]
        )

        # Assert - default path should be resolved to absolute path
        assert "outputs" in args_default.output_dir
        assert "results_tables" in args_default.output_dir
        assert os.path.isabs(args_default.output_dir)

        # Assert - custom absolute path should remain unchanged
        assert args_custom.output_dir == custom_path

    def test_all_databases_argument(self):
        """
        Test the --all-databases argument.

        Verifies that the option to process all databases
        is parsed correctly.
        """
        # Arrange
        parser = BioRemPPArgumentParser()

        # Act
        args = parser.parse_args(["--input", "test.txt", "--all-databases"])

        # Assert
        assert args.all_databases is True
        assert args.database is None

    def test_specific_database_argument(self):
        """
        Test the --database argument with different options.

        Verifies that specific database selection works
        with all supported database types.
        """
        # Arrange
        parser = BioRemPPArgumentParser()
        databases = ["biorempp", "kegg", "hadeg", "toxcsm"]

        for db in databases:
            # Act
            args = parser.parse_args(["--input", "test.txt", "--database", db])

            # Assert
            assert args.database == db
            assert args.all_databases is False

    def test_invalid_database_argument(self):
        """
        Test error handling for invalid database.

        Verifies that an invalid database name raises
        appropriate error.
        """
        # Arrange
        parser = BioRemPPArgumentParser()

        # Act & Assert
        with pytest.raises(SystemExit):
            parser.parse_args(["--input", "test.txt", "--database", "invalid_db"])

    def test_list_databases_argument(self):
        """
        Test the --list-databases argument.

        Verifies that the list databases command is
        parsed correctly.
        """
        # Arrange
        parser = BioRemPPArgumentParser()

        # Act
        args = parser.parse_args(["--list-databases"])

        # Assert
        assert args.list_databases is True

    def test_database_info_argument(self):
        """
        Test the --database-info argument.

        Verifies that the database info command is
        parsed correctly for different databases.
        """
        # Arrange
        parser = BioRemPPArgumentParser()
        databases = ["biorempp", "kegg", "hadeg", "toxcsm"]

        for db in databases:
            # Act
            args = parser.parse_args(["--database-info", db])

            # Assert
            assert args.database_info == db

    def test_quiet_argument(self):
        """
        Test the --quiet argument for silent mode.

        Verifies that the quiet flag is parsed correctly
        and sets appropriate verbosity level.
        """
        # Arrange
        parser = BioRemPPArgumentParser()

        # Act
        args_short = parser.parse_args(
            ["--input", "test.txt", "--database", "biorempp", "-q"]
        )

        args_long = parser.parse_args(
            ["--input", "test.txt", "--database", "biorempp", "--quiet"]
        )

        # Assert
        assert args_short.quiet is True
        assert args_long.quiet is True

    def test_verbose_argument(self):
        """
        Test the --verbose argument for detailed mode.

        Verifies that the verbose flag is parsed correctly
        and sets appropriate verbosity level.
        """
        # Arrange
        parser = BioRemPPArgumentParser()

        # Act
        args_short = parser.parse_args(
            ["--input", "test.txt", "--database", "biorempp", "-v"]
        )

        args_long = parser.parse_args(
            ["--input", "test.txt", "--database", "biorempp", "--verbose"]
        )

        # Assert
        assert args_short.verbose is True
        assert args_long.verbose is True

    def test_debug_argument(self):
        """
        Test the --debug argument for debug mode.

        Verifies that the debug flag is parsed correctly
        and sets appropriate verbosity level.
        """
        # Arrange
        parser = BioRemPPArgumentParser()

        # Act
        args = parser.parse_args(
            ["--input", "test.txt", "--database", "biorempp", "--debug"]
        )

        # Assert
        assert args.debug is True

    def test_mutually_exclusive_verbosity_arguments(self):
        """
        Test mutually exclusive verbosity arguments.

        Verifies that combining verbosity options raises
        appropriate errors.
        """
        # Arrange
        parser = BioRemPPArgumentParser()

        # Act & Assert - Test quiet + verbose conflict
        with pytest.raises(SystemExit):
            parser.parse_args(
                [
                    "--input",
                    "test.txt",
                    "--database",
                    "biorempp",
                    "--quiet",
                    "--verbose",
                ]
            )

        # Act & Assert - Test verbose + debug conflict
        with pytest.raises(SystemExit):
            parser.parse_args(
                [
                    "--input",
                    "test.txt",
                    "--database",
                    "biorempp",
                    "--verbose",
                    "--debug",
                ]
            )

        # Act & Assert - Test quiet + debug conflict
        with pytest.raises(SystemExit):
            parser.parse_args(
                ["--input", "test.txt", "--database", "biorempp", "--quiet", "--debug"]
            )

    def test_short_verbosity_options(self):
        """
        Test short verbosity options.

        Verifies that all short verbosity flags work correctly
        and are mutually exclusive.
        """
        # Arrange
        parser = BioRemPPArgumentParser()

        # Act - Test individual short options
        args_q = parser.parse_args(
            ["--input", "test.txt", "--database", "biorempp", "-q"]
        )

        args_v = parser.parse_args(
            ["--input", "test.txt", "--database", "biorempp", "-v"]
        )

        # Assert
        assert args_q.quiet is True
        assert args_v.verbose is True

        # Act & Assert - Test conflicting short options
        with pytest.raises(SystemExit):
            parser.parse_args(
                ["--input", "test.txt", "--database", "biorempp", "-q", "-v"]
            )

    def test_info_commands_without_input(self):
        """
        Test information commands that don't require input.

        Verifies that info commands work without requiring
        input file or database selection.
        """
        # Arrange
        parser = BioRemPPArgumentParser()

        # Act & Assert - List databases
        args_list = parser.parse_args(["--list-databases"])
        assert args_list.list_databases is True

        # Act & Assert - Database info
        args_info = parser.parse_args(["--database-info", "biorempp"])
        assert args_info.database_info == "biorempp"

    def test_get_parser_method(self):
        """
        Test the get_parser() method.

        Verifies that the get_parser method returns
        the correct ArgumentParser instance.
        """
        # Arrange
        parser_wrapper = BioRemPPArgumentParser()

        # Act
        parser = parser_wrapper.get_parser()

        # Assert
        assert isinstance(parser, argparse.ArgumentParser)
        assert parser is parser_wrapper.parser

    def test_complex_argument_combinations(self, tmp_path):
        """
        Test complex combinations of arguments.

        Verifies that various valid argument combinations
        are parsed correctly.
        """
        # Arrange
        input_file = tmp_path / "complex_test.txt"
        input_file.write_text("test data")
        parser = BioRemPPArgumentParser()

        # Define platform-specific path
        if platform.system() == "Windows":
            custom_path = "C:/custom/output"
        else:
            custom_path = "/custom/output"

        # Act
        args = parser.parse_args(
            [
                "--input",
                str(input_file),
                "--database",
                "kegg",
                "--output-dir",
                custom_path,
                "--verbose",
            ]
        )

        # Assert
        assert args.input == str(input_file)
        assert args.database == "kegg"
        assert args.output_dir == custom_path
        assert args.verbose is True
        assert args.quiet is False
        assert args.debug is False

    @pytest.mark.parametrize("database", ["biorempp", "kegg", "hadeg", "toxcsm"])
    def test_all_database_options_parametrized(self, database):
        """
        Test all database options parametrized.

        Verifies that all supported database options
        are parsed correctly.
        """
        # Arrange
        parser = BioRemPPArgumentParser()

        # Act
        args = parser.parse_args(["--input", "test.txt", "--database", database])

        # Assert
        assert args.database == database

    @pytest.mark.parametrize(
        "verbosity_args,expected",
        [
            (["-q"], {"quiet": True, "verbose": False, "debug": False}),
            (["-v"], {"quiet": False, "verbose": True, "debug": False}),
            (["--quiet"], {"quiet": True, "verbose": False, "debug": False}),
            (["--verbose"], {"quiet": False, "verbose": True, "debug": False}),
            (["--debug"], {"quiet": False, "verbose": False, "debug": True}),
        ],
    )
    def test_all_verbosity_options_parametrized(self, verbosity_args, expected):
        """
        Test all verbosity options parametrized.

        Verifies that all verbosity flags are parsed correctly
        and set appropriate values.
        """
        # Arrange
        parser = BioRemPPArgumentParser()

        # Act
        args = parser.parse_args(
            ["--input", "test.txt", "--database", "biorempp"] + verbosity_args
        )

        # Assert
        for attr, value in expected.items():
            assert getattr(args, attr) == value

    @pytest.mark.parametrize(
        "info_command",
        [
            ["--list-databases"],
            ["--database-info", "biorempp"],
            ["--database-info", "kegg"],
            ["--database-info", "hadeg"],
            ["--database-info", "toxcsm"],
        ],
    )
    def test_info_commands_work_without_required_args(self, info_command):
        """
        Test that info commands work without required arguments.

        Verifies that information commands function properly
        without requiring input files or database selection.
        """
        # Arrange
        parser = BioRemPPArgumentParser()

        # Act
        args = parser.parse_args(info_command)

        # Assert
        if "--list-databases" in info_command:
            assert args.list_databases is True
        else:
            assert args.database_info in ["biorempp", "kegg", "hadeg", "toxcsm"]

    def test_help_text_generation(self):
        """
        Test help text generation.

        Verifies that the parser generates appropriate
        help text.
        """
        # Arrange
        parser = BioRemPPArgumentParser()

        # Act
        help_text = parser.get_parser().format_help()

        # Assert
        assert "BioRemPP" in help_text
        assert "--input" in help_text
        assert "--database" in help_text
        assert "--all-databases" in help_text
        assert "--output-dir" in help_text
        assert "--verbose" in help_text
        assert "--quiet" in help_text
        assert "--debug" in help_text
        assert "--list-databases" in help_text
        assert "--database-info" in help_text

    def test_required_arguments_validation(self):
        """
        Test validation of required arguments.

        Verifies that the parser accepts various argument combinations
        since validation is context-dependent.
        """
        # Arrange
        parser = BioRemPPArgumentParser()

        # Act & Assert - No arguments should work (info commands allowed)
        args = parser.parse_args([])
        assert args is not None

        # Act & Assert - Only database argument should work
        args = parser.parse_args(["--database", "biorempp"])
        assert args.database == "biorempp"

        # Act & Assert - Only input argument should work
        args = parser.parse_args(["--input", "test.txt"])
        assert args.input == "test.txt"
