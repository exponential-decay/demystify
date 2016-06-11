#!/usr/bin/env python
# -*- coding: utf-8 -*-

#[blacklist]
#ids='fmt/111','fmt/682','fmt/394'
#filenames='.DS_Store','Untitled Document'
#directorynames='Untitled Folder','(copy','.git'
#fileextensions='exe','dll','.txt'

#create 
class HandleBlacklist:

   CFG_BLACK = 'blacklist'
   CFG_FNAMES = 'filenames'
   CFG_DIRS = 'directorynames'
   CFG_IDS = 'ids'
   CFG_EXT = 'fileextensions'

   FILENAMES = 'file names'
   IDS = 'ids'
   DIRECTORIES = 'directories'
   EXTENSIONS = 'extensions'

   def blacklist(self, config):
      #four section dictionary
      self.blacklist = {}
      if config.has_section(self.CFG_BLACK):
         if config.has_option(self.CFG_BLACK,self.CFG_IDS):
            self.blacklist[self.IDS] = config.get(self.CFG_BLACK, self.CFG_IDS).replace("'","").split(',')
         else:
            self.blacklist[self.IDS] = None
         if config.has_option(self.CFG_BLACK, self.CFG_FNAMES):
            self.blacklist[self.FILENAMES] = config.get(self.CFG_BLACK, self.CFG_FNAMES).replace("'","").split(',')
         else:
            self.blacklist[self.FILENAMES] = None
         if config.has_option(self.CFG_BLACK,self.CFG_DIRS):
            self.blacklist[self.DIRECTORIES] = config.get(self.CFG_BLACK, self.CFG_DIRS).replace("'","").split(',')
         else:
            self.blacklist[self.DIRECTORIES] = None
         if config.has_option(self.CFG_BLACK,self.CFG_EXT):
            self.blacklist[self.EXTENSIONS] = config.get(self.CFG_BLACK, self.CFG_EXT).replace("'","").split(',')
         else:
            self.blacklist[self.EXTENSIONS] = None
      return self.blacklist

