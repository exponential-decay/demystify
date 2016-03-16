import sys
import sqlite3

class GenerateBaselineDB:

   def getDBFilename(self, export):
      return export.replace(".csv", "") + ".db"
