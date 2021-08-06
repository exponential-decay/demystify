# -*- coding: utf-8 -*-

# pylint: disable=W1633

from __future__ import absolute_import, division, print_function

try:
    from ConfigParser import NoOptionError
except ImportError:
    from configparser import NoOptionError

import logging
import sqlite3
import sys
from collections import Counter

from libs import AnalysisResultsClass
from libs.AnalysisQueriesClass import AnalysisQueries
from libs.DenylistQueriesClass import DenylistQueries
from libs.HandleDenylistClass import HandleDenylist
from libs.RoguesQueriesClass import RogueQueries
from libs.version import AnalysisVersion
from pathlesstaken import pathlesstaken


class AnalysisError(Exception):
    """Exception for DemystifyAnalysis object."""


class DemystifyAnalysis:
    """DemystifyAnalysis"""

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

    ID_TIKA = "TIKA"
    ID_PRONOM = "PRONOM"
    ID_FREEDESKTOP = "FREE"
    ID_NONE = "NONE"

    TOOLTYPE_DROID = "droid"

    def __init__(self, database_path=None, config=False, denylist=None):
        """Constructor for DemystifyAnalysis object."""

        logging.error("Analysis init: %s %s %s", database_path, config, denylist)

        if database_path is None:
            raise AnalysisError(
                "Cannot initialize analysis class without a database: {}".format(
                    database_path
                )
            )

        # Give the object a place to hold results and the powers to
        # generate data for that.
        self.analysis_results = AnalysisResultsClass.AnalysisResults()
        self.query = AnalysisQueries()

        # Initialize database connection variables.
        self._open_database(database_path)
        self.analysis_results.tooltype = self.__querydb__(self.query.SELECT_TOOL, True)[
            0
        ]

        self.denylist = denylist

        # Initialize instance variables.
        self.extensionIDonly = None
        self.binaryIDs = None
        self.noids = None
        self.xmlIDs = None
        self.textIDs = None
        self.filenameIDs = None

        # Initialize namespaace data.
        self._initialize_namespace_details(config)

    def __del__(self):
        """Destructor for DemystifyAnalysis object."""
        try:
            self._close_database()
        except AttributeError:
            logging.error("Destructor should not reach here...")

    def __version__(self):
        """Return a version number for the analysis."""
        v = AnalysisVersion()
        self.analysis_results.__version_no__ = v.getVersion()
        return self.analysis_results.__version_no__

    def _open_database(self, dbfilename):
        """Open the database connection and initialize the instance
        variables needed to run the demystify analysis.
        """
        self.analysis_results.filename = dbfilename.rstrip(".db")
        self.conn = sqlite3.connect(dbfilename)
        self.conn.text_factory = str  # encoded as ascii, not unicode / return ascii
        self.cursor = self.conn.cursor()

    def _close_database(self):
        """Close the database connection."""
        self.conn.close()

    def _initialize_namespace_details(self, config):
        """Initialize namespace data.

        Working with Siegfried means that we can work with multiple
        namespaces. Setup work and initialization of class variables is
        all done here.
        """
        self.namespacedata = None
        self.priority_ns_id = None
        self.pronom_ns_id = None
        self.freedesktop_ns_id = None
        self.tika_ns_id = None

        self.namespacedata = self.__querydb__(self.query.SELECT_NS_DATA)

        if self.analysis_results.tooltype == self.TOOLTYPE_DROID:
            self.analysis_results.namespacecount = 1
            return

        self.analysis_results.namespacecount = self.__querydb__(
            self.query.SELECT_COUNT_NAMESPACES, True
        )[0]
        if self.analysis_results.namespacecount <= 1:
            return

        # Assign an index in the namespace lookup table to our instance
        # variables to support lookup during the analysis.
        for namespace_details in self.namespacedata:
            sig_details = namespace_details[2]
            if "DROID_" in sig_details and "limited to" not in sig_details:
                self.pronom_ns_id = namespace_details[0]
            elif "tika" in sig_details:
                self.tika_ns_id = namespace_details[0]
            elif "freedesktop" in sig_details:
                self.freedesktop_ns_id = namespace_details[0]

        # Workout priority ID based on the namespace indices above.
        self.priority_ns_id = self.__get_ns_priority__(self.__readconfig__(config))

    def __get_ns_priority__(self, config):
        if not config:
            return self.pronom_ns_id
        if config == self.ID_PRONOM:
            return self.pronom_ns_id
        if config == self.ID_FREEDESKTOP:
            return self.freedesktop_ns_id
        if config == self.ID_TIKA:
            return self.tika_ns_id
        return None

    def __readconfig__(self, config):
        """Read values from config.

        At this point in time this is only a way to prioritize a
        namespace in the output.

        :param config: Configuration object (ConfigParser)
        :return: Namespace ID (String const) or None (Nonetype)
        """
        if not config:
            return None
        if not config.has_section("priority"):
            return None
        try:
            config.get("priority", "pronom").lower() == "true"
            return self.ID_PRONOM
        except NoOptionError:
            pass
        try:
            config.get("priority", "freedesktop").lower() == "true"
            return self.ID_FREEDESKTOP
        except NoOptionError:
            pass
        try:
            config.get("priority", "tika").lower() == "true"
            return self.ID_TIKA
        except NoOptionError:
            pass
        return None

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

    # List queries

    def list_duplicate_files_from_hash(self):
        """Process duplicates based on hash from analysis."""

        # Result will looks as follows: list([HASH, COUNT])
        result = self.__querydb__(AnalysisQueries.SELECT_COUNT_DUPLICATE_CHECKSUMS)

        duplicatelist = []
        duplicate_sum = {}
        roguepaths = []

        self.analysis_results.totalHASHduplicates = 0

        for res in result:
            count = int(res[1])
            checksum = res[0]

            # There is a potential or empty checksums in the database,
            # either through incorrectly writing the data or rogue
            # datasets, avoid processing and outputting those here.
            if checksum == "":
                continue

            self.analysis_results.totalHASHduplicates = (
                self.analysis_results.totalHASHduplicates + count
            )
            duplicate_examples = self.__querydb__(
                self.query.list_duplicate_paths(res[0])
            )
            pathlist = []
            for duplicates in duplicate_examples:
                filename = duplicates[0]
                pathlist.append(filename)
                self.analysis_results.duplicatespathlist.append(filename)
            roguepaths = "{}{}".format(roguepaths, pathlist)
            duplicate_sum["checksum"] = checksum
            duplicate_sum["count"] = count
            duplicate_sum["examples"] = pathlist
            duplicatelist.append(duplicate_sum)
            duplicate_sum = {}

        self.analysis_results.duplicateHASHlisting = duplicatelist
        return roguepaths

    def listzerobytefiles(self):
        self.analysis_results.zerobytecount = self.__querydb__(
            AnalysisQueries.SELECT_COUNT_ZERO_BYTE_FILES, True, True
        )
        if self.analysis_results.zerobytecount > 0:
            self.analysis_results.zerobytelist = self.__querydb__(
                AnalysisQueries.SELECT_ZERO_BYTE_FILEPATHS, False, False, True
            )
        else:
            self.analysis_results.zerobytelist = None
        return self.analysis_results.zerobytecount

    def calculatePercent(self, total, subset):
        if total > 0:
            percentage = (subset / total) * 100
            return "%.1f" % round(percentage, 1)

    def msoftfnameanalysis(self):
        namelist = self.__querydb__(AnalysisQueries.SELECT_FILENAMES)
        dirlist = self.__querydb__(AnalysisQueries.SELECT_DIRNAMES)

        charcheck = pathlesstaken.PathlesstakenAnalysis()

        self.rogue_names = []
        self.rogue_dirs = []

        namereport = []
        for d in namelist:
            try:
                namestring = u"{}".format(d[0].decode("utf8"))
            except AttributeError:
                namestring = u"{}".format(d[0])
            checkedname = charcheck.complete_file_name_analysis(namestring)
            if len(checkedname) > 0:
                namereport.append(checkedname)
                self.rogue_names.append(d[0])

        dirreport = []
        for d in dirlist:
            try:
                dirstring = u"{}".format(d[0].decode("utf8"))
            except AttributeError:
                dirstring = u"{}".format(d[0])
            checkedname = charcheck.complete_file_name_analysis(dirstring, True)
            if len(checkedname) > 0:
                dirreport.append(checkedname)
                self.rogue_dirs.append(d[0])

        self.analysis_results.badFileNames = namereport
        self.analysis_results.badDirNames = dirreport

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

        tooltype = self.analysis_results.tooltype
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
        for id_ in allids:
            file = id_[0]
            try:
                method = id_[2].lower().strip()
                idrow = id_[1]
                ns = id_[3]
                method_list.append(
                    str(file) + "," + method + "," + str(idrow) + "," + str(ns)
                )
            except AttributeError:
                logging.error("We shouldn't have this issue - begins in sqlitefid")
                pass

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

        self.analysis_results.identifiedfilecount = len(container_bin) + len(binary_bin)

        self.analysis_results.unidentifiedfilecount = (
            self.analysis_results.filecount - self.analysis_results.identifiedfilecount
        )
        self.analysis_results.extensionIDOnlyCount = len(extension_bin)

        self.extensionIDonly = extension_bin
        self.noids = none_bin

        self.binaryIDs = binaryidrows
        self.xmlIDs = xmlidrows
        self.textIDs = textidrows
        self.filenameIDs = filenameidrows

        self.analysis_results.xmlidfilecount = len(xml_bin)
        self.analysis_results.textidfilecount = len(text_bin)
        self.analysis_results.filenameidfilecount = len(filename_bin)

        # ID Method frequencylist can be created here also
        # e.g. [('None', 2269), ('Text', 149), ('Signature', 57), ('Filename', 52), ('Extension', 7), ('Container', 1)]
        # self.analysis_results.idmethodFrequency
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
        self.analysis_results.idmethodFrequency = list_of_lists
        self.analysis_results.zeroidcount = len(none_bin)

        # Rogues: Get All ids for All tools (need also a PRONOM only one later)
        self.analysis_results.rogue_identified_all = (
            container_bin + binary_bin + text_bin + xml_bin
        )

    def getMethodIDResults(self, methodids, fmt_version=False):
        # TODO: Fine line between formatting, and not formatting in this function
        countlist = []
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

            if fmt_version is False:
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
        # #########['id','basis','filesize','filename','offset']##########
        boftup = [None, "basis", "filename", "filesize", 0]
        eoftup = [None, "basis", "filename", "filesize", 0]
        # #########['id','basis','filesize','filename','offset']##########

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

                    if eof is not None and eoftup[4] < eof:
                        eoftup[0] = fileid
                        eoftup[1] = match.strip()
                        eoftup[2] = filename
                        eoftup[3] = filesize
                        eoftup[4] = eof

        if boftup[0] is None:
            boftup = None
        if eoftup[0] is None:
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

    def getdenylistresults(self):
        bl = DenylistQueries()
        denylist = {}

        if self.denylist.get(HandleDenylist.IDS) is not None:
            q4 = bl.getids(self.denylist[HandleDenylist.IDS])
            ids = self.__querydb__(q4)
            if ids:
                for found in ids:
                    denylist[found[0]] = (HandleDenylist.IDS, found[2].strip())

        if self.denylist.get(HandleDenylist.EXTENSIONS) is not None:
            q3 = bl.getexts(self.denylist[HandleDenylist.EXTENSIONS])
            extensions = self.__querydb__(q3)
            if extensions:
                for found in extensions:
                    if found[0] not in list(denylist.keys()):
                        denylist[found[0]] = (HandleDenylist.EXTENSIONS, found[2])

        if self.denylist.get(HandleDenylist.FILENAMES) is not None:
            q1 = bl.getfilenames(self.denylist[HandleDenylist.FILENAMES])
            filenames = self.__querydb__(q1)
            if filenames:
                for found in filenames:
                    if found[0] not in list(denylist.keys()):
                        denylist[found[0]] = (HandleDenylist.FILENAMES, found[1])

        if self.denylist.get(HandleDenylist.DIRECTORIES) is not None:
            q2 = bl.getdirnames(self.denylist[HandleDenylist.DIRECTORIES])
            directories = self.__querydb__(q2)
            if directories:
                for found in directories:
                    if found[0] not in list(denylist.keys()):
                        denylist[found[0]] = (HandleDenylist.DIRECTORIES, found[1])

        if not denylist:
            denylist = False
        else:
            newlist = []
            for k, v in denylist.items():
                self.analysis_results.rogue_denylist.append(k)
                newlist.append(v)
            count = Counter(newlist)
            newlist = []
            for c, v in count.items():
                newlist.append(c + (v,))
            newlist.sort(key=lambda tup: tup[len(tup) - 1], reverse=True)
            denylist = newlist

            for b in denylist:
                if b[0] == HandleDenylist.DIRECTORIES:
                    self.analysis_results.denylist_directories.append((b[1], b[2]))
                if b[0] == HandleDenylist.FILENAMES:
                    self.analysis_results.denylist_filenames.append((b[1], b[2]))
                if b[0] == HandleDenylist.EXTENSIONS:
                    self.analysis_results.denylist_exts.append((b[1], b[2]))
                if b[0] == HandleDenylist.IDS:
                    self.analysis_results.denylist_ids.append((b[1], b[2]))

    def queryDB(self):
        """Query runner for all demystify queries based on how the
        object has been configured up to now.

        :returns: The analysis object containing all of the results. The
            object can be used to then output different serialization
            types.
        """
        logging.info("Querying database")
        self.hashtype = self.__querydb__(AnalysisQueries.SELECT_HASH, True)[0]
        if self.hashtype == "None" or self.hashtype == "False":
            sys.stderr.write(AnalysisQueries.ERROR_NOHASH + "\n")
            self.analysis_results.hashused = False
        else:
            self.analysis_results.hashused = True

        self.analysis_results.collectionsize = self.__querydb__(
            AnalysisQueries.SELECT_COLLECTION_SIZE, True, True
        )
        self.analysis_results.filecount = self.__querydb__(
            AnalysisQueries.SELECT_COUNT_FILES, True, True
        )
        self.analysis_results.containercount = self.__querydb__(
            AnalysisQueries.SELECT_COUNT_CONTAINERS, True, True
        )
        self.analysis_results.filesincontainercount = self.__querydb__(
            AnalysisQueries.SELECT_COUNT_FILES_IN_CONTAINERS, True, True
        )
        self.analysis_results.directoryCount = self.__querydb__(
            AnalysisQueries.SELECT_COUNT_FOLDERS, True, True
        )

        # not necessarily used in the output
        self.analysis_results.uniqueFileNames = self.__querydb__(
            AnalysisQueries.SELECT_COUNT_UNIQUE_FILENAMES, True, True
        )
        self.analysis_results.uniqueDirectoryNames = (
            self.__querydb__(AnalysisQueries.SELECT_COUNT_UNIQUE_DIRNAMES, True, True)
            - self.NONROOTBASEDIR
        )

        # ------------WHAT IS AND ISN'T IDENTIFIED SUMMARY------------#
        self.create_id_breakdown()
        # ------------WHAT IS AND ISN'T IDENTIFIED SUMMARY------------#

        self.analysis_results.extmismatchCount = self.__querydb__(
            AnalysisQueries.SELECT_COUNT_EXT_MISMATCHES, True, True
        )
        self.analysis_results.distinctSignaturePuidcount = self.__querydb__(
            AnalysisQueries.SELECT_COUNT_FORMAT_COUNT, True, True
        )

        if self.analysis_results.tooltype != "droid":
            self.analysis_results.distinctOtherIdentifiers = self.__querydb__(
                AnalysisQueries.SELECT_COUNT_OTHER_FORMAT_COUNT, True, True
            )
            self.analysis_results.distinctXMLIdentifiers = self.__querydb__(
                self.query.select_count_identifiers("XML"), True, True
            )
            self.analysis_results.distinctTextIdentifiers = self.__querydb__(
                self.query.select_count_identifiers("Text"), True, True
            )
            self.analysis_results.distinctFilenameIdentifiers = self.__querydb__(
                self.query.select_count_identifiers("Filename"), True, True
            )

            self.analysis_results.xml_identifiers = self.__querydb__(
                self.query.select_frequency_identifier_types("XML")
            )
            self.analysis_results.text_identifiers = self.__querydb__(
                self.query.select_frequency_identifier_types("Text")
            )
            self.analysis_results.filename_identifiers = self.__querydb__(
                self.query.select_frequency_identifier_types("Filename")
            )

        self.analysis_results.distinctextensioncount = self.__querydb__(
            AnalysisQueries.SELECT_COUNT_EXTENSION_RANGE, True, True
        )

        # todo: consider merit of each identification bin
        mimeids = self.binaryIDs + self.xmlIDs + self.textIDs
        self.analysis_results.mimetypeFrequency = self.__querydb__(
            self.query.getmimes(mimeids)
        )

        # NOTE: Must be calculated after we have total, and subset values
        self.analysis_results.identifiedPercentage = self.calculatePercent(
            self.analysis_results.filecount, self.analysis_results.identifiedfilecount
        )
        self.analysis_results.unidentifiedPercentage = self.calculatePercent(
            self.analysis_results.filecount, self.analysis_results.unidentifiedfilecount
        )

        self.analysis_results.dateFrequency = self.__querydb__(
            AnalysisQueries.SELECT_YEAR_FREQUENCY_COUNT
        )
        self.analysis_results.signatureidentifiedfrequency = self.__querydb__(
            AnalysisQueries.SELECT_BINARY_MATCH_COUNT
        )
        self.analysis_results.extensionOnlyIDList = self.__querydb__(
            AnalysisQueries.SELECT_PUIDS_EXTENSION_ONLY
        )
        self.analysis_results.multipleidentificationcount = self.multiplecount(
            self.analysis_results.namespacecount
        )

        # most complicated way to retrieve extension only PUIDs
        if len(self.extensionIDonly) > 0:
            extid = self.query.query_from_ids(self.extensionIDonly, "Extension")
            test = self.__querydb__(extid)
            combined_list = []
            for entry in test:
                entry = " ".join(entry)
                combined_list.append(entry)
            sorted_list = Counter(elem for elem in combined_list).most_common()
            self.analysis_results.extensionOnlyIDFrequency = sorted_list

        # OKAY stat...
        self.analysis_results.uniqueExtensionsInCollectionList = self.__querydb__(
            AnalysisQueries.SELECT_ALL_UNIQUE_EXTENSIONS
        )
        self.analysis_results.frequencyOfAllExtensions = self.__querydb__(
            AnalysisQueries.SELECT_COUNT_EXTENSION_FREQUENCY
        )

        # Additional useful queries...
        self.analysis_results.containertypeslist = self.__querydb__(
            AnalysisQueries.SELECT_CONTAINER_TYPES
        )

        # MORE WORK NEEDED ON ROGUES NOW... ACCURACY IS PARAMOUNT
        if len(self.extensionIDonly) > 0:
            """TODO: The values below are not used - why?"""
            # extonly = self.query.query_from_ids(self.extensionIDonly)
            # extrogues = self.__querydb__(extonly)
        if len(self.noids) > 0:  # NOT THE SAME AS COMPLETELY UNIDENTIFIED
            """TODO: The values below are not used - why?"""
            # none = self.query.query_from_ids(self.noids)
            # nonerogues = self.__querydb__(none)

        # create a statistic for aggregated binary identification
        if self.binaryIDs is not None and len(self.binaryIDs) > 0:
            self.analysis_results.signatureidentifiers = self.getMethodIDResults(
                self.binaryIDs, True
            )

        # New functions thanks to Siegfried
        if self.binaryIDs is not None and len(self.binaryIDs) > 0:
            self.analysis_results.binaryidentifiers = self.getMethodIDResults(
                self.binaryIDs
            )
        if self.xmlIDs is not None and len(self.xmlIDs) > 0:
            self.analysis_results.xmlidentifiers = self.getMethodIDResults(self.xmlIDs)
        if self.textIDs is not None and len(self.textIDs) > 0:
            self.analysis_results.textidentifiers = self.getMethodIDResults(
                self.textIDs
            )
        if self.filenameIDs is not None and len(self.filenameIDs) > 0:
            self.analysis_results.filenameidentifiers = self.getMethodIDResults(
                self.filenameIDs
            )
        if self.analysis_results.tooltype != "droid":
            (
                self.analysis_results.bof_distance,
                self.analysis_results.eof_distance,
            ) = self.__analysebasis__()
            self.analysis_results.errorlist = self.__querydb__(
                AnalysisQueries.SELECT_FREQUENCY_ERRORS
            )

        # we need namespace data - and NS queries can be generic
        # ns count earlier on in this function can be left as-is
        if (
            self.analysis_results.namespacecount is not None
            and self.analysis_results.namespacecount > 0
        ):
            # analysis_results.nsdatalist.
            self.get_namespace_data_list()

            # get nsgap count
            if self.analysis_results.namespacecount > 1:
                idslist = []
                for ns in self.namespacedata:
                    nsid = ns[0]
                    idslist = idslist + self.__querydb__(
                        self.query.get_ns_gap_count_lists(nsid), False, False, True
                    )

                counted = dict(Counter(idslist))
                noids = []
                for x in counted:
                    if counted[x] == self.analysis_results.namespacecount:
                        noids.append(x)
                self.analysis_results.identificationgaps = len(noids)

            # handle filename analysis
            self.msoftfnameanalysis()

            # ###################################################################################
            # ######DENYLIST RESULTS: GET RESULTS SPECIFIC TO THE DENYLIST FUNCTIONALITY#######
            # ###################################################################################
            if self.denylist is not None:
                self.analysis_results.denylist = True
                self.getdenylistresults()

            # ###################################################################################
            # ROGUES: Functions associated with Rogues - Nearly every QUERY that returns a PATH#
            # ###################################################################################

            # need to run these regardless of choice to use rogues
            self.listzerobytefiles()  # self.analysis_results.zerobytelist

            if self.analysis_results.hashused is True:
                self.analysis_results.rogue_duplicates = (
                    self.list_duplicate_files_from_hash()
                )

            if self.analysis_results.multipleidentificationcount > 0:
                self.analysis_results.rogue_multiple_identification_list = self.multiple_id_paths(
                    self.analysis_results.namespacecount
                )

            if self.rogueanalysis:

                rq = RogueQueries()
                self.analysis_results.rogue_all_paths = self.__querydb__(
                    rq.SELECT_ALL_FILEPATHS, False, False, True
                )
                self.analysis_results.rogue_all_dirs = self.__querydb__(
                    rq.SELECT_ALL_FOLDERS, False, False, True
                )

                self.analysis_results.rogue_extension_mismatches = self.__querydb__(
                    rq.SELECT_EXTENSION_MISMATCHES, False, False, True
                )

                # NEED THIS FOR DROID TOOL ONLY?
                if self.analysis_results.tooltype == "droid":
                    self.pronom_ns_id = 1

                if self.pronom_ns_id is not None:
                    self.analysis_results.rogue_pronom_ns_id = self.pronom_ns_id
                    self.analysis_results.rogue_identified_pronom = self.__querydb__(
                        rq.get_pronom_identified_files(self.pronom_ns_id),
                        False,
                        False,
                        True,
                    )
                else:
                    self.analysis_results.rogue_identified_all = self.__querydb__(
                        rq.get_all_non_ids(self.analysis_results.rogue_identified_all),
                        False,
                        False,
                        True,
                    )

                self.analysis_results.rogue_file_name_paths = self.__querydb__(
                    rq.get_rogue_name_paths(self.rogue_names), False, False, True
                )

                if len(self.rogue_dirs) > 0:
                    self.analysis_results.rogue_dir_name_paths = self.__querydb__(
                        rq.get_rogue_dir_paths(self.rogue_dirs), False, False, True
                    )

        return self.analysis_results

    def get_namespace_data_list(self):
        """..."""
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
                    nsid, self.analysis_results.namespacecount
                ),
                True,
                True,
            )
            nsdatalist.append(nsdict)
        self.analysis_results.nsdatalist = nsdatalist

    def runanalysis(self, analyze_rogues):
        """Runs the analysis on the supplied report.

        :param analyze_rogues: Boolean that lets the analysis engine know
            to handle the rogue list at the same time (bool).
        :returns: The analysis object containing all of the results. The
            object can be used to then output different serialization
            types.
        """
        logging.info("Running analysis, rogues: %s", analyze_rogues)
        self.rogueanalysis = analyze_rogues
        return self.queryDB()
