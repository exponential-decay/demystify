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
   
   def __itemlist__(self, list):
      output = ''
      for item in list:
         output = output + item + "\n"
      return output.strip("\n")
         
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

   def __frequencyoutput__(self, list):
      val = ''
      for item in list:
         val = val + str(item[0]) + " (" + str(item[1]) + "), "
      return val.strip(", ")
   
   def getDateList(self):
      return self.__frequencyoutput__(self.analysisresults.dateFrequency)
   
   def __outputdupes__(self, list):
      output = ''
      for dupes in self.analysisresults.duplicateHASHlisting:	#TODO: consider count next to HASH val
         output = output + "Checksum: " + str(dupes['checksum']) + "\n"
         output = output + "Count: " + str(dupes['count']) + "\n"
         output = output + "Example: " + str(dupes['examples'][0]) + "\n\n"
         
      return output.strip("\n")
      
   def generateTEXT(self):
      self.printFormattedText(self.STRINGS.REPORT_TITLE)
      self.printFormattedText(self.STRINGS.REPORT_VERSION + ": " + self.analysisresults.__version__())
      self.printFormattedText(self.STRINGS.REPORT_FILE + ": " + self.analysisresults.filename)
      
      self.printFormattedText("")
      
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
      for item in self.analysisresults.sigIDPUIDList:
         output = ""
         if item[2] != 'no value':
            output = item[0] + ", " + item[1] + " " + item[2]
         else:
            output = item[0] + ", " + item[1]            
         self.printFormattedText(output)

      self.__output_list_title__(self.STRINGS.HEADING_FREQUENCY_PUIDS_IDENTIFIED)
      self.printFormattedText(self.__frequencyoutput__(self.analysisresults.sigIDPUIDFrequency))

      if len(self.analysisresults.extensionOnlyIDList) > 0:
         self.__output_list_title__(self.STRINGS.HEADING_EXTENSION_ONLY)
         for item in self.analysisresults.extensionOnlyIDList:
            output = item[0] + ", " + item[1]
            self.printFormattedText(output)
      
      self.__output_list_title__(self.STRINGS.HEADING_DATE_RANGE)
      self.printFormattedText(self.getDateList())
      
      self.__output_list_title__(self.STRINGS.HEADING_ID_METHOD)
      self.printFormattedText(self.__frequencyoutput__(self.analysisresults.idmethodFrequency))

      if len(self.analysisresults.extensionOnlyIDList) > 0:
         self.__output_list_title__(self.STRINGS.HEADING_FREQUENCY_EXTENSION_ONLY)
         self.printFormattedText(self.__frequencyoutput__(self.analysisresults.extensionOnlyIDFrequency))

      self.__output_list_title__(self.STRINGS.HEADING_UNIQUE_EXTENSIONS)
      output = ''
      for item in self.analysisresults.uniqueExtensionsInCollectionList:
         output = output + item[0] + ", " 
      self.printFormattedText(output.strip(", "))

      if len(self.analysisresults.multipleIDList) > 0:
         self.__output_list_title__(self.STRINGS.HEADING_LIST_MULTIPLE)
         self.printFormattedText(self.__itemlist__(self.analysisresults.multipleIDList))

      self.__output_list_title__(self.STRINGS.HEADING_FREQUENCY_EXTENSIONS_ALL)
      self.printFormattedText(self.__frequencyoutput__(self.analysisresults.frequencyOfAllExtensions)) 

      self.__output_list_title__(self.STRINGS.HEADING_FREQUENCY_MIME)
      self.printFormattedText(self.__frequencyoutput__(self.analysisresults.mimetypeFrequency))

      self.printFormattedText("\n")
      if self.analysisresults.zerobytecount > 0:
         self.printFormattedText(self.__output_list__(self.STRINGS.HEADING_LIST_ZERO_BYTES, self.analysisresults.zerobytecount))
         self.printFormattedText(self.__itemlist__(self.analysisresults.zerobytelist))

      self.printFormattedText("\n")

      if len(self.analysisresults.filesWithNoIDList) > 0:
         self.printFormattedText(self.__output_list__(self.STRINGS.HEADING_NO_ID, self.analysisresults.zeroidcount))
         self.printFormattedText(self.__itemlist__(self.analysisresults.filesWithNoIDList))
      
      self.__output_list_title__(self.STRINGS.TEXT_ONLY_FIVE_TOP_PUIDS)
      self.printFormattedText(self.__frequencyoutput__(self.analysisresults.topPUIDList))
      
      self.__output_list_title__(self.STRINGS.TEXT_ONLY_FIVE_TOP_EXTENSIONS)
      self.printFormattedText(self.__frequencyoutput__(self.analysisresults.topExtensionList))

      if len(self.analysisresults.containertypeslist) > 0:
         self.__output_list_title__(self.STRINGS.HEADING_ARCHIVE_FORMATS)
         output = ""
         for archive in self.analysisresults.containertypeslist:
            output = output + archive[0] + ", " 
         self.printFormattedText(output.strip(", ") + "\n\n")

      if self.analysisresults.hashused > 0:
         if self.analysisresults.totalHASHduplicates > 0:
            self.__output_list__(self.STRINGS.HEADING_IDENTICAL_CONTENT, self.analysisresults.totalHASHduplicates)
            self.printFormattedText(self.__outputdupes__(self.analysisresults.duplicateHASHlisting))
                  
      if len(self.analysisresults.badFilenames) > 0:
         self.__output_list_title__(self.STRINGS.HEADING_TROUBLESOME_FILENAMES)
         for badnames in self.analysisresults.badFilenames:
            # Already UTF-8 on way into here...
            self.printFormattedText(badnames, False)




