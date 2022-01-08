# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import sys

from demystify import analysis_from_csv

if sys.version_info[0] == 3:
    PY3 = True
else:
    PY3 = False


def test_denylist():
    """Enable denylist and test the results here."""
    assert False, "this test isn't implemented yet..."
