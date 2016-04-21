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
   NS_NAME = 'pronom'
   NS_ID = 0
   NS_DETAILS = 'droid'    #to be overwritten by filename
         
   def __init__(self, basedb, BOM=False):
      self.basedb = basedb
      self.BOM = BOM
      self.basedb.tooltype = 'droid'
   
   def insertfiledbstring(self, keys, values):
      insert = "INSERT INTO " + self.basedb.FILEDATATABLE
      return insert + "(" + keys.strip(", ") + ") VALUES (" + values.strip(", ") + ");"

   def insertiddbstring(self, keys, values):
      insert = "INSERT INTO " + self.basedb.IDTABLE
      return insert + "(" + keys.strip(", ") + ") VALUES (" + values.strip(", ") + ");"

   def file_id_junction_insert(self, file, id):
      return "INSERT INTO " + self.basedb.ID_JUNCTION + "(" + self.basedb.FILEID + "," \
               + self.basedb.IDID + ") VALUES (" + str(file) + "," + str(id) + ");"

   def populateIDTable(self, formats, method, status, mismatch):
      add_fields = ['METHOD', 'STATUS', 'NS_ID', 'EXTENSION_MISMATCH']
      add_values = ['"' + method + '"', '"' + status + '"', '"' + str(self.NS_ID) + '"', '"' + str(mismatch) + '"']
      idvaluelist = []
      idkeylist = []
      idkeystring = ''
      idvaluestring = ''
      for format in formats:
         idkeystring = ', '.join(format.keys()).split(',') + add_fields
         idvaluestring = ', '.join(format.values()).split(',') + add_values
         idvaluelist.append(idvaluestring)
         idkeylist.append(idkeystring)
      return idkeylist, idvaluelist

   def setupNamespaceConstants(self, cursor, filename):
      self.NS_DETAILS = filename
      insert = "INSERT INTO " + self.basedb.NAMESPACETABLE + " (" + "NS_NAME" + ", " \
                  + "NS_DETAILS" + ") VALUES ('" + self.NS_NAME + "', '" + self.NS_DETAILS + "');"
      cursor.execute(insert)
      return cursor.lastrowid 

   def droidDBSetup(self, droidcsv, cursor):
      self.NS_ID = self.setupNamespaceConstants(cursor, droidcsv)

      if droidcsv != False:
         droidcsvhandler = droidCSVHandler()
         droidlist = droidcsvhandler.readDROIDCSV(droidcsv, self.BOM)

      droidlist = droidcsvhandler.addurischeme(droidlist)
      droidlist = droidcsvhandler.addYear(droidlist)
      droidlist = droidcsvhandler.adddirname(droidlist)

      for file in droidlist:
         filekeystring = ''
         filevaluestring = ''
         idkeystring = ''
         idvaluestring = ''
         
         #FIELDS FOR MULTIPLE ID FIELDS
         METHOD = file['METHOD']
         if METHOD == '':
            METHOD = 'None'            
         STATUS = file['STATUS']
         MISMATCH = file['EXTENSION_MISMATCH']
         if MISMATCH == 'true':
            MISMATCH = '1'
         else:
            MISMATCH = '0'

         MULTIPLE = False
         if int(file['FORMAT_COUNT']) > 1:
            MULTIPLE = True
         MULTIPLE_DONE = False

         for key, value in file.items():
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
                  if MULTIPLE_DONE == False:
                     MULTIPLE_KEY_LIST, MULTIPLE_VALUE_LIST = self.populateIDTable(file[droidcsvhandler.DICT_FORMATS], METHOD, STATUS, MISMATCH)
                     MULTIPLE_DONE = True    #don't loop around this more than is needed
         
         id = None
         file = None
                      
         if filekeystring != '' and filevaluestring != '':
            cursor.execute(self.insertfiledbstring(filekeystring, filevaluestring))         
            file = cursor.lastrowid
         
         if MULTIPLE != True:
            if idkeystring != '' and idvaluestring != '':
               idkeystring = idkeystring + 'NS_ID'
               idvaluestring = idvaluestring + '"' + str(self.NS_ID) + '"'
               cursor.execute(self.insertiddbstring(idkeystring, idvaluestring))
               id = (cursor.lastrowid)

            if id != None and file != None:
               cursor.execute(self.file_id_junction_insert(file,id))
         else:
            for i,v in enumerate(MULTIPLE_KEY_LIST):
               insert = self.insertiddbstring(', '.join(v), ', '.join(MULTIPLE_VALUE_LIST[i]))
               cursor.execute(insert)
               id = cursor.lastrowid               
               if file != None:
                  cursor.execute(self.file_id_junction_insert(file,id))
