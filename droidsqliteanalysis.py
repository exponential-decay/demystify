# -*- coding: utf-8 -*-

from __future__ import division
import argparse
import sys
import sqlite3
import csv
import re
import droid2sqlite
from urlparse import urlparse

class DROIDAnalysis:

	# DB self.cursor
	cursor = None

	# Counts
	filecount = 0
	containercount = 0
	filesincontainercount = 0	
	foldercount = 0
	uniquedircount = 0
	identifiedfilecount = 0
	unidentifiedcount = 0
	zeroidcount = 0
	extensionIDOnlyCount = 0
	distinctextensioncount = 0
	distinctextpuidcount = 0
	distinctbinpuidcount = 0

	def __countQuery__(self, query):
		self.cursor.execute(query)
		count = self.cursor.fetchone()[0]
		print "XXXX: " + str(count)
		return count

	def __listQuery__(self, query, separator):
		self.cursor.execute(query)
		result = self.cursor.fetchall()
		row = ""
		for r in result:
			if len(r) > 1:
				item = ""
				for t in r:
					item = item + str(t) + ", "
				row = row + item[:-2] + separator
			else:
				row = row + str(r[0]) + ", " 
		print row[:-2]

	def __alternativeFrequencyQuery__(self, query):
		self.cursor.execute(query)
		result = self.cursor.fetchall()
		return result

	def countFilesQuery(self):
		self.filecount = self.__countQuery__( 
			"SELECT COUNT(NAME) FROM droid WHERE (TYPE='File' OR TYPE='Container')")

	# Container objects known by DROID...
	def countContainerObjects(self):
		self.containercount = self.__countQuery__(
			"SELECT COUNT(NAME) FROM droid WHERE TYPE='Container'")
	
	def countFilesInContainerObjects(self):
		self.filesincontainercount = self.__countQuery__( 
			"SELECT COUNT(NAME) FROM droid WHERE URI_SCHEME!='file' AND (TYPE='File' OR TYPE='Container')")

	def countUniqueDirs(self):
		self.uniquedirs = self.__countQuery__( 
			"SELECT COUNT(DISTINCT DIR_NAME) FROM droid")

	def countIdentifiedQuery(self):
		self.identifiedfilecount = self.__countQuery__( 
			"SELECT COUNT(NAME) FROM droid WHERE (TYPE='File' OR TYPE='Container') AND METHOD='Signature'")

	def countTotalUnidentifiedQuery(self):
		self.unidentifiedfilecount = self.__countQuery__( 
			"SELECT COUNT(NAME) FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (METHOD='no value' OR METHOD='Extension')")	
	
	def countFoldersQuery(self):
		self.foldercount = self.__countQuery__( 
			"SELECT COUNT(NAME) FROM droid WHERE TYPE='Folder'")

	def countZeroID(self):
		self.zeroidcount = self.__countQuery__( 
			"SELECT COUNT(NAME) FROM droid WHERE METHOD='no value' AND (TYPE='File' OR TYPE='Container')")

	def countExtensionIDOnly(self):
		self.extensionIDOnlyCount = self.__countQuery__( 
			"SELECT COUNT(NAME) FROM droid WHERE METHOD='Extension' AND(TYPE='File' OR TYPE='Container')")
	
	# PUIDS for files identified by DROID using binary matching techniques
	def countSignaturePUIDS(self):
		self.distinctbinpuidcount = self.__countQuery__( 
			"SELECT COUNT(DISTINCT PUID) FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (METHOD='Signature' OR METHOD='Container')")
		
	def countExtensionPUIDS(self):
		self.distinctextpuidcount = self.__countQuery__( 
			"SELECT COUNT(DISTINCT PUID) FROM droid WHERE (TYPE='File' OR TYPE='Container') AND METHOD='Extension'")

	def countExtensions(self):
		self.distinctextensioncount = self.__countQuery__( 
			"SELECT COUNT(DISTINCT EXT) FROM droid WHERE TYPE='File' OR TYPE='Container'")








	# Frequency list queries
	def identifiedBinaryMatchedPUIDFrequency(self):
		self.__listQuery__( 
			"SELECT PUID, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (METHOD='Signature' OR METHOD='Container') GROUP BY PUID ORDER BY TOTAL DESC",  " | ")

	def allExtensionsFrequency(self):
		self.__listQuery__(
			"SELECT EXT, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') GROUP BY EXT ORDER BY TOTAL DESC", " | ")





	# List queries
	def listUniqueBinaryMatchedPUIDS(self):
		self.__listQuery__(
			"SELECT DISTINCT PUID FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (METHOD='Signature' OR METHOD='Container')", " | ")

	def listAllUniqueExtensions(self):	
		self.__listQuery__(
			"SELECT DISTINCT EXT FROM droid WHERE (TYPE='File' OR TYPE='Container')", " | ")

	def listExtensionOnlyIdentificationPUIDS(self):	
		self.__listQuery__(		
			"SELECT DISTINCT PUID, FORMAT_NAME FROM droid WHERE (TYPE='File' OR TYPE='Container') AND METHOD='Extension'", " | ")

	def listDuplicates(self):
		duplicatequery = "SELECT MD5_HASH, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') GROUP BY MD5_HASH ORDER BY TOTAL DESC"
		result = self.__alternativeFrequencyQuery__(duplicatequery)
		for r in result:
			if r[1] > 1:
				duplicatemd5 = r[0]
				
				print
				print "Duplicate hash: " + duplicatemd5
				self.__listQuery__("SELECT MD5_HASH, DIR_NAME, NAME FROM droid WHERE MD5_HASH='" + duplicatemd5 + "'", "\n")

	def listTopTwenty(self, freqTuple, matchTotal, total, text):

		print matchTotal

		x = 0
		index = "null"
		for i,t in enumerate(freqTuple):
			if t[1] <= matchTotal:
				x = x + t[1]
				if x >= matchTotal:
					index = i
					break
	
		if index is not "null":
			print 
			print "Top 20% (out of " + str(total) + " ) " + text + ": "
			for i in range(index):
				print freqTuple[i][0] + "       COUNT: " + str(freqTuple[i][1])
	
		#else:
		#	print "Format frequency: "
		#	for t in test:
		#		print freqTuple[i][0] + "       COUNT: " + str(freqTuple[i][1])

	def paretoListings(self):
		# 80% of the effects come from 20% of the causes		
		
		# duplication in this function can potentially be removed through
		# effective use of classes...
			
		puidTotal = self.identifiedfilecount
		puidPareto = int(puidTotal * 0.80)
	
		print puidTotal

		extTotal = self.distinctextensioncount
		extPareto = int(extTotal * 0.80)

		puidquery = "SELECT PUID, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (METHOD='Signature' OR METHOD='Container') GROUP BY PUID ORDER BY TOTAL DESC"
		extquery = "SELECT EXT, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') GROUP BY EXT ORDER BY TOTAL DESC"

		self.listTopTwenty(self.__alternativeFrequencyQuery__(puidquery), puidPareto, puidTotal, "binary identified PUIDS")
		self.listTopTwenty(self.__alternativeFrequencyQuery__(extquery), extPareto, extTotal, "format extensions")


	def foldersWithDodgyCharacters(self):
		countDirs = "SELECT DISTINCT NAME FROM droid"
		self.cursor.execute(countDirs)
		dirlist = self.cursor.fetchall()
		for d in dirlist:
			dirstring = d[0]
			self.detect_invalid_characters(dirstring)
		return 
	
	def filesWithDodgyCharacters(self):

		return
	
	# stats output... 
	def calculateIdentifiedPercent(self):
		allcount = self.filecount
		count = self.identifiedfilecount
		if allcount > 0:
			percentage = (count/allcount)*100
			print "Percentage of the collection identified: " + '%.1f' % round(percentage, 1) + "%"
		else:
			print "Zero files" 

	def calculateUnidentifiedPercent(self):
		allcount = self.filecount
		count = self.unidentifiedfilecount		
		if allcount > 0:
			percentage = (count/allcount)*100
			print "Percentage of the collection unidentified: " + '%.1f' % round(percentage, 1) + "%"
		else:
			print "Zero files" 
		


	def detect_invalid_characters_test(self):
		#Strings for unit tests
		test_strings = ['COM4', 'COM4.txt', '.com4', 'abcCOM4text', 'abc.com4.txt.abc', 'con', 'CON', 'consumer', 'ף', 'י', 'צ', 'ףיצ', 'file[bracket]one.txt', 'file[two.txt', 'filethree].txt', '-=_|\"', '(<|>|:|"|/|\\|\?|\*|\||\x00-\x1f)']	
	
		# First test, all ASCII characters?
		for s in test_strings:
			self.detect_invalid_characters(s)
	
	def is_ascii(self, s):
		 return all(ord(c) < 128 for c in s)

	def detect_invalid_characters(self, s):
		#http://msdn.microsoft.com/en-us/library/aa365247(VS.85).aspx

		#non-ascii characters
		if not self.is_ascii(s):
			print "Characters in filename outside of ASCII range: " + s
		
		#non-recommended characters
		charlist = ['<','>',':','"','/','\\','?','*','|', ']', '[']
		for c in charlist:
			if c in s:
				print "File: " + s + " contains: " + c
				break
		
		#non-printable characters
		for c in range(0x1f):
			if chr(c) in s:
				print "File: " + s + " contains: " + hex(c)
				break

		#space or period at end of a name
		badnames = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', \
							'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', \
								'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', \
									'LPT6', 'LPT7', 'LPT8', 'LPT9']
				
		for c in badnames:
			if c.lower() in s[0:len(c)].lower():
				problem = True
				try:
					if s[len(c)] == '.':					#zero-based index
						problem = True
					else:
						problem = False
				except IndexError:
					problem = True
				if problem == True:
					print "File: " + s + " contains, reserved name: " + c



	

	def queryDB(self):
		self.countFilesQuery()
		self.countContainerObjects()
		self.countFilesInContainerObjects()
		self.countFoldersQuery()
		self.countIdentifiedQuery()
		self.countTotalUnidentifiedQuery()
		self.countZeroID()
		self.countExtensionIDOnly()
		self.countSignaturePUIDS()
		self.countExtensionPUIDS()
		self.countExtensions()
		self.countUniqueDirs()

		print
		print "Signature identified PUIDs in collection:"
		#self.listUniqueBinaryMatchedPUIDS()

		print
		print "Frequency of all binary matched PUIDs:"
		#self.identifiedBinaryMatchedPUIDFrequency()

		print
		print "Extension only identification in collection:"
		#self.listExtensionOnlyIdentificationPUIDS()

		print
		print "Unique extensions identified in collection:"
		#self.listAllUniqueExtensions()

		print
		print "Frequency of all extensions:"
		#self.allExtensionsFrequency()

		#self.paretoListings()

		print
		print "Total items in collection unidentified:"
		#self.calculateUnidentifiedPercent()
		
		print
		print "Total items in collection identified:"
		#self.calculateIdentifiedPercent()
		
		print 
		print "Listing duplicates: "
		#self.listDuplicates()


		self.foldersWithDodgyCharacters()	
		self.filesWithDodgyCharacters()
		

	def openDROIDDB(self, dbfilename):
		conn = sqlite3.connect(dbfilename)
		conn.text_factory = str		#encoded as ascii, not unicode / return ascii
		
		self.cursor = conn.cursor()
		self.queryDB()		# primary db query functions
		#self.detect_invalid_characters("s")		# need to pass strings to this... 
		conn.close()

def handleDROIDDB(dbfilename):
	analysis = DROIDAnalysis()	
	analysis.openDROIDDB(dbfilename)
	#TODO: Incorrect filetypes provided, e.g. providing CSV not DB

def handleDROIDCSV(droidcsv):
	droid2sqlite.handleDROIDCSV(droidcsv)
	#TODO: Handle CSV through to analysis option

def main():

	#	Usage: 	--csv [droid report]

	#	Handle command line arguments for the script
	parser = argparse.ArgumentParser(description='Analyse DROID results stored in a SQLite DB')
	parser.add_argument('--csv', help='Optional: Single DROID CSV to read.', default=False)
	parser.add_argument('--db', help='Optional: Single DROID sqlite db to read.', default=False)

	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(1)

	#	Parse arguments into namespace object to reference later in the script
	global args
	args = parser.parse_args()
	
	if args.csv:
		handleDROIDCSV(args.csv)	
	if args.db:
		handleDROIDDB(args.db)		
	else:
		sys.exit(1)

if __name__ == "__main__":
	main()
