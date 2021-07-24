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

from __future__ import absolute_import, division

import argparse
import logging
import os
import sys
import time

LOGFORMAT = "%(asctime)-15s %(levelname)s: %(message)s"
DATEFORMAT = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(format=LOGFORMAT, datefmt=DATEFORMAT, level="INFO")


if sys.version_info[0] == 3:
    PY3 = True
else:
    PY3 = False


try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

from libs.DemystifyAnalysisClass import DemystifyAnalysis
from libs.HandleDenylistClass import HandleDenylist
from libs.IdentifyDatabase import IdentifyDB

# custom output handlers
from libs.outputhandlers.htmloutputclass import DROIDAnalysisHTMLOutput
from libs.outputhandlers.roguesgalleryoutputclass import rogueoutputclass
from libs.outputhandlers.textoutputclass import DROIDAnalysisTextOutput
from sqlitefid import sqlitefid

rogueconfig = False


def _handle_denylist_config():
    """Handles static configuration options, i.e. rogues and heroes
    filtering for the rsync lists this module can output.

    return: List containing denylist items (List)
    """
    DENYLIST = "denylist.cfg"

    if os.path.isfile(DENYLIST):
        config = ConfigParser.RawConfigParser()
        config.read(DENYLIST)
        denylist = HandleDenylist().denylist(config)

        global rogueconfig
        rogueconfig = config

    else:
        denylist = False

    return denylist


def handleOutput(analysisresults, txtout=False, rogues=False, heroes=False):
    """Handle output from the analysis.

    :param analysisresults: Object containing all of our analysis
        results (DROIDAnalysisResults)
    :param txtout: Output text (True) vs. HTML (False) (Bool)
    :param rogues: Output rogues gallery output for rsync (Bool)
    :param heroes: Output heroes gallery output for rsync (Bool)

    :return: None (Nonetype)
    """

    logging.info(type(analysisresults))

    if txtout is True:
        logging.info("Outputting text report")
        textoutput = DROIDAnalysisTextOutput(analysisresults)
        print(textoutput.printTextResults())
    elif rogues is True:
        logging.info("Rogues reporting is on")
        rogueoutput = rogueoutputclass(analysisresults, rogueconfig)
        rogueoutput.printTextResults()
    elif heroes is True:
        logging.info("Heroes reporting is on")
        rogueoutput = rogueoutputclass(analysisresults, rogueconfig, heroes)
        rogueoutput.printTextResults()
    else:
        logging.info("Outputting HTML report")
        htmloutput = DROIDAnalysisHTMLOutput(analysisresults)
        if PY3:
            print(htmloutput.printHTMLResults())
        else:
            print(htmloutput.printHTMLResults().encode("utf8"))


# function should go somewhere more appropriate in time
def getConfigInfo():
    cfg = "config.cfg"
    if os.path.exists(cfg) and os.path.isfile(cfg):
        conf = ConfigParser.ConfigParser()
        conf.read(cfg)
    else:
        conf = False
    return conf


def handleDROIDDB(dbfilename, denylist, rogues=False, heroes=False):
    analysis = DemystifyAnalysis(dbfilename, getConfigInfo(), denylist)

    # avoid unecessary processing with rogue path analyses
    rogueanalysis = False
    if rogues is not False or heroes is not False:
        rogueanalysis = True

    # send rogue argument to analysis class
    analysisresults = analysis.runanalysis(rogueanalysis)
    analysis.closeDROIDDB()
    return analysisresults


def handleDROIDCSV(droidcsv, analyse, txtout, denylist, rogues=False, heroes=False):
    dbfilename = sqlitefid.identifyinput(droidcsv)
    logging.info("db filename: %s", dbfilename)
    if dbfilename is not None:
        if analyse is True:
            analysisresults = handleDROIDDB(dbfilename, denylist, rogues, heroes)
            handleOutput(analysisresults, txtout, rogues, heroes)


def outputtime(start_time):
    logging.info("Output took: %s seconds", (time.time() - start_time))


def main():

    #   Usage:  --csv [droid report]

    #   Handle command line arguments for the script
    parser = argparse.ArgumentParser(
        description="Analyse DROID and Siegfried results stored in a SQLite database"
    )
    parser.add_argument(
        "--export",
        "--droid",
        "--sf",
        "--exp",
        help="Optional: DROID or Siegfried export to read, and then analyse",
        default=False,
    )
    parser.add_argument(
        "--db",
        help="Optional: Single DROID or Siegfried sqlite db to read",
        default=False,
    )
    parser.add_argument(
        "--txt", "--text", help="Output HTML instead of text", action="store_true"
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

    start_time = time.time()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    #   Parse arguments into namespace object to reference later in the script
    global args
    args = parser.parse_args()
    denylist = False
    if args.denylist or args.rogues or args.heroes:
        denylist = _handle_denylist_config()
    if args.export:
        handleDROIDCSV(args.export, True, args.txt, denylist, args.rogues, args.heroes)
        outputtime(start_time)
    if args.db:
        if os.path.isfile(args.db):
            iddb = IdentifyDB()
            if iddb.identify_export(args.db) == iddb.SQLITE_DB:
                analysisresults = handleDROIDDB(
                    args.db, denylist, args.rogues, args.heroes
                )
                handleOutput(analysisresults, args.txt, args.rogues, args.heroes)
                outputtime(start_time)
            else:
                sys.exit("Exiting: Not a recognised SQLite file.")
        else:
            sys.exit("Exiting: Not a file.")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
