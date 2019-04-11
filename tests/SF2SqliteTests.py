import sys

sys.path.append("../libs")

from PyDateHandler import PyDateHandler
from SFHandlerClass import SFYAMLHandler
from unittest import TestCase, TestLoader, TextTestRunner


class SF2SqliteTests(TestCase):
    def setup(self):
        self.sfhandler = SFYAMLHandler()
        self.datehandler = PyDateHandler()
        sys.stderr.write("\n")

    def test_get_datestring_without_timezone(self):
        self.setup()
        test1 = self.datehandler.get_datestring_without_timezone(
            "2016-01-01T20:45:12+13:00"
        )
        test2 = self.datehandler.get_datestring_without_timezone(
            "2015-01-01T20:45:12-04:00"
        )
        test3 = self.datehandler.get_datestring_without_timezone("2015-01-01T20:45:12")
        test4 = self.datehandler.get_datestring_without_timezone("nonsense-data")
        test5 = self.datehandler.get_datestring_without_timezone(
            "1999-01-01T20:45:12$04:00"
        )
        test6 = self.datehandler.get_datestring_without_timezone("2014-02-22T15:14:00")

        self.assertEqual(test1, 2016)
        self.assertEqual(test2, 2015)
        self.assertEqual(test3, 2015)
        self.assertEqual(test4, False)
        self.assertEqual(test5, 1999)
        self.assertEqual(test6, 2014)

        sys.stderr.write("\n")

    def test_getYear(self):
        self.setup()
        test1 = self.sfhandler.getYear("2016-01-01T20:45:12+13:00")
        test2 = self.sfhandler.getYear("2015-01-01T20:45:12-04:00")
        test3 = self.sfhandler.getYear("nonsense-data")
        test4 = self.sfhandler.getYear("2014-02-22T15:14:00")

        self.assertEqual(test1, 2016)
        self.assertEqual(test2, 2015)
        self.assertEqual(test3, "None")
        self.assertEqual(test4, 2014)

        sys.stderr.write("\n")


def main():
    suite = TestLoader().loadTestsFromTestCase(SF2SqliteTests)
    TextTestRunner().run(suite)


if __name__ == "__main__":
    main()
