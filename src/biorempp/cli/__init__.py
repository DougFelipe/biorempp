"""
BioRemPP Command Line Interface Package

This package provides comprehensive command-line interface components for
BioRemPP, implementing a clean separation between argument processing and
output presentation. The CLI package follows modern design principles to
deliver an intuitive and user-friendly experience.

CLI Architecture:
    The package implements a modular approach with specialized components
    for different aspects of command-line interaction, promoting maintainability
    and extensibility while ensuring consistent user experience across all
    operations.

Core Components:
    - BioRemPPArgumentParser: Argument parsing and validation engine
    - OutputFormatter: Result presentation and user feedback system

Design Principles:
    - Single Responsibility: Each component handles one aspect of CLI interaction
    - Separation of Concerns: Argument parsing separated from output formatting
    - User Experience Focus: Clean, informative, and professional interface
    - Extensibility: Easy addition of new argument types and output formats

Argument Processing:
    The argument parser provides structured handling of input files, database
    selection, output configuration, and system information commands with
    comprehensive validation and error handling.

Output Formatting:
    The output formatter delivers, informative displays with
    progress indicators, result summaries, and error reporting following
    modern CLI design patterns and structured layouts.

Integration Points:
    - Command execution pipeline integration
    - Error handling and user feedback systems
    - Logging and debugging infrastructure
    - Result processing and file management
"""

from .argument_parser import BioRemPPArgumentParser
from .output_formatter import OutputFormatter

__all__ = [
    "BioRemPPArgumentParser",
    "OutputFormatter",
]
