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

   #namespace argument is used for anything requiring the output of a namespace too, e.g. IDS
   def __frequencyoutput__(self, itemlist, zeros=False, namespace=False):         
      val = ''
      ns = None
      if type(itemlist) is not list:
         sys.stderr.write("LOG: Not sending a list to a function wanting a list." + "\n")
      else:
         for item in itemlist:
            if namespace == True: 
               if ns is None:
                  ns = str(item[0])
               else:
                  if ns != str(item[0]):
                     val = val.strip(', ') + "\n\n"
                     ns = str(item[0])
               val = val + 'ns:' + str(ns) + " "
               item = (item[1], item[2])
            if zeros == True:
               val = val + str(item[0]) + ", "
            else:
               val = val + str(item[0]) + " (" + str(item[1]) + "), "
         val = val.strip(", ")
         
      return val
   
   def getDateList(self):
      if self.analysisresults.dateFrequency is not None:
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
      self.printFormattedText(self.STRINGS.REPORT_TOOL + ": " + self.analysisresults.tooltype)
      self.printFormattedText("")
      self.printFormattedText(self.STRINGS.NAMESPACES + ": " + str(self.analysisresults.namespacecount))
      
      self.printFormattedText("")
      
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_TOTAL_FILES, self.analysisresults.filecount))
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_ARCHIVE_FILES, self.analysisresults.containercount))
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_INSIDE_ARCHIVES, self.analysisresults.filesincontainercount))
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_DIRECTORIES, self.analysisresults.directoryCount))
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_UNIQUE_DIRNAMES, self.analysisresults.uniqueDirectoryNames))
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_IDENTIFIED_FILES, self.analysisresults.identifiedfilecount))
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_MULTIPLE, self.analysisresults.multipleidentificationcount))
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_UNIDENTIFIED, self.analysisresults.unidentifiedfilecount))
      
      if self.analysisresults.tooltype != 'droid':
         self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_TEXT_ID, self.analysisresults.textidfilecount))
         self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_FILENAME_ID, self.analysisresults.filenameidfilecount))
            
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_EXTENSION_ID, self.analysisresults.extensionIDOnlyCount))
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_EXTENSION_MISMATCH, self.analysisresults.extmismatchCount))
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_ID_PUID_COUNT, self.analysisresults.distinctSignaturePuidcount))
      
      if self.analysisresults.tooltype != 'droid':
         self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_OTHER_ID_COUNT, self.analysisresults.distinctOtherIdentifiers))
         self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_TEXT_ID_COUNT, self.analysisresults.distinctTextIdentifiers))
         self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_FILENAME_ID_COUNT, self.analysisresults.distinctFilenameIdentifiers))      
      
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_UNIQUE_EXTENSIONS, self.analysisresults.distinctextensioncount))
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_ZERO_BYTE, self.analysisresults.zerobytecount))

      if self.analysisresults.hashused > 0:
         self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_IDENTICAL_FILES, self.analysisresults.totalHASHduplicates))

      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_MULTIPLE_SPACES, len(self.analysisresults.multiplespacelist)))
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_PERCENTAGE_IDENTIFIED, self.analysisresults.identifiedPercentage))
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_PERCENTAGE_UNIDENTIFIED, self.analysisresults.unidentifiedPercentage))


      #return the size of the collection
      size = self.analysisresults.collectionsize #easier to reference from a var
      self.printFormattedText(self.STRINGS.HEADING_SIZE + ": " + str(int(size)) + " bytes | " + str(int(size/(1048576))) + " MiB/MB (Megabytes)") #MiB/MB = (2^1024)*2

      if self.analysisresults.signatureidentifiers is not None:
         #[0]DISTINCT IDDATA.ID, [1]NSDATA.NS_NAME, [2]IDDATA.FORMAT_NAME, [3]IDDATA.FORMAT_VERSION
         self.__output_list_title__(self.STRINGS.HEADING_IDENTIFIED)
         for item in self.analysisresults.signatureidentifiers:
            output = ""
            if item[3] != 'no value':
               output = 'ns:' + item[1] + ' ' + item[0] + ", " + item[2] + " " + item[3]
            else:
               output = 'ns:' + item[1] + ' ' + item[0] + ", " + item[2]            
            self.printFormattedText(output.rstrip(', '))

      if self.analysisresults.textidentifiers is not None:
         self.__output_list_title__(self.STRINGS.HEADING_TEXT_ID)
         for item in self.analysisresults.textidentifiers:
            self.printFormattedText(item)
      if self.analysisresults.filenameidentifiers is not None:
         self.__output_list_title__(self.STRINGS.HEADING_FILENAME_ID)
         for item in self.analysisresults.filenameidentifiers:
            self.printFormattedText(item)

      if self.analysisresults.sigIDPUIDFrequency is not None:
         self.__output_list_title__(self.STRINGS.HEADING_FREQUENCY_PUIDS_IDENTIFIED)
         self.printFormattedText(self.__frequencyoutput__(self.analysisresults.sigIDPUIDFrequency, False, True))

      if self.analysisresults.extensionIDOnlyCount > 0:
         if self.analysisresults.extensionOnlyIDList is not None:
            if len(self.analysisresults.extensionOnlyIDList) > 0:
               self.__output_list_title__(self.STRINGS.HEADING_EXTENSION_ONLY)
               for item in self.analysisresults.extensionOnlyIDList:
                  output = item[0] + ", " + item[1]
                  self.printFormattedText(output)
      
      dates = self.getDateList()
      if dates is not None:
         self.__output_list_title__(self.STRINGS.HEADING_DATE_RANGE)
         self.printFormattedText(dates)

      if self.analysisresults.idmethodFrequency is not None:
         self.__output_list_title__(self.STRINGS.HEADING_ID_METHOD)
         self.printFormattedText(self.__frequencyoutput__(self.analysisresults.idmethodFrequency))
      
      if self.analysisresults.extensionIDOnlyCount > 0:
         if self.analysisresults.extensionOnlyIDList is not None and self.analysisresults.extensionOnlyIDFrequency is not None:
            if len(self.analysisresults.extensionOnlyIDList) > 0:
               self.__output_list_title__(self.STRINGS.HEADING_FREQUENCY_EXTENSION_ONLY)
               self.printFormattedText(self.__frequencyoutput__(self.analysisresults.extensionOnlyIDFrequency))

      if self.analysisresults.uniqueExtensionsInCollectionList is not None:
         self.__output_list_title__(self.STRINGS.HEADING_UNIQUE_EXTENSIONS)
         output = ''
         for item in self.analysisresults.uniqueExtensionsInCollectionList:
            output = output + item[0] + ", " 
         self.printFormattedText(output.strip(", "))

      if self.analysisresults.multipleIDList is not None:
         if len(self.analysisresults.multipleIDList) > 0:
            self.__output_list_title__(self.STRINGS.HEADING_LIST_MULTIPLE)
            self.printFormattedText(self.__itemlist__(self.analysisresults.multipleIDList))

      if self.analysisresults.frequencyOfAllExtensions is not None:
         self.__output_list_title__(self.STRINGS.HEADING_FREQUENCY_EXTENSIONS_ALL)
         self.printFormattedText(self.__frequencyoutput__(self.analysisresults.frequencyOfAllExtensions)) 

      if self.analysisresults.mimetypeFrequency is not None:
         self.__output_list_title__(self.STRINGS.HEADING_FREQUENCY_MIME)
         self.printFormattedText(self.__frequencyoutput__(self.analysisresults.mimetypeFrequency, True))

      if self.analysisresults.zerobytecount > 0:
         self.printFormattedText("\n")
         self.printFormattedText(self.__output_list__(self.STRINGS.HEADING_LIST_ZERO_BYTES, self.analysisresults.zerobytecount))
         self.printFormattedText(self.__itemlist__(self.analysisresults.zerobytelist))

      '''
      if self.analysisresults.filesWithNoIDList is not None:
         if len(self.analysisresults.filesWithNoIDList) > 0:
            self.printFormattedText("\n")
            self.printFormattedText(self.__output_list__(self.STRINGS.HEADING_NO_ID, self.analysisresults.zeroidcount))
            self.printFormattedText(self.__itemlist__(self.analysisresults.filesWithNoIDList))
      '''
      
      if self.analysisresults.containertypeslist is not None:
         if len(self.analysisresults.containertypeslist) > 0:
            self.__output_list_title__(self.STRINGS.HEADING_ARCHIVE_FORMATS)
            output = ""
            for archive in self.analysisresults.containertypeslist:
               output = output + archive[0] + ", " 
            self.printFormattedText(output.strip(", "))

      self.printFormattedText('\n' , True)

      if self.analysisresults.hashused > 0:
         if self.analysisresults.totalHASHduplicates > 0:
            self.printFormattedText(self.__output_list__(self.STRINGS.HEADING_IDENTICAL_CONTENT, self.analysisresults.totalHASHduplicates))
            self.printFormattedText(self.__outputdupes__(self.analysisresults.duplicateHASHlisting))

      if self.analysisresults.badFileNames is not None:
         if len(self.analysisresults.badFileNames) > 0:
            self.__output_list_title__(self.STRINGS.HEADING_TROUBLESOME_FILENAMES)
            for badnames in self.analysisresults.badFileNames:
               # Already UTF-8 on way into here...
               self.printFormattedText(badnames, False)
      
      if self.analysisresults.badDirNames is not None:
         if len(self.analysisresults.badDirNames) > 0:
            self.__output_list_title__(self.STRINGS.HEADING_TROUBLESOME_FILENAMES)
            for badnames in self.analysisresults.badDirNames:
               # Already UTF-8 on way into here...
               self.printFormattedText(badnames, False)      
