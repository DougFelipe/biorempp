"""
BioRemPP Utilities Module.

This module serves as the comprehensive utility collection for BioRemPP,
providing essential infrastructure components for I/O operations, logging
systems, error handling, and user feedback management across the entire
analysis pipeline.

The utilities module implements foundational services that support all
BioRemPP operations with professional-grade logging, robust error handling,
user feedback systems, and efficient file management capabilities
designed for data processing workflows.

Key Components
--------------
I/O Utilities : module
    File management, path resolution, and data output operations.
    Provides timestamped file generation, project root detection,
    and DataFrame export functionality with standardized formats.

Logging Systems : module
    Comprehensive logging infrastructure with multiple configurations.
    Includes standard logging, silent logging for CLI applications,
    and environment-based configuration for different deployment scenarios.

Error Handling : module
    Error management with user-friendly message translation.
    Implements enhanced error handlers with contextual information,
    recovery suggestions, and consistent error presentation patterns.

User Feedback : module
    User interaction and progress indication systems.
    Features progress bars, status indicators, verbosity control,
    and feedback managers for complex multi-step operations.

Enhanced Systems : module
    Feedback and error handling components.
    Provides user experience improvements with visual
    progress tracking, contextual error reporting.

Architecture Overview
--------------------
The utilities module follows a layered architecture design:
1. Core Utilities: Basic I/O and file management operations
2. Logging Layer: Comprehensive logging and monitoring systems
3. Error Layer: Professional error handling and user guidance
4. Feedback Layer: User interaction and progress indication
5. Enhanced Layer: Advanced UX and sophisticated feedback systems

Integration Features
-------------------
- Consistent API design across all utility components
- Environment-aware configuration for different deployment contexts
- Professional logging with file-based technical details
- User-friendly error messages with actionable guidance
- Progress indication for long-running bioinformatics operations
- Modular design enabling selective component usage

Design Principles
----------------
- Clean Architecture: Clear separation of concerns and responsibilities
- Dependency Injection: Configurable components for enhanced testability
- UX: Modern CLI design patterns and user experience
- Error Resilience: Comprehensive error handling with graceful degradation
- Performance Focus: Efficient operations for large-scale data processing

Example Usage
------------
    from biorempp.utils import (
        save_dataframe_output,
        get_logger,
        EnhancedErrorHandler,
        EnhancedFeedbackManager
    )

    # File operations
    output_path = save_dataframe_output(df, "results", "analysis")

    # Logging setup
    logger = get_logger("my_module")
    logger.info("Processing started")

    # Error handling
    error_handler = EnhancedErrorHandler()

    # User feedback
    feedback = EnhancedFeedbackManager()
    feedback.show_progress("Processing data...")

Technical Features
-----------------
- Thread-safe logging operations for concurrent processing
- Environment variable configuration for deployment flexibility
- Timestamped file generation for organized output management
- Progress tracking for long-running computational operations
- Professional error presentation with technical and user-friendly modes
- Modular imports enabling selective component utilization
"""

from .enhanced_user_feedback import EnhancedFeedbackManager

# Error handling
from .error_handler import EnhancedErrorHandler, get_error_handler

# I/O utilities
from .io_utils import (
    generate_timestamped_filename,
    get_project_root,
    resolve_output_path,
    save_dataframe_output,
)

# Logging configuration
from .logging_config import configure_from_env, get_logger, setup_logging

# Silent logging for CLI
from .silent_logging import get_logger as get_silent_logger
from .silent_logging import setup_silent_logging, show_database_list, show_user_message

# User feedback systems
from .user_feedback import (
    ProgressIndicator,
    UserFeedbackManager,
    get_user_feedback,
    set_verbosity,
)

__all__ = [
    # I/O utilities
    "save_dataframe_output",
    "get_project_root",
    "resolve_output_path",
    "generate_timestamped_filename",
    # Logging
    "get_logger",
    "setup_logging",
    "configure_from_env",
    # Silent logging
    "setup_silent_logging",
    "get_silent_logger",
    "show_user_message",
    "show_database_list",
    # Error handling
    "EnhancedErrorHandler",
    "get_error_handler",
    # User feedback
    "ProgressIndicator",
    "UserFeedbackManager",
    "get_user_feedback",
    "set_verbosity",
    "EnhancedFeedbackManager",
]
