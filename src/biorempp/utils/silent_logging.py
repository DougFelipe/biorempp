"""Silent logging configuration for CLI usage."""

import logging
from datetime import datetime
from pathlib import Path


def setup_silent_logging():
    """Setup logging that completely silences console output."""

    # Create logs directory
    log_dir = Path("outputs/logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    # Setup file logging only
    log_file = log_dir / f"biorempp_{datetime.now().strftime('%Y%m%d')}.log"

    # Configure root logger to only write to file
    root_logger = logging.getLogger()
    root_logger.handlers.clear()  # Remove all existing handlers
    root_logger.setLevel(logging.DEBUG)

    # File handler for technical logs
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)-25s | %(funcName)-15s | %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)

    # Create a null handler to suppress console output
    # (Not used but kept for reference)

    # Apply silent logging to ALL biorempp related modules
    # This is more aggressive - captures any logger starting with "biorempp"
    class BioRemPPLoggerFilter:
        """Custom filter to redirect all biorempp logs to file only."""

        def filter(self, record):
            # If it's a biorempp module, send to file only (return False for console)
            if record.name.startswith("biorempp"):
                return False
            return True

    # Apply filter to stderr to prevent console logging
    console_filter = BioRemPPLoggerFilter()

    # Override any existing console handlers
    for handler in logging.root.handlers[:]:
        if isinstance(handler, logging.StreamHandler):
            handler.addFilter(console_filter)

    # Also set up specific silencing for known problematic modules
    problem_modules = [
        "biorempp",
        "biorempp.main",
        "biorempp.app",
        "biorempp.pipelines",
        "biorempp.pipelines.input_processing",
        "biorempp.input_processing",
        "biorempp.input_processing.input_loader",
        "biorempp.input_processing.input_validator",
        "biorempp.input_processing.biorempp_merge_processing",
        "biorempp.input_processing.hadeg_merge_processing",
        "biorempp.input_processing.kegg_merge_processing",
        "biorempp.input_processing.toxcsm_merge_processing",
        "biorempp.utils",
        "biorempp.utils.io_utils",
        "biorempp.commands",
        "biorempp.cli",
    ]

    for module_name in problem_modules:
        logger = logging.getLogger(module_name)
        logger.propagate = False  # Don't propagate to root
        logger.handlers.clear()  # Remove all handlers
        logger.addHandler(file_handler)  # Only file handler
        logger.setLevel(logging.DEBUG)

    return root_logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger that only writes to file, not console."""
    logger = logging.getLogger(f"biorempp.{name}")
    logger.propagate = False  # Don't send to root logger

    # Ensure it has the file handler
    log_dir = Path("outputs/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"biorempp_{datetime.now().strftime('%Y%m%d')}.log"

    # Add file handler if not exists
    if not logger.handlers:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_formatter = logging.Formatter(
            (
                "%(asctime)s | %(levelname)-8s | %(name)-25s | "
                "%(funcName)-15s | %(message)s"
            )
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)

    return logger


def show_user_message(message: str, message_type: str = "info"):
    """Show clean messages to user without logging overhead."""

    icons = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌",
        "processing": "⚙️",
    }

    icon = icons.get(message_type, "ℹ️")
    print(f"{icon} {message}")


def show_database_list():
    """Show clean database list."""
    print("\n🧬 BioRemPP - Available Databases")
    print("═" * 67)
    print("📊 BIOREMPP     │ 6,623 records    │ Enzyme-compound interactions")
    print("📊 HADEG        │ 1,168 records    │ Human metabolism pathways")
    print("📊 KEGG         │ 871 records      │ Degradation pathways")
    print("📊 TOXCSM       │ 323 records      │ Toxicity predictions")
    print("\n💡 Usage: biorempp --input your_data.txt --database biorempp")
    print("💡 Or use all: biorempp --input your_data.txt --all-databases\n")
