# -*- coding: utf-8 -*-

"""Demystify

Demystify is a utility for static analysis of file format identification
tool results. The utility analyses all aspects of a format
identification result from filename to the checksums to provide
de-duplication reporting. In sum total demystify:

   * Analyses directory and file names for characters that may need to
     be looked after differently in a digital preservation workflow.
   * Provides de-duplication reporting based on different checksum
     algorithm outputs.
   * Charts the most frequent formats in a report and helps to visualize
     the long tail.
   * Identifies other issues with a format identification, e.g.
     extension only results and multiple-IDs.
   * Summarizes your results as best as possible.

The features were extended with the help of colleague and friend AKB
(Andrea K. Byrne) to include rogues output. Rogues output is a way of
filtering on more information relevant to your institution, e.g. if
your workplaces is one of those rare entities that want to filter on
.ds_store objects. Those results will be presented in reports and
rsync style lists for filtering on disk.
"""

import argparse
import logging
import os
import sys
import time

LOGFORMAT = (
    "%(asctime)-15s %(levelname)s: %(filename)s:%(lineno)s:%(funcName)s(): %(message)s"
)
DATEFORMAT = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(format=LOGFORMAT, datefmt=DATEFORMAT, level="INFO")

import configparser as ConfigParser

from .libs.DemystifyAnalysisClass import AnalysisError, DemystifyAnalysis
from .libs.HandleDenylistClass import HandleDenylist
from .libs.IdentifyDatabase import IdentifyDB

# Custom output handlers
from .libs.outputhandlers.htmloutputclass import FormatAnalysisHTMLOutput
from .libs.outputhandlers.roguesgalleryoutputclass import rogueoutputclass
from .libs.outputhandlers.textoutputclass import FormatAnalysisTextOutput
from .sqlitefid.src.sqlitefid import sqlitefid

# Don't write .pyc files.
sys.dont_write_bytecode = True


class DenyListError(Exception):
    """An exception for when denylist is being used incorrectly."""


def get_config():
    """Retrieve overall configuration for the utility.

    :return: Configuration object with global configuration for
        Demystify (ConfigParser) or None (NoneType)
    """
    CONFIG = "config.cfg"
    if not os.path.isfile(CONFIG):
        logging.error("Not using config config file doesn't exist: %s", CONFIG)
        return None
    config = ConfigParser.ConfigParser()
    config.read(CONFIG)
    return config


def _handle_denylist_config() -> tuple:
    """Reads the denylist configuration and provides feedback to the
    caller when this option has been invoked but a denylist isn't
    available.

    :return: (Denylist (dict), Config Object (ConfigParser)) (Tuple)

    :raises: DenyListError if this function is invoked but there isn't a
        denylist available to be used.
    """
    DENYLIST = "denylist.cfg"
    denylist_path = os.path.join(os.getcwd(), DENYLIST)
    if not os.path.isfile(denylist_path):
        raise DenyListError(
            f"denylist doesn't exist, ensure that a {DENYLIST} file exists in the directory you are calling demystify from. Pipe `--denylist_template` to a file to create a baseline"
        )
    config = ConfigParser.RawConfigParser()
    config.read(denylist_path)
    denylist = HandleDenylist().denylist(config)
    return denylist, config


def handle_output(
    analysis_results, txtout=False, rogues=False, heroes=False, rogueconfig=None
):
    """Handle output from the analysis.

    :param analysis_results: Object containing all of our analysis
        results (AnalysisResults)
    :param txtout: Output text (True) vs. HTML (False) (Bool)
    :param rogues: Output rogues gallery output for rsync (Bool)
    :param heroes: Output heroes gallery output for rsync (Bool)

    :return: None (Nonetype)
    """
    ROGUES_TEXT = (
        "Rogues and Heroes output. "
        "Rogues and Heroes analysis is still in its early BETA stages. "
        "Please report any feedback you have around its accuracy and helpfulness. "
        "The feedback received will help improve the feature."
    )

    if txtout is True:
        logging.info("Outputting text report")
        textoutput = FormatAnalysisTextOutput(analysis_results)
        print(textoutput.printTextResults())
    elif rogues is True:
        logging.info(ROGUES_TEXT)
        rogueoutput = rogueoutputclass(analysis_results, rogueconfig)
        rogueoutput.printTextResults()
    elif heroes is True:
        logging.info(ROGUES_TEXT)
        rogueoutput = rogueoutputclass(analysis_results, rogueconfig, heroes)
        rogueoutput.printTextResults()
    else:
        logging.info("Outputting HTML report")
        htmloutput = FormatAnalysisHTMLOutput(analysis_results)
        print(htmloutput.printHTMLResults())


def analysis_from_database(database_path, denylist=None, rogues=False, heroes=False):
    """Analysis of format identification report from existing database.

    :param database_path: path to sqlite database containing analysis
        data (String)
    :param denylist: information to filter from denylist (List)
    :param rogues: flag to output rogues (Boolean)
    :param heroes: flag to output heroes (Boolean)
    :return: analysis_results (AnalysisResults)
    """
    logging.info("Analysis from database: %s", database_path)
    try:
        analysis = DemystifyAnalysis(database_path, get_config(), denylist)
    except AnalysisError as err:
        raise AnalysisError(err)
    rogue_analysis = False
    if rogues is not False or heroes is not False:
        rogue_analysis = True
    analysis.runanalysis(rogue_analysis)
    return analysis


def analysis_from_csv(format_report, analyze, denylist=None, rogues=None, heroes=None):
    """Analysis of format identification report from raw data, i.e.
    DROID CSV, SF YAML etc.

    :param format_report: path to format report (String)
    :param analyze: flag to request analysis from this utility, as
        opposed to just outputting a database file (Boolean)
    :param denylist: information to filter from denylist (Dict)
    :param rogues: flag to output rogues (Boolean)
    :param heroes: flag to output heroes (Boolean)
    :return: None (Nonetype)
    """
    logging.info("Generating database from input report...")
    database_path = sqlitefid.identify_and_process_input(format_report)
    logging.info("Database path: %s", database_path)
    if database_path is None:
        logging.error("No database filename supplied: %s", database_path)
        return
    if analyze is not True:
        logging.error("Analysis is not set: %s", analyze)
        return
    analysis = analysis_from_database(database_path, denylist, rogues, heroes)
    return analysis


def output_time(start_time):
    """Output a time taken to process string given a start_time."""
    logging.info("Output took: %s seconds", (time.time() - start_time))


def get_denylist_template() -> str:
    """Return a denylist to be piped to a file by the caller."""
    from .denylist_template import denylist_template

    return denylist_template


def main():
    """Primary entry point for Demystify from the command line."""
    parser = argparse.ArgumentParser(
        description="Analyse DROID and Siegfried results stored in a SQLite database"
    )
    parser.add_argument(
        "--export",
        "--droid",
        "--sf",
        "--exp",
        help="Optional: DROID or Siegfried export to read, and then analyze",
        default=False,
    )
    parser.add_argument(
        "--db",
        help="Optional: Single DROID or Siegfried sqlite db to read",
        default=False,
    )
    parser.add_argument(
        "--txt", "--text", help="Output text instead of HTML", action="store_true"
    )
    parser.add_argument(
        "--denylist", help="Use configured denylist", action="store_true"
    )
    parser.add_argument(
        "--rogues",
        "--rogue",
        help="Output 'Rogues Gallery' listing",
        action="store_true",
    )
    parser.add_argument(
        "--heroes",
        "--hero",
        help="Output 'Heroes Gallery' listing",
        action="store_true",
    )
    parser.add_argument(
        "--denylist_template",
        help="Output a denylist template for your own configuration",
        action="store_true",
    )
    start_time = time.time()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    global args
    args = parser.parse_args()
    denylist = None
    if args.denylist_template:
        print(get_denylist_template())
        sys.exit()
    rogueconfig = None
    if args.denylist or args.rogues or args.heroes:
        try:
            denylist, rogueconfig = _handle_denylist_config()
        except DenyListError as err:
            logging.warning(err)
            sys.exit(1)
    if args.export:
        args.db = False
        analysis = analysis_from_csv(
            args.export, True, denylist, args.rogues, args.heroes
        )
    if args.db:
        if not IdentifyDB().identify_export(args.db):
            logging.error("Not a recognized sqlite database: %s", args.db)
            sys.exit(1)
        analysis = analysis_from_database(args.db, denylist, args.rogues, args.heroes)
    if analysis:
        handle_output(
            analysis.analysis_results, args.txt, args.rogues, args.heroes, rogueconfig
        )
        output_time(start_time)
    logging.info("Demystify: ...analysis complete")


if __name__ == "__main__":
    main()
