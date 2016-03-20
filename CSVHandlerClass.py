import unicodecsv
import os.path
import datetime
from urlparse import urlparse

class genericCSVHandler():

   BOM = False
   BOMVAL = '\xEF\xBB\xBF'

   def __init__(self, BOM=False):
      self.BOM = BOM

   def __getCSVheaders__(self, csvcolumnheaders):
      header_list = []
      for header in csvcolumnheaders:      
         header_list.append(header)
      return header_list

   # returns list of rows, each row is a dictionary
   # header: value, pair. 
   def csvaslist(self, csvfname):
      columncount = 0
      csvlist = None
      if os.path.isfile(csvfname): 
         csvlist = []
         with open(csvfname, 'rb') as csvfile:
            if self.BOM is True:
               csvfile.seek(len(self.BOMVAL))
            csvreader = unicodecsv.reader(csvfile)
            for row in csvreader:
               if csvreader.line_num == 1:		# not zero-based index
                  header_list = self.__getCSVheaders__(row)
                  columncount = len(header_list)
               else:
                  csv_dict = {}
                  #for each column in header
                  #note: don't need ID data. Ignoring multiple ID.
                  for i in range(columncount):
                     csv_dict[header_list[i]] = row[i]
                  csvlist.append(csv_dict)
      return csvlist

class droidCSVHandler():

   #returns droidlist type
   def readDROIDCSV(self, droidcsvfname, BOM=False):
      csvhandler = genericCSVHandler(BOM)
      self.csv = csvhandler.csvaslist(droidcsvfname)
      return self.csv

   def getDirName(self, filepath):
      return os.path.dirname(filepath)
   
   def adddirname(self, droidlist):
      for row in droidlist:
         row['DIR_NAME'] = self.getDirName(row['FILE_PATH'])
      return droidlist   

   def addurischeme(self, droidlist):
      for row in droidlist:
         row['URI_SCHEME'] = self.getURIScheme(row['URI'])
      return droidlist

   def getYear(self, datestring):
      dt = datetime.datetime.strptime(datestring.split('+', 1)[0], '%Y-%m-%dT%H:%M:%S')
      return int(dt.year)

   def addYear(self, droidlist):
      for row in droidlist:
         if row['LAST_MODIFIED'] is not '':
            row['YEAR'] = str(self.getYear(row['LAST_MODIFIED']))
      return droidlist

   def removecontainercontents(self, droidlist):
      newlist = []   # naive remove causes loop to skip items
      for row in droidlist:
         uris = self.getURIScheme(row['URI'])
         if self.getURIScheme(row['URI']) == 'file':
            newlist.append(row)
      return newlist
   
   def removefolders(self, droidlist):
      #TODO: We can generate counts here and store in member vars
      newlist = []   # naive remove causes loop to skip items
      for i,row in enumerate(droidlist):
         if row['TYPE'] != 'Folder':
            newlist.append(row)      
      return newlist
 
   def retrievefolderlist(self, droidlist):
      newlist = []
      for row in droidlist:
         if row['TYPE'] == 'Folder':
            newlist.append(row['FILE_PATH'])
      return newlist
   
   def retrievefoldernames(self, droidlist):
      newlist = []
      for row in droidlist:
         if row['TYPE'] == 'Folder':
            newlist.append(row['NAME'])
      return newlist
   
   def getURIScheme(self, url):
      return urlparse(url).scheme
