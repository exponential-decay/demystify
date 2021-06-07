# -*- coding: utf-8 -*-

from __future__ import absolute_import

import re


class RegexFnameAnalysis:
    def __init__(self):
        # detect multiple contiguous spaces in filenames
        self.multiplespaceregex = re.compile(r"(\s{2,100})")

    # detect multiple contiguous spaces in filenames
    def detectMultipleSpaces(self, fname):
        doublespaces = False
        if self.multiplespaceregex.search(fname) is not None:
            doublespaces = True
        return doublespaces
