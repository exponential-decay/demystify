# -*- coding: utf-8 -*-

from __future__ import division
import argparse
import sys
import sqlite3
import csv
import droid2sqlite
import htmloutputclass
import textoutputclass
import droidsqliteanalysis
import MsoftFnameAnalysis
import RegexFnameAnalysis
from urlparse import urlparse
from lxml import etree, html

class DROIDAnalysis:

   def __version__(self):
      self.__version__ = '0.0.x' #0.0.4
      return self.__version__

   ## DB self.cursor
   cursor = None

   # Counts
   filecount = 0
   containercount = 0
   filesincontainercount = 0	
   directoryCount = 0
   uniqueFileNames = 0
   uniqueDirectoryNames = 0
   identifiedfilecount = 0
   multipleidentificationcount = 0 
   unidentifiedfilecount = 0
   distinctSignaturePuidcount = 0
   extensionIDOnlyCount = 0
   distinctextensioncount = 0
   extmismatchCount = 0
   zeroidcount = 0
   
   unidentifiedPercentage = 0
   identifiedPercentage = 0
   
   sigIDPUIDList = 0
   sigIDPUIDFrequency = 0
   
   extensionOnlyIDList = 0
   extensionOnlyIDFrequency = 0
   
   #TODO: Turn lists into lists? Formatting at end..?
   uniqueExtensionsInCollectionList = 0
   multipleIDList = 0
   frequencyOfAllExtensions = 0
   
   idmethodFrequency = 0
   
   mimetypeFrequency = 0
   
   filesWithNoIDList = 0
   topPUIDList = 0
   topExtensionList = 0
   
   totalmd5duplicates = 0
   duplicatemd5listing = []

   totaluniquefilenames = 0
   duplicatefnamelisting = [] 
   
   containertypeslist = 0
   
   zerobytecount = 0
   zerobytelist = 0
   
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
      return self.__listQuery__(		
         "SELECT FILE_PATH FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (FORMAT_COUNT!='1' AND FORMAT_COUNT!='0')", "\n")
      return

   def listContainerTypes(self):
      return self.__listQuery__(
         "SELECT DISTINCT URI_SCHEME FROM droid WHERE (TYPE='File' AND URI_SCHEME!='file')", " | ")

   def listNoIdentificationFiles(self):
      return self.__listQuery__(	
         "SELECT FILE_PATH FROM droid WHERE METHOD='no value' AND (TYPE='File' OR TYPE='Container')", "\n")

   def listZeroByteObjects(self):
      return self.__listQuery__(	
         "SELECT FILE_PATH FROM droid WHERE TYPE='File' AND SIZE='0'", "\n")

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
      self.totaluniquefilenames = totaluniquefilenames
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
      self.totalmd5duplicates = totalduplicates
      return duplicatelist









   ###
   # Top n listings...
   ###
   def topPUIDS(self, number):
      # Hypothesis: 80% of the effects come from 20% of the causes		

      eightyPercentTotalPUIDs = int(self.identifiedfilecount * 0.80)		# 80 percent figure
      countIdentifiedPuids = "SELECT PUID, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (METHOD='Signature' OR METHOD='Container') GROUP BY PUID ORDER BY TOTAL DESC"
      return self.listTopItems(self.__alternativeFrequencyQuery__(countIdentifiedPuids), number)
      
   def topExts(self, number):
      # Hypothesis: 80% of the effects come from 20% of the causes		

      eightyPercentTotalExts = int(self.filecount * 0.80)		# 80 percent figure
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
   
      self.filecount = self.countFilesQuery()
      self.containercount = self.countContainerObjects()
      self.filesincontainercount = self.countFilesInContainerObjects()
      self.directoryCount = self.countFoldersQuery()
      self.uniqueFileNames = self.countUniqueFileNames()
      self.uniqueDirectoryNames = self.countUniqueDirectoryNames()
      self.identifiedfilecount = self.countIdentifiedQuery()
      self.multipleidentificationcount = self.countMultipleIdentifications()
      self.unidentifiedfilecount = self.countTotalUnidentifiedQuery()
      self.extensionIDOnlyCount = self.countExtensionIDOnly()
      self.distinctSignaturePuidcount = self.countDistinctSignaturePUIDS()
      self.distinctextensioncount = self.countDistinctExtensions()
      self.extmismatchCount = self.countExtensionMismatches()
      
      self.idmethodFrequency = self.idmethodFrequencyCount()
      self.mimetypeFrequency = self.mimetypeFrequencyCount()
      
      self.zeroidcount = self.countZeroID()

      #NOTE: Must be calculated after we have total, and subset values
      self.identifiedPercentage = self.calculatePercent(self.filecount, self.identifiedfilecount)		
      self.unidentifiedPercentage = self.calculatePercent(self.filecount, self.unidentifiedfilecount)

      self.sigIDPUIDList = self.listUniqueBinaryMatchedPUIDS()
      self.sigIDPUIDFrequency = self.identifiedBinaryMatchedPUIDFrequency()
      self.extensionOnlyIDList = self.listExtensionOnlyIdentificationPUIDS()
      self.extensionOnlyIDFrequency = self.extensionOnlyIdentificationFrequency()
      self.uniqueExtensionsInCollectionList = self.listAllUniqueExtensions()
      self.frequencyOfAllExtensions = self.allExtensionsFrequency()
      self.filesWithNoIDList = self.listNoIdentificationFiles()
      
      self.multipleIDList = self.listMultipleIdentifications()
      
      self.duplicatefnamelisting = self.listDuplicateFilenames()
      self.duplicatemd5listing = self.listDuplicateFilesFromMD5()
      self.topPUIDList = self.topPUIDS(5)
      self.topExtensionList = self.topExts(5)		
      self.containertypeslist = self.listContainerTypes()
      
      self.zerobytecount = self.countZeroByteObjects()
      self.zerobytelist = self.listZeroByteObjects()

      self.badFilenames = self.msoftfnameanalysis()
      self.multiplespacelist = self.fileswithspaces()

      #self.printText()
      self.printHTML()
      
   def printText(self):
      textout = textoutputclass.DROIDAnalysisTextOutput()
      
   def printHTML(self):
      htmlout = htmloutputclass.DROIDAnalysisHTMLOutput(self)
      sys.stdout.write(htmlout.printHTMLResults())
      
   def openDROIDDB(self, dbfilename):
      conn = sqlite3.connect(dbfilename)
      conn.text_factory = str		#encoded as ascii, not unicode / return ascii
      
      self.cursor = conn.cursor()
      self.queryDB()		# primary db query functions
      
      conn.close()