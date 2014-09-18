# -*- coding: utf-8 -*-
import re

class RegexFnameAnalysis:

   def __init__(self):
      #detect multiple contiguous spaces in filenames
      self.multiplespaceregex = re.compile(r'(\s{2,100})')
      
   #detect multiple contiguous spaces in filenames
   def detectMultipleSpaces(self, fname):
      if self.multiplespaceregex.search(fname) is not None:
         return True
      else:
         return False