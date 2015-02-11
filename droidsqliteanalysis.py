# -*- coding: utf-8 -*-

from __future__ import division
import argparse
import sys
import droid2sqlite
import DroidAnalysisClass

def handleDROIDDB(dbfilename):
   analysis = DroidAnalysisClass.DROIDAnalysis()	
   analysis.openDROIDDB(dbfilename)
   #TODO: Incorrect filetypes provided, e.g. providing CSV not DB

def handleDROIDCSV(droidcsv, analyse=False):
   dbfilename = droid2sqlite.handleDROIDCSV(droidcsv)
   if analyse == True:
      handleDROIDDB(dbfilename)

def main():

   #	Usage: 	--csv [droid report]

   #	Handle command line arguments for the script
   parser = argparse.ArgumentParser(description='Analyse DROID results stored in a SQLite DB')
   parser.add_argument('--csv', help='Optional: Single DROID CSV to read.', default=False)
   parser.add_argument('--csva', help='Optional: DROID CSV to read, and then analyse.', default=False)
   parser.add_argument('--db', help='Optional: Single DROID sqlite db to read.', default=False)

   if len(sys.argv)==1:
      parser.print_help()
      sys.exit(1)

   #	Parse arguments into namespace object to reference later in the script
   global args
   args = parser.parse_args()
   
   if args.csv:
      handleDROIDCSV(args.csv)
   if args.csva:
      handleDROIDCSV(args.csva, True)
   if args.db:
      handleDROIDDB(args.db)
   
   else:
      sys.exit(1)

if __name__ == "__main__":
   main()
