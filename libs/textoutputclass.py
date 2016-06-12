# -*- coding: utf-8 -*-

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
   def __frequencyoutput__(self, itemlist, zeros=False):         
      val = ''
      ns = None
      if type(itemlist) is not list:
         sys.stderr.write("LOG: Not sending a list to a function wanting a list." + "\n")
      else:
         for item in itemlist:
            if zeros == True:
               val = val + str(item[0]) + ", "
            else:
               val = val + str(item[0]) + " (" + str(item[1]) + "), "
         val = val.strip(", ")
         
      return val

   def __aggregatelists__(self, itemlist):
      outstr = ''
      if type(itemlist) is not list:
         sys.stderr.write("LOG: Not sending a list to a function wanting a list." + "\n")
      else:
         for item in itemlist:
            name = item[0]
            if item[1] != None:
               count = "(" + str(item[1]) + ")"
               outstr = outstr + name + " " + count + "\n"
            else:
               outstr = outstr + name + "\n"
      return outstr.strip("\n")
      
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

   def __handlenamespacestats__(self, nsdatalist, signaturefrequency):
      #e.g.{'binary method count': '57', 'text method count': '37', 'namespace title': 'freedesktop.org', 
      #'filename method count': '45', 'namespace details': 'freedesktop.org.xml'}   
      ds = DroidAnalysisClass.DROIDAnalysis()
      output = ''
      for ns in nsdatalist:
         signatureids = signaturefrequency
         nstitle = ns[ds.NS_CONST_TITLE]
         identified = ns[ds.NS_CONST_BINARY_COUNT]
         xmlid = ns[ds.NS_CONST_XML_COUNT]
         text = ns[ds.NS_CONST_TEXT_COUNT]
         filename = ns[ds.NS_CONST_FILENAME_COUNT]
         ext = ns[ds.NS_CONST_EXTENSION_COUNT]
         unidentified = self.analysisresults.filecount - identified
         percent_not = ds.calculatePercent(self.analysisresults.filecount, unidentified)
         percent_ok = ds.calculatePercent(self.analysisresults.filecount, identified)
         output = output + self.STRINGS.HEADING_NAMESPACE + ": " + nstitle + " (" + ns[ds.NS_CONST_DETAILS] + ")" "\n"
         output = output + self.STRINGS.SUMMARY_IDENTIFIED_FILES + ": " + str(identified) + "\n"         
         output = output + self.STRINGS.SUMMARY_MULTIPLE + ": " + str(ns[ds.NS_CONST_MULTIPLE_IDS]) + "\n"
         output = output + self.STRINGS.SUMMARY_UNIDENTIFIED + ": " + str(unidentified) + "\n"
         output = output + self.STRINGS.SUMMARY_EXTENSION_ID + ": " + str(ext) + "\n"

         if self.analysisresults.tooltype != 'droid':
            output = output + self.STRINGS.SUMMARY_XML_ID + ": " + str(xmlid) + "\n"
            output = output + self.STRINGS.SUMMARY_TEXT_ID + ": " + str(text) + "\n"
            output = output + self.STRINGS.SUMMARY_FILENAME_ID + ": " + str(filename) + "\n"

         output = output + self.STRINGS.SUMMARY_PERCENTAGE_IDENTIFIED + ": " + str(percent_ok) + "\n"
         output = output + self.STRINGS.SUMMARY_PERCENTAGE_UNIDENTIFIED + ": " + str(percent_not) + "\n"
         output = output + "\n"
         output = output + self.STRINGS.HEADING_FREQUENCY_PUIDS_IDENTIFIED + "\n"
         for idrow in signatureids:
            if idrow[0] == nstitle:
               output = output + idrow[1] + " (" + str(idrow[2]) + "), "
         output = output.strip(", ")
         output = output + "\n\n"
      return output.strip("\n")

   def __generateOffsetText__(self, offsettext):
      #########['id','basis','filename','filesize','offset']##########
      offs = offsettext
      if offs != None:
         return offs[0] + ", " + offs[1] + " e.g. " + offs[2] + " filesize: " + str(offs[3]) + ", " + str(offs[4]) + " bytes"

   def __removenamespaceid__(self, oldlist):
      newlist = []
      for item in self.analysisresults.binaryidentifiers:
         newlist.append((str(item[0]), None))
      return newlist

   def generateTEXT(self):   
      if self.analysisresults.tooltype != 'droid':
         self.printFormattedText(self.STRINGS.REPORT_TITLE_SF)
      else:
         self.printFormattedText(self.STRINGS.REPORT_TITLE_DR)

      self.printFormattedText(self.STRINGS.REPORT_VERSION + ": " + self.analysisresults.__version__())
      self.printFormattedText(self.STRINGS.REPORT_FILE + ": " + self.analysisresults.filename)
      self.printFormattedText(self.STRINGS.REPORT_TOOL + ": " + self.analysisresults.tooltype)
      self.printFormattedText("")
      self.printFormattedText(self.STRINGS.NAMESPACES + ": " + str(self.analysisresults.namespacecount))

      if self.analysisresults.bof_distance is not None:
         self.printFormattedText(self.STRINGS.SUMMARY_DISTANCE_BOF + ": " + self.__generateOffsetText__(self.analysisresults.bof_distance))

      if self.analysisresults.eof_distance is not None:
         self.printFormattedText(self.STRINGS.SUMMARY_DISTANCE_EOF + ": " + self.__generateOffsetText__(self.analysisresults.eof_distance))
      
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
         self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_XML_ID, self.analysisresults.xmlidfilecount))
         self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_TEXT_ID, self.analysisresults.textidfilecount))
         self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_FILENAME_ID, self.analysisresults.filenameidfilecount))

      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_EXTENSION_ID, self.analysisresults.extensionIDOnlyCount))
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_EXTENSION_MISMATCH, self.analysisresults.extmismatchCount))
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_ID_PUID_COUNT, self.analysisresults.distinctSignaturePuidcount))
      
      if self.analysisresults.tooltype != 'droid':
         self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_OTHER_ID_COUNT, self.analysisresults.distinctOtherIdentifiers))
         self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_XML_ID_COUNT, self.analysisresults.distinctXMLIdentifiers))
         self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_TEXT_ID_COUNT, self.analysisresults.distinctTextIdentifiers))
         self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_FILENAME_ID_COUNT, self.analysisresults.distinctFilenameIdentifiers))      
      
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_UNIQUE_EXTENSIONS, self.analysisresults.distinctextensioncount))
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_ZERO_BYTE, self.analysisresults.zerobytecount))

      if self.analysisresults.hashused > 0:
         self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_IDENTICAL_FILES, self.analysisresults.totalHASHduplicates))

      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_MULTIPLE_SPACES, len(self.analysisresults.multiplespacelist)))
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_PERCENTAGE_IDENTIFIED, self.analysisresults.identifiedPercentage))
      self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_PERCENTAGE_UNIDENTIFIED, self.analysisresults.unidentifiedPercentage))

      if self.analysisresults.identificationgaps is not None:
         self.printFormattedText(self.__output_list__(self.STRINGS.SUMMARY_GAPS_COVERED, self.analysisresults.identificationgaps))

      #return the size of the collection
      size = self.analysisresults.collectionsize #easier to reference from a var
      self.printFormattedText(self.STRINGS.HEADING_SIZE + ": " + str(float(size)) + " bytes | " + str(round(float(float(size)/(1048576)), 1)) + " MiB/MB (Megabytes)") #MiB/MB = (2^1024)*2

      if self.analysisresults.signatureidentifiers is not None:
         #('ns:pronom x-fmt/266 GZIP Format, extension match gz; byte match at 0, 3', 1)
         self.__output_list_title__(self.STRINGS.HEADING_AGGREGATE_BINARY_IDENTIFIED)
         for ids in self.analysisresults.signatureidentifiers:
            self.printFormattedText(ids[0].rstrip(", "))

      if self.analysisresults.binaryidentifiers is not None:
         self.__output_list_title__(self.STRINGS.HEADING_BINARY_ID)
         newlist = self.__removenamespaceid__(self.analysisresults.binaryidentifiers)
         self.printFormattedText(self.__aggregatelists__(newlist))         
      if self.analysisresults.xmlidentifiers is not None:
         self.__output_list_title__(self.STRINGS.HEADING_XML_ID)
         newlist = self.__removenamespaceid__(self.analysisresults.xmlidentifiers)
         self.printFormattedText(self.__aggregatelists__(newlist))
      if self.analysisresults.textidentifiers is not None:
         self.__output_list_title__(self.STRINGS.HEADING_TEXT_ID)
         newlist = self.__removenamespaceid__(self.analysisresults.textidentifiers)
         self.printFormattedText(self.__aggregatelists__(newlist))
      if self.analysisresults.filenameidentifiers is not None:
         self.__output_list_title__(self.STRINGS.HEADING_FILENAME_ID)
         newlist = self.__removenamespaceid__(self.analysisresults.filenameidentifiers)
         self.printFormattedText(self.__aggregatelists__(newlist))

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
         mimes = self.analysisresults.mimetypeFrequency
         for m in mimes:
            if m[0] == '':
               mimes.remove(m)
         self.printFormattedText(self.__frequencyoutput__(self.analysisresults.mimetypeFrequency))

      ##########NS SPECIFIC OUTPUT####################
      if self.analysisresults.signatureidentifiedfrequency is not None and self.analysisresults.nsdatalist is not None:
         self.__output_list_title__(self.STRINGS.HEADING_NAMESPACE_SPECIFIC_STATISTICS)
         self.printFormattedText(self.__handlenamespacestats__(self.analysisresults.nsdatalist, self.analysisresults.signatureidentifiedfrequency))
      ##########NS SPECIFIC OUTPUT####################

      ##########ID SPECIFIC OUTPUT#################### #XML, TEXT, FILENAME
      if self.analysisresults.xml_identifiers is not None and len(self.analysisresults.xml_identifiers) > 0:
         self.__output_list_title__(self.STRINGS.HEADING_XML_ID_COMPLETE)
         self.printFormattedText(self.__frequencyoutput__(self.analysisresults.xml_identifiers)) 
      if self.analysisresults.text_identifiers is not None and len(self.analysisresults.text_identifiers) > 0:
         self.__output_list_title__(self.STRINGS.HEADING_TEXT_ID_COMPLETE)
         self.printFormattedText(self.__frequencyoutput__(self.analysisresults.text_identifiers)) 
      if self.analysisresults.filename_identifiers is not None and len(self.analysisresults.filename_identifiers) > 0:
         self.__output_list_title__(self.STRINGS.HEADING_FILENAME_ID_COMPLETE)
         self.printFormattedText(self.__frequencyoutput__(self.analysisresults.filename_identifiers)) 
      ##########ID SPECIFIC OUTPUT#################### #XML, TEXT, FILENAME

      if self.analysisresults.zerobytecount > 0:
         self.printFormattedText("\n")
         self.printFormattedText(self.__output_list__(self.STRINGS.HEADING_LIST_ZERO_BYTES, self.analysisresults.zerobytecount))
         self.printFormattedText(self.__itemlist__(self.analysisresults.zerobytelist))
      
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

      if self.analysisresults.blacklist is True:
         if self.analysisresults.blacklist_ids:
            self.__output_list_title__(self.STRINGS.HEADING_BLACKLIST_IDS)
            self.printFormattedText(self.__aggregatelists__(self.analysisresults.blacklist_ids))
         if self.analysisresults.blacklist_exts:
            self.__output_list_title__(self.STRINGS.HEADING_BLACKLIST_EXTS)
            self.printFormattedText(self.__aggregatelists__(self.analysisresults.blacklist_exts))
         if self.analysisresults.blacklist_filenames:
            self.__output_list_title__(self.STRINGS.HEADING_BLACKLIST_FILENAMES)
            self.printFormattedText(self.__aggregatelists__(self.analysisresults.blacklist_filenames))
         if self.analysisresults.blacklist_directories:
            self.__output_list_title__(self.STRINGS.HEADING_BLACKLIST_DIRS)
            self.printFormattedText(self.__aggregatelists__(self.analysisresults.blacklist_directories))

      if self.analysisresults.errorlist is not None:
         self.__output_list_title__(self.STRINGS.HEADING_ERRORS)
         self.printFormattedText(self.__frequencyoutput__(self.analysisresults.errorlist)) 
