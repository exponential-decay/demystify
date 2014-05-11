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

	def __countQuery__(self, cursor, query):
		cursor.execute(query)
		count = cursor.fetchone()[0]
		print "XXXX: " + str(count)
		return count
	
	def countFilesQuery(self, cursor):
		self.filecount = self.__countQuery__(cursor, 
			"SELECT COUNT(NAME) FROM droid WHERE (TYPE='File' OR TYPE='Container')")

	# Container objects known by DROID...
	def countContainerObjects(self, cursor):
		self.containercount = self.__countQuery__(cursor, 
			"SELECT COUNT(NAME) FROM droid WHERE TYPE='Container'")
	
	def countFilesInContainerObjects(self, cursor):
		self.filesincontainercount = self.__countQuery__(cursor, 
			"SELECT COUNT(NAME) FROM droid WHERE URI_SCHEME!='file' AND (TYPE='File' OR TYPE='Container')")

	def countUniqueDirs(self, cursor):
		self.uniquedirs = self.__countQuery__(cursor, 
			"SELECT COUNT(DISTINCT DIR_NAME) FROM droid")

	def countIdentifiedQuery(self, cursor):
		self.identifiedfilecount = self.__countQuery__(cursor, 
			"SELECT COUNT(NAME) FROM droid WHERE (TYPE='File' OR TYPE='Container') AND METHOD='Signature'")

	def countFoldersQuery(self, cursor):
		self.foldercount = self.__countQuery__(cursor, 
			"SELECT COUNT(NAME) FROM droid WHERE TYPE='Folder'")

	def countTotalUnidentifiedQuery(self, cursor):
		self.unidentifiedfilecount = self.__countQuery__(cursor, 
			"SELECT COUNT(NAME) FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (METHOD='no value' OR METHOD='Extension')")	

	def countZeroID(self, cursor):
		self.zeroidcount = self.__countQuery__(cursor, 
			"SELECT COUNT(NAME) FROM droid WHERE METHOD='no value' AND (TYPE='File' OR TYPE='Container')")

	def countExtensionIDOnly(self, cursor):
		self.extensionIDOnlyCount = self.__countQuery__(cursor, 
			"SELECT COUNT(NAME) FROM droid WHERE METHOD='Extension' AND(TYPE='File' OR TYPE='Container')")
	
	# PUIDS for files identified by DROID using binary matching techniques
	def countSignaturePUIDS(self, cursor):
		self.distinctbinpuidcount = self.__countQuery__(cursor, 
			"SELECT COUNT(DISTINCT PUID) FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (METHOD='Signature' OR METHOD='Container')")
		
	def countExtensionPUIDS(self, cursor):
		self.distinctextpuidcount = self.__countQuery__(cursor, 
			"SELECT COUNT(DISTINCT PUID) FROM droid WHERE (TYPE='File' OR TYPE='Container') AND METHOD='Extension'")

	def countExtensions(self, cursor):
		self.distinctextensioncount = self.__countQuery__(cursor, 
			"SELECT COUNT(DISTINCT EXT) FROM droid WHERE TYPE='File' OR TYPE='Container'")




	def identifiedPUIDFrequency(self, cursor):
		#self.zeroidcount = self.__countQuery__(cursor, "SELECT COUNT(NAME) FROM droid WHERE TYPE='File' OR TYPE='Container' AND METHOD='no value'")
		test = "SELECT PUID, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (METHOD='Signature' OR METHOD='Container') GROUP BY PUID ORDER BY TOTAL DESC"
		cursor.execute(test)
		test = cursor.fetchall()
		return test

	def allExtensionsFrequency(self, cursor):
		#self.zeroidcount = self.__countQuery__(cursor, "SELECT COUNT(NAME) FROM droid WHERE TYPE='File' OR TYPE='Container' AND METHOD='no value'")		
		test = "SELECT EXT, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') GROUP BY EXT ORDER BY TOTAL DESC"
		cursor.execute(test)
		test = cursor.fetchall()
		return test




	def listUniqueMatchedPUIDS(self, cursor):
		countfiles = "SELECT DISTINCT PUID FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (METHOD='Signature' OR METHOD='Container')"
		cursor.execute(countfiles)
		test = cursor.fetchall()
		for t in test:
			print t[0]

	def listAllUniqueExtensions(self, cursor):	
		countfiles = "SELECT DISTINCT EXT FROM droid WHERE TYPE='File' OR TYPE='Container'"
		cursor.execute(countfiles)
		test = cursor.fetchall()
		for t in test:
			print t[0]

	def listExtensionOnlyIdentification(self, cursor):	
		countfiles = "SELECT DISTINCT PUID FROM droid WHERE TYPE='File' OR TYPE='Container' AND METHOD='Extension'"
		cursor.execute(countfiles)
		test = cursor.fetchall()
		for t in test:
			print t[0]








	def listTopTwenty(self, freqTuple, matchTotal, total, text):
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
	
		else:
			print "Format frequency: "
			#for t in test:
			#	print freqTuple[i][0] + "       COUNT: " + str(freqTuple[i][1])






	def paretoListings(self, cursor):
		# duplication in this function can potentially be removed through
		# effective use of classes...
	
		puidTotal = self.identifiedfilecount
		puidPareto = int(puidTotal * 0.80)
	
		extTotal = self.countExtensions(cursor)
		extPareto = int(extTotal * 0.80)

		self.listTopTwenty(self.identifiedPUIDFrequency(cursor), puidPareto, puidTotal, "identified PUIDS")
		self.listTopTwenty(self.allExtensionsFrequency(cursor), puidPareto, extTotal, "format extensions")




	def calculateIdentifiedPercent(self):
		allcount = self.filecount
		count = self.identifiedfilecount
		#if allcount > 0:
		#	percentage = (count/allcount)*100
		#	print "Percentage of the collection identified: " + '%.1f' % round(percentage, 1) + "%"
		#else:
		#	print "Zero files" 
		return count

	def calculateUnidentifiedPercent(self):
		allcount = self.filecount
		#if allcount > 0:
		#	percentage = (count/allcount)*100
		#	print "Percentage of the collection unidentified: " + '%.1f' % round(percentage, 1) + "%"
		#else:
		#	print "Zero files" 
		return count



	
	def is_ascii(self, s):
		 return all(ord(c) < 128 for c in s)

	def detect_invalid_characters(self, s):
		#http://msdn.microsoft.com/en-us/library/aa365247(VS.85).aspx
	
		#Strings for unit tests
		test_strings = ['COM4', 'COM4.txt', '.com4', 'abccom4text', 'abc.com4.txt.abc', 'con', 'CON', 'ף', 'י', 'צ', 'ףיצ', 'file[bracket]one.txt', 'file[two.txt', 'filethree].txt', '-=_|\"', '(<|>|:|"|/|\\|\?|\*|\||\x00-\x1f)']	
	
		# First test, all ASCII characters?
		for s in test_strings:
			if not is_ascii(s):
				print "We have some characters outside of ASCII range: " + s
	
		#regex strings...
	
		#CON|PRN|AUX|NUL
		msdn_bad_names_one = "(^)(con|prn|aux|nul)($|.|.[0-9a-zA-Z]{1,5}$)"		# badname + extension
		
		#COM1-COM9 | LPT1-LPT9
		msdn_bad_names_two = "((^)(COM|LPT)(.*[1-9]))($|(.[0-9a-zA-Z]{0,5}))"	# badname + extension
	
		#<, >, :, ", /, \, ?, *, |, \x00-\x1f
		non_recommended_chars = '(<|>|:|"|/|\\|\?|\*|\||\x00-\x1f)'

		#[]
		square_brackets = '(\[|\])'

		bad_names_one_regex = re.compile(msdn_bad_names_one, re.IGNORECASE)
		bad_names_two_regex = re.compile(msdn_bad_names_two, re.IGNORECASE)	
		bad_characters_regex = re.compile(non_recommended_chars, re.IGNORECASE)
		square_bracket_regex = re.compile(square_brackets, re.IGNORECASE)	
	
		for s in test_strings:	
			bad_tuples_one = re.findall(bad_names_one_regex, s)
			bad_tuples_two = re.findall(bad_names_two_regex, s)
			bad_char_tuples = re.findall(bad_characters_regex, s)
			bracket_tuples = re.findall(square_bracket_regex, s)	

			if bad_char_tuples:
				print "got some bad characters: " + s
			if bad_tuples_one or bad_tuples_two:
				print "Got some bad filenames: " + s
			if bracket_tuples:
				print "Got some square brackets: " + s

	def checkDodgyCharacters(self, cursor):
		countDirs = "SELECT DISTINCT DIR_NAME FROM droid"
		cursor.execute(countDirs)
		dirlist = cursor.fetchall()
		for d in dirlist:
			print d[0]

	

	def queryDB(self, cursor):
		self.countFilesQuery(cursor)
		self.countContainerObjects(cursor)
		self.countFilesInContainerObjects(cursor)
		self.countFoldersQuery(cursor)
		self.countTotalUnidentifiedQuery(cursor)
		self.countZeroID(cursor)
		self.countExtensionIDOnly(cursor)
		self.countSignaturePUIDS(cursor)
		self.countExtensionPUIDS(cursor)
		self.countExtensions(cursor)
		#self.paretoListings(cursor)
		#self.countUniqueDirs(cursor)

	def openDROIDDB(self, dbfilename):
		conn = sqlite3.connect(dbfilename)
		cursor = conn.cursor()
		self.queryDB(cursor)		# primary db query functions
		#self.detect_invalid_characters("s")		# need to pass strings to this... 
		conn.close()

def handleDROIDDB(dbfilename):
	analysis = DROIDAnalysis()	
	analysis.openDROIDDB(dbfilename)

def handleDROIDCSV(droidcsv):
	droid2sqlite.handleDROIDCSV(droidcsv)

def main():

	#	Usage: 	--csv [jp2file]

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
