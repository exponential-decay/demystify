#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division

import argparse
import os
import sys
import time

from DROIDLoaderClass import DROIDLoader
from FidoLoaderClass import FidoLoader
from GenerateBaselineDBClass import GenerateBaselineDB
from IdentifyExportClass import IdentifyExport
from SFLoaderClass import SFLoader
from Version import SqliteFIDVersion


def identifyinput(export):
    id = IdentifyExport()
    type = id.exportid(export)
    if type == id.DROIDTYPE:
        return handleDROIDCSV(export)
    elif type == id.DROIDTYPEBOM:
        return handleDROIDCSV(export, True)
    elif type == id.SFTYPE:
        return handleSFYAML(export)
    elif type == id.FIDOTYPE:
        return handleFIDOCSV(export)
    elif type == id.SFCSVTYPE:
        sys.stderr.write("Sigfried CSV. Not currently handled.")
    elif type == id.UNKTYPE:
        sys.stderr.write("Unknown export type.")
        return None


def handleDROIDCSV(droidcsv, BOM=False):
    global basedb
    basedb = GenerateBaselineDB(droidcsv)
    loader = DROIDLoader(basedb, BOM)
    loader.droidDBSetup(droidcsv, basedb.getcursor())
    basedb.closedb()
    return basedb.dbname


def handleSFYAML(sfexport):
    global basedb
    basedb = GenerateBaselineDB(sfexport)
    loader = SFLoader(basedb)
    loader.sfDBSetup(sfexport, basedb.getcursor())
    basedb.closedb()
    return basedb.dbname


def handleFIDOCSV(fidoexport):
    # global basedb
    # basedb = GenerateBaselineDB(fidoexport)
    basedb = None
    loader = FidoLoader(basedb)
    loader.fidoDBSetup(fidoexport, None)
    # loader.fidoDBSetup(fidoexport, basedb.getcursor())
    # basedb.closedb()
    # return basedb.dbname


def outputtime(start_time):
    sys.stderr.write("\n" + "--- %s seconds ---" % (time.time() - start_time) + "\n")


def main():

    # 	Usage: 	--csv [droid report]
    # 	Handle command line arguments for the script
    parser = argparse.ArgumentParser(
        description="Place DROID profiles into a SQLite DB"
    )
    parser.add_argument(
        "--export", "--droid", "--sf", help="Optional: Single tool export to read."
    )
    parser.add_argument(
        "--version", help="Optional: Output version number.", action="store_true"
    )

    start_time = time.time()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    # 	Parse arguments into namespace object to reference later in the script
    global args
    args = parser.parse_args()

    if args.version:
        v = SqliteFIDVersion()
        sys.stdout.write(v.getVersion() + "\n")
        sys.exit(1)

    if args.export:
        if os.path.isfile(args.export):
            identifyinput(args.export)
            outputtime(start_time)
        else:
            sys.exit("Exiting: Not a file.")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
