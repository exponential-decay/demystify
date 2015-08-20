import sys
import DroidAnalysisClass

class DROIDAnalysisTextOutput:

   def __init__(self, analysisresults):
      self.analysisresults = analysisresults
      
   def printTextResults(self):
      print "Analysis version: " + self.analysisresults.__version__() + '\n'
   
      print "Total files: " + str(self.analysisresults.filecount)
      print "Total container objects: " + str(self.analysisresults.containercount)
      print "Total files in containers: " + str(self.analysisresults.filesincontainercount) 
      print "Total directories: " + str(self.analysisresults.directoryCount)
      print "Total unique directory names: " + str(self.analysisresults.uniqueDirectoryNames)
      print "Total identified files (signature and container): " + str(self.analysisresults.identifiedfilecount)
      print "Total multiple identifications (signature and container): " + str(self.analysisresults.multipleidentificationcount)
      print "Total unidentified files (extension and blank): " + str(self.analysisresults.unidentifiedfilecount)
      print "Total extension ID only count: " + str(self.analysisresults.extensionIDOnlyCount)
      print "Total extension mismatches: " + str(self.analysisresults.extmismatchCount)		#TODO: List, but could be long
      print "Total signature IDd PUID count: " + str(self.analysisresults.distinctSignaturePuidcount)
      print "Total distinct extensions across collection: " + str(self.analysisresults.distinctextensioncount)
      print "Total zero-byte files in collection: " + str(self.analysisresults.zerobytecount)
      print "Total files with duplicate content (MD5 value): " + str(self.analysisresults.totalmd5duplicates)
      print "Total files with multiple contiguous space characters: " + str(len(self.analysisresults.multiplespacelist))
      print "Percentage of collection identified: " + str(self.analysisresults.identifiedPercentage)
      print "Percentage of collection unidentified: " + str(self.analysisresults.unidentifiedPercentage)

      print
      print "Signature identified PUIDs in collection (signature and container):"
      print self.analysisresults.sigIDPUIDList

      print
      print "Frequency of signature identified PUIDs:"
      print self.analysisresults.sigIDPUIDFrequency

      print
      print "Extension only identification in collection:"
      print self.analysisresults.extensionOnlyIDList

      print 
      print "ID Method Frequency: "
      print self.analysisresults.idmethodFrequency

      print 
      print "Frequency of extension only identification in collection: "
      print self.analysisresults.extensionOnlyIDFrequency

      print
      print "Unique extensions identified across all objects (ID & non-ID):"
      print self.analysisresults.uniqueExtensionsInCollectionList

      print
      print "List of files with multiple identifications: "
      print self.analysisresults.multipleIDList 

      print
      print "Frequency of all extensions:"
      print self.analysisresults.frequencyOfAllExtensions 

      print
      print "MIMEType (Internet Media Type) Frequency: "
      print self.analysisresults.mimetypeFrequency

      print
      print "Zero byte objects in collection: " + str(self.analysisresults.zerobytecount)
      print self.analysisresults.zerobytelist

      print
      print "Files with no identification: " + str(self.analysisresults.zeroidcount)
      print self.analysisresults.filesWithNoIDList

      print
      print "Top signature and container identified PUIDs: "
      print self.analysisresults.topPUIDList
      
      print
      print "Top extensions across collection: "		
      print self.analysisresults.topExtensionList 	

      print
      print "Container types in collection: "
      print self.analysisresults.containertypeslist

      print 
      print "Files with duplicate content (Total: " + str(self.analysisresults.totalmd5duplicates) + "):"
      for d in self.analysisresults.duplicatemd5listing:	#TODO: consider count next to MD5 val
         print d
         print
                  
      print
      print "Identifying troublesome filenames: "
      for badnames in self.analysisresults.badFilenames:
         # Already UTF-8 on way into here...
         sys.stdout.write(badnames)
      
      print
      print "Files with multiple contiguous spaces (Total: " + str(len(self.analysisresults.multiplespacelist)) + ")" 
      for f in self.analysisresults.multiplespacelist:
         print "original:   " + f[1] 
         print "spaces (%): " + f[1].replace(' ', '%')
         print "location:   " + "".join(f)
         print
