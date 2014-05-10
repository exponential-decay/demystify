# -*- coding: utf-8 -*-

from __future__ import division
import argparse
import sys
import sqlite3
import csv
import hashlib
import os
import time
import datetime
from urlparse import urlparse

class DROIDLoader:

	csvcolumncount = 0
	moduleversion = sqlite3.version
	sqliteversion = sqlite3.sqlite_version
	contenthash = 0
	timestamp = 0

	#DROID SPECIFIC COLUMN INDEXES
	URI_COL = 2

	def getTimestamp(self):
		ts = time.time()
		st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		self.timestamp = st

	def getContentHash(self, droidcsv):
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
		self.contenthash = csvhash.hexdigest()

	def createDBID(self, cursor):
		self.dropDBIDTable(cursor)
		cursor.execute("CREATE TABLE dbid (CONTENT_MD5, TIMESTAMP)")
		cursor.execute("INSERT INTO dbid VALUES ('" + str(self.contenthash) + "', '" + str(self.timestamp) + "')")

	def createDROIDTable(self, cursor, csvcolumnheaders):
		# turn csv headers list into a csv string, write query, create table

		self.csvcolumncount = len(csvcolumnheaders)
		columns = ""
		for header in csvcolumnheaders:
			if header == "URI":
				columns = columns + header + ", " + "URI_SCHEME, "
				self.csvcolumncount+=1
			else:
				columns = columns + header + ", "

		cursor.execute("CREATE TABLE droid (" + columns[:-2] + ")")
		return True

	def dropTable(self, cursor, tablename):
		# If we've a db already, can check it has a droid table
		cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='" + tablename + "';")
		# Can't DROP something that doesn't exist...
		if cursor.fetchone() is not None:
			cursor.execute("DROP table " + tablename + "")	# DROP just in case

	def dropDROIDTable(self, cursor):
		self.dropTable(cursor, 'droid')
		return

	def dropDBIDTable(self, cursor):
		self.dropTable(cursor, 'dbid')

	def getDBFilename(self, droidcsv):
		return droidcsv.replace(".csv", "") + ".db"

	def userOverwriteOption(self, conn, msg):
		user_input = raw_input("DROID DB file exists, " + msg + " Overwrite (y/n): ")
		if user_input[0:1].lower()	== 'y':
			conn.close()
			overwrite = True
			return overwrite
		else:
			print "Program exiting..."
			print
			conn.close()
			sys.exit(0)

	def checkDBExists(self, dbfilename):
		#if .db file exists, read MD5 column
		#if different, do something, else do nothing...
		#both optimisation and protection
		#md5, date added
		overwrite = False
		if os.path.isfile(dbfilename):
			# File exists			
			conn = sqlite3.connect(dbfilename)
			cursor = conn.cursor()
			cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dbid';")
			if cursor.fetchone() is not None:
				cursor.execute("SELECT CONTENT_MD5 FROM dbid")
				if cursor.fetchone()[0] == self.contenthash:
					cursor.execute("SELECT TIMESTAMP FROM dbid")
					print
					print "Identical content hashes, generated: " + cursor.fetchone()[0]
					overwrite = self.userOverwriteOption(conn, "hashes identical.")
			else:
				print
				overwrite = self.userOverwriteOption(conn, "hashes cannot be read.")

			return overwrite

	def droidDBSetup(self, droidcsv):

		dbfilename = self.getDBFilename(droidcsv)
		self.getContentHash(droidcsv)
		self.getTimestamp()
		
		if self.checkDBExists(dbfilename):

			conn = sqlite3.connect(dbfilename)
			cursor = conn.cursor()
			self.dropDROIDTable(cursor)	# may place elsewhere, e.g. when looking for dupes

			with open(droidcsv, 'rb') as csvfile:
				droidreader = csv.reader(csvfile)
				for row in droidreader:
					if droidreader.line_num == 1:		# not zero-based index
						tablequery = self.createDROIDTable(cursor, row)
					else:
						rowstr = ""	
						for i,item in enumerate(row[0:self.csvcolumncount-1]):
									
							if item == "":
								rowstr = rowstr + "'no value'"
							else:
								rowstr = rowstr + "'" + item + "'"
				
							if i == self.URI_COL:
								url = item
								rowstr = rowstr + ",'" + urlparse(url).scheme + "'"
	
							if i < self.csvcolumncount-2:
								rowstr = rowstr + ","

						cursor.execute("INSERT INTO droid VALUES (" + rowstr + ")")

			self.createDBID(cursor) 

			# Save (commit) the changes
			conn.commit()

			# We can also close the connection if we are done with it.
			# Just be sure any changes have been committed or they will be lost.
			conn.close()
			print

def handleDROIDCSV(droidcsv):
	loader = DROIDLoader()
	loader.droidDBSetup(droidcsv)

def main():

	#	Usage: 	--csv [droid report]

	#	Handle command line arguments for the script
	parser = argparse.ArgumentParser(description='Place DROID profiles into a SQLite DB')
	parser.add_argument('--csv', help='Optional: Single DROID CSV to read.')
	
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
