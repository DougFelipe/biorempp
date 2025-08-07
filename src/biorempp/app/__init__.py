"""
BioRemPP Application Package.

This package contains the main application orchestrator and factory
components for the command pattern architecture.
"""

from .application import BioRemPPApplication
from .command_factory import CommandFactory

__all__ = [
    "BioRemPPApplication",
    "CommandFactory",
]
