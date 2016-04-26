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

   #we need this value because we extract basedirs for all folders, including
   #the root directory of the extract, creating one additional entry
   #TODO: consider handling better...
   NONROOTBASEDIR = 1

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
   
   def __querydb__(self, query, fetchone=False, numberquery=False, tolist=False):
      self.cursor.execute(query)
      if fetchone is True and numberquery is False:
         return self.cursor.fetchone()
      if fetchone is True and numberquery is True:
         return self.cursor.fetchone()[0]      
      else:
         if tolist is False:
            return self.cursor.fetchall()
         else:
            list = []
            for result in self.cursor.fetchall():
               list.append(result[0])
            return list               
   
   def __alternativeFrequencyQuery__(self, query):
      self.cursor.execute(query)
      result = self.cursor.fetchall()
      return result
      
   ###
   # List queries

   '''def listExtensionIDOnly(self):
      return self.__listQuery1__( 
         "SELECT FILE_PATH FROM droid WHERE METHOD='Extension' AND(TYPE='File' OR TYPE='Container')")'''
    
   def listDuplicateFilesFromHASH(self):		
      result = self.__querydb__(AnalysisQueries.SELECT_COUNT_DUPLICATE_CHECKSUMS)

      duplicate_sum = {}
      duplicatelist = []
      
      self.analysisresults.totalHASHduplicates = 0
      for r in result:
         self.analysisresults.totalHASHduplicates = self.analysisresults.totalHASHduplicates + int(r[1])
        
      #result list([HASH, COUNT])      
      query = AnalysisQueries()      
      for r in result:               
         example = self.__querydb__(query.list_duplicate_paths(r[0]))
         pathlist = []
         for e in example:
            pathlist.append(e[0])
            self.analysisresults.duplicatespathlist.append(e[0])   #create path only listing

         duplicate_sum['checksum'] = str(r[0])
         duplicate_sum['count'] = str(r[1])
         duplicate_sum['examples'] = pathlist
         duplicatelist.append(duplicate_sum)
         duplicate_sum = {}
                  
      self.analysisresults.duplicateHASHlisting = duplicatelist
      return len(self.analysisresults.duplicateHASHlisting)

   def listzerobytefiles(self):
      self.analysisresults.zerobytecount = self.__querydb__(AnalysisQueries.SELECT_COUNT_ZERO_BYTE_FILES, True, True)
      if self.analysisresults.zerobytecount > 0:
         self.analysisresults.zerobytelist = self.__querydb__(AnalysisQueries.SELECT_ZERO_BYTE_FILEPATHS, False, False, True)
      else:
         self.analysisresults.zerobytelist = None   
      return self.analysisresults.zerobytecount

   def listRoguePUIDs(self, puidlist):   
      query = AnalysisQueries()       
      searchlist = []            
      for puid in puidlist:
         result = self.__querydb__(query.count_id_instances(puid), True, True)   
         if result > 0:
            searchlist.append(puid)

      roguepuidpathlist = []
      for puid in searchlist:
         result = self.__querydb__(query.search_id_instance_filepaths(puid))        
         for r in result:
            roguepuidpathlist.append(r[0])
            
      self.analysisresults.roguepuidlisting = roguepuidpathlist      
      return len(self.analysisresults.roguepuidlisting)

   def calculatePercent(self, total, subset):
      if total > 0:
         percentage = (subset/total)*100
         return '%.1f' % round(percentage, 1)
        
   def msoftfnameanalysis(self):
      namelist = self.__querydb__(AnalysisQueries.SELECT_FILENAMES)
      dirlist = self.__querydb__(AnalysisQueries.SELECT_DIRNAMES)
      
      charcheck = MsoftFnameAnalysis.MsoftFnameAnalysis()
      
      namereport = []
      for d in namelist:
         namestring = d[0]
         checkedname = charcheck.completeFnameAnalysis(namestring).encode('utf-8')
         if checkedname != '':
            namereport.append(checkedname)

      #TODO: Handle recursive paths better to avoid duplication
      dirreport = []
      for d in dirlist:
         dirstring = d[0]
         checkedname = charcheck.completeFnameAnalysis(dirstring, True).encode('utf-8')
         if checkedname != '':
            dirreport.append(checkedname)

      self.analysisresults.badFileNames = namereport
      self.analysisresults.badDirNames = dirreport

   def multiplecount(self, nscount):
      query = AnalysisQueries()       
      return self.__querydb__(query.count_multiple_ids(self.analysisresults.namespacecount), True, True)         

   def handleIDBreakdown(self, query, tooltype):

      allids = self.__querydb__(query)
      
      method_list = []
      
      container_bin = []
      binary_bin = []
      text = []
      filename = []
      extension = []
      none = []
      
      #create a set to remove the fileids with duplicate methods
      for id in allids:
         file = id[0]
         method = id[1].lower().strip()
         method_list.append(str(file) + "," + method)
   
      for id in list(method_list):
         idlist = id.split(',', 1)
         type = idlist[1]
         idno = idlist[0]
         if type == 'container':
            if idno not in container_bin:             
               container_bin.append(idno)

      for id in list(method_list):
         idlist = id.split(',', 1)
         type = idlist[1]
         idno = idlist[0]
         if type == 'signature':
            if idno not in container_bin and idno not in binary_bin:             
               binary_bin.append(idno)
            
      for id in list(method_list):
         idlist = id.split(',', 1)
         type = idlist[1]
         idno = idlist[0]
         if type == 'text':
            if idno not in container_bin and idno not in binary_bin and idno not in text:
               text.append(idno)      

      for id in list(method_list):
         idlist = id.split(',', 1)
         type = idlist[1]
         idno = idlist[0]
         if type == 'filename':
            if idno not in container_bin and idno not in binary_bin and idno not in text and idno not in filename:
               filename.append(idno)      
   
      for id in list(method_list):
         idlist = id.split(',', 1)
         type = idlist[1]
         idno = idlist[0]
         if type == 'extension':
            if idno not in container_bin and idno not in binary_bin and idno not in text and idno not in filename and idno not in extension:
               extension.append(idno)       

      for id in list(method_list):
         idlist = id.split(',', 1)
         type = idlist[1]
         idno = idlist[0]
         if type == 'none':
            if idno not in container_bin and idno not in binary_bin and idno not in text and idno not in filename and idno not in extension and idno not in none:
               none.append(idno)      
   
      self.analysisresults.identifiedfilecount = len(container_bin) + len(binary_bin)
      self.analysisresults.unidentifiedfilecount = len(none)            
      self.analysisresults.extensionIDOnlyCount = len(extension)
      
      if tooltype != 'droid':
         self.analysisresults.textidfilecount = len(text) 
         self.analysisresults.filenameidfilecount = len(filename) 
      
      self.analysisresults.multipleidentificationcount = self.multiplecount(self.analysisresults.namespacecount)  

      #ID Method frequencylist can be created here also
      #e.g. [('None', 2269), ('Text', 149), ('Signature', 57), ('Filename', 52), ('Extension', 7), ('Container', 1)]
      #self.analysisresults.idmethodFrequency
      list1 = ('None', len(none))
      list2 = ('Container', len(container_bin))
      list3 = ('Signature', len(binary_bin))
      list4 = ('Extension', len(extension))

      list_of_lists = [list1, list2, list3, list4]
      if tooltype != 'droid':
         list5 = ('Filename', len(filename))
         list6 = ('Text', len(text))
         list_of_lists.append(list5)
         list_of_lists.append(list6)

      list_of_lists.sort(key=lambda tup: tup[1], reverse=True)
      self.analysisresults.idmethodFrequency = list_of_lists
      self.analysisresults.zeroidcount = len(none)

   def queryDB(self):
      self.analysisresults.tooltype = self.__querydb__(AnalysisQueries.SELECT_TOOL, True)[0]
      self.analysisresults.namespacecount = self.__querydb__(AnalysisQueries.SELECT_COUNT_NAMESPACES, True)[0]
            
      self.hashtype = self.__querydb__(AnalysisQueries.SELECT_HASH, True)[0]
      if self.hashtype == "None":
         sys.stderr.write(AnalysisQueries.ERROR_NOHASH + "\n")
         self.analysisresults.hashused = False
      else:
         self.analysisresults.hashused = True

      self.analysisresults.collectionsize = self.__querydb__(AnalysisQueries.SELECT_COLLECTION_SIZE, True, True)
      self.analysisresults.filecount = self.__querydb__(AnalysisQueries.SELECT_COUNT_FILES, True, True)
      self.analysisresults.containercount = self.__querydb__(AnalysisQueries.SELECT_COUNT_CONTAINERS, True, True)      
      self.analysisresults.filesincontainercount = self.__querydb__(AnalysisQueries.SELECT_COUNT_FILES_IN_CONTAINERS, True, True)
      self.analysisresults.directoryCount = self.__querydb__(AnalysisQueries.SELECT_COUNT_FOLDERS, True, True)

      #not necessarily used in the output
      self.analysisresults.uniqueFileNames = self.__querydb__(AnalysisQueries.SELECT_COUNT_UNIQUE_FILENAMES, True, True)
      
      self.analysisresults.uniqueDirectoryNames = (self.__querydb__(AnalysisQueries.SELECT_COUNT_UNIQUE_DIRNAMES, True, True) - self.NONROOTBASEDIR)
      
      
      #------------WHAT IS AND ISN'T IDENTIFIED SUMMARY------------#                  
      self.handleIDBreakdown(AnalysisQueries.SELECT_COUNT_ID_METHODS, self.analysisresults.tooltype)
      #------------WHAT IS AND ISN'T IDENTIFIED SUMMARY------------#    

      self.analysisresults.extmismatchCount = self.__querydb__(AnalysisQueries.SELECT_COUNT_EXT_MISMATCHES, True, True)
      self.analysisresults.distinctSignaturePuidcount = self.__querydb__(AnalysisQueries.SELECT_COUNT_FORMAT_COUNT, True, True) 

      if self.analysisresults.tooltype != 'droid':
         self.analysisresults.distinctOtherIdentifiers = self.__querydb__(AnalysisQueries.SELECT_COUNT_OTHER_FORMAT_COUNT, True, True)
         self.analysisresults.distinctTextIdentifiers = self.__querydb__(AnalysisQueries.SELECT_COUNT_TEXT_IDENTIFIERS, True, True)
         self.analysisresults.distinctFilenameIdentifiers = self.__querydb__(AnalysisQueries.SELECT_COUNT_FILENAME_IDENTIFIERS, True, True)
         
      
      self.analysisresults.distinctextensioncount = self.__querydb__(AnalysisQueries.SELECT_COUNT_EXTENSION_RANGE, True, True)

      self.analysisresults.mimetypeFrequency = self.__querydb__(AnalysisQueries.SELECT_MIME_RANGE)
      
      #NOTE: Must be calculated after we have total, and subset values
      self.analysisresults.identifiedPercentage = self.calculatePercent(self.analysisresults.filecount, self.analysisresults.identifiedfilecount)
      self.analysisresults.unidentifiedPercentage = self.calculatePercent(self.analysisresults.filecount, self.analysisresults.unidentifiedfilecount)

      '''
      self.analysisresults.sigIDPUIDList = self.__querydb__(AnalysisQueries.SELECT_DISTINCT_BINARY_MATCH_NAMES)
      self.analysisresults.dateFrequency = self.__querydb__(AnalysisQueries.SELECT_YEAR_FREQUENCY_COUNT)      
      self.analysisresults.sigIDPUIDFrequency = self.__querydb__(AnalysisQueries.SELECT_BINARY_MATCH_COUNT)
      

      
      #TODO: POTENTIALLY DELETE BELOW
      #TODO: POTENTIALLY DELETE BELOW
      #TODO: POTENTIALLY DELETE BELOW
      self.analysisresults.extensionOnlyIDList = self.__querydb__(AnalysisQueries.SELECT_PUIDS_EXTENSION_ONLY)
      #TODO: WE MIGHT NOT USE THIS
      #self.analysisresults.extensionOnlyIDfnameList = self.listExtensionIDOnly()
      self.analysisresults.extensionOnlyIDFrequency = self.__querydb__(AnalysisQueries.SELECT_EXT_ONLY_FREQUENCY)
      #"SELECT FILE_PATH FROM droid WHERE METHOD='no value' AND (TYPE='File' OR TYPE='Container')"
      self.analysisresults.filesWithNoIDList = self.__querydb__(AnalysisQueries.SELECT_ZERO_ID_FILES, False, False, True)
      #TODO: POTENTIALLY DELETE ABOVE
      #TODO: POTENTIALLY DELETE ABOVE
      #TODO: POTENTIALLY DELETE ABOVE

      #OKAY stat...
      self.analysisresults.uniqueExtensionsInCollectionList = self.__querydb__(AnalysisQueries.SELECT_ALL_UNIQUE_EXTENSIONS)
      self.analysisresults.frequencyOfAllExtensions = self.__querydb__(AnalysisQueries.SELECT_COUNT_EXTENSION_FREQUENCY)
      self.analysisresults.extmismatchList = self.__querydb__(AnalysisQueries.SELECT_EXTENSION_MISMATCHES) 
      
      
      self.analysisresults.multipleIDList = self.__querydb__(AnalysisQueries.SELECT_MULTIPLE_ID_PATHS, False, False, True)

      #Originally PARETO principle: 80% of the effects from from 20% of the causes
      self.analysisresults.topPUIDList = self.analysisresults.sigIDPUIDFrequency[0:5]
      self.analysisresults.topExtensionList = self.analysisresults.frequencyOfAllExtensions[0:5]
      
      #Additional useful queries...
      self.analysisresults.containertypeslist = self.__querydb__(AnalysisQueries.SELECT_CONTAINER_TYPES)
            
      #more complicated listings
      if self.analysisresults.hashused is True:
         self.listDuplicateFilesFromHASH()      #expensive duplicate checking [default: ON]      
         
      self.listzerobytefiles()
      self.msoftfnameanalysis()

      if self.roguepuids != False:
         self.listRoguePUIDs(self.roguepuids)

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
