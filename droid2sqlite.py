# -*- coding: utf-8 -*-

from __future__ import division
import argparse
import sys
from IdentifyExportClass import IdentifyExport
from GenerateBaselineDBClass import GenerateBaselineDB
from DROIDLoaderClass import DROIDLoader

def handleDROIDCSV(droidcsv, BOM=False): 
   global basedb
   basedb = GenerateBaselineDB(droidcsv)
   loader = DROIDLoader(basedb, BOM)
   loader.droidDBSetup(droidcsv, basedb.getcursor())
   basedb.closedb()

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
      id = IdentifyExport()
      type = id.exportid(args.export)
      if type == id.DROIDTYPE:
         handleDROIDCSV(args.export)
      elif type == id.DROIDTYPEBOM:
         handleDROIDCSV(args.export, True)
      elif type == id.UNKTYPE:
         sys.stderr.write("Unknown export type." + "\n")		
   else:
      sys.exit(1)

if __name__ == "__main__":
   main()
