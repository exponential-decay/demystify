# -*- coding: utf-8 -*-

from __future__ import division
import time
import argparse
import sys
import droid2sqlite
import htmloutputclass
import textoutputclass
import roguesgalleryoutputclass
import DroidAnalysisClass

def handleOutput(analysisresults, htmlout=False, rogues=False):
   if htmlout is True:
      htmloutput = htmloutputclass.DROIDAnalysisHTMLOutput(analysisresults)
      sys.stdout.write(htmloutput.printHTMLResults())   
   elif rogues is True:
      rogueoutput = roguesgalleryoutputclass.rogueoutputclass(analysisresults)
      rogueoutput.printTextResults()
   else:
      textoutput = textoutputclass.DROIDAnalysisTextOutput(analysisresults)
      textoutput.printTextResults() # Text class still uses print statements... 

def handleDROIDDB(dbfilename, htmlout=False, rogues=False):
   analysis = DroidAnalysisClass.DROIDAnalysis()	
   analysisresults = analysis.openDROIDDB(dbfilename)
   handleOutput(analysisresults, htmlout, rogues)

def handleDROIDCSV(droidcsv, analyse=False, htmlout=False, rogues=False):
   dbfilename = droid2sqlite.handleDROIDCSV(droidcsv)
   if analyse == True:
      analysisresults = handleDROIDDB(dbfilename)
      handleOutput(analysisresults, htmlout, rogues)

def main():

   start_time = time.time()

   #	Usage: 	--csv [droid report]

   #	Handle command line arguments for the script
   parser = argparse.ArgumentParser(description='Analyse DROID results stored in a SQLite DB')
   parser.add_argument('--csv', help='Optional: Single DROID CSV to read.', default=False)
   parser.add_argument('--csva', help='Optional: DROID CSV to read, and then analyse.', default=False)
   parser.add_argument('--db', help='Optional: Single DROID sqlite db to read.', default=False)
   parser.add_argument("--htm", "--html", help="Output HTML instead of text.", action="store_true")
   parser.add_argument("--rogues", "--rogue", help="Output 'Rogues Gallery' listing.", action="store_true")

   if len(sys.argv)==1:
      parser.print_help()
      sys.exit(1)

   #	Parse arguments into namespace object to reference later in the script
   global args
   args = parser.parse_args()
   
   if args.csv:
      handleDROIDCSV(args.csv)
   if args.csva:
      handleDROIDCSV(args.csva, True, args.htm, args.rogues)
   if args.db:
      handleDROIDDB(args.db, args.htm, args.rogues)
   
   else:
      sys.exit(1)

   sys.stderr.write("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
   main()
