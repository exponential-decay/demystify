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
   
   def __printNewline__(self):
      self.printFormattedText("\n")
      
   def __output_list_title__(self, title):
      self.__printNewline__()
      self.printFormattedText(title + ":")
      
   def printFormattedText(self, string, newline=True):
      lnend = ''
      if newline:
         lnend = "\n"
      self.textoutput = self.textoutput + str(string) + lnend
      
   def printTextResults(self):
      self.generateTEXT()
      return self.textoutput
      
   def getDateList(self):
      dates = ''
      for s in self.analysisresults.dateFrequency:
         s = s.split(',')
         dates = dates + s[0] + " (" + s[1].strip() + ")" + ", " 
      dates = dates.rstrip(", ")
      return dates
   
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


      #return the size of the collection
      size = self.analysisresults.collectionsize #easier to reference from a var
      self.printFormattedText(self.STRINGS.HEADING_SIZE + ": " + str(size) + " bytes | " + str(size/(1048576)) + " MiB/MB (Megabytes)") #MiB/MB = (2^1024)*2

      self.__output_list_title__(self.STRINGS.HEADING_IDENTIFIED)
      self.printFormattedText(self.analysisresults.sigIDPUIDList)

      self.__output_list_title__(self.STRINGS.HEADING_FREQUENCY_PUIDS_IDENTIFIED)
      self.printFormattedText(self.analysisresults.sigIDPUIDFrequency)

      if len(self.analysisresults.extensionOnlyIDList) > 0:
         self.__output_list_title__(self.STRINGS.HEADING_EXTENSION_ONLY)
         self.printFormattedText(self.analysisresults.extensionOnlyIDList)
      
      self.printFormattedText(self.__output_list__(self.STRINGS.HEADING_DATE_RANGE, self.getDateList()))
      
      self.__output_list_title__(self.STRINGS.HEADING_ID_METHOD)
      self.printFormattedText(self.analysisresults.idmethodFrequency)

      if len(self.analysisresults.extensionOnlyIDList) > 0:
         self.__output_list_title__(self.STRINGS.HEADING_FREQUENCY_EXTENSION_ONLY)
         self.printFormattedText(self.analysisresults.extensionOnlyIDFrequency)

      self.__output_list_title__(self.STRINGS.HEADING_UNIQUE_EXTENSIONS)
      self.printFormattedText(self.analysisresults.uniqueExtensionsInCollectionList)

      if len(self.analysisresults.multipleIDList) > 0:
         self.__output_list_title__(self.STRINGS.HEADING_LIST_MULTIPLE)
         self.printFormattedText(self.analysisresults.multipleIDList) 

      self.__output_list_title__(self.STRINGS.HEADING_FREQUENCY_EXTENSIONS_ALL)
      self.printFormattedText(self.analysisresults.frequencyOfAllExtensions) 

      self.__output_list_title__(self.STRINGS.HEADING_FREQUENCY_MIME)
      self.printFormattedText(self.analysisresults.mimetypeFrequency)

      if self.analysisresults.zerobytecount > 0:
         self.__output_list__(self.STRINGS.HEADING_LIST_ZERO_BYTES, self.analysisresults.zerobytecount)
         self.printFormattedText(self.analysisresults.zerobytelist)

      self.__output_list__(self.STRINGS.HEADING_NO_ID, self.analysisresults.zeroidcount)
      self.printFormattedText(self.analysisresults.filesWithNoIDList)
      
      self.__output_list_title__(self.STRINGS.TEXT_ONLY_FIVE_TOP_PUIDS)
      self.printFormattedText(self.analysisresults.topPUIDList)
      
      self.__output_list_title__(self.STRINGS.TEXT_ONLY_FIVE_TOP_EXTENSIONS)
      self.printFormattedText(self.analysisresults.topExtensionList) 	

      if len(self.analysisresults.containertypeslist) > 0:
         self.__output_list_title__(self.STRINGS.HEADING_ARCHIVE_FORMATS)
         self.printFormattedText(self.analysisresults.containertypeslist)

      if self.analysisresults.hashused > 0:
         if self.analysisresults.totalHASHduplicates > 0:
            self.__output_list__(self.STRINGS.HEADING_IDENTICAL_CONTENT, self.analysisresults.totalHASHduplicates)
            for dupes in self.analysisresults.duplicateHASHlisting:	#TODO: consider count next to HASH val
               self.printFormattedText("Checksum: " + str(dupes['checksum']))
               self.printFormattedText("Count: " + str(dupes['count']))
               self.printFormattedText("Example: " + str(dupes['examples'][0]) + "\n")
      
      if len(self.analysisresults.badFilenames) > 0:
         self.__output_list_title__(self.STRINGS.HEADING_TROUBLESOME_FILENAMES)
         for badnames in self.analysisresults.badFilenames:
            # Already UTF-8 on way into here...
            self.printFormattedText(badnames, False)




