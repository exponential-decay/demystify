import sys
from ToolMappingClass import ToolMapping
from SFHandlerClass import SFYAMLHandler

class SFLoader:

   basedb = ''
         
   def __init__(self, basedb):
      self.basedb = basedb
      
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

      identifiers = sf.getIdentifiersList()
      files = sf.getFiles()

      #Awkward structure to navigate
      #sf.sfdata['header']
      #sf.sfdata['files']
      #sf.sfdata['files'][0]['identification']

      for f in files:
         filekeystring = ''
         filevaluestring = ''
         for key, value in f.items():
            if key in ToolMapping.SF_FILE_MAP:
               filekeystring = filekeystring + ToolMapping.SF_FILE_MAP[key] + ", "
               filevaluestring = filevaluestring + "'" + str(value) + "', "
               print filekeystring
               print filevaluestring


