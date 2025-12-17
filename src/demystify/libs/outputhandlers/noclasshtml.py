# -*- coding: utf-8 -*-

import html as html_lib
import logging
import re
from typing import Final

try:
    from src.demystify.libs import DemystifyAnalysisClass
    from src.demystify.libs.AnalysisResultsClass import AnalysisResults
except ModuleNotFoundError:
    # Needed to run from root dir.
    from demystify.libs import DemystifyAnalysisClass
    from demystify.libs.AnalysisResultsClass import AnalysisResults


try:
    from i18n.internationalstrings import AnalysisStringsEN as strings
except ModuleNotFoundError:
    try:
        from src.demystify.i18n.internationalstrings import AnalysisStringsEN as strings
    except ModuleNotFoundError:
        from demystify.i18n.internationalstrings import AnalysisStringsEN as strings

logger = logging.getLogger(__name__)


NONE_REPLACE_DEBUG = "Replacing 'None': A field in the database is null because there is no data, replacing at the presentation later..."

contrast_switch: Final[
    str
] = """
<!-- contrast switcher via: https://github.com/picocss/pico/discussions/381#discussioncomment-11341046 -->

<div><p>
    <button class="outline" onclick="document.documentElement.setAttribute('data-theme', document.documentElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light')">
    <div style="width:26px;height:246x;">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 32 32" fill="currentColor" class="icon-theme-toggle theme-toggle moon">
            <clipPath id="theme-toggle-cutout">
                <path d="M0-11h25a1 1 0 0017 13v30H0Z"></path>
            </clipPath>
            <g clip-path="url(#theme-toggle-cutout)">
                <circle cx="16" cy="16" r="8.4"></circle>
                <path d="M18.3 3.2c0 1.3-1 2.3-2.3 2.3s-2.3-1-2.3-2.3S14.7.9 16 .9s2.3 1 2.3 2.3zm-4.6 25.6c0-1.3 1-2.3 2.3-2.3s2.3 1 2.3 2.3-1 2.3-2.3 2.3-2.3-1-2.3-2.3zm15.1-10.5c-1.3 0-2.3-1-2.3-2.3s1-2.3 2.3-2.3 2.3 1 2.3 2.3-1 2.3-2.3 2.3zM3.2 13.7c1.3 0 2.3 1 2.3 2.3s-1 2.3-2.3 2.3S.9 17.3.9 16s1-2.3 2.3-2.3zm5.8-7C9 7.9 7.9 9 6.7 9S4.4 8 4.4 6.7s1-2.3 2.3-2.3S9 5.4 9 6.7zm16.3 21c-1.3 0-2.3-1-2.3-2.3s1-2.3 2.3-2.3 2.3 1 2.3 2.3-1 2.3-2.3 2.3zm2.4-21c0 1.3-1 2.3-2.3 2.3S23 7.9 23 6.7s1-2.3 2.3-2.3 2.4 1 2.4 2.3zM6.7 23C8 23 9 24 9 25.3s-1 2.3-2.3 2.3-2.3-1-2.3-2.3 1-2.3 2.3-2.3z"></path>
            </g>
        </svg>
    </div>
    </button>
</p></div>
"""


def html_header(htm_string: str, analysis_results: AnalysisResults):
    """Output the HTML header."""

    htm_string = make_text(htm_string=htm_string, text="<!DOCTYPE html>")
    htm_string = make_text(htm_string=htm_string, text="<html lang='en'>")
    htm_string = make_text(htm_string=htm_string, text="<head>")
    if analysis_results.tooltype != "droid":
        htm_string = make_text(
            htm_string=htm_string, text=f"<title>{strings.REPORT_TITLE_SF}</title>"
        )
    else:
        htm_string = make_text(
            htm_string=htm_string, text=f"<title>{strings.REPORT_TITLE_DR}</title>"
        )

    htm_string = make_text(
        htm_string=htm_string,
        text="<meta http-equiv='Content-Type' content='text/html; charset=utf-8'>",
    )
    htm_string = make_text(
        htm_string=htm_string,
        text="<link rel=\"icon\" href=\"data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2016%2016'%3E%3Ctext%20x='0'%20y='14'%3E🕵️%3C/text%3E%3C/svg%3E\" type=\"image/svg+xml\">",
    )

    style = """
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.css" type="text/css">
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.lime.min.css">
      <style>
         @media print
         {
            details > summary {
                display: none !important;
            }
            details::details-content {
                border: none  !important;;
                content-visibility: visible;
                height: auto !important;
                font-size: smaller;
            }
         }
      </style>
    """
    htm_string = make_text(htm_string=htm_string, text=style)
    htm_string = make_text(htm_string=htm_string, text="</head>")
    return htm_string


def remove_none(old_list: list, format_unknown: bool = False) -> list:
    """Remove `None` from the given list of tuples."""
    new_list = []
    for item in old_list:
        if item[1] == "None":
            if not format_unknown:
                new_list.append((item[0], ""))
                continue
            new_list.append((item[0], "Format name is unknown"))
        else:
            new_list.append((item[0], item[1]))
    return new_list


def make_text(htm_string: str, text: str):
    res = f"{htm_string}"
    if isinstance(text, list):
        for txt in text:
            res = f"{res}{txt}</br>\n"
        res = f"{res}\n"
        return res
    res = f"{res}{text}\n"
    return res


def make_summary(text: str):
    """Todo..."""
    return f"<details class='noprint'>\n<summary role='button' class='outline primary'>\n{strings.REPORT_MORE_INFORMATION}\n</summary>\n<p>\n{text}\n</p>\n</details>\n"


def make_list_item(title, content, value):
    """Todo..."""
    return f'<li title="{title}">{content}: {value}</li>\n'


def printHTMLResults(self):
    self.generateHTML()
    return self.htmloutput


def split_id_results(puid):
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


def output_meter(value: int, min: int, max: int) -> str:
    """Todo..."""
    return f"<td><meter style='width: 100%;' value='{str(value).strip()}' min='{min}' max='{max}'>&nbsp;METER VISUALISATION AVAILABLE IN GOOGLE CHROME&nbsp;</meter></td>"


def make_offset_text(title: str, statistic: list):
    """Generate offset text.

    Data input should look as follows:

        * ['id','basis','filename','filesize','offset']
    """

    example = f"<br><br><code>{statistic[0]}, {statistic[1]} e.g. {statistic[2]} filesize: {statistic[3]}. {statistic[4]} bytes</code><br>\n"
    return f"<b>{title}: </b>{example}"


def identifier_chart(
    analysis_results: AnalysisResults, count_list: list, reverse_list=True
):
    """Todo..."""
    count_list.sort(key=lambda tup: tup[1], reverse=reverse_list)
    htm_string = f"{output_heading(strings.HEADING_FREQUENCY_PUIDS_IDENTIFIED, strings.HEADING_DESC_FREQUENCY_PUIDS_IDENTIFIED)}"
    htm_string = (
        f"{htm_string}<table><tr>"
        f"<th>{strings.COLUMN_HEADER_VALUES_ID}</th>"
        f"<th>{strings.COLUMN_HEADER_VALUES_COUNT}</th>"
        f"<th>{strings.COLUMN_HEADER_VALUES_YEAR}</th></tr>"
    )
    for sig in count_list:
        htm_string = f"{htm_string}<tr><td>"
        if "fmt/" in sig[0]:
            url = f"<a target='_blank' href='https://nationalarchives.gov.uk/PRONOM/{sig[0]}'>{sig[0]}</a>"
            htm_string = f"\n{htm_string}{url}\n"
        else:
            htm_string = make_text(htm_string, sig[0])
        htm_string = f"{htm_string}</td><td>{str(sig[1]).strip()}</td>"
        meter = output_meter(sig[1], 0, analysis_results.filecount)
        htm_string = f"{htm_string}{meter}"
        htm_string = f"{htm_string}</tr>"
    htm_string = f"{htm_string}</table>"
    return htm_string


def namespace_stats(analysis_results: AnalysisResults):
    """Todo..."""
    # e.g.{'binary method count': '57', 'text method count': '37', 'namespace title': 'freedesktop.org',
    # 'filename method count': '45', 'namespace details': 'freedesktop.org.xml'}

    nsdatalist = analysis_results.nsdatalist
    signaturefrequency = analysis_results.signatureidentifiedfrequency

    try:
        demystify = DemystifyAnalysisClass.DemystifyBase()
    except DemystifyAnalysisClass.AnalysisError:
        logging.error(
            "There shouldn't be a new DemystifyAnalysis object here: not performing NS work..."
        )
        return

    htm_string = ""

    for ns in nsdatalist:
        signatureids = signaturefrequency
        nstitle = ns[demystify.NS_CONST_TITLE]
        identified = ns[demystify.NS_CONST_BINARY_COUNT]
        xmlid = ns[demystify.NS_CONST_XML_COUNT]
        text = ns[demystify.NS_CONST_TEXT_COUNT]
        filename = ns[demystify.NS_CONST_FILENAME_COUNT]
        ext = ns[demystify.NS_CONST_EXTENSION_COUNT]
        unidentified = analysis_results.filecount - identified
        percent_not = demystify.calculatePercent(
            analysis_results.filecount, unidentified
        )
        percent_ok = demystify.calculatePercent(analysis_results.filecount, identified)

        list_val = make_list_item(
            strings.HEADING_DESC_NAMESPACE,
            f"<b>{strings.HEADING_NAMESPACE}</b>",
            f"<i>{nstitle} ({ns[demystify.NS_CONST_DETAILS]})</i>",
        )

        htm_string = f"{htm_string}<ul>{list_val}"

        list_val = make_list_item(
            strings.SUMMARY_DESC_IDENTIFIED_FILES,
            strings.SUMMARY_IDENTIFIED_FILES,
            str(identified),
        )

        htm_string = f"{htm_string}{list_val}"

        list_val = make_list_item(
            strings.SUMMARY_DESC_MULTIPLE,
            strings.SUMMARY_MULTIPLE,
            str(ns[demystify.NS_CONST_MULTIPLE_IDS]),
        )

        htm_string = f"{htm_string}{list_val}"

        list_val = make_list_item(
            strings.SUMMARY_DESC_UNIDENTIFIED,
            strings.SUMMARY_UNIDENTIFIED,
            str(unidentified),
        )

        htm_string = f"{htm_string}{list_val}"

        list_val = make_list_item(
            strings.SUMMARY_DESC_EXTENSION_ID,
            strings.SUMMARY_EXTENSION_ID,
            str(ext),
        )

        htm_string = f"{htm_string}{list_val}"

        if analysis_results.tooltype != "droid":

            list_val = make_list_item(
                strings.SUMMARY_DESC_XML_ID,
                strings.SUMMARY_XML_ID,
                str(xmlid),
            )

            htm_string = f"{htm_string}{list_val}"

            list_val = make_list_item(
                strings.SUMMARY_DESC_TEXT_ID,
                strings.SUMMARY_TEXT_ID,
                str(text),
            )

            htm_string = f"{htm_string}{list_val}"

            list_val = make_list_item(
                strings.SUMMARY_DESC_FILENAME_ID,
                strings.SUMMARY_FILENAME_ID,
                str(filename),
            )

            htm_string = f"{htm_string}{list_val}"

        list_val = make_list_item(
            strings.SUMMARY_DESC_PERCENTAGE_IDENTIFIED,
            strings.SUMMARY_PERCENTAGE_IDENTIFIED,
            str(percent_ok),
        )

        htm_string = f"{htm_string}{list_val}"

        list_val = make_list_item(
            strings.SUMMARY_DESC_PERCENTAGE_UNIDENTIFIED,
            strings.SUMMARY_PERCENTAGE_UNIDENTIFIED,
            str(percent_not),
        )

        htm_string = f"{htm_string}{list_val}</ul>"

        nslist = []
        for idrow in signatureids:
            if idrow[0] == nstitle:
                nslist.append(idrow[1:])
        table = output_table(
            listing=nslist,
            heading=None,
            description=None,
            count=True,
            maxcolumns=2,
        )
        htm_string = f"{htm_string}{table}"
    return htm_string


def remove_namespace_id(old_list: str):
    """Todo..."""
    new_list = []
    for item in old_list:
        new_list.append(str(item[0]))
    return new_list


def output_heading(heading, description):
    """Output an analysis heading and its detailed description."""
    htm_string = f"<h2>{heading}</h2>"
    htm_string = f"{htm_string}{make_summary(description)}\n"
    return htm_string


def output_table(
    listing: list,
    heading: str,
    description: str,
    count: bool = True,
    maxcolumns: int = 5,
):
    htm_string = ""
    if heading is not None and description is not None:
        htm_string = output_heading(heading, description)
    list_len = len(listing)
    rows = int(list_len / 5)
    if list_len % 5 > 0:
        rows = rows + 1
    rowno = 0
    colno = 0
    htm_string = f"{htm_string}<table><tr>"
    for item in listing:
        value = ""
        if ", None" in item:
            logging.debug(
                "replacing `None` a field in the database is null", NONE_REPLACE_DEBUG
            )
            item = item.replace(", None", "")
        if isinstance(item, str):
            value = item
        elif len(item) == 1:
            value = str(item[0])
        elif count is False:
            if item[1] == "":
                value = f"{item[0]}, Format name is unknown"
            else:
                value = f"{item[0]}, {item[1]}"
        else:
            value = f"{item[0]} ({item[1]})"
        if colno < maxcolumns:
            htm_string = f"{htm_string}<td><code>{value}</code></td>"
            colno = colno + 1
        else:
            rowno = rowno + 1
            htm_string = f"{htm_string}</tr><tr>"
            htm_string = f"{htm_string}<td><code>{value}</code></td>"
            colno = 1

    if not colno < maxcolumns:
        htm_string = f"{htm_string}</tr></table>"
        return htm_string
    for td in range(maxcolumns - colno):
        htm_string = f"{htm_string}<td>&nbsp;</td>"
    htm_string = f"{htm_string}</tr></table>"
    return htm_string


def report_metadata(analysis_results: AnalysisResults):
    """Output report metadata."""
    htm_string = ""
    if analysis_results.tooltype != "droid":
        htm_string = make_text(
            htm_string,
            f"<h1>{strings.REPORT_TITLE_SF}</h1>\n",
        )
    else:
        htm_string = make_text(
            htm_string,
            f"<h1>{strings.REPORT_TITLE_DR}</h1>\n",
        )
    htm_string = make_text(
        htm_string,
        f"<b>{strings.REPORT_VERSION}: </b>{analysis_results.__version__()}<br>\n",
    )

    htm_string = make_text(
        htm_string,
        f"<b>{strings.REPORT_FILE}: </b>{analysis_results.filename}<br>\n",
    )

    htm_string = make_text(
        htm_string,
        f"<b>{strings.REPORT_TOOL}: </b>{analysis_results.tooltype}<br>\n",
    )

    htm_string = make_text(
        htm_string,
        f"<b>{strings.NAMESPACES}: </b>{analysis_results.namespacecount}<br>\n",
    )

    return htm_string


def report_distance_scanned(analysis_results: AnalysisResults) -> str:
    """For Siegfried and to understand how much data we're scanning
    when identifying files, we can output the number of bytes
    read. This can be useful for signature development."""
    if not analysis_results.bof_distance:
        return ""
    htm_string = make_offset_text(
        title=strings.SUMMARY_DISTANCE_BOF, statistic=analysis_results.bof_distance
    )
    if not analysis_results.eof_distance:
        return htm_string
    offset_text = make_offset_text(
        title=strings.SUMMARY_DISTANCE_EOF, statistic=analysis_results.eof_distance
    )
    htm_string = f"{htm_string}<br>{offset_text}"
    return htm_string


def non_droid_id_type_summary(analysis_results: AnalysisResults):
    """Todo..."""
    htm_string = ""
    htm_string = make_text(
        htm_string,
        make_list_item(
            strings.SUMMARY_DESC_XML_ID,
            strings.SUMMARY_XML_ID,
            analysis_results.xmlidfilecount,
        ),
    )
    htm_string = make_text(
        htm_string,
        make_list_item(
            strings.SUMMARY_DESC_TEXT_ID,
            strings.SUMMARY_TEXT_ID,
            analysis_results.textidfilecount,
        ),
    )
    htm_string = make_text(
        htm_string,
        make_list_item(
            strings.SUMMARY_DESC_FILENAME_ID,
            strings.SUMMARY_FILENAME_ID,
            analysis_results.filenameidfilecount,
        ),
    )
    return htm_string


def non_droid_id_type_detailed_summary(analysis_results: AnalysisResults):
    """Todo..."""
    htm_string = ""
    htm_string = make_text(
        htm_string,
        make_list_item(
            strings.SUMMARY_DESC_OTHER_ID_COUNT,
            strings.SUMMARY_OTHER_ID_COUNT,
            analysis_results.distinctOtherIdentifiers,
        ),
    )
    htm_string = make_text(
        htm_string,
        make_list_item(
            strings.SUMMARY_DESC_XML_ID_COUNT,
            strings.SUMMARY_XML_ID_COUNT,
            analysis_results.distinctXMLIdentifiers,
        ),
    )
    htm_string = make_text(
        htm_string,
        make_list_item(
            strings.SUMMARY_DESC_TEXT_ID_COUNT,
            strings.SUMMARY_TEXT_ID_COUNT,
            analysis_results.distinctTextIdentifiers,
        ),
    )
    htm_string = make_text(
        htm_string,
        make_list_item(
            strings.SUMMARY_DESC_FILENAME_ID_COUNT,
            strings.SUMMARY_FILENAME_ID_COUNT,
            analysis_results.distinctFilenameIdentifiers,
        ),
    )
    return htm_string


def report_summary(analysis_results: AnalysisResults) -> str:
    """Todo..."""

    htm_string = ""

    htm_string = make_text(
        htm_string,
        "<h2>{}</h2>".format(strings.REPORT_SUMMARY),
    )

    htm_string = make_text(
        htm_string,
        "<ul>",
    )

    htm_string = make_text(
        htm_string,
        make_list_item(
            strings.SUMMARY_DESC_TOTAL_FILES,
            strings.SUMMARY_TOTAL_FILES,
            analysis_results.filecount,
        ),
    )
    htm_string = make_text(
        htm_string,
        make_list_item(
            strings.SUMMARY_DESC_ARCHIVE_FILES,
            strings.SUMMARY_ARCHIVE_FILES,
            analysis_results.containercount,
        ),
    )

    # even if we have archive files, if the analysis isn't on, we
    # can't output this value
    if analysis_results.filesincontainercount > 0:
        htm_string = make_text(
            htm_string,
            make_list_item(
                strings.SUMMARY_DESC_INSIDE_ARCHIVES,
                strings.SUMMARY_INSIDE_ARCHIVES,
                analysis_results.filesincontainercount,
            ),
        )

    htm_string = make_text(
        htm_string,
        make_list_item(
            strings.SUMMARY_DESC_DIRECTORIES,
            strings.SUMMARY_DIRECTORIES,
            analysis_results.directoryCount,
        ),
    )
    htm_string = make_text(
        htm_string,
        make_list_item(
            strings.SUMMARY_DESC_UNIQUE_DIRNAMES,
            strings.SUMMARY_UNIQUE_DIRNAMES,
            analysis_results.uniqueDirectoryNames,
        ),
    )
    htm_string = make_text(
        htm_string,
        make_list_item(
            strings.SUMMARY_DESC_IDENTIFIED_FILES,
            strings.SUMMARY_IDENTIFIED_FILES,
            analysis_results.identifiedfilecount,
        ),
    )
    htm_string = make_text(
        htm_string,
        make_list_item(
            strings.SUMMARY_DESC_MULTIPLE,
            strings.SUMMARY_MULTIPLE,
            analysis_results.multipleidentificationcount,
        ),
    )
    htm_string = make_text(
        htm_string,
        make_list_item(
            strings.SUMMARY_DESC_UNIDENTIFIED,
            strings.SUMMARY_UNIDENTIFIED,
            analysis_results.unidentifiedfilecount,
        ),
    )

    if analysis_results.tooltype != "droid":
        # TODO: verify function name...
        non_droid_id = non_droid_id_type_summary(analysis_results)
        htm_string = f"{htm_string}{non_droid_id}"

    htm_string = make_text(
        htm_string,
        make_list_item(
            strings.SUMMARY_DESC_EXTENSION_ID,
            strings.SUMMARY_EXTENSION_ID,
            analysis_results.extensionIDOnlyCount,
        ),
    )
    htm_string = make_text(
        htm_string,
        make_list_item(
            strings.SUMMARY_DESC_EXTENSION_MISMATCH,
            strings.SUMMARY_EXTENSION_MISMATCH,
            analysis_results.extmismatchCount,
        ),
    )
    htm_string = make_text(
        htm_string,
        make_list_item(
            strings.SUMMARY_DESC_ID_PUID_COUNT,
            strings.SUMMARY_ID_PUID_COUNT,
            analysis_results.distinctSignaturePuidcount,
        ),
    )

    if analysis_results.tooltype != "droid":
        # TODO: verify function name...
        non_droid_id = non_droid_id_type_detailed_summary(analysis_results)
        htm_string = f"{htm_string}{non_droid_id}"

    htm_string = make_text(
        htm_string,
        make_list_item(
            strings.SUMMARY_DESC_UNIQUE_EXTENSIONS,
            strings.SUMMARY_UNIQUE_EXTENSIONS,
            analysis_results.distinctextensioncount,
        ),
    )
    htm_string = make_text(
        htm_string,
        make_list_item(
            strings.SUMMARY_DESC_ZERO_BYTE,
            strings.SUMMARY_ZERO_BYTE,
            analysis_results.zerobytecount,
        ),
    )

    if analysis_results.hashused is True:
        htm_string = make_text(
            htm_string,
            make_list_item(
                strings.SUMMARY_DESC_IDENTICAL_FILES,
                strings.SUMMARY_IDENTICAL_FILES,
                analysis_results.totalHASHduplicates,
            ),
        )

    htm_string = make_text(
        htm_string,
        make_list_item(
            strings.SUMMARY_DESC_PERCENTAGE_IDENTIFIED,
            strings.SUMMARY_PERCENTAGE_IDENTIFIED,
            analysis_results.identifiedPercentage,
        ),
    )
    htm_string = make_text(
        htm_string,
        make_list_item(
            strings.SUMMARY_DESC_PERCENTAGE_UNIDENTIFIED,
            strings.SUMMARY_PERCENTAGE_UNIDENTIFIED,
            analysis_results.unidentifiedPercentage,
        ),
    )

    if (
        analysis_results.namespacecount > 1
        and analysis_results.identificationgaps is not None
    ):
        htm_string = make_text(
            htm_string,
            make_list_item(
                strings.SUMMARY_DESC_GAPS_COVERED,
                strings.SUMMARY_GAPS_COVERED,
                analysis_results.identificationgaps,
            ),
        )

    htm_string = make_text(
        htm_string,
        "</ul>",
    )

    return htm_string


def report_size(analysis_results: AnalysisResults) -> str:
    """Output the size of the collection we have profiled. Size is
    calculated as: MiB/MB = (2^1024)*2.
    """
    htm_string = ""
    htm_string = output_heading(strings.HEADING_SIZE, strings.HEADING_DESC_SIZE)
    htm_string = make_text(
        htm_string,
        f"{float(analysis_results.collectionsize)} bytes | {round(float(float(analysis_results.collectionsize) / (1048576)), 1)} MiB/MB (Megabytes)",
    )
    return htm_string


def report_identifiers(analysis_results: AnalysisResults) -> str:
    """Todo..."""
    if analysis_results.signatureidentifiers is None:
        return ""
    signature_id_list = []
    count_list = []
    for puid in analysis_results.signatureidentifiers:
        namespace, identifier, formatname, count = split_id_results(puid)
        count_list.append((identifier, int(count)))
        signature_id_list.append((namespace, identifier, formatname, int(count)))
    logger.info(len(count_list))
    chart = identifier_chart(analysis_results, count_list)
    return chart


def report_format_classification(analysis_results: AnalysisResults) -> str:
    """TOdo...."""
    if not analysis_results.classifications_count > 0:
        return ""
    htm_string = output_heading(
        strings.HEADING_CLASSIFICATION, strings.HEADING_DESC_CLASSIFICATION
    )
    htm_string = (
        f"{htm_string}<table><tr>"
        f"<th>{strings.COLUMN_HEADER_VALUES_CLASSIFICATION}</th>"
        f"<th>{strings.COLUMN_HEADER_VALUES_COUNT}</th></tr>"
    )
    for format_classification in analysis_results.classifications:
        try:
            classification = format_classification[0]
        except IndexError as err:
            logger.error("cannot access format classification: %s", err)
            return ""
        if classification.lower() == "none":
            classification = "No format type classification"
        htm_string = f"{htm_string}<tr><td>"
        htm_string = f"{htm_string}{classification}"
        htm_string = f"{htm_string}</td><td>{format_classification[1]}</td>"
        meter = output_meter(format_classification[1], 0, analysis_results.filecount)
        htm_string = f"{htm_string}{meter}</tr>"
    htm_string = f"{htm_string}</table>\n"
    return htm_string


def report_date_range(analysis_results: AnalysisResults) -> str:
    """Todo..."""
    if analysis_results.dateFrequency is None:
        return ""
    # Date Ranges
    htm_string = output_heading(
        strings.HEADING_DATE_RANGE, strings.HEADING_DESC_DATE_RANGE
    )
    htm_string = f"{htm_string}<table><tr><th>{strings.COLUMN_HEADER_VALUES_YEAR}</th><th>{strings.COLUMN_HEADER_VALUES_COUNT}</th><th>&nbsp;</th></tr>"

    for dates in analysis_results.dateFrequency:
        htm_string = f"{htm_string}<tr><td>"
        htm_string = f"{htm_string}<a target='_blank' href='https://en.wikipedia.org/wiki/{dates[0]}'>{dates[0]}</a>"
        htm_string = f"{htm_string}</td><td>{dates[1]}</td>"
        meter = output_meter(dates[1], 0, analysis_results.filecount)
        htm_string = f"{htm_string}{meter}</tr>"
    htm_string = f"{htm_string}</table>"
    return htm_string


def report_aggregated_ff_sigs(analysis_results: AnalysisResults) -> str:
    """Todo..."""

    if analysis_results.signatureidentifiers is None:
        return ""
    signature_id_list = []
    for puid in analysis_results.signatureidentifiers:
        namespace, identifier, formatname, count = split_id_results(puid)
        signature_id_list.append((namespace, identifier, formatname, int(count)))
    if not signature_id_list:
        return ""
    # Signature identified PUIDs in collection (signature and container)
    htm_string = output_heading(
        strings.HEADING_AGGREGATE_BINARY_IDENTIFIED, strings.HEADING_DESC_IDENTIFIED
    )
    htm_string = (
        f"{htm_string}<table><tr>"
        f"<th>{strings.COLUMN_HEADER_VALUES_ID}</th>"
        f"<th>{strings.COLUMN_HEADER_VALUES_NAMESPACE}</th>"
        f"<th>{strings.COLUMN_HEADER_VALUES_FORMAT}</th>"
        f"<th>{strings.COLUMN_HEADER_VALUES_COUNT}</th></tr>"
    )
    signature_id_list.sort(key=lambda keys: int(keys[3]), reverse=True)
    # Tuple object: (namespace, identifier, format name, int(count))
    #
    #   For example: ('ns:pronom fmt/19, Acrobat PDF 1.5 - Portable Document Format, 1.5 (6)', 1)
    #
    for id_ in signature_id_list:
        if "fmt/" in id_[1]:
            markup = (
                f"<tr><td>\n"
                f"<a target='_blank' href='https://nationalarchives.gov.uk/PRONOM/{id_[1]}'>{id_[1]}</a></td>\n"
            )
        else:
            markup = f"<tr><td>{id_[1]}</td>"
        markup = f"{markup}<td>{id_[0]}</td><td>{id_[2]}</td><td>{id_[3]}</td></tr>"
        htm_string = f"{htm_string}{markup}"
    htm_string = f"{htm_string}</table>"
    return htm_string


def report_aggregate_binary(analysis_results: AnalysisResults) -> str:
    """Todo..."""

    if not analysis_results.binaryidentifiers:
        return ""
    new_list = remove_namespace_id(analysis_results.binaryidentifiers)
    return output_table(
        listing=new_list,
        heading=strings.HEADING_BINARY_ID,
        description=strings.HEADING_DESC_BINARY_ID,
        count=True,
        maxcolumns=1,
    )


def report_aggregate_xml(analysis_results: AnalysisResults) -> str:
    """Todo..."""

    if not analysis_results.xmlidentifiers:
        return ""
    new_list = remove_namespace_id(analysis_results.xmlidentifiers)
    return output_table(
        listing=new_list,
        heading=strings.HEADING_XML_ID,
        description=strings.HEADING_DESC_XML_ID,
        count=True,
        maxcolumns=1,
    )


def report_aggregate_text(analysis_results: AnalysisResults) -> str:
    """Todo..."""

    if not analysis_results.textidentifiers:
        return ""
    new_list = remove_namespace_id(analysis_results.textidentifiers)
    return output_table(
        listing=new_list,
        heading=strings.HEADING_TEXT_ID,
        description=strings.HEADING_DESC_TEXT_ID,
        count=True,
        maxcolumns=1,
    )


def report_aggregate_filename(analysis_results: AnalysisResults) -> str:
    """Todo..."""

    if not analysis_results.filenameidentifiers:
        return ""
    new_list = remove_namespace_id(analysis_results.filenameidentifiers)
    return output_table(
        listing=new_list,
        heading=strings.HEADING_FILENAME_ID,
        description=strings.HEADING_DESC_FILENAME_ID,
        count=True,
        maxcolumns=1,
    )


def report_id_method_frequency(analysis_results: AnalysisResults) -> str:
    """TODO..."""
    if not analysis_results.idmethodFrequency:
        return ""
    return output_table(
        listing=analysis_results.idmethodFrequency,
        heading=strings.HEADING_ID_METHOD,
        description=strings.HEADING_DESC_ID_METHOD,
    )


def report_extension_only(analysis_results: AnalysisResults) -> str:
    """Todo..."""
    if not analysis_results.extensionOnlyIDList:
        return ""
    new_list = remove_none(analysis_results.extensionOnlyIDList)
    return output_table(
        listing=new_list,
        heading=strings.HEADING_EXTENSION_ONLY,
        description=strings.HEADING_DESC_EXTENSION_ONLY,
        count=False,
        maxcolumns=2,
    )


def report_frequency_extension_only(analysis_results: AnalysisResults) -> str:
    """Todo..."""

    if not analysis_results.extensionOnlyIDList:
        return ""
    if not len(analysis_results.extensionOnlyIDList) > 0:
        return ""
    # Extension Only Identification
    extlist = analysis_results.extensionOnlyIDList
    for item in list(extlist):
        if "unknown" in item[0].lower():
            extlist.remove(item)
            continue
        extlist = remove_none(old_list=extlist, format_unknown=True)
    if analysis_results.tooltype != "droid":
        # we have basis information so need a bigger table...
        return output_table(
            listing=extlist,
            heading=strings.HEADING_FREQUENCY_EXTENSION_ONLY,
            description=strings.HEADING_DESC_FREQUENCY_EXTENSION_ONLY,
            count=True,
            maxcolumns=2,
        )
    return output_table(
        listing=extlist,
        heading=strings.HEADING_FREQUENCY_EXTENSION_ONLY,
        description=strings.HEADING_DESC_FREQUENCY_EXTENSION_ONLY,
        count=True,
        maxcolumns=3,
    )


def report_frequency_all_extensions(analysis_results: AnalysisResults) -> str:
    """Todo..."""
    if not analysis_results.frequencyOfAllExtensions:
        return ""
    return output_table(
        listing=analysis_results.frequencyOfAllExtensions,
        heading=strings.HEADING_FREQUENCY_EXTENSIONS_ALL,
        description=strings.HEADING_DESC_FREQUENCY_EXTENSIONS_ALL,
    )


def report_all_unique_extensions(analysis_results: AnalysisResults) -> str:
    """Todo..."""
    if not analysis_results.uniqueExtensionsInCollectionList:
        return
    return output_table(
        listing=analysis_results.uniqueExtensionsInCollectionList,
        heading=strings.HEADING_UNIQUE_EXTENSIONS,
        description=strings.HEADING_DESC_UNIQUE_EXTENSIONS,
        count=False,
    )


def report_multiple_identification(analysis_results: AnalysisResults) -> str:
    """Todo..."""
    if not analysis_results.rogue_multiple_identification_list:
        return ""
    if not len(analysis_results.rogue_multiple_identification_list) > 0:
        return ""
    return output_table(
        listing=analysis_results.rogue_multiple_identification_list,
        heading=strings.HEADING_LIST_MULTIPLE,
        description=strings.HEADING_DESC_LIST_MULTIPLE,
        count=False,
        maxcolumns=1,
    )


def report_mimetypes(analysis_results: AnalysisResults) -> str:
    """Todo..."""

    if not analysis_results.mimetypeFrequency:
        return ""
    mimes = analysis_results.mimetypeFrequency
    for mime in list(mimes):
        if mime[0] != "":
            continue
        mimes.remove(mime)
    return output_table(
        listing=mimes,
        heading=strings.HEADING_FREQUENCY_MIME,
        description=strings.HEADING_DESC_FREQUENCY_MIME,
        count=True,
        maxcolumns=2,
    )


def report_results_per_identifier(analysis_results: AnalysisResults) -> str:
    """Todo..."""

    if not analysis_results.signatureidentifiedfrequency:
        return ""
    if not analysis_results.nsdatalist:
        return ""
    header = output_heading(
        strings.HEADING_NAMESPACE_SPECIFIC_STATISTICS,
        strings.HEADING_DESC_NAMESPACE_SPECIFIC_STATISTICS,
    )
    namespace_details = namespace_stats(
        analysis_results=analysis_results,
    )
    return f"{header}\n{namespace_details}\n"


def report_all_xml_identifiers(analysis_results: AnalysisResults) -> str:
    """Todo..."""
    if not analysis_results.xml_identifiers:
        return ""
    if not len(analysis_results.xml_identifiers) > 0:
        return ""
    return output_table(
        listing=analysis_results.xml_identifiers,
        heading=strings.HEADING_XML_ID_COMPLETE,
        description=strings.HEADING_DESC_XML_ID_COMPLETE,
        count=True,
        maxcolumns=1,
    )


def report_all_text_identifiers(analysis_results: AnalysisResults) -> str:
    """Todo..."""
    if not analysis_results.text_identifiers:
        return ""
    if not analysis_results.text_identifiers:
        return ""
    return output_table(
        listing=analysis_results.text_identifiers,
        heading=strings.HEADING_TEXT_ID_COMPLETE,
        description=strings.HEADING_DESC_TEXT_ID_COMPLETE,
        count=True,
        maxcolumns=1,
    )


def report_all_filename_identifiers(analysis_results: AnalysisResults) -> str:
    """Todo..."""
    if not analysis_results.filename_identifiers:
        return ""
    if not len(analysis_results.filename_identifiers) > 0:
        return ""
    return output_table(
        listing=analysis_results.filename_identifiers,
        heading=strings.HEADING_FILENAME_ID_COMPLETE,
        description=strings.HEADING_DESC_FILENAME_ID_COMPLETE,
        count=True,
        maxcolumns=1,
    )


def report_zero_byte_files(analysis_results: AnalysisResults) -> str:
    """Todo..."""

    if not analysis_results.zerobytelist:
        return ""
    if not len(analysis_results.zerobytelist):
        return ""
    return output_table(
        listing=analysis_results.zerobytelist,
        heading=strings.HEADING_LIST_ZERO_BYTES,
        description=strings.HEADING_DESC_LIST_ZERO_BYTES,
        count=False,
        maxcolumns=1,
    )


def report_aggregate_file_types(analysis_results: AnalysisResults) -> str:
    """Todo..."""
    if not analysis_results.containertypeslist:
        return ""
    if not len(analysis_results.containertypeslist) > 0:
        return ""
    return output_table(
        listing=analysis_results.containertypeslist,
        heading=strings.HEADING_ARCHIVE_FORMATS,
        description=strings.HEADING_DESC_ARCHIVE_FORMATS,
        count=False,
    )


def report_duplicates(analysis_results: AnalysisResults) -> str:
    """Todo..."""
    if not analysis_results.hashused:
        return ""
    if not analysis_results.duplicateHASHlisting:
        return ""
    htm_string = output_heading(
        heading=f"{strings.HEADING_IDENTICAL_CONTENT} ({analysis_results.totalHASHduplicates})",
        description=f"{strings.HEADING_DESC_IDENTICAL_CONTENT} ({analysis_results.totalHASHduplicates})",
    )
    for dupes in analysis_results.duplicateHASHlisting:
        htm_string = (
            f"{htm_string}<b>{dupes['checksum']}</b> Count: {dupes['count']}<br><br>\n"
        )
        htm_string = f"{htm_string}<pre>"
        for example in dupes["examples"]:
            try:
                text = f"{example.decode('UTF-8')}"
            except (AttributeError, UnicodeEncodeError):
                text = f"{example}"
            htm_string = f"{htm_string}{html_lib.escape(text)}\n"
        htm_string = f"{htm_string}</pre><br>\n"
    return htm_string


def report_non_ascii_file_names(analysis_results: AnalysisResults) -> str:
    """Todo..."""

    if not analysis_results.badFileNames:
        return ""
    if not len(analysis_results.badFileNames) > 0:
        return ""
    htm_string = output_heading(
        strings.HEADING_TROUBLESOME_FILENAMES,
        strings.HEADING_DESC_TROUBLESOME_FILENAMES,
    )
    for fname in analysis_results.badFileNames:
        fname = html_lib.escape(fname)
        fname = fname.replace("File:", "<b>File:</b>")
        htm_string = f"{htm_string}{fname}<br>\n"
    return htm_string


def report_non_ascii_directory_names(analysis_results: AnalysisResults) -> str:
    """Todo...."""
    if not analysis_results.badDirNames:
        return ""
    if not len(analysis_results.badDirNames) > 0:
        return ""
    htm_string = output_heading(
        strings.HEADING_TROUBLESOME_DIRNAMES,
        strings.HEADING_DESC_TROUBLESOME_DIRNAMES,
    )
    for fname in analysis_results.badDirNames:
        fname = html_lib.escape(fname)
        fname = fname.replace("Directory:", "<b>Directory:</b>")
        htm_string = f"{htm_string}{fname}<br>\n"
    return htm_string


def report_denylist_ids(analysis_results: AnalysisResults) -> str:
    """Todo..."""
    if not analysis_results.denylist:
        return ""
    if not analysis_results.denylist_ids:
        return ""
    return output_table(
        listing=analysis_results.denylist_ids,
        heading=strings.HEADING_DENYLIST_IDS,
        description=strings.HEADING_DESC_DENYLIST,
        count=True,
        maxcolumns=1,
    )


def report_denylist_extensions(analysis_results: AnalysisResults) -> str:
    """Todo..."""
    if not analysis_results.denylist:
        return ""
    if not analysis_results.denylist_exts:
        return ""
    return output_table(
        listing=analysis_results.denylist_exts,
        heading=strings.HEADING_DENYLIST_EXTS,
        description=strings.HEADING_DESC_DENYLIST,
        count=True,
        maxcolumns=3,
    )


def report_denylist_filenames(analysis_results: AnalysisResults) -> str:
    """Todo..."""
    if not analysis_results.denylist:
        return ""
    if not analysis_results.denylist_filenames:
        return ""
    return output_table(
        listing=analysis_results.denylist_filenames,
        heading=strings.HEADING_DENYLIST_FILENAMES,
        description=strings.HEADING_DESC_DENYLIST,
        count=True,
        maxcolumns=1,
    )


def report_denylist_directories(analysis_results: AnalysisResults) -> str:
    """Todo..."""
    if not analysis_results.denylist:
        return ""
    if not analysis_results.denylist_directories:
        return ""
    return output_table(
        listing=analysis_results.denylist_directories,
        heading=strings.HEADING_DENYLIST_DIRS,
        description=strings.HEADING_DESC_DENYLIST,
        count=True,
        maxcolumns=1,
    )


def report_error_list(analysis_results: AnalysisResults) -> str:
    """Todo..."""
    if not analysis_results.errorlist:
        return ""
    return output_table(
        listing=analysis_results.errorlist,
        heading=strings.HEADING_ERRORS,
        description=strings.HEADING_DESC_ERRORS,
        count=True,
        maxcolumns=1,
    )


SECTIONS = [
    report_metadata,
    report_distance_scanned,
    report_summary,
    report_size,
    report_identifiers,
    report_format_classification,
    report_date_range,
    report_aggregated_ff_sigs,
    report_aggregate_binary,
    report_aggregate_xml,
    report_aggregate_text,
    report_aggregate_filename,
    report_id_method_frequency,
    report_extension_only,
    report_frequency_extension_only,
    report_frequency_all_extensions,
    report_all_unique_extensions,
    report_multiple_identification,
    report_mimetypes,
    report_results_per_identifier,
    report_all_xml_identifiers,
    report_all_text_identifiers,
    report_all_filename_identifiers,
    report_zero_byte_files,
    report_aggregate_file_types,
    report_duplicates,
    report_non_ascii_file_names,
    report_non_ascii_directory_names,
    report_denylist_ids,
    report_denylist_extensions,
    report_denylist_filenames,
    report_denylist_directories,
    report_error_list,
]


def html_body(htm_string: str, analysis_results: AnalysisResults):
    """Output the HTML body."""

    htm_string = make_text(
        htm_string,
        "<body>\n<main class='container' style='width: 1000px;'>\n",
    )

    for section in SECTIONS:
        analysis_htm = section(analysis_results)
        if analysis_htm == "":
            continue
        htm_string = f"{htm_string}{analysis_htm}"
        htm_string = f"{htm_string}\n<hr>\n"

    htm_string = make_text(
        htm_string,
        "</main>\n</body>\n",
    )

    return htm_string


def html(analysis_results: AnalysisResults):
    """Output a HTML report."""

    logger.info("outputting clean html")

    htm_string = ""

    htm_string = html_header(htm_string, analysis_results)
    htm_string = html_body(htm_string, analysis_results)

    return htm_string
