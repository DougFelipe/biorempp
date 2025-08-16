import sys

"""
    biorempp package initializer.

This module handles the initialization of the biorempp package, including
version detection and silent logging configuration.

Version Handling
----------------
Determines the package version using `importlib.metadata` (Python >= 3.8) or
`importlib_metadata` (Python < 3.8). If the package version cannot be determined,
the version is set to "unknown".

Silent Logging
--------------
Initializes a silent logging system to suppress unnecessary console output by calling
`setup_silent_logging()` from `biorempp.utils.silent_logging`.

Attributes
----------
__version__ : str
    The version of the biorempp package, or "unknown" if not found.

Notes
-----
- The version detection logic is compatible with both modern and legacy Python versions.
- The silent logging setup is performed automatically upon package import.
"""

if sys.version_info[:2] >= (3, 8):
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover

else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

finally:
    del version, PackageNotFoundError

# Initialize silent logging system (no console spam)
from biorempp.utils.silent_logging import setup_silent_logging

# Set up silent logging configuration
setup_silent_logging()
