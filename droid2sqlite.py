#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import argparse
import os
import sys
from libs.IdentifyExportClass import IdentifyExport
from libs.GenerateBaselineDBClass import GenerateBaselineDB
from libs.DROIDLoaderClass import DROIDLoader
from libs.SFLoaderClass import SFLoader
from libs.FidoLoaderClass import FidoLoader

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
   #global basedb
   #basedb = GenerateBaselineDB(fidoexport)
   basedb = None   
   loader = FidoLoader(basedb)
   loader.fidoDBSetup(fidoexport, None)
   #loader.fidoDBSetup(fidoexport, basedb.getcursor())
   #basedb.closedb()
   #return basedb.dbname
   

def main():

   #	Usage: 	--csv [droid report]
   #	Handle command line arguments for the script
   parser = argparse.ArgumentParser(description='Place DROID profiles into a SQLite DB')
   parser.add_argument('--export', '--droid', '--sf', help='Optional: Single tool export to read.')
   
   if len(sys.argv)==1:
      parser.print_help()
      sys.exit(1)

   #	Parse arguments into namespace object to reference later in the script
   global args
   args = parser.parse_args()
   
   if args.export:
      if os.path.isfile(args.export):
         identifyinput(args.export)
      else:
         sys.exit("Exiting: Not a file.")
   else:
      sys.exit(1)

if __name__ == "__main__":
   main()
