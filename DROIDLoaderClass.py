import os
import sys 
import sqlite3
import hashlib
import datetime
import csv
from urlparse import urlparse

class DROIDLoader:

   basedb = ''

   #18 columns total...
   DROID_FILEDATA_TABLE = ["ID","PARENT_ID","URI","FILE_PATH","NAME","SIZE","TYPE","EXT","LAST_MODIFIED","HASH"]
   DROID_IDENTIFICATION = ['METHOD','STATUS','EXTENSION_MISMATCH','FORMAT_COUNT','PUID','MIME_TYPE','FORMAT_NAME','FORMAT_VERSION']

   

   csvcolumncount = 0
   hashtype = 0

   #DROID SPECIFIC COLUMN INDEXES
   #zer0-based index
   URI_COL = 2
   PATH_COL = 3
   DATE_COL = 10
   
   BOMLEN = len("\xEF\xBB\xBF")
   
   #avoid overflow for multiple-ids (better way possible?)
   LAST_COL = 18
   
   def __init__(self, basedb, BOM=False):
      #basedb here as we still add information to the metadata table midway
      self.basedb = basedb
      self.BOM=BOM
   
   def createDROIDTable(self, cursor, csvcolumnheaders):
      # turn csv headers list into a csv string, write query, create table

      self.csvcolumncount = len(csvcolumnheaders)
      columns = ""
      for header in csvcolumnheaders:
         if header == "URI":
            columns = columns + header + ", " + "URI_SCHEME, "
            self.csvcolumncount+=1
         elif header == "FILE_PATH":
            columns = columns + header + ", " + "DIR_NAME, "
            self.csvcolumncount+=1
         elif "_HASH" in header:    #regex alternative: ^([[:alnum:]]*)(_HASH)$
            self.basedb.sethashtype(header.split('_', 1)[0])
            columns = columns + "HASH" + ", "
         elif header == "LAST_MODIFIED":
            columns = columns + header + " TIMESTAMP" + ","
            columns = columns + "YEAR INTEGER" + ","
         else:
            #sys.stderr.write(header + "\n")
            columns = columns + header + ", "

      cursor.execute("CREATE TABLE droid (" + columns[:-2] + ")")
      return True

   def droidDBSetup(self, droidcsv, cursor):

      with open(droidcsv, 'rb') as csvfile:
      
         #we ignore the first three bytes (BOM) and read-on
         if self.BOM == True:
            csvfile.seek(self.BOMLEN)
            
         droidreader = csv.reader(csvfile)
         
         #for row in DROID reader:
         #   print row
         

   def _droidDBSetup(self, droidcsv, cursor):

      with open(droidcsv, 'rb') as csvfile:
      
         #we ignore the first three bytes (BOM) and read-on
         if self.BOM == True:
            csvfile.seek(self.BOMLEN)
      
         droidreader = csv.reader(csvfile)
         
         
         for row in droidreader:
            if droidreader.line_num == 1:		# not zero-based index
               tablequery = self.createDROIDTable(cursor, row)
            else:
               rowstr = ""	
               for i,item in enumerate(row[0:self.csvcolumncount-1]):

                  if i != self.LAST_COL:  #avoid overrun of columns when multi-id occurs
                     
                     if item == "":
                        rowstr = rowstr + ',"no value"'
                     else:
                        rowstr = rowstr + ',"' + item + '"'
                                    
                     if i == self.URI_COL:
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
                           rowstr = rowstr + ',"' + "no value" + '"'

               cursor.execute("INSERT INTO droid VALUES (" + rowstr.lstrip(',') + ")")
