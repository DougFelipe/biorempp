"""
Utilities module for biorempp package.

This module contains utility functions for I/O operations, logging,
error handling, and user feedback.
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
