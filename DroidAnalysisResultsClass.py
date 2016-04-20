# -*- coding: utf-8 -*-
import DroidAnalysisClass

class DROIDAnalysisResults:
   
   #version
   version = 0

   #filename
   filename = ''

   #hashused
   hashused = False

   # Counts
   collectionsize = 0
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
   zeroidcount = 0

   extmismatchCount = 0
   extmismatchList = 0
   
   unidentifiedPercentage = 0
   identifiedPercentage = 0
   
   sigIDPUIDList = None
   sigIDPUIDFrequency = None
   
   dateFrequency = None

   extensionOnlyIDList = None
   extensionOnlyIDFrequency = 0
   extensionOnlyIDfnameList = 0 
   
   #TODO: Turn lists into lists? Formatting at end..?
   uniqueExtensionsInCollectionList = None
   multipleIDList = None
   frequencyOfAllExtensions = None
   
   idmethodFrequency = None
   
   mimetypeFrequency = None
   
   filesWithNoIDList = None
   topPUIDList = None
   topExtensionList = None
   
   totalmd5duplicates = 0
   duplicatemd5listing = []
   duplicatemd5altlisting = []

   totaluniquefilenames = 0
   duplicatefnamelisting = [] 
   duplicatefnamealtlisting = []
   
   containertypeslist = None
   
   zerobytecount = 0
   zerobytelist = None
   
   multiplespacelist = ''
   badFileNames = None
   badDirNames = None
   
   duplicateHASHlisting = None
   totalHASHduplicates = None

   #rogues
   duplicatespathlist = []
      
   def __version__(self):
      analysis = DroidAnalysisClass.DROIDAnalysis()
      self.version = analysis.__version__()
      return self.version
