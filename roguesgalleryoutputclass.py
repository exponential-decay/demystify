import sys
import DroidAnalysisClass

class rogueoutputclass:

   roguelist = []

   def __init__(self, analysisresults, heroes=False):
      self.analysisresults = analysisresults
      self.heroes = heroes

   def outputlist(self, pathlist):
      for x in pathlist:
         if x != "no value":
            sys.stdout.write(x + "\n")
            
   def rogueorhero(self, pathlist):
      if pathlist != False:
         self.roguelist = self.roguelist + pathlist

   def printTextResults(self):

      self.rogueorhero(self.analysisresults.multipleIDList)
      self.rogueorhero(self.analysisresults.filesWithNoIDList)
      self.rogueorhero(self.analysisresults.extensionOnlyIDfnameList)
      self.rogueorhero(self.analysisresults.extmismatchList) 
      self.rogueorhero(self.analysisresults.zerobytelist)
      self.rogueorhero(self.analysisresults.duplicatemd5pathlisting)
      
      if self.heroes is True:
         heros = list(set(self.analysisresults.allfilepaths) - set(self.roguelist))
         self.outputlist(heros)
      else:
         self.outputlist(set(self.roguelist))
