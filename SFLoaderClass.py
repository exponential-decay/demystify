import sys
from ToolMappingClass import ToolMapping
from SFHandlerClass import SFYAMLHandler

class SFLoader:

   basedb = ''
   identifiers = ''   

   def __init__(self, basedb):
      self.basedb = basedb
      self.basedb.tooltype = 'siegfried'

   def insertfiledbstring(self, keys, values):
      insert = "INSERT INTO " + self.basedb.FILEDATATABLE
      return insert + "(" + keys.strip(", ") + ") VALUES (" + values.strip(", ") + ");"

   def insertiddbstring(self, keys, values):
      insert = "INSERT INTO " + self.basedb.IDTABLE
      return insert + "(" + keys.strip(", ") + ") VALUES (" + values.strip(", ") + ");"

   def file_id_junction_insert(self, file, id):
      return "INSERT INTO " + self.basedb.ID_JUNCTION + "(" + self.basedb.FILEID + "," \
               + self.basedb.IDID + ") VALUES (" + str(file) + "," + str(id) + ");"

   def addDirsToDB(self, dirs, cursor):
      for d in dirs:
         if '/' not in d:
            name = d.rsplit('\\',1)
         else:
            name = d.rsplit('/',1)
         if len(name) == 2:
            name = name[1]
         else:
            name = d            
         insert = "INSERT INTO " + self.basedb.FILEDATATABLE + " (" + 'FILE_PATH, DIR_NAME, NAME,SIZE, TYPE' + ")" \
            + "VALUES ('" + d + "','" + d + "','" + name + "',0,'Folder'" + ");"
         cursor.execute(insert)

   def handleID(self, idsection, idkeystring, idvaluestring, nsdict):
      idk = []
      idv = []
      for x in self.identifiers:
         for key, value in idsection[x].items():
            if key in ToolMapping.SF_ID_MAP:
               idkeystring = idkeystring + ToolMapping.SF_ID_MAP[key] + ", "
               idvaluestring = idvaluestring + "'" + str(value) + "', "
            #unmapped: Basis and Warning
         if x in nsdict:
            idkeystring = idkeystring + self.basedb.NSID 
            idvaluestring = idvaluestring + str(nsdict[x])
         else:
            sys.stderr.write("LOG: Issue with namespace dictionary table.")
         idk.append(idkeystring.strip(", "))
         idv.append(idvaluestring.strip(", "))
         idkeystring = ''
         idvaluestring = ''
      return idk, idv

   def populateNStable(self, sf, cursor, header):
      nsdict = {}
      #N.B. Not handling: sig.sig name
      #N.B. Not handling: scandate
      #N.B. Not handling: siegfried version
      count = header[sf.HEADCOUNT]
      nstext = sf.HEADNAMESPACE
      detailstext = sf.HEADDETAILS
      for h in range(count):
         no = h+1
         ns = nstext + str(no)
         details = detailstext + str(no)

         #NSID is integer primary key == rowid()
         insert = "INSERT INTO " + self.basedb.NAMESPACETABLE + "(" + 'NS_NAME' + ", " \
               + 'NS_DETAILS' + ") VALUES ('" + str(header[ns]) + "', '" + str(header[details]) + "');"

         cursor.execute(insert)
         nsdict[str(header[ns])] = cursor.lastrowid 
      return nsdict

   #find all unique directory values in listing...
   def handledirectories(self, dirs, sf, count=False):
      newlist = []
      dirset = set(dirs)
      for d in dirset:
         newlist.append(sf.getDirName(d))
      newlist = set(newlist)                 #make newlist unique
      dirset = list(dirset) + list(newlist)  #concatenate unique sets as lists
      if count == False:
         return self.handledirectories(dirset, sf, len(dirset))
      else:
         if len(dirset) != count:
            return self.handledirectories(dirset, sf, len(dirset))
         else:
            return dirset
         
   def sfDBSetup(self, sfexport, cursor):
      sf = SFYAMLHandler()
      sf.readSFYAML(sfexport)
      
      sfdata = sf.sfdata

      sf.addfilename(sfdata)
      sf.adddirname(sfdata)
      sf.addYear(sfdata)
      sf.addExt(sfdata)

      self.identifiers = sf.getIdentifiersList()
      nsdict = self.populateNStable(sf, cursor, sf.getHeaders())      

      dirlist = []

      #Awkward structures to navigate----------#
      #sf.sfdata['header']                     #
      #sf.sfdata['files']                      #
      #sf.sfdata['files'][0]['identification'] #
      #----------------------------------------#
      for f in sf.getFiles():
         filekeystring = ''
         filevaluestring = ''
         idkeystring = ''
         idvaluestring = ''
         for key, value in f.items():
            if key in ToolMapping.SF_FILE_MAP:
               filekeystring = filekeystring + ToolMapping.SF_FILE_MAP[key] + ", "
               filevaluestring = filevaluestring + "'" + str(value) + "', "
            if key == sf.FIELDDIRNAME:
               dirlist.append(value)
            else:
               #understand what to do with errors in SF output
               if key == 'errors':
                  if value != '':
                     sys.stderr.write("LOG (understanding ERROR output): " + value + "\n")
               if key == sf.DICTID:
                  idkey, idvalue = self.handleID(value, idkeystring, idvaluestring, nsdict)

         fileid = None
         
         if filekeystring != '' and filevaluestring != '':
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

         if sf.hashtype != False:
            self.basedb.hashtype = sf.hashtype
            
      #final act - add directories to file table--#
      #---does not work well for absolute paths---#
      #uniquedirs = self.handledirectories(dirlist, sf)
      uniquedirs = set(dirlist)
      self.addDirsToDB(uniquedirs, cursor)
