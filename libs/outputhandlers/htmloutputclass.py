# -*- coding: utf-8 -*-

# pylint: disable=W1633

from __future__ import absolute_import, division

import re
import sys

from i18n.internationalstrings import AnalysisStringsEN as IN_EN
from libs import DemystifyAnalysisClass

if sys.version_info[0] == 3:
    PY3 = True
else:
    PY3 = False


class DROIDAnalysisHTMLOutput:
    def __init__(self, analysisresults):
        self.wiki = True
        self.STRINGS = IN_EN
        self.analysisresults = analysisresults
        self.htmloutput = u""

    def STDOUTprintFormattedText(self, text):
        sys.stdout.write(text)
        self.__printnewline__()

    def STDOUT__printnewline__(self):
        sys.stdout.write("\n")

    def printFormattedText(self, text):
        if isinstance(text, list):
            for txt in text:
                self.htmloutput = "{}{}</br></br>".format(self.htmloutput, txt)
            self.__printnewline__()
            return

        if PY3:
            newtext = text
        else:
            newtext = u"{}".format(text)
        self.htmloutput = u"{}{}".format(self.htmloutput, newtext)
        self.__printnewline__()

    def __printnewline__(self):
        self.htmloutput = u"{}\n".format(self.htmloutput)

    def __htmlnewline__(self, no=1):
        for x in range(no):
            self.printFormattedText("</br>")

    def __make_str__(self, str_):
        return u"{}:".format(str_)

    def __make_summary__(self, str_):
        return "<details><summary>{}</br></summary></br>{}</br></details>".format(
            self.STRINGS.REPORT_MORE_INFORMATION, str_
        )

    def __make_list_item__(self, title, content, value):
        return '<li title="{}">{}{}</li>'.format(
            title, self.__make_str__(content), value
        )

    def __keyvalue_output__(self, list):
        self.__htmlnewline__()
        for item in list:
            self.printFormattedText("{}, {}</br>".format(item[0], item[1]))
        self.__htmlnewline__()
        self.printFormattedText("<hr/>")

    def __csv_output__(self, list):
        self.__htmlnewline__()
        out = ""
        for item in list:
            out = "{}{}, ".format(out, item[0])
        self.printFormattedText(out.strip(", "))
        self.__htmlnewline__(2)
        self.printFormattedText("<hr/>")

    # Trial function we're not using yet... Prettty Print
    def prettyprinthtml():
        # document_root = html.fromstring(self.htmloutput)
        # print document_root
        # print(etree.tostring(document_root, encoding='utf-8', pretty_print=True))
        return None

    def printHTMLResults(self):
        self.generateHTML()
        return self.htmloutput

    def splitidresults(self, puid):
        identifier = puid[0].rsplit("(", 1)[0]
        namespace = puid[0].split(" ", 1)[0]

        # TODO: Flake8 doesn't like the escape sequence here... `\/` is
        # this really invalid? What alternatives are there for what we
        # want to achieve?
        patt = re.compile("(x-)?fmt\/[0-9]+")  # noqa

        p = re.search(patt, identifier)
        if p is not None:
            p = p.span()
            identifier = identifier[p[0] : p[1]]
        else:
            identifier = identifier.replace(namespace, "").strip()
            identifier = identifier.split(",", 1)[0]
        count = puid[0].rsplit("(", 1)[1].replace(")", "")
        formatname = (
            puid[0]
            .replace(namespace, "")
            .replace("({})".format(count), "")
            .replace("{}, ".format(identifier), "")
            .strip(", ")
        )
        if formatname == "":
            formatname = identifier
        return namespace, identifier, formatname, count

    def __outputmeter__(self, value, minval, maxval):
        return '<td><meter style="width: 300px;" value="{}" min="{}" max="{}">&nbsp;METER VISUALISATION AVAILABLE IN GOOGLE CHROME&nbsp;</meter></td>'.format(
            str(value).strip(), minval, maxval
        )

    def __generateOffsetText__(self, offsettext):
        # #########['id','basis','filename','filesize','offset']##########
        offs = offsettext
        if offs is not None:
            return "<code>{}, {} e.g. {} filesize: {}. {} bytes</code>".format(
                offs[0], offs[1], offs[2], offs[3], offs[4]
            )

    def identifierchart(self, countlist, reverse_list=True):
        countlist.sort(key=lambda tup: tup[1], reverse=reverse_list)
        # Signature ID PUIDs
        self.__outputheading__(
            self.STRINGS.HEADING_FREQUENCY_PUIDS_IDENTIFIED,
            self.STRINGS.HEADING_DESC_FREQUENCY_PUIDS_IDENTIFIED,
        )
        self.printFormattedText("<table>")
        # http://www.nationalarchives.gov.uk/aboutapps/pronom/puid.htm <- link to reinstate somewhere
        self.printFormattedText(
            '<table><th style="text-align: left;">{}</th><th style="text-align: left;">{}</th><th style="text-align: left;">{}</th>'.format(
                self.STRINGS.COLUMN_HEADER_VALUES_ID,
                self.STRINGS.COLUMN_HEADER_VALUES_COUNT,
                self.STRINGS.COLUMN_HEADER_VALUES_YEAR,
            )
        )
        for sig in countlist:
            self.printFormattedText('<tr><td style="width: 220px;">')
            if "fmt/" in sig[0]:
                self.printFormattedText(
                    '<a target="_blank" href="http://apps.nationalarchives.gov.uk/PRONOM/{}">{}</a>'.format(
                        sig[0], sig[0]
                    )
                )
            else:
                self.printFormattedText(sig[0])
            self.printFormattedText(
                '</td><td style="width: 100px;">{}</td>'.format(str(sig[1]).strip())
            )
            self.printFormattedText(
                self.__outputmeter__(sig[1], 0, self.analysisresults.filecount)
            )
            self.printFormattedText("</tr>")
        self.printFormattedText("</table>")
        self.__htmlnewline__()
        self.printFormattedText("<hr/>")

    def signature_id_listing(self, idlist):
        # Signature identified PUIDs in collection (signature and container)
        self.__outputheading__(
            self.STRINGS.HEADING_AGGREGATE_BINARY_IDENTIFIED,
            self.STRINGS.HEADING_DESC_IDENTIFIED,
        )
        self.printFormattedText("<table>")
        self.printFormattedText(
            '<table><th style="text-align: left;">{}</th><th style="text-align: left;">{}</th><th style="text-align: left;">{}</th><th style="text-align: left;">{}</th>'.format(
                self.STRINGS.COLUMN_HEADER_VALUES_ID,
                self.STRINGS.COLUMN_HEADER_VALUES_NAMESPACE,
                self.STRINGS.COLUMN_HEADER_VALUES_FORMAT,
                self.STRINGS.COLUMN_HEADER_VALUES_COUNT,
            )
        )
        # ex: ('ns:pronom fmt/19, Acrobat PDF 1.5 - Portable Document Format, 1.5 (6)', 1)
        # Tuple object: (namespace, identifier, formatname, int(count))
        # Can sort using Lambda on count as required... unlikely at first
        for i in idlist:
            if "fmt/" in i[1]:
                markup = '<tr><td style="width: 200px;"><a target="_blank" href="http://apps.nationalarchives.gov.uk/PRONOM/{}"{}</a></td>'.format(
                    i[1], i[1]
                )
            else:
                markup = '<tr><td style="width: 100px;">{}</td>'.format(i[1])
            markup = '{}<td style="width: 150px;">{}</td><td>{}</td><td style="text-align:center">{}</td></tr>'.format(
                markup, i[0], i[2], i[3]
            )
            self.printFormattedText(markup)
        self.printFormattedText("</table>")
        self.__htmlnewline__(2)
        self.printFormattedText("<hr/>")

    def __handleidspecificoutput__(self):
        # handle output for other identifiers in the namespace
        if (
            self.analysisresults.xml_identifiers is not None
            and len(self.analysisresults.xml_identifiers) > 0
        ):
            self.__outputtable__(
                self.analysisresults.xml_identifiers,
                self.STRINGS.HEADING_XML_ID_COMPLETE,
                self.STRINGS.HEADING_DESC_XML_ID_COMPLETE,
                True,
                1,
                "800",
            )
        if (
            self.analysisresults.text_identifiers is not None
            and len(self.analysisresults.text_identifiers) > 0
        ):
            self.__outputtable__(
                self.analysisresults.text_identifiers,
                self.STRINGS.HEADING_TEXT_ID_COMPLETE,
                self.STRINGS.HEADING_DESC_TEXT_ID_COMPLETE,
                True,
                1,
                "800",
            )
        if (
            self.analysisresults.filename_identifiers is not None
            and len(self.analysisresults.filename_identifiers) > 0
        ):
            self.__outputtable__(
                self.analysisresults.filename_identifiers,
                self.STRINGS.HEADING_FILENAME_ID_COMPLETE,
                self.STRINGS.HEADING_DESC_FILENAME_ID_COMPLETE,
                True,
                1,
                "800",
            )

    def __handlenamespacestats__(self, nsdatalist, signaturefrequency):
        # e.g.{'binary method count': '57', 'text method count': '37', 'namespace title': 'freedesktop.org',
        # 'filename method count': '45', 'namespace details': 'freedesktop.org.xml'}
        ds = DemystifyAnalysisClass.DemystifyAnalysis()
        for ns in nsdatalist:
            signatureids = signaturefrequency
            nstitle = ns[ds.NS_CONST_TITLE]
            identified = ns[ds.NS_CONST_BINARY_COUNT]
            xmlid = ns[ds.NS_CONST_XML_COUNT]
            text = ns[ds.NS_CONST_TEXT_COUNT]
            filename = ns[ds.NS_CONST_FILENAME_COUNT]
            ext = ns[ds.NS_CONST_EXTENSION_COUNT]
            unidentified = self.analysisresults.filecount - identified
            percent_not = ds.calculatePercent(
                self.analysisresults.filecount, unidentified
            )
            percent_ok = ds.calculatePercent(self.analysisresults.filecount, identified)

            self.printFormattedText(
                self.__make_list_item__(
                    self.STRINGS.HEADING_DESC_NAMESPACE,
                    "<b>{}</b>".format(self.STRINGS.HEADING_NAMESPACE),
                    "<i>{} ({})</i>".format(nstitle, ns[ds.NS_CONST_DETAILS]),
                )
            )
            self.printFormattedText(
                self.__make_list_item__(
                    self.STRINGS.SUMMARY_DESC_IDENTIFIED_FILES,
                    self.STRINGS.SUMMARY_IDENTIFIED_FILES,
                    str(identified),
                )
            )
            self.printFormattedText(
                self.__make_list_item__(
                    self.STRINGS.SUMMARY_DESC_MULTIPLE,
                    self.STRINGS.SUMMARY_MULTIPLE,
                    str(ns[ds.NS_CONST_MULTIPLE_IDS]),
                )
            )
            self.printFormattedText(
                self.__make_list_item__(
                    self.STRINGS.SUMMARY_DESC_UNIDENTIFIED,
                    self.STRINGS.SUMMARY_UNIDENTIFIED,
                    str(unidentified),
                )
            )
            self.printFormattedText(
                self.__make_list_item__(
                    self.STRINGS.SUMMARY_DESC_EXTENSION_ID,
                    self.STRINGS.SUMMARY_EXTENSION_ID,
                    str(ext),
                )
            )

            if self.analysisresults.tooltype != "droid":
                self.printFormattedText(
                    self.__make_list_item__(
                        self.STRINGS.SUMMARY_DESC_XML_ID,
                        self.STRINGS.SUMMARY_XML_ID,
                        str(xmlid),
                    )
                )
                self.printFormattedText(
                    self.__make_list_item__(
                        self.STRINGS.SUMMARY_DESC_TEXT_ID,
                        self.STRINGS.SUMMARY_TEXT_ID,
                        str(text),
                    )
                )
                self.printFormattedText(
                    self.__make_list_item__(
                        self.STRINGS.SUMMARY_DESC_FILENAME_ID,
                        self.STRINGS.SUMMARY_FILENAME_ID,
                        str(filename),
                    )
                )

            self.printFormattedText(
                self.__make_list_item__(
                    self.STRINGS.SUMMARY_DESC_PERCENTAGE_IDENTIFIED,
                    self.STRINGS.SUMMARY_PERCENTAGE_IDENTIFIED,
                    str(percent_ok),
                )
            )
            self.printFormattedText(
                self.__make_list_item__(
                    self.STRINGS.SUMMARY_DESC_PERCENTAGE_UNIDENTIFIED,
                    self.STRINGS.SUMMARY_PERCENTAGE_UNIDENTIFIED,
                    str(percent_not),
                )
            )
            self.__htmlnewline__()
            nslist = []
            for idrow in signatureids:
                if idrow[0] == nstitle:
                    nslist.append(idrow[1:])
            self.__outputtable__(nslist, None, None, True, 2, "400")

    def __removenamespaceid__(self, oldlist):
        newlist = []
        for item in oldlist:
            newlist.append(str(item[0]))
        return newlist

    def outputaggregatelists(self):
        if self.analysisresults.binaryidentifiers is not None:
            newlist = self.__removenamespaceid__(self.analysisresults.binaryidentifiers)
            self.__outputtable__(
                newlist,
                self.STRINGS.HEADING_BINARY_ID,
                self.STRINGS.HEADING_DESC_BINARY_ID,
                True,
                1,
                "800",
                False,
            )
        if self.analysisresults.xmlidentifiers is not None:
            newlist = self.__removenamespaceid__(self.analysisresults.xmlidentifiers)
            self.__outputtable__(
                newlist,
                self.STRINGS.HEADING_XML_ID,
                self.STRINGS.HEADING_DESC_XML_ID,
                True,
                1,
                "800",
                False,
            )
        if self.analysisresults.textidentifiers is not None:
            newlist = self.__removenamespaceid__(self.analysisresults.textidentifiers)
            self.__outputtable__(
                newlist,
                self.STRINGS.HEADING_TEXT_ID,
                self.STRINGS.HEADING_DESC_TEXT_ID,
                True,
                1,
                "800",
                False,
            )
        if self.analysisresults.filenameidentifiers is not None:
            newlist = self.__removenamespaceid__(
                self.analysisresults.filenameidentifiers
            )
            self.__outputtable__(
                newlist,
                self.STRINGS.HEADING_FILENAME_ID,
                self.STRINGS.HEADING_DESC_FILENAME_ID,
                True,
                1,
                "800",
                False,
            )

    def __outputheading__(self, heading, description):
        self.printFormattedText("<h2>{}</h2>".format(self.__make_str__(heading)))
        self.printFormattedText(self.__make_summary__(description))
        self.__htmlnewline__()

    def __outputtable__(
        self,
        listing,
        heading,
        description,
        count=True,
        maxcolumns=5,
        pixels="160",
        nonewline=False,
    ):
        pixels = str(pixels)
        newline = True
        if heading is not None and description is not None:
            self.__outputheading__(heading, description)
        length = len(listing)
        rows = int(length / 5)
        if length % 5 > 0:
            rows = rows + 1
        rowno = 0
        colno = 0
        self.printFormattedText(
            "<table style='border-collapse: collapse; border-color: #222222'><tr>"
        )
        for item in listing:
            if type(item) is str:
                if nonewline is False:
                    string = "{}</br></br>".format(item)
                    newline = False
                else:
                    string = item
            elif len(item) == 1:
                string = str(item[0])
            elif count is False:
                if item[1] == "":
                    string = "{}, Format name not set".format(item[0])
                else:
                    string = "{}, {}".format(item[0], item[1])
            else:
                string = "{} ({})".format(item[0], item[1])
            if colno < maxcolumns:
                self.printFormattedText(
                    "<td width='{}'><code>{}</code></td>".format(pixels, string)
                )
                colno = colno + 1
            else:
                rowno = rowno + 1
                self.printFormattedText("</tr><tr>")
                self.printFormattedText(
                    "<td width='{}'><code>{}</code></td>".format(pixels, string)
                )
                colno = 1
        self.printFormattedText("</tr></table>")
        if newline is True:
            self.__htmlnewline__()
        self.printFormattedText("<hr/>")

    def generateHTML(self):
        self.printFormattedText("<!DOCTYPE html>")
        self.printFormattedText("<html lang='en'>")
        self.printFormattedText("<head>")
        if self.analysisresults.tooltype != "droid":
            self.printFormattedText(
                "<title>{}</title>".format(self.STRINGS.REPORT_TITLE_SF)
            )
        else:
            self.printFormattedText(
                "<title>{}</title>".format(self.STRINGS.REPORT_TITLE_DR)
            )
        self.printFormattedText(
            "<meta http-equiv='Content-Type' content='text/html; charset=utf-8'>"
        )
        self.printFormattedText("</head>")

        self.printFormattedText(
            "<body style='font-family: calibri, arial; letter-spacing: 0.5px; margin:0 auto; width: 800px; '>"
        )

        if self.analysisresults.tooltype != "droid":
            self.printFormattedText("<h1>{}</h1>".format(self.STRINGS.REPORT_TITLE_SF))
        else:
            self.printFormattedText("<h1>{}</h1>".format(self.STRINGS.REPORT_TITLE_DR))

        self.printFormattedText(
            "<b>{}: </b>{}".format(
                self.STRINGS.REPORT_VERSION, self.analysisresults.__version__()
            )
        )
        self.__htmlnewline__()
        self.printFormattedText(
            "<b>{}: </b>{}".format(
                self.STRINGS.REPORT_FILE, self.analysisresults.filename
            )
        )
        self.__htmlnewline__()
        self.printFormattedText(
            "<b>{}: </b>{}".format(
                self.STRINGS.REPORT_TOOL, self.analysisresults.tooltype
            )
        )
        self.__htmlnewline__(2)
        self.printFormattedText(
            "<b>{}: </b>{}".format(
                self.STRINGS.NAMESPACES, self.analysisresults.namespacecount
            )
        )
        self.__htmlnewline__()
        if self.analysisresults.bof_distance is not None:
            self.__htmlnewline__()
            self.printFormattedText(
                "<b>{}: </b>{}".format(
                    self.STRINGS.SUMMARY_DISTANCE_BOF,
                    self.__generateOffsetText__(self.analysisresults.bof_distance),
                )
            )
        if self.analysisresults.eof_distance is not None:
            if self.analysisresults.bof_distance is not None:
                self.__htmlnewline__()
            self.__htmlnewline__()
            self.printFormattedText(
                "<b>{}: </b>{}".format(
                    self.STRINGS.SUMMARY_DISTANCE_EOF,
                    self.__generateOffsetText__(self.analysisresults.eof_distance),
                )
            )

        self.printFormattedText("<h2>{}</h2>".format(self.STRINGS.REPORT_SUMMARY))

        self.printFormattedText("<ul>")
        self.printFormattedText(
            self.__make_list_item__(
                self.STRINGS.SUMMARY_DESC_TOTAL_FILES,
                self.STRINGS.SUMMARY_TOTAL_FILES,
                self.analysisresults.filecount,
            )
        )
        self.printFormattedText(
            self.__make_list_item__(
                self.STRINGS.SUMMARY_DESC_ARCHIVE_FILES,
                self.STRINGS.SUMMARY_ARCHIVE_FILES,
                self.analysisresults.containercount,
            )
        )

        # even if we have archive files, if the analysis isn't on, we can't output this value
        if self.analysisresults.filesincontainercount > 0:
            self.printFormattedText(
                self.__make_list_item__(
                    self.STRINGS.SUMMARY_DESC_INSIDE_ARCHIVES,
                    self.STRINGS.SUMMARY_INSIDE_ARCHIVES,
                    self.analysisresults.filesincontainercount,
                )
            )

        self.printFormattedText(
            self.__make_list_item__(
                self.STRINGS.SUMMARY_DESC_DIRECTORIES,
                self.STRINGS.SUMMARY_DIRECTORIES,
                self.analysisresults.directoryCount,
            )
        )
        self.printFormattedText(
            self.__make_list_item__(
                self.STRINGS.SUMMARY_DESC_UNIQUE_DIRNAMES,
                self.STRINGS.SUMMARY_UNIQUE_DIRNAMES,
                self.analysisresults.uniqueDirectoryNames,
            )
        )
        self.printFormattedText(
            self.__make_list_item__(
                self.STRINGS.SUMMARY_DESC_IDENTIFIED_FILES,
                self.STRINGS.SUMMARY_IDENTIFIED_FILES,
                self.analysisresults.identifiedfilecount,
            )
        )
        self.printFormattedText(
            self.__make_list_item__(
                self.STRINGS.SUMMARY_DESC_MULTIPLE,
                self.STRINGS.SUMMARY_MULTIPLE,
                self.analysisresults.multipleidentificationcount,
            )
        )
        self.printFormattedText(
            self.__make_list_item__(
                self.STRINGS.SUMMARY_DESC_UNIDENTIFIED,
                self.STRINGS.SUMMARY_UNIDENTIFIED,
                self.analysisresults.unidentifiedfilecount,
            )
        )

        if self.analysisresults.tooltype != "droid":
            self.printFormattedText(
                self.__make_list_item__(
                    self.STRINGS.SUMMARY_DESC_XML_ID,
                    self.STRINGS.SUMMARY_XML_ID,
                    self.analysisresults.xmlidfilecount,
                )
            )
            self.printFormattedText(
                self.__make_list_item__(
                    self.STRINGS.SUMMARY_DESC_TEXT_ID,
                    self.STRINGS.SUMMARY_TEXT_ID,
                    self.analysisresults.textidfilecount,
                )
            )
            self.printFormattedText(
                self.__make_list_item__(
                    self.STRINGS.SUMMARY_DESC_FILENAME_ID,
                    self.STRINGS.SUMMARY_FILENAME_ID,
                    self.analysisresults.filenameidfilecount,
                )
            )

        self.printFormattedText(
            self.__make_list_item__(
                self.STRINGS.SUMMARY_DESC_EXTENSION_ID,
                self.STRINGS.SUMMARY_EXTENSION_ID,
                self.analysisresults.extensionIDOnlyCount,
            )
        )
        self.printFormattedText(
            self.__make_list_item__(
                self.STRINGS.SUMMARY_DESC_EXTENSION_MISMATCH,
                self.STRINGS.SUMMARY_EXTENSION_MISMATCH,
                self.analysisresults.extmismatchCount,
            )
        )
        self.printFormattedText(
            self.__make_list_item__(
                self.STRINGS.SUMMARY_DESC_ID_PUID_COUNT,
                self.STRINGS.SUMMARY_ID_PUID_COUNT,
                self.analysisresults.distinctSignaturePuidcount,
            )
        )

        if self.analysisresults.tooltype != "droid":
            self.printFormattedText(
                self.__make_list_item__(
                    self.STRINGS.SUMMARY_DESC_OTHER_ID_COUNT,
                    self.STRINGS.SUMMARY_OTHER_ID_COUNT,
                    self.analysisresults.distinctOtherIdentifiers,
                )
            )
            self.printFormattedText(
                self.__make_list_item__(
                    self.STRINGS.SUMMARY_DESC_XML_ID_COUNT,
                    self.STRINGS.SUMMARY_XML_ID_COUNT,
                    self.analysisresults.distinctXMLIdentifiers,
                )
            )
            self.printFormattedText(
                self.__make_list_item__(
                    self.STRINGS.SUMMARY_DESC_TEXT_ID_COUNT,
                    self.STRINGS.SUMMARY_TEXT_ID_COUNT,
                    self.analysisresults.distinctTextIdentifiers,
                )
            )
            self.printFormattedText(
                self.__make_list_item__(
                    self.STRINGS.SUMMARY_DESC_FILENAME_ID_COUNT,
                    self.STRINGS.SUMMARY_FILENAME_ID_COUNT,
                    self.analysisresults.distinctFilenameIdentifiers,
                )
            )

        self.printFormattedText(
            self.__make_list_item__(
                self.STRINGS.SUMMARY_DESC_UNIQUE_EXTENSIONS,
                self.STRINGS.SUMMARY_UNIQUE_EXTENSIONS,
                self.analysisresults.distinctextensioncount,
            )
        )
        self.printFormattedText(
            self.__make_list_item__(
                self.STRINGS.SUMMARY_DESC_ZERO_BYTE,
                self.STRINGS.SUMMARY_ZERO_BYTE,
                self.analysisresults.zerobytecount,
            )
        )

        if self.analysisresults.hashused > 0:
            self.printFormattedText(
                self.__make_list_item__(
                    self.STRINGS.SUMMARY_DESC_IDENTICAL_FILES,
                    self.STRINGS.SUMMARY_IDENTICAL_FILES,
                    self.analysisresults.totalHASHduplicates,
                )
            )

        self.printFormattedText(
            self.__make_list_item__(
                self.STRINGS.SUMMARY_DESC_MULTIPLE_SPACES,
                self.STRINGS.SUMMARY_MULTIPLE_SPACES,
                len(self.analysisresults.multiplespacelist),
            )
        )
        self.printFormattedText(
            self.__make_list_item__(
                self.STRINGS.SUMMARY_DESC_PERCENTAGE_IDENTIFIED,
                self.STRINGS.SUMMARY_PERCENTAGE_IDENTIFIED,
                self.analysisresults.identifiedPercentage,
            )
        )
        self.printFormattedText(
            self.__make_list_item__(
                self.STRINGS.SUMMARY_DESC_PERCENTAGE_UNIDENTIFIED,
                self.STRINGS.SUMMARY_PERCENTAGE_UNIDENTIFIED,
                self.analysisresults.unidentifiedPercentage,
            )
        )

        if (
            self.analysisresults.namespacecount > 1
            and self.analysisresults.identificationgaps is not None
        ):
            self.printFormattedText(
                self.__make_list_item__(
                    self.STRINGS.SUMMARY_DESC_GAPS_COVERED,
                    self.STRINGS.SUMMARY_GAPS_COVERED,
                    self.analysisresults.identificationgaps,
                )
            )

        self.printFormattedText("</ul>")
        self.__htmlnewline__()
        self.printFormattedText("<hr/>")

        # return the size of the collection
        self.__outputheading__(
            self.STRINGS.HEADING_SIZE, self.STRINGS.HEADING_DESC_SIZE
        )

        # easier to reference from a var
        size = self.analysisresults.collectionsize

        self.printFormattedText(
            "{} bytes | {} MiB/MB (Megabytes)".format(
                float(size), round(float(float(size) / (1048576)), 1)
            )
        )  # MiB/MB = (2^1024)*2
        self.__htmlnewline__(2)
        self.printFormattedText("<hr/>")

        signature_id_list = []
        if self.analysisresults.signatureidentifiers is not None:
            countlist = []
            for puid in self.analysisresults.signatureidentifiers:
                namespace, identifier, formatname, count = self.splitidresults(puid)
                countlist.append((identifier, int(count)))
                signature_id_list.append(
                    (namespace, identifier, formatname, int(count))
                )
            self.identifierchart(countlist)

        if self.analysisresults.dateFrequency is not None:
            # Date Ranges
            self.__outputheading__(
                self.STRINGS.HEADING_DATE_RANGE, self.STRINGS.HEADING_DESC_DATE_RANGE
            )
            self.printFormattedText("<table>")
            self.printFormattedText(
                '<table><th style="text-align: left;">{}</a></th><th style="text-align: left;">{}</th>'.format(
                    self.STRINGS.COLUMN_HEADER_VALUES_YEAR,
                    self.STRINGS.COLUMN_HEADER_VALUES_COUNT,
                )
            )
            for dates in self.analysisresults.dateFrequency:
                self.printFormattedText('<tr><td style="width: 100px;">')

                if self.wiki is True:
                    self.printFormattedText(
                        '<a target="_blank" href="https://en.wikipedia.org/wiki/{}">{}</a>'.format(
                            dates[0], dates[0]
                        )
                    )
                else:
                    self.printFormattedText("<b>{}</b>".format(dates[0]))

                self.printFormattedText("</td><td>{}</td>".format(dates[1]))

                # Unused Meter Code...
                self.printFormattedText(
                    self.__outputmeter__(dates[1], 0, self.analysisresults.filecount)
                )
                self.printFormattedText("</tr>")

            self.printFormattedText("</table>")
            self.__htmlnewline__()
            self.printFormattedText("<hr/>")

        # Output charts first... most visual, immediate summary, next stats
        if len(signature_id_list) > 0:
            self.signature_id_listing(signature_id_list)

        # ###MORE AGGREGATE LISTS PER IDENTIFIER###
        self.outputaggregatelists()
        # ###MORE AGGREGATE LISTS PER IDENTIFIER###

        if self.analysisresults.idmethodFrequency is not None:
            # ID Method Frequency
            self.__outputtable__(
                self.analysisresults.idmethodFrequency,
                self.STRINGS.HEADING_ID_METHOD,
                self.STRINGS.HEADING_DESC_ID_METHOD,
            )

        if self.analysisresults.extensionOnlyIDList is not None:
            # Extension Only ID : TODO: Consider usefulness...
            self.__outputtable__(
                self.analysisresults.extensionOnlyIDList,
                self.STRINGS.HEADING_EXTENSION_ONLY,
                self.STRINGS.HEADING_DESC_EXTENSION_ONLY,
                False,
                2,
                "400",
            )

        if self.analysisresults.extensionOnlyIDList is not None:
            if len(self.analysisresults.extensionOnlyIDList) > 0:
                # Extension Only Identification
                extlist = self.analysisresults.extensionOnlyIDList
                for item in list(extlist):
                    if "UNKNOWN" in item[0] or "unknown" in item[0]:
                        extlist.remove(item)
                if self.analysisresults.tooltype != "droid":
                    # we have basis information so need a bigger table...
                    self.__outputtable__(
                        extlist,
                        self.STRINGS.HEADING_FREQUENCY_EXTENSION_ONLY,
                        self.STRINGS.HEADING_DESC_FREQUENCY_EXTENSION_ONLY,
                        True,
                        2,
                        "400",
                    )
                else:
                    self.__outputtable__(
                        extlist,
                        self.STRINGS.HEADING_FREQUENCY_EXTENSION_ONLY,
                        self.STRINGS.HEADING_DESC_FREQUENCY_EXTENSION_ONLY,
                        True,
                        3,
                        "275",
                    )

        if self.analysisresults.frequencyOfAllExtensions is not None:
            # Extension Frequency
            self.__outputtable__(
                self.analysisresults.frequencyOfAllExtensions,
                self.STRINGS.HEADING_FREQUENCY_EXTENSIONS_ALL,
                self.STRINGS.HEADING_DESC_FREQUENCY_EXTENSIONS_ALL,
            )

        if self.analysisresults.uniqueExtensionsInCollectionList is not None:
            # Unique Extensions Identified
            self.__outputtable__(
                self.analysisresults.uniqueExtensionsInCollectionList,
                self.STRINGS.HEADING_UNIQUE_EXTENSIONS,
                self.STRINGS.HEADING_DESC_UNIQUE_EXTENSIONS,
                False,
            )

        if self.analysisresults.rogue_multiple_identification_list is not None:
            if len(self.analysisresults.rogue_multiple_identification_list) > 0:
                # Files with multiple identifications, signature only
                self.__outputtable__(
                    self.analysisresults.rogue_multiple_identification_list,
                    self.STRINGS.HEADING_LIST_MULTIPLE,
                    self.STRINGS.HEADING_DESC_LIST_MULTIPLE,
                    False,
                    1,
                    "800",
                )

        if self.analysisresults.mimetypeFrequency is not None:
            # Mimetype Frequency
            mimes = self.analysisresults.mimetypeFrequency
            for m in list(mimes):
                if m[0] == "":
                    mimes.remove(m)
            self.__outputtable__(
                mimes,
                self.STRINGS.HEADING_FREQUENCY_MIME,
                self.STRINGS.HEADING_DESC_FREQUENCY_MIME,
                True,
                2,
                "400",
            )

        # ##########NS SPECIFIC OUTPUT####################
        if (
            self.analysisresults.signatureidentifiedfrequency is not None
            and self.analysisresults.nsdatalist is not None
        ):
            self.__outputheading__(
                self.STRINGS.HEADING_NAMESPACE_SPECIFIC_STATISTICS,
                self.STRINGS.HEADING_DESC_NAMESPACE_SPECIFIC_STATISTICS,
            )
            self.__handlenamespacestats__(
                self.analysisresults.nsdatalist,
                self.analysisresults.signatureidentifiedfrequency,
            )
        # ##########NS SPECIFIC OUTPUT####################

        # ##########ID SPECIFIC OUTPUT#################### #XML, TEXT, FILENAME
        self.__handleidspecificoutput__()
        # ##########ID SPECIFIC OUTPUT#################### #XML, TEXT, FILENAME

        if self.analysisresults.zerobytelist is not None:
            if len(self.analysisresults.zerobytelist):
                # Zero Byte Objects
                self.__outputtable__(
                    self.analysisresults.zerobytelist,
                    self.STRINGS.HEADING_LIST_ZERO_BYTES,
                    self.STRINGS.HEADING_DESC_LIST_ZERO_BYTES,
                    False,
                    1,
                    "800",
                    True,
                )

        if self.analysisresults.containertypeslist is not None:
            if len(self.analysisresults.containertypeslist) > 0:
                # archive file types
                self.__outputtable__(
                    self.analysisresults.containertypeslist,
                    self.STRINGS.HEADING_ARCHIVE_FORMATS,
                    self.STRINGS.HEADING_DESC_ARCHIVE_FORMATS,
                    False,
                )

        if self.analysisresults.hashused is True:
            if self.analysisresults.duplicateHASHlisting is not None:
                # Duplicate Content
                self.__outputheading__(
                    "{} ({})".format(
                        self.STRINGS.HEADING_IDENTICAL_CONTENT,
                        self.analysisresults.totalHASHduplicates,
                    ),
                    "{} ({})".format(
                        self.STRINGS.HEADING_DESC_IDENTICAL_CONTENT,
                        self.analysisresults.totalHASHduplicates,
                    ),
                )
                for dupes in self.analysisresults.duplicateHASHlisting:
                    self.printFormattedText(
                        "<b>{}</b> Count: {}<br/><br/>".format(
                            dupes["checksum"], dupes["count"]
                        )
                    )
                    self.printFormattedText("<code>")
                    for ex in dupes["examples"]:
                        try:
                            text = u"{}<br/>".format(ex.decode("utf8"))
                        except (AttributeError, UnicodeEncodeError):
                            text = u"{}<br/>".format(ex)
                        self.printFormattedText(text)
                    self.printFormattedText("</code>")
                    self.__htmlnewline__()

                self.printFormattedText("<hr/>")

        if self.analysisresults.badFileNames is not None:
            if len(self.analysisresults.badFileNames) > 0:
                # Troublesome Filenames
                self.__outputheading__(
                    self.STRINGS.HEADING_TROUBLESOME_FILENAMES,
                    self.STRINGS.HEADING_DESC_TROUBLESOME_FILENAMES,
                )
                for fnames in self.analysisresults.badFileNames:
                    self.printFormattedText(fnames)
                    self.__htmlnewline__(2)
                self.printFormattedText("<hr/>")

        if self.analysisresults.badDirNames is not None:
            if len(self.analysisresults.badDirNames) > 0:
                # Troublesome Filenames
                self.__outputheading__(
                    self.STRINGS.HEADING_TROUBLESOME_DIRNAMES,
                    self.STRINGS.HEADING_DESC_TROUBLESOME_DIRNAMES,
                )
                for fnames in self.analysisresults.badDirNames:
                    self.printFormattedText(fnames)
                    self.__htmlnewline__(2)
                self.printFormattedText("<hr/>")

        if self.analysisresults.denylist is True:
            if self.analysisresults.denylist_ids:
                self.__outputtable__(
                    self.analysisresults.denylist_ids,
                    self.STRINGS.HEADING_DENYLIST_IDS,
                    self.STRINGS.HEADING_DESC_DENYLIST,
                    True,
                    1,
                    "800",
                )
            if self.analysisresults.denylist_exts:
                self.__outputtable__(
                    self.analysisresults.denylist_exts,
                    self.STRINGS.HEADING_DENYLIST_EXTS,
                    self.STRINGS.HEADING_DESC_DENYLIST,
                    True,
                    3,
                    "260",
                )
            if self.analysisresults.denylist_filenames:
                self.__outputtable__(
                    self.analysisresults.denylist_filenames,
                    self.STRINGS.HEADING_DENYLIST_FILENAMES,
                    self.STRINGS.HEADING_DESC_DENYLIST,
                    True,
                    1,
                    "800",
                )
            if self.analysisresults.denylist_directories:
                self.__outputtable__(
                    self.analysisresults.denylist_directories,
                    self.STRINGS.HEADING_DENYLIST_DIRS,
                    self.STRINGS.HEADING_DESC_DENYLIST,
                    True,
                    1,
                    "800",
                )

        if self.analysisresults.errorlist:
            self.__outputtable__(
                self.analysisresults.errorlist,
                self.STRINGS.HEADING_ERRORS,
                self.STRINGS.HEADING_DESC_ERRORS,
                True,
                1,
                "800",
            )

        self.__htmlnewline__()
        self.printFormattedText("</body>")
