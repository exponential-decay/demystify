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

      for x in sfdata[sf.DICTFILES]:
         print x    
         print
         print

      #print sfdata[sf.DICTHEADER]

      #print sfdata[sf.DICTFILES]
