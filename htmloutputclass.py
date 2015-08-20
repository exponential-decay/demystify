import sys
import DroidAnalysisClass

class DROIDAnalysisHTMLOutput:

   htmloutput = ''

   def __init__(self, analysisresults):
      self.analysisresults = analysisresults

   def STDOUTprintFormattedText(self, text):
      sys.stdout.write(text)
      self.__printnewline__()
   
   def STDOUT__printnewline__(self):
      sys.stdout.write("\n")

   def printFormattedText(self, text):
      #sys.stdout.write(text)
      
      if type(text) is list:
         for t in text:
            self.htmloutput = self.htmloutput + t + "</br>"
      else:
         self.htmloutput = self.htmloutput + text
         
      self.__printnewline__()
   
   def __printnewline__(self):
      self.htmloutput = self.htmloutput + "\n"
      #sys.stdout.write("\n")
   
   def __htmlnewline__(self, no=1):
      for x in range(no):
         self.printFormattedText("</br>")
   
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
      self.printFormattedText("<title>DROID Sqlite Analysis Results</title>")
      self.printFormattedText("<meta http-equiv='Content-Type' content='text/html; charset=utf-8'>")
      self.printFormattedText("</head>")
   
      self.printFormattedText("<body style='font-family: calibri, arial; letter-spacing: 0.5px; margin:0 auto; width: 800px; '>")
   
      self.printFormattedText("<h1>DROID Analysis</h1>")
      self.printFormattedText("<b>" + "Analysis version: </b>" + self.analysisresults.__version__())
      self.__htmlnewline__() 
      self.printFormattedText("<b>" + "Analysis file: </b>" + self.analysisresults.filename)
      self.__htmlnewline__(2) 

      self.printFormattedText("<h2>Sumary Statistics</h2>")
   
      self.printFormattedText("<ul>")
      self.printFormattedText("<li>" + "Total files: " + str(self.analysisresults.filecount) + "</li>")
      self.printFormattedText("<li>" + "Total container objects: " + str(self.analysisresults.containercount) + "</li>")
      self.printFormattedText("<li>" + "Total files in containers: " + str(self.analysisresults.filesincontainercount) + "</li>")
      self.printFormattedText("<li>" + "Total directories: " + str(self.analysisresults.directoryCount) + "</li>")
      self.printFormattedText("<li>" + "Total unique directory names: " + str(self.analysisresults.uniqueDirectoryNames) + "</li>")
      self.printFormattedText("<li>" + "Total identified files (signature and container): " + str(self.analysisresults.identifiedfilecount) + "</li>")
      self.printFormattedText("<li>" + "Total multiple identifications (signature and container): " + str(self.analysisresults.multipleidentificationcount) + "</li>")
      self.printFormattedText("<li>" + "Total unidentified files (extension and blank): " + str(self.analysisresults.unidentifiedfilecount) + "</li>")
      self.printFormattedText("<li>" + "Total extension ID only count: " + str(self.analysisresults.extensionIDOnlyCount) + "</li>")
      self.printFormattedText("<li>" + "Total extension mismatches: " + str(self.analysisresults.extmismatchCount) + "</li>")		
      self.printFormattedText("<li>" + "Total signature IDd PUID count: " + str(self.analysisresults.distinctSignaturePuidcount) + "</li>")
      self.printFormattedText("<li>" + "Total distinct extensions across collection: " + str(self.analysisresults.distinctextensioncount) + "</li>")
      self.printFormattedText("<li>" + "Total zero-byte files in collection: " + str(self.analysisresults.zerobytecount) + "</li>")
      self.printFormattedText("<li>" + "Total files with duplicate content (MD5 value): " + str(self.analysisresults.totalmd5duplicates) + "</li>")
      
      #Remove duplicate filename reporting
      #self.printFormattedText("<li>" + "Total files with duplicate filenames: " + str(self.analysisresults.filecount - self.analysisresults.uniqueFileNames) + "</li>")
      
      self.printFormattedText("<li>" + "Total files with multiple contiguous space characters: " + str(len(self.analysisresults.multiplespacelist)) + "</li>")
      self.printFormattedText("<li>" + "Percentage of collection identified: " + str(self.analysisresults.identifiedPercentage) + "</li>")
      self.printFormattedText("<li>" + "Percentage of collection unidentified: " + str(self.analysisresults.unidentifiedPercentage) + "</li>")
      self.printFormattedText("</ul>")
      self.__htmlnewline__() 
      self.printFormattedText("<hr/>")

      #Signature identified PUIDs in collection (signature and container)
      self.printFormattedText("<h2>" + "Identified Formats in the Collection:" + "</h2>")
      self.printFormattedText("<details><summary>Identification Information.</summary><br/>" + "Some important additional information." + "</details>")
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
      self.printFormattedText("<h2>" + "Frequency of signature identified PUIDs:" + "</h2>")
      self.printFormattedText("<details><summary>Identification Information.</summary><br/>" + "Some important additional information." + "</details>")
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


      #Extension Only ID
      self.printFormattedText("<h2>" + "Extension only identification in collection:" + "</h2>")
      self.printFormattedText("<details><summary>Identification Information.</summary><br/>" + "Some important additional information." + "</details>")
      self.__htmlnewline__() 
      self.printFormattedText(self.analysisresults.extensionOnlyIDList.replace('|', '</br>'))
      self.__htmlnewline__(2) 
      self.printFormattedText("<hr/>")

      #ID Method Frequency
      self.printFormattedText("<h2>" + "ID Method Frequency: " + "</h2>")
      self.printFormattedText("<details><summary>Identification Information.</summary><br/>" + "Some important additional information." + "</details>")
      self.__htmlnewline__() 
      self.printFormattedText(self.analysisresults.idmethodFrequency.replace('\n', '</br>'))
      self.__htmlnewline__(2) 
      self.printFormattedText("<hr/>")

      #Extension Only Identification
      self.printFormattedText("<h2>" + "Frequency of extension only identification in collection: " + "</h2>")
      self.printFormattedText("<details><summary>Identification Information.</summary><br/>" + "Some important additional information." + "</details>")
      self.__htmlnewline__() 
      self.printFormattedText(self.analysisresults.extensionOnlyIDFrequency)
      self.__htmlnewline__() 
      self.printFormattedText("<hr/>")

      #Unique Extensions Identified
      self.printFormattedText("<h2>" + "Unique extensions identified across all objects (ID & non-ID):" + "</h2>")
      self.printFormattedText("<details><summary>Identification Information.</summary><br/>" + "Some important additional information." + "</details>")
      self.__htmlnewline__() 
      self.printFormattedText(self.analysisresults.uniqueExtensionsInCollectionList)
      self.__htmlnewline__() 
      self.printFormattedText("<hr/>")


      #Files with multiple identifications
      self.printFormattedText("<h2>" + "List of files with multiple identifications: " + "</h2>")
      self.printFormattedText("<details><summary>Description of the term multiple identifications.</summary><br/>" + "Files with size greater than zero and have two or more DROID PUID values associated." + "</details>")
      self.__htmlnewline__() 
      self.printFormattedText(self.analysisresults.multipleIDList)
      self.__htmlnewline__() 
      self.printFormattedText("<hr/>")


      #Extension Frequency
      self.printFormattedText("<h2>" + "Frequency of all extensions:" + "</h2>")
      self.printFormattedText("<details><summary>Identification Information.</summary><br/>" + "Some important additional information." + "</details>")
      self.__htmlnewline__() 
      self.printFormattedText(self.analysisresults.frequencyOfAllExtensions)
      self.__htmlnewline__() 
      self.printFormattedText("<hr/>")


      #Mimetype Frequency
      self.printFormattedText("<h2>" + "MIMEType (Internet Media Type) Frequency: " + "</h2>")
      self.printFormattedText("<details><summary>Identification Information.</summary><br/>" + "Some important additional information." + "</details>")
      self.__htmlnewline__() 
      self.printFormattedText(self.analysisresults.mimetypeFrequency)
      self.__htmlnewline__() 
      self.printFormattedText("<hr/>")


      #Zero Byte Objects
      self.printFormattedText("<h2>" + "Zero byte objects in collection: " + str(self.analysisresults.zerobytecount) + "</h2>")
      self.printFormattedText("<details><summary>Identification Information.</summary><br/>" + "Some important additional information." + "</details>")
      self.__htmlnewline__() 
      self.printFormattedText(self.analysisresults.zerobytelist)


      #Zero Identification
      self.printFormattedText("<h2>" + "Files with no identification: " + str(self.analysisresults.zeroidcount) + "</h2>")
      self.printFormattedText("<details><summary>Identification Information.</summary><br/>" + "Some important additional information." + "</details>")
      self.__htmlnewline__() 
      self.printFormattedText(self.analysisresults.filesWithNoIDList)
      self.__htmlnewline__() 
      self.printFormattedText("<hr/>")


      #Top signature and container IDs
      self.printFormattedText("<h2>" + "Top signature and container identified PUIDs: " + "</h2>")
      self.printFormattedText("<details><summary>Identification Information.</summary><br/>" + "Some important additional information." + "</details>")
      self.__htmlnewline__() 
      self.printFormattedText(self.analysisresults.topPUIDList)
      self.__htmlnewline__() 
      self.printFormattedText("<hr/>")


      #Extensions in Collection
      self.printFormattedText("<h2>" + "Top extensions across collection: " + "</h2>")
      self.printFormattedText("<details><summary>Identification Information.</summary><br/>" + "Some important additional information." + "</details>")
      self.__htmlnewline__() 
      self.printFormattedText(self.analysisresults.topExtensionList)
      self.__htmlnewline__() 
      self.printFormattedText("<hr/>")


      #Container Types
      self.printFormattedText("<h2>" + "Container types in collection: " + "</h2>")
      self.printFormattedText("<details><summary>Identification Information.</summary><br/>" + "Some important additional information." + "</details>")
      self.__htmlnewline__() 
      if len(self.analysisresults.containertypeslist) == 0:
         self.printFormattedText("There are no container types in the collection.")
      else:
         for d in self.analysisresults.containertypeslist:
            self.printFormattedText(d)
            self.__htmlnewline__(2) 
      self.__htmlnewline__(3) 
      self.printFormattedText("<hr/>")


      #Duplicate Content      
      self.printFormattedText("<h2>" + "Files with duplicate content (Total: " + str(self.analysisresults.totalmd5duplicates) + "):" + "</h2>")
      self.printFormattedText("<details><summary>Identification Information.</summary><br/>" + "Some important additional information." + "</details>")
      self.__htmlnewline__() 
      for d in self.analysisresults.duplicatemd5listing:	#TODO: consider count next to MD5 val
         self.printFormattedText(d.replace('\n', '</br>').replace(',','</br>').replace('Context:','<b>Context:</b>').replace('Filename:','<b>Filename:</b>'))
         self.__htmlnewline__(2) 
      self.printFormattedText("<hr/>")


      #Duplicate Filenames - TODO - consider if we need
      '''self.printFormattedText("<h2>" + "Files with duplicate filenames (Total: " + str(self.analysisresults.filecount - self.analysisresults.uniqueFileNames) + ")" + "</h2>")
      self.printFormattedText("<details><summary>Identification Information.</summary><br/>" + "Some important additional information." + "</details>")
      self.__htmlnewline__() 
      self.printFormattedText("<details><summary>Duplicate Filename Listing: <b>" + str(len(self.analysisresults.duplicatefnamelisting)) + "</b></summary>")
      self.__htmlnewline__() 
      for d in	self.analysisresults.duplicatefnamelisting:	#TODO: Can potentially be too many
      	self.printFormattedText(d.replace(',', ' &mdash; '))
      	self.__htmlnewline__(2) 
      self.printFormattedText("</details>")
      self.__htmlnewline__(2) 
      self.printFormattedText("<hr/>")'''


      #Troublesome Filenames
      self.printFormattedText("<h2>" + "Identifying troublesome filenames: " + "</h2>")
      self.printFormattedText("<details><summary>Identification Information.</summary><br/>" + "Some important additional information." + "</details>")
      self.__htmlnewline__() 
      for fnames in self.analysisresults.badFilenames:
         self.printFormattedText(fnames)
         self.__htmlnewline__(2) 
      self.__htmlnewline__() 
      self.printFormattedText("<hr/>")
      
      
      #Contiguous Spaces - TODO - consider if we need
      '''self.printFormattedText("<h2>" + "Files with multiple contiguous spaces (Total: " + str(len(self.analysisresults.multiplespacelist)) + ")" + "</h2>")
      self.printFormattedText("<details><summary>Identification Information.</summary><br/>" + "Some important additional information." + "</details>")
      self.__htmlnewline__() 
      for f in self.analysisresults.multiplespacelist:
         self.printFormattedText("<b>Original Name:</b>   " + f[1])
         self.__htmlnewline__(1) 
         self.printFormattedText("<b>Spaces Shown (&#9644;) :</b> " + f[1].replace(' ', ' &#9644; '))
         self.__htmlnewline__(1) 
         self.printFormattedText("<b>Location:</b>   " + "".join(f))
         self.__htmlnewline__(2)'''
      
      
      self.__htmlnewline__(2) 
      self.printFormattedText("</body>")
      