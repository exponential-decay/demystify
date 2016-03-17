import unicodecsv
import os.path
from urlparse import urlparse

class genericCSVHandler():

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
   def readDROIDCSV(self, droidcsvfname):
      csvhandler = genericCSVHandler()
      self.csv = csvhandler.csvaslist(droidcsvfname)
      return self.csv

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
