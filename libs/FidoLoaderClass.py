# -*- coding: utf-8 -*-
import sys
from ToolMappingClass import ToolMapping
from CSVHandlerClass import *

class FidoLoader:

   basedb = ''

   def __init__(self, basedb):
      self.basedb = basedb

   def fidoDBSetup(self, export, cursor):
      sys.stdout.write("Placeholder Code: Currently not handling FIDO exports." + "\n") 
