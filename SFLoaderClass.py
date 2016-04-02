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

      sf.adddirname(sfdata)

      #print sfdata[sf.DICTHEADER]

      #print sfdata[sf.DICTFILES]
