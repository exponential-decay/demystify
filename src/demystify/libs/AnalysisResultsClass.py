# -*- coding: utf-8 -*-

"""Analysis results module."""

from .version import AnalysisVersion


class AnalysisResults:
    """Analysis results object to hold the output of Demystify before
    a caller maps it to a suitable output format, e.g. HTML, Text.
    """

    def __init__(self):

        self.version = 0
        self.filename = ""
        self.tooltype = None

        # Denylist.
        self.denylist = None
        self.denylist_filenames = []
        self.denylist_directories = []
        self.denylist_ids = []
        self.denylist_exts = []

        # Counts
        self.collectionsize = 0
        self.filecount = 0
        self.containercount = 0
        self.filesincontainercount = 0
        self.directoryCount = 0
        self.uniqueFileNames = 0
        self.uniqueDirectoryNames = 0
        self.identifiedfilecount = 0
        self.multipleidentificationcount = 0
        self.unidentifiedfilecount = 0
        self.distinctSignaturePuidcount = 0
        self.extensionIDOnlyCount = 0
        self.distinctextensioncount = 0
        self.zeroidcount = 0

        # Histogram of identifiers returned in the report with concrete,
        # Binary or Container IDs.
        self.binaryidentifiers = None

        # Siegfried only. Rely on capabilities in Siegfried only.
        self.xmlidfilecount = 0
        self.textidfilecount = 0
        self.filenameidfilecount = 0
        self.distinctOtherIdentifiers = 0
        self.distinctXMLIdentifiers = 0
        self.distinctTextIdentifiers = 0
        self.distinctFilenameIdentifiers = 0
        self.textidentifiers = None
        self.filenameidentifiers = None
        self.xmlidentifiers = None
        self.bof_distance = None
        self.eof_distance = None
        self.namespacecount = None
        self.namespacedata = None
        self.nsdatalist = None
        self.identificationgaps = None
        self.errorlist = None
        self.xml_identifiers = None
        self.text_identifiers = None
        self.filename_identifiers = None

        # Not Siegfried only. Additional statistics that work across
        # identifiers.
        self.extmismatchCount = 0

        self.unidentifiedPercentage = 0
        self.identifiedPercentage = 0

        self.signatureidentifiers = None
        self.signatureidentifiedfrequency = None

        self.dateFrequency = None

        self.extensionOnlyIDFrequency = 0
        self.extensionOnlyIDList = []

        self.uniqueExtensionsInCollectionList = None
        self.frequencyOfAllExtensions = None

        self.idmethodFrequency = None

        self.mimetypeFrequency = None

        self.containertypeslist = None

        self.duplicatespathlist = []

        self.zerobytecount = 0
        self.zerobytelist = None

        self.badFileNames = None
        self.badDirNames = None

        # Hash related values.
        self.hashused = False
        self.duplicateHASHlisting = None
        self.totalHASHduplicates = None

        # Rogue related values.
        self.rogue_pronom_ns_id = None
        self.rogue_all_paths = None
        self.rogue_all_dirs = None
        self.rogue_denylist = []
        self.rogue_duplicates = []
        self.rogue_identified_all = []
        self.rogue_identified_pronom = []
        self.rogue_extension_mismatches = []
        self.rogue_multiple_identification_list = []
        self.rogue_file_name_paths = []  # non-ascii file names
        self.rogue_dir_name_paths = []  # non-ascii dir names

    def __version__(self):
        v = AnalysisVersion()
        self.version = v.getVersion()
        return self.version
