import sys
import DroidAnalysisClass
from internationalstrings import AnalysisStringsEN as IN_EN

class DROIDAnalysisTextOutput:

   textoutput = ''

   def __init__(self, analysisresults):
      self.STRINGS = IN_EN
      self.analysisresults = analysisresults

   def __output_list__(self, title, value):
      return title + ": " + str(value)
      
   def printFormattedText(self, string):
      self.textoutput = self.textoutput + string + "\n"
      return ""
      
   def printTextResults(self):
      self.generateTEXT()
      return self.textoutput
   
   def generateTEXT(self):
      self.printFormattedText(self.STRINGS.REPORT_TITLE)
      self.printFormattedText(self.STRINGS.REPORT_VERSION + ": " + self.analysisresults.__version__())
      self.printFormattedText(self.STRINGS.REPORT_FILE + ": " + self.analysisresults.filename)
   
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_TOTAL_FILES, self.analysisresults.filecount))
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_ARCHIVE_FILES, self.analysisresults.containercount))
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_INSIDE_ARCHIVES, self.analysisresults.filesincontainercount))
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_DIRECTORIES, self.analysisresults.directoryCount))
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_UNIQUE_DIRNAMES, self.analysisresults.uniqueDirectoryNames))
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_IDENTIFIED_FILES, self.analysisresults.identifiedfilecount))
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_MULTIPLE, self.analysisresults.multipleidentificationcount))
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_UNIDENTIFIED, self.analysisresults.unidentifiedfilecount))
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_EXTENSION_ID, self.analysisresults.extensionIDOnlyCount))
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_EXTENSION_MISMATCH, self.analysisresults.extmismatchCount))
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_ID_PUID_COUNT, self.analysisresults.distinctSignaturePuidcount))
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_UNIQUE_EXTENSIONS, self.analysisresults.distinctextensioncount))
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_ZERO_BYTE, self.analysisresults.zerobytecount))

      if self.analysisresults.hashused > 0:
         self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_IDENTICAL_FILES, self.analysisresults.totalHASHduplicates))

      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_MULTIPLE_SPACES, len(self.analysisresults.multiplespacelist)))
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_PERCENTAGE_IDENTIFIED, self.analysisresults.identifiedPercentage))
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_PERCENTAGE_UNIDENTIFIED, self.analysisresults.unidentifiedPercentage))

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

      if self.analysisresults.hashused > 0:
         print 
         print "Files with duplicate content (Total: " + str(self.analysisresults.totalHASHduplicates) + "):"
         for d in self.analysisresults.duplicateHASHlisting:	#TODO: consider count next to HASH val
            print d
            print
                  
      print
      print "Identifying troublesome filenames: "
      for badnames in self.analysisresults.badFilenames:
         # Already UTF-8 on way into here...
         sys.stdout.write(badnames)
