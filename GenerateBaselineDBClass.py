import sys
import time
import sqlite3

class GenerateBaselineDB:

   IDTABLE = 'idata'
   METADATATABLE = 'dbmd'
   FILEDATATABLE = 'filedata'
   NAMESPACETABLE = 'namespacedata'
   
   #How to create an ID in SQLITE: http://stackoverflow.com/a/9342301
   #FILE ID is a new ID for the purpose of this database
   #ANALYSIS ID is the ID from the input analysis
   #PARENT ID is the ID of the parent of the file, will be a folder
   FILEDATA_TABLE = ["FILE_ID integer primary key","ANALYSIS_ID","PARENT_ID","URI","URI_SCHEME","FILE_PATH","NAME","SIZE","TYPE","EXT","LAST_MODIFIED TIMESTAMP","YEAR INTEGER","HASH"]

   dbname = ''
   timestamp = ''
   cursor = ''

   def __init__(self, export):
      self.dbname = self.getDBFilename(export)
      self.dbsetup()

   def dbsetup(self):
      self.timestamp = self.gettimestamp()
      self.conn = sqlite3.connect(self.dbname)
      self.cursor = self.conn.cursor()   
      self.droptables(self.cursor)
      
      #create a table to hold information about the file only
      self.createfiledatatable()
      
      return self.cursor

   def getcursor(self):
      return self.cursor

   def closedb(self):
      #write MD
      self.createDBMD(self.cursor)

      # Save (commit) the changes
      self.conn.execute("CREATE INDEX HASH ON droid(HASH)");
      self.conn.execute("CREATE INDEX NAME ON droid(NAME)");
      self.conn.execute("CREATE INDEX PUID ON droid(PUID)");

      # Save (commit) the changes
      self.conn.commit()

      # We can also close the connection if we are done with it.
      # TO be sure any changes have been committed or they will be lost.
      self.conn.close()
   
   def getDBFilename(self, export):
      return export.replace(".csv", "") + ".db"

   def sethashtype(self, hash):
      self.hashtype = hash

   def gettimestamp(self):
      return time.strftime('%Y-%m-%dT%H:%M:%S')

   def droptables(self, cursor):
      self.dropDBMDTable(cursor)
      self.dropDROIDTable(cursor)
      self.dropFILEDATATable(cursor)

   def dropTable(self, cursor, tablename):
      #check we have a table to drop
      cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='" + tablename + "';")
      #can't drop something that doesn't exist
      if cursor.fetchone() is not None:
         cursor.execute("DROP table " + tablename + "")	# DROP just in case

   def dropDROIDTable(self, cursor):
      self.dropTable(cursor, 'droid')
      return

   def dropDBMDTable(self, cursor):
      self.dropTable(cursor, self.METADATATABLE)
      
   def dropFILEDATATable(self, cursor):
      self.dropTable(cursor, self.FILEDATATABLE)

   #Database metadata table
   def createDBMD(self, cursor):
      cursor.execute("CREATE TABLE " + self.METADATATABLE + " (TIMESTAMP, HASH_TYPE)")
      cursor.execute("INSERT INTO dbmd VALUES ('" + str(self.timestamp) + "', + '" + str(self.hashtype) + "')")
      
   def createfiledatatable(self):   
      table = 'CREATE TABLE ' + self.FILEDATATABLE + ' ('
      for column in self.FILEDATA_TABLE:
         table = table + str(column) + ","
      table = table.rstrip(',') + ')'
      self.cursor.execute(table)