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
from collections import Counter

class DROIDAnalysis:

   #we need this value because we extract basedirs for all folders, including
   #the root directory of the extract, creating one additional entry
   #TODO: consider handling better...
   NONROOTBASEDIR = 1

   #somenamespaceconsts
   NS_CONST_TITLE = 'namespace title'
   NS_CONST_DETAILS = 'namespace details'
   NS_CONST_TEXT_COUNT = 'text method count'
   NS_CONST_FILENAME_COUNT = 'filename method count'
   NS_CONST_EXTENSION_COUNT = 'extension method count'
   NS_CONST_BINARY_COUNT = 'binary method count'
   NS_CONST_MULTIPLE_IDS = 'multiple ids'

   #variables we need internally:
   extensionIDonly = None
   noids = None
   textIDs = None
   filenameIDs = None

   namespacedata = None

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
      self.cursor.execute(query.replace('  ', ''))
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
      
      binaryidrows = []    #and containers
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
               binaryidrows.append((idno, idrow))

      for id in list(method_list):
         type, idno, idrow = self.__getsplit__(id)
         if type == 'signature':
            if idno not in container_bin and idno not in binary_bin:             
               binary_bin.append(idno)
               binaryidrows.append((idno, idrow))
            
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
      
      self.analysisresults.unidentifiedfilecount = self.analysisresults.filecount - self.analysisresults.identifiedfilecount           
      self.analysisresults.extensionIDOnlyCount = len(extension)
      
      self.extensionIDonly = extension
      self.noids = none

      self.binaryIDs = binaryidrows
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

   def getMethodIDResults(self, methodids, version=False):
      #TODO: Fine line between formatting, and not formatting in this function
      countlist = []
      text = ''
      methodresults = self.__querydb__(self.query.query_from_idrows(methodids))
      for id in methodresults:
         name = id[2]
         if name == '':
            name = ", "
         else:
            name = ", " + name + ", "
         basis = id[3]
         if basis is not None:
            basis = "[" + basis + "]"
         else:
            basis = ''
         #('pronom', 'x-fmt/111', 'Plain Text File', 'text match ASCII')
         idval = "ns:" + id[0] + " " + id[1] + name + basis
         if version == True:
            #we're creating a less detailed statistic for summary purposes
            idval = "ns:" + id[0] + " " + id[1] + name + id[4]
         countlist.append(idval)      
      #counter returns dict
      templist = Counter(countlist)            
      countlist = []
      for k,v in templist.iteritems():
         countlist.append((k,v))      
      return sorted(countlist)

   def __analysebasis__(self):
      basislist_bof = []
      basislist_eof = []
      basis = self.__querydb__(AnalysisQueries.SELECT_BYTE_MATCH_BASIS) 
      for idrow in basis:
         val = idrow[0].split(';')
         filesize = int(idrow[3])
         for x in val:
            if 'byte match' in x:
               length = 0
               value = x.strip().replace('byte match at ', '')
               offset = value.split(',',1)[0]
               if '[[[' in offset:
                  #offset might look like: byte match at [[[0 4]] [[30 19]]] (signature 1/2)
                  #highest match is at 30 bytes, for 19 bytes...
                  splitvals = offset.replace('[[[','').replace('[[','')
                  splitvals = splitvals.replace(']]]','').replace(']]','')
                  tmp = splitvals.split(' ',4)
                  if len(tmp) > 3:
                     offset = int(tmp[2])
                     length = int(tmp[3])
               else:
                  offset = int(offset)
                  length = int(value.replace(',','').split(' ',2)[1])
               offlen = offset+length
               basislist_bof.append((offlen, idrow))
               basislist_eof.append(((filesize-offlen), idrow))

      basislist_bof.sort(key=lambda tup: tup[0], reverse=True)
      basislist_eof.sort(key=lambda tup: tup[0], reverse=False)
      
      top_bof = basislist_bof[0]
      idval_bof = top_bof[1][1]
      fname_bof = top_bof[1][2]
      matchdetails_bof = top_bof[1][0]
      size_bof = str(top_bof[1][3])

      top_eof = basislist_eof[0]           
      idval_eof = top_eof[1][1]
      fname_eof = top_eof[1][2]
      matchdetails_eof = top_eof[1][0]  
      size_eof = str(top_eof[1][3])
    
      distance_bof = "(" + str(top_bof[0]) + ") " + idval_bof + ", " + matchdetails_bof + " e.g. " + fname_bof + " " + size_bof + " bytes"
      distance_eof = "(" + str(top_eof[0]) + ") " + idval_eof + ", " + matchdetails_eof + " e.g. " + fname_eof + " " + size_eof + " bytes"
      return distance_bof, distance_eof

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
         
      self.analysisresults.dateFrequency = self.__querydb__(AnalysisQueries.SELECT_YEAR_FREQUENCY_COUNT)      
      self.analysisresults.signatureidentifiedfrequency = self.__querydb__(AnalysisQueries.SELECT_BINARY_MATCH_COUNT)      
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

      #MORE WORK NEEDED ON ROGUES NOW... ACCURACY IS PARAMOUNT
      if len(self.extensionIDonly) > 0:
         extonly = self.query.query_from_ids(self.extensionIDonly)
         extrogues = self.__querydb__(extonly)
      if len(self.noids) > 0:    #NOT THE SAME AS COMPLETELY UNIDENTIFIED
         none = self.query.query_from_ids(self.noids)
         nonerogues = self.__querydb__(none)

      self.analysisresults.extmismatchList = self.__querydb__(AnalysisQueries.SELECT_EXTENSION_MISMATCHES) 

      if self.analysisresults.multipleidentificationcount > 0:
         self.analysisresults.multipleIDList = self.multipleIDList(self.analysisresults.namespacecount)

      #create a statistic for aggregated binary identification
      if self.binaryIDs is not None and len(self.binaryIDs) > 0:
         self.analysisresults.signatureidentifiers = self.getMethodIDResults(self.binaryIDs, True)

      #New functions thanks to Siegfried
      if self.binaryIDs is not None and len(self.binaryIDs) > 0:
         self.analysisresults.binaryidentifiers = self.getMethodIDResults(self.binaryIDs)
      if self.textIDs is not None and len(self.textIDs) > 0:
         self.analysisresults.textidentifiers = self.getMethodIDResults(self.textIDs)
      if self.filenameIDs is not None and len(self.filenameIDs) > 0:
         self.analysisresults.filenameidentifiers = self.getMethodIDResults(self.filenameIDs)
      if self.analysisresults.tooltype != 'droid':
         self.analysisresults.bof_distance, self.analysisresults.eof_distance = self.__analysebasis__() 
      #we need namespace data - ann NS queries can be generic
      #ns count earlier on in this function can be left as-is
      if self.analysisresults.namespacecount is not None and self.analysisresults.namespacecount > 0:
         self.namespacedata = self.__querydb__(AnalysisQueries.SELECT_NS_DATA)
         nsdatalist = []
         for ns in self.namespacedata:
            nsdict = {}
            nsid = ns[0]
            nsdict[self.NS_CONST_TITLE] = ns[1]
            nsdict[self.NS_CONST_DETAILS] = ns[2]
            nsdict[self.NS_CONST_BINARY_COUNT] = self.__querydb__(self.query.get_ns_methods(nsid), True, True)
            nsdict[self.NS_CONST_TEXT_COUNT] = self.__querydb__(self.query.get_ns_methods(nsid, False, 'Text'), True, True)
            nsdict[self.NS_CONST_FILENAME_COUNT] = self.__querydb__(self.query.get_ns_methods(nsid, False, 'Filename'), True, True)
            nsdict[self.NS_CONST_EXTENSION_COUNT] = self.__querydb__(self.query.get_ns_methods(nsid, False, 'Extension'), True, True)
            nsdict[self.NS_CONST_MULTIPLE_IDS] = self.__querydb__(self.query.get_ns_multiple_ids(nsid, self.analysisresults.namespacecount), True, True)
            nsdatalist.append(nsdict)
         self.analysisresults.nsdatalist = nsdatalist
         
         #get nsgap count
         idslist = []
         for ns in self.namespacedata:
            nsid = ns[0]
            idslist = idslist + self.__querydb__(self.query.get_ns_gap_count_lists(nsid), False, False, True)

         counted = dict(Counter(idslist))         
         noids = []
         for x in counted:
            if counted[x] == self.analysisresults.namespacecount:
               noids.append(x)
         self.analysisresults.identificationgaps = len(noids)
         
      return self.analysisresults
      
   def openDROIDDB(self, dbfilename):
      self.analysisresults.filename = dbfilename.rstrip('.db')
   
      conn = sqlite3.connect(dbfilename)
      conn.text_factory = str		#encoded as ascii, not unicode / return ascii
      
      self.cursor = conn.cursor()
      analysisresults = self.queryDB()		# primary db query functions
      
      conn.close()

      return self.analysisresults
