# -*- coding: utf-8 -*-
# based on: http://msdn.microsoft.com/en-us/library/aa365247(VS.85).aspx

import sys
sys.path.append(r'cooperhewitt/unicode/')
import names
from internationalstrings import AnalysisStringsEN as IN_EN

class MsoftFnameAnalysis:

   report = ''

   def __init__(self):
      self.STRINGS = IN_EN

   #Note: verbose default false because of potential no. characters in a collection
   def completeFnameAnalysis(self, s, folders=False, verbose=False):
      #need to ensure argument is interpreted correctly as UNICODE on way in
      #without explicit decode we have str type
      s = s.decode('utf8')
  
      self.report= u""
      self.verbose = verbose
      
      self.detectNonAsciiCharacters(s, folders)
      self.detectNonRecommendedCharacters(s, folders)
      self.detectNonPrintableCharacters(s, folders)
      self.detectMsoftReservedNames(s, folders)
      self.detectSpaceAtEndOfName(s, folders)
      self.detectPeriodAtEndOfName(s, folders)
      return self.report

   def reportIssue(self, s, msg, value='', folders=False):
      if folders == True:
         text = 'Directory: '
      else:
         text = 'File: '
      self.report = self.report + text + s + " " + msg + " " + value + "\n"

   def unicodename(self, c):
      ref = names.lookup()
      name = ref.name(c)
      return "%s: %s" % (name, c)

   def detectNonAsciiCharacters(self, s, folders=False):
      #Nicer method: all(ord(c) < 128 for c in s)
      nonascii = False
      for c in s:
         if ord(c) > 128:
            nonascii = True
            if nonascii == True:
               self.reportIssue(s, self.STRINGS.FNAME_CHECK_ASCII + ":", hex(ord(c)) + ", " + self.unicodename(c), folders)
               nonascii == False
            if self.verbose == False:
               break

   def detectNonRecommendedCharacters(self, s, folders=False):
      charlist = ['<','>',':','"','/','\\','?','*','|', ']', '[']
      if folders==True:
         charlist = ['<','>','"','?','*','|', ']', '[']
         
      for c in s:
         if c in charlist:
            self.reportIssue(s, self.STRINGS.FNAME_CHECK_NOT_RECOMMENDED + ":", hex(ord(c)) + ", " + self.unicodename(c), folders)
            if self.verbose == False:
               break

   def detectNonPrintableCharacters(self, s, folders=False):
      for c in range(0x1f):
         if chr(c) in s:
            self.reportIssue(s, self.STRINGS.FNAME_CHECK_NON_PRINT + ":", hex(c) + ", " + self.unicodename(c), folders)
            if self.verbose == False:
               break

   def detectMsoftReservedNames(self, s, folders=False):
      badnames = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', \
                     'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', \
                        'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', \
                           'LPT6', 'LPT7', 'LPT8', 'LPT9']
            
      for c in badnames:
         if c.lower() in s[0:len(c)].lower():
            problem = True
            try:
               if s[len(c)] == '.':					#zero-based index
                  problem = True
               else:
                  problem = False
            except IndexError:
               problem = True
            if problem == True:
               self.reportIssue(s, self.STRINGS.FNAME_CHECK_RESERVED + ": ", c, folders)

   def detectSpaceAtEndOfName(self, s, folders=False):
      if s.endswith(' '):
         self.reportIssue(s, self.STRINGS.FNAME_CHECK_SPACE + ".", folders)
         
   def detectPeriodAtEndOfName(self, s, folders):		
      if s.endswith('.'):
         self.reportIssue(s, self.STRINGS.FNAME_CHECK_PERIOD + ".", folders=False)
      
   def __detect_invalid_characters_test__(self):
      #Strings for unit tests
      test_strings = ['COM4', 'COM4.txt', '.com4', 'abcCOM4text', 'abc.com4.txt.abc', 'con', 'CON', 'consumer', 'space ', 'preiod.', 'ף', 'י', 'צ', 'ףיצ', 'file[bracket]one.txt', 'file[two.txt', 'filethree].txt', '-=_|\"', '(<|>|:|"|/|\\|\?|\*|\||\x00-\x1f)']	
   
      # First test, all ASCII characters?
      for s in test_strings:
         self.detect_invalid_characters(s)

def main():
   
   import sys

   input = sys.argv[1:]
   input = " ".join(input)

   input = input.decode('utf-8')

   analysis = MsoftFnameAnalysis().completeFnameAnalysis(input, True)
   sys.stdout.write(analysis)

if __name__ == "__main__":
   main()
