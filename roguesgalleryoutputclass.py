import sys
import DroidAnalysisClass

class rogueoutputclass:

   def __init__(self, analysisresults):
      self.analysisresults = analysisresults

   def printTextResults(self):

   	print self.analysisresults.multipleIDList
   	print self.analysisresults.filesWithNoIDList
   	print self.analysisresults.extensionOnlyIDList
   	print self.analysisresults.extmismatchList 
   	print self.analysisresults.zerobytelist
   	print self.analysisresults.duplicatemd5altlisting
   	print self.analysisresults.duplicatefnamealtlisting
   	print self.analysisresults.multiplespacelist

