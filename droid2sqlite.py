# -*- coding: utf-8 -*-
from __future__ import division
import argparse
import sys
from libs.IdentifyExportClass import IdentifyExport
from libs.GenerateBaselineDBClass import GenerateBaselineDB
from libs.DROIDLoaderClass import DROIDLoader
from libs.SFLoaderClass import SFLoader

def identifyinput(export):
   id = IdentifyExport()
   type = id.exportid(export)
   if type == id.DROIDTYPE:
      return handleDROIDCSV(export)
   elif type == id.DROIDTYPEBOM:
      return handleDROIDCSV(export, True)
   elif type == id.SFTYPE:
      return handleSFYAML(export)
   elif type == id.UNKTYPE:
      sys.stderr.write("Unknown export type." + "\n")	
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
      identifyinput(args.export)
   else:
      sys.exit(1)

if __name__ == "__main__":
   main()
