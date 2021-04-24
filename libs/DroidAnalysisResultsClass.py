# -*- coding: utf-8 -*-
from __future__ import absolute_import

from libs.version import AnalysisVersion


class DROIDAnalysisResults:

    # version
    version = 0

    # filename
    filename = ""

    # hashused
    hashused = False

    # tooltype
    tooltype = None

    # blacklist
    blacklist = False
    blacklist_filenames = []
    blacklist_directories = []
    blacklist_ids = []
    blacklist_exts = []

    # Counts
    collectionsize = 0
    filecount = 0
    containercount = 0
    filesincontainercount = 0
    directoryCount = 0
    uniqueFileNames = 0
    uniqueDirectoryNames = 0
    identifiedfilecount = 0
    multipleidentificationcount = 0
    unidentifiedfilecount = 0
    distinctSignaturePuidcount = 0
    extensionIDOnlyCount = 0
    distinctextensioncount = 0
    zeroidcount = 0

    # SF ONLY
    xmlidfilecount = 0
    textidfilecount = 0
    filenameidfilecount = 0
    distinctOtherIdentifiers = 0
    distinctXMLIdentifiers = 0
    distinctTextIdentifiers = 0
    distinctFilenameIdentifiers = 0
    textidentifiers = None
    filenameidentifiers = None
    binaryidentifiers = None
    xmlidentifiers = None
    bof_distance = None
    eof_distance = None
    namespacecount = None
    namespacedata = None
    nsdatalist = None
    identificationgaps = None
    errorlist = None
    xml_identifiers = None
    text_identifiers = None
    filename_identifiers = None
    # SF ONLY

    extmismatchCount = 0

    unidentifiedPercentage = 0
    identifiedPercentage = 0

    signatureidentifiers = None
    signatureidentifiedfrequency = None

    dateFrequency = None

    extensionOnlyIDFrequency = 0
    extensionOnlyIDList = []

    # TODO: Turn lists into lists? Formatting at end..?
    uniqueExtensionsInCollectionList = None
    frequencyOfAllExtensions = None

    idmethodFrequency = None

    mimetypeFrequency = None

    topPUIDList = None
    topExtensionList = None

    totalmd5duplicates = 0
    duplicatemd5listing = []
    duplicatemd5altlisting = []

    totaluniquefilenames = 0
    duplicatefnamelisting = []
    duplicatefnamealtlisting = []

    containertypeslist = None

    duplicatespathlist = []

    zerobytecount = 0
    zerobytelist = None

    multiplespacelist = ""
    badFileNames = None
    badDirNames = None

    duplicateHASHlisting = None
    totalHASHduplicates = None

    # rogues
    rogue_pronom_ns_id = None
    rogue_all_paths = None
    rogue_all_dirs = None
    rogue_blacklist = []
    rogue_duplicates = []
    rogue_identified_all = []
    rogue_identified_pronom = []
    rogue_extension_mismatches = []
    rogue_multiple_identification_list = []
    rogue_file_name_paths = []  # non-ascii file names
    rogue_dir_name_paths = []  # non-ascii dir names

    def __version__(self):
        v = AnalysisVersion()
        self.version = v.getVersion()
        return self.version
