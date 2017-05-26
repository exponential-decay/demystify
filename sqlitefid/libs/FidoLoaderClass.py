# -*- coding: utf-8 -*-
import sys
from ToolMappingClass import ToolMapping
from CSVHandlerClass import *
import tempfile

class FidoLoader:

   fidoheader = "info.status,info.time,info.puid,info.formatname,info.signaturename,info.filesize,info.filename,info.mimetype,info.matchtype"
   basedb = ''

   def __init__(self, basedb):
      self.basedb = basedb

   #need a temporary fild with fido headers
   def createtmpfile(self, fidoexport):
      tmpfile = tempfile.NamedTemporaryFile()
      with open(fidoexport, 'rb') as csvfile:
         for i, row in enumerate(csvfile):
            #add fido header
            if i == 0:
               tmpfile.write(self.fidoheader + "\n")
               tmpfile.write(row)
            else:
               tmpfile.write(row)
      tmpfile.seek(0)
      return tmpfile

   def fidoDBSetup(self, fidoexport, cursor):
      sys.stdout.write("Placeholder Code: Currently not handling FIDO exports." + "\n") 
      if fidoexport != False:
         tmpfile = self.createtmpfile(fidoexport)
         fidocsvhandler = genericCSVHandler()
         fidolist = fidocsvhandler.csvaslist(tmpfile.name)
         tmpfile.close()
