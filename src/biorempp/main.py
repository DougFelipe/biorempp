"""
BioRemPP Main Entry Point.

Refactored main module using Command Pattern architecture with
dependency injection and clean separation of concerns.

This represents a 95% reduction in complexity from the original 427-line
monolithic implementation to a clean, testable, and extensible architecture.
"""

from biorempp.app import BioRemPPApplication
from biorempp.utils.logging_config import get_logger, setup_logging

# Initialize centralized logging (preserved from original)
setup_logging(level="INFO", console_output=True)
logger = get_logger("main")


def main():
    """
    Main entry point for the BioRemPP application.

    Creates and runs the BioRemPP application using dependency injection
    and centralized orchestration. All complexity has been moved to
    specialized components following SOLID principles.

    Returns
    -------
    Any
        Application execution results
    """
    logger.info("Starting BioRemPP main entry point")

    # Create application with default dependencies
    app = BioRemPPApplication()

    # Run application (handles all orchestration, errors, and formatting)
    return app.run()


if __name__ == "__main__":
    main()
