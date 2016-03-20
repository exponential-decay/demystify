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
   hashtype = ''
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

      droidlist = droidcsvhandler.addurischeme(droidlist)
      droidlist = droidcsvhandler.addYear(droidlist)

      for x in droidlist:
         filekeystring = ''
         filevaluestring = ''
         idkeystring = ''
         idvaluestring = ''
         for key, value in x.items():
         
            #print key
         
            if key in ToolMapping.FILE_MAP:
               filekeystring = filekeystring + ToolMapping.FILE_MAP[key] + ", "
               filevaluestring = filevaluestring + "'" + value + "', "
            if key in ToolMapping.DROID_ID_MAP:
               idkeystring = idkeystring + ToolMapping.DROID_ID_MAP[key] + ", "
               idvaluestring = idvaluestring + "'" + value + "', "

         cursor.execute(self.insertfiledbstring(filekeystring, filevaluestring))         
         file = cursor.lastrowid
         
         cursor.execute(self.insertiddbstring(idkeystring, idvaluestring))
         id = (cursor.lastrowid)

         cursor.execute(self.file_id_junction_insert(file,id))

   def _droidDBSetup(self, droidcsv, cursor):

      with open(droidcsv, 'rb') as csvfile:
      
         droidreader = csv.reader(csvfile)

         for row in droidreader:
            #if droidreader.line_num == 1:		# not zero-based index
            #   tablequery = self.createDROIDTable(cursor, row)
            #else:
            rowstr = ""	
            for i,item in enumerate(row[0:18-1]):

               if i != 18:  #avoid overrun of columns when multi-id occurs
                  
                  if item == "":
                     rowstr = rowstr + ',"no value"'
                  else:
                     rowstr = rowstr + ',"' + item + '"'
                                    
                     '''if i == self.URI_COL:
                        url = item
                        rowstr = rowstr + ',"' + urlparse(url).scheme + '"'

                     if i == self.PATH_COL:
                        dir = item
                        rowstr = rowstr + ',"' + os.path.dirname(item) + '"'		

                     if i == self.DATE_COL:
                        if item is not '':
                           datestring = item
                           #split at '+' if timezone is there, we're only interested in year
                           dt = datetime.datetime.strptime(datestring.split('+', 1)[0], '%Y-%m-%dT%H:%M:%S')
                           rowstr = rowstr + ',"' + str(dt.year) + '"'
                        else:
                           rowstr = rowstr + ',"' + "no value" + '"'''
               
               #print rowstr
               #cursor.execute("INSERT INTO droid VALUES (" + rowstr.lstrip(',') + ")")
