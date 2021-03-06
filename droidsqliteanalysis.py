#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import time
import argparse
import os
import sys
import ConfigParser
import libs.ExportDBClass
from libs.DroidAnalysisClass import DROIDAnalysis
from libs.IdentifyDatabase import IdentifyDB
from libs.HandleBlacklistClass import HandleBlacklist

# custom output handlers
from libs.outputhandlers.htmloutputclass import DROIDAnalysisHTMLOutput
from libs.outputhandlers.textoutputclass import DROIDAnalysisTextOutput
from libs.outputhandlers.roguesgalleryoutputclass import rogueoutputclass

# sqlitefid
sys.path.insert(0, "sqlitefid")
sys.path.insert(0, "sqlitefid/libs")
import sqlitefid

rogueconfig = False


def handleConfig(blacklist):
    if os.path.isfile(blacklist):
        config = ConfigParser.RawConfigParser()
        config.read(blacklist)  # adds to config object in own right
        hbl = HandleBlacklist()
        blacklist = hbl.blacklist(config)
        global rogueconfig
        rogueconfig = config
    else:
        blacklist = False
    return blacklist


def handleOutput(analysisresults, txtout=False, rogues=False, heroes=False):
    if txtout is True:
        textoutput = DROIDAnalysisTextOutput(analysisresults)
        sys.stdout.write(
            textoutput.printTextResults()
        )  # Text class still uses print statements...
    elif rogues is True:
        rogueoutput = rogueoutputclass(analysisresults, rogueconfig)
        rogueoutput.printTextResults()
    elif heroes is True:
        rogueoutput = rogueoutputclass(analysisresults, rogueconfig, heroes)
        rogueoutput.printTextResults()
    else:
        htmloutput = DROIDAnalysisHTMLOutput(analysisresults)
        sys.stdout.write(htmloutput.printHTMLResults())


# function should go somewhere more appropriate in time
def getConfigInfo():
    cfg = "config.cfg"
    if os.path.exists(cfg) and os.path.isfile(cfg):
        conf = ConfigParser.ConfigParser()
        conf.read(cfg)
    else:
        conf = False
    return conf


def handleDROIDDB(dbfilename, blacklist, rogues=False, heroes=False):
    analysis = DROIDAnalysis(dbfilename, getConfigInfo(), blacklist)

    # avoid unecessary processing with rogue path analyses
    rogueanalysis = False
    if rogues != False or heroes != False:
        rogueanalysis = True

    # send rogue argument to analysis class
    analysisresults = analysis.runanalysis(rogueanalysis)
    analysis.closeDROIDDB()
    return analysisresults


def handleDROIDCSV(droidcsv, analyse, txtout, blacklist, rogues=False, heroes=False):
    dbfilename = sqlitefid.identifyinput(droidcsv)
    if dbfilename is not None:
        if analyse == True:
            analysisresults = handleDROIDDB(dbfilename, blacklist, rogues, heroes)
            handleOutput(analysisresults, txtout, rogues, heroes)


def outputtime(start_time):
    sys.stderr.write("\n" + "--- %s seconds ---" % (time.time() - start_time) + "\n")


def main():

    # 	Usage: 	--csv [droid report]

    # 	Handle command line arguments for the script
    parser = argparse.ArgumentParser(
        description="Analyse DROID and Siegfried results stored in a SQLite database"
    )
    parser.add_argument(
        "--export",
        "--droid",
        "--sf",
        "--exp",
        help="Optional: DROID or Siegfried export to read, and then analyse.",
        default=False,
    )
    parser.add_argument(
        "--db",
        help="Optional: Single DROID or Siegfried sqlite db to read.",
        default=False,
    )
    parser.add_argument(
        "--txt", "--text", help="Output HTML instead of text.", action="store_true"
    )
    parser.add_argument(
        "--blacklist", help="Use configured blacklist.", action="store_true"
    )
    parser.add_argument(
        "--rogues",
        "--rogue",
        help="Output 'Rogues Gallery' listing.",
        action="store_true",
    )
    parser.add_argument(
        "--heroes",
        "--hero",
        help="Output 'Heroes Gallery' listing.",
        action="store_true",
    )

    start_time = time.time()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    # 	Parse arguments into namespace object to reference later in the script
    global args
    args = parser.parse_args()

    if args.blacklist or args.rogues or args.heroes:
        args.blacklist = "blacklist.cfg"
        blacklist = handleConfig(args.blacklist)
    else:
        blacklist = False

    if args.export:
        handleDROIDCSV(args.export, True, args.txt, blacklist, args.rogues, args.heroes)
        outputtime(start_time)
    if args.db:
        if os.path.isfile(args.db):
            iddb = IdentifyDB()
            if iddb.identify_export(args.db) == iddb.SQLITE_DB:
                analysisresults = handleDROIDDB(
                    args.db, blacklist, args.rogues, args.heroes
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
