# -*- coding: utf-8 -*-

from __future__ import division
import time
import argparse
import os
import sys
import droid2sqlite
import ConfigParser
import htmloutputclass
import textoutputclass
import roguesgalleryoutputclass
import DroidAnalysisClass
import ExportDBClass

def handleConfig(blacklist):
   config = blacklist
   configfname = "blacklist.cfg"
   if os.path.isfile(configfname):
      config = ConfigParser.ConfigParser()
      config.read(configfname)
   return config

def handleOutput(analysisresults, htmlout=False, rogues=False, heroes=False):
   if htmlout is True:
      htmloutput = htmloutputclass.DROIDAnalysisHTMLOutput(analysisresults)
      sys.stdout.write(htmloutput.printHTMLResults())   
   elif rogues is True:
      rogueoutput = roguesgalleryoutputclass.rogueoutputclass(analysisresults)
      rogueoutput.printTextResults()
   elif heroes is True:
      rogueoutput = roguesgalleryoutputclass.rogueoutputclass(analysisresults, heroes)
      rogueoutput.printTextResults()      
   else:
      textoutput = textoutputclass.DROIDAnalysisTextOutput(analysisresults)
      sys.stdout.write(textoutput.printTextResults()) # Text class still uses print statements... 

def handleDROIDDB(dbfilename, config=False):
   analysis = DroidAnalysisClass.DROIDAnalysis(config)	
   analysisresults = analysis.openDROIDDB(dbfilename)
   return analysisresults

def handleDROIDCSV(droidcsv, analyse=False, htmlout=False, rogues=False, heroes=False, config=False):
   dbfilename = droid2sqlite.handleDROIDCSV(droidcsv)
   if analyse == True:
      analysisresults = handleDROIDDB(dbfilename, config)
      handleOutput(analysisresults, htmlout, rogues, heroes)

def outputtime(start_time):
   sys.stderr.write("--- %s seconds ---" % (time.time() - start_time) + "\n")

def main():

   #	Usage: 	--csv [droid report]

   #	Handle command line arguments for the script
   parser = argparse.ArgumentParser(description='Analyse DROID results stored in a SQLite DB')
   parser.add_argument('--csv', help='Optional: Single DROID CSV to read.', default=False)
   parser.add_argument('--csva', help='Optional: DROID CSV to read, and then analyse.', default=False)
   parser.add_argument('--db', help='Optional: Single DROID sqlite db to read.', default=False)
   parser.add_argument("--htm", "--html", help="Output HTML instead of text.", action="store_true")
   parser.add_argument("--rogues", "--rogue", help="Output 'Rogues Gallery' listing.", action="store_true")
   parser.add_argument("--heroes", "--hero", help="Output 'Heroes Gallery' listing.", action="store_true")
   parser.add_argument("--blacklist", "--bl", help="Use configured blacklist.", action="store_true")
   parser.add_argument("--export", "--exp", help="Export SQLITE DB as CSV.", default=False)

   start_time = time.time()

   if len(sys.argv)==1:
      parser.print_help()
      sys.exit(1)

   #	Parse arguments into namespace object to reference later in the script
   global args
   args = parser.parse_args()
   
   config = handleConfig(args.blacklist)
   
   if args.csv:
      handleDROIDCSV(args.csv)
      outputtime(start_time)
   if args.csva:
      handleDROIDCSV(args.csva, True, args.htm, args.rogues, args.heroes, config)
      outputtime(start_time)
   if args.db:
      analysisresults = handleDROIDDB(args.db, config)
      #handleOutput(analysisresults, args.htm, args.rogues, args.heroes)
      outputtime(start_time)
   if args.export:
      ex = ExportDBClass.ExportDB()
      ex.exportDB(args.export)
   
   else:
      sys.exit(1)

if __name__ == "__main__":      
   main()

