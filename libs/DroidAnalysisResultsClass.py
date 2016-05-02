# -*- coding: utf-8 -*-
import DroidAnalysisClass

class DROIDAnalysisResults:
   
   #version
   version = 0

   #filename
   filename = ''

   #hashused
   hashused = False

   #tooltype
   tooltype = None

   #namespace count
   namespacecount = None

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

   #SF ONLY
   textidfilecount = 0
   filenameidfilecount = 0
   distinctOtherIdentifiers = 0
   distinctTextIdentifiers = 0
   distinctFilenameIdentifiers = 0
   textidentifiers = None
   filenameidentifiers = None
   #SF ONLY

   extmismatchCount = 0
   extmismatchList = 0
   
   unidentifiedPercentage = 0
   identifiedPercentage = 0
   
   signatureidentifiers = None
   sigIDPUIDFrequency = None
   
   dateFrequency = None

   extensionOnlyIDFrequency = 0
   extensionOnlyIDfnameList = 0 
   
   #TODO: Turn lists into lists? Formatting at end..?
   uniqueExtensionsInCollectionList = None
   multipleIDList = None
   frequencyOfAllExtensions = None
   
   idmethodFrequency = None
   
   mimetypeFrequency = None
   
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
