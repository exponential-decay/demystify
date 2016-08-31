import sys
import DroidAnalysisClass
from HandleBlacklistClass import HandleBlacklist

class rogueoutputclass:

   roguelist = []

   dupes = False
   pro = False
   black = False
   fnames = False
   dirs = False
   zero = False
   multi = False
   ext = False

   def __init__(self, analysisresults, config, heroes=False):
      self.analysisresults = analysisresults
      self.heroes = heroes
      self.handleconfig(config)

   def handleconfig(self, config):
      if config != False:
         if config.has_section(HandleBlacklist.CFG_ROGUES):
            if config.has_option(HandleBlacklist.CFG_ROGUES, HandleBlacklist.ROGUE_DUPE):
               self.dupes = config.get(HandleBlacklist.CFG_ROGUES, HandleBlacklist.ROGUE_DUPE).lower()
            if config.has_option(HandleBlacklist.CFG_ROGUES, HandleBlacklist.ROGUE_PRO):
               self.pro = config.get(HandleBlacklist.CFG_ROGUES, HandleBlacklist.ROGUE_PRO).lower()
            if config.has_option(HandleBlacklist.CFG_ROGUES, HandleBlacklist.ROGUE_BLACK):
               self.black = config.get(HandleBlacklist.CFG_ROGUES, HandleBlacklist.ROGUE_BLACK).lower()
            if config.has_option(HandleBlacklist.CFG_ROGUES, HandleBlacklist.ROGUE_FNAMES):
               self.fnames = config.get(HandleBlacklist.CFG_ROGUES, HandleBlacklist.ROGUE_FNAMES).lower()
            if config.has_option(HandleBlacklist.CFG_ROGUES, HandleBlacklist.ROGUE_DIRS):
               self.dirs = config.get(HandleBlacklist.CFG_ROGUES, HandleBlacklist.ROGUE_DIRS).lower()
            if config.has_option(HandleBlacklist.CFG_ROGUES, HandleBlacklist.ROGUE_ZERO):
               self.zero = config.get(HandleBlacklist.CFG_ROGUES, HandleBlacklist.ROGUE_ZERO).lower()
            if config.has_option(HandleBlacklist.CFG_ROGUES, HandleBlacklist.ROGUE_MULTI):
               self.multi = config.get(HandleBlacklist.CFG_ROGUES, HandleBlacklist.ROGUE_MULTI).lower()
            if config.has_option(HandleBlacklist.CFG_ROGUES, HandleBlacklist.ROGUE_EXT):
               self.ext = config.get(HandleBlacklist.CFG_ROGUES, HandleBlacklist.ROGUE_EXT).lower()

   def outputlist(self, pathlist):
      for x in pathlist:
         if x != "no value":              #todo: no values in duplicates, why?
            sys.stdout.write(str(x) + "\n")

   def rogueorhero(self, pathlist):
      if pathlist != False and pathlist != None:
         self.roguelist = self.roguelist + pathlist

   def printTextResults(self):

      if self.dupes == 'true':
         if self.analysisresults.hashused is True:
            self.rogueorhero(self.analysisresults.rogue_duplicates)

      if self.zero == 'true':
         self.rogueorhero(self.analysisresults.zerobytelist)

      if self.ext == 'true':
         self.rogueorhero(self.analysisresults.rogue_extension_mismatches)

      if self.multi == 'true':
         if self.analysisresults.multipleidentificationcount > 0:
            self.rogueorhero(self.analysisresults.rogue_multiple_identification_list)

      #PRONOM ONLY UNIDENTIFIED
      #output all unidentified files, but also, only when not using DROID output
      if self.analysisresults.tooltype != 'droid': 
         if self.analysisresults.rogue_pronom_ns_id != None and self.pro == 'true':
            self.rogueorhero(self.analysisresults.rogue_identified_pronom)
         else:
               self.rogueorhero(self.analysisresults.rogue_identified_all)
      else:
         if self.pro == 'true':
            self.rogueorhero(self.analysisresults.rogue_identified_pronom)

      if self.fnames == 'true':
         self.rogueorhero(self.analysisresults.rogue_file_name_paths)
      if self.dirs == 'true':
         self.rogueorhero(self.analysisresults.rogue_dir_name_paths)

      if self.black == 'true':
         self.rogueorhero(self.analysisresults.rogue_blacklist)
     
      number_allfiles = len(set(self.analysisresults.rogue_all_paths))
      number_alldirs = len(set(self.analysisresults.rogue_all_dirs))
     
      #Sets make it impossible to duplicate output... Also dealing with paths not files
      #so the numbers will add up slightly strangely if we don't think about folders too...
      if self.heroes is True:      
         hfiles = set(self.analysisresults.rogue_all_paths) - set(self.roguelist)
         hfolders = set(self.analysisresults.rogue_all_dirs) - set(self.roguelist)
         hset = list(hfiles) + list(hfolders)
         
         foldercount = len(hfolders)
         filecount = len(hfiles)
         
         self.outputlist(hset)
         sys.stderr.write("\n" + str(filecount) + " out of (" + str(number_allfiles)  + ") files output in rogues gallery.")
         sys.stderr.write("\n" + str(foldercount) + " out of (" + str(number_alldirs)  + ") directories output in rogues gallery." + "\n")
         
      else:
         rset = set(self.roguelist)         
         nofolders = len(rset - set(self.analysisresults.rogue_all_dirs))
         foldercount = abs(len(rset) - nofolders)
         filecount = len(rset) - foldercount

         self.outputlist(rset)
         sys.stderr.write("\n" + str(filecount) + " out of (" + str(number_allfiles)  + ") files output in rogues gallery.")
         sys.stderr.write("\n" + str(foldercount) + " out of (" + str(number_alldirs)  + ") directories output in rogues gallery." + "\n")

