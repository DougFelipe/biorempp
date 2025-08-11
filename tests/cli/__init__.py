"""
Tests for the BioRemPP CLI module.

This module contains comprehensive tests for the entire command line interface
of BioRemPP, including argument parsing, output formatting, and integration
between CLI components.

Test Structure:
    - test_argument_parser.py: Tests for argument parsing and validation
    - test_output_formatter.py: Tests for output formatting and presentation

Test Coverage:
    - Command line argument parsing
    - Input parameter validation
    - Mutually exclusive argument groups
    - Single database output formatting
    - Multiple database output formatting
    - Error handling and feedback messages
    - CLI component integration

Included Test Cases:
    - Success scenarios (happy path)
    - Required argument validation
    - Mutually exclusive argument conflicts
    - Different verbosity levels
    - Individual vs all database selection
    - Information and discovery commands
    - Single and multiple result formatting
    - Error handling and interruptions
    - Performance metrics calculation

Testing Methodology:
    - Extensive use of mocks for component isolation
    - Parametrized tests for multiple scenarios
    - Reusable fixtures for test data
    - PEP 8 and flake8 compliance verification
    - English documentation as standardized

Dependencies:
    - pytest: Main testing framework
    - unittest.mock: Mocking external components
    - argparse: For argument parsing tests
    - io.StringIO: For console output capture

Author: BioRemPP Development Team
"""
