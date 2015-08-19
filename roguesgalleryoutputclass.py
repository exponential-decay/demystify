import sys
import DroidAnalysisClass

class rogueoutputclass:

   def __init__(self, analysisresults):
      self.analysisresults = analysisresults

   def printTextResults(self):

      '''print self.analysisresults.multipleIDList
      print self.analysisresults.filesWithNoIDList
      print self.analysisresults.extensionOnlyIDfnameList
      print self.analysisresults.extmismatchList 
      print self.analysisresults.zerobytelist'''
      #for x in self.analysisresults.duplicatemd5pathlisting:
      #  print x
      for d in self.analysisresults.duplicatefnamepathlisting:
         if d != "no value":
            sys.stdout.write(d + "\n")
      #for f in self.analysisresults.multiplespacelist:
      #   print "\\".join(f)

