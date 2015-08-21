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

def handleConfig():
   config = False
   configfname = "blacklist.cfg"
   if os.path.isfile(configfname):
      config = ConfigParser.ConfigParser()
      config.read(configfname)
   return config

def handleOutput(analysisresults, htmlout=False, rogues=False, heros=False):
   if htmlout is True:
      htmloutput = htmloutputclass.DROIDAnalysisHTMLOutput(analysisresults)
      sys.stdout.write(htmloutput.printHTMLResults())   
   elif rogues is True:
      rogueoutput = roguesgalleryoutputclass.rogueoutputclass(analysisresults)
      rogueoutput.printTextResults()
   elif heros is True:
      rogueoutput = roguesgalleryoutputclass.rogueoutputclass(analysisresults, heros)
      rogueoutput.printTextResults()      
   else:
      textoutput = textoutputclass.DROIDAnalysisTextOutput(analysisresults)
      textoutput.printTextResults() # Text class still uses print statements... 

def handleDROIDDB(dbfilename, htmlout=False, config=False):
   analysis = DroidAnalysisClass.DROIDAnalysis(config)	
   analysisresults = analysis.openDROIDDB(dbfilename)
   return analysisresults

def handleDROIDCSV(droidcsv, analyse=False, htmlout=False, rogues=False, config=False):
   dbfilename = droid2sqlite.handleDROIDCSV(droidcsv)
   if analyse == True:
      analysisresults = handleDROIDDB(dbfilename, config)
      handleOutput(analysisresults, htmlout, rogues)

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
   parser.add_argument("--heros", "--hero", help="Output 'Heros Gallery' listing.", action="store_true")

   start_time = time.time()

   if len(sys.argv)==1:
      parser.print_help()
      sys.exit(1)

   #	Parse arguments into namespace object to reference later in the script
   global args
   args = parser.parse_args()
   
   config = handleConfig()
   
   if args.csv:
      handleDROIDCSV(args.csv)
      outputtime(start_time)
   if args.csva:
      handleDROIDCSV(args.csva, True, args.htm, args.rogues, args.heros, config)
      outputtime(start_time)
   if args.db:
      analysisresults = handleDROIDDB(args.db, args.htm, config)
      handleOutput(analysisresults, args.htm, args.rogues, args.heros)
      outputtime(start_time)
   
   else:
      sys.exit(1)

if __name__ == "__main__":      
   main()

