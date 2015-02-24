import sys
import DroidAnalysisClass

class rogueoutputclass:

   def __init__(self, analysisresults):
      self.analysisresults = analysisresults

   def printTextResults(self):

      print self.analysisresults.multipleIDList
      print self.analysisresults.filesWithNoIDList
      print self.analysisresults.extensionOnlyIDfnameList
      print self.analysisresults.extmismatchList 
      print self.analysisresults.zerobytelist
      for x in self.analysisresults.duplicatemd5altlisting:
        print x
      for d in self.analysisresults.duplicatefnamealtlisting:
         print d
      for f in self.analysisresults.multiplespacelist:
         print "\\".join(f)

