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
      
   def printFormattedText(self, string):
      self.textoutput = self.textoutput + string + "\n"
      return ""
      
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
      print self.analysisresults.sigIDPUIDList

      self.__output_list_title__(self.STRINGS.HEADING_FREQUENCY_PUIDS_IDENTIFIED)
      print self.analysisresults.sigIDPUIDFrequency

      self.__output_list_title__(self.STRINGS.HEADING_EXTENSION_ONLY)
      print self.analysisresults.extensionOnlyIDList
      
      self.printFormattedText(self.__output_list__(self.STRINGS.HEADING_DATE_RANGE, self.getDateList()))
      
      self.__output_list_title__(self.STRINGS.HEADING_ID_METHOD)
      print self.analysisresults.idmethodFrequency

      self.__output_list_title__(self.STRINGS.HEADING_FREQUENCY_EXTENSION_ONLY)
      print self.analysisresults.extensionOnlyIDFrequency

      self.__output_list_title__(self.STRINGS.HEADING_UNIQUE_EXTENSIONS)
      print self.analysisresults.uniqueExtensionsInCollectionList

      self.__output_list_title__(self.STRINGS.HEADING_LIST_MULTIPLE)
      print self.analysisresults.multipleIDList 

      self.__output_list_title__(self.STRINGS.HEADING_FREQUENCY_EXTENSIONS_ALL)
      print self.analysisresults.frequencyOfAllExtensions 

      self.__output_list_title__(self.STRINGS.HEADING_FREQUENCY_MIME)
      print self.analysisresults.mimetypeFrequency

      self.__output_list__(self.STRINGS.HEADING_LIST_ZERO_BYTES, self.analysisresults.zerobytecount)
      print self.analysisresults.zerobytelist

      self.__output_list__(self.STRINGS.HEADING_NO_ID, self.analysisresults.zeroidcount)
      print self.analysisresults.filesWithNoIDList
      
      self.__output_list_title__(self.STRINGS.TEXT_ONLY_FIVE_TOP_PUIDS)
      print self.analysisresults.topPUIDList
      
      self.__output_list_title__(self.STRINGS.TEXT_ONLY_FIVE_TOP_EXTENSIONS)
      print self.analysisresults.topExtensionList 	

      self.__output_list_title__(self.STRINGS.HEADING_ARCHIVE_FORMATS)
      print self.analysisresults.containertypeslist

      if self.analysisresults.hashused > 0:
         self.__output_list__(self.STRINGS.HEADING_IDENTICAL_CONTENT, self.analysisresults.totalHASHduplicates)
         for d in self.analysisresults.duplicateHASHlisting:	#TODO: consider count next to HASH val
            print d
            self.__printNewline__()
      
      if len(self.analysisresults.badFilenames) > 0:
         self.__output_list_title__(self.STRINGS.HEADING_TROUBLESOME_FILENAMES)
         for badnames in self.analysisresults.badFilenames:
            # Already UTF-8 on way into here...
            sys.stdout.write(badnames)
