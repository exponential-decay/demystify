#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import time
import argparse
import os
import sys
import droid2sqlite
import ConfigParser
import libs.ExportDBClass
import droid2sqlite
from libs.htmloutputclass import DROIDAnalysisHTMLOutput
from libs.textoutputclass import DROIDAnalysisTextOutput
from libs.roguesgalleryoutputclass import rogueoutputclass
from libs.DroidAnalysisClass import DROIDAnalysis
from libs.IdentifyDatabase import IdentifyDB

def handleConfig(blacklist):
   config = blacklist
   configfname = "blacklist.cfg"
   if os.path.isfile(configfname):
      config = ConfigParser.ConfigParser()
      config.read(configfname)
   return config

def handleOutput(analysisresults, txtout=False, rogues=False, heroes=False):
   if txtout is True:
      textoutput = DROIDAnalysisTextOutput(analysisresults)
      sys.stdout.write(textoutput.printTextResults()) # Text class still uses print statements...  
   elif rogues is True:
      rogueoutput = rogueoutputclass(analysisresults)
      rogueoutput.printTextResults()
   elif heroes is True:
      rogueoutput = roguesgalleryoutputclass.rogueoutputclass(analysisresults, heroes)
      rogueoutput.printTextResults()      
   else:
      htmloutput = DROIDAnalysisHTMLOutput(analysisresults)
      sys.stdout.write(htmloutput.printHTMLResults())     
   
def handleDROIDDB(dbfilename, config=False):
   cfg = 'config.cfg'
   if os.path.exists(cfg) and os.path.isfile(cfg):
      conf = ConfigParser.ConfigParser()
      conf.read(cfg)
   analysis = DROIDAnalysis(dbfilename, conf)	
   analysisresults = analysis.runanalysis()
   analysis.closeDROIDDB()
   return analysisresults

def handleDROIDCSV(droidcsv, analyse=False, txtout=False, rogues=False, heroes=False, blacklist=False):
   dbfilename = droid2sqlite.identifyinput(droidcsv)
   if dbfilename is not None:
      if analyse == True:
         analysisresults = handleDROIDDB(dbfilename)
         handleOutput(analysisresults, txtout, rogues, heroes)

def outputtime(start_time):
   sys.stderr.write("\n" + "--- %s seconds ---" % (time.time() - start_time) + "\n")

def main():

   #	Usage: 	--csv [droid report]

   #	Handle command line arguments for the script
   parser = argparse.ArgumentParser(description='Analyse DROID and Siegfried results stored in a SQLite database')
   parser.add_argument('--export', '--droid', '--sf', '--exp', help='Optional: DROID or Siegfried export to read, and then analyse.', default=False)
   parser.add_argument('--db', help='Optional: Single DROID or Siegfried sqlite db to read.', default=False)
   parser.add_argument("--txt", "--text", help="Output HTML instead of text.", action="store_true")
   #parser.add_argument("--rogues", "--rogue", help="Output 'Rogues Gallery' listing.", action="store_true")
   #parser.add_argument("--heroes", "--hero", help="Output 'Heroes Gallery' listing.", action="store_true")
   #parser.add_argument("--blacklist", help="Use configured blacklist.", action="store_true")

   start_time = time.time()

   if len(sys.argv)==1:
      parser.print_help()
      sys.exit(1)

   #	Parse arguments into namespace object to reference later in the script
   global args
   args = parser.parse_args()
   
   #if args.blacklist:
   #   blacklist = handleConfig(args.blacklist)
      
   if args.export:
      handleDROIDCSV(args.export, True, args.txt)
      outputtime(start_time)
   if args.db:
      if os.path.isfile(args.db):
         iddb = IdentifyDB()
         if iddb.identify_export(args.db) == iddb.SQLITE_DB:
            analysisresults = handleDROIDDB(args.db)
            handleOutput(analysisresults, args.txt)
            outputtime(start_time)
         else:
            sys.exit("Exiting: Not a recognised SQLite file.")
      else:
         sys.exit("Exiting: Not a file.")
   else:
      sys.exit(1)

if __name__ == "__main__":      
   main()

