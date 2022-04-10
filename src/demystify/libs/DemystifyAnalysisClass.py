# -*- coding: utf-8 -*-

# pylint: disable=W1633

import logging
import sqlite3
from collections import Counter
from configparser import NoOptionError

try:
    # Required for imports calling from repository root.
    from src.demystify.pathlesstaken.src.pathlesstaken import pathlesstaken
except ModuleNotFoundError:
    # Required for Pypi install.
    from ..pathlesstaken.src.pathlesstaken import pathlesstaken

from . import AnalysisResultsClass
from .AnalysisQueriesClass import AnalysisQueries
from .DenylistQueriesClass import DenylistQueries
from .HandleDenylistClass import HandleDenylist
from .RoguesQueriesClass import RogueQueries
from .version import AnalysisVersion


class AnalysisError(Exception):
    """Exception for DemystifyAnalysis object."""


class DemystifyBase(object):
    """Super class for Demystify statistics with helpers for Demystify
    and callers.
    """

    # Namespace constants.
    NS_CONST_TITLE = "namespace title"
    NS_CONST_DETAILS = "namespace details"
    NS_CONST_XML_COUNT = "xml method count"
    NS_CONST_TEXT_COUNT = "text method count"
    NS_CONST_FILENAME_COUNT = "filename method count"
    NS_CONST_EXTENSION_COUNT = "extension method count"
    NS_CONST_BINARY_COUNT = "binary method count"
    NS_CONST_MULTIPLE_IDS = "multiple ids"

    @staticmethod
    def calculatePercent(total, subset):
        if total > 0:
            percentage = (subset / total) * 100
            return "%.1f" % round(percentage, 1)
        return 0


class DemystifyAnalysis(DemystifyBase):
    """DemystifyAnalysis"""

    # We need this value because we extract basedirs for all folders, including
    # the root directory of the extract, creating one additional entry.
    NONROOTBASEDIR = 1

    ID_TIKA = "TIKA"
    ID_PRONOM = "PRONOM"
    ID_FREEDESKTOP = "FREE"
    ID_NONE = "NONE"

    TOOLTYPE_DROID = "droid"

    def __init__(self, database_path=None, config=False, denylist=None):
        """Constructor for DemystifyAnalysis object."""
        logging.debug(
            "Analysis __init__(): database_path: %s config: %s denylist: %s",
            database_path,
            config,
            denylist,
        )
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
        self.analysis_results.tooltype = self._querydb(self.query.SELECT_TOOL, True)[0]

        self.denylist = denylist

        # Initialize instance variables.
        self.extensionIDonly = None
        self.binaryIDs = None
        self.noids = None
        self.xmlIDs = None
        self.textIDs = None
        self.filenameIDs = None

        # Initialize namespace data.
        self._initialize_namespace_details(config)

    def __del__(self):
        """Destructor for DemystifyAnalysis object."""
        logging.debug("DemystifyAnalysis destructor...")
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
        self.priority_ns_id = None
        self.pronom_ns_id = None
        self.freedesktop_ns_id = None
        self.tika_ns_id = None

        self.namespacedata = self._querydb(self.query.SELECT_NS_DATA)

        if self.analysis_results.tooltype == self.TOOLTYPE_DROID:
            self.analysis_results.namespacecount = 1
            return

        self.analysis_results.namespacecount = self._querydb(
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
        self.priority_ns_id = self._get_ns_priority(self._readconfig(config))

    def _get_ns_priority(self, config):
        if not config:
            return self.pronom_ns_id
        if config == self.ID_PRONOM:
            return self.pronom_ns_id
        if config == self.ID_FREEDESKTOP:
            return self.freedesktop_ns_id
        if config == self.ID_TIKA:
            return self.tika_ns_id
        return None

    def _readconfig(self, config):
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
            _ = config.get("priority", "pronom").lower() == "true"
            return self.ID_PRONOM
        except NoOptionError:
            pass
        try:
            _ = config.get("priority", "freedesktop").lower() == "true"
            return self.ID_FREEDESKTOP
        except NoOptionError:
            pass
        try:
            _ = config.get("priority", "tika").lower() == "true"
            return self.ID_TIKA
        except NoOptionError:
            pass
        return None

    def _querydb(self, query, fetchone=False, numberquery=False, tolist=False):
        """Query DB helper functions as syntactic sugar for the caller
        so that a number of different sqlite query calls styles can be
        used and the caller can do less work to pull those values apart.
        """
        self.cursor.execute(query.replace("  ", ""))
        if fetchone is True and numberquery is False:
            return self.cursor.fetchone()
        if fetchone is True and numberquery is True:
            return self.cursor.fetchone()[0]
        if tolist is False:
            return self.cursor.fetchall()
        list_ = []
        for result in self.cursor.fetchall():
            list_.append(result[0])
        return list_

    # List queries

    def list_duplicate_files_from_hash(self):
        """Process duplicates based on hash from analysis."""
        result = self._querydb(AnalysisQueries.SELECT_COUNT_DUPLICATE_CHECKSUMS)
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
            duplicate_examples = self._querydb(self.query.list_duplicate_paths(res[0]))
            pathlist = []
            for duplicates in duplicate_examples:
                filename = duplicates[0]
                pathlist.append(filename)
                self.analysis_results.duplicatespathlist.append(filename)
            roguepaths = pathlist
            duplicate_sum["checksum"] = checksum
            duplicate_sum["count"] = count
            duplicate_sum["examples"] = pathlist
            duplicatelist.append(duplicate_sum)
            duplicate_sum = {}
        self.analysis_results.duplicateHASHlisting = duplicatelist
        return roguepaths

    def listzerobytefiles(self):
        self.analysis_results.zerobytecount = self._querydb(
            AnalysisQueries.SELECT_COUNT_ZERO_BYTE_FILES, True, True
        )
        if self.analysis_results.zerobytecount > 0:
            self.analysis_results.zerobytelist = self._querydb(
                AnalysisQueries.SELECT_ZERO_BYTE_FILEPATHS, False, False, True
            )
        else:
            self.analysis_results.zerobytelist = None
        return self.analysis_results.zerobytecount

    def msoftfnameanalysis(self):
        namelist = self._querydb(AnalysisQueries.SELECT_FILENAMES)
        dirlist = self._querydb(AnalysisQueries.SELECT_DIRNAMES)

        charcheck = pathlesstaken.PathlesstakenAnalysis()

        self.rogue_names = []
        self.rogue_dirs = []

        namereport = []
        for name in namelist:
            try:
                namestring = "{}".format(name[0].decode("utf8"))
            except AttributeError:
                namestring = "{}".format(name[0])
            checkedname = charcheck.complete_file_name_analysis(namestring)
            if len(checkedname) > 0:
                namereport.append(checkedname)
                self.rogue_names.append(name[0])

        dirreport = []
        for dir_ in dirlist:
            try:
                dirstring = "{}".format(dir_[0].decode("utf8"))
            except AttributeError:
                dirstring = "{}".format(dir_[0])
            checkedname = charcheck.complete_file_name_analysis(dirstring, True)
            if len(checkedname) > 0:
                dirreport.append(checkedname)
                self.rogue_dirs.append(dir_[0])

        self.analysis_results.badFileNames = namereport
        self.analysis_results.badDirNames = dirreport

    def multiplecount(self, nscount):
        return self._querydb(self.query.count_multiple_ids(nscount), True, True)

    def multiple_id_paths(self, nscount, paths=True):
        return self._querydb(
            self.query.count_multiple_ids(nscount, paths), False, False, True
        )

    @staticmethod
    def _getsplit(vals):
        idlist = vals.split(",", 3)
        if len(idlist) == 4:
            type_ = idlist[1]
            idno = idlist[0]
            idrow = idlist[2]
            ns = idlist[3]
            return type_, idno, idrow, ns

    def create_id_breakdown(self):
        """Create a breakdown of IDs and methods. The breakdown is
        created (the opposite of) accumulativly, i.e. we start with all
        the data, and then slowly remove it from the sets based on the
        quality of identification. So, container, signature, xml, text,
        filename, extension... etc.

        End result is an array of tuples I think, but need to come back
        to this documentation to make that clearer...
        """

        tooltype = self.analysis_results.tooltype
        query = self.query.methods_return_ns_sort(self.priority_ns_id)
        allids = self._querydb(query)
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

        # create a set to remove the file ids with duplicate methods
        for id_ in allids:
            file = id_[0]
            method = id_[2].lower().strip()
            idrow = id_[1]
            ns = id_[3]
            method_data = "{},{},{},{}".format(file, method, idrow, ns)
            method_list.append(method_data)

        # go through list the first time and prioritize container and signature
        # and THEN our sorted list of NS identifiers...
        for id_ in list(method_list):
            type_, idno, idrow, ns = self._getsplit(id_)
            if type_ == "container":
                if idno not in container_bin:
                    container_bin.append(idno)
                    binaryidrows.append((idno, idrow))
            if type_ == "signature":
                if idno not in container_bin and idno not in binary_bin:
                    binary_bin.append(idno)
                    binaryidrows.append((idno, idrow))

        for id_ in list(method_list):
            type_, idno, idrow, ns = self._getsplit(id_)
            if type_ == "xml":
                if (
                    idno not in container_bin
                    and idno not in binary_bin
                    and idno not in xml_bin
                ):
                    xml_bin.append(idno)
                    xmlidrows.append((idno, idrow))

        for id_ in list(method_list):
            type_, idno, idrow, ns = self._getsplit(id_)
            if type_ == "text":
                if (
                    idno not in container_bin
                    and idno not in binary_bin
                    and idno not in xml_bin
                    and idno not in text_bin
                ):
                    text_bin.append(idno)
                    textidrows.append((idno, idrow))

        for id_ in list(method_list):
            type_, idno, idrow, ns = self._getsplit(id_)
            if type_ == "filename":
                if (
                    idno not in container_bin
                    and idno not in binary_bin
                    and idno not in xml_bin
                    and idno not in text_bin
                    and idno not in filename_bin
                ):
                    filename_bin.append(idno)
                    filenameidrows.append((idno, idrow))

        for id_ in list(method_list):
            type_, idno, idrow, ns = self._getsplit(id_)
            if type_ == "extension":
                if (
                    idno not in container_bin
                    and idno not in binary_bin
                    and idno not in xml_bin
                    and idno not in text_bin
                    and idno not in filename_bin
                    and idno not in extension_bin
                ):
                    extension_bin.append(idno)

        for id_ in list(method_list):
            type_, idno, idrow, ns = self._getsplit(id_)
            if type_ == "none":
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
        countlist = []
        methodresults = self._querydb(
            self.query.query_from_idrows(methodids, self.priority_ns_id)
        )

        for id_ in methodresults:
            ns_id = id_[5]
            name = id_[2]

            if name == "":
                name = ", "
            else:
                name = ", {}, ".format(name)

            basis = id_[3]
            if basis is not None:
                basis = "[{}]".format(basis)
            else:
                basis = ""

            if fmt_version is False:
                idval = "{}{}{}{} {} ({})".format(
                    id_[0], id_[1], name, id_[4], basis, id_[6]
                )
            else:
                idval = "{}{}{}{} ({})".format(id_[0], id_[1], name, id_[4], id_[6])
            countlist.append((idval, ns_id))

        # counter returns dict
        templist = Counter(countlist)

        countlist = []

        for k, v in templist.items():
            countlist.append((k[0], v, k[1]))  # add ns to sort by

        countlist = self._prioritysort(countlist)

        final_countlist = []
        for c in countlist:
            final_countlist.append((c[0], c[1]))

        return final_countlist

    def _prioritysort(self, method_list):
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

    def _split_match(self, match):
        """Return offset and number of sequences used from a Siegfried
        match.

            Examples:
                byte match at [[0 4] [30 19]] (signature 1/2) (2 seqs.)
                byte match at 0, 4 (1 seq.)
                byte match at 0, 4 (1 seq.)
                byte match at 0, 4 (signature 1/3) (1 seq.)
                byte match at [[0 4] [30 8] [38 19]] (signature 2/2) (3 seqs.)
                byte match at [[0 129] [149 56]] (2 seqs.)
                byte match at [[0 8] [2117 8]] (2 seqs.)

        :param match: match line from Siegfried (string)
        :return: offset, sequence_count (list, string)
        """
        SIG_MARKER = "(signature"
        if SIG_MARKER in match:
            match = match.split(SIG_MARKER, 1)[0]
        if "[[[" in match:
            # Canonical example is two brackets, below, so it
            # might be possible to deprecate this.
            return self._handle_match_with_square_brackets(match)
        if "[[" in match:
            # Example: byte match at [[0 16] [77 4] [45015 12]].
            return self._handle_match_with_square_brackets(match)
        return self._handle_match_without_brackets(match)

    @staticmethod
    def _update_stats(stat_list, file_id, match, file_name, file_size, bof_eof):
        """Update stats using indices."""
        stat_list[0] = file_id
        stat_list[1] = match.strip()
        stat_list[2] = file_name
        stat_list[3] = file_size
        stat_list[4] = bof_eof
        return stat_list

    def _get_bases(self, basis):
        """Process the output from the database with Siegfried basis
        results.

            Fields used below in bof_stats and eof_stats are:
                [
                    'id_',
                    'basis',
                    'filesize',
                    'filename',
                    'offset',
                ]
        """
        BYTE_MATCH = "byte match"
        # Stats lists maintain an accumulation of correct state as it is
        # extracted from the basis field returned by Siegfried.
        bof_stats = [None, "basis", "filename", "filesize", 0]
        eof_stats = [None, "basis", "filename", "filesize", 0]
        for idrow in basis:
            val = idrow[0].split(";")
            file_size = int(idrow[3])
            file_name = idrow[2]
            file_id = idrow[1]
            for match in val:
                if BYTE_MATCH not in match:
                    continue
                offs, sequence_count = self._split_match(match)
                try:
                    bof, eof, file_size = self._get_match_offsets(
                        offs, sequence_count, file_size
                    )
                except ValueError:
                    logging.error("Cannot handle basis: %s %s", offs, match)
                    continue
                if bof != 0 and bof > bof_stats[4]:
                    bof_stats = self._update_stats(
                        bof_stats, file_id, match.strip(), file_name, file_size, bof
                    )
                if eof is not None and eof > eof_stats[4]:
                    eof_stats = self._update_stats(
                        eof_stats, file_id, match.strip(), file_name, file_size, eof
                    )
        if bof_stats[0] is None:
            bof_stats = None
        if eof_stats[0] is None:
            eof_stats = None
        return bof_stats, eof_stats

    def _analysebasis(self):
        """Determine the longest distances scanned from the beginning
        and end of file in a Siegfried report.
        """
        basis = self._querydb(AnalysisQueries.SELECT_BYTE_MATCH_BASIS)
        return self._get_bases(basis)

    @staticmethod
    def _get_match_offsets(basis, sequence_count, file_size):
        """Return BOF and EOF values for a match's basis.

            Info to improve this moving forward:
                For a multi-byte sequence:
                    * File size: 348
                    * byte match at [[0 6] [346 2]]
                        - offset 1 = 0
                        - offset_match_length 1 = 6
                        - offset 2 = 346
                        - offset_match_length 2 = 2
                    * BOF read is 6 bytes from beginning: (0, 6).
                    * EOF read is 2 bytes from the end:
                        (2 bytes, from 346 out of 348).
                    * Return:
                        * BOF value: 6
                        * EOF value: 2

        :param basis: basis list (list)
        :param sequence_count: number of sequences (int)
        :param file_size: size of file analyzed (int)
        :return: BOF, EOF, file size
        """
        bof = 0
        eof = 0
        sequence_count = int(sequence_count)
        file_size = int(file_size)
        if sequence_count == 1:
            pos = int(basis[0])
            pos_len = int(basis[1])
            bof = pos + pos_len
            eof = file_size - pos
            return bof, None, file_size
        for _, sequence in enumerate(range(sequence_count)):
            try:
                offset = int(basis[sequence * 2])
                offset_match_length = int(basis[(sequence * 2) + 1])
            except IndexError:
                continue
            # Understand match sequence length relative to 0 bytes (BOF)
            # or EOF (file size) and use those values to try and create
            # the bounds for the file.
            tmp_bof = offset + offset_match_length
            tmp_eof = file_size - offset
            if tmp_bof < tmp_eof:
                bof = tmp_bof
            elif tmp_eof < tmp_bof:
                eof = tmp_eof
        return bof, eof, file_size

    @staticmethod
    def _handle_match_with_square_brackets(basis):
        """Split the match basis from Siegfried when there are square
        brackets to be dealt with.
        """
        BYTE_MATCH_AT = "byte match at"
        SIGNATURE = "signature"
        basis = basis.replace(BYTE_MATCH_AT, "").strip()
        # Number of sequences is the count of square brackets times two
        # to account for the two values offset, position.
        no_sequences = (basis.count("[") - 1) * 2
        basis = (basis.replace("[", "")).replace("]", "").replace(" ", ",")
        basis = basis.split(",", no_sequences)
        if SIGNATURE in basis[len(basis) - 1]:
            basis = basis[:-1]
        return basis, int(no_sequences / 2)

    @staticmethod
    def _handle_match_without_brackets(basis):
        basis = basis.replace("byte match at", "").strip()
        basis = basis.replace("(", ",(")
        basis = basis.replace(" ", "").split(",", 2)[:2]
        return basis, 1

    def getdenylistresults(self):
        """Generate results based on the denylist provided to the
        analysis.
        """
        dl = DenylistQueries()
        denylist = {}

        if self.denylist.get(HandleDenylist.IDS) is not None:
            q4 = dl.getids(self.denylist[HandleDenylist.IDS])
            ids = self._querydb(q4)
            if ids:
                for found in ids:
                    denylist[found[0]] = (HandleDenylist.IDS, found[2].strip())

        if self.denylist.get(HandleDenylist.EXTENSIONS) is not None:
            q3 = dl.getexts(self.denylist[HandleDenylist.EXTENSIONS])
            extensions = self._querydb(q3)
            if extensions:
                for found in extensions:
                    if found[0] not in list(denylist.keys()):
                        denylist[found[0]] = (HandleDenylist.EXTENSIONS, found[2])

        if self.denylist.get(HandleDenylist.FILENAMES) is not None:
            q1 = dl.getfilenames(self.denylist[HandleDenylist.FILENAMES])
            filenames = self._querydb(q1)
            if filenames:
                for found in filenames:
                    if found[0] not in list(denylist.keys()):
                        denylist[found[0]] = (HandleDenylist.FILENAMES, found[1])

        if self.denylist.get(HandleDenylist.DIRECTORIES) is not None:
            q2 = dl.getdirnames(self.denylist[HandleDenylist.DIRECTORIES])
            directories = self._querydb(q2)
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
        self.hashtype = self._querydb(AnalysisQueries.SELECT_HASH, True)[0]
        if self.hashtype == "None" or self.hashtype == "False":
            logging.info(AnalysisQueries.ERROR_NOHASH)
            self.analysis_results.hashused = False
        else:
            self.analysis_results.hashused = True

        self.analysis_results.collectionsize = self._querydb(
            AnalysisQueries.SELECT_COLLECTION_SIZE, True, True
        )
        self.analysis_results.filecount = self._querydb(
            AnalysisQueries.SELECT_COUNT_FILES, True, True
        )
        self.analysis_results.containercount = self._querydb(
            AnalysisQueries.SELECT_COUNT_CONTAINERS, True, True
        )
        self.analysis_results.filesincontainercount = self._querydb(
            AnalysisQueries.SELECT_COUNT_FILES_IN_CONTAINERS, True, True
        )
        self.analysis_results.directoryCount = self._querydb(
            AnalysisQueries.SELECT_COUNT_FOLDERS, True, True
        )

        # not necessarily used in the output
        self.analysis_results.uniqueFileNames = self._querydb(
            AnalysisQueries.SELECT_COUNT_UNIQUE_FILENAMES, True, True
        )
        self.analysis_results.uniqueDirectoryNames = (
            self._querydb(AnalysisQueries.SELECT_COUNT_UNIQUE_DIRNAMES, True, True)
            - self.NONROOTBASEDIR
        )

        # ------------WHAT IS AND ISN'T IDENTIFIED SUMMARY------------#
        self.create_id_breakdown()
        # ------------WHAT IS AND ISN'T IDENTIFIED SUMMARY------------#

        self.analysis_results.extmismatchCount = self._querydb(
            AnalysisQueries.SELECT_COUNT_EXT_MISMATCHES, True, True
        )
        self.analysis_results.distinctSignaturePuidcount = self._querydb(
            AnalysisQueries.SELECT_COUNT_FORMAT_COUNT, True, True
        )

        if self.analysis_results.tooltype != "droid":
            self.analysis_results.distinctOtherIdentifiers = self._querydb(
                AnalysisQueries.SELECT_COUNT_OTHER_FORMAT_COUNT, True, True
            )
            self.analysis_results.distinctXMLIdentifiers = self._querydb(
                self.query.select_count_identifiers("XML"), True, True
            )
            self.analysis_results.distinctTextIdentifiers = self._querydb(
                self.query.select_count_identifiers("Text"), True, True
            )
            self.analysis_results.distinctFilenameIdentifiers = self._querydb(
                self.query.select_count_identifiers("Filename"), True, True
            )

            self.analysis_results.xml_identifiers = self._querydb(
                self.query.select_frequency_identifier_types("XML")
            )
            self.analysis_results.text_identifiers = self._querydb(
                self.query.select_frequency_identifier_types("Text")
            )
            self.analysis_results.filename_identifiers = self._querydb(
                self.query.select_frequency_identifier_types("Filename")
            )

        self.analysis_results.distinctextensioncount = self._querydb(
            AnalysisQueries.SELECT_COUNT_EXTENSION_RANGE, True, True
        )

        mimeids = self.binaryIDs + self.xmlIDs + self.textIDs
        self.analysis_results.mimetypeFrequency = self._querydb(
            self.query.getmimes(mimeids)
        )

        # NOTE: Must be calculated after we have total, and subset values
        self.analysis_results.identifiedPercentage = self.calculatePercent(
            self.analysis_results.filecount, self.analysis_results.identifiedfilecount
        )
        self.analysis_results.unidentifiedPercentage = self.calculatePercent(
            self.analysis_results.filecount, self.analysis_results.unidentifiedfilecount
        )

        self.analysis_results.dateFrequency = self._querydb(
            AnalysisQueries.SELECT_YEAR_FREQUENCY_COUNT
        )

        self.analysis_results.signatureidentifiedfrequency = self._querydb(
            AnalysisQueries.SELECT_BINARY_MATCH_COUNT
        )
        self.analysis_results.extensionOnlyIDList = self._querydb(
            AnalysisQueries.SELECT_PUIDS_EXTENSION_ONLY
        )
        self.analysis_results.multipleidentificationcount = self.multiplecount(
            self.analysis_results.namespacecount
        )

        # most complicated way to retrieve extension only PUIDs
        if len(self.extensionIDonly) > 0:
            extid = self.query.query_from_ids(self.extensionIDonly, "Extension")
            test = self._querydb(extid)
            combined_list = []
            for entry in test:
                entry = " ".join(entry)
                combined_list.append(entry)
            sorted_list = Counter(elem for elem in combined_list).most_common()
            self.analysis_results.extensionOnlyIDFrequency = sorted_list

        # OKAY stat...
        self.analysis_results.uniqueExtensionsInCollectionList = self._querydb(
            AnalysisQueries.SELECT_ALL_UNIQUE_EXTENSIONS
        )
        self.analysis_results.frequencyOfAllExtensions = self._querydb(
            AnalysisQueries.SELECT_COUNT_EXTENSION_FREQUENCY
        )

        # Additional useful queries...
        self.analysis_results.containertypeslist = self._querydb(
            AnalysisQueries.SELECT_CONTAINER_TYPES
        )

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
            ) = self._analysebasis()
            self.analysis_results.errorlist = self._querydb(
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
                    idslist = idslist + self._querydb(
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
                self.analysis_results.rogue_multiple_identification_list = (
                    self.multiple_id_paths(self.analysis_results.namespacecount)
                )

            if self.rogueanalysis:
                self._handle_rogue_analysis()

        return self.analysis_results

    def _handle_rogue_analysis(self):
        """Gather all the information needed to output a rogues or
        heroes listing as requested by the caller.
        """
        rogue_queries = RogueQueries()
        self.analysis_results.rogue_all_paths = self._querydb(
            rogue_queries.SELECT_ALL_FILEPATHS,
            fetchone=False,
            numberquery=False,
            tolist=True,
        )
        self.analysis_results.rogue_all_dirs = self._querydb(
            rogue_queries.SELECT_ALL_FOLDERS,
            fetchone=False,
            numberquery=False,
            tolist=True,
        )
        self.analysis_results.rogue_extension_mismatches = self._querydb(
            rogue_queries.SELECT_EXTENSION_MISMATCHES,
            fetchone=False,
            numberquery=False,
            tolist=True,
        )
        # TODO: This piece of code is either too complex, or not documented
        # well enough. Handling of unidentified files gets difficult when not
        # using PRONOM/DROID anyway. And get more complicated when using more
        # than one namespace. I'd like to see this refined, made easier to
        # read.
        if self.analysis_results.tooltype == "droid":
            self.pronom_ns_id = 1
        if self.pronom_ns_id is not None:
            self.analysis_results.rogue_pronom_ns_id = self.pronom_ns_id
            self.analysis_results.rogue_identified_pronom = self._querydb(
                rogue_queries.get_pronom_identified_files(self.pronom_ns_id),
                fetchone=False,
                numberquery=False,
                tolist=True,
            )
        else:
            self.analysis_results.rogue_identified_all = self._querydb(
                rogue_queries.get_all_non_ids(
                    self.analysis_results.rogue_identified_all
                ),
                fetchone=False,
                numberquery=False,
                tolist=True,
            )
        self.analysis_results.rogue_file_name_paths = self._querydb(
            rogue_queries.get_rogue_name_paths(self.rogue_names),
            fetchone=False,
            numberquery=False,
            tolist=True,
        )
        if len(self.rogue_dirs) > 0:
            self.analysis_results.rogue_dir_name_paths = self._querydb(
                rogue_queries.get_rogue_dir_paths(self.rogue_dirs),
                fetchone=False,
                numberquery=False,
                tolist=True,
            )

    def get_namespace_data_list(self):
        """Retrieve information about namespaces."""
        nsdatalist = []
        for ns in self.namespacedata:
            nsdict = {}
            nsid = ns[0]
            nsdict[self.NS_CONST_TITLE] = ns[1]
            nsdict[self.NS_CONST_DETAILS] = ns[2]
            nsdict[self.NS_CONST_BINARY_COUNT] = self._querydb(
                self.query.get_ns_methods(nsid), True, True
            )
            nsdict[self.NS_CONST_XML_COUNT] = self._querydb(
                self.query.get_ns_methods(nsid, False, "XML"), True, True
            )
            nsdict[self.NS_CONST_TEXT_COUNT] = self._querydb(
                self.query.get_ns_methods(nsid, False, "Text"), True, True
            )
            nsdict[self.NS_CONST_FILENAME_COUNT] = self._querydb(
                self.query.get_ns_methods(nsid, False, "Filename"), True, True
            )
            nsdict[self.NS_CONST_EXTENSION_COUNT] = self._querydb(
                self.query.get_ns_methods(nsid, False, "Extension"), True, True
            )
            nsdict[self.NS_CONST_MULTIPLE_IDS] = self._querydb(
                self.query.get_ns_multiple_ids(nsid), True, True
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
        logging.info("Running analysis, Rogues or Heroes: %s", analyze_rogues)
        self.rogueanalysis = analyze_rogues
        return self.queryDB()
