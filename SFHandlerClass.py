# -*- coding: utf-8 -*-
# we don't import YAML handler for this 
# as no standard PYTHON handler library

class SFYaml:
   
   sectioncount = 0
   identifiercount = 0
   
   YAMLSECTION = "---"
   YAMLNAMESPACE = 'name'
   YAMLDETAILS = 'details'

   header = {}

   HEADDETAILS = 'id_details'
   HEADNAMESPACE = 'id_namespace'
   HEADCOUNT = 'identifier_count'

   FILERECORDLEN = 6

   #structures for holding formst information
   filedetails = {}
   iddetails = {}

   #all files in report
   files = []

   fileheaders = ['filename', 'filesize', 'modified', 'errors', 'md5', 'sha1', 'sha256', 'sha512', 'crc']
   iddata = ['ns', 'id', 'format', 'version', 'mime', 'basis', 'warning']

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
      for s in sfrecord:
         s = self.handleentry(s)
         if s[0] in self.fileheaders:
            print s[0] + " is file data."   
         if s[0] in self.iddata:
            print s[0] + " is identification data."
            #if s[0] == 'ns':
               
         #ignore 'matches'

   def sfaslist(self, sfname):
      processing = False
      filedata = []
      with open(sfname, 'rb') as sfile:
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
                  self.filesection(filedata) 
                  filedata = []
               else:
                  processing = True
                  if line != self.YAMLSECTION: 
                     filedata.append(line)

      #print self.header
