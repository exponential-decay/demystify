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
from AnalysisQueriesClass import AnalysisQueries
from urlparse import urlparse
from lxml import etree, html

class DROIDAnalysis:

   def __init__(self, config=False):
      self.config = self.__readconfig__(config)
         
      self.analysisresults = DroidAnalysisResultsClass.DROIDAnalysisResults()

   def __version__(self):
      self.analysisresults.__version__ = '0.3.0' #need something reasonable here...
      return self.analysisresults.__version__

   def __readconfig__(self, config):
      configout = False
      
      self.blacklistpuids = False
      self.blacklistzeros = False
      
      #self.roguesduplicatenames = True // to implement

      self.roguesduplicatechecksums = True
      self.roguepuids = False
      
      if config != False:
         if config.has_section('rogues'):
            if config.has_option('rogues', 'duplicatechecksums'):
               self.roguesduplicatechecksums = config.get('rogues', 'duplicatechecksums').lower()
            if config.has_option('rogues', 'roguepuids'):
               self.roguepuids = config.get('rogues', 'roguepuids').split(',')  

      return configout

   ## DB self.cursor
   cursor = None
   
   def __querydb__(self, query, fetchone=False, numberquery=False):
      self.cursor.execute(query)
      if fetchone is True and numberquery is False:
         return self.cursor.fetchone()
      if fetchone is True and numberquery is True:
         return self.cursor.fetchone()[0]
      else:
         return self.cursor.fetchall()   
   
   def __countQuery__(self, query):
      self.cursor.execute(query)
      count = self.cursor.fetchone()[0]
      return count

   '''def __listQuery1__(self, query):
      self.cursor.execute(query)
      result = self.cursor.fetchall()
      resultlist = []
      for r in result:
         resultlist.append(r[0])
      return resultlist'''

   def __listQuery__(self, query):
      self.cursor.execute(query)
      result = self.cursor.fetchall()
      return result

   '''def __listPUIDSQuery__(self, query, separator=False):
      self.cursor.execute(query)
      result = self.cursor.fetchall()
      return result'''

   def __listDuplicateQuery__(self, query):
      self.cursor.execute(query)
      result = self.cursor.fetchall()
      examples = []
      for a in result:
         examples.append(str(a[0]))
      return examples

   def __alternativeFrequencyQuery__(self, query):
      self.cursor.execute(query)
      result = self.cursor.fetchall()
      return result
      
   def countZeroByteObjects(self):
      return self.__countQuery__( 
         "SELECT COUNT(SIZE) FROM droid WHERE (TYPE='File') AND (SIZE='0')")
      return

   ###
   # Frequency list queries
   ###
   def dateRangeFrequency(self):
      return self.__listPUIDSQuery__("SELECT YEAR, COUNT(YEAR) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') GROUP BY YEAR ORDER BY TOTAL DESC")

   def extensionOnlyIdentificationFrequency(self):
      return self.__listQuery__( 
         "SELECT PUID, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (METHOD='Extension') GROUP BY PUID ORDER BY TOTAL DESC",  " | ")

   def allExtensionsFrequency(self):
      return self.__listQuery__(
         "SELECT EXT, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') GROUP BY EXT ORDER BY TOTAL DESC")

   ###
   # List queries
   ###
   def listUniqueBinaryMatchedPUIDS(self):
      return self.__listPUIDSQuery__(
         "SELECT DISTINCT PUID, FORMAT_NAME, FORMAT_VERSION FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (METHOD='Signature' OR METHOD='Container')", "\n")

   def listAllUniqueExtensions(self):	
      return self.__listQuery__(
         "SELECT DISTINCT EXT FROM droid WHERE (TYPE='File' OR TYPE='Container')")

   def listExtensionOnlyIdentificationPUIDS(self):	
      return self.__listQuery__(		
         "SELECT DISTINCT PUID, FORMAT_NAME FROM droid WHERE (TYPE='File' OR TYPE='Container') AND METHOD='Extension'")

   def listMultipleIdentifications(self):
      return self.__listQuery1__(		
         "SELECT FILE_PATH FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (FORMAT_COUNT!='1' AND FORMAT_COUNT!='0') AND (CAST(SIZE AS INT) > 0)")
      return

   def listContainerTypes(self):
      return self.__listQuery__(
         "SELECT DISTINCT URI_SCHEME FROM droid WHERE (TYPE='File' AND URI_SCHEME!='file')")

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

   def listDuplicateFilesFromHASH(self):		
      duplicatequery = "SELECT HASH, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') GROUP BY HASH ORDER BY TOTAL DESC"
      result = self.__alternativeFrequencyQuery__(duplicatequery)
      
      duplicatestr = {}
      duplicatelist = []
      totalduplicates = 0

      for r in result:     #result = (hash, count)
         count = r[1]
         if count > 1:
            totalduplicates = totalduplicates + count
            duplicateHASH = r[0]
            examples = self.__listDuplicateQuery__("SELECT FILE_PATH FROM droid WHERE HASH='" + duplicateHASH + "'ORDER BY DIR_NAME")          
            duplicatestr['checksum'] = str(duplicateHASH)
            duplicatestr['count'] = str(count)
            duplicatestr['examples'] = examples
            duplicatelist.append(duplicatestr)
            duplicatestr = {}

      self.analysisresults.totalHASHduplicates = totalduplicates
      return duplicatelist

   def listRoguePUIDs(self, puidlist):
      searchlist = []
      for puid in puidlist:
         puidquery = "SELECT COUNT(*) AS total FROM droid WHERE (PUID='" + puid + "')"
         result = self.__countQuery__(puidquery)      
         if result > 0:
            searchlist.append(puid)

      roguepuidpathlist = []
      for p in searchlist:
         roguepuidpathlist = roguepuidpathlist + self.__listQuery1__("SELECT FILE_PATH FROM droid WHERE PUID='" + p + "' ORDER BY FILE_PATH DESC")

      return roguepuidpathlist

   def listDuplicateHASHFilepaths(self):
      duplicatequery = "SELECT HASH, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') GROUP BY HASH ORDER BY TOTAL DESC"
      result = self.__alternativeFrequencyQuery__(duplicatequery)
      
      duplicatestr = ''
      duplicatelist = []
      totalduplicates = 0
      for r in result:
         count = r[1]
         if count > 1:
            totalduplicates = totalduplicates + count
            duplicatestr = self.__listQuery1__("SELECT FILE_PATH FROM droid WHERE HASH='" + r[0] + "' ORDER BY FILE_PATH DESC")
            duplicatelist = duplicatelist + duplicatestr
      self.analysisresults.totalHASHduplicates = totalduplicates
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

   #TODO: Delete and refine functions above...
   def listTopItems(self, frequencyQueryResult, number):
      return frequencyQueryResult[0:number]

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
      
   def determineifHASHwasused(self):
      return self.__countQuery__(
         "select count(*) from DROID where HASH != 'no value' and  TYPE = 'File'")
   
   def __generatefilenamelistwithdirs__(self):
      countDirs = "SELECT DIR_NAME, NAME FROM droid"
      self.cursor.execute(countDirs)
      self.fdirlist = self.cursor.fetchall()

   def __generatefilepathlistnodirs__(self):
      pathlist = []
      allfilepaths = "SELECT FILE_PATH FROM DROID WHERE TYPE != 'Folder' and FILE_PATH != 'no value'"     
      self.cursor.execute(allfilepaths)
      for x in self.cursor.fetchall():
         pathlist.append(x[0])
      return pathlist
     
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
   
   def __getHashAlgorithm__(self):
      hashtype = 0
      findhash = "SELECT HASH_TYPE from DBMD;"
      self.cursor.execute(findhash)
      result = self.cursor.fetchone()[0]
      if result is not None:
         hashtype = result
      return hashtype 
        
   def queryDB(self):
      #preliminary functions to generate data from DB
      self.fnamelist = self.__querydb__(AnalysisQueries.SELECT_ALL_NAMES)
      self.fdirlist = self.__querydb__(AnalysisQueries.SELECT_FILENAMES_AND_DIRNAMES)
      
      self.hashtype = self.__querydb__(AnalysisQueries.SELECT_HASH, True)[0]
      if self.hashtype == "None":
         sys.stderr.write(AnalysisQueries.ERROR_NOHASH + "\n")

      self.analysisresults.collectionsize = self.__querydb__(AnalysisQueries.SELECT_COLLECTION_SIZE, True, True)
      self.analysisresults.filecount = self.__querydb__(AnalysisQueries.SELECT_COUNT_FILES, True, True)
      self.analysisresults.containercount = self.__querydb__(AnalysisQueries.SELECT_COUNT_CONTAINERS, True, True)
      self.analysisresults.filesincontainercount = self.__querydb__(AnalysisQueries.SELECT_COUNT_FILES_IN_CONTAINERS, True, True)
      self.analysisresults.directoryCount = self.__querydb__(AnalysisQueries.SELECT_COUNT_FOLDERS, True, True)
      self.analysisresults.uniqueFileNames = self.__querydb__(AnalysisQueries.SELECT_COUNT_UNIQUE_FILENAMES, True, True)
      self.analysisresults.uniqueDirectoryNames = self.__querydb__(AnalysisQueries.SELECT_COUNT_UNIQUE_DIRNAMES, True, True)
      self.analysisresults.identifiedfilecount = self.__querydb__(AnalysisQueries.SELECT_COUNT_IDENTIFIED_FILES, True, True)
      self.analysisresults.multipleidentificationcount = self.__querydb__(AnalysisQueries.SELECT_COUNT_MULTIPLE_ID, True, True)
      self.analysisresults.unidentifiedfilecount = self.__querydb__(AnalysisQueries.SELECT_COUNT_UNIDENTIFIED, True, True)            
      self.analysisresults.extensionIDOnlyCount = self.__querydb__(AnalysisQueries.SELECT_COUNT_EXTENSION_ONLY, True, True)
      self.analysisresults.distinctSignaturePuidcount = self.__querydb__(AnalysisQueries.SELECT_COUNT_FORMAT_RANGE, True, True)            
      self.analysisresults.distinctextensioncount = self.__querydb__(AnalysisQueries.SELECT_COUNT_EXTENSION_RANGE, True, True)
      self.analysisresults.extmismatchCount = self.__querydb__(AnalysisQueries.SELECT_COUNT_MISMATCHES, True, True)

      self.analysisresults.idmethodFrequency = self.__querydb__(AnalysisQueries.SELECT_METHOD_FREQUENCY_COUNT)      
      self.analysisresults.mimetypeFrequency = self.__querydb__(AnalysisQueries.SELECT_MIME_FREQUENCY_COUNT)
      
      
      self.analysisresults.zeroidcount = self.__querydb__(AnalysisQueries.SELECT_COUNT_ZEROID, True, True)
      

      #NOTE: Must be calculated after we have total, and subset values
      self.analysisresults.identifiedPercentage = self.calculatePercent(self.analysisresults.filecount, self.analysisresults.identifiedfilecount)		
      self.analysisresults.unidentifiedPercentage = self.calculatePercent(self.analysisresults.filecount, self.analysisresults.unidentifiedfilecount)



      self.analysisresults.sigIDPUIDList = self.__querydb__(AnalysisQueries.SELECT_BINARY_MATCH_COUNT)

      
      #self.analysisresults.dateFrequency = self.dateRangeFrequency()
      
      
      '''self.analysisresults.sigIDPUIDFrequency = self.identifiedBinaryMatchedPUIDFrequency()
      self.analysisresults.extensionOnlyIDList = self.listExtensionOnlyIdentificationPUIDS()
      self.analysisresults.extensionOnlyIDfnameList = self.listExtensionIDOnly()
      self.analysisresults.extensionOnlyIDFrequency = self.extensionOnlyIdentificationFrequency()
      self.analysisresults.uniqueExtensionsInCollectionList = self.listAllUniqueExtensions()
      self.analysisresults.frequencyOfAllExtensions = self.allExtensionsFrequency()
      self.analysisresults.filesWithNoIDList = self.listNoIdentificationFiles()
      self.analysisresults.extmismatchList = self.listExtensionMismatches()
      
      self.analysisresults.multipleIDList = self.listMultipleIdentifications()
      
      #expensive duplicate checking [default: ON]
      self.analysisresults.duplicateHASHlisting = self.listDuplicateFilesFromHASH()

      self.analysisresults.topPUIDList = self.topPUIDS(5)
      self.analysisresults.topExtensionList = self.topExts(5)		
      self.analysisresults.containertypeslist = self.listContainerTypes()
      
      self.analysisresults.zerobytecount = self.countZeroByteObjects()
      self.analysisresults.zerobytelist = self.listZeroByteObjects()

      self.analysisresults.badFilenames = self.msoftfnameanalysis()

      self.analysisresults.allfilepaths = self.__generatefilepathlistnodirs__()

      #rogues
      self.analysisresults.duplicateHASHpathlisting = False
               
      if self.roguesduplicatechecksums == "true":
         self.analysisresults.duplicateHASHpathlisting = self.listDuplicateHASHFilepaths()
      else:
         sys.stderr.write("Rogue gallery: Will not output paths for duplicate checksums." + "\n")

      if self.roguepuids != False:
         sys.stderr.write("Rogue gallery: Will output rogue PUIDs in rogue listing." + "\n")
         self.analysisresults.roguepuidlisting = self.listRoguePUIDs(self.roguepuids)

      '''

      return self.analysisresults
      
   def openDROIDDB(self, dbfilename):
      self.analysisresults.filename = dbfilename.rstrip('.db')
   
      conn = sqlite3.connect(dbfilename)
      conn.text_factory = str		#encoded as ascii, not unicode / return ascii
      
      self.cursor = conn.cursor()
      analysisresults = self.queryDB()		# primary db query functions
      
      conn.close()

      return self.analysisresults
