import sys
from ToolMappingClass import ToolMapping
from SFHandlerClass import SFYAMLHandler

class SFLoader:

   basedb = ''
   identifiers = ''   

   def __init__(self, basedb):
      self.basedb = basedb

   def insertfiledbstring(self, keys, values):
      insert = "INSERT INTO " + self.basedb.FILEDATATABLE
      return insert + "(" + keys.strip(", ") + ") VALUES (" + values.strip(", ") + ");"

   def insertiddbstring(self, keys, values):
      insert = "INSERT INTO " + self.basedb.IDTABLE
      return insert + "(" + keys.strip(", ") + ") VALUES (" + values.strip(", ") + ");"

   def file_id_junction_insert(self, file, id):
      return "INSERT INTO " + self.basedb.ID_JUNCTION + "(" + self.basedb.FILEID + "," \
               + self.basedb.IDID + ") VALUES (" + str(file) + "," + str(id) + ");"

   def handleID(self, idsection, idkeystring, idvaluestring):
      idk = []
      idv = []
      for x in self.identifiers:
         for key, value in idsection[x].items():
            if key in ToolMapping.SF_ID_MAP:
               idkeystring = idkeystring + ToolMapping.SF_ID_MAP[key] + ", "
               idvaluestring = idvaluestring + "'" + str(value) + "', "
            #unmapped: Basis and Warning
         idk.append(idkeystring)
         idv.append(idvaluestring)
         idkeystring = ''
         idvaluestring = ''
      return idk, idv
      
   def sfDBSetup(self, sfexport, cursor):
      sf = SFYAMLHandler()
      sf.readSFYAML(sfexport)
      
      sfdata = sf.sfdata

      sf.addfilename(sfdata)
      sf.adddirname(sfdata)
      sf.addYear(sfdata)

      self.identifiers = sf.getIdentifiersList()
      files = sf.getFiles()

      #Awkward structure to navigate
      #sf.sfdata['header']
      #sf.sfdata['files']
      #sf.sfdata['files'][0]['identification']

      for f in files:
         filekeystring = ''
         filevaluestring = ''
         idkeystring = ''
         idvaluestring = ''
         for key, value in f.items():
            if key in ToolMapping.SF_FILE_MAP:
               filekeystring = filekeystring + ToolMapping.SF_FILE_MAP[key] + ", "
               filevaluestring = filevaluestring + "'" + str(value) + "', "
            else:
               #understand what to do with errors in SF output
               if key == 'errors':
                  if value != '':
                     sys.stderr.write("LOG: " + value + "\n")
               if key == sf.DICTID:
                  idkey, idvalue = self.handleID(value, idkeystring, idvaluestring)

      
         cursor.execute(self.insertfiledbstring(filekeystring, filevaluestring))         
         fileid = cursor.lastrowid

         insert = []  
         for x in range(len(idkey)):
            insert.append(self.insertiddbstring(''.join(idkey[x]), ''.join(idvalue[x])))

         rowlist = []
         for i in insert:
            cursor.execute(i)
            rowlist.append(cursor.lastrowid)

         for rowid in rowlist:
            cursor.execute(self.file_id_junction_insert(fileid,rowid))

