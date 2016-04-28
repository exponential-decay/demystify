#Test list of duplicates returned. (count, values)
#Test rogues paths are only paths to files, and not paths to directories
#Test config options are working

from unittest import TestCase, TestLoader, TextTestRunner
from DroidAnalysisClass import *
import testdata

class DroidAnalysisClassTests(TestCase):

   def setup(self):
      self.empty = DetectEmpties()
   
   def testRecurseDeleteFolders(self):
      print "test todo"   

def main():
	suite = TestLoader().loadTestsFromTestCase(DroidAnalysisClassTests)
	TextTestRunner().run(suite)
	
if __name__ == "__main__":
	main()