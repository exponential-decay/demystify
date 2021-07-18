# -*- coding: utf-8 -*-

from __future__ import absolute_import

from libs.version import AnalysisVersion


class DROIDAnalysisResults:
    def __init__(self):

        # version
        self.version = 0

        # filename
        self.filename = ""

        # hashused
        self.hashused = False

        # tooltype
        self.tooltype = None

        # blacklist
        self.blacklist = False
        self.blacklist_filenames = []
        self.blacklist_directories = []
        self.blacklist_ids = []
        self.blacklist_exts = []

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

        # SF ONLY
        self.xmlidfilecount = 0
        self.textidfilecount = 0
        self.filenameidfilecount = 0
        self.distinctOtherIdentifiers = 0
        self.distinctXMLIdentifiers = 0
        self.distinctTextIdentifiers = 0
        self.distinctFilenameIdentifiers = 0
        self.textidentifiers = None
        self.filenameidentifiers = None
        self.binaryidentifiers = None
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

        # SF ONLY
        self.extmismatchCount = 0

        self.unidentifiedPercentage = 0
        self.identifiedPercentage = 0

        self.signatureidentifiers = None
        self.signatureidentifiedfrequency = None

        self.dateFrequency = None

        self.extensionOnlyIDFrequency = 0
        self.extensionOnlyIDList = []

        # TODO: Turn lists into lists? Formatting at end..?
        self.uniqueExtensionsInCollectionList = None
        self.frequencyOfAllExtensions = None

        self.idmethodFrequency = None

        self.mimetypeFrequency = None

        self.topPUIDList = None
        self.topExtensionList = None

        self.totalmd5duplicates = 0
        self.duplicatemd5listing = []
        self.duplicatemd5altlisting = []

        self.totaluniquefilenames = 0
        self.duplicatefnamelisting = []
        self.duplicatefnamealtlisting = []

        self.containertypeslist = None

        self.duplicatespathlist = []

        self.zerobytecount = 0
        self.zerobytelist = None

        self.multiplespacelist = ""
        self.badFileNames = None
        self.badDirNames = None

        self.duplicateHASHlisting = None
        self.totalHASHduplicates = None

        # rogues
        self.rogue_pronom_ns_id = None
        self.rogue_all_paths = None
        self.rogue_all_dirs = None
        self.rogue_blacklist = []
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
