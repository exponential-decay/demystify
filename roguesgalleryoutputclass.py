import sys
import DroidAnalysisClass

class rogueoutputclass:

   herolist = []

   def __init__(self, analysisresults, heros=False):
      self.analysisresults = analysisresults
      self.heros = heros

   def outputlist(self, pathlist):
      for x in pathlist:
         if x != "no value":
            sys.stdout.write(x + "\n")
            
   def rogueorhero(self, pathlist):
      if self.heros == False:
         if pathlist != False:
            self.outputlist(pathlist)
      else:
         #heros list to become direct opposite of rogues list
         if pathlist != False:
            self.herolist = self.herolist + pathlist

   def printTextResults(self):

      self.rogueorhero(self.analysisresults.multipleIDList)
      self.rogueorhero(self.analysisresults.filesWithNoIDList)
      self.rogueorhero(self.analysisresults.extensionOnlyIDfnameList)
      self.rogueorhero(self.analysisresults.extmismatchList) 
      self.rogueorhero(self.analysisresults.zerobytelist)
      self.rogueorhero(self.analysisresults.duplicatemd5pathlisting)
      
      if self.heros is True:
         self.outputlist(self.herolist)