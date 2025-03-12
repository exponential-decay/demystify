# -*- coding: utf-8 -*-

"""Version.py

Helper class to return the version of this application to the caller.
"""

from importlib.metadata import PackageNotFoundError, version


def get_version():
    """Returns a version string to the caller."""
    semver = "0.0.0"
    __version__ = f"{semver}-dev"
    try:
        __version__ = version("demystify_digipres")
    except PackageNotFoundError:
        # package is not installed
        pass
    return __version__
