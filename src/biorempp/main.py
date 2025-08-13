"""
BioRemPP Main Entry Point.

Main module using Command Pattern architecture with
dependency injection and clean separation of concerns.
"""

from biorempp.app.application import BioRemPPApplication
from biorempp.utils.silent_logging import setup_silent_logging

# Initialize silent logging (no console spam)
setup_silent_logging()


def main():
    """
    Main entry point for the BioRemPP application.

    Creates and runs the BioRemPP application using dependency injection
    and centralized orchestration. All complexity has been moved to
    specialized components following SOLID principles.

    This function serves as the CLI entry point and does not return
    values to prevent unwanted output in command-line usage.
    """

    # Technical logging (to file only, no console spam)
    import logging

    logger = logging.getLogger("biorempp.main")
    logger.info("Starting BioRemPP main entry point")

    # Create and run the application
    app = BioRemPPApplication()
    app.run()  # Don't return result to avoid CLI output pollution


if __name__ == "__main__":
    main()
