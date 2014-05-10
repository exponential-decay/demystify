# -*- coding: utf-8 -*-

from __future__ import division
import argparse
import sys
import sqlite3
import csv
import re
import hashlib
import os
from urlparse import urlparse

class DROIDLoader:

	csvcolumncount = 0
	moduleversion = sqlite3.version
	sqliteversion = sqlite3.sqlite_version

	def hashCSV(self, droidcsv):
		#http://stackoverflow.com/questions/1131220/get-md5-hash-of-big-files-in-python

	 	csvhash = hashlib.md5()

		f = open(droidcsv)		

		while True:
			data = f.read(8192)
			if not data:
				break
			else:
				csvhash.update(data)
			
		f.close()
	
		return csvhash

	def createTableQuery(self, csvcolumnheaders):
		# turn csv headers list into a csv string
		# wrap sql create table query

		self.csvcolumncount = len(csvcolumnheaders)
		
		columns = ""
		for header in csvcolumnheaders:
			columns = columns + header + ", "

		createtablequery = "CREATE TABLE droid (" + columns[:-2] + ")"
	
		return createtablequery

	def droidDBSetup(self, droidcsv):

		#if .db file exists, read MD5 column
		#if different, do something, else do nothing...
		#both optimisation and protection
		#md5, date added
		print self.hashCSV(droidcsv).hexdigest()

		with open(droidcsv, 'rb') as csvfile:
			droidreader = csv.reader(csvfile)
			for row in droidreader:
				rowstr = ""
				if droidreader.line_num == 1:		# not zero-based index
					self.createTableQuery(row)
	
def handleDROIDCSV(droidcsv):
	loader = DROIDLoader()
	loader.droidDBSetup(droidcsv)

def main():

	#	Usage: 	--csv [jp2file]

	#	Handle command line arguments for the script
	parser = argparse.ArgumentParser(description='Place DROID profiles into a SQLite DB')
	parser.add_argument('--csv', help='Optional: Single DROID CSV to read.')
	
	#parser.add_argument('--pro', help='Optional: XML profile to validate against.', default=False)
	#parser.add_argument('--dif', help='Optional: Generate diff in errorlog if validation fails.', default=False)

	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(1)

	#	Parse arguments into namespace object to reference later in the script
	global args
	args = parser.parse_args()
	
	if args.csv:
		handleDROIDCSV(args.csv)			
	else:
		sys.exit(1)

if __name__ == "__main__":
	main()
