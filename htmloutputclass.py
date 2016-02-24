import sys
import DroidAnalysisClass
from internationalstrings import AnalysisStringsEN as IN_EN

class DROIDAnalysisHTMLOutput:

   htmloutput = ''

   def __init__(self, analysisresults):
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
            self.htmloutput = self.htmloutput + t + "</br>"
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
      return "<details><summary>" + self.STRINGS.REPORT_MORE_INFORMATION + "</summary></br>" + str + "</details>"
   
   def __make_list_item__(self, title, content, value):
      return "<li title='" + title + "'>" + self.__make_str__(content) + str(value) + "</li>"
   
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
      self.printFormattedText("<title>" + self.STRINGS.REPORT_TITLE + "</title>")
      self.printFormattedText("<meta http-equiv='Content-Type' content='text/html; charset=utf-8'>")
      self.printFormattedText("</head>")
   
      self.printFormattedText("<body style='font-family: calibri, arial; letter-spacing: 0.5px; margin:0 auto; width: 800px; '>")
   
      self.printFormattedText("<h1>" + self.STRINGS.REPORT_TITLE + "</h1>")
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
      
      self.printFormattedText(str(size) + " bytes | " + str(size/(1048576)) + " MiB/MB (Megabytes)") #MiB/MB = (2^1024)*2
      self.__htmlnewline__(2) 
      self.printFormattedText("<hr/>")

      #Signature identified PUIDs in collection (signature and container)
      self.printFormattedText("<h2>" + self.__make_str__(self.STRINGS.HEADING_IDENTIFIED) + "</h2>")
      self.printFormattedText(self.__make_summary__(self.STRINGS.HEADING_DESC_IDENTIFIED))
      self.__htmlnewline__() 
      
      self.printFormattedText('<table>')
      self.printFormattedText('<table><th style="text-align: left;"><a target="_blank" href="http://www.nationalarchives.gov.uk/aboutapps/pronom/puid.htm">PUID</a></th><th style="text-align: left;">Format Name</th>')
      for x in self.analysisresults.sigIDPUIDList:
         x = x.split(',')
         new_x = '<tr><td style="width: 100px;"><a target="_blank" href="http://apps.nationalarchives.gov.uk/PRONOM/' + x[0] + '">' + x[0] + '</a></td><td>' + "".join(x[1:]) + '</td></tr>'
         self.printFormattedText(new_x)
      self.printFormattedText('</table>')

      self.__htmlnewline__(2)  
      self.printFormattedText("<hr/>")


      #Signature ID PUIDs
      self.printFormattedText("<h2>" + self.__make_str__(self.STRINGS.HEADING_FREQUENCY_PUIDS_IDENTIFIED) + "</h2>")
      self.printFormattedText(self.__make_summary__(self.STRINGS.HEADING_DESC_FREQUENCY_PUIDS_IDENTIFIED))
      self.__htmlnewline__()
      self.printFormattedText('<table>')
      self.printFormattedText('<table><th style="text-align: left;"><a target="_blank" href="http://www.nationalarchives.gov.uk/aboutapps/pronom/puid.htm">PUID</a></th><th style="text-align: left;">Count</th>') 
      for s in self.analysisresults.sigIDPUIDFrequency:
         s = s.split(',')
         self.printFormattedText('<tr><td style="width: 100px;">')
         self.printFormattedText('<a target="_blank" href="http://apps.nationalarchives.gov.uk/PRONOM/' + s[0] + '">' + s[0] + '</a>')
         self.printFormattedText('</td><td>' + s[1].strip() + '</td>')
 
         #Unused Meter Code...
         self.printFormattedText('<td><meter style="width: 300px;" value="' + s[1].strip() + '" min="0" max="' + str(self.analysisresults.filecount) + '">test</meter></td>')
        
         self.printFormattedText('</tr>')
        
      self.printFormattedText('</table>')
      self.__htmlnewline__() 
      self.printFormattedText("<hr/>")

      #Date Ranges
      self.printFormattedText("<h2>" + self.__make_str__(self.STRINGS.HEADING_DATE_RANGE) + "</h2>")
      self.printFormattedText(self.__make_summary__(self.STRINGS.HEADING_DESC_DATE_RANGE))
      self.__htmlnewline__()
      self.printFormattedText('<table>')
      self.printFormattedText('<table><th style="text-align: left;">Year</a></th><th style="text-align: left;">Count</th>') 
      for s in self.analysisresults.dateFrequency:
         s = s.split(',')
         self.printFormattedText('<tr><td style="width: 100px;">')

         #self.printFormattedText('<a target="_blank" href="https://en.wikipedia.org/wiki/' + s[0] + '">' + s[0] + '</a>')
         
         self.printFormattedText('<b>' + s[0] + '</b>')
         self.printFormattedText('</td><td>' + s[1].strip() + '</td>')
 
         #Unused Meter Code...
         self.printFormattedText('<td><meter style="width: 300px;" value="' + s[1].strip() + '" min="0" max="' + str(self.analysisresults.filecount) + '">test</meter></td>')
        
         self.printFormattedText('</tr>')
        
      self.printFormattedText('</table>')
      self.__htmlnewline__() 
      self.printFormattedText("<hr/>")

      #Extension Only ID
      self.printFormattedText("<h2>" + self.__make_str__(self.STRINGS.HEADING_EXTENSION_ONLY) + "</h2>")
      self.printFormattedText(self.__make_summary__(self.STRINGS.HEADING_DESC_EXTENSION_ONLY))
      self.__htmlnewline__() 
      self.printFormattedText(self.analysisresults.extensionOnlyIDList.replace('|', '</br>'))
      self.__htmlnewline__(2) 
      self.printFormattedText("<hr/>")

      #ID Method Frequency
      self.printFormattedText("<h2>" + self.__make_str__(self.STRINGS.HEADING_ID_METHOD) + "</h2>")
      self.printFormattedText(self.__make_summary__(self.STRINGS.HEADING_DESC_ID_METHOD))
      self.__htmlnewline__() 
      self.printFormattedText(self.analysisresults.idmethodFrequency.replace('\n', '</br>'))
      self.__htmlnewline__(2) 
      self.printFormattedText("<hr/>")

      #Extension Only Identification
      self.printFormattedText("<h2>" + self.__make_str__(self.STRINGS.HEADING_FREQUENCY_EXTENSION_ONLY) + "</h2>")
      self.printFormattedText(self.__make_summary__(self.STRINGS.HEADING_DESC_FREQUENCY_EXTENSION_ONLY))
      self.__htmlnewline__() 
      self.printFormattedText(self.analysisresults.extensionOnlyIDFrequency)
      self.__htmlnewline__() 
      self.printFormattedText("<hr/>")

      #Unique Extensions Identified
      self.printFormattedText("<h2>" + self.__make_str__(self.STRINGS.HEADING_UNIQUE_EXTENSIONS) + "</h2>")
      self.printFormattedText(self.__make_summary__(self.STRINGS.HEADING_DESC_UNIQUE_EXTENSIONS))
      self.__htmlnewline__() 
      self.printFormattedText(self.analysisresults.uniqueExtensionsInCollectionList)
      self.__htmlnewline__() 
      self.printFormattedText("<hr/>")

      if len(self.analysisresults.multipleIDList) > 0:
         #Files with multiple identifications
         self.printFormattedText("<h2>" + self.__make_str__(self.STRINGS.HEADING_LIST_MULTIPLE) + "</h2>")
         self.printFormattedText(self.__make_summary__(self.STRINGS.HEADING_DESC_LIST_MULTIPLE))
         self.__htmlnewline__() 
         self.printFormattedText(self.analysisresults.multipleIDList)
         self.__htmlnewline__() 
         self.printFormattedText("<hr/>")

      #Extension Frequency
      self.printFormattedText("<h2>" + self.__make_str__(self.STRINGS.HEADING_FREQUENCY_EXTENSIONS_ALL) + "</h2>")
      self.printFormattedText(self.__make_summary__(self.STRINGS.HEADING_DESC_FREQUENCY_EXTENSIONS_ALL))
      self.__htmlnewline__() 
      self.printFormattedText(self.analysisresults.frequencyOfAllExtensions)
      self.__htmlnewline__() 
      self.printFormattedText("<hr/>")

      #Mimetype Frequency
      self.printFormattedText("<h2>" + self.__make_str__(self.STRINGS.HEADING_FREQUENCY_MIME) + "</h2>")
      self.printFormattedText(self.__make_summary__(self.STRINGS.HEADING_DESC_FREQUENCY_MIME))
      self.__htmlnewline__() 
      self.printFormattedText(self.analysisresults.mimetypeFrequency)
      self.__htmlnewline__() 
      self.printFormattedText("<hr/>")

      if len(self.analysisresults.zerobytelist):
         #Zero Byte Objects
         self.printFormattedText("<h2>" + self.__make_str__(self.STRINGS.HEADING_LIST_ZERO_BYTES) + str(self.analysisresults.zerobytecount) + "</h2>")
         self.printFormattedText(self.__make_summary__(self.STRINGS.HEADING_DESC_LIST_ZERO_BYTES))
         self.__htmlnewline__() 
         self.printFormattedText(self.analysisresults.zerobytelist)
         self.printFormattedText("<hr/>")

      #Zero Identification
      if len(self.analysisresults.filesWithNoIDList) > 0:
         self.printFormattedText("<h2>" + self.__make_str__(self.STRINGS.HEADING_NO_ID) + str(self.analysisresults.zeroidcount) + "</h2>")
         self.printFormattedText(self.__make_summary__(self.STRINGS.HEADING_DESC_NO_ID))
         self.__htmlnewline__() 
         self.printFormattedText(self.analysisresults.filesWithNoIDList)
         self.__htmlnewline__() 
         self.printFormattedText("<hr/>")

      if len(self.analysisresults.containertypeslist) > 0:
         #Container Types
         self.printFormattedText("<h2>" + self.__make_str__(self.STRINGS.HEADING_ARCHIVE_FORMATS) + "</h2>")
         self.printFormattedText(self.__make_summary__(self.STRINGS.HEADING_DESC_ARCHIVE_FORMATS))
         self.__htmlnewline__() 
         sys.stderr.write(str(self.analysisresults.containertypeslist))
         self.printFormattedText(self.analysisresults.containertypeslist)
         self.printFormattedText("<hr/>")

      if self.analysisresults.hashused > 0:
         #Duplicate Content      
         self.printFormattedText("<h2>" + self.__make_str__(self.STRINGS.HEADING_IDENTICAL_CONTENT) + "(" + str(self.analysisresults.totalHASHduplicates) + ")" + "</h2>")
         self.printFormattedText(self.__make_summary__(self.STRINGS.HEADING_DESC_IDENTICAL_CONTENT))
         self.__htmlnewline__() 
         for d in self.analysisresults.duplicateHASHlisting:	#TODO: consider count next to HASH val
            self.printFormattedText(d.replace('\n', '</br>').replace(',','</br>').replace('Context:','<b>Context:</b>').replace('Filename:','<b>Filename:</b>'))
            self.__htmlnewline__(2) 
         self.printFormattedText("<hr/>")

      if len(self.analysisresults.badFilenames) > 0:
         #Troublesome Filenames
         self.printFormattedText("<h2>" + self.__make_str__(self.STRINGS.HEADING_TROUBLESOME_FILENAMES) + "</h2>")
         self.printFormattedText(self.__make_summary__(self.STRINGS.HEADING_DESC_TROUBLESOME_FILENAMES))
         self.__htmlnewline__() 
         for fnames in self.analysisresults.badFilenames:
            self.printFormattedText(fnames)
            self.__htmlnewline__(2) 
         self.__htmlnewline__() 
         self.printFormattedText("<hr/>")
      
      self.__htmlnewline__(2) 
      self.printFormattedText("</body>")
      
