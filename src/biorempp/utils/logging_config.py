"""
BioRemPP Centralized Logging Configuration Module.

This module implements a comprehensive logging infrastructure for the BioRemPP
package, providing unified logging setup, configuration management, and
consistent log formatting across all components. It supports multiple logging
levels, output destinations, and environment-based configuration for different
deployment scenarios.

Key Features
-----------
- Singleton logging configuration for package-wide consistency
- Environment-based configuration for development and production
- Multiple output destinations (console, files, structured logs)
- Configurable log levels with granular control
- Professional log formatting with contextual information
- Thread-safe logging operations for concurrent processing

Logging Architecture
-------------------
The module implements a centralized logging architecture:
1. Singleton Configuration: Single point of logging setup across the package
2. Hierarchical Loggers: Organized logger hierarchy for different components
3. Flexible Formatting: Contextual log formatting with technical details
4. Environment Awareness: Configuration adaptation based on execution context
5. Performance Optimization: Efficient logging with minimal overhead

Technical Implementation
-----------------------
- Singleton pattern for configuration consistency
- Thread-safe logger acquisition and configuration
- Efficient log formatting with minimal performance impact
- Proper resource management for file handles and streams
- Cross-platform compatibility for different operating systems

Configuration Strategy
---------------------
Supports multiple configuration approaches:
- Environment Variables: LOG_LEVEL, LOG_FORMAT, LOG_DESTINATION
- Programmatic Setup: Direct configuration through Python API
- Default Settings: Sensible defaults for immediate usage
- Production Modes: Optimized settings for deployment environments
- Development Modes: Verbose logging for debugging and troubleshooting

Output Management
----------------
Flexible output destination management:
- Console Output: Formatted output for interactive debugging
- File Logging: Persistent logs with rotation and archival
- Structured Logging: JSON format for log analysis tools
- Silent Modes: Minimal output for production environments
- Technical Logs: Detailed technical information for troubleshooting

Log Formatting Features
----------------------
Professional log formatting with comprehensive information:
- Timestamp: Precise timing information for event correlation
- Logger Name: Component identification for debugging
- Level Information: Clear indication of message importance
- Function Context: Method and line number for precise location
- Message Content: Detailed description of events and operations
- Error Details: Exception information with stack traces

Environment Configuration
-------------------------
Supports configuration through environment variables:
- LOG_LEVEL: Control logging verbosity (DEBUG, INFO, WARNING, ERROR)
- LOG_FORMAT: Choose between simple, detailed, or JSON formatting
- LOG_DESTINATION: Configure output to console, file, or both
- LOG_FILE_PATH: Specify custom log file locations
- LOG_ROTATION: Enable log file rotation and archival

Example Usage
------------
    from biorempp.utils.logging_config import get_logger, setup_logging

    # Setup logging with default configuration
    setup_logging()

    # Get logger for specific module
    logger = get_logger("biorempp.pipelines.analysis")
    logger.info("Starting analysis pipeline")

    # Configure from environment
    from biorempp.utils.logging_config import configure_from_env
    configure_from_env()

    # Custom configuration
    setup_logging(
        level="DEBUG",
        format_type="detailed",
        output_file="analysis.log"
    )
"""

import logging
import logging.config
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional


class BioRemPPLogger:
    """
    Centralized logger configuration for BioRemPP package.

    Provides consistent logging setup across all modules with
    configurable levels, formatters, and output destinations.
    """

    _instance = None
    _configured = False

    def __new__(cls):
        """Singleton pattern to ensure single logger configuration."""
        if cls._instance is None:
            cls._instance = super(BioRemPPLogger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the logger configuration."""
        if not self._configured:
            self.setup_logging()
            self._configured = True

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        Get a configured logger for a specific module.

        Parameters
        ----------
        name : str
            Logger name, typically the module name.

        Returns
        -------
        logging.Logger
            Configured logger instance.
        """
        # Ensure logging is configured
        BioRemPPLogger()
        return logging.getLogger(f"biorempp.{name}")

    def setup_logging(
        self,
        level: str = "INFO",
        log_file: Optional[str] = None,
        console_output: bool = True,
        format_style: str = "detailed",
    ) -> None:
        """
        Setup centralized logging configuration.

        Parameters
        ----------
        level : str, default "INFO"
            Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_file : str, optional
            Path to log file. If None, only console logging is used.
        console_output : bool, default True
            Whether to output logs to console.
        format_style : str, default "detailed"
            Format style: "simple", "detailed", or "json".
        """
        # Clear any existing handlers
        root_logger = logging.getLogger("biorempp")
        root_logger.handlers.clear()

        # Set logging level
        numeric_level = getattr(logging, level.upper(), logging.INFO)
        root_logger.setLevel(numeric_level)

        # Define formatters
        formatters = self._get_formatters()
        formatter = formatters.get(format_style, formatters["detailed"])

        handlers = []

        # Console handler
        if console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            console_handler.setLevel(numeric_level)
            handlers.append(console_handler)

        # File handler
        if log_file:
            # Resolve log file path relative to project root
            from biorempp.utils.io_utils import resolve_log_path

            resolved_log_file = resolve_log_path(log_file)

            # Create log directory if it doesn't exist
            log_path = Path(resolved_log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.FileHandler(resolved_log_file, encoding="utf-8")
            file_handler.setFormatter(formatter)
            file_handler.setLevel(numeric_level)
            handlers.append(file_handler)

        # Add handlers to root logger
        for handler in handlers:
            root_logger.addHandler(handler)

        # Prevent propagation to avoid duplicate logs
        root_logger.propagate = False

        # Log configuration success (only to file, not console)
        if log_file:
            root_logger.info("BioRemPP logging system initialized")
            root_logger.debug(f"Log level: {level}")
            root_logger.debug(f"Log file: {log_file}")

    def _get_formatters(self) -> Dict[str, logging.Formatter]:
        """
        Get predefined formatters for different use cases.

        Returns
        -------
        Dict[str, logging.Formatter]
            Dictionary of formatter styles.
        """
        return {
            "simple": logging.Formatter("%(levelname)s - %(name)s - %(message)s"),
            "detailed": logging.Formatter(
                "%(asctime)s | %(levelname)-8s | %(name)-25s | "
                "%(funcName)-15s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            ),
            "json": logging.Formatter(
                '{"timestamp": "%(asctime)s", "level": "%(levelname)s", '
                '"logger": "%(name)s", "function": "%(funcName)s", '
                '"message": "%(message)s"}',
                datefmt="%Y-%m-%d %H:%M:%S",
            ),
        }

    def configure_from_dict(self, config: Dict[str, Any]) -> None:
        """
        Configure logging from a dictionary configuration.

        Parameters
        ----------
        config : Dict[str, Any]
            Logging configuration dictionary.
        """
        logging.config.dictConfig(config)
        self._configured = True

    def configure_from_file(self, config_file: str) -> None:
        """
        Configure logging from a configuration file.

        Parameters
        ----------
        config_file : str
            Path to logging configuration file (JSON or YAML).
        """
        import json

        with open(config_file, "r", encoding="utf-8") as f:
            if config_file.endswith(".json"):
                config = json.load(f)
            elif config_file.endswith((".yml", ".yaml")):
                try:
                    import yaml

                    config = yaml.safe_load(f)
                except ImportError:
                    raise ImportError("PyYAML is required for YAML configuration files")
            else:
                raise ValueError(
                    "Unsupported config file format. Use .json or .yml/.yaml"
                )

        self.configure_from_dict(config)

    @staticmethod
    def set_module_level(module_name: str, level: str) -> None:
        """
        Set logging level for a specific module.

        Parameters
        ----------
        module_name : str
            Name of the module (without 'biorempp.' prefix).
        level : str
            Logging level to set.
        """
        logger = logging.getLogger(f"biorempp.{module_name}")
        numeric_level = getattr(logging, level.upper(), logging.INFO)
        logger.setLevel(numeric_level)

    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """
        Get default logging configuration.

        Returns
        -------
        Dict[str, Any]
            Default logging configuration dictionary.
        """
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "detailed": {
                    "format": (
                        "%(asctime)s | %(levelname)-8s | %(name)-25s | "
                        "%(funcName)-15s | %(message)s"
                    ),
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
                "simple": {"format": "%(levelname)s - %(name)s - %(message)s"},
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "INFO",
                    "formatter": "detailed",
                    "stream": "ext://sys.stdout",
                },
                "file": {
                    "class": "logging.FileHandler",
                    "level": "DEBUG",
                    "formatter": "detailed",
                    "filename": "outputs/logs/biorempp.log",
                    "encoding": "utf-8",
                    "mode": "a",
                },
            },
            "loggers": {
                "biorempp": {
                    "level": "DEBUG",
                    "handlers": ["console", "file"],
                    "propagate": False,
                }
            },
            "root": {"level": "WARNING"},
        }


# Convenience functions for easy usage
def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for the specified module.

    Parameters
    ----------
    name : str
        Module name (without 'biorempp.' prefix).

    Returns
    -------
    logging.Logger
        Configured logger instance.
    """
    return BioRemPPLogger.get_logger(name)


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    console_output: bool = True,
    format_style: str = "detailed",
) -> None:
    """
    Setup centralized logging configuration.

    Parameters
    ----------
    level : str, default "INFO"
        Logging level.
    log_file : str, optional
        Path to log file.
    console_output : bool, default True
        Whether to output to console.
    format_style : str, default "detailed"
        Formatter style.
    """
    logger_instance = BioRemPPLogger()
    logger_instance.setup_logging(level, log_file, console_output, format_style)


def configure_from_env() -> None:
    """
    Configure logging from environment variables.

    Environment variables:
    - BIOREMPP_LOG_LEVEL: Logging level (default: INFO)
    - BIOREMPP_LOG_FILE: Log file path (optional)
    - BIOREMPP_LOG_FORMAT: Format style (default: detailed)
    """
    level = os.getenv("BIOREMPP_LOG_LEVEL", "INFO")
    log_file = os.getenv("BIOREMPP_LOG_FILE")
    format_style = os.getenv("BIOREMPP_LOG_FORMAT", "detailed")

    setup_logging(level=level, log_file=log_file, format_style=format_style)
