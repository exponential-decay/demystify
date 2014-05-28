# -*- coding: utf-8 -*-

from __future__ import division
import argparse
import sys
import sqlite3
import csv
import droid2sqlite
import MsoftFnameAnalysis
from urlparse import urlparse

class DROIDAnalysis:

	# DB self.cursor
	cursor = None

	# Counts
	filecount = 0
	containercount = 0
	filesincontainercount = 0	
	directoryCount = 0
	uniqueDirectoryNames = 0
	identifiedfilecount = 0
	unidentifiedfilecount = 0
	distinctSignaturePuidcount = 0
	extensionIDOnlyCount = 0
	distinctextensioncount = 0
	zeroidcount = 0
	
	def printResults(self):
		print "Total files: " + str(self.filecount)
		print "Total container objects: " + str(self.containercount)
		print "Total files in containers: " + str(self.filesincontainercount) 
		print "Total directories: " + str(self.directoryCount)
		print "Total unique directory names: " + str(self.uniqueDirectoryNames)
		print "Total identified files (signature and container): " + str(self.identifiedfilecount)
		print "Total unidentified files (extension and blank): " + str(self.unidentifiedfilecount)
		print "Total extension ID only count: " + str(self.extensionIDOnlyCount)
		print "Total signature IDd PUID count: " + str(self.distinctSignaturePuidcount)
		print "Total distinct extensions across collection: " + str(self.distinctextensioncount)
		print "Total zero id count: " + str(self.zeroidcount)
		print "Percentage of collection identified: " + str(self.identifiedPercentage)
		print "Percentage of collection unidentified: " + str(self.unidentifiedPercentage)

		print
		print "Signature identified PUIDs in collection:"
		print self.sigIDPUIDList

		print
		print "Frequency of signature identified PUIDs:"
		print self.sigIDPUIDFrequency

		print
		print "Extension only identification in collection:"
		print self.extensionOnlyIDList

		print 
		print "Frequency of extension only identification in collection: "
		print self.extensionOnlyIDFrequency

		print
		print "Unique extensions identified across collection:"
		print self.uniqueExtensionsInCollectionList

		print
		print "Frequency of all extensions:"
		print self.frequencyOfAllExtensions 

		print
		print "List of files with no identification: "
		print self.filesWithNoIDList
	
		print 
		print "Duplicate listing: "
		for d in self.duplicateListing:
			print d
			print

		print "Pareto statistics: "
		print self.PUIDParetoList
		print
		print self.extensionParetoList
			
	def __countQuery__(self, query):
		self.cursor.execute(query)
		count = self.cursor.fetchone()[0]
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
				row = row + str(r[0]) + separator 
		return row[:-2]

	def __alternativeFrequencyQuery__(self, query):
		self.cursor.execute(query)
		result = self.cursor.fetchall()
		return result

	def countFilesQuery(self):
		return self.__countQuery__( 
			"SELECT COUNT(NAME) FROM droid WHERE (TYPE='File' OR TYPE='Container')")

	# Container objects known by DROID...
	def countContainerObjects(self):
		return self.__countQuery__(
			"SELECT COUNT(NAME) FROM droid WHERE TYPE='Container'")
	
	def countFilesInContainerObjects(self):
		return self.__countQuery__( 
			"SELECT COUNT(NAME) FROM droid WHERE URI_SCHEME!='file' AND (TYPE='File' OR TYPE='Container')")

	def countFoldersQuery(self):
		return self.__countQuery__( 
			"SELECT COUNT(NAME) FROM droid WHERE TYPE='Folder'")

	def countUniqueDirectoryNames(self):
		return self.__countQuery__( 
			"SELECT COUNT(DISTINCT DIR_NAME) FROM droid")

	def countIdentifiedQuery(self):
		return self.__countQuery__( 
			"SELECT COUNT(NAME) FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (METHOD='Signature' or METHOD='Container')")

	def countTotalUnidentifiedQuery(self):
		return self.__countQuery__( 
			"SELECT COUNT(NAME) FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (METHOD='no value' OR METHOD='Extension')")	

	def countZeroID(self):
		return self.__countQuery__( 
			"SELECT COUNT(NAME) FROM droid WHERE METHOD='no value' AND (TYPE='File' OR TYPE='Container')")

	def countExtensionIDOnly(self):
		return self.__countQuery__( 
			"SELECT COUNT(NAME) FROM droid WHERE METHOD='Extension' AND(TYPE='File' OR TYPE='Container')")
	
	# PUIDS for files identified by DROID using binary matching techniques
	def countDistinctSignaturePUIDS(self):
		return self.__countQuery__( 
			"SELECT COUNT(DISTINCT PUID) FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (METHOD='Signature' OR METHOD='Container')")
		
	def countDistinctExtensions(self):
		return self.__countQuery__( 
			"SELECT COUNT(DISTINCT EXT) FROM droid WHERE TYPE='File' OR TYPE='Container'")

	###
	# Frequency list queries
	###
	def identifiedBinaryMatchedPUIDFrequency(self):
		return self.__listQuery__( 
			"SELECT PUID, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (METHOD='Signature' OR METHOD='Container') GROUP BY PUID ORDER BY TOTAL DESC",  " | ")

	def extensionOnlyIdentificationFrequency(self):
		return self.__listQuery__( 
			"SELECT PUID, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (METHOD='Extension') GROUP BY PUID ORDER BY TOTAL DESC",  " | ")

	def allExtensionsFrequency(self):
		return self.__listQuery__(
			"SELECT EXT, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') GROUP BY EXT ORDER BY TOTAL DESC", " | ")

	###
	# List queries
	###
	def listUniqueBinaryMatchedPUIDS(self):
		return self.__listQuery__(
			"SELECT DISTINCT PUID FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (METHOD='Signature' OR METHOD='Container')", " | ")

	def listAllUniqueExtensions(self):	
		return self.__listQuery__(
			"SELECT DISTINCT EXT FROM droid WHERE (TYPE='File' OR TYPE='Container')", " | ")

	def listExtensionOnlyIdentificationPUIDS(self):	
		return self.__listQuery__(		
			"SELECT DISTINCT PUID, FORMAT_NAME FROM droid WHERE (TYPE='File' OR TYPE='Container') AND METHOD='Extension'", " | ")

	def listNoIdentificationFiles(self):
		return self.__listQuery__(	
			"SELECT FILE_PATH FROM droid WHERE METHOD='no value' AND (TYPE='File' OR TYPE='Container')", "\n")

	def listDuplicates(self):
		duplicatestr = ''
		duplicatelist = []
		duplicatequery = "SELECT MD5_HASH, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') GROUP BY MD5_HASH ORDER BY TOTAL DESC"
		result = self.__alternativeFrequencyQuery__(duplicatequery)
		for r in result:
			if r[1] > 1:
				duplicatemd5 = r[0]
				duplicatestr = "Duplicate hash: " + duplicatemd5 + '\n'
				duplicatestr = duplicatestr + self.__listQuery__("SELECT MD5_HASH, DIR_NAME, NAME FROM droid WHERE MD5_HASH='" + duplicatemd5 + "'", "\n")
				duplicatelist.append(duplicatestr)
		return duplicatelist

	###
	# Pareto listings
	###
	def paretoListingPUIDS(self):
		# Hypothesis: 80% of the effects come from 20% of the causes		

		eightyPercentTotalPUIDs = int(self.identifiedfilecount * 0.80)		# 80 percent figure
		countIdentifiedPuids = "SELECT PUID, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (METHOD='Signature' OR METHOD='Container') GROUP BY PUID ORDER BY TOTAL DESC"
		return self.listTopTwenty(self.__alternativeFrequencyQuery__(countIdentifiedPuids), eightyPercentTotalPUIDs, self.identifiedfilecount, "Identified formats", "identified formats")
		
	def paretoListingExts(self):
		# Hypothesis: 80% of the effects come from 20% of the causes		

		eightyPercentTotalExts = int(self.filecount * 0.80)		# 80 percent figure
		countExtensions = "SELECT EXT, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') GROUP BY EXT ORDER BY TOTAL DESC"
		return self.listTopTwenty(self.__alternativeFrequencyQuery__(countExtensions), eightyPercentTotalExts, self.filecount, "Extensions for formats", "total files")

	def listTopTwenty(self, frequencyQueryResult, eightyPercentTotal, total, introtext, endtext):
		toptwentystr = ''
		x = 0
		index = "null"
		
		for i,t in enumerate(frequencyQueryResult):
			count = t[1]
			if count <= eightyPercentTotal:
				x = x + count
				if x >= eightyPercentTotal:
					index = i
					break
	
		if index is not "null": 
			toptwentystr = introtext + " contributing to 20% of collection out of " + str(total) + " " + endtext + "\n"
			for i in range(index):
				label = frequencyQueryResult[i][0]
				count = frequencyQueryResult[i][1]
				toptwentystr = toptwentystr + label + "       count: " + str(count)
	
		else:
			toptwentystr = "Format frequency: " + "\n"
			toptwentystr = toptwentystr + freqTuple[0][0] + "       count: " + str(freqTuple[0][1])
		
		return toptwentystr

	###
	# Additional functions on DB
	###
	def filesWithDodgyCharacters(self):
		countDirs = "SELECT DISTINCT NAME FROM droid"
		self.cursor.execute(countDirs)
		dirlist = self.cursor.fetchall()
		charcheck = MsoftFnameAnalysis.MsoftFnameAnalysis()
		for d in dirlist:
			dirstring = d[0]
			charcheck.completeFnameAnalysis(dirstring)
		return

	###
	# Stats output... #TODO: Merge and document these two functions better
	###
	def calculateIdentifiedPercent(self):
		allcount = self.filecount
		count = self.identifiedfilecount
		if allcount > 0:
			percentage = (count/allcount)*100
			return '%.1f' % round(percentage, 1)

	def calculateUnidentifiedPercent(self):
		allcount = self.filecount
		count = self.unidentifiedfilecount		

		if allcount > 0:
			percentage = (count/allcount)*100
			return '%.1f' % round(percentage, 1)
						
	def queryDB(self):
		self.filecount = self.countFilesQuery()
		self.containercount = self.countContainerObjects()
		self.filesincontainercount = self.countFilesInContainerObjects()
		self.directoryCount = self.countFoldersQuery()
		self.uniqueDirectoryNames = self.countUniqueDirectoryNames()
		self.identifiedfilecount = self.countIdentifiedQuery()
		self.unidentifiedfilecount = self.countTotalUnidentifiedQuery()
		self.extensionIDOnlyCount = self.countExtensionIDOnly()
		self.distinctSignaturePuidcount = self.countDistinctSignaturePUIDS()
		self.distinctextensioncount = self.countDistinctExtensions()
		self.zeroidcount = self.countZeroID()
		self.unidentifiedPercentage = self.calculateUnidentifiedPercent()
		self.identifiedPercentage = self.calculateIdentifiedPercent()
		self.sigIDPUIDList = self.listUniqueBinaryMatchedPUIDS()
		self.sigIDPUIDFrequency = self.identifiedBinaryMatchedPUIDFrequency()
		self.extensionOnlyIDList = self.listExtensionOnlyIdentificationPUIDS()
		self.extensionOnlyIDFrequency = self.extensionOnlyIdentificationFrequency()
		self.uniqueExtensionsInCollectionList = self.listAllUniqueExtensions()
		self.frequencyOfAllExtensions = self.allExtensionsFrequency()
		self.filesWithNoIDList = self.listNoIdentificationFiles()
		self.duplicateListing = self.listDuplicates()
		self.PUIDParetoList = self.paretoListingPUIDS()
		self.extensionParetoList = self.paretoListingExts()		
		self.printResults()
		
		#TODO: handle this correctly
		print
		print "Identifying troublesome filenames: "
		self.badFilenames = self.filesWithDodgyCharacters()

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
