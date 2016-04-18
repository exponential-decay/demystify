import sys
from ToolMappingClass import ToolMapping
from SFHandlerClass import SFYAMLHandler

class SFLoader:

   basedb = ''
   identifiers = ''   

   def __init__(self, basedb):
      self.basedb = basedb

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
      print sf.readSFYAML(sfexport)
      
      sfdata = sf.sfdata

      sf.addfilename(sfdata)
      sf.adddirname(sfdata)
      sf.addYear(sfdata)

      #   HEADDETAILS = 'id details '
      #   HEADNAMESPACE = 'id namespace '
      #   HEADCOUNT = 'identifier count'

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
               #print filekeystring
               #print filevaluestring
            else:
               #understand what to do with errors in SF output
               if key == 'errors':
                  if value != '':
                     sys.stderr.write("LOG: " + value + "\n")
               if key == sf.DICTID:
                  idk, idv = self.handleID(value, idkeystring, idvaluestring)



