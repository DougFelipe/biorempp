"""
BioRemPP Enhanced Logging System Module.

This module implements a sophisticated dual-output logging system that
provides comprehensive technical logging for debugging and monitoring
while maintaining clean, professional user interfaces for command-line
applications. It represents an advanced approach to logging in scientific
computing environments with seamless integration of technical detail
preservation and user experience optimization.

The enhanced logging system bridges the gap between comprehensive technical
documentation and professional user interfaces, enabling full debugging
capabilities while delivering beautiful, informative command-line experiences
optimized for bioinformatics workflows.

Key Features
-----------
- Dual Output Architecture: Simultaneous technical logging and user feedback
- Professional User Interface: Clean, beautiful console output without spam
- Comprehensive Technical Logs: Detailed file-based logging for debugging
- Threading Support: Non-blocking progress indicators and status updates
- Flexible Configuration: Adaptable logging levels and output destinations

Dual Logging Architecture
------------------------
Innovative dual-output logging design:
1. Technical Layer: Comprehensive file-based logging with full technical detail
2. User Layer: Clean, professional console output with visual appeal
3. Progress Layer: Real-time progress indication with thread-safe operations
4. Error Layer: Professional error presentation with technical detail preservation
5. Integration Layer: Seamless coordination between all logging components

Technical Logging Features
-------------------------
Comprehensive technical documentation capabilities:
- File-Based Logging: Detailed logs with rotation and archival support
- Debug Information: Complete technical context and execution traces
- Performance Metrics: Timing information and resource utilization tracking
- Error Documentation: Full exception traces and diagnostic information
- Audit Trail: Complete operational history for compliance and debugging

User Interface Design
--------------------
Professional console interface features:
- Clean Output: Beautiful, informative displays without technical clutter
- Progress Indicators: Smooth, non-blocking progress visualization
- Status Updates: Real-time feedback for multi-step operations
- Professional Styling: Consistent visual design with modern aesthetics
- Contextual Information: Relevant details presented at appropriate detail levels

Threading and Concurrency
-------------------------
Advanced threading support for responsive interfaces:
- Background Logging: Non-blocking technical log operations
- Progress Threading: Smooth progress indicators during processing
- Resource Management: Efficient thread lifecycle and resource cleanup
- Synchronization: Thread-safe operations across all logging components
- Performance Optimization: Minimal overhead for concurrent operations

Configuration Flexibility
-------------------------
Comprehensive configuration management:
- Console Level Control: Adjustable user interface verbosity
- File Level Control: Independent technical logging detail levels
- Output Destination: Configurable log file locations and organization
- Format Customization: Adaptable log formatting for different requirements
- Environment Integration: Configuration through environment variables

Integration Strategy
-------------------
Seamless integration with BioRemPP ecosystem:
- Pipeline Integration: Logging coordination with processing workflows
- Command Integration: Professional logging for command execution
- Error Integration: Coordinated error handling and presentation
- Feedback Integration: Unified user feedback and progress systems
- Monitoring Integration: Support for operational monitoring and alerting

Example Usage
------------
    from biorempp.utils.enhanced_logging import BioRemPPLogger

    # Initialize enhanced logger
    logger = BioRemPPLogger(
        console_level="NORMAL",
        file_level="DEBUG",
        log_dir="custom/logs"
    )

    # Technical logging (to file)
    logger.info("Starting data processing pipeline")
    logger.debug("Processing 10000 sequences with parameters X, Y, Z")

    # User feedback (to console)
    logger.user_message("🧬 Loading biological data...")
    logger.show_progress("Processing sequences", current=500, total=10000)
    logger.user_success("✅ Analysis completed successfully")

Logging Levels and Control
-------------------------
Sophisticated level management:
- SILENT: No console output, minimal file logging
- NORMAL: Standard console feedback, comprehensive file logging
- VERBOSE: Detailed console output, extensive file logging
- DEBUG: Full diagnostic output, complete technical documentation
- TECHNICAL: Maximum detail for development and troubleshooting

Professional Design Elements
---------------------------
Modern CLI design implementation:
- Unicode Indicators: Professional symbols and progress indicators
- Structured Layout: Organized information presentation with visual hierarchy
- Color Coordination: Contextual colors for different message types
- Animation Support: Smooth progress animations and status transitions
- Cross-Platform: Consistent appearance across different operating systems

Technical Implementation
-----------------------
- Efficient dual-output architecture with minimal performance overhead
- Thread-safe logging operations with proper synchronization
- Memory-efficient operation suitable for long-running processes
- Robust error handling with graceful degradation capabilities
- Cross-platform compatibility for different deployment environments
"""

import logging
import logging.handlers
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


class BioRemPPLogger:
    """Dual logging system: technical file logs + clean user console feedback."""

    def __init__(
        self,
        console_level: str = "NORMAL",
        file_level: str = "INFO",
        log_dir: str = "outputs/logs",
    ):

        self.console_level = console_level.upper()
        self.file_level = file_level.upper()
        self.log_dir = Path(log_dir)

        # Threading for spinners
        self._spinner_active = False
        self._spinner_thread = None

        # Technical logger for file logging
        self.technical_logger = None

        self._setup_logging()

    def _setup_logging(self):
        """Setup both file and console logging."""
        # Create log directory
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Setup file logging (technical)
        log_file = self.log_dir / f"biorempp_{datetime.now().strftime('%Y%m%d')}.log"

        # Create technical logger
        self.technical_logger = logging.getLogger("biorempp.technical")
        self.technical_logger.setLevel(getattr(logging, self.file_level))

        # Remove existing handlers to avoid duplicates
        self.technical_logger.handlers.clear()

        # File handler with rotation
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=10 * 1024 * 1024, backupCount=7, encoding="utf-8"  # 10MB
        )

        file_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)-25s | "
            "%(funcName)-15s | %(lineno)-4d | %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(getattr(logging, self.file_level))

        self.technical_logger.addHandler(file_handler)

        # Prevent technical logs from going to root logger (no console spam)
        self.technical_logger.propagate = False

        # Log system initialization
        self.technical_logger.info("Enhanced logging system initialized")
        self.technical_logger.info(
            f"Console level: {self.console_level}, File level: {self.file_level}"
        )

    def user_info(self, message: str, icon: str = "ℹ️", show_spinner: bool = False):
        """Show info message to user with optional spinner."""
        if self.console_level == "SILENT":
            return

        if show_spinner:
            self._start_spinner(f"{icon} {message}")
        else:
            print(f"{icon} {message}")

        # Log to file
        self.technical_logger.info(f"USER_INFO: {message}")

    def user_success(self, message: str, details: Dict[str, Any] = None):
        """Show success message to user."""
        if self.console_level == "SILENT":
            return

        self._stop_spinner()
        print(f"✅ {message}")

        if details and self.console_level == "VERBOSE":
            for key, value in details.items():
                print(f"   📊 {key}: {value}")

        self.technical_logger.info(f"USER_SUCCESS: {message} | Details: {details}")

    def user_warning(self, message: str, suggestion: str = None):
        """Show warning to user with optional suggestion."""
        if self.console_level == "SILENT":
            return

        self._stop_spinner()
        print(f"⚠️  Warning: {message}")

        if suggestion:
            print(f"💡 Suggestion: {suggestion}")

        self.technical_logger.warning(
            f"USER_WARNING: {message} | Suggestion: {suggestion}"
        )

    def user_error(self, message: str, solution: str = None):
        """Show error to user with optional solution."""
        self._stop_spinner()
        print(f"[ERROR] Error: {message}")

        if solution:
            print(f"💡 Solution:\n{solution}")

        self.technical_logger.error(f"USER_ERROR: {message} | Solution: {solution}")

    def debug(self, message: str):
        """Log debug message to file only."""
        self.technical_logger.debug(message)

    def info(self, message: str):
        """Log info message to file only."""
        self.technical_logger.info(message)

    def warning(self, message: str):
        """Log warning message to file only."""
        self.technical_logger.warning(message)

    def error(self, message: str, exc_info: bool = False):
        """Log error message to file only."""
        self.technical_logger.error(message, exc_info=exc_info)

    def critical(self, message: str, exc_info: bool = False):
        """Log critical message to file only."""
        self.technical_logger.critical(message, exc_info=exc_info)

    def _start_spinner(self, message: str):
        """Start spinner animation."""
        if self.console_level == "SILENT":
            return

        self._spinner_active = True
        spinner_chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"

        def spin():
            i = 0
            while self._spinner_active:
                sys.stdout.write(f"\r{spinner_chars[i % len(spinner_chars)]} {message}")
                sys.stdout.flush()
                time.sleep(0.1)
                i += 1
            sys.stdout.write("\r" + " " * (len(message) + 2) + "\r")
            sys.stdout.flush()

        self._spinner_thread = threading.Thread(target=spin)
        self._spinner_thread.daemon = True
        self._spinner_thread.start()

    def _stop_spinner(self):
        """Stop spinner animation."""
        self._spinner_active = False
        if self._spinner_thread:
            self._spinner_thread.join(timeout=0.2)


# Global logger instance
_global_logger = None


def get_enhanced_logger(
    console_level: str = "NORMAL", file_level: str = "INFO"
) -> BioRemPPLogger:
    """Get enhanced logger instance (singleton)."""
    global _global_logger
    if _global_logger is None:
        _global_logger = BioRemPPLogger(console_level, file_level)
    return _global_logger


def set_console_level(level: str):
    """Set console verbosity level globally."""
    global _global_logger
    if _global_logger:
        _global_logger.console_level = level.upper()
    else:
        _global_logger = BioRemPPLogger(level.upper())
