# -*- coding: utf-8 -*-
import DroidAnalysisClass

class DROIDAnalysisResults:
   
   #version
   version = 0

   #filename
   filename = ''

   #hashused
   hashused = 0

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
   
   sigIDPUIDList = 0
   sigIDPUIDFrequency = 0
   
   dateFrequency = 0

   extensionOnlyIDList = 0
   extensionOnlyIDFrequency = 0
   extensionOnlyIDfnameList = 0 
   
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
   duplicatemd5altlisting = []

   totaluniquefilenames = 0
   duplicatefnamelisting = [] 
   duplicatefnamealtlisting = []
   
   containertypeslist = 0
   
   zerobytecount = 0
   zerobytelist = 0
   
   multiplespacelist = ''
   badFilenames = ''
      
   def __version__(self):
      analysis = DroidAnalysisClass.DROIDAnalysis()
      self.version = analysis.__version__()
      return self.version
