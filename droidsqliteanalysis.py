# -*- coding: utf-8 -*-
from __future__ import division
import argparse
import sys
import sqlite3
import csv
import re
import droid2sqlite
from urlparse import urlparse

def countFilesQuery(c):
	countfiles = "SELECT COUNT(NAME) FROM droid WHERE TYPE='File' OR TYPE='Container'"
	c.execute(countfiles)
	count = c.fetchone()[0]
	print "Number of Files in collection: " + str(count)
	return count

# Container objects known by DROID...
def countContainerObjects(c):
	countfiles = "SELECT COUNT(NAME) FROM droid WHERE TYPE='Container'"
	c.execute(countfiles)
	count = c.fetchone()[0]
	print "Number of Container objects in collection: " + str(count)
	
	countfiles = "SELECT DISTINCT EXT FROM droid WHERE TYPE='Container'"
	c.execute(countfiles)
	test = c.fetchall()
	for t in test:
		print t[0]
	
	return count
	
def countFilesInContainerObjects(c):
	countfiles = "SELECT COUNT(NAME) FROM droid WHERE URI_SCHEME!='file' AND (TYPE='File' OR TYPE='Container')"
	c.execute(countfiles)
	count = c.fetchone()[0]
	print "Number of Files inside container objects: " + str(count)
	return count

def countFoldersQuery(c):
	countfiles = "SELECT COUNT(NAME) FROM droid WHERE TYPE='Folder'"
	c.execute(countfiles)
	count = c.fetchone()
	print "Number of Folders in collection: " + str(count[0])
	return count

def countIdentifiedQuery(c):
	allcount = countFilesQuery(c)
	countfiles = "SELECT COUNT(NAME) FROM droid WHERE (TYPE='File' OR TYPE='Container') AND METHOD='Signature'"
	c.execute(countfiles)
	count = c.fetchone()[0]
	print "Number of Identified Files in collectionxx: " + str(count)
	
	if allcount > 0:
		percentage = (count/allcount)*100
		print "Percentage of the collection identified: " + '%.1f' % round(percentage, 1) + "%"
	else:
		print "Zero files" 
	return count

def countTotalUnidentifiedQuery(c):
	allcount = countFilesQuery(c)
	countfiles = "SELECT COUNT(NAME) FROM droid WHERE TYPE='File' OR TYPE='Container' AND (METHOD='no value' OR METHOD='Extension')"
	c.execute(countfiles)
	count = c.fetchone()[0]
	print "Number of Unidentified Files in collection (ext only and zero ID method): " + str(count)
	
	if allcount > 0:
		percentage = (count/allcount)*100
		print "Percentage of the collection unidentified: " + '%.1f' % round(percentage, 1) + "%"
	else:
		print "Zero files" 
	return count
	
def countZeroIDMethod(c):
	countfiles = "SELECT COUNT(NAME) FROM droid WHERE TYPE='File' OR TYPE='Container' AND METHOD='no value'"
	c.execute(countfiles)
	count = c.fetchone()[0]
	print "Number of Unidentified files (zero ID method): " + str(count)
	return count

def countExtensionIDOnly(c):
	countfiles = "SELECT COUNT(NAME) FROM droid WHERE TYPE='File' OR TYPE='Container' AND METHOD='Extension'"
	c.execute(countfiles)
	count = c.fetchone()[0]
	print "Number of Extension only identifications: " + str(count)
	return count

# PUIDS for files identified by DROID using binary matching techniques
def countSignaturePUIDS(c):
	countfiles = "SELECT COUNT(DISTINCT PUID) FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (METHOD='Signature' OR METHOD='Container')"
	c.execute(countfiles)
	count = c.fetchone()[0]
	print "Number of unique 'signature' PUIDs: " + str(count)
	
	countfiles = "SELECT DISTINCT PUID FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (METHOD='Signature' OR METHOD='Container')"
	c.execute(countfiles)
	test = c.fetchall()
	for t in test:
		print t[0]
	
	return count
	
def countExtensionPUIDS(c):
	countfiles = "SELECT COUNT(DISTINCT PUID) FROM droid WHERE TYPE='File' OR TYPE='Container' AND METHOD='Extension'"
	c.execute(countfiles)
	count = c.fetchone()[0]
	print "Number of unique 'extension' PUIDs: " + str(count)
	
	countfiles = "SELECT DISTINCT PUID FROM droid WHERE TYPE='File' OR TYPE='Container' AND METHOD='Extension'"
	c.execute(countfiles)
	test = c.fetchall()
	for t in test:
		print t[0]
	
	return count

def countExtensions(c):
	countfiles = "SELECT COUNT(DISTINCT EXT) FROM droid WHERE TYPE='File' OR TYPE='Container'"
	c.execute(countfiles)
	count = c.fetchone()[0]
	print "Number of unique extensions: " + str(count)
	
	countfiles = "SELECT DISTINCT EXT FROM droid WHERE TYPE='File' OR TYPE='Container'"
	c.execute(countfiles)
	test = c.fetchall()
	for t in test:
		print t[0]

	return count

def identifiedPUIDFrequency(c):
	test = "SELECT PUID, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (METHOD='Signature' OR METHOD='Container') GROUP BY PUID ORDER BY TOTAL DESC"
	c.execute(test)
	test = c.fetchall()
	return test

def allExtensionsFrequency(c):
	test = "SELECT EXT, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') GROUP BY EXT ORDER BY TOTAL DESC"
	c.execute(test)
	test = c.fetchall()
	return test

def listTopTwenty(freqTuple, matchTotal, total, text):
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
		for t in test:
			print freqTuple[i][0] + "       COUNT: " + str(freqTuple[i][1])

def paretoListings(c):
	# duplication in this function can potentially be removed through
	# effective use of classes...
	
	puidTotal = countIdentifiedQuery(c)
	puidPareto = int(puidTotal * 0.80)
	
	extTotal = countExtensions(c)
	extPareto = int(extTotal * 0.80)

	listTopTwenty(identifiedPUIDFrequency(c), puidPareto, puidTotal, "identified PUIDS")
	listTopTwenty(allExtensionsFrequency(c), puidPareto, extTotal, "format extensions")
	
def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def detect_invalid_characters(s):
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

def queryDB(cursor):
	countFilesQuery(cursor)
	countContainerObjects(cursor)
	countFilesInContainerObjects(cursor)
	countFoldersQuery(cursor)
	countTotalUnidentifiedQuery(cursor)
	countZeroIDMethod(cursor)
	countExtensionIDOnly(cursor)
	countSignaturePUIDS(cursor)
	countExtensionPUIDS(cursor)
	countExtensions(cursor)
	paretoListings(cursor)

def openDROIDDB(dbfilename):
	conn = sqlite3.connect(dbfilename)
	cursor = conn.cursor()
	# queryDB(cursor)		# primary db query functions
	detect_invalid_characters("s")		# need to pass strings to this... 
	conn.close()

def handleDROIDDB(dbfilename):
	openDROIDDB(dbfilename)

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
