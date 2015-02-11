# -*- coding: utf-8 -*-

from __future__ import division
import argparse
import sys
import sqlite3
import csv
import droid2sqlite
import MsoftFnameAnalysis
import RegexFnameAnalysis
from urlparse import urlparse
from lxml import etree, html

class DROIDAnalysis:

   def __version__(self):
      self.__version__ = '0.0.x' #0.0.4
      return self.__version__

   ## DB self.cursor
   cursor = None

   # Counts
   filecount = 0
   containercount = 0
   filesincontainercount = 0	
   directoryCount = 0
   uniqueFileNames = 0
   uniqueDirectoryNames = 0
   identifiedfilecount = 0
   multipleidentificationcount = 0 
   unidentifiedfilecount = 0
   distinctSignaturePuidcount = 0
   extensionIDOnlyCount = 0
   distinctextensioncount = 0
   extmismatchCount = 0
   zeroidcount = 0
   
   unidentifiedPercentage = 0
   identifiedPercentage = 0
   
   sigIDPUIDList = 0
   sigIDPUIDFrequency = 0
   
   extensionOnlyIDList = 0
   extensionOnlyIDFrequency = 0
   
   #TODO: Turn lists into lists? Formatting at end..?
   uniqueExtensionsInCollectionList = 0
   multipleIDList = 0
   frequencyOfAllExtensions = 0
   
   idmethodFrequency = 0
   
   mimetypeFrequency = 0
   
   filesWithNoIDList = 0
   topPUIDList = 0
   topExtensionList = 0
   
   totalmd5duplicates = 0
   duplicatemd5listing = []

   totaluniquefilenames = 0
   duplicatefnamelisting = [] 
   
   containertypeslist = 0
   
   zerobytecount = 0
   zerobytelist = 0

   htmloutput = ""

   def STDOUTprintFormattedText(self, text):
      sys.stdout.write(text)
      self.__printnewline__()
   
   def STDOUT__printnewline__(self):
      sys.stdout.write("\n")

   def printFormattedText(self, text):
      #sys.stdout.write(text)
      self.htmloutput = self.htmloutput + text
      self.__printnewline__()
   
   def __printnewline__(self):
      self.htmloutput = self.htmloutput + "\n"
      #sys.stdout.write("\n")
   
   def __htmlnewline__(self, no=1):
      for x in range(no):
         self.printFormattedText("</br>")
   
   def printMDResults(self):
   
      self.printFormattedText("<!DOCTYPE html>")
      self.printFormattedText("<html lang='en'>")
      self.printFormattedText("<head>")
      self.printFormattedText("<title>DROID Sqlite Analysis Results</title>")
      self.printFormattedText("<meta http-equiv='Content-Type' content='text/html; charset=utf-8'>")
      self.printFormattedText("</head>")
   
      self.printFormattedText("<body style='font-family: calibri, arial; letter-spacing: 0.5px; margin:0 auto; width: 800px; '>")
   
      self.printFormattedText("<h1>DROID Analysis</h1>")
      self.printFormattedText("<b>" + "Analysis version: " + self.__version__() + "</b>")
      self.__htmlnewline__(2) 

      self.printFormattedText("<h2>Sumary Statistics</h2>")
   
      self.printFormattedText("<ul>")
      self.printFormattedText("<li>" + "Total files: " + str(self.filecount) + "</li>")
      self.printFormattedText("<li>" + "Total container objects: " + str(self.containercount) + "</li>")
      self.printFormattedText("<li>" + "Total files in containers: " + str(self.filesincontainercount) + "</li>")
      self.printFormattedText("<li>" + "Total directories: " + str(self.directoryCount) + "</li>")
      self.printFormattedText("<li>" + "Total unique directory names: " + str(self.uniqueDirectoryNames) + "</li>")
      self.printFormattedText("<li>" + "Total identified files (signature and container): " + str(self.identifiedfilecount) + "</li>")
      self.printFormattedText("<li>" + "Total multiple identifications (signature and container): " + str(self.multipleidentificationcount) + "</li>")
      self.printFormattedText("<li>" + "Total unidentified files (extension and blank): " + str(self.unidentifiedfilecount) + "</li>")
      self.printFormattedText("<li>" + "Total extension ID only count: " + str(self.extensionIDOnlyCount) + "</li>")
      self.printFormattedText("<li>" + "Total extension mismatches: " + str(self.extmismatchCount) + "</li>")		
      self.printFormattedText("<li>" + "Total signature IDd PUID count: " + str(self.distinctSignaturePuidcount) + "</li>")
      self.printFormattedText("<li>" + "Total distinct extensions across collection: " + str(self.distinctextensioncount) + "</li>")
      self.printFormattedText("<li>" + "Total zero-byte files in collection: " + str(self.zerobytecount) + "</li>")
      self.printFormattedText("<li>" + "Total files with duplicate content (MD5 value): " + str(self.totalmd5duplicates) + "</li>")
      self.printFormattedText("<li>" + "Total files with duplicate filenames: " + str(self.filecount - self.uniqueFileNames) + "</li>")
      self.printFormattedText("<li>" + "Total files with multiple contiguous space characters: " + str(len(self.multiplespacelist)) + "</li>")
      self.printFormattedText("<li>" + "Percentage of collection identified: " + str(self.identifiedPercentage) + "</li>")
      self.printFormattedText("<li>" + "Percentage of collection unidentified: " + str(self.unidentifiedPercentage) + "</li>")
      self.printFormattedText("</ul>")
      self.__htmlnewline__() 
      self.printFormattedText("<hr/>")

      #Signature identified PUIDs in collection (signature and container)
      self.printFormattedText("<h2>" + "Identified Formats in the Collection:" + "</h2>")
      self.printFormattedText("<details><summary>Identification Information.</summary><br/>" + "Some important additional information." + "</details>")
      self.__htmlnewline__() 
      
      self.printFormattedText('<table>')
      self.printFormattedText('<table><th style="text-align: left;"><a target="_blank" href="http://www.nationalarchives.gov.uk/aboutapps/pronom/puid.htm">PUID</a></th><th style="text-align: left;">Format Name</th>')
      for x in self.sigIDPUIDList:
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
      for s in self.sigIDPUIDFrequency:
         s = s.split(',')
         self.printFormattedText('<tr><td style="width: 100px;">')
         self.printFormattedText('<a target="_blank" href="http://apps.nationalarchives.gov.uk/PRONOM/' + s[0] + '">' + s[0] + '</a>')
         self.printFormattedText('</td><td>' + s[1].strip() + '</td></tr>')
        
         #Unused Meter Code...
         #self.printFormattedText('<meter style="width: 500px;" value="' + s[1].strip() + '" min="0" max="' + str(self.filecount) + '">test</meter>')
        
      self.printFormattedText('</table>')
      self.__htmlnewline__() 
      self.printFormattedText("<hr/>")


      #Extension Only ID
      self.printFormattedText("<h2>" + "Extension only identification in collection:" + "</h2>")
      self.printFormattedText("<details><summary>Identification Information.</summary><br/>" + "Some important additional information." + "</details>")
      self.__htmlnewline__() 
      self.printFormattedText(self.extensionOnlyIDList.replace('|', '</br>'))
      self.__htmlnewline__(2) 
      self.printFormattedText("<hr/>")

      #ID Method Frequency
      self.printFormattedText("<h2>" + "ID Method Frequency: " + "</h2>")
      self.printFormattedText("<details><summary>Identification Information.</summary><br/>" + "Some important additional information." + "</details>")
      self.__htmlnewline__() 
      self.printFormattedText(self.idmethodFrequency.replace('\n', '</br>'))
      self.__htmlnewline__(2) 
      self.printFormattedText("<hr/>")

      #Extension Only Identification
      self.printFormattedText("<h2>" + "Frequency of extension only identification in collection: " + "</h2>")
      self.printFormattedText("<details><summary>Identification Information.</summary><br/>" + "Some important additional information." + "</details>")
      self.__htmlnewline__() 
      self.printFormattedText(self.extensionOnlyIDFrequency)
      self.__htmlnewline__() 
      self.printFormattedText("<hr/>")

      #Unique Extensions Identified
      self.printFormattedText("<h2>" + "Unique extensions identified across all objects (ID & non-ID):" + "</h2>")
      self.printFormattedText("<details><summary>Identification Information.</summary><br/>" + "Some important additional information." + "</details>")
      self.__htmlnewline__() 
      self.printFormattedText(self.uniqueExtensionsInCollectionList)
      self.__htmlnewline__() 
      self.printFormattedText("<hr/>")


      #Files with multiple identifications
      self.printFormattedText("<h2>" + "List of files with multiple identifications: " + "</h2>")
      self.printFormattedText("<details><summary>Identification Information.</summary><br/>" + "Some important additional information." + "</details>")
      self.__htmlnewline__() 
      self.printFormattedText(self.multipleIDList)
      self.__htmlnewline__() 
      self.printFormattedText("<hr/>")


      #Extension Frequency
      self.printFormattedText("<h2>" + "Frequency of all extensions:" + "</h2>")
      self.printFormattedText("<details><summary>Identification Information.</summary><br/>" + "Some important additional information." + "</details>")
      self.__htmlnewline__() 
      self.printFormattedText(self.frequencyOfAllExtensions)
      self.__htmlnewline__() 
      self.printFormattedText("<hr/>")


      #Mimetype Frequency
      self.printFormattedText("<h2>" + "MIMEType (Internet Media Type) Frequency: " + "</h2>")
      self.printFormattedText("<details><summary>Identification Information.</summary><br/>" + "Some important additional information." + "</details>")
      self.__htmlnewline__() 
      self.printFormattedText(self.mimetypeFrequency)
      self.__htmlnewline__() 
      self.printFormattedText("<hr/>")


      #Zero Byte Objects
      self.printFormattedText("<h2>" + "Zero byte objects in collection: " + str(self.zerobytecount) + "</h2>")
      self.printFormattedText("<details><summary>Identification Information.</summary><br/>" + "Some important additional information." + "</details>")
      self.__htmlnewline__() 
      self.printFormattedText(self.zerobytelist)


      #Zero Identification
      self.printFormattedText("<h2>" + "Files with no identification: " + str(self.zeroidcount) + "</h2>")
      self.printFormattedText("<details><summary>Identification Information.</summary><br/>" + "Some important additional information." + "</details>")
      self.__htmlnewline__() 
      self.printFormattedText(self.filesWithNoIDList)
      self.__htmlnewline__() 
      self.printFormattedText("<hr/>")


      #Top signature and container IDs
      self.printFormattedText("<h2>" + "Top signature and container identified PUIDs: " + "</h2>")
      self.printFormattedText("<details><summary>Identification Information.</summary><br/>" + "Some important additional information." + "</details>")
      self.__htmlnewline__() 
      self.printFormattedText(self.topPUIDList)
      self.__htmlnewline__() 
      self.printFormattedText("<hr/>")


      #Extensions in Collection
      self.printFormattedText("<h2>" + "Top extensions across collection: " + "</h2>")
      self.printFormattedText("<details><summary>Identification Information.</summary><br/>" + "Some important additional information." + "</details>")
      self.__htmlnewline__() 
      self.printFormattedText(self.topExtensionList)
      self.__htmlnewline__() 
      self.printFormattedText("<hr/>")


      #Container Types
      self.printFormattedText("<h2>" + "Container types in collection: " + "</h2>")
      self.printFormattedText("<details><summary>Identification Information.</summary><br/>" + "Some important additional information." + "</details>")
      self.__htmlnewline__() 
      if len(self.containertypeslist) == 0:
         self.printFormattedText("There are no container types in the collection.")
      else:
         for d in self.containertypeslist:
            self.printFormattedText(d)
            self.__htmlnewline__(2) 
      self.__htmlnewline__(3) 
      self.printFormattedText("<hr/>")


      #Duplicate Content      
      self.printFormattedText("<h2>" + "Files with duplicate content (Total: " + str(self.totalmd5duplicates) + "):" + "</h2>")
      self.printFormattedText("<details><summary>Identification Information.</summary><br/>" + "Some important additional information." + "</details>")
      self.__htmlnewline__() 
      for d in self.duplicatemd5listing:	#TODO: consider count next to MD5 val
         self.printFormattedText(d.replace('\n', '</br>').replace(',','</br>').replace('Context:','<b>Context:</b>').replace('Filename:','<b>Filename:</b>'))
         self.__htmlnewline__(2) 
      self.printFormattedText("<hr/>")


      #Duplicate Filenames
      self.printFormattedText("<h2>" + "Files with duplicate filenames (Total: " + str(self.filecount - self.uniqueFileNames) + ")" + "</h2>")
      self.printFormattedText("<details><summary>Identification Information.</summary><br/>" + "Some important additional information." + "</details>")
      self.__htmlnewline__() 
      self.printFormattedText("<details><summary>Duplicate Filename Listing: <b>" + str(self.totaluniquefilenames) + "</b></summary>")
      self.__htmlnewline__() 
      for d in	self.duplicatefnamelisting:	#TODO: Can potentially be too many
      	self.printFormattedText(d.replace(',', ' &mdash; '))
      	self.__htmlnewline__(2) 
      self.printFormattedText("</details>")
      self.__htmlnewline__(2) 
      self.printFormattedText("<hr/>")


      #Troublesome Filenames
      self.printFormattedText("<h2>" + "Identifying troublesome filenames: " + "</h2>")
      self.printFormattedText("<details><summary>Identification Information.</summary><br/>" + "Some important additional information." + "</details>")
      self.__htmlnewline__() 
      for fnames in self.badFilenames:
         self.printFormattedText(fnames)
         self.__htmlnewline__(2) 
      self.__htmlnewline__() 
      self.printFormattedText("<hr/>")
      
      
      #Contiguous Spaces
      self.printFormattedText("<h2>" + "Files with multiple contiguous spaces (Total: " + str(len(self.multiplespacelist)) + ")" + "</h2>")
      self.printFormattedText("<details><summary>Identification Information.</summary><br/>" + "Some important additional information." + "</details>")
      self.__htmlnewline__() 
      for f in self.multiplespacelist:
         self.printFormattedText("<b>Original Name:</b>   " + f[1])
         self.__htmlnewline__(1) 
         self.printFormattedText("<b>Spaces Shown (&#9644;) :</b> " + f[1].replace(' ', ' &#9644; '))
         self.__htmlnewline__(1) 
         self.printFormattedText("<b>Location:</b>   " + "".join(f))
         self.__htmlnewline__(2) 
      
      self.__htmlnewline__(2) 


      self.printFormattedText("</body>")
 
   
   
   def printResults(self):
      print "Analysis version: " + self.__version__() + '\n'
   
      print "Total files: " + str(self.filecount)
      print "Total container objects: " + str(self.containercount)
      print "Total files in containers: " + str(self.filesincontainercount) 
      print "Total directories: " + str(self.directoryCount)
      print "Total unique directory names: " + str(self.uniqueDirectoryNames)
      print "Total identified files (signature and container): " + str(self.identifiedfilecount)
      print "Total multiple identifications (signature and container): " + str(self.multipleidentificationcount)
      print "Total unidentified files (extension and blank): " + str(self.unidentifiedfilecount)
      print "Total extension ID only count: " + str(self.extensionIDOnlyCount)
      print "Total extension mismatches: " + str(self.extmismatchCount)		#TODO: List, but could be long
      print "Total signature IDd PUID count: " + str(self.distinctSignaturePuidcount)
      print "Total distinct extensions across collection: " + str(self.distinctextensioncount)
      print "Total zero-byte files in collection: " + str(self.zerobytecount)
      print "Total files with duplicate content (MD5 value): " + str(self.totalmd5duplicates)
      print "Total files with duplicate filenames: " + str(self.filecount - self.uniqueFileNames)
      print "Total files with multiple contiguous space characters: " + str(len(self.multiplespacelist))
      print "Percentage of collection identified: " + str(self.identifiedPercentage)
      print "Percentage of collection unidentified: " + str(self.unidentifiedPercentage)

      print
      print "Signature identified PUIDs in collection (signature and container):"
      print self.sigIDPUIDList

      print
      print "Frequency of signature identified PUIDs:"
      print self.sigIDPUIDFrequency

      print
      print "Extension only identification in collection:"
      print self.extensionOnlyIDList

      print 
      print "ID Method Frequency: "
      print self.idmethodFrequency

      print 
      print "Frequency of extension only identification in collection: "
      print self.extensionOnlyIDFrequency

      print
      print "Unique extensions identified across all objects (ID & non-ID):"
      print self.uniqueExtensionsInCollectionList

      print
      print "List of files with multiple identifications: "
      print self.multipleIDList 

      print
      print "Frequency of all extensions:"
      print self.frequencyOfAllExtensions 

      print
      print "MIMEType (Internet Media Type) Frequency: "
      print self.mimetypeFrequency

      print
      print "Zero byte objects in collection: " + str(self.zerobytecount)
      print self.zerobytelist

      print
      print "Files with no identification: " + str(self.zeroidcount)
      print self.filesWithNoIDList

      print
      print "Top signature and container identified PUIDs: "
      print self.topPUIDList
      
      print
      print "Top extensions across collection: "		
      print self.topExtensionList 	

      print
      print "Container types in collection: "
      print self.containertypeslist

      print 
      print "Files with duplicate content (Total: " + str(self.totalmd5duplicates) + "):"
      for d in self.duplicatemd5listing:	#TODO: consider count next to MD5 val
         print d
         print
         
      print
      print "Files with duplicate filenames (Total: " + str(self.filecount - self.uniqueFileNames) + ")"
      print "Listing disabled as potentially too many..."
      print "Total unique values: " + str(self.totaluniquefilenames)
      #for d in	self.duplicatefnamelisting:	#TODO: Can potentially be too many
      #	print d
      #	print
         
      print
      print "Identifying troublesome filenames: "
      sys.stdout.write(self.badFilenames.encode('utf8'))
      
      print
      print "Files with multiple contiguous spaces (Total: " + str(len(self.multiplespacelist)) + ")" 
      for f in self.multiplespacelist:
         print "original:   " + f[1] 
         print "spaces (%): " + f[1].replace(' ', '%')
         print "location:   " + "".join(f)
         print
      
   def __countQuery__(self, query):
      self.cursor.execute(query)
      count = self.cursor.fetchone()[0]
      return count

   def __listQuery__(self, query, separator):
      self.cursor.execute(query)
      result = self.cursor.fetchall()
      row = ""
      for r in result:
         if len(r) > 1:
            item = ""
            for t in r:
               item = item + str(t) + ", "
            row = row + item[:-2] + separator
         else:
            row = row + str(r[0]) + separator
      try:
         if row[len(row)-2] == "|":
            return row[:-2]
         else:
            return row[:-1]
      except IndexError:
         return row[:-1]
         
   def __listPUIDSQuery__(self, query, separator):
      self.cursor.execute(query)
      result = self.cursor.fetchall()
      row = []
      for r in result:
         if len(r) > 1:
            item = ""
            for t in r:
               item = item + str(t) + ", "
            row.append(item[:-2])
         else:
            row.append(str(r[0]))
      return row


   def __listDuplicateQuery__(self, query, separator):
      self.cursor.execute(query)
      result = self.cursor.fetchall()
      row = ""
      for r in result:
         if len(r) == 2:
            item = "Context: " + r[0] + "\n Filename: " + r[1] + '\n\n'
            row = row + item
      try:
         if row[len(row)-2] == "|":
            return row[:-2]
         else:
            return row[:-1]
      except IndexError:
         return row[:-1]

   def __alternativeFrequencyQuery__(self, query):
      self.cursor.execute(query)
      result = self.cursor.fetchall()
      return result

   def countFilesQuery(self):
      return self.__countQuery__( 
         "SELECT COUNT(NAME) FROM droid WHERE (TYPE='File' OR TYPE='Container')")

   # Container objects known by DROID...
   def countContainerObjects(self):
      return self.__countQuery__(
         "SELECT COUNT(NAME) FROM droid WHERE TYPE='Container'")
   
   def countFilesInContainerObjects(self):
      return self.__countQuery__( 
         "SELECT COUNT(NAME) FROM droid WHERE (URI_SCHEME!='file') AND (TYPE='File' OR TYPE='Container')")

   def countFoldersQuery(self):
      return self.__countQuery__( 
         "SELECT COUNT(NAME) FROM droid WHERE TYPE='Folder'")

   def countUniqueFileNames(self):
      return self.__countQuery__( 
         "SELECT COUNT(DISTINCT NAME) FROM droid WHERE (TYPE='File' OR TYPE='Container')")

   def countUniqueDirectoryNames(self):
      return (self.__countQuery__( 
         "SELECT COUNT(DISTINCT DIR_NAME) FROM droid") - 1)	#Will always be minus one accounts for base-dirs

   def countIdentifiedQuery(self):
      return self.__countQuery__( 
         "SELECT COUNT(NAME) FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (METHOD='Signature' or METHOD='Container')")

   def countMultipleIdentifications(self):
      return self.__countQuery__( 
         "SELECT COUNT(FORMAT_COUNT) FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (FORMAT_COUNT!='1' AND FORMAT_COUNT!='0')")

   def countTotalUnidentifiedQuery(self):
      return self.__countQuery__( 
         "SELECT COUNT(NAME) FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (METHOD='no value' OR METHOD='Extension')")	

   def countZeroID(self):
      return self.__countQuery__( 
         "SELECT COUNT(NAME) FROM droid WHERE METHOD='no value' AND (TYPE='File' OR TYPE='Container')")

   def countExtensionIDOnly(self):
      return self.__countQuery__( 
         "SELECT COUNT(NAME) FROM droid WHERE METHOD='Extension' AND(TYPE='File' OR TYPE='Container')")
   
   # PUIDS for files identified by DROID using binary matching techniques
   def countDistinctSignaturePUIDS(self):
      return self.__countQuery__( 
         "SELECT COUNT(DISTINCT PUID) FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (METHOD='Signature' OR METHOD='Container')")
      
   def countDistinctExtensions(self):
      return self.__countQuery__( 
         "SELECT COUNT(DISTINCT EXT) FROM droid WHERE TYPE='File' OR TYPE='Container'")
   
   def countExtensionMismatches(self):
      return self.__countQuery__( 
         "SELECT COUNT(EXTENSION_MISMATCH) FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (EXTENSION_MISMATCH='true')")	

   def countZeroByteObjects(self):
      return self.__countQuery__( 
         "SELECT COUNT(SIZE) FROM droid WHERE (TYPE='File') AND (SIZE='0')")
      return

   ###
   # Frequency list queries
   ###
   def identifiedBinaryMatchedPUIDFrequency(self):
      return self.__listPUIDSQuery__( 
         "SELECT PUID, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (METHOD='Signature' OR METHOD='Container') GROUP BY PUID ORDER BY TOTAL DESC",  " | ")

   def extensionOnlyIdentificationFrequency(self):
      return self.__listQuery__( 
         "SELECT PUID, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (METHOD='Extension') GROUP BY PUID ORDER BY TOTAL DESC",  " | ")

   def allExtensionsFrequency(self):
      return self.__listQuery__(
         "SELECT EXT, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') GROUP BY EXT ORDER BY TOTAL DESC", " | ")

   def idmethodFrequencyCount(self):
      return self.__listQuery__(
         "SELECT METHOD, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') GROUP BY METHOD ORDER BY TOTAL DESC", "\n")	
   

   def mimetypeFrequencyCount(self):
      return self.__listQuery__(
         "SELECT MIME_TYPE, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') GROUP BY MIME_TYPE ORDER BY TOTAL DESC", " | ")

   ###
   # List queries
   ###
   def listUniqueBinaryMatchedPUIDS(self):
      return self.__listPUIDSQuery__(
         "SELECT DISTINCT PUID, FORMAT_NAME, FORMAT_VERSION FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (METHOD='Signature' OR METHOD='Container')", "\n")

   def listAllUniqueExtensions(self):	
      return self.__listQuery__(
         "SELECT DISTINCT EXT FROM droid WHERE (TYPE='File' OR TYPE='Container')", " | ")

   def listExtensionOnlyIdentificationPUIDS(self):	
      return self.__listQuery__(		
         "SELECT DISTINCT PUID, FORMAT_NAME FROM droid WHERE (TYPE='File' OR TYPE='Container') AND METHOD='Extension'", " | ")

   def listMultipleIdentifications(self):
      return self.__listQuery__(		
         "SELECT FILE_PATH FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (FORMAT_COUNT!='1' AND FORMAT_COUNT!='0')", "\n")
      return

   def listContainerTypes(self):
      return self.__listQuery__(
         "SELECT DISTINCT URI_SCHEME FROM droid WHERE (TYPE='File' AND URI_SCHEME!='file')", " | ")

   def listNoIdentificationFiles(self):
      return self.__listQuery__(	
         "SELECT FILE_PATH FROM droid WHERE METHOD='no value' AND (TYPE='File' OR TYPE='Container')", "\n")

   def listZeroByteObjects(self):
      return self.__listQuery__(	
         "SELECT FILE_PATH FROM droid WHERE TYPE='File' AND SIZE='0'", "\n")

   def listDuplicateFilenames(self):
      duplicatequery = "SELECT NAME, COUNT(NAME) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') GROUP BY NAME ORDER BY TOTAL DESC"
      result = self.__alternativeFrequencyQuery__(duplicatequery)
      
      duplicatestr = ''
      duplicatelist = []
      totaluniquefilenames = 0
      for r in result:
         count = r[1]
         if count > 1:
            totaluniquefilenames = totaluniquefilenames + 1
            duplicatename = r[0]
            duplicatestr = duplicatestr + "Count: " + str(count) + " , " + "Name: " + duplicatename + '\n'
            duplicatelist.append(duplicatestr)
            duplicatestr = ''
      self.totaluniquefilenames = totaluniquefilenames
      return duplicatelist






   def listDuplicateFilesFromMD5(self):		
      duplicatequery = "SELECT MD5_HASH, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') GROUP BY MD5_HASH ORDER BY TOTAL DESC"
      result = self.__alternativeFrequencyQuery__(duplicatequery)
      
      duplicatestr = ''
      duplicatelist = []
      totalduplicates = 0
      for r in result:
         count = r[1]
         if count > 1:
            totalduplicates = totalduplicates + count
            duplicatemd5 = r[0]
            duplicatestr = "Count: " + str(count) + '\n'
            duplicatestr = duplicatestr + "Duplicate checksum: " + duplicatemd5 + '\n\n'
            duplicatestr = duplicatestr + self.__listDuplicateQuery__("SELECT DIR_NAME, NAME FROM droid WHERE MD5_HASH='" + duplicatemd5 + "' ORDER BY DIR_NAME", "\n\n")
            duplicatelist.append(duplicatestr)
      self.totalmd5duplicates = totalduplicates
      return duplicatelist









   ###
   # Top n listings...
   ###
   def topPUIDS(self, number):
      # Hypothesis: 80% of the effects come from 20% of the causes		

      eightyPercentTotalPUIDs = int(self.identifiedfilecount * 0.80)		# 80 percent figure
      countIdentifiedPuids = "SELECT PUID, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') AND (METHOD='Signature' OR METHOD='Container') GROUP BY PUID ORDER BY TOTAL DESC"
      return self.listTopItems(self.__alternativeFrequencyQuery__(countIdentifiedPuids), number)
      
   def topExts(self, number):
      # Hypothesis: 80% of the effects come from 20% of the causes		

      eightyPercentTotalExts = int(self.filecount * 0.80)		# 80 percent figure
      countExtensions = "SELECT EXT, COUNT(*) AS total FROM droid WHERE (TYPE='File' OR TYPE='Container') GROUP BY EXT ORDER BY TOTAL DESC"
      return self.listTopItems(self.__alternativeFrequencyQuery__(countExtensions), number)

   def listTopItems(self, frequencyQueryResult, number):
      toptwentystr = ''
      
      try:
         for i in range(number):
            label = frequencyQueryResult[i][0]
            count = frequencyQueryResult[i][1]
            toptwentystr = toptwentystr + label + "       count: " + str(count) + "\n"
      except IndexError:
         # No more values we can list so return string as is...
         toptwentystr = toptwentystr
         
      return toptwentystr

   ###
   # Stats output...
   ###
   def calculatePercent(self, total, subset):
      if total > 0:
         percentage = (subset/total)*100
         return '%.1f' % round(percentage, 1)

   ###
   # Additional functions on DB
   ###
   
   def __generatefilenamelist__(self):
      #multi-use variable: get filenames from DB
      countDirs = "SELECT NAME FROM droid"
      self.cursor.execute(countDirs)
      self.fnamelist = self.cursor.fetchall()
      
   def __generatefilenamelistwithdirs__(self):
      countDirs = "SELECT DIR_NAME, NAME FROM droid"
      self.cursor.execute(countDirs)
      self.fdirlist = self.cursor.fetchall()
      
   def msoftfnameanalysis(self):
      charcheck = MsoftFnameAnalysis.MsoftFnameAnalysis()
      fnamereport = []
      #Pass filename to fname analysis
      for d in self.fnamelist:
         fnamestring = d[0]
         checkedname = charcheck.completeFnameAnalysis(fnamestring).encode('utf-8')
         if checkedname != '':
            fnamereport.append(checkedname)
      return fnamereport
                  
   def fileswithspaces(self):
      multiplespacelist = []
      charcheck = RegexFnameAnalysis.RegexFnameAnalysis()
      
      for d in self.fdirlist:
         if len(d) != 2:
            sys.stderr.write("File name, directory list pair is irregular (!=2). Exiting...\n")
            sys.exit(1)
         else:
            fnamestring = d[1]
            if charcheck.detectMultipleSpaces(fnamestring) == True:
               multiplespacelist.append(d)
      return multiplespacelist
         
   def queryDB(self):
      #preliminary functions to generate data from DB
      self.__generatefilenamelist__()
      self.__generatefilenamelistwithdirs__()
   
      self.filecount = self.countFilesQuery()
      self.containercount = self.countContainerObjects()
      self.filesincontainercount = self.countFilesInContainerObjects()
      self.directoryCount = self.countFoldersQuery()
      self.uniqueFileNames = self.countUniqueFileNames()
      self.uniqueDirectoryNames = self.countUniqueDirectoryNames()
      self.identifiedfilecount = self.countIdentifiedQuery()
      self.multipleidentificationcount = self.countMultipleIdentifications()
      self.unidentifiedfilecount = self.countTotalUnidentifiedQuery()
      self.extensionIDOnlyCount = self.countExtensionIDOnly()
      self.distinctSignaturePuidcount = self.countDistinctSignaturePUIDS()
      self.distinctextensioncount = self.countDistinctExtensions()
      self.extmismatchCount = self.countExtensionMismatches()
      
      self.idmethodFrequency = self.idmethodFrequencyCount()
      self.mimetypeFrequency = self.mimetypeFrequencyCount()
      
      self.zeroidcount = self.countZeroID()

      #NOTE: Must be calculated after we have total, and subset values
      self.identifiedPercentage = self.calculatePercent(self.filecount, self.identifiedfilecount)		
      self.unidentifiedPercentage = self.calculatePercent(self.filecount, self.unidentifiedfilecount)

      self.sigIDPUIDList = self.listUniqueBinaryMatchedPUIDS()
      self.sigIDPUIDFrequency = self.identifiedBinaryMatchedPUIDFrequency()
      self.extensionOnlyIDList = self.listExtensionOnlyIdentificationPUIDS()
      self.extensionOnlyIDFrequency = self.extensionOnlyIdentificationFrequency()
      self.uniqueExtensionsInCollectionList = self.listAllUniqueExtensions()
      self.frequencyOfAllExtensions = self.allExtensionsFrequency()
      self.filesWithNoIDList = self.listNoIdentificationFiles()
      
      self.multipleIDList = self.listMultipleIdentifications()
      
      self.duplicatefnamelisting = self.listDuplicateFilenames()
      self.duplicatemd5listing = self.listDuplicateFilesFromMD5()
      self.topPUIDList = self.topPUIDS(5)
      self.topExtensionList = self.topExts(5)		
      self.containertypeslist = self.listContainerTypes()
      
      self.zerobytecount = self.countZeroByteObjects()
      self.zerobytelist = self.listZeroByteObjects()

      self.badFilenames = self.msoftfnameanalysis()
      self.multiplespacelist = self.fileswithspaces()

      #self.printResults()
      self.printHTML()
      
   def printHTML(self):
      self.printMDResults()
      sys.stdout.write(self.htmloutput)
      #document_root = html.fromstring(self.htmloutput)
      #print document_root
      #print(etree.tostring(document_root, encoding='utf-8', pretty_print=True))

   def openDROIDDB(self, dbfilename):
      conn = sqlite3.connect(dbfilename)
      conn.text_factory = str		#encoded as ascii, not unicode / return ascii
      
      self.cursor = conn.cursor()
      self.queryDB()		# primary db query functions
      
      conn.close()