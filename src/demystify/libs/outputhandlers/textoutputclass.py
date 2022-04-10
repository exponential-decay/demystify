# -*- coding: utf-8 -*-

# pylint: disable=W1633

import logging
import re

try:
    from src.demystify.i18n.internationalstrings import AnalysisStringsEN as IN_EN
    from src.demystify.libs import DemystifyAnalysisClass
except ModuleNotFoundError:
    # Needed to run from root dir.
    from demystify.i18n.internationalstrings import AnalysisStringsEN as IN_EN
    from demystify.libs import DemystifyAnalysisClass

# NONE_REPLACE_DEBUG is a logging prompt to help us to understand what
# needs changing around 'None'/null values from the database. These
# values are driven by the report, and standard handling in sqlitefid.
# E.g. if there is no version associated with a format, its version is
# None. This should be fixed in the data structures used to output the
# text, or in the database queries, not the presentation layer (arguably).
NONE_REPLACE_DEBUG = "Replacing 'None': A field in the database is null because there is no data, replacing at the presentation later..."


class FormatAnalysisTextOutput:
    """Object to help encapsulate text only output functions."""

    textoutput = ""

    def __init__(self, analysis_results):
        self.STRINGS = IN_EN
        self.analysis_results = analysis_results

    @staticmethod
    def _output_list(title, value):
        ret = "{}: {}".format(title, value)
        return ret

    @staticmethod
    def _itemlist(list_):
        output = ""
        for item in list_:
            "{}{}\n".format(output, item)
        return output.strip("\n")

    def _printNewline(self):
        self.printFormattedText("\n")

    def _output_list_title(self, title):
        self._printNewline()
        self.printFormattedText("{}:".format(title))

    @staticmethod
    def splitidresults(puid):
        identifier = puid[0].rsplit("(", 1)[0]
        namespace = puid[0].split(" ", 1)[0]
        patt = re.compile("(x-)?fmt\\/[0-9]+")  # noqa
        p = re.search(patt, identifier)
        if p is not None:
            p = p.span()
            identifier = identifier[p[0] : p[1]]
        else:
            identifier = identifier.replace(namespace, "").strip()
            identifier = identifier.split(",", 1)[0]
        count = puid[0].rsplit("(", 1)[1].replace(")", "")
        if ", None" in puid[0]:
            logging.debug(NONE_REPLACE_DEBUG)
        logging.debug(NONE_REPLACE_DEBUG)
        # 'None' is usually driven by the database. If there is a format
        # called "None" it will erroneously replace the name of that.
        # Usually, version will be replaced below as formats don't all
        # have versions. This should be fixed at the the data layer.
        formatname = (
            puid[0]
            .replace(namespace, "")
            .replace("({})".format(count), "")
            .replace("{}, ".format(identifier), "")
            .replace(", None", "")
            .strip(", ")
        )
        if formatname == "":
            formatname = identifier
        return namespace, identifier, formatname, count

    def printFormattedText(self, string, newline=True):
        line_end = ""
        if newline:
            line_end = "\n"
        try:
            string = "{}".format(string)
        except UnicodeEncodeError:
            string = "{}".format(string.encode("utf8"))
        self.textoutput = "{}{}{}".format(self.textoutput, string, line_end)

    def printTextResults(self):
        self.generateTEXT()
        return self.textoutput

    @staticmethod
    def _frequencyoutput(itemlist, zeros=False):
        val = ""
        if not isinstance(itemlist, list):
            logging.error("Not sending a list to a function wanting a list")
        else:
            for item in itemlist:
                if zeros is True:
                    val = "{}{}, ".format(val, item[0])
                else:
                    val = "{}{} ({}), ".format(val, item[0], item[1])
            val = val.strip(", ")

        return val

    @staticmethod
    def _aggregatelists(itemlist):
        outstr = ""
        if not isinstance(itemlist, list):
            logging.error("Not sending a list to a function wanting a list.")
        else:
            for item in itemlist:
                name = item[0]
                if item[1] is not None:
                    count = "({})".format(item[1])
                    outstr = "{}{} {}\n".format(outstr, name, count)
                else:
                    outstr = "{}{}\n".format(outstr, name)
        return outstr.strip("\n")

    def getDateList(self):
        if self.analysis_results.dateFrequency is not None:
            return self._frequencyoutput(self.analysis_results.dateFrequency)

    @staticmethod
    def _outputdupes(list_):
        output = ""
        for dupes in list_:
            output = "{}Checksum: {}\n".format(output, dupes["checksum"])
            output = "{}Count: {}\n".format(output, dupes["count"])
            output = "{}Example: {}\n\n".format(output, dupes["examples"][0])
        return output.strip("\n")

    def _handlenamespacestats(self, nsdatalist, signaturefrequency):
        """Output statistics about namespace.

        e.g.{
                'binary method count': '57',
                'text method count': '37',
                'namespace title':
                'freedesktop.org',
                'filename method count': '45',
                'namespace details': 'freedesktop.org.xml',
            }
        """
        demystify = DemystifyAnalysisClass.DemystifyBase()
        output = ""
        for ns in nsdatalist:
            signatureids = signaturefrequency
            nstitle = ns[demystify.NS_CONST_TITLE]
            identified = ns[demystify.NS_CONST_BINARY_COUNT]
            xmlid = ns[demystify.NS_CONST_XML_COUNT]
            text = ns[demystify.NS_CONST_TEXT_COUNT]
            filename = ns[demystify.NS_CONST_FILENAME_COUNT]
            ext = ns[demystify.NS_CONST_EXTENSION_COUNT]
            unidentified = self.analysis_results.filecount - identified
            percent_not = demystify.calculatePercent(
                self.analysis_results.filecount, unidentified
            )
            percent_ok = demystify.calculatePercent(
                self.analysis_results.filecount, identified
            )
            output = "{}{}: {} ({})\n".format(
                output,
                self.STRINGS.HEADING_NAMESPACE,
                nstitle,
                ns[demystify.NS_CONST_DETAILS],
            )
            output = "{}{}: {}\n".format(
                output, self.STRINGS.SUMMARY_IDENTIFIED_FILES, identified
            )
            output = "{}{}: {}\n".format(
                output,
                self.STRINGS.SUMMARY_MULTIPLE,
                ns[demystify.NS_CONST_MULTIPLE_IDS],
            )
            output = "{}{}: {}\n".format(
                output, self.STRINGS.SUMMARY_UNIDENTIFIED, unidentified
            )
            output = "{}{}: {}\n".format(output, self.STRINGS.SUMMARY_EXTENSION_ID, ext)
            if self.analysis_results.tooltype != "droid":
                output = "{}{}: {}\n".format(output, self.STRINGS.SUMMARY_XML_ID, xmlid)
                output = "{}{}: {}\n".format(output, self.STRINGS.SUMMARY_TEXT_ID, text)
                output = "{}{}: {}\n".format(
                    output, self.STRINGS.SUMMARY_FILENAME_ID, str(filename)
                )
            output = "{}{}: {}\n".format(
                output, self.STRINGS.SUMMARY_PERCENTAGE_IDENTIFIED, percent_ok
            )
            output = "{}{}: {}\n".format(
                output, self.STRINGS.SUMMARY_PERCENTAGE_UNIDENTIFIED, percent_not
            )
            output = "{}\n".format(output)
            output = "{}{}\n".format(
                output, self.STRINGS.HEADING_FREQUENCY_PUIDS_IDENTIFIED
            )
            for idrow in signatureids:
                if idrow[0] == nstitle:
                    output = "{}{} ({}), ".format(output, idrow[1], idrow[2])
            output = output.strip(", ")
            output = "{}\n\n".format(output)
        return output.strip("\n")

    @staticmethod
    def _generateOffsetText(offsettext):
        offs = offsettext
        if offs is not None:
            ret = "{}, {} e.g. {} filesize: {}, {} bytes".format(
                offs[0], offs[1], offs[2], offs[3], offs[4]
            )
            return ret
        return None

    @staticmethod
    def _remove_version_if_none(identifier_list):
        """Versions that are None are not presented very nicely in the
        report. While this should be fixed at the data layer, we can
        also fix it with this helper.
        """
        NONE_STR = ", None"
        new_list = []
        for item in identifier_list:
            if NONE_STR in item[0]:
                new_list.append((item[0].replace(NONE_STR, "", 2), item[1]))
            else:
                new_list.append(item)
        return new_list

    @staticmethod
    def _removenamespaceid(oldlist):
        newlist = []
        for item in oldlist:
            newlist.append((str(item[0]), None))
        return newlist

    @staticmethod
    def _separated_text(t1, t2):
        """Concatenate two strings with a colon in listings."""
        return "{}: {}".format(t1, t2)

    def generateTEXT(self):
        if self.analysis_results.tooltype != "droid":
            self.printFormattedText(self.STRINGS.REPORT_TITLE_SF)
        else:
            self.printFormattedText(self.STRINGS.REPORT_TITLE_DR)

        # Output common list details, e.g. analysis version.
        ver = self._separated_text(
            self.STRINGS.REPORT_VERSION, self.analysis_results.__version__()
        )
        self.printFormattedText(ver)
        filename = self._separated_text(
            self.STRINGS.REPORT_FILE, self.analysis_results.filename
        )
        self.printFormattedText(filename)
        tool_type = self._separated_text(
            self.STRINGS.REPORT_TOOL, self.analysis_results.tooltype
        )
        self.printFormattedText(tool_type)
        self.printFormattedText("")
        namespace_count = self._separated_text(
            self.STRINGS.NAMESPACES, self.analysis_results.namespacecount
        )
        self.printFormattedText(namespace_count)

        bof = self._separated_text(
            self.STRINGS.SUMMARY_DISTANCE_BOF,
            self._generateOffsetText(self.analysis_results.bof_distance),
        )
        if self.analysis_results.bof_distance is not None:
            self.printFormattedText(bof)

        eof = self._separated_text(
            self.STRINGS.SUMMARY_DISTANCE_EOF,
            self._generateOffsetText(self.analysis_results.eof_distance),
        )
        if self.analysis_results.eof_distance is not None:
            self.printFormattedText(eof)

        self.printFormattedText("")
        self.printFormattedText(
            self._output_list(
                self.STRINGS.SUMMARY_TOTAL_FILES, self.analysis_results.filecount
            )
        )
        self.printFormattedText(
            self._output_list(
                self.STRINGS.SUMMARY_ARCHIVE_FILES, self.analysis_results.containercount
            )
        )

        # even if we have archive files, if the analysis isn't on, we can't output this value
        if self.analysis_results.filesincontainercount > 0:
            self.printFormattedText(
                self._output_list(
                    self.STRINGS.SUMMARY_INSIDE_ARCHIVES,
                    self.analysis_results.filesincontainercount,
                )
            )

        self.printFormattedText(
            self._output_list(
                self.STRINGS.SUMMARY_DIRECTORIES, self.analysis_results.directoryCount
            )
        )
        self.printFormattedText(
            self._output_list(
                self.STRINGS.SUMMARY_UNIQUE_DIRNAMES,
                self.analysis_results.uniqueDirectoryNames,
            )
        )
        self.printFormattedText(
            self._output_list(
                self.STRINGS.SUMMARY_IDENTIFIED_FILES,
                self.analysis_results.identifiedfilecount,
            )
        )
        self.printFormattedText(
            self._output_list(
                self.STRINGS.SUMMARY_MULTIPLE,
                self.analysis_results.multipleidentificationcount,
            )
        )
        self.printFormattedText(
            self._output_list(
                self.STRINGS.SUMMARY_UNIDENTIFIED,
                self.analysis_results.unidentifiedfilecount,
            )
        )

        if self.analysis_results.tooltype != "droid":
            self.printFormattedText(
                self._output_list(
                    self.STRINGS.SUMMARY_XML_ID, self.analysis_results.xmlidfilecount
                )
            )
            self.printFormattedText(
                self._output_list(
                    self.STRINGS.SUMMARY_TEXT_ID, self.analysis_results.textidfilecount
                )
            )
            self.printFormattedText(
                self._output_list(
                    self.STRINGS.SUMMARY_FILENAME_ID,
                    self.analysis_results.filenameidfilecount,
                )
            )

        self.printFormattedText(
            self._output_list(
                self.STRINGS.SUMMARY_EXTENSION_ID,
                self.analysis_results.extensionIDOnlyCount,
            )
        )
        self.printFormattedText(
            self._output_list(
                self.STRINGS.SUMMARY_EXTENSION_MISMATCH,
                self.analysis_results.extmismatchCount,
            )
        )
        self.printFormattedText(
            self._output_list(
                self.STRINGS.SUMMARY_ID_PUID_COUNT,
                self.analysis_results.distinctSignaturePuidcount,
            )
        )

        if self.analysis_results.tooltype != "droid":
            self.printFormattedText(
                self._output_list(
                    self.STRINGS.SUMMARY_OTHER_ID_COUNT,
                    self.analysis_results.distinctOtherIdentifiers,
                )
            )
            self.printFormattedText(
                self._output_list(
                    self.STRINGS.SUMMARY_XML_ID_COUNT,
                    self.analysis_results.distinctXMLIdentifiers,
                )
            )
            self.printFormattedText(
                self._output_list(
                    self.STRINGS.SUMMARY_TEXT_ID_COUNT,
                    self.analysis_results.distinctTextIdentifiers,
                )
            )
            self.printFormattedText(
                self._output_list(
                    self.STRINGS.SUMMARY_FILENAME_ID_COUNT,
                    self.analysis_results.distinctFilenameIdentifiers,
                )
            )

        self.printFormattedText(
            self._output_list(
                self.STRINGS.SUMMARY_UNIQUE_EXTENSIONS,
                self.analysis_results.distinctextensioncount,
            )
        )
        self.printFormattedText(
            self._output_list(
                self.STRINGS.SUMMARY_ZERO_BYTE, self.analysis_results.zerobytecount
            )
        )

        if self.analysis_results.hashused > 0:
            self.printFormattedText(
                self._output_list(
                    self.STRINGS.SUMMARY_IDENTICAL_FILES,
                    self.analysis_results.totalHASHduplicates,
                )
            )

        self.printFormattedText(
            self._output_list(
                self.STRINGS.SUMMARY_PERCENTAGE_IDENTIFIED,
                self.analysis_results.identifiedPercentage,
            )
        )
        self.printFormattedText(
            self._output_list(
                self.STRINGS.SUMMARY_PERCENTAGE_UNIDENTIFIED,
                self.analysis_results.unidentifiedPercentage,
            )
        )

        if (
            self.analysis_results.namespacecount > 1
            and self.analysis_results.identificationgaps is not None
        ):
            self.printFormattedText(
                self._output_list(
                    self.STRINGS.SUMMARY_GAPS_COVERED,
                    self.analysis_results.identificationgaps,
                )
            )

        # Print out the size of the collection.
        size = self.analysis_results.collectionsize  # easier to reference from a var
        size_text = "{}: {} bytes | {} MiB/MB (Megabytes)".format(
            self.STRINGS.HEADING_SIZE,
            float(size),
            str(round(float(float(size) / (1048576)), 1)),
        )
        self.printFormattedText(size_text)  # MiB/MB = (2^1024)*2

        signature_id_list = []
        if self.analysis_results.signatureidentifiers is not None:
            countlist = []
            for puid in self.analysis_results.signatureidentifiers:
                namespace, identifier, formatname, count = self.splitidresults(puid)
                countlist.append((identifier, int(count)))
                signature_id_list.append(
                    (namespace, identifier, formatname, int(count))
                )

        if self.analysis_results.signatureidentifiers is not None:
            self._output_list_title(self.STRINGS.HEADING_AGGREGATE_BINARY_IDENTIFIED)
            signature_id_list.sort(key=lambda keys: int(keys[3]), reverse=True)
            for id_ in signature_id_list:
                identifier = "{}, {}, {} ({})".format(id_[0], id_[1], id_[2], id_[3])
                # Replacing ", None" here should be safe as it only affects
                # the identifier field, not 'any' text output.
                NONE_STR = ", None"
                if NONE_STR in identifier:
                    logging.debug(NONE_REPLACE_DEBUG)
                    identifier = identifier.replace(NONE_STR, "")
                self.printFormattedText(identifier)

        if self.analysis_results.binaryidentifiers is not None:
            new_list = self._remove_version_if_none(
                self.analysis_results.binaryidentifiers
            )
            new_list = self._removenamespaceid(new_list)
            self.printFormattedText(self._aggregatelists(new_list))

        if self.analysis_results.xmlidentifiers is not None:
            self._output_list_title(self.STRINGS.HEADING_XML_ID)
            new_list = self._remove_version_if_none(
                self.analysis_results.xmlidentifiers
            )
            new_list = self._removenamespaceid(new_list)
            self.printFormattedText(self._aggregatelists(new_list))
        if self.analysis_results.textidentifiers is not None:
            self._output_list_title(self.STRINGS.HEADING_TEXT_ID)
            new_list = self._remove_version_if_none(
                self.analysis_results.textidentifiers
            )
            new_list = self._removenamespaceid(new_list)
            self.printFormattedText(self._aggregatelists(new_list))
        if self.analysis_results.filenameidentifiers is not None:
            self._output_list_title(self.STRINGS.HEADING_FILENAME_ID)
            new_list = self._remove_version_if_none(
                self.analysis_results.filenameidentifiers
            )
            new_list = self._removenamespaceid(new_list)
            self.printFormattedText(self._aggregatelists(new_list))

        if self.analysis_results.extensionIDOnlyCount > 0:
            if self.analysis_results.extensionOnlyIDList is not None:
                if len(self.analysis_results.extensionOnlyIDList) > 0:
                    self._output_list_title(self.STRINGS.HEADING_EXTENSION_ONLY)
                    for item in self.analysis_results.extensionOnlyIDList:
                        if item[1] == "None":
                            output = "{}".format(item[0])
                        else:
                            output = "{}, {}".format(item[0], item[1])
                        self.printFormattedText(output)

        dates = self.getDateList()
        if dates is not None:
            self._output_list_title(self.STRINGS.HEADING_DATE_RANGE)
            self.printFormattedText(dates)

        if self.analysis_results.idmethodFrequency is not None:
            self._output_list_title(self.STRINGS.HEADING_ID_METHOD)
            id_method_frequency = self._frequencyoutput(
                self.analysis_results.idmethodFrequency
            )
            # Very specific targeting of None here for ID method frequency.
            NONE_STR = ", None ("
            NONE_REPLACE = ", No method ("
            if NONE_STR in id_method_frequency:
                id_method_frequency = id_method_frequency.replace(
                    NONE_STR, NONE_REPLACE, 1
                )
            self.printFormattedText(id_method_frequency)

        if self.analysis_results.extensionIDOnlyCount > 0:
            if (
                self.analysis_results.extensionOnlyIDList is not None
                and self.analysis_results.extensionOnlyIDFrequency is not None
            ):
                if len(self.analysis_results.extensionOnlyIDList) > 0:
                    self._output_list_title(
                        self.STRINGS.HEADING_FREQUENCY_EXTENSION_ONLY
                    )
                    self.printFormattedText(
                        self._frequencyoutput(
                            self.analysis_results.extensionOnlyIDFrequency
                        )
                    )

        if self.analysis_results.uniqueExtensionsInCollectionList is not None:
            self._output_list_title(self.STRINGS.HEADING_UNIQUE_EXTENSIONS)
            output = ""
            for item in self.analysis_results.uniqueExtensionsInCollectionList:
                output = "{}{}, ".format(output, item[0])
            self.printFormattedText(output.strip(", "))

        if self.analysis_results.rogue_multiple_identification_list is not None:
            if len(self.analysis_results.rogue_multiple_identification_list) > 0:
                self._output_list_title(self.STRINGS.HEADING_LIST_MULTIPLE)
                self.printFormattedText(
                    self._itemlist(
                        self.analysis_results.rogue_multiple_identification_list
                    )
                )

        if self.analysis_results.frequencyOfAllExtensions is not None:
            self._output_list_title(self.STRINGS.HEADING_FREQUENCY_EXTENSIONS_ALL)
            self.printFormattedText(
                self._frequencyoutput(self.analysis_results.frequencyOfAllExtensions)
            )

        if self.analysis_results.mimetypeFrequency is not None:
            self._output_list_title(self.STRINGS.HEADING_FREQUENCY_MIME)
            mimes = self.analysis_results.mimetypeFrequency
            for m in mimes:
                if m[0] == "":
                    mimes.remove(m)
            self.printFormattedText(
                self._frequencyoutput(self.analysis_results.mimetypeFrequency)
            )

        if (
            self.analysis_results.signatureidentifiedfrequency is not None
            and self.analysis_results.nsdatalist is not None
        ):
            self._output_list_title(self.STRINGS.HEADING_NAMESPACE_SPECIFIC_STATISTICS)
            namespace_results = self._handlenamespacestats(
                self.analysis_results.nsdatalist,
                self.analysis_results.signatureidentifiedfrequency,
            )
            self.printFormattedText(namespace_results)

        # ##########ID SPECIFIC OUTPUT#################### # XML, TEXT, FILENAME
        if (
            self.analysis_results.xml_identifiers is not None
            and len(self.analysis_results.xml_identifiers) > 0
        ):
            self._output_list_title(self.STRINGS.HEADING_XML_ID_COMPLETE)
            self.printFormattedText(
                self._frequencyoutput(self.analysis_results.xml_identifiers)
            )
        if (
            self.analysis_results.text_identifiers is not None
            and len(self.analysis_results.text_identifiers) > 0
        ):
            self._output_list_title(self.STRINGS.HEADING_TEXT_ID_COMPLETE)
            self.printFormattedText(
                self._frequencyoutput(self.analysis_results.text_identifiers)
            )
        if (
            self.analysis_results.filename_identifiers is not None
            and len(self.analysis_results.filename_identifiers) > 0
        ):
            self._output_list_title(self.STRINGS.HEADING_FILENAME_ID_COMPLETE)
            self.printFormattedText(
                self._frequencyoutput(self.analysis_results.filename_identifiers)
            )
        # ##########ID SPECIFIC OUTPUT#################### # XML, TEXT, FILENAME

        if self.analysis_results.zerobytecount > 0:
            self.printFormattedText("\n")
            self.printFormattedText(
                self._output_list(
                    self.STRINGS.HEADING_LIST_ZERO_BYTES,
                    self.analysis_results.zerobytecount,
                )
            )
            self.printFormattedText(self._itemlist(self.analysis_results.zerobytelist))

        if self.analysis_results.containertypeslist is not None:
            if len(self.analysis_results.containertypeslist) > 0:
                self._output_list_title(self.STRINGS.HEADING_ARCHIVE_FORMATS)
                output = ""
                for archive in self.analysis_results.containertypeslist:
                    output = "{}{}, ".format(output, archive[0])
                self.printFormattedText(output.strip(", "))

        self.printFormattedText("\n", True)

        if self.analysis_results.hashused > 0:
            if self.analysis_results.totalHASHduplicates > 0:
                self.printFormattedText(
                    self._output_list(
                        self.STRINGS.HEADING_IDENTICAL_CONTENT,
                        self.analysis_results.totalHASHduplicates,
                    )
                )
                self.printFormattedText(
                    self._outputdupes(self.analysis_results.duplicateHASHlisting)
                )

        if self.analysis_results.badFileNames is not None:
            if len(self.analysis_results.badFileNames) > 0:
                self._output_list_title(self.STRINGS.HEADING_TROUBLESOME_FILENAMES)
                for badnames in self.analysis_results.badFileNames:
                    # Already UTF-8 on way into here...
                    self.printFormattedText(badnames, False)

        if self.analysis_results.badDirNames is not None:
            if len(self.analysis_results.badDirNames) > 0:
                self._output_list_title(self.STRINGS.HEADING_TROUBLESOME_FILENAMES)
                for badnames in self.analysis_results.badDirNames:
                    # Already UTF-8 on way into here...
                    self.printFormattedText(badnames, False)

        if self.analysis_results.denylist is True:
            if self.analysis_results.denylist_ids:
                self._output_list_title(self.STRINGS.HEADING_DENYLIST_IDS)
                self.printFormattedText(
                    self._aggregatelists(self.analysis_results.denylist_ids)
                )
            if self.analysis_results.denylist_exts:
                self._output_list_title(self.STRINGS.HEADING_DENYLIST_EXTS)
                self.printFormattedText(
                    self._aggregatelists(self.analysis_results.denylist_exts)
                )
            if self.analysis_results.denylist_filenames:
                self._output_list_title(self.STRINGS.HEADING_DENYLIST_FILENAMES)
                self.printFormattedText(
                    self._aggregatelists(self.analysis_results.denylist_filenames)
                )
            if self.analysis_results.denylist_directories:
                self._output_list_title(self.STRINGS.HEADING_DENYLIST_DIRS)
                self.printFormattedText(
                    self._aggregatelists(self.analysis_results.denylist_directories)
                )

        if self.analysis_results.errorlist:
            self._output_list_title(self.STRINGS.HEADING_ERRORS)
            self.printFormattedText(
                self._frequencyoutput(self.analysis_results.errorlist)
            )
