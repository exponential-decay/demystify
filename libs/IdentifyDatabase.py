import sys

class IdentifyDB:

   SQLITE_DB = 'SQLITE 3'
   UNKNOWN_DB = 'unknown'

   #'SQLite format 3'
   sqlite3 = '\x53\x51\x4C\x69\x74\x65\x20\x66\x6F\x72\x6D\x61\x74\x20\x33'

   def identify_export(self, db):   
      dbid = self.UNKNOWN_DB
      f = open(db, 'rb')
      db_magic = f.read(len(self.sqlite3))
      f.close()      
      if db_magic == self.sqlite3:
         dbid = self.SQLITE_DB                 
      return dbid