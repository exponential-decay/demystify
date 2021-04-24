# -*- coding: utf-8 -*-
import os.path
import sys

import unicodecsv

try:
    from urlparse import urlparse
except ImportError:
    import urllib.parse as urlparse

from PyDateHandler import PyDateHandler
from urlparse import urlparse


class genericCSVHandler:

    BOM = False
    BOMVAL = "\xEF\xBB\xBF"
    DICT_FORMATS = "FORMATS"

    def __init__(self, BOM=False):
        self.BOM = BOM

    def __getCSVheaders__(self, csvcolumnheaders):
        header_list = []
        for header in csvcolumnheaders:
            header_list.append(header)
        return header_list

    # returns list of rows, each row is a dictionary
    # header: value, pair.
    def csvaslist(self, csvfname):
        columncount = 0
        csvlist = None
        if os.path.isfile(csvfname):
            csvlist = []
            with open(csvfname, "rb") as csvfile:
                if self.BOM is True:
                    csvfile.seek(len(self.BOMVAL))
                csvreader = unicodecsv.reader(csvfile)
                for row in csvreader:
                    if csvreader.line_num == 1:  # not zero-based index
                        header_list = self.__getCSVheaders__(row)
                        columncount = len(header_list)
                    else:
                        csv_dict = {}
                        # for each column in header
                        # note: don't need ID data. Ignoring multiple ID.
                        for i in range(columncount):
                            csv_dict[header_list[i]] = row[i]
                        csvlist.append(csv_dict)
        return csvlist

    # bespoke function for DROID only - non-transferrable (probably)
    def csvaslist_DROID(self, csvfname):

        MULTIPLE = False
        FORMAT_COUNT = 13  # index of FORMAT_COUNT
        multi_fields = ["ID", "MIME_TYPE", "FORMAT_NAME", "FORMAT_VERSION"]
        multilist = []

        columncount = 0
        csvlist = None
        if os.path.isfile(csvfname):
            csvlist = []
            with open(csvfname, "rb") as csvfile:

                if self.BOM is True:
                    csvfile.seek(len(self.BOMVAL))

                # inspect line by reading it first.
                for lineno, line in enumerate(csvfile):

                    # check line for characters we can't parse...
                    line = self.checkline(line, lineno)

                    # create a dict to store row information
                    csv_dict = {}

                    # read each line into a unicode csv reader
                    csvreader = unicodecsv.reader(line.splitlines())

                    # first we need to retrieve the header information from the first line
                    if lineno == 0:
                        for row in csvreader:
                            header_list = self.__getCSVheaders__(row)
                            columncount = len(header_list)

                    for row in csvreader:

                        # for each column in header
                        # note: don't need ID data. Ignoring multiple ID.
                        for i in range(columncount):
                            if i == FORMAT_COUNT:
                                if row[i] != u"":
                                    count = int(row[i])
                                else:
                                    count = 0

                                csv_dict[header_list[i]] = count

                                # exception for multiple ids
                                if count > 1:
                                    MULTIPLE = True
                                    max_fields = len(multi_fields) * count

                                    # continue to put the remainder of the content into a dict
                                    format_list = row[FORMAT_COUNT + 1 :]
                                    format_list = format_list[:max_fields]

                                    while count > 0:
                                        mfields = multi_fields
                                        mdict = {}
                                        for i, t in enumerate(mfields):
                                            mdict[t] = '"' + format_list[i] + '"'
                                        format_list = format_list[len(mfields) :]
                                        multilist.append(mdict)
                                        count -= 1

                                    # break for loop after cycling through remainder
                                    # for loop controls regular number of columns (count)
                                    # while loop takes us the into an exception mechanism negating that
                                    break
                            else:
                                try:
                                    csv_dict[header_list[i]] = row[i]
                                except IndexError:
                                    sys.stderr.write(
                                        "Row len too short. Cannot write row: "
                                        + str(row)
                                        + "\n"
                                    )
                                    break

                        # continue with exception and add new dict to primary dict
                        if MULTIPLE == True:
                            csv_dict[self.DICT_FORMATS] = multilist
                            multilist = []

                        # add list and reset variables
                        csvlist.append(csv_dict)
                        MULTIPLE = False

        return csvlist

    def checkline(self, line, lineno):
        if "\x00" in line:
            sys.stderr.write(
                "CSV line "
                + str(lineno + 1)
                + " contains null byte '\\x00'. Replacing with an empty string.\n"
            )
            line = line.replace("\x00", "")
        return line


class droidCSVHandler:
    def __init__(self):
        # date handler class
        self.pydate = PyDateHandler()

    # returns droidlist type
    def readDROIDCSV(self, droidcsvfname, BOM=False):
        csvhandler = genericCSVHandler(BOM)
        self.DICT_FORMATS = csvhandler.DICT_FORMATS
        self.csv = csvhandler.csvaslist_DROID(droidcsvfname)
        return self.csv

    def getDirName(self, filepath):
        return os.path.dirname(filepath)

    def adddirname(self, droidlist):
        for row in droidlist:
            row[u"DIR_NAME"] = self.getDirName(row["FILE_PATH"])
        return droidlist

    def addurischeme(self, droidlist):
        for row in droidlist:
            row[u"URI_SCHEME"] = self.getURIScheme(row["URI"])
        return droidlist

    def getYear(self, datestring):
        return self.pydate.getYear(datestring)

    def addYear(self, droidlist):
        for row in droidlist:
            if row["LAST_MODIFIED"] is not "":
                row[u"YEAR"] = str(self.getYear(row["LAST_MODIFIED"])).decode("utf-8")
        return droidlist

    def removecontainercontents(self, droidlist):
        newlist = []  # naive remove causes loop to skip items
        for row in droidlist:
            uris = self.getURIScheme(row["URI"])
            if self.getURIScheme(row["URI"]) == "file":
                newlist.append(row)
        return newlist

    def removefolders(self, droidlist):
        # TODO: We can generate counts here and store in member vars
        newlist = []  # naive remove causes loop to skip items
        for i, row in enumerate(droidlist):
            if row["TYPE"] != "Folder":
                newlist.append(row)
        return newlist

    def retrievefolderlist(self, droidlist):
        newlist = []
        for row in droidlist:
            if row["TYPE"] == "Folder":
                newlist.append(row["FILE_PATH"])
        return newlist

    def retrievefoldernames(self, droidlist):
        newlist = []
        for row in droidlist:
            if row["TYPE"] == "Folder":
                newlist.append(row["NAME"])
        return newlist

    def getURIScheme(self, url):
        return urlparse(url).scheme
