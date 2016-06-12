import sys
import DroidAnalysisClass

class rogueoutputclass:

   roguelist = []

   def __init__(self, analysisresults, heroes=False):
      self.analysisresults = analysisresults
      self.heroes = heroes

   def outputlist(self, pathlist):
      for x in pathlist:
         if x != "no value":              #todo: no values in duplicates, why?
            sys.stdout.write(x + "\n")

   def rogueorhero(self, pathlist):
      if pathlist != False:
         self.roguelist = self.roguelist + pathlist

   def printTextResults(self):

      if self.analysisresults.hashused is True:
         self.rogueorhero(self.analysisresults.rogue_duplicates)

      self.rogueorhero(self.analysisresults.zerobytelist)

      self.rogueorhero(self.analysisresults.rogue_extension_mismatches)

      if self.analysisresults.multipleidentificationcount > 0:
         self.rogueorhero(self.analysisresults.rogue_multiple_identification_list)

      if self.analysisresults.pronom_ns_id != None:
         self.rogueorhero(self.analysisresults.rogue_identified_pronom)
      else:
         self.rogueorhero(self.analysisresults.rogue_identified_all)

      self.rogueorhero(self.analysisresults.rogue_file_name_paths)
      self.rogueorhero(self.analysisresults.rogue_dir_name_paths)

      self.rogueorhero(self.analysisresults.rogue_blacklist)
     
      #Sets make it impossible to duplicate output... Also dealing with paths not files
      #so the numbers will add up slightly strangely if we don't think about folders too...
      if self.heroes is True:
         heroes = list(set(self.analysisresults.rogue_all_paths) - set(self.roguelist))
         self.outputlist(heroes)
         sys.stderr.write("\n" + str(len(set(heroes))) + " file paths output in heroes gallery." + "\n")
      else:
         self.outputlist(set(self.roguelist))
         sys.stderr.write("\n" + str(len(set(self.roguelist))) + " file paths output in rogues gallery." + "\n")

