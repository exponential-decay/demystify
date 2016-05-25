import sys
sys.path.append('../libs')

from SFHandlerClass import SFYAMLHandler
from unittest import TestCase, TestLoader, TextTestRunner

class SF2SqliteTests(TestCase):

   def setup(self):
      self.sfhandler = SFYAMLHandler()

   def test_do_something(self):
      self.setup()
      test1 = self.sfhandler.getYear('2016-01-01T20:45:12+13:00')
      test2 = self.sfhandler.getYear('2015-01-01T20:45:12-04:00')
      
      self.assertEqual(test1,2016)
      self.assertEqual(test2,2015)
      
def main():
	suite = TestLoader().loadTestsFromTestCase(SF2SqliteTests)
	TextTestRunner().run(suite)
	
if __name__ == "__main__":
	main()