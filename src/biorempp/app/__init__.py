"""
BioRemPP Application Module.

This module serves as the main application package for BioRemPP,
providing the central orchestration and factory components for
the complete bioremediation analysis system.

The application module implements clean architecture principles
with dependency injection, command pattern implementation,
and comprehensive error handling for professional bioinformatics
data processing workflows.

Key Components
--------------
BioRemPPApplication : class
    Main application orchestrator that coordinates all system components
    using dependency injection and centralized error handling.
    Manages the complete execution flow from argument parsing to result
    presentation with comprehensive exception handling.

CommandFactory : class
    Factory pattern implementation for creating appropriate command
    instances based on parsed CLI arguments. Provides intelligent
    command routing and validation for info, merger, and processing
    operations.

Architecture Overview
--------------------
The application follows a layered architecture:
1. Application Layer: Main orchestrator and entry point
2. Factory Layer: Command creation and routing logic
3. Command Layer: Individual command implementations
4. Service Layer: Processing pipelines and business logic
5. Data Layer: Input processing and database operations

Integration Features
-------------------
- Dependency injection for enhanced testability
- Centralized error handling with user-friendly messages
- Professional logging system with file-based technical logs
- Command pattern implementation for operation management
- Clean separation of concerns across all components

Example Usage
------------
    from biorempp.app import BioRemPPApplication, CommandFactory

    # Create and run application
    app = BioRemPPApplication()
    result = app.run([
        '--all-databases',
        '--input', 'samples.txt',
        '--output-dir', 'results'
    ])

    # Custom factory usage
    factory = CommandFactory()
    command = factory.create_command(parsed_args)
    command_type = factory.get_command_type(parsed_args)

Technical Features
-----------------
- Clean architecture with dependency injection
- Command pattern for operation management
- Factory pattern for command creation
- Comprehensive error handling and logging
- Professional user feedback and progress indication
- Support for both interactive and batch execution modes

Design Patterns
--------------
- Application Orchestrator: Coordinates all components
- Factory Pattern: Command creation and routing
- Command Pattern: Operation encapsulation and execution
- Dependency Injection: Enhanced testability and modularity
"""

from biorempp.app.application import BioRemPPApplication
from biorempp.app.command_factory import CommandFactory

__all__ = ["BioRemPPApplication", "CommandFactory"]
