# -*- coding: utf-8 -*-
import re
import sys
import DroidAnalysisClass
from internationalstrings import AnalysisStringsEN as IN_EN

class DROIDAnalysisHTMLOutput:

   htmloutput = ''

   def __init__(self, analysisresults):
      self.wiki = True
      self.STRINGS = IN_EN
      self.analysisresults = analysisresults

   def STDOUTprintFormattedText(self, text):
      sys.stdout.write(text)
      self.__printnewline__()
   
   def STDOUT__printnewline__(self):
      sys.stdout.write("\n")

   def printFormattedText(self, text):
      if type(text) is list:
         for t in text:
            self.htmloutput = self.htmloutput + str(t) + "</br></br>"
      else:
         self.htmloutput = self.htmloutput + text
         
      self.__printnewline__()
   
   def __printnewline__(self):
      self.htmloutput = self.htmloutput + "\n"
   
   def __htmlnewline__(self, no=1):
      for x in range(no):
         self.printFormattedText("</br>")
   
   def __make_str__(self, str):
      return str + ": "
      
   def __make_summary__(self, str):
      return "<details><summary>" + self.STRINGS.REPORT_MORE_INFORMATION + "</br></summary></br>" + str + "</br></details>"
   
   def __make_list_item__(self, title, content, value):
      return "<li title='" + title + "'>" + self.__make_str__(content) + str(value) + "</li>"
   
   def __keyvalue_output__(self, list):
      self.__htmlnewline__()
      for item in list:
         self.printFormattedText(str(item[0]) + ", " + str(item[1]) + '</br>')
      self.__htmlnewline__() 
      self.printFormattedText("<hr/>")

   def __csv_output__(self, list):
      self.__htmlnewline__()
      out = ""
      for item in list:
         out = out + str(item[0]) + ", "
      self.printFormattedText(out.strip(", "))
      self.__htmlnewline__(2) 
      self.printFormattedText("<hr/>")

   #Trial function we're not using yet... Prettty Print
   def prettyprinthtml():
      #document_root = html.fromstring(self.htmloutput)
      #print document_root
      #print(etree.tostring(document_root, encoding='utf-8', pretty_print=True))
      return None
   
   def printHTMLResults(self):
      self.generateHTML()
      return self.htmloutput
   
   def generateHTML(self):
   
      self.printFormattedText("<!DOCTYPE html>")
      self.printFormattedText("<html lang='en'>")
      self.printFormattedText("<head>")
      if self.analysisresults.tooltype != 'droid':
         self.printFormattedText("<title>" + self.STRINGS.REPORT_TITLE_SF + "</title>")
      else:
         self.printFormattedText("<title>" + self.STRINGS.REPORT_TITLE_DR + "</title>")
      self.printFormattedText("<meta http-equiv='Content-Type' content='text/html; charset=utf-8'>")
      self.printFormattedText("</head>")
   
      self.printFormattedText("<body style='font-family: calibri, arial; letter-spacing: 0.5px; margin:0 auto; width: 800px; '>")

      if self.analysisresults.tooltype != 'droid':   
         self.printFormattedText("<h1>" + self.STRINGS.REPORT_TITLE_SF + "</h1>")
      else:
         self.printFormattedText("<h1>" + self.STRINGS.REPORT_TITLE_DR + "</h1>")

      self.printFormattedText("<b>" + self.STRINGS.REPORT_VERSION + ": </b>" + self.analysisresults.__version__())
      self.__htmlnewline__() 
      self.printFormattedText("<b>" + self.STRINGS.REPORT_FILE + ": </b>" + self.analysisresults.filename)
      self.__htmlnewline__(2) 

      self.printFormattedText("<h2>" + self.STRINGS.REPORT_SUMMARY + "</h2>")

      self.printFormattedText("<ul>")
      self.printFormattedText(self.__make_list_item__(self.STRINGS.SUMMARY_DESC_TOTAL_FILES, self.STRINGS.SUMMARY_TOTAL_FILES, self.analysisresults.filecount))
      self.printFormattedText(self.__make_list_item__(self.STRINGS.SUMMARY_DESC_ARCHIVE_FILES, self.STRINGS.SUMMARY_ARCHIVE_FILES, self.analysisresults.containercount))
      self.printFormattedText(self.__make_list_item__(self.STRINGS.SUMMARY_DESC_INSIDE_ARCHIVES, self.STRINGS.SUMMARY_INSIDE_ARCHIVES, self.analysisresults.filesincontainercount))
      self.printFormattedText(self.__make_list_item__(self.STRINGS.SUMMARY_DESC_DIRECTORIES, self.STRINGS.SUMMARY_DIRECTORIES, self.analysisresults.directoryCount))
      self.printFormattedText(self.__make_list_item__(self.STRINGS.SUMMARY_DESC_UNIQUE_DIRNAMES, self.STRINGS.SUMMARY_UNIQUE_DIRNAMES, self.analysisresults.uniqueDirectoryNames))
      self.printFormattedText(self.__make_list_item__(self.STRINGS.SUMMARY_DESC_IDENTIFIED_FILES, self.STRINGS.SUMMARY_IDENTIFIED_FILES, self.analysisresults.identifiedfilecount))
      self.printFormattedText(self.__make_list_item__(self.STRINGS.SUMMARY_DESC_MULTIPLE, self.STRINGS.SUMMARY_MULTIPLE, self.analysisresults.multipleidentificationcount))
      self.printFormattedText(self.__make_list_item__(self.STRINGS.SUMMARY_DESC_UNIDENTIFIED, self.STRINGS.SUMMARY_UNIDENTIFIED, self.analysisresults.unidentifiedfilecount))
      self.printFormattedText(self.__make_list_item__(self.STRINGS.SUMMARY_DESC_EXTENSION_ID, self.STRINGS.SUMMARY_EXTENSION_ID, self.analysisresults.extensionIDOnlyCount))
      self.printFormattedText(self.__make_list_item__(self.STRINGS.SUMMARY_DESC_EXTENSION_MISMATCH, self.STRINGS.SUMMARY_EXTENSION_MISMATCH, self.analysisresults.extmismatchCount))
      self.printFormattedText(self.__make_list_item__(self.STRINGS.SUMMARY_DESC_ID_PUID_COUNT, self.STRINGS.SUMMARY_ID_PUID_COUNT, self.analysisresults.distinctSignaturePuidcount))
      self.printFormattedText(self.__make_list_item__(self.STRINGS.SUMMARY_DESC_UNIQUE_EXTENSIONS, self.STRINGS.SUMMARY_UNIQUE_EXTENSIONS, self.analysisresults.distinctextensioncount))
      self.printFormattedText(self.__make_list_item__(self.STRINGS.SUMMARY_DESC_ZERO_BYTE, self.STRINGS.SUMMARY_ZERO_BYTE, self.analysisresults.zerobytecount))

      if self.analysisresults.hashused > 0:
         self.printFormattedText(self.__make_list_item__(self.STRINGS.SUMMARY_DESC_IDENTICAL_FILES, self.STRINGS.SUMMARY_IDENTICAL_FILES, self.analysisresults.totalHASHduplicates))

      self.printFormattedText(self.__make_list_item__(self.STRINGS.SUMMARY_DESC_MULTIPLE_SPACES, self.STRINGS.SUMMARY_MULTIPLE_SPACES, len(self.analysisresults.multiplespacelist)))
      self.printFormattedText(self.__make_list_item__(self.STRINGS.SUMMARY_DESC_PERCENTAGE_IDENTIFIED, self.STRINGS.SUMMARY_PERCENTAGE_IDENTIFIED, self.analysisresults.identifiedPercentage))
      self.printFormattedText(self.__make_list_item__(self.STRINGS.SUMMARY_DESC_PERCENTAGE_UNIDENTIFIED, self.STRINGS.SUMMARY_PERCENTAGE_UNIDENTIFIED, self.analysisresults.unidentifiedPercentage))
      self.printFormattedText("</ul>")
      self.__htmlnewline__() 
      self.printFormattedText("<hr/>")

      #return the size of the collection
      self.printFormattedText("<h2>" + self.__make_str__(self.STRINGS.HEADING_SIZE) + "</h2>")
      self.printFormattedText(self.__make_summary__(self.STRINGS.HEADING_DESC_SIZE))
      self.__htmlnewline__() 
      
      #easier to reference from a var
      size = self.analysisresults.collectionsize
      
      self.printFormattedText(str(int(size)) + " bytes | " + str(int(size/(1048576))) + " MiB/MB (Megabytes)") #MiB/MB = (2^1024)*2
      self.__htmlnewline__(2) 
      self.printFormattedText("<hr/>")

      if self.analysisresults.signatureidentifiers is not None:

         #Signature identified PUIDs in collection (signature and container)
         self.printFormattedText("<h2>" + self.__make_str__(self.STRINGS.HEADING_IDENTIFIED) + "</h2>")
         self.printFormattedText(self.__make_summary__(self.STRINGS.HEADING_DESC_IDENTIFIED))
         self.__htmlnewline__() 
      
         self.printFormattedText('<table>')
         self.printFormattedText('<table><th style="text-align: left;"><a target="_blank" href="http://www.nationalarchives.gov.uk/aboutapps/pronom/puid.htm">PUID</a></th><th style="text-align: left;">' + self.STRINGS.COLUMN_HEADER_VALUES_FORMAT + '</th><th style="text-align: left;">' + self.STRINGS.COLUMN_HEADER_VALUES_COUNT + '</th>')
               
         #ex: ('ns:pronom fmt/19, Acrobat PDF 1.5 - Portable Document Format, 1.5 (6)', 1)
         for puid in self.analysisresults.signatureidentifiers:
            #(x-)?fmt\/[0-9]+
            identifier = puid[0].rsplit('(',1)[0]
            count = puid[0].rsplit('(',1)[1].replace(')','')
            patt = re.compile('(x-)?fmt\/[0-9]+')
            p = re.search(patt, identifier)
            if p is not None:
               p = p.span()
               markup = '<tr><td style="width: 100px;"><a target="_blank" href="http://apps.nationalarchives.gov.uk/PRONOM/' + identifier[p[0]:p[1]] + '">' + identifier[p[0]:p[1]] + '</a></td><td>' + identifier + '</td><td style="text-align:center">' + str(count) + '</td></tr>'
            else:
               idtext = identifier.split(',',1)[0].replace('ns:tika', '').replace('ns:freedesktop.org','').strip()
               markup = '<tr><td style="width: 150px;">' + idtext + '</td><td>' + identifier + '</td><td style="text-align:center">' + str(count) + '</td></tr>'
            self.printFormattedText(markup)
         self.printFormattedText('</table>')

         self.__htmlnewline__(2)  
         self.printFormattedText("<hr/>")
      
      '''
      if self.analysisresults.sigIDPUIDFrequency is not None:
         #Signature ID PUIDs
         self.printFormattedText("<h2>" + self.__make_str__(self.STRINGS.HEADING_FREQUENCY_PUIDS_IDENTIFIED) + "</h2>")
         self.printFormattedText(self.__make_summary__(self.STRINGS.HEADING_DESC_FREQUENCY_PUIDS_IDENTIFIED))
         self.__htmlnewline__()
         self.printFormattedText('<table>')
         self.printFormattedText('<table><th style="text-align: left;"><a target="_blank" href="http://www.nationalarchives.gov.uk/aboutapps/pronom/puid.htm">PUID</a></th><th style="text-align: left;">' + self.STRINGS.COLUMN_HEADER_VALUES_COUNT + '</th>') 
         for sig in self.analysisresults.sigIDPUIDFrequency:
            self.printFormattedText('<tr><td style="width: 100px;">')
            self.printFormattedText('<a target="_blank" href="http://apps.nationalarchives.gov.uk/PRONOM/' + sig[0] + '">' + sig[0] + '</a>')
            self.printFormattedText('</td><td>' + str(sig[1]).strip() + '</td>')
    
            #Unused Meter Code...
            self.printFormattedText('<td><meter style="width: 300px;" value="' + str(sig[1]).strip() + '" min="0" max="' + str(self.analysisresults.filecount) + '">test</meter></td>')
           
            self.printFormattedText('</tr>')
           
         self.printFormattedText('</table>')
         self.__htmlnewline__() 
         self.printFormattedText("<hr/>")

      if self.analysisresults.dateFrequency is not None:
         #Date Ranges
         self.printFormattedText("<h2>" + self.__make_str__(self.STRINGS.HEADING_DATE_RANGE) + "</h2>")
         self.printFormattedText(self.__make_summary__(self.STRINGS.HEADING_DESC_DATE_RANGE))
         self.__htmlnewline__()
         self.printFormattedText('<table>')
         self.printFormattedText('<table><th style="text-align: left;">' + self.STRINGS.COLUMN_HEADER_VALUES_YEAR + '</a></th><th style="text-align: left;">' + self.STRINGS.COLUMN_HEADER_VALUES_COUNT + '</th>') 
         for dates in self.analysisresults.dateFrequency:
            self.printFormattedText('<tr><td style="width: 100px;">')
                    
            if self.wiki is True:
               self.printFormattedText('<a target="_blank" href="https://en.wikipedia.org/wiki/' + str(dates[0]) + '">' + str(dates[0]) + '</a>')
            else:
               self.printFormattedText('<b>' + str(dates[0]) + '</b>')
               
            self.printFormattedText('</td><td>' + str(dates[1]).strip() + '</td>')
    
            #Unused Meter Code...
            self.printFormattedText('<td><meter style="width: 300px;" value="' + str(dates[1]).strip() + '" min="0" max="' + str(self.analysisresults.filecount) + '">test</meter></td>')
            self.printFormattedText('</tr>')
           
         self.printFormattedText('</table>')
         self.__htmlnewline__() 
         self.printFormattedText("<hr/>")

      if self.analysisresults.idmethodFrequency is not None:
         #ID Method Frequency
         self.printFormattedText("<h2>" + self.__make_str__(self.STRINGS.HEADING_ID_METHOD) + "</h2>")
         self.printFormattedText(self.__make_summary__(self.STRINGS.HEADING_DESC_ID_METHOD))
         self.__htmlnewline__() 
         for method in self.analysisresults.idmethodFrequency:
            self.printFormattedText(str(method[0]) + ", " + str(method[1]) + '</br>')
         self.__htmlnewline__() 
         self.printFormattedText("<hr/>")

      if self.analysisresults.extensionOnlyIDList is not None:
         if len(self.analysisresults.extensionOnlyIDList) > 0:
            #Extension Only ID
            self.printFormattedText("<h2>" + self.__make_str__(self.STRINGS.HEADING_EXTENSION_ONLY) + "</h2>")
            self.printFormattedText(self.__make_summary__(self.STRINGS.HEADING_DESC_EXTENSION_ONLY))
            self.__keyvalue_output__(self.analysisresults.extensionOnlyIDList)
         
      if self.analysisresults.extensionOnlyIDList is not None:
         if len(self.analysisresults.extensionOnlyIDList) > 0:
            #Extension Only Identification
            self.printFormattedText("<h2>" + self.__make_str__(self.STRINGS.HEADING_FREQUENCY_EXTENSION_ONLY) + "</h2>")
            self.printFormattedText(self.__make_summary__(self.STRINGS.HEADING_DESC_FREQUENCY_EXTENSION_ONLY))
            self.__keyvalue_output__(self.analysisresults.extensionOnlyIDFrequency)

      if self.analysisresults.uniqueExtensionsInCollectionList is not None:
         #Unique Extensions Identified
         self.printFormattedText("<h2>" + self.__make_str__(self.STRINGS.HEADING_UNIQUE_EXTENSIONS) + "</h2>")
         self.printFormattedText(self.__make_summary__(self.STRINGS.HEADING_DESC_UNIQUE_EXTENSIONS))
         self.__htmlnewline__()
         extstr = ''
         for ext in self.analysisresults.uniqueExtensionsInCollectionList:
            extstr = extstr + ext[0] + ", "
         self.printFormattedText(extstr.strip(", "))
         self.__htmlnewline__(2) 
         self.printFormattedText("<hr/>")

      if self.analysisresults.multipleIDList is not None:
         if len(self.analysisresults.multipleIDList) > 0:
            #Files with multiple identifications
            self.printFormattedText("<h2>" + self.__make_str__(self.STRINGS.HEADING_LIST_MULTIPLE) + "</h2>")
            self.printFormattedText(self.__make_summary__(self.STRINGS.HEADING_DESC_LIST_MULTIPLE))
            self.__htmlnewline__()
            self.printFormattedText("<code>")
            self.printFormattedText(self.analysisresults.multipleIDList)
            self.printFormattedText("</code>")
            self.__htmlnewline__() 
            self.printFormattedText("<hr/>")

      if self.analysisresults.frequencyOfAllExtensions is not None: 
         #Extension Frequency
         self.printFormattedText("<h2>" + self.__make_str__(self.STRINGS.HEADING_FREQUENCY_EXTENSIONS_ALL) + "</h2>")
         self.printFormattedText(self.__make_summary__(self.STRINGS.HEADING_DESC_FREQUENCY_EXTENSIONS_ALL))
         self.__keyvalue_output__(self.analysisresults.frequencyOfAllExtensions)

      if self.analysisresults.mimetypeFrequency is not None:      
         #Mimetype Frequency
         self.printFormattedText("<h2>" + self.__make_str__(self.STRINGS.HEADING_FREQUENCY_MIME) + "</h2>")
         self.printFormattedText(self.__make_summary__(self.STRINGS.HEADING_DESC_FREQUENCY_MIME))
         self.__keyvalue_output__(self.analysisresults.mimetypeFrequency)

      if self.analysisresults.zerobytelist is not None:
         if len(self.analysisresults.zerobytelist):
            #Zero Byte Objects
            self.printFormattedText("<h2>" + self.__make_str__(self.STRINGS.HEADING_LIST_ZERO_BYTES) + str(self.analysisresults.zerobytecount) + "</h2>")
            self.printFormattedText(self.__make_summary__(self.STRINGS.HEADING_DESC_LIST_ZERO_BYTES))
            self.__htmlnewline__() 
            self.printFormattedText("<code>")
            self.printFormattedText(self.analysisresults.zerobytelist)
            self.printFormattedText("</code>")
            self.printFormattedText("<hr/>")

      if self.analysisresults.filesWithNoIDList is not None:
         if len(self.analysisresults.filesWithNoIDList) > 0:
            #Zero Identification
            self.printFormattedText("<h2>" + self.__make_str__(self.STRINGS.HEADING_NO_ID) + str(self.analysisresults.zeroidcount) + "</h2>")
            self.printFormattedText(self.__make_summary__(self.STRINGS.HEADING_DESC_NO_ID))
            self.__htmlnewline__() 
            self.printFormattedText("<code>")
            self.printFormattedText(self.analysisresults.filesWithNoIDList)
            self.printFormattedText("</code>")
            self.printFormattedText("<hr/>")

      if self.analysisresults.containertypeslist is not None:
         if len(self.analysisresults.containertypeslist) > 0:
            #archive file types
            self.printFormattedText("<h2>" + self.__make_str__(self.STRINGS.HEADING_ARCHIVE_FORMATS) + "</h2>")
            self.printFormattedText(self.__make_summary__(self.STRINGS.HEADING_DESC_ARCHIVE_FORMATS))
            self.__csv_output__(self.analysisresults.containertypeslist)

      if self.analysisresults.hashused is True:
         if self.analysisresults.duplicateHASHlisting is not None:
            #Duplicate Content      
            self.printFormattedText("<h2>" + self.__make_str__(self.STRINGS.HEADING_IDENTICAL_CONTENT) + "(" + str(self.analysisresults.totalHASHduplicates) + ")" + "</h2>")
            self.printFormattedText(self.__make_summary__(self.STRINGS.HEADING_DESC_IDENTICAL_CONTENT))
            self.__htmlnewline__() 
            for dupes in self.analysisresults.duplicateHASHlisting:	#TODO: consider count next to HASH val
               self.printFormattedText("<b>" + dupes['checksum'] + "</b> Count: " + dupes['count'] + "<br/><br/>")
               self.printFormattedText("<code>")
               for ex in dupes['examples']:
                  self.printFormattedText(ex + "<br/>")
               self.printFormattedText("</code>")
               self.__htmlnewline__(2) 
            self.printFormattedText("<hr/>")

      if self.analysisresults.badFileNames is not None:
         if len(self.analysisresults.badFileNames) > 0:
            #Troublesome Filenames
            self.printFormattedText("<h2>" + self.__make_str__(self.STRINGS.HEADING_TROUBLESOME_FILENAMES) + "</h2>")
            self.printFormattedText(self.__make_summary__(self.STRINGS.HEADING_DESC_TROUBLESOME_FILENAMES))
            self.__htmlnewline__() 
            for fnames in self.analysisresults.badFileNames:
               self.printFormattedText(fnames)
               self.__htmlnewline__(2) 
            self.__htmlnewline__() 
            self.printFormattedText("<hr/>")

      if self.analysisresults.badDirNames is not None:
         if len(self.analysisresults.badDirNames) > 0:
            #Troublesome Filenames
            self.printFormattedText("<h2>" + self.__make_str__(self.STRINGS.HEADING_TROUBLESOME_DIRNAMES) + "</h2>")
            self.printFormattedText(self.__make_summary__(self.STRINGS.HEADING_DESC_TROUBLESOME_DIRNAMES))
            self.__htmlnewline__() 
            for fnames in self.analysisresults.badDirNames:
               self.printFormattedText(fnames)
               self.__htmlnewline__(2) 
            self.__htmlnewline__() 
            self.printFormattedText("<hr/>")
      '''
      
      self.__htmlnewline__(2) 
      self.printFormattedText("</body>")
      
