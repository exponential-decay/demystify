# -*- coding: utf-8 -*-

# pylint: disable=W1633

from __future__ import absolute_import, division

import logging
import re
import sys

from i18n.internationalstrings import AnalysisStringsEN as IN_EN

from .. import DemystifyAnalysisClass

if sys.version_info[0] == 3:
    PY3 = True
else:
    PY3 = False

# NONE_REPLACE_DEBUG is a logging prompt to help us to understand what
# needs changing around 'None'/null values from the database. These
# values are driven by the report, and standard handling in sqlitefid.
# E.g. if there is no version associated with a format, its version is
# None. This should be fixed in the data structures used to output the
# text, or in the database queries, not the presentation layer (arguably).
NONE_REPLACE_DEBUG = "Replacing 'None': A field in the database is null because there is no data, replacing at the presentation later..."


class DROIDAnalysisTextOutput:

    textoutput = ""

    def __init__(self, analysis_results):
        self.STRINGS = IN_EN
        self.analysis_results = analysis_results

    def __output_list__(self, title, value):
        return title + ": " + str(value)

    def __itemlist__(self, list):
        output = ""
        for item in list:
            output = output + str(item) + "\n"
        return output.strip("\n")

    def __printNewline__(self):
        self.printFormattedText("\n")

    def __output_list_title__(self, title):
        self.__printNewline__()
        self.printFormattedText(title + ":")

    def splitidresults(self, puid):
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
        line_end = u""
        if newline:
            line_end = u"\n"
        try:
            string = "{}".format(string)
        except UnicodeEncodeError:
            string = b"{}".format(string.encode("utf8"))
        self.textoutput = "{}{}{}".format(self.textoutput, string, line_end)

    def printTextResults(self):
        self.generateTEXT()
        return self.textoutput

    # namespace argument is used for anything requiring the output of a namespace too, e.g. IDS
    def __frequencyoutput__(self, itemlist, zeros=False):
        val = ""
        if not isinstance(itemlist, list):
            sys.stderr.write(
                "LOG: Not sending a list to a function wanting a list." + "\n"
            )
        else:
            for item in itemlist:
                if zeros is True:
                    val = "{}{}, ".format(val, item[0])
                else:
                    val = "{}{} ({}), ".format(val, item[0], item[1])
            val = val.strip(", ")

        return val

    def __aggregatelists__(self, itemlist):
        outstr = ""
        if not isinstance(itemlist, list):
            sys.stderr.write(
                "LOG: Not sending a list to a function wanting a list." + "\n"
            )
        else:
            for item in itemlist:
                name = item[0]
                if item[1] is not None:
                    count = "(" + str(item[1]) + ")"
                    outstr = outstr + name + " " + count + "\n"
                else:
                    outstr = outstr + name + "\n"
        return outstr.strip("\n")

    def getDateList(self):
        if self.analysis_results.dateFrequency is not None:
            return self.__frequencyoutput__(self.analysis_results.dateFrequency)

    def __outputdupes__(self, list):
        output = ""
        for dupes in self.analysis_results.duplicateHASHlisting:
            output = output + "Checksum: " + str(dupes["checksum"]) + "\n"
            output = output + "Count: " + str(dupes["count"]) + "\n"
            output = output + "Example: " + str(dupes["examples"][0]) + "\n\n"
        return output.strip("\n")

    def __handlenamespacestats__(self, nsdatalist, signaturefrequency):
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
            output = (
                output
                + self.STRINGS.HEADING_NAMESPACE
                + ": "
                + nstitle
                + " ("
                + ns[demystify.NS_CONST_DETAILS]
                + ")"
                "\n"
            )
            output = (
                output
                + self.STRINGS.SUMMARY_IDENTIFIED_FILES
                + ": "
                + str(identified)
                + "\n"
            )
            output = (
                output
                + self.STRINGS.SUMMARY_MULTIPLE
                + ": "
                + str(ns[demystify.NS_CONST_MULTIPLE_IDS])
                + "\n"
            )
            output = (
                output
                + self.STRINGS.SUMMARY_UNIDENTIFIED
                + ": "
                + str(unidentified)
                + "\n"
            )
            output = output + self.STRINGS.SUMMARY_EXTENSION_ID + ": " + str(ext) + "\n"

            if self.analysis_results.tooltype != "droid":
                output = output + self.STRINGS.SUMMARY_XML_ID + ": " + str(xmlid) + "\n"
                output = output + self.STRINGS.SUMMARY_TEXT_ID + ": " + str(text) + "\n"
                output = (
                    output
                    + self.STRINGS.SUMMARY_FILENAME_ID
                    + ": "
                    + str(filename)
                    + "\n"
                )

            output = (
                output
                + self.STRINGS.SUMMARY_PERCENTAGE_IDENTIFIED
                + ": "
                + str(percent_ok)
                + "\n"
            )
            output = (
                output
                + self.STRINGS.SUMMARY_PERCENTAGE_UNIDENTIFIED
                + ": "
                + str(percent_not)
                + "\n"
            )
            output = output + "\n"
            output = output + self.STRINGS.HEADING_FREQUENCY_PUIDS_IDENTIFIED + "\n"
            for idrow in signatureids:
                if idrow[0] == nstitle:
                    output = output + idrow[1] + " (" + str(idrow[2]) + "), "
            output = output.strip(", ")
            output = output + "\n\n"

        return output.strip("\n")

    def __generateOffsetText__(self, offsettext):
        # #########['id','basis','filename','filesize','offset']##########
        offs = offsettext
        if offs is not None:
            return (
                offs[0]
                + ", "
                + offs[1]
                + " e.g. "
                + offs[2]
                + " filesize: "
                + str(offs[3])
                + ", "
                + str(offs[4])
                + " bytes"
            )

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

    def generateTEXT(self):
        if self.analysis_results.tooltype != "droid":
            self.printFormattedText(self.STRINGS.REPORT_TITLE_SF)
        else:
            self.printFormattedText(self.STRINGS.REPORT_TITLE_DR)

        self.printFormattedText(
            self.STRINGS.REPORT_VERSION + ": " + self.analysis_results.__version__()
        )
        self.printFormattedText(
            self.STRINGS.REPORT_FILE + ": " + self.analysis_results.filename
        )
        self.printFormattedText(
            self.STRINGS.REPORT_TOOL + ": " + self.analysis_results.tooltype
        )
        self.printFormattedText("")
        self.printFormattedText(
            self.STRINGS.NAMESPACES + ": " + str(self.analysis_results.namespacecount)
        )

        if self.analysis_results.bof_distance is not None:
            self.printFormattedText(
                self.STRINGS.SUMMARY_DISTANCE_BOF
                + ": "
                + self.__generateOffsetText__(self.analysis_results.bof_distance)
            )

        if self.analysis_results.eof_distance is not None:
            self.printFormattedText(
                self.STRINGS.SUMMARY_DISTANCE_EOF
                + ": "
                + self.__generateOffsetText__(self.analysis_results.eof_distance)
            )

        self.printFormattedText("")

        self.printFormattedText(
            self.__output_list__(
                self.STRINGS.SUMMARY_TOTAL_FILES, self.analysis_results.filecount
            )
        )
        self.printFormattedText(
            self.__output_list__(
                self.STRINGS.SUMMARY_ARCHIVE_FILES, self.analysis_results.containercount
            )
        )

        # even if we have archive files, if the analysis isn't on, we can't output this value
        if self.analysis_results.filesincontainercount > 0:
            self.printFormattedText(
                self.__output_list__(
                    self.STRINGS.SUMMARY_INSIDE_ARCHIVES,
                    self.analysis_results.filesincontainercount,
                )
            )

        self.printFormattedText(
            self.__output_list__(
                self.STRINGS.SUMMARY_DIRECTORIES, self.analysis_results.directoryCount
            )
        )
        self.printFormattedText(
            self.__output_list__(
                self.STRINGS.SUMMARY_UNIQUE_DIRNAMES,
                self.analysis_results.uniqueDirectoryNames,
            )
        )
        self.printFormattedText(
            self.__output_list__(
                self.STRINGS.SUMMARY_IDENTIFIED_FILES,
                self.analysis_results.identifiedfilecount,
            )
        )
        self.printFormattedText(
            self.__output_list__(
                self.STRINGS.SUMMARY_MULTIPLE,
                self.analysis_results.multipleidentificationcount,
            )
        )
        self.printFormattedText(
            self.__output_list__(
                self.STRINGS.SUMMARY_UNIDENTIFIED,
                self.analysis_results.unidentifiedfilecount,
            )
        )

        if self.analysis_results.tooltype != "droid":
            self.printFormattedText(
                self.__output_list__(
                    self.STRINGS.SUMMARY_XML_ID, self.analysis_results.xmlidfilecount
                )
            )
            self.printFormattedText(
                self.__output_list__(
                    self.STRINGS.SUMMARY_TEXT_ID, self.analysis_results.textidfilecount
                )
            )
            self.printFormattedText(
                self.__output_list__(
                    self.STRINGS.SUMMARY_FILENAME_ID,
                    self.analysis_results.filenameidfilecount,
                )
            )

        self.printFormattedText(
            self.__output_list__(
                self.STRINGS.SUMMARY_EXTENSION_ID,
                self.analysis_results.extensionIDOnlyCount,
            )
        )
        self.printFormattedText(
            self.__output_list__(
                self.STRINGS.SUMMARY_EXTENSION_MISMATCH,
                self.analysis_results.extmismatchCount,
            )
        )
        self.printFormattedText(
            self.__output_list__(
                self.STRINGS.SUMMARY_ID_PUID_COUNT,
                self.analysis_results.distinctSignaturePuidcount,
            )
        )

        if self.analysis_results.tooltype != "droid":
            self.printFormattedText(
                self.__output_list__(
                    self.STRINGS.SUMMARY_OTHER_ID_COUNT,
                    self.analysis_results.distinctOtherIdentifiers,
                )
            )
            self.printFormattedText(
                self.__output_list__(
                    self.STRINGS.SUMMARY_XML_ID_COUNT,
                    self.analysis_results.distinctXMLIdentifiers,
                )
            )
            self.printFormattedText(
                self.__output_list__(
                    self.STRINGS.SUMMARY_TEXT_ID_COUNT,
                    self.analysis_results.distinctTextIdentifiers,
                )
            )
            self.printFormattedText(
                self.__output_list__(
                    self.STRINGS.SUMMARY_FILENAME_ID_COUNT,
                    self.analysis_results.distinctFilenameIdentifiers,
                )
            )

        self.printFormattedText(
            self.__output_list__(
                self.STRINGS.SUMMARY_UNIQUE_EXTENSIONS,
                self.analysis_results.distinctextensioncount,
            )
        )
        self.printFormattedText(
            self.__output_list__(
                self.STRINGS.SUMMARY_ZERO_BYTE, self.analysis_results.zerobytecount
            )
        )

        if self.analysis_results.hashused > 0:
            self.printFormattedText(
                self.__output_list__(
                    self.STRINGS.SUMMARY_IDENTICAL_FILES,
                    self.analysis_results.totalHASHduplicates,
                )
            )

        self.printFormattedText(
            self.__output_list__(
                self.STRINGS.SUMMARY_PERCENTAGE_IDENTIFIED,
                self.analysis_results.identifiedPercentage,
            )
        )
        self.printFormattedText(
            self.__output_list__(
                self.STRINGS.SUMMARY_PERCENTAGE_UNIDENTIFIED,
                self.analysis_results.unidentifiedPercentage,
            )
        )

        if (
            self.analysis_results.namespacecount > 1
            and self.analysis_results.identificationgaps is not None
        ):
            self.printFormattedText(
                self.__output_list__(
                    self.STRINGS.SUMMARY_GAPS_COVERED,
                    self.analysis_results.identificationgaps,
                )
            )

        # return the size of the collection
        size = self.analysis_results.collectionsize  # easier to reference from a var
        self.printFormattedText(
            self.STRINGS.HEADING_SIZE
            + ": "
            + str(float(size))
            + " bytes | "
            + str(round(float(float(size) / (1048576)), 1))
            + " MiB/MB (Megabytes)"
        )  # MiB/MB = (2^1024)*2

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
            self.__output_list_title__(self.STRINGS.HEADING_AGGREGATE_BINARY_IDENTIFIED)
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
            self.printFormattedText(self.__aggregatelists__(new_list))

        if self.analysis_results.xmlidentifiers is not None:
            self.__output_list_title__(self.STRINGS.HEADING_XML_ID)
            new_list = self._remove_version_if_none(
                self.analysis_results.xmlidentifiers
            )
            new_list = self._removenamespaceid(new_list)
            self.printFormattedText(self.__aggregatelists__(new_list))
        if self.analysis_results.textidentifiers is not None:
            self.__output_list_title__(self.STRINGS.HEADING_TEXT_ID)
            new_list = self._remove_version_if_none(
                self.analysis_results.textidentifiers
            )
            new_list = self._removenamespaceid(new_list)
            self.printFormattedText(self.__aggregatelists__(new_list))
        if self.analysis_results.filenameidentifiers is not None:
            self.__output_list_title__(self.STRINGS.HEADING_FILENAME_ID)
            new_list = self._remove_version_if_none(
                self.analysis_results.filenameidentifiers
            )
            new_list = self._removenamespaceid(new_list)
            self.printFormattedText(self.__aggregatelists__(new_list))

        if self.analysis_results.extensionIDOnlyCount > 0:
            if self.analysis_results.extensionOnlyIDList is not None:
                if len(self.analysis_results.extensionOnlyIDList) > 0:
                    self.__output_list_title__(self.STRINGS.HEADING_EXTENSION_ONLY)
                    for item in self.analysis_results.extensionOnlyIDList:
                        if item[1] == "None":
                            output = u"{}".format(item[0])
                        else:
                            output = u"{}, {}".format(item[0], item[1])
                        self.printFormattedText(output)

        dates = self.getDateList()
        if dates is not None:
            self.__output_list_title__(self.STRINGS.HEADING_DATE_RANGE)
            self.printFormattedText(dates)

        if self.analysis_results.idmethodFrequency is not None:
            self.__output_list_title__(self.STRINGS.HEADING_ID_METHOD)
            id_method_frequency = self.__frequencyoutput__(
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
                    self.__output_list_title__(
                        self.STRINGS.HEADING_FREQUENCY_EXTENSION_ONLY
                    )
                    self.printFormattedText(
                        self.__frequencyoutput__(
                            self.analysis_results.extensionOnlyIDFrequency
                        )
                    )

        if self.analysis_results.uniqueExtensionsInCollectionList is not None:
            self.__output_list_title__(self.STRINGS.HEADING_UNIQUE_EXTENSIONS)
            output = ""
            for item in self.analysis_results.uniqueExtensionsInCollectionList:
                output = output + item[0] + ", "
            self.printFormattedText(output.strip(", "))

        if self.analysis_results.rogue_multiple_identification_list is not None:
            if len(self.analysis_results.rogue_multiple_identification_list) > 0:
                self.__output_list_title__(self.STRINGS.HEADING_LIST_MULTIPLE)
                self.printFormattedText(
                    self.__itemlist__(
                        self.analysis_results.rogue_multiple_identification_list
                    )
                )

        if self.analysis_results.frequencyOfAllExtensions is not None:
            self.__output_list_title__(self.STRINGS.HEADING_FREQUENCY_EXTENSIONS_ALL)
            self.printFormattedText(
                self.__frequencyoutput__(self.analysis_results.frequencyOfAllExtensions)
            )

        if self.analysis_results.mimetypeFrequency is not None:
            self.__output_list_title__(self.STRINGS.HEADING_FREQUENCY_MIME)
            mimes = self.analysis_results.mimetypeFrequency
            for m in mimes:
                if m[0] == "":
                    mimes.remove(m)
            self.printFormattedText(
                self.__frequencyoutput__(self.analysis_results.mimetypeFrequency)
            )

        if (
            self.analysis_results.signatureidentifiedfrequency is not None
            and self.analysis_results.nsdatalist is not None
        ):
            self.__output_list_title__(
                self.STRINGS.HEADING_NAMESPACE_SPECIFIC_STATISTICS
            )
            namespace_results = self.__handlenamespacestats__(
                self.analysis_results.nsdatalist,
                self.analysis_results.signatureidentifiedfrequency,
            )
            self.printFormattedText(namespace_results)

        # ##########ID SPECIFIC OUTPUT#################### # XML, TEXT, FILENAME
        if (
            self.analysis_results.xml_identifiers is not None
            and len(self.analysis_results.xml_identifiers) > 0
        ):
            self.__output_list_title__(self.STRINGS.HEADING_XML_ID_COMPLETE)
            self.printFormattedText(
                self.__frequencyoutput__(self.analysis_results.xml_identifiers)
            )
        if (
            self.analysis_results.text_identifiers is not None
            and len(self.analysis_results.text_identifiers) > 0
        ):
            self.__output_list_title__(self.STRINGS.HEADING_TEXT_ID_COMPLETE)
            self.printFormattedText(
                self.__frequencyoutput__(self.analysis_results.text_identifiers)
            )
        if (
            self.analysis_results.filename_identifiers is not None
            and len(self.analysis_results.filename_identifiers) > 0
        ):
            self.__output_list_title__(self.STRINGS.HEADING_FILENAME_ID_COMPLETE)
            self.printFormattedText(
                self.__frequencyoutput__(self.analysis_results.filename_identifiers)
            )
        # ##########ID SPECIFIC OUTPUT#################### # XML, TEXT, FILENAME

        if self.analysis_results.zerobytecount > 0:
            self.printFormattedText("\n")
            self.printFormattedText(
                self.__output_list__(
                    self.STRINGS.HEADING_LIST_ZERO_BYTES,
                    self.analysis_results.zerobytecount,
                )
            )
            self.printFormattedText(
                self.__itemlist__(self.analysis_results.zerobytelist)
            )

        if self.analysis_results.containertypeslist is not None:
            if len(self.analysis_results.containertypeslist) > 0:
                self.__output_list_title__(self.STRINGS.HEADING_ARCHIVE_FORMATS)
                output = ""
                for archive in self.analysis_results.containertypeslist:
                    output = output + archive[0] + ", "
                self.printFormattedText(output.strip(", "))

        self.printFormattedText("\n", True)

        if self.analysis_results.hashused > 0:
            if self.analysis_results.totalHASHduplicates > 0:
                self.printFormattedText(
                    self.__output_list__(
                        self.STRINGS.HEADING_IDENTICAL_CONTENT,
                        self.analysis_results.totalHASHduplicates,
                    )
                )
                self.printFormattedText(
                    self.__outputdupes__(self.analysis_results.duplicateHASHlisting)
                )

        if self.analysis_results.badFileNames is not None:
            if len(self.analysis_results.badFileNames) > 0:
                self.__output_list_title__(self.STRINGS.HEADING_TROUBLESOME_FILENAMES)
                for badnames in self.analysis_results.badFileNames:
                    # Already UTF-8 on way into here...
                    self.printFormattedText(badnames, False)

        if self.analysis_results.badDirNames is not None:
            if len(self.analysis_results.badDirNames) > 0:
                self.__output_list_title__(self.STRINGS.HEADING_TROUBLESOME_FILENAMES)
                for badnames in self.analysis_results.badDirNames:
                    # Already UTF-8 on way into here...
                    self.printFormattedText(badnames, False)

        if self.analysis_results.denylist is True:
            if self.analysis_results.denylist_ids:
                self.__output_list_title__(self.STRINGS.HEADING_DENYLIST_IDS)
                self.printFormattedText(
                    self.__aggregatelists__(self.analysis_results.denylist_ids)
                )
            if self.analysis_results.denylist_exts:
                self.__output_list_title__(self.STRINGS.HEADING_DENYLIST_EXTS)
                self.printFormattedText(
                    self.__aggregatelists__(self.analysis_results.denylist_exts)
                )
            if self.analysis_results.denylist_filenames:
                self.__output_list_title__(self.STRINGS.HEADING_DENYLIST_FILENAMES)
                self.printFormattedText(
                    self.__aggregatelists__(self.analysis_results.denylist_filenames)
                )
            if self.analysis_results.denylist_directories:
                self.__output_list_title__(self.STRINGS.HEADING_DENYLIST_DIRS)
                self.printFormattedText(
                    self.__aggregatelists__(self.analysis_results.denylist_directories)
                )

        if self.analysis_results.errorlist:
            self.__output_list_title__(self.STRINGS.HEADING_ERRORS)
            self.printFormattedText(
                self.__frequencyoutput__(self.analysis_results.errorlist)
            )
