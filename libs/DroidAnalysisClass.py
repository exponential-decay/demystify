# -*- coding: utf-8 -*-

from __future__ import division
import argparse
import sys
import sqlite3
import csv
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

   #variables we need internally:
   extensionIDonly = None
   noids = None
   textIDs = None
   filenameIDs = None

   def __init__(self, config=False):
      self.query = AnalysisQueries()
      self.config = self.__readconfig__(config)       
      self.analysisresults = DroidAnalysisResultsClass.DROIDAnalysisResults()

   def __version__(self):
      self.analysisresults.__version__ = '0.4.0' #need something reasonable here...
      return self.analysisresults.__version__

   def __readconfig__(self, config):
      configout = False
      
      self.blacklistpuids = False
      self.blacklistzeros = False
      
      #self.roguesduplicatenames = True // to implement

      self.roguesduplicatechecksums = True
      self.rogueids = False
      
      if config != False:
         if config.has_section('rogues'):
            if config.has_option('rogues', 'duplicatechecksums'):
               self.roguesduplicatechecksums = config.get('rogues', 'duplicatechecksums').lower()
            if config.has_option('rogues', 'ids'):
               self.rogueids = config.get('rogues', 'ids').split(',')  

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
    
   def listDuplicateFilesFromHASH(self):		
      result = self.__querydb__(AnalysisQueries.SELECT_COUNT_DUPLICATE_CHECKSUMS)

      duplicate_sum = {}
      duplicatelist = []
      
      self.analysisresults.totalHASHduplicates = 0
      for r in result:
         self.analysisresults.totalHASHduplicates = self.analysisresults.totalHASHduplicates + int(r[1])
        
      #result list([HASH, COUNT])           
      for r in result:               
         example = self.__querydb__(self.query.list_duplicate_paths(r[0]))
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

   def listRogueIDs(self, idlist):        
      searchlist = []            
      for id in idlist:
         result = self.__querydb__(self.query.count_id_instances(id), True, True)   
         if result > 0:
            searchlist.append(id)

      rogueidpathlist = []
      for id in searchlist:
         result = self.__querydb__(self.query.search_id_instance_filepaths(id))        
         for r in result:
            rogueidpathlist.append(r[0])
            
      self.analysisresults.roguepuidlisting = rogueidpathlist      
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
      return self.__querydb__(self.query.count_multiple_ids(nscount), True, True)         

   def multipleIDList(self, nscount):       
      return self.__querydb__(self.query.count_multiple_ids(nscount, True), False, False, True) 

   def __getsplit__(self, vals):
      idlist = vals.split(',', 2)
      if len(idlist) is 3:         
         type = idlist[1]
         idno = idlist[0]
         idrow = idlist[2]
         return type, idno, idrow

   def handleIDBreakdown(self, query, tooltype):

      allids = self.__querydb__(query)      
      method_list = []
      
      container_bin = []
      binary_bin = []
      text = []
      filename = []
      extension = []
      none = []
      
      textidrows = []
      filenameidrows = []
      
      #create a set to remove the fileids with duplicate methods
      for id in allids:
         file = id[0]
         method = id[2].lower().strip()
         idrow = id[1]
         method_list.append(str(file) + "," + method + "," + str(idrow))
   
      for id in list(method_list):
         type, idno, idrow = self.__getsplit__(id)
         if type == 'container':
            if idno not in container_bin:             
               container_bin.append(idno)

      for id in list(method_list):
         type, idno, idrow = self.__getsplit__(id)
         if type == 'signature':
            if idno not in container_bin and idno not in binary_bin:             
               binary_bin.append(idno)
            
      for id in list(method_list):
         type, idno, idrow = self.__getsplit__(id)
         if type == 'text':
            if idno not in container_bin and idno not in binary_bin and idno not in text:
               text.append(idno)   
               textidrows.append((idno, idrow))

      for id in list(method_list):
         type, idno, idrow = self.__getsplit__(id)
         if type == 'filename':
            if idno not in container_bin and idno not in binary_bin and idno not in text and idno not in filename:
               filename.append(idno)
               filenameidrows.append((idno, idrow))
   
      for id in list(method_list):
         type, idno, idrow = self.__getsplit__(id)
         if type == 'extension':
            if idno not in container_bin and idno not in binary_bin and idno not in text and idno not in filename and idno not in extension:
               extension.append(idno)       

      for id in list(method_list):
         type, idno, idrow = self.__getsplit__(id)
         if type == 'none':
            if idno not in container_bin and idno not in binary_bin and idno not in text and idno not in filename and idno not in extension and idno not in none:
               none.append(idno)      
   
      self.analysisresults.identifiedfilecount = len(container_bin) + len(binary_bin)
      self.analysisresults.unidentifiedfilecount = len(none)            
      self.analysisresults.extensionIDOnlyCount = len(extension)
      
      self.extensionIDonly = extension
      self.noids = none

      self.textIDs = textidrows
      self.filenameIDs = filenameidrows

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
      
      self.analysisresults.sigIDPUIDList = self.__querydb__(AnalysisQueries.SELECT_DISTINCT_BINARY_MATCH_NAMES)      
      self.analysisresults.dateFrequency = self.__querydb__(AnalysisQueries.SELECT_YEAR_FREQUENCY_COUNT)      
      self.analysisresults.sigIDPUIDFrequency = self.__querydb__(AnalysisQueries.SELECT_BINARY_MATCH_COUNT)      
      self.analysisresults.extensionOnlyIDList = self.__querydb__(AnalysisQueries.SELECT_PUIDS_EXTENSION_ONLY)
      
      #most complicated way to retrieve extension only PUIDs
      if len(self.extensionIDonly) > 0:
         extid = self.query.query_from_ids(self.extensionIDonly, 'Extension')
         test = self.__querydb__(extid)
         combined_list = []   #namespace + id
         from collections import Counter
         for entry in test:
            entry = 'ns:' + ' '.join(entry)
            combined_list.append(entry) 
         sorted_list = Counter(elem for elem in combined_list).most_common()
         self.analysisresults.extensionOnlyIDFrequency = sorted_list
      
      #OKAY stat...
      self.analysisresults.uniqueExtensionsInCollectionList = self.__querydb__(AnalysisQueries.SELECT_ALL_UNIQUE_EXTENSIONS)
      self.analysisresults.frequencyOfAllExtensions = self.__querydb__(AnalysisQueries.SELECT_COUNT_EXTENSION_FREQUENCY)
                  
      #Additional useful queries...
      self.analysisresults.containertypeslist = self.__querydb__(AnalysisQueries.SELECT_CONTAINER_TYPES)
            
      #more complicated listings
      if self.analysisresults.hashused is True:
         self.listDuplicateFilesFromHASH()      #expensive duplicate checking [default: ON]      
      
      #handle output of zero-byte files and filename analysis  
      self.listzerobytefiles()      
      self.msoftfnameanalysis()
      
      #ROGUE QUERIES (relies on returning filepaths)
      #NB.Need a query where there is no PUID e.g. Rosetta validation procedure
      if self.rogueids != False:
         self.listRogueIDs(self.rogueids)

      if len(self.extensionIDonly) > 0:
         extonly = self.query.query_from_ids(self.extensionIDonly)
         extrogues = self.__querydb__(extonly)
      if len(self.noids) > 0:
         none = self.query.query_from_ids(self.noids)
         nonerogues = self.__querydb__(none)

      self.analysisresults.extmismatchList = self.__querydb__(AnalysisQueries.SELECT_EXTENSION_MISMATCHES) 

      if self.analysisresults.multipleidentificationcount > 0:
         self.analysisresults.multipleIDList = self.multipleIDList(self.analysisresults.namespacecount)

      #New functions thanks to Siegfried
      '''if self.textIDs is not None and len(self.textIDs) > 0:
         textids = self.query.query_from_ids(self.textIDs, 'Text')
         print self.__querydb__(textids)'''

      '''if self.filenameIDs is not None and len(self.filenameIDs) > 0:
         filenameids = self.query.query_from_ids(self.filenameIDs, 'Filename')
         print self.__querydb__(filenameids)'''

      #print self.textIDs
      #print self.filenameIDs

      return self.analysisresults
      
   def openDROIDDB(self, dbfilename):
      self.analysisresults.filename = dbfilename.rstrip('.db')
   
      conn = sqlite3.connect(dbfilename)
      conn.text_factory = str		#encoded as ascii, not unicode / return ascii
      
      self.cursor = conn.cursor()
      analysisresults = self.queryDB()		# primary db query functions
      
      conn.close()

      return self.analysisresults
