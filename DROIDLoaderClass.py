import os
import sys 
import sqlite3
import hashlib
import datetime
import csv
from urlparse import urlparse
from ToolMappingClass import ToolMapping
from CSVHandlerClass import *

class DROIDLoader:

   basedb = ''
   BOM = False
         
   def __init__(self, basedb, BOM=False):
      self.basedb = basedb
      self.BOM = BOM
   
   def insertfiledbstring(self, keys, values):
      insert = "INSERT INTO " + self.basedb.FILEDATATABLE
      return insert + "(" + keys.strip(", ") + ") VALUES (" + values.strip(", ") + ");"

   def insertiddbstring(self, keys, values):
      insert = "INSERT INTO " + self.basedb.IDTABLE
      return insert + "(" + keys.strip(", ") + ") VALUES (" + values.strip(", ") + ");"

   def file_id_junction_insert(self, file, id):
      return "INSERT INTO " + self.basedb.ID_JUNCTION + "(" + self.basedb.FILEID + "," \
               + self.basedb.IDID + ") VALUES (" + str(file) + "," + str(id) + ");"

   def droidDBSetup(self, droidcsv, cursor):

      if droidcsv != False:
         droidcsvhandler = droidCSVHandler()
         droidlist = droidcsvhandler.readDROIDCSV(droidcsv, self.BOM)

      #droidlist = droidcsvhandler.addurischeme(droidlist)
      #droidlist = droidcsvhandler.addYear(droidlist)
      #droidlist = droidcsvhandler.adddirname(droidlist)

      for x in droidlist:
         filekeystring = ''
         filevaluestring = ''
         idkeystring = ''
         idvaluestring = ''

         MULTIPLE = False
         if int(x['FORMAT_COUNT']) > 1:
            MULTIPLE = True

         for key, value in x.items():
            if key != 'FORMAT_COUNT':
               if key == "MIME_TYPE" or key == "METHOD":
                  if value == '':
                     value = 'None'
               if self.basedb.hashtype == False:
                  if "_HASH" in key:
                     self.basedb.hashtype = key.split('_', 1)[0]
                  elif key == "HASH":
                     #no hash used in export
                     self.basedb.hashtype = "None"
               if key in ToolMapping.DROID_FILE_MAP:
                  filekeystring = filekeystring + ToolMapping.DROID_FILE_MAP[key] + ", "
                  filevaluestring = filevaluestring + "'" + value + "', "
               if MULTIPLE == False:
                  if key in ToolMapping.DROID_ID_MAP:
                     if key == 'EXTENSION_MISMATCH':
                        if value == 'true':
                           value = "1"
                        elif value == 'false':
                           value = "0"
                     idkeystring = idkeystring + ToolMapping.DROID_ID_MAP[key] + ", "
                     idvaluestring = idvaluestring + "'" + value + "', "
               else:
                  #self.pupulateNSTable()
                  print x[droidcsvhandler.DICT_FORMATS]
         
         id = None
         file = None
                      
         if filekeystring != '' and filevaluestring != '':
            cursor.execute(self.insertfiledbstring(filekeystring, filevaluestring))         
            file = cursor.lastrowid
         
         if idkeystring != '' and idvaluestring != '':
            cursor.execute(self.insertiddbstring(idkeystring, idvaluestring))
            id = (cursor.lastrowid)

         if id != None and file != None:
            cursor.execute(self.file_id_junction_insert(file,id))
