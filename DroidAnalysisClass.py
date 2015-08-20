# -*- coding: utf-8 -*-

from __future__ import division
import argparse
import sys
import sqlite3
import csv
import droid2sqlite
import droidsqliteanalysis
import MsoftFnameAnalysis
import RegexFnameAnalysis
import DroidAnalysisResultsClass
from urlparse import urlparse
from lxml import etree, html

class DROIDAnalysis:

   def __init__(self, config=False):
      self.config = self.__readconfig__(config)
         
      self.analysisresults = DroidAnalysisResultsClass.DROIDAnalysisResults()

   def __version__(self):
      self.analysisresults.__version__ = '0.0.x' #0.0.4
      return self.analysisresults.__version__

   def __readconfig__(self, config):
      configout = False
      
      self.blacklistpuids = False
      self.blacklistzeros = False
      
      self.roguesduplicatechecksums = True
      self.roguesduplicatenames = True
      
      if config != False:
         if config.has_section('rogues'):
            if config.has_option('rogues', 'duplicatechecksums'):
               self.roguesduplicatechecksums = config.get('rogues', 'duplicatechecksums').lower()
            if config.has_option('rogues', 'duplicatenames'):
               self.roguesduplicatenames = config.get('rogues', 'duplicatenames').lower()
      
      return configout

   ## DB self.cursor
   cursor = None
   
   def __countQuery__(self, query):
      self.cursor.execute(query)
      count = self.cursor.fetchone()[0]
      return count

   def __listQuery1__(self, query):
      self.cursor.execute(query)
      result = self.cursor.fetchall()
      resultlist = []
      for r in result:
         resultlist.append(r[0])
      return resultlist

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
      try:
         if row[len(row)-2] == "|":
            return row[:-2]
         else:
            return row[:-1]
      except IndexError:
         return row[:-1]
         
   def __listPUIDSQuery__(self, query, separator):
      self.cursor.execute(query)
      result = self.cursor.fetchall()
      row = []
      for r in result:
         if len(r) > 1:
            item = ""
            for t in r:
               item = item + str(t) + ", "
            row.append(item[:-2])
         else:
            row.append(str(r[0]))
      return row


   def __listDuplicateQuery__(self, query, separator):
      self.cursor.execute(query)
      result = self.cursor.fetchall()
      row = ""
      for r in result:
         if len(r) == 2:
            item = "Context: " + r[0] + "\n Filename: " + r[1] + '\n\n'
            row = row + item
      try:
         if row[len(row)-2] == "|":
            return row[:-2]
         else:
            return row[:-1]
      except IndexError:
         return row[:-1]

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
         "SELECT COUNT(NAME) FROM droid WHERE (URI_SCHEME!='file') AND (TYPE='File' OR TYPE='Container')")

   def countFoldersQuery(self):
      return self.__countQuery__( 
         "SELECT COUNT(NAME) FROM droid WHERE TYPE='Folder'")

   def countUniqueFileNames(self):
      return self.__countQuery__( 
         "SELECT COUNT(DISTINCT NAME) FROM droid WHERE (TYPE='File' OR TYPE='Container')")

   def countUniqueDirectoryNames(self):
      return (self.__countQuery__( 
         "SELECT COUNT(DISTINCT DIR_NAME) FROM droid") - 1)	#Will always be minus one accounts for base-dirs

   def countIdentifiedQuery(self):
      return self.__countQuery__( 
         "SELECT COUNT(NAME) FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (METHOD='Signature' or METHOD='Container')")

   def countMultipleIdentifications(self):
      return self.__countQuery__( 
         "SELECT COUNT(FORMAT_COUNT) FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (FORMAT_COUNT!='1' AND FORMAT_COUNT!='0')")

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
   
   def countExtensionMismatches(self):
      return self.__countQuery__( 
         "SELECT COUNT(EXTENSION_MISMATCH) FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (EXTENSION_MISMATCH='true')")	

   def countZeroByteObjects(self):
      return self.__countQuery__( 
         "SELECT COUNT(SIZE) FROM droid WHERE (TYPE='File') AND (SIZE='0')")
      return

   ###
   # Frequency list queries
   ###
   def identifiedBinaryMatchedPUIDFrequency(self):
      return self.__listPUIDSQuery__( 
         "SELECT PUID, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (METHOD='Signature' OR METHOD='Container') GROUP BY PUID ORDER BY TOTAL DESC",  " | ")

   def extensionOnlyIdentificationFrequency(self):
      return self.__listQuery__( 
         "SELECT PUID, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (METHOD='Extension') GROUP BY PUID ORDER BY TOTAL DESC",  " | ")

   def allExtensionsFrequency(self):
      return self.__listQuery__(
         "SELECT EXT, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') GROUP BY EXT ORDER BY TOTAL DESC", " | ")

   def idmethodFrequencyCount(self):
      return self.__listQuery__(
         "SELECT METHOD, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') GROUP BY METHOD ORDER BY TOTAL DESC", "\n")	
   

   def mimetypeFrequencyCount(self):
      return self.__listQuery__(
         "SELECT MIME_TYPE, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') GROUP BY MIME_TYPE ORDER BY TOTAL DESC", " | ")

   ###
   # List queries
   ###
   def listUniqueBinaryMatchedPUIDS(self):
      return self.__listPUIDSQuery__(
         "SELECT DISTINCT PUID, FORMAT_NAME, FORMAT_VERSION FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (METHOD='Signature' OR METHOD='Container')", "\n")

   def listAllUniqueExtensions(self):	
      return self.__listQuery__(
         "SELECT DISTINCT EXT FROM droid WHERE (TYPE='File' OR TYPE='Container')", " | ")

   def listExtensionOnlyIdentificationPUIDS(self):	
      return self.__listQuery__(		
         "SELECT DISTINCT PUID, FORMAT_NAME FROM droid WHERE (TYPE='File' OR TYPE='Container') AND METHOD='Extension'", " | ")

   def listMultipleIdentifications(self):
      return self.__listQuery1__(		
         "SELECT FILE_PATH FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (FORMAT_COUNT!='1' AND FORMAT_COUNT!='0')")
      return

   def listContainerTypes(self):
      return self.__listQuery__(
         "SELECT DISTINCT URI_SCHEME FROM droid WHERE (TYPE='File' AND URI_SCHEME!='file')", " | ")

   def listNoIdentificationFiles(self):
      return self.__listQuery1__(	
         "SELECT FILE_PATH FROM droid WHERE METHOD='no value' AND (TYPE='File' OR TYPE='Container')")

   def listZeroByteObjects(self):
      return self.__listQuery1__(	
         "SELECT FILE_PATH FROM droid WHERE TYPE='File' AND SIZE='0'")

   def listExtensionIDOnly(self):
      return self.__listQuery1__( 
         "SELECT FILE_PATH FROM droid WHERE METHOD='Extension' AND(TYPE='File' OR TYPE='Container')")
    
   def listExtensionMismatches(self):
      return self.__listQuery1__( 
         "SELECT FILE_PATH FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (EXTENSION_MISMATCH='true')")   

   def listDuplicateFilenames(self):
      duplicatequery = "SELECT NAME, COUNT(NAME) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') GROUP BY NAME ORDER BY TOTAL DESC"
      result = self.__alternativeFrequencyQuery__(duplicatequery)
      
      duplicatestr = ''
      duplicatelist = []
      totaluniquefilenames = 0
      for r in result:
         count = r[1]
         if count > 1:
            totaluniquefilenames = totaluniquefilenames + 1
            duplicatename = r[0]
            duplicatestr = duplicatestr + "Count: " + str(count) + " , " + "Name: " + duplicatename + '\n'
            duplicatelist.append(duplicatestr)
            duplicatestr = ''
      self.analysisresults.totaluniquefilenames = totaluniquefilenames
      return duplicatelist

   def listDuplicateFilesFromMD5(self):		
      duplicatequery = "SELECT MD5_HASH, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') GROUP BY MD5_HASH ORDER BY TOTAL DESC"
      result = self.__alternativeFrequencyQuery__(duplicatequery)
      
      duplicatestr = ''
      duplicatelist = []
      totalduplicates = 0
      for r in result:
         count = r[1]
         if count > 1:
            totalduplicates = totalduplicates + count
            duplicatemd5 = r[0]
            duplicatestr = "Count: " + str(count) + '\n'
            duplicatestr = duplicatestr + "Duplicate checksum: " + duplicatemd5 + '\n\n'
            duplicatestr = duplicatestr + self.__listDuplicateQuery__("SELECT DIR_NAME, NAME FROM droid WHERE MD5_HASH='" + duplicatemd5 + "' ORDER BY DIR_NAME", "\n\n")
            duplicatelist.append(duplicatestr)
      self.analysisresults.totalmd5duplicates = totalduplicates
      return duplicatelist

   def listDuplicateFnameFilepaths(self):
      duplicatequery = "SELECT NAME, COUNT(NAME) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') GROUP BY NAME ORDER BY TOTAL DESC"
      result = self.__alternativeFrequencyQuery__(duplicatequery)
      
      duplicatestr = ''
      duplicatelist = []
      totaluniquefilenames = 0
      duplicatenames = []
      for r in result:
         count = r[1]
         if count > 1:
            totaluniquefilenames = totaluniquefilenames + 1
            duplicatename = r[0]
            duplicatelist = duplicatelist + self.__listQuery1__('SELECT FILE_PATH FROM droid WHERE NAME="' + duplicatename + '" ORDER BY FILE_PATH DESC')
      self.analysisresults.totaluniquefilenames = totaluniquefilenames
      return duplicatelist

   def listDuplicateMD5Filepaths(self):
      duplicatequery = "SELECT MD5_HASH, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') GROUP BY MD5_HASH ORDER BY TOTAL DESC"
      result = self.__alternativeFrequencyQuery__(duplicatequery)
      
      duplicatestr = ''
      duplicatelist = []
      totalduplicates = 0
      for r in result:
         count = r[1]
         if count > 1:
            totalduplicates = totalduplicates + count
            duplicatestr = self.__listQuery1__("SELECT FILE_PATH FROM droid WHERE MD5_HASH='" + r[0] + "' ORDER BY FILE_PATH DESC")
            duplicatelist = duplicatelist + duplicatestr
      self.analysisresults.totalmd5duplicates = totalduplicates
      return duplicatelist    









   ###
   # Top n listings...
   ###
   def topPUIDS(self, number):
      # Hypothesis: 80% of the effects come from 20% of the causes		

      eightyPercentTotalPUIDs = int(self.analysisresults.identifiedfilecount * 0.80)		# 80 percent figure
      countIdentifiedPuids = "SELECT PUID, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (METHOD='Signature' OR METHOD='Container') GROUP BY PUID ORDER BY TOTAL DESC"
      return self.listTopItems(self.__alternativeFrequencyQuery__(countIdentifiedPuids), number)
      
   def topExts(self, number):
      # Hypothesis: 80% of the effects come from 20% of the causes		

      eightyPercentTotalExts = int(self.analysisresults.filecount * 0.80)		# 80 percent figure
      countExtensions = "SELECT EXT, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') GROUP BY EXT ORDER BY TOTAL DESC"
      return self.listTopItems(self.__alternativeFrequencyQuery__(countExtensions), number)

   def listTopItems(self, frequencyQueryResult, number):
      toptwentystr = ''
      
      try:
         for i in range(number):
            label = frequencyQueryResult[i][0]
            count = frequencyQueryResult[i][1]
            toptwentystr = toptwentystr + label + "       count: " + str(count) + "\n"
      except IndexError:
         # No more values we can list so return string as is...
         toptwentystr = toptwentystr
         
      return toptwentystr

   ###
   # Stats output...
   ###
   def calculatePercent(self, total, subset):
      if total > 0:
         percentage = (subset/total)*100
         return '%.1f' % round(percentage, 1)

   ###
   # Additional functions on DB
   ###
   
   def __generatefilenamelist__(self):
      #multi-use variable: get filenames from DB
      countDirs = "SELECT NAME FROM droid"
      self.cursor.execute(countDirs)
      self.fnamelist = self.cursor.fetchall()
      
   def __generatefilenamelistwithdirs__(self):
      countDirs = "SELECT DIR_NAME, NAME FROM droid"
      self.cursor.execute(countDirs)
      self.fdirlist = self.cursor.fetchall()
      
   def msoftfnameanalysis(self):
      charcheck = MsoftFnameAnalysis.MsoftFnameAnalysis()
      fnamereport = []
      #Pass filename to fname analysis
      for d in self.fnamelist:
         fnamestring = d[0]
         checkedname = charcheck.completeFnameAnalysis(fnamestring).encode('utf-8')
         if checkedname != '':
            fnamereport.append(checkedname)
      return fnamereport
                  
   def fileswithspaces(self):
      multiplespacelist = []
      charcheck = RegexFnameAnalysis.RegexFnameAnalysis()
      
      for d in self.fdirlist:
         if len(d) != 2:
            sys.stderr.write("File name, directory list pair is irregular (!=2). Exiting...\n")
            sys.exit(1)
         else:
            fnamestring = d[1]
            if charcheck.detectMultipleSpaces(fnamestring) == True:
               multiplespacelist.append(d)
      return multiplespacelist
         
   def queryDB(self):
      #preliminary functions to generate data from DB
      self.__generatefilenamelist__()
      self.__generatefilenamelistwithdirs__()
   
      self.analysisresults.filecount = self.countFilesQuery()
      self.analysisresults.containercount = self.countContainerObjects()
      self.analysisresults.filesincontainercount = self.countFilesInContainerObjects()
      self.analysisresults.directoryCount = self.countFoldersQuery()
      self.analysisresults.uniqueFileNames = self.countUniqueFileNames()
      self.analysisresults.uniqueDirectoryNames = self.countUniqueDirectoryNames()
      self.analysisresults.identifiedfilecount = self.countIdentifiedQuery()
      self.analysisresults.multipleidentificationcount = self.countMultipleIdentifications()
      self.analysisresults.unidentifiedfilecount = self.countTotalUnidentifiedQuery()
      self.analysisresults.extensionIDOnlyCount = self.countExtensionIDOnly()
      self.analysisresults.distinctSignaturePuidcount = self.countDistinctSignaturePUIDS()
      self.analysisresults.distinctextensioncount = self.countDistinctExtensions()
      self.analysisresults.extmismatchCount = self.countExtensionMismatches()
      
      self.analysisresults.idmethodFrequency = self.idmethodFrequencyCount()
      self.analysisresults.mimetypeFrequency = self.mimetypeFrequencyCount()
      
      self.analysisresults.zeroidcount = self.countZeroID()

      #NOTE: Must be calculated after we have total, and subset values
      self.analysisresults.identifiedPercentage = self.calculatePercent(self.analysisresults.filecount, self.analysisresults.identifiedfilecount)		
      self.analysisresults.unidentifiedPercentage = self.calculatePercent(self.analysisresults.filecount, self.analysisresults.unidentifiedfilecount)

      self.analysisresults.sigIDPUIDList = self.listUniqueBinaryMatchedPUIDS()
      self.analysisresults.sigIDPUIDFrequency = self.identifiedBinaryMatchedPUIDFrequency()
      self.analysisresults.extensionOnlyIDList = self.listExtensionOnlyIdentificationPUIDS()
      self.analysisresults.extensionOnlyIDfnameList = self.listExtensionIDOnly()
      self.analysisresults.extensionOnlyIDFrequency = self.extensionOnlyIdentificationFrequency()
      self.analysisresults.uniqueExtensionsInCollectionList = self.listAllUniqueExtensions()
      self.analysisresults.frequencyOfAllExtensions = self.allExtensionsFrequency()
      self.analysisresults.filesWithNoIDList = self.listNoIdentificationFiles()
      self.analysisresults.extmismatchList = self.listExtensionMismatches()
      
      self.analysisresults.multipleIDList = self.listMultipleIdentifications()
      
      #expensive duplicate checking [default: ON]
      self.analysisresults.duplicatefnamelisting = self.listDuplicateFilenames()
      self.analysisresults.duplicatemd5listing = self.listDuplicateFilesFromMD5()

      self.analysisresults.topPUIDList = self.topPUIDS(5)
      self.analysisresults.topExtensionList = self.topExts(5)		
      self.analysisresults.containertypeslist = self.listContainerTypes()
      
      self.analysisresults.zerobytecount = self.countZeroByteObjects()
      self.analysisresults.zerobytelist = self.listZeroByteObjects()

      self.analysisresults.badFilenames = self.msoftfnameanalysis()
      self.analysisresults.multiplespacelist = self.fileswithspaces()

      #rogues
      if self.roguesduplicatenames == "true":
         self.analysisresults.duplicatefnamepathlisting = self.listDuplicateFnameFilepaths()
         
      if self.roguesduplicatechecksums == "true":
         self.analysisresults.duplicatemd5pathlisting = self.listDuplicateMD5Filepaths()

      return self.analysisresults
      
   def openDROIDDB(self, dbfilename):
      self.analysisresults.filename = dbfilename.rstrip('.db')
   
      conn = sqlite3.connect(dbfilename)
      conn.text_factory = str		#encoded as ascii, not unicode / return ascii
      
      self.cursor = conn.cursor()
      analysisresults = self.queryDB()		# primary db query functions
      
      conn.close()

      return self.analysisresults
