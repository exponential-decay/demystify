import sys
import time
import sqlite3

class GenerateBaselineDB:

   IDTABLE = 'IDDATA'
   METADATATABLE = 'DBMD'
   FILEDATATABLE = 'FILEDATA'
   NAMESPACETABLE = 'namespacedata'
   ID_JUNCTION = 'IDRESULTS'
   
   #file_id_junction
   FILEID = "FILE_ID"
   IDID = "ID_ID"
   
   #How to create an ID in SQLITE: http://stackoverflow.com/a/9342301
   #FILE ID is a new ID for the purpose of this database
   #INPUT_FILE_ID is the ID from the input analysis
   #PARENT ID is the ID of the parent of the file, will be a folder
   FILEDATA_TABLE = [FILEID,"INPUT_ID","PARENT_ID","URI","URI_SCHEME","FILE_PATH","DIR_NAME","NAME","SIZE","TYPE","EXT","LAST_MODIFIED","YEAR","HASH"]

   #TODO: FORMAT COUNT WILL LIKELY NEED TO BE MOVED TO NAMESPACEDATA BY CREATING A SECOND ID ROW
   IDTABLE_TABLE = [IDID,'NAMESPACE','METHOD','STATUS','ID','BASIS','MIME_TYPE','FORMAT_NAME','FORMAT_VERSION','EXTENSION_MISMATCH','FORMAT_COUNT']

   dbname = ''
   timestamp = ''
   cursor = ''
   hashtype = False

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
      self.createidtable()
      self.createjunctiontable(self.ID_JUNCTION, self.FILEID, self.IDID)
      return self.cursor

   def getcursor(self):
      return self.cursor

   def closedb(self):
      #write MD
      self.createDBMD(self.cursor)

      # Save (commit) the changes
      self.conn.execute("CREATE INDEX HASH ON " + self.FILEDATATABLE + "(HASH)");
      self.conn.execute("CREATE INDEX NAME ON " + self.FILEDATATABLE + "(NAME)");
      self.conn.execute("CREATE INDEX PUID ON " + self.IDTABLE + "(ID)");

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
      self.dropFILEDATATable(cursor)
      self.dropIDTable(cursor)
      self.dropIDJunction(cursor)

   def dropTable(self, cursor, tablename):
      #check we have a table to drop
      cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='" + tablename + "';")
      #can't drop something that doesn't exist
      if cursor.fetchone() is not None:
         cursor.execute("DROP table " + tablename + "")	# DROP just in case

   def dropDBMDTable(self, cursor):
      self.dropTable(cursor, self.METADATATABLE)
      
   def dropFILEDATATable(self, cursor):
      self.dropTable(cursor, self.FILEDATATABLE)

   def dropIDTable(self, cursor):
      self.dropTable(cursor, self.IDTABLE)
      
   def dropIDJunction(self, cursor):
      self.dropTable(cursor, self.ID_JUNCTION)

   #Database metadata table
   def createDBMD(self, cursor):
      cursor.execute("CREATE TABLE " + self.METADATATABLE + " (TIMESTAMP TIMESTAMPE, HASH_TYPE)")
      cursor.execute("INSERT INTO " + self.METADATATABLE + " VALUES ('" + str(self.timestamp) + "', + '" + str(self.hashtype) + "')")
   
   def createfield(self, table, column, type=False):
      if type is not False:
         table = table + str(column) + " " + type + ","
      else:
         table = table + str(column) + ","
      return table
      
   def createfiledatatable(self):   
      table = 'CREATE TABLE ' + self.FILEDATATABLE + ' ('
      for column in self.FILEDATA_TABLE:
         if column == 'LAST_MODIFIED':
            table = self.createfield(table, column, "TIMESTAMP")
         elif column == 'YEAR':
            table = self.createfield(table, column, "INTEGER")
         elif column == 'FILE_ID':
            table = self.createfield(table, column, "integer primary key")
         elif column == 'PARENT_ID' or column == 'INPUT_ID' or column == 'SIZE':
            table = self.createfield(table, column, "integer")
         else:
            table = self.createfield(table, column)      
      table = table.rstrip(',') + ')'
      self.cursor.execute(table)
      
   def createidtable(self):   
      table = 'CREATE TABLE ' + self.IDTABLE + ' ('
      for column in self.IDTABLE_TABLE:
         if column == self.IDID:
            table = self.createfield(table, column, "integer primary key") 
         elif column == 'FORMAT_COUNT' or column == 'NAMESPACE':
            table = self.createfield(table, column, "integer")
         elif column == 'EXTENSION_MISMATCH':
            table = self.createfield(table, column, "boolean")
         else:
            table = self.createfield(table, column)
      table = table.rstrip(',') + ')'
      self.cursor.execute(table)
      
   def createjunctiontable(self, name, pkey1, pkey2):      
      table = 'CREATE TABLE ' + name + '('
      table = table + pkey1 + " INTEGER, "
      table = table + pkey2 + " INTEGER, "
      table = table + "PRIMARY KEY (" + pkey1 + "," + pkey2 + ")"
      table = table.rstrip(',') + ')'
      self.cursor.execute(table)