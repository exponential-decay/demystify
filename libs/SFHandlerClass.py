# -*- coding: utf-8 -*-
# we don't import YAML handler for this 
# as no standard PYTHON handler library
import os.path
import urllib
import codecs
from urlparse import urlparse, urljoin
from PyDateHandler import PyDateHandler

class SFYAMLHandler:

   def __init__(self):
      #date handler class   
      self.pydate = PyDateHandler()
   
   sectioncount = 0
   identifiercount = 0
   
   YAMLSECTION = "---"
   YAMLNAMESPACE = 'name'
   YAMLDETAILS = 'details'

   header = {}

   HEADDETAILS = 'id details '
   HEADNAMESPACE = 'id namespace '
   HEADCOUNT = 'identifier count'

   FILERECORDLEN = 6

   #structures for holding formst information
   filedetails = {}
   iddetails = {}

   #all files in report
   files = []

   hashtype = None

   hashes = ['md5', 'sha1', 'sha256', 'sha512', 'crc']
   fileheaders = ['filename', 'filesize', 'modified', 'errors', 'md5', 'sha1', 'sha256', 'sha512', 'crc']
   iddata = ['ns', 'id', 'format', 'version', 'mime', 'basis', 'warning']
   containers = {'zip': 'x-fmt/263', 'gz': 'x-fmt/266', 'tar': 'x-fmt/265', 'warc': 'fmt/289'}
   
   mismatch_warning = 'extension mismatch'
   filename_only = 'match on filename only' 
   extension_only_one = 'match on extension only' 
   extension_only_two = 'extension match'

   text_basis = 'text match'
   byte_basis = 'byte match'
   container_basis_one = 'container match'
   container_basis_two = 'container name'
   xml_basis = 'xml match'   

   PROCESSING_ERROR = -1
   filecount = 0
   
   sfdata = {}
   DICTHEADER = 'header'
   DICTFILES = 'files'
   DICTID = 'identification'

   TYPECONT = 'Container'
   TYPEFILE = 'File'
   
   #additional fields given to SF output
   FIELDFILENAME = 'filename'
   FIELDURI = 'uri'
   FIELDURISCHEME = 'uri scheme'
   FIELDDIRNAME = 'directory'
   FIELDYEAR = 'year'
   FIELDCONTTYPE = 'containertype'
   FIELDTYPE = 'type'
   FIELDMETHOD = 'method'
   FIELDMISMATCH = 'extension mismatch'
   FIELDEXT = 'ext'
   FIELDVERSION = 'version'

   def getHeaders(self):
      return self.sfdata[self.DICTHEADER]

   def getIdentifiersList(self):
      namespaces = []
      ids = self.sfdata[self.DICTHEADER][self.HEADCOUNT]
      for x in range(ids):
         namespaces.append(self.sfdata[self.DICTHEADER][self.HEADNAMESPACE + str(x+1)]) 
      return namespaces

   def getFiles(self):
      return self.sfdata[self.DICTFILES]

   def stripkey(self, line):
      line = line.strip()
      line = line.replace('- ', '')
      return line

   def stripvalue(self, line):
      line = line.strip()
      line = line.lstrip("'").rstrip("'")
      return line

   def handleentry(self, line):
      line = line.split(':', 1)
      line[0] = self.stripkey(line[0])
      line[1] = self.stripvalue(line[1])
      return line

   def headersection(self, line):
      if line != self.YAMLSECTION:
         line = self.handleentry(line)
         if line[0] == self.YAMLNAMESPACE:
            self.identifiercount+=1
            ns = self.HEADNAMESPACE + str(self.identifiercount)
            self.header[ns] = line[1]
         elif line[0] == self.YAMLDETAILS:
            details = self.HEADDETAILS + str(self.identifiercount)
            self.header[details] = line[1]   
            self.header[self.HEADCOUNT] = self.identifiercount
         elif line[0] != 'identifiers':
            self.header[line[0]] = line[1]

   def filesection(self, sfrecord):
      iddict = {}    # { nsname : {id : x, mime : x } }  
      filedict = {}
      
      ns = ''
      iddata = {}
      
      for s in sfrecord:
         s = self.handleentry(s)
         if s[0] in self.fileheaders:
            filedict[s[0]] = s[1]  
            if s[0] == self.FIELDFILENAME:
               fname = filedict[self.FIELDFILENAME]
               furi = self.addFileURI(fname)
               for f in self.files:
                  needle_name = f[self.FIELDFILENAME]
                  needle_type = f[self.FIELDTYPE]
                  haystack = fname
                  if needle_name in haystack:
                     if needle_type == self.TYPECONT:
                        furi = self.addContainerURI(f, filedict, furi)                      
               filedict[self.FIELDURI] = furi
               filedict[self.FIELDURISCHEME] = self.geturischeme(furi)
            if s[0] in self.hashes and self.hashtype == False:
               self.hashtype = s[0]

         if s[0] in self.iddata:         
            #-------------------------------------------------------------#
            #TRIGGER: add data to dict on NS as a trigger, create new dict#
            #-------------------------------------------------------------# 
            if s[0] == 'ns':
               if len(iddata) > 0:
                  if self.FIELDVERSION not in iddata:
                     iddata[self.FIELDVERSION] = ''
                  iddict[ns] = iddata
                  iddata = {}
               ns = s[1]     
            #-------------------------------------------------------------#
            #TRIGGER: add data to dict on NS as a trigger, create new dict#
            #-------------------------------------------------------------#           
            else:
               if s[0] == 'id':
                  self.getContainers(s[1], filedict)
               if s[0] == 'basis':
                  if s[1] == '':
                     s[1] = None
                  self.getMethod(s[1], iddata)
               if s[0] == 'warning':
                  if s[1] == '':
                     s[1] = None
                  self.getMethod(s[1], iddata, filedict, True)
                  self.getMismatch(s[1], iddata)
               if s[0] == 'mime':
                  if s[1] == 'UNKNOWN' or s[1] == '':
                     s[1] = 'none'
               iddata[s[0]] = s[1]

      if self.FIELDVERSION not in iddata:
         iddata[self.FIELDVERSION] = ''
      
      #on loop completion add final id record
      iddict[ns] = iddata
      
      #add complete id data to filedata, return
      filedict[self.DICTID] = iddict
      return filedict

   def readSFYAML(self, sfname):
      processing = False
      filedata = []
      with codecs.open(sfname, encoding='utf-8') as sfile:
         for line in sfile: 
            line = line.strip()
            if line == self.YAMLSECTION:
               self.sectioncount += 1
               # new section so handle appropriately 
               processing = False
            if self.sectioncount == 1:
               self.headersection(line)
            elif self.sectioncount > 1:
               if processing == False and len(filedata) > 0:
                  self.files.append(self.filesection(filedata))
                  filedata = []
               else:
                  processing = True
                  if line != self.YAMLSECTION: 
                     filedata.append(line)
      
      #Add final section of data to list
      if len(filedata) > 0:         
         self.files.append(self.filesection(filedata))
      
      #Attempt at useful return value - number of files processed vs. processing error
      if len(self.files) == self.sectioncount - 1:
         self.filecount = len(self.files)
      else:
         self.filecount = self.PROCESSING_ERROR
      
      #concatenate header and file details (not needed, but maybe convenient)
      self.sfdata[self.DICTHEADER] = self.header
      self.sfdata[self.DICTFILES] = self.files      
      return self.filecount

   def getMismatch(self, warning, iddata):
      if warning is not None:
         if self.mismatch_warning in warning:
            iddata[self.FIELDMISMATCH] = True
         else:
            iddata[self.FIELDMISMATCH] = False

   def getMethod(self, basis, iddata, filedict=False, warning=False):
      if warning is False and basis != None:
         if self.container_basis_one in basis or self.container_basis_two in basis:
            iddata[self.FIELDMETHOD] = 'Container'
         elif self.byte_basis in basis:
            iddata[self.FIELDMETHOD] = 'Signature'
         elif self.xml_basis in basis:
            iddata[self.FIELDMETHOD] = 'XML'
         elif self.text_basis in basis:
            iddata[self.FIELDMETHOD] = 'Text'
         elif self.extension_only_two in basis:
            iddata[self.FIELDMETHOD] = 'Extension'
         else: 
            iddata[self.FIELDMETHOD] = ''
         
      if warning is True and basis != None: 
         if self.filename_only in basis:
            method = 'Filename'
         elif self.extension_only_one in basis:
            method = 'Extension'     
         else:
            #warning comes after basis in SF report
            #posit: at this point anything else is not 
            #really an identification at all 
            method = 'None' 
         if self.FIELDMETHOD not in iddata: 
            iddata[self.FIELDMETHOD] = method

   def getDirName(self, filepath):
      return os.path.dirname(filepath)   

   def getFileName(self, filepath):
      fname = os.path.basename(filepath)
      if len(fname) == len(filepath):
         #retrieving filename probably didn't work... maybe windows path
         import ntpath  #imported in Windows when OS is imported
         fname = ntpath.basename(filepath)
      return os.path.basename(fname)
   
   def adddirname(self, sfdata):
      for row in sfdata[self.DICTFILES]:
         fname = row[self.FIELDFILENAME]
         row[self.FIELDDIRNAME] = self.getDirName(fname) 
      return sfdata

   def addfilename(self, sfdata):
      for row in sfdata[self.DICTFILES]:
         fname = row[self.FIELDFILENAME]
         row['name'] = self.getFileName(fname)
      return sfdata

   def addYear(self, sfdata):
      for row in sfdata[self.DICTFILES]:
         year = row['modified']
         row[self.FIELDYEAR] = self.getYear(year)
      return sfdata
      
   def getYear(self, datestring):
      return self.pydate.getYear(datestring)

   def getContainers(self, id, filedict):
      #only set as File if and only if it isn't a Container
      #container overrides all...
      if id in self.containers.values():
         filedict[self.FIELDTYPE] = self.TYPECONT
         #get container type: http://stackoverflow.com/a/13149770
         filedict[self.FIELDCONTTYPE] = self.containers.keys()[self.containers.values().index(id)]
      else:
         if self.FIELDTYPE in filedict:
            if filedict[self.FIELDTYPE] != self.TYPECONT:
               filedict[self.FIELDTYPE] = self.TYPEFILE
         else: 
            filedict[self.FIELDTYPE] = self.TYPEFILE 

   def addFileURI(self, fname):
      fname = fname.replace("\\","/")
      test = urllib.pathname2url(fname.encode('utf-8'))
      fname = urljoin('file:', test)

      #decode to match droid/sf output
      fname = urllib.unquote(fname).decode('utf-8')
      return fname

   def addContainerURI(self, container, containedfile, fname):
      fname = fname
      fname = container[self.FIELDCONTTYPE] + ":" + fname 
      fname = fname.replace(container[self.FIELDFILENAME], container[self.FIELDFILENAME] + "!")
      return fname

   def geturischeme(self, fname):
      return urlparse(fname).scheme

   def addExt(self, sfdata):
      for row in sfdata[self.DICTFILES]:
         name = row['name'].rsplit('.', 1)
         if len(name) == 2:
            row[self.FIELDEXT] = name[1]
         else:       
            row[self.FIELDEXT] = ''  #no extension...          
      return sfdata
