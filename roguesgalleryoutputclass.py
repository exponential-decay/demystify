import sys
import DroidAnalysisClass

class rogueoutputclass:

   def __init__(self, analysisresults, heros=False):
      self.analysisresults = analysisresults

   def outputlist(self, pathlist):
      if pathlist != False:
         for x in pathlist:
            if x != "no value":
               sys.stdout.write(x + "\n")

   def printTextResults(self):

      self.outputlist(self.analysisresults.multipleIDList)
      self.outputlist(self.analysisresults.filesWithNoIDList)
      self.outputlist(self.analysisresults.extensionOnlyIDfnameList)
      self.outputlist(self.analysisresults.extmismatchList) 
      self.outputlist(self.analysisresults.zerobytelist)
      self.outputlist(self.analysisresults.duplicatemd5pathlisting)