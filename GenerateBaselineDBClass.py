import sys
import time
import sqlite3

class GenerateBaselineDB:

   dbname = ''
   timestamp = ''

   def __init__(self, export):
      self.dbname = self.getDBFilename(export)

   def dbsetup(self):
      self.timestamp = self.gettimestamp()

      self.conn = sqlite3.connect(self.dbname)
      cursor = self.conn.cursor()   
      self.droptables(cursor)
      return cursor

   def droptables(self, cursor):
      self.dropDBMDTable(cursor)
      self.dropDROIDTable(cursor)

   def closedb(self, cursor):
      #write MD
      self.createDBMD(cursor)

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
      self.dropTable(cursor, 'dbmd')

   #Database metadata table
   def createDBMD(self, cursor):
      cursor.execute("CREATE TABLE dbmd (TIMESTAMP, HASH_TYPE)")
      cursor.execute("INSERT INTO dbmd VALUES ('" + str(self.timestamp) + "', + '" + str(self.hashtype) + "')")

