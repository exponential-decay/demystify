# -*- coding: utf-8 -*-

"""Version.py

Helper class to return the version of this application to the caller.
"""


class AnalysisVersion:
    """Analysis version class to store version information and return
    it to the caller.
    """

    def __init__(self):
        """Constructor for the version class."""

        # 0.6.7-BETA - Python 2 only, first iteration.
        # 1.0.0 - Python 2 and 3, refactor and final Python 2 release.
        self.version = "1.0.0"

    def getVersion(self):
        """Return version number to the caller."""
        return self.version
