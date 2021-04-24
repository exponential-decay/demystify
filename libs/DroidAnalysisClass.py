# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import argparse
import csv
import sqlite3
import sys
from collections import Counter

from lxml import etree, html

from libs import DroidAnalysisResultsClass, RegexFnameAnalysis
from libs.AnalysisQueriesClass import AnalysisQueries
from libs.BlacklistQueriesClass import BlacklistQueries
from libs.RoguesQueriesClass import RogueQueries

from libs import MsoftFnameAnalysis

try:
    from urlparse import urlparse
except ImportError:
    import urllib.parse as urlparse

from collections import Counter

from lxml import etree, html

from libs.HandleBlacklistClass import HandleBlacklist
from libs.version import AnalysisVersion


class DROIDAnalysis:
    def __version__(self):
        v = AnalysisVersion()
        self.analysisresults.__version_no__ = v.getVersion()
        return self.analysisresults.__version_no__

    # we need this value because we extract basedirs for all folders, including
    # the root directory of the extract, creating one additional entry
    # TODO: consider handling better...
    NONROOTBASEDIR = 1

    # somenamespaceconsts
    NS_CONST_TITLE = "namespace title"
    NS_CONST_DETAILS = "namespace details"
    NS_CONST_XML_COUNT = "xml method count"
    NS_CONST_TEXT_COUNT = "text method count"
    NS_CONST_FILENAME_COUNT = "filename method count"
    NS_CONST_EXTENSION_COUNT = "extension method count"
    NS_CONST_BINARY_COUNT = "binary method count"
    NS_CONST_MULTIPLE_IDS = "multiple ids"

    # variables we need internally:
    extensionIDonly = None
    binaryIDs = None
    noids = None
    xmlIDs = None
    textIDs = None
    filenameIDs = None
    namespacedata = None
    priority_ns_id = None

    # namespaceids
    pronom_ns_id = None
    freedesktop_ns_id = None
    tika_ns_id = None

    ID_TIKA = "TIKA"
    ID_PRONOM = "PRONOM"
    ID_FREEDESKTOP = "FREE"
    ID_NONE = "NONE"

    def __init__(self, dbfilename=None, config=False, blacklist=False):
        self.analysisresults = DroidAnalysisResultsClass.DROIDAnalysisResults()
        if dbfilename != None:
            self.openDROIDDB(dbfilename)
            self.query = AnalysisQueries()
            self.analysisresults.tooltype = self.__querydb__(
                self.query.SELECT_TOOL, True
            )[0]
            self.analysisresults.namespacecount = self.__querydb__(
                self.query.SELECT_COUNT_NAMESPACES, True
            )[0]
            self.namespacedata = self.__querydb__(self.query.SELECT_NS_DATA)
            nsdata = self.namespacedata
            if self.analysisresults.namespacecount > 1:
                for ns_deets in nsdata:
                    # to prioritize PRONOM look for below strings, and avoid limited to DROID signature files
                    #'DROID_SignatureFile_V84.xml; container-signature-20160121.xml; built without reports; limited to ids: x-fmt/111'
                    sig_deets = ns_deets[2]
                    if "DROID_" in sig_deets and "limited to" not in sig_deets:
                        self.pronom_ns_id = ns_deets[0]
                    elif "tika" in sig_deets:
                        self.tika_ns_id = ns_deets[0]
                    elif "freedesktop" in sig_deets:
                        self.freedesktop_ns_id = ns_deets[0]
                self.__get_ns_priority__(self.__readconfig__(config))
            self.blacklist = blacklist

    def __get_ns_priority__(self, config):
        if config == False:
            self.priority_ns_id = self.pronom_ns_id
        else:
            if config == self.ID_PRONOM:
                self.priority_ns_id = self.pronom_ns_id
            if config == self.ID_FREEDESKTOP:
                self.priority_ns_id = self.freedesktop_ns_id
            if config == self.ID_TIKA:
                self.priority_ns_id = self.tika_ns_id
            if config == self.ID_NONE:
                self.priority_ns_id = None

    def __readconfig__(self, config):
        ns_out = None
        if config != None:
            if config.has_section("priority"):
                if (
                    config.has_option("priority", "pronom") is True
                    and config.get("priority", "pronom").lower() == "true"
                ):
                    ns_out = self.ID_PRONOM
                elif (
                    config.has_option("priority", "freedesktop")
                    and config.get("priority", "freedesktop").lower() == "true"
                ):
                    ns_out = self.ID_FREEDESKTOP
                elif (
                    config.has_option("priority", "tika")
                    and config.get("priority", "tika").lower() == "true"
                ):
                    ns_out = self.ID_TIKA
                elif (
                    config.has_option("priority", "none")
                    and config.get("priority", "none").lower() == "true"
                ):
                    ns_out = self.ID_NONE
                else:
                    ns_out = None
                if ns_out == "":
                    ns_out = None

        return ns_out

    ## DB self.cursor
    cursor = None

    def __querydb__(self, query, fetchone=False, numberquery=False, tolist=False):
        self.cursor.execute(query.replace("  ", ""))
        if fetchone is True and numberquery is False:
            return self.cursor.fetchone()
        if fetchone is True and numberquery is True:
            return self.cursor.fetchone()[0]
        else:
            if tolist is False:
                return self.cursor.fetchall()
            else:
                list = []
                for result in self.cursor.fetchall():
                    list.append(result[0])
                return list

    ###
    # List queries

    def listDuplicateFilesFromHASH(self):
        result = self.__querydb__(AnalysisQueries.SELECT_COUNT_DUPLICATE_CHECKSUMS)

        duplicate_sum = {}
        duplicatelist = []

        self.analysisresults.totalHASHduplicates = 0
        for r in result:
            self.analysisresults.totalHASHduplicates = (
                self.analysisresults.totalHASHduplicates + int(r[1])
            )

        roguepaths = []

        # result list([HASH, COUNT])
        for r in result:
            example = self.__querydb__(self.query.list_duplicate_paths(r[0]))
            pathlist = []
            for e in example:
                pathlist.append(e[0])
                self.analysisresults.duplicatespathlist.append(
                    e[0]
                )  # create path only listing

            roguepaths = roguepaths + pathlist

            duplicate_sum["checksum"] = str(r[0])
            duplicate_sum["count"] = str(r[1])
            duplicate_sum["examples"] = pathlist
            duplicatelist.append(duplicate_sum)
            duplicate_sum = {}

        self.analysisresults.duplicateHASHlisting = duplicatelist
        return roguepaths

    def listzerobytefiles(self):
        self.analysisresults.zerobytecount = self.__querydb__(
            AnalysisQueries.SELECT_COUNT_ZERO_BYTE_FILES, True, True
        )
        if self.analysisresults.zerobytecount > 0:
            self.analysisresults.zerobytelist = self.__querydb__(
                AnalysisQueries.SELECT_ZERO_BYTE_FILEPATHS, False, False, True
            )
        else:
            self.analysisresults.zerobytelist = None
        return self.analysisresults.zerobytecount

    def calculatePercent(self, total, subset):
        if total > 0:
            percentage = (subset / total) * 100
            return "%.1f" % round(percentage, 1)

    def msoftfnameanalysis(self):
        namelist = self.__querydb__(AnalysisQueries.SELECT_FILENAMES)
        dirlist = self.__querydb__(AnalysisQueries.SELECT_DIRNAMES)

        charcheck = MsoftFnameAnalysis.MsoftFnameAnalysis()

        self.rogue_names = []
        self.rogue_dirs = []

        namereport = []
        for d in namelist:
            namestring = d[0]
            checkedname = charcheck.complete_file_name_analysis(namestring).encode("utf-8")
            if checkedname != "":
                namereport.append(checkedname)
                self.rogue_names.append(d[0])

        # TODO: Handle recursive paths better to avoid duplication
        dirreport = []
        for d in dirlist:
            dirstring = d[0]
            checkedname = charcheck.complete_file_name_analysis(dirstring, True).encode(
                "utf-8"
            )
            if checkedname != "":
                dirreport.append(checkedname)
                self.rogue_dirs.append(d[0])

        self.analysisresults.badFileNames = namereport
        self.analysisresults.badDirNames = dirreport

    def multiplecount(self, nscount):
        return self.__querydb__(self.query.count_multiple_ids(nscount), True, True)

    def multiple_id_paths(self, nscount, paths=True):
        return self.__querydb__(
            self.query.count_multiple_ids(nscount, paths), False, False, True
        )

    def __getsplit__(self, vals):
        idlist = vals.split(",", 3)
        if len(idlist) == 4:
            type = idlist[1]
            idno = idlist[0]
            idrow = idlist[2]
            ns = idlist[3]
            return type, idno, idrow, ns

    def create_id_breakdown(self):

        tooltype = self.analysisresults.tooltype
        query = self.query.methods_return_ns_sort(self.priority_ns_id)
        allids = self.__querydb__(query)
        method_list = []

        container_bin = []
        binary_bin = []
        xml_bin = []
        text_bin = []
        filename_bin = []
        extension_bin = []
        none_bin = []

        binaryidrows = []  # and containers
        xmlidrows = []
        textidrows = []
        filenameidrows = []

        # create a set to remove the fileids with duplicate methods
        for id in allids:
            file = id[0]
            method = id[2].lower().strip()
            idrow = id[1]
            ns = id[3]
            method_list.append(
                str(file) + "," + method + "," + str(idrow) + "," + str(ns)
            )

        # go through list the first time and prioritize container and signature
        # and THEN our sorted list of NS identifiers...
        for id in list(method_list):
            type, idno, idrow, ns = self.__getsplit__(id)
            if type == "container":
                if idno not in container_bin:
                    container_bin.append(idno)
                    binaryidrows.append((idno, idrow))
            if type == "signature":
                if idno not in container_bin and idno not in binary_bin:
                    binary_bin.append(idno)
                    binaryidrows.append((idno, idrow))

        for id in list(method_list):
            type, idno, idrow, ns = self.__getsplit__(id)
            if type == "xml":
                if (
                    idno not in container_bin
                    and idno not in binary_bin
                    and idno not in xml_bin
                ):
                    xml_bin.append(idno)
                    xmlidrows.append((idno, idrow))

        for id in list(method_list):
            type, idno, idrow, ns = self.__getsplit__(id)
            if type == "text":
                if (
                    idno not in container_bin
                    and idno not in binary_bin
                    and idno not in xml_bin
                    and idno not in text_bin
                ):
                    text_bin.append(idno)
                    textidrows.append((idno, idrow))

        for id in list(method_list):
            type, idno, idrow, ns = self.__getsplit__(id)
            if type == "filename":
                if (
                    idno not in container_bin
                    and idno not in binary_bin
                    and idno not in xml_bin
                    and idno not in text_bin
                    and idno not in filename_bin
                ):
                    filename_bin.append(idno)
                    filenameidrows.append((idno, idrow))

        for id in list(method_list):
            type, idno, idrow, ns = self.__getsplit__(id)
            if type == "extension":
                if (
                    idno not in container_bin
                    and idno not in binary_bin
                    and idno not in xml_bin
                    and idno not in text_bin
                    and idno not in filename_bin
                    and idno not in extension_bin
                ):
                    extension_bin.append(idno)

        for id in list(method_list):
            type, idno, idrow, ns = self.__getsplit__(id)
            if type == "none":
                if (
                    idno not in container_bin
                    and idno not in binary_bin
                    and idno not in xml_bin
                    and idno not in text_bin
                    and idno not in filename_bin
                    and idno not in extension_bin
                    and idno not in none_bin
                ):
                    none_bin.append(idno)

        self.analysisresults.identifiedfilecount = len(container_bin) + len(binary_bin)

        self.analysisresults.unidentifiedfilecount = (
            self.analysisresults.filecount - self.analysisresults.identifiedfilecount
        )
        self.analysisresults.extensionIDOnlyCount = len(extension_bin)

        self.extensionIDonly = extension_bin
        self.noids = none_bin

        self.binaryIDs = binaryidrows
        self.xmlIDs = xmlidrows
        self.textIDs = textidrows
        self.filenameIDs = filenameidrows

        self.analysisresults.xmlidfilecount = len(xml_bin)
        self.analysisresults.textidfilecount = len(text_bin)
        self.analysisresults.filenameidfilecount = len(filename_bin)

        # ID Method frequencylist can be created here also
        # e.g. [('None', 2269), ('Text', 149), ('Signature', 57), ('Filename', 52), ('Extension', 7), ('Container', 1)]
        # self.analysisresults.idmethodFrequency
        list1 = ("None", len(none_bin))
        list2 = ("Container", len(container_bin))
        list3 = ("Signature", len(binary_bin))
        list4 = ("Extension", len(extension_bin))

        list_of_lists = [list1, list2, list3, list4]
        if tooltype != "droid":
            list5 = ("Filename", len(filename_bin))
            list6 = ("Text", len(text_bin))
            list7 = ("XML", len(xml_bin))
            list_of_lists.append(list5)
            list_of_lists.append(list6)
            list_of_lists.append(list7)

        list_of_lists.sort(key=lambda tup: tup[1], reverse=True)
        self.analysisresults.idmethodFrequency = list_of_lists
        self.analysisresults.zeroidcount = len(none_bin)

        # Rogues: Get All ids for All tools (need also a PRONOM only one later)
        self.analysisresults.rogue_identified_all = (
            container_bin + binary_bin + text_bin + xml_bin
        )

    def getMethodIDResults(self, methodids, fmt_version=False):
        # TODO: Fine line between formatting, and not formatting in this function
        countlist = []
        text = ""
        methodresults = self.__querydb__(
            self.query.query_from_idrows(methodids, self.priority_ns_id)
        )
        for id in methodresults:
            """
            0  'ns:' || NSDATA.NS_NAME || ' ',
            1  IDDATA.ID,
            2  IDDATA.FORMAT_NAME,
            3  IDDATA.BASIS,
            4  IDDATA.FORMAT_VERSION,
            5  IDDATA.NS_ID,
            6  COUNT(IDDATA.ID
            """
            ns_id = id[5]
            name = id[2]
            if name == "":
                name = ", "
            else:
                name = ", " + name + ", "

            basis = id[3]
            if basis is not None:
                basis = "[" + basis + "]"
            else:
                basis = ""

            if fmt_version == False:
                idval = (
                    id[0] + id[1] + name + id[4] + " " + basis + " (" + str(id[6]) + ")"
                )  # concatenate count
            else:
                # we're creating a less detailed statistic for summary purposes
                idval = (
                    id[0] + id[1] + name + id[4] + " (" + str(id[6]) + ")"
                )  # concatenate count
            countlist.append((idval, ns_id))

        # counter returns dict
        templist = Counter(countlist)

        countlist = []

        for k, v in templist.items():
            countlist.append((k[0], v, k[1]))  # add ns to sort by

        countlist = self.__prioritysort__(countlist)

        final_countlist = []
        for c in countlist:
            final_countlist.append((c[0], c[1]))

        return final_countlist

    def __prioritysort__(self, method_list):
        # sort into two sets then combine
        l1 = []
        l2 = []
        for m in method_list:
            if m[2] == self.priority_ns_id:
                l1.append(m)
            else:
                l2.append(m)
            l1.sort(reverse=False)
            l2.sort(reverse=True)
        return l1 + l2

    def __analysebasis__(self):
        #########['id','basis','filesize','filename','offset']##########
        boftup = [None, "basis", "filename", "filesize", 0]
        eoftup = [None, "basis", "filename", "filesize", 0]
        #########['id','basis','filesize','filename','offset']##########

        basis = self.__querydb__(AnalysisQueries.SELECT_BYTE_MATCH_BASIS)

        for idrow in basis:
            val = idrow[0].split(";")
            filesize = int(idrow[3])
            filename = idrow[2]
            fileid = idrow[1]
            for match in val:
                if "byte match" in match:
                    if "[[[" in match:
                        offs, length = self.__handlesquares__(match)
                    elif "[[" in match:
                        # Previously looking for triple square brackets, but
                        # now seems to be [[]] e.g.
                        # byte match at [[0 16] [77 4] [45015 12]]
                        #
                        offs, length = self.__handlesquares__(match)
                    else:
                        offs, length = self.__handlenosquares__(match)
                    try:
                        bof, eof, filesize = self.__getoffs__(
                            offs, int(length), int(filesize)
                        )
                    except ValueError:
                        print("Cannot handle basis:", offs, match, file=sys.stderr)
                        continue

                    if bof != 0 and boftup[4] < bof:
                        boftup[0] = fileid
                        boftup[1] = match.strip()
                        boftup[2] = filename
                        boftup[3] = filesize
                        boftup[4] = bof

                    if eof != None and eoftup[4] < eof:
                        eoftup[0] = fileid
                        eoftup[1] = match.strip()
                        eoftup[2] = filename
                        eoftup[3] = filesize
                        eoftup[4] = eof

        if boftup[0] == None:
            boftup = None
        if eoftup[0] == None:
            eoftup = None

        return boftup, eoftup

    def __getoffs__(self, basis, length, filesize):
        if length == 1:
            pos = int(basis[0])
            pos_len = int(basis[1])
            bof = pos + pos_len
            eof = filesize - pos
            return bof, None, filesize
        else:
            bof = 0
            eof = 0
            for x in range(length):
                tmppos = basis[x * 2]
                tmplen = basis[(x * 2) + 1]
                tmpbof = int(tmppos) + int(tmplen)
                tmpeof = filesize - int(tmppos)
                if tmpbof < tmpeof:
                    bof = tmpbof
                elif tmpeof < tmpbof:
                    eof = tmpeof
            return bof, eof, filesize

    def __handlesquares__(self, basis):
        basis = basis.replace("byte match at", "").strip()
        no_sequences = (basis.count("[[")) * 2
        basis = (basis.replace("[", "")).replace("]", "").replace(" ", ",")
        return basis.split(",", no_sequences)[:no_sequences], (no_sequences / 2)

    def __handlenosquares__(self, basis):
        basis = basis.replace("byte match at", "").strip()
        basis = basis.replace("(", ",(")
        basis = basis.replace(" ", "").split(",", 2)[:2]
        return basis, 1

    def getblacklistresults(self):
        bl = BlacklistQueries()
        blacklist = {}

        if self.blacklist[HandleBlacklist.IDS] != None:
            q4 = bl.getids(self.blacklist[HandleBlacklist.IDS])
            ids = self.__querydb__(q4)
            if ids:
                for found in ids:
                    blacklist[found[0]] = (HandleBlacklist.IDS, found[2].strip())

        if self.blacklist[HandleBlacklist.EXTENSIONS] != None:
            q3 = bl.getexts(self.blacklist[HandleBlacklist.EXTENSIONS])
            extensions = self.__querydb__(q3)
            if extensions:
                for found in extensions:
                    if found[0] not in blacklist.keys():
                        blacklist[found[0]] = (HandleBlacklist.EXTENSIONS, found[2])

        if self.blacklist[HandleBlacklist.FILENAMES] != None:
            q1 = bl.getfilenames(self.blacklist[HandleBlacklist.FILENAMES])
            filenames = self.__querydb__(q1)
            if filenames:
                for found in filenames:
                    if found[0] not in blacklist.keys():
                        blacklist[found[0]] = (HandleBlacklist.FILENAMES, found[1])

        if self.blacklist[HandleBlacklist.DIRECTORIES] != None:
            q2 = bl.getdirnames(self.blacklist[HandleBlacklist.DIRECTORIES])
            directories = self.__querydb__(q2)
            if directories:
                for found in directories:
                    if found[0] not in blacklist.keys():
                        blacklist[found[0]] = (HandleBlacklist.DIRECTORIES, found[1])

        if not blacklist:
            blacklist = False
        else:
            newlist = []
            for k, v in blacklist.iteritems():
                self.analysisresults.rogue_blacklist.append(k)
                newlist.append(v)
            count = Counter(newlist)
            newlist = []
            for c, v in count.iteritems():
                newlist.append(c + (v,))
            newlist.sort(key=lambda tup: tup[len(tup) - 1], reverse=True)
            blacklist = newlist

            for b in blacklist:
                if b[0] == HandleBlacklist.DIRECTORIES:
                    self.analysisresults.blacklist_directories.append((b[1], b[2]))
                if b[0] == HandleBlacklist.FILENAMES:
                    self.analysisresults.blacklist_filenames.append((b[1], b[2]))
                if b[0] == HandleBlacklist.EXTENSIONS:
                    self.analysisresults.blacklist_exts.append((b[1], b[2]))
                if b[0] == HandleBlacklist.IDS:
                    self.analysisresults.blacklist_ids.append((b[1], b[2]))

    def queryDB(self):
        self.hashtype = self.__querydb__(AnalysisQueries.SELECT_HASH, True)[0]
        if self.hashtype == "None" or self.hashtype == "False":
            sys.stderr.write(AnalysisQueries.ERROR_NOHASH + "\n")
            self.analysisresults.hashused = False
        else:
            self.analysisresults.hashused = True

        self.analysisresults.collectionsize = self.__querydb__(
            AnalysisQueries.SELECT_COLLECTION_SIZE, True, True
        )
        self.analysisresults.filecount = self.__querydb__(
            AnalysisQueries.SELECT_COUNT_FILES, True, True
        )
        self.analysisresults.containercount = self.__querydb__(
            AnalysisQueries.SELECT_COUNT_CONTAINERS, True, True
        )
        self.analysisresults.filesincontainercount = self.__querydb__(
            AnalysisQueries.SELECT_COUNT_FILES_IN_CONTAINERS, True, True
        )
        self.analysisresults.directoryCount = self.__querydb__(
            AnalysisQueries.SELECT_COUNT_FOLDERS, True, True
        )

        # not necessarily used in the output
        self.analysisresults.uniqueFileNames = self.__querydb__(
            AnalysisQueries.SELECT_COUNT_UNIQUE_FILENAMES, True, True
        )
        self.analysisresults.uniqueDirectoryNames = (
            self.__querydb__(AnalysisQueries.SELECT_COUNT_UNIQUE_DIRNAMES, True, True)
            - self.NONROOTBASEDIR
        )

        # ------------WHAT IS AND ISN'T IDENTIFIED SUMMARY------------#
        self.create_id_breakdown()
        # ------------WHAT IS AND ISN'T IDENTIFIED SUMMARY------------#

        self.analysisresults.extmismatchCount = self.__querydb__(
            AnalysisQueries.SELECT_COUNT_EXT_MISMATCHES, True, True
        )
        self.analysisresults.distinctSignaturePuidcount = self.__querydb__(
            AnalysisQueries.SELECT_COUNT_FORMAT_COUNT, True, True
        )

        if self.analysisresults.tooltype != "droid":
            self.analysisresults.distinctOtherIdentifiers = self.__querydb__(
                AnalysisQueries.SELECT_COUNT_OTHER_FORMAT_COUNT, True, True
            )
            self.analysisresults.distinctXMLIdentifiers = self.__querydb__(
                self.query.select_count_identifiers("XML"), True, True
            )
            self.analysisresults.distinctTextIdentifiers = self.__querydb__(
                self.query.select_count_identifiers("Text"), True, True
            )
            self.analysisresults.distinctFilenameIdentifiers = self.__querydb__(
                self.query.select_count_identifiers("Filename"), True, True
            )

            self.analysisresults.xml_identifiers = self.__querydb__(
                self.query.select_frequency_identifier_types("XML")
            )
            self.analysisresults.text_identifiers = self.__querydb__(
                self.query.select_frequency_identifier_types("Text")
            )
            self.analysisresults.filename_identifiers = self.__querydb__(
                self.query.select_frequency_identifier_types("Filename")
            )

        self.analysisresults.distinctextensioncount = self.__querydb__(
            AnalysisQueries.SELECT_COUNT_EXTENSION_RANGE, True, True
        )

        # todo: consider merit of each identification bin
        mimeids = self.binaryIDs + self.xmlIDs + self.textIDs
        self.analysisresults.mimetypeFrequency = self.__querydb__(
            self.query.getmimes(mimeids)
        )

        # NOTE: Must be calculated after we have total, and subset values
        self.analysisresults.identifiedPercentage = self.calculatePercent(
            self.analysisresults.filecount, self.analysisresults.identifiedfilecount
        )
        self.analysisresults.unidentifiedPercentage = self.calculatePercent(
            self.analysisresults.filecount, self.analysisresults.unidentifiedfilecount
        )

        self.analysisresults.dateFrequency = self.__querydb__(
            AnalysisQueries.SELECT_YEAR_FREQUENCY_COUNT
        )
        self.analysisresults.signatureidentifiedfrequency = self.__querydb__(
            AnalysisQueries.SELECT_BINARY_MATCH_COUNT
        )
        self.analysisresults.extensionOnlyIDList = self.__querydb__(
            AnalysisQueries.SELECT_PUIDS_EXTENSION_ONLY
        )
        self.analysisresults.multipleidentificationcount = self.multiplecount(
            self.analysisresults.namespacecount
        )

        # most complicated way to retrieve extension only PUIDs
        if len(self.extensionIDonly) > 0:
            extid = self.query.query_from_ids(self.extensionIDonly, "Extension")
            test = self.__querydb__(extid)
            combined_list = []  # namespace + id
            for entry in test:
                entry = " ".join(entry)
                combined_list.append(entry)
            sorted_list = Counter(elem for elem in combined_list).most_common()
            self.analysisresults.extensionOnlyIDFrequency = sorted_list

        # OKAY stat...
        self.analysisresults.uniqueExtensionsInCollectionList = self.__querydb__(
            AnalysisQueries.SELECT_ALL_UNIQUE_EXTENSIONS
        )
        self.analysisresults.frequencyOfAllExtensions = self.__querydb__(
            AnalysisQueries.SELECT_COUNT_EXTENSION_FREQUENCY
        )

        # Additional useful queries...
        self.analysisresults.containertypeslist = self.__querydb__(
            AnalysisQueries.SELECT_CONTAINER_TYPES
        )

        # MORE WORK NEEDED ON ROGUES NOW... ACCURACY IS PARAMOUNT
        if len(self.extensionIDonly) > 0:
            extonly = self.query.query_from_ids(self.extensionIDonly)
            extrogues = self.__querydb__(extonly)
        if len(self.noids) > 0:  # NOT THE SAME AS COMPLETELY UNIDENTIFIED
            none = self.query.query_from_ids(self.noids)
            nonerogues = self.__querydb__(none)

        # create a statistic for aggregated binary identification
        if self.binaryIDs is not None and len(self.binaryIDs) > 0:
            self.analysisresults.signatureidentifiers = self.getMethodIDResults(
                self.binaryIDs, True
            )

        # New functions thanks to Siegfried
        if self.binaryIDs is not None and len(self.binaryIDs) > 0:
            self.analysisresults.binaryidentifiers = self.getMethodIDResults(
                self.binaryIDs
            )
        if self.xmlIDs is not None and len(self.xmlIDs) > 0:
            self.analysisresults.xmlidentifiers = self.getMethodIDResults(self.xmlIDs)
        if self.textIDs is not None and len(self.textIDs) > 0:
            self.analysisresults.textidentifiers = self.getMethodIDResults(self.textIDs)
        if self.filenameIDs is not None and len(self.filenameIDs) > 0:
            self.analysisresults.filenameidentifiers = self.getMethodIDResults(
                self.filenameIDs
            )
        if self.analysisresults.tooltype != "droid":
            (
                self.analysisresults.bof_distance,
                self.analysisresults.eof_distance,
            ) = self.__analysebasis__()
            self.analysisresults.errorlist = self.__querydb__(
                AnalysisQueries.SELECT_FREQUENCY_ERRORS
            )
        # we need namespace data - ann NS queries can be generic
        # ns count earlier on in this function can be left as-is
        if (
            self.analysisresults.namespacecount is not None
            and self.analysisresults.namespacecount > 0
        ):
            nsdatalist = []
            for ns in self.namespacedata:
                nsdict = {}
                nsid = ns[0]
                nsdict[self.NS_CONST_TITLE] = ns[1]
                nsdict[self.NS_CONST_DETAILS] = ns[2]
                nsdict[self.NS_CONST_BINARY_COUNT] = self.__querydb__(
                    self.query.get_ns_methods(nsid), True, True
                )
                nsdict[self.NS_CONST_XML_COUNT] = self.__querydb__(
                    self.query.get_ns_methods(nsid, False, "XML"), True, True
                )
                nsdict[self.NS_CONST_TEXT_COUNT] = self.__querydb__(
                    self.query.get_ns_methods(nsid, False, "Text"), True, True
                )
                nsdict[self.NS_CONST_FILENAME_COUNT] = self.__querydb__(
                    self.query.get_ns_methods(nsid, False, "Filename"), True, True
                )
                nsdict[self.NS_CONST_EXTENSION_COUNT] = self.__querydb__(
                    self.query.get_ns_methods(nsid, False, "Extension"), True, True
                )
                nsdict[self.NS_CONST_MULTIPLE_IDS] = self.__querydb__(
                    self.query.get_ns_multiple_ids(
                        nsid, self.analysisresults.namespacecount
                    ),
                    True,
                    True,
                )
                nsdatalist.append(nsdict)
            self.analysisresults.nsdatalist = nsdatalist

            # get nsgap count
            if self.analysisresults.namespacecount > 1:
                idslist = []
                for ns in self.namespacedata:
                    nsid = ns[0]
                    idslist = idslist + self.__querydb__(
                        self.query.get_ns_gap_count_lists(nsid), False, False, True
                    )

                counted = dict(Counter(idslist))
                noids = []
                for x in counted:
                    if counted[x] == self.analysisresults.namespacecount:
                        noids.append(x)
                self.analysisresults.identificationgaps = len(noids)

            # handle filename analysis
            self.msoftfnameanalysis()

            ###################################################################################
            ######BLACKLIST RESULTS: GET RESULTS SPECIFIC TO THE BLACKLIST FUNCTIONALITY#######
            ###################################################################################
            if self.blacklist is not False:
                self.analysisresults.blacklist = True
                self.getblacklistresults()

            ###################################################################################
            # ROGUES: Functions associated with Rogues - Nearly every QUERY that returns a PATH#
            ###################################################################################

            # need to run these regardless of choice to use rogues
            self.listzerobytefiles()  # self.analysisresults.zerobytelist

            if self.analysisresults.hashused is True:
                self.analysisresults.rogue_duplicates = (
                    self.listDuplicateFilesFromHASH()
                )  # expensive duplicate checking [default: ON]

            if self.analysisresults.multipleidentificationcount > 0:
                self.analysisresults.rogue_multiple_identification_list = self.multiple_id_paths(
                    self.analysisresults.namespacecount
                )

            if self.rogueanalysis:

                rq = RogueQueries()
                self.analysisresults.rogue_all_paths = self.__querydb__(
                    rq.SELECT_ALL_FILEPATHS, False, False, True
                )
                self.analysisresults.rogue_all_dirs = self.__querydb__(
                    rq.SELECT_ALL_FOLDERS, False, False, True
                )

                self.analysisresults.rogue_extension_mismatches = self.__querydb__(
                    rq.SELECT_EXTENSION_MISMATCHES, False, False, True
                )

                # NEED THIS FOR DROID TOOL ONLY?
                if self.analysisresults.tooltype == "droid":
                    self.pronom_ns_id = 1

                if self.pronom_ns_id != None:
                    self.analysisresults.rogue_pronom_ns_id = self.pronom_ns_id
                    self.analysisresults.rogue_identified_pronom = self.__querydb__(
                        rq.get_pronom_identified_files(self.pronom_ns_id),
                        False,
                        False,
                        True,
                    )
                else:
                    self.analysisresults.rogue_identified_all = self.__querydb__(
                        rq.get_all_non_ids(self.analysisresults.rogue_identified_all),
                        False,
                        False,
                        True,
                    )

                self.analysisresults.rogue_file_name_paths = self.__querydb__(
                    rq.get_rogue_name_paths(self.rogue_names), False, False, True
                )

                if len(self.rogue_dirs) > 0:
                    self.analysisresults.rogue_dir_name_paths = self.__querydb__(
                        rq.get_rogue_dir_paths(self.rogue_dirs), False, False, True
                    )

        return self.analysisresults

    def runanalysis(self, rogueanalysis):
        self.rogueanalysis = rogueanalysis
        analysisresults = self.queryDB()  # primary db query functions
        return self.analysisresults

    def openDROIDDB(self, dbfilename):
        self.analysisresults.filename = dbfilename.rstrip(".db")
        self.conn = sqlite3.connect(dbfilename)
        self.conn.text_factory = str  # encoded as ascii, not unicode / return ascii
        self.cursor = self.conn.cursor()

    def closeDROIDDB(self):
        self.conn.close()
