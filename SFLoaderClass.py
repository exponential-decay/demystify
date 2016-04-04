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

#      for x in identidiers:
                  
      
     #    print x
'''
      for x in sfdata[sf.DICTFILES]:
         for y in identifiers:   
            basis = x[sf.DICTID][y]['method']
            if basis is not None:
               print '"' + basis + '"'
   '''            
            #for z in y:
               #print z
      #for x in sfdata[sf.DICTFILES]:
      #   print x[sf.FIELDURI]
      #   print x[sf.FIELDURISCHEME]

      #print sfdata[sf.DICTHEADER]

      #print sfdata[sf.DICTFILES]
