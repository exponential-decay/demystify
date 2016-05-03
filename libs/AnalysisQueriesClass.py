class AnalysisQueries:
   
   SELECT_FILENAMES = "SELECT FILEDATA.NAME FROM FILEDATA"
   SELECT_DIRNAMES = "SELECT DISTINCT FILEDATA.DIR_NAME FROM FILEDATA"
   
   SELECT_HASH = "SELECT DBMD.HASH_TYPE FROM DBMD"
   SELECT_TOOL = "SELECT DBMD.TOOL_TYPE FROM DBMD"
   
   SELECT_COLLECTION_SIZE = "SELECT SUM(FILEDATA.SIZE) FROM FILEDATA"
   SELECT_COUNT_FILES = "SELECT COUNT(FILEDATA.FILE_ID) FROM FILEDATA WHERE (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container')"
   
   SELECT_COUNT_CONTAINERS = "SELECT COUNT(FILEDATA.FILE_ID) FROM FILEDATA WHERE FILEDATA.TYPE='Container'"
   SELECT_CONTAINER_TYPES = "SELECT DISTINCT FILEDATA.EXT FROM FILEDATA WHERE FILEDATA.TYPE='Container'"
   SELECT_COUNT_FILES_IN_CONTAINERS = "SELECT COUNT(FILEDATA.FILE_ID) FROM FILEDATA WHERE (FILEDATA.URI_SCHEME!='file') AND (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container')"

   SELECT_COUNT_ZERO_BYTE_FILES = "SELECT COUNT(FILEDATA.SIZE) FROM FILEDATA WHERE (FILEDATA.TYPE!='Folder') AND (FILEDATA.SIZE='0')"
   SELECT_ZERO_BYTE_FILEPATHS = "SELECT FILEDATA.FILE_PATH FROM FILEDATA WHERE FILEDATA.TYPE='File' AND FILEDATA.SIZE='0'"

   SELECT_COUNT_FOLDERS = "SELECT COUNT(FILEDATA.FILE_ID) FROM FILEDATA WHERE FILEDATA.TYPE='Folder'"
   
   SELECT_COUNT_UNIQUE_FILENAMES = "SELECT COUNT(DISTINCT FILEDATA.NAME) FROM FILEDATA WHERE (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container')"
   SELECT_COUNT_UNIQUE_DIRNAMES =  "SELECT COUNT(DISTINCT FILEDATA.DIR_NAME) FROM FILEDATA"
   
   SELECT_COUNT_NAMESPACES = 'SELECT COUNT(NSDATA.NS_ID) FROM NSDATA'
   
   SELECT_COUNT_ID_METHODS = """SELECT IDRESULTS.FILE_ID, IDDATA.ID_ID, IDDATA.METHOD as METHOD
                              FROM IDRESULTS
                              JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID"""

   SELECT_COUNT_EXT_MISMATCHES = """SELECT COUNT(distinct(IDRESULTS.FILE_ID))
                                       FROM IDRESULTS
                                       JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                                       WHERE IDDATA.EXTENSION_MISMATCH='True'"""                                          

   #TODO: Currency is PUID, what do we do for Tika and Freedesktop and others?
   SELECT_COUNT_FORMAT_COUNT = """SELECT COUNT(DISTINCT IDDATA.ID)
                                    FROM IDRESULTS
                                    JOIN NSDATA on IDDATA.NS_ID = NSDATA.NS_ID
                                    JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                                    WHERE (NSDATA.NS_NAME='pronom')
                                    AND (IDDATA.METHOD='Signature' OR IDDATA.METHOD='Container')"""

   SELECT_COUNT_OTHER_FORMAT_COUNT = """SELECT COUNT(DISTINCT IDDATA.ID)
                                       FROM IDRESULTS
                                       JOIN NSDATA on IDDATA.NS_ID = NSDATA.NS_ID
                                       JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                                       WHERE (NSDATA.NS_NAME!='pronom')
                                       AND (IDDATA.METHOD='Signature' OR IDDATA.METHOD='Container')"""

   #PRONOM and OTHERS Text identifiers as one result
   SELECT_COUNT_TEXT_IDENTIFIERS = """SELECT count(DISTINCT IDMETHOD)
                                       FROM (SELECT IDRESULTS.FILE_ID, IDDATA.ID as IDMETHOD
                                       FROM IDRESULTS
                                       JOIN NSDATA on IDDATA.NS_ID = NSDATA.NS_ID
                                       JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                                       AND (IDDATA.METHOD='Text'))"""

   #PRONOM and OTHERS Filename identifiers as one result
   SELECT_COUNT_FILENAME_IDENTIFIERS = """SELECT COUNT(DISTINCT IDMETHOD)
                                             FROM (SELECT IDRESULTS.FILE_ID, IDDATA.ID as IDMETHOD
                                             FROM IDRESULTS
                                             JOIN NSDATA on IDDATA.NS_ID = NSDATA.NS_ID
                                             JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                                             AND (IDDATA.METHOD='Filename'))"""

   SELECT_COUNT_EXTENSION_RANGE = """SELECT COUNT(DISTINCT FILEDATA.EXT) 
                                       FROM FILEDATA  
                                       WHERE FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container'"""

   SELECT_METHOD_FREQUENCY_COUNT = """SELECT IDDATA.METHOD, COUNT(*) AS total 
                                       FROM IDRESULTS  
                                       JOIN FILEDATA on IDRESULTS.FILE_ID = FILEDATA.FILE_ID
                                       JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID                                          
                                       WHERE (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container') 
                                       GROUP BY IDDATA.METHOD ORDER BY TOTAL DESC"""	

   #select the gamut of MIMEs in the accession/extract, not counts
   SELECT_MIME_RANGE = """SELECT DISTINCT IDDATA.MIME_TYPE AS total 
                                       FROM IDRESULTS 
                                       JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                                       WHERE IDDATA.MIME_TYPE!='None' and IDDATA.MIME_TYPE!='none'
                                       GROUP BY IDDATA.MIME_TYPE ORDER BY TOTAL DESC"""

   SELECT_BINARY_MATCH_COUNT = """SELECT NSDATA.NS_NAME, IDDATA.ID, COUNT(IDDATA.ID) as TOTAL
                                    FROM IDRESULTS
                                    JOIN NSDATA on IDDATA.NS_ID = NSDATA.NS_ID
                                    JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                                    WHERE (IDDATA.METHOD='Signature' OR IDDATA.METHOD='Container')
                                    GROUP BY IDDATA.ID ORDER BY NSDATA.NS_NAME, TOTAL DESC"""

   SELECT_YEAR_FREQUENCY_COUNT = """SELECT FILEDATA.YEAR, COUNT(FILEDATA.YEAR) AS total 
                                       FROM FILEDATA 
                                       WHERE (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container') 
                                       GROUP BY FILEDATA.YEAR ORDER BY TOTAL DESC"""


   #TODO: THIS STAT NEEDS REVISITING IN LIGHT OF SIEGFRIED
   #MULTIPLE IDS WILL BE REFLECTED USING MULTIPLE NAMESPACE PLACES - HOW TO REPORT ON?
   SELECT_PUIDS_EXTENSION_ONLY = """SELECT DISTINCT IDDATA.ID, IDDATA.FORMAT_NAME 
                                    FROM IDDATA 
                                    WHERE (IDDATA.METHOD='Extension')"""
   
   SELECT_ALL_UNIQUE_EXTENSIONS = """SELECT DISTINCT FILEDATA.EXT 
                                    FROM FILEDATA 
                                    WHERE (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container')
                                    AND FILEDATA.EXT!=''"""

   SELECT_COUNT_EXTENSION_FREQUENCY = """SELECT FILEDATA.EXT, COUNT(*) AS total 
                                       FROM FILEDATA
                                       WHERE (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container') 
                                       AND FILEDATA.EXT!=''
                                       GROUP BY FILEDATA.EXT ORDER BY TOTAL DESC"""

   SELECT_EXTENSION_MISMATCHES = """SELECT FILEDATA.FILE_PATH
                                    FROM IDRESULTS
                                    JOIN FILEDATA on IDRESULTS.FILE_ID = FILEDATA.FILE_ID
                                    JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                                    AND (IDDATA.EXTENSION_MISMATCH='True')"""

   #MULTIPLE ID FOR FILES GREATER THAN ZERO BYTES
   SELECT_MULTIPLE_ID_PATHS = """SELECT FILEDATA.FILE_PATH 
                                 FROM IDRESULTS 
                                 JOIN FILEDATA on IDRESULTS.FILE_ID = FILEDATA.FILE_ID
                                 JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID                                      
                                 WHERE (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container') 
                                 AND (IDDATA.FORMAT_COUNT > 1) 
                                 AND (FILEDATA.SIZE > 0)"""

   SELECT_COUNT_DUPLICATE_CHECKSUMS = """SELECT FILEDATA.HASH, COUNT(*) AS TOTAL
                                          FROM FILEDATA
                                          WHERE FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container'
                                          GROUP BY FILEDATA.HASH
                                          HAVING TOTAL > 1
                                          ORDER BY TOTAL DESC"""
   #siegfried only...
   SELECT_BYTE_MATCH_BASIS = """SELECT DISTINCT IDDATA.BASIS, IDDATA.ID, FILEDATA.NAME
                                 FROM IDRESULTS
                                 JOIN FILEDATA on IDRESULTS.FILE_ID = FILEDATA.FILE_ID
                                 JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                                 WHERE IDDATA.BASIS LIKE '%byte match%'"""

   def count_multiple_ids(self, nscount, paths=False):
      count = 'SELECT count(FREQUENCY)' + "\n"
      pathquery = 'SELECT PATH' + "\n"               
      body = """FROM (SELECT FILEDATA.FILE_PATH AS PATH, COUNT(FILEDATA.FILE_ID) AS FREQUENCY
                  FROM IDRESULTS
                  JOIN FILEDATA on IDRESULTS.FILE_ID = FILEDATA.FILE_ID
                  JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                  GROUP BY FILEDATA.FILE_ID
                  ORDER BY COUNT(FILEDATA.FILE_ID) DESC)
                  WHERE FREQUENCY > """
      
      query = ''
      if paths == False:
         query = count + body + str(nscount)
      else:
         query = pathquery + body + str(nscount)
      return query

   def list_duplicate_paths(self, checksum):
      return "SELECT FILE_PATH FROM FILEDATA WHERE FILEDATA.HASH='" + checksum + "'ORDER BY FILEDATA.FILE_PATH"

   def count_id_instances(self, id):
      return "SELECT COUNT(*) AS total FROM IDDATA WHERE (IDDATA.ID='" + id + "')"

   def search_id_instance_filepaths(self, id):
      query_part1 = """SELECT FILEDATA.FILE_PATH 
                        FROM IDRESULTS 
                        JOIN FILEDATA on IDRESULTS.FILE_ID = FILEDATA.FILE_ID
                        JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID  
                        WHERE IDDATA.ID='""" 
      
      query_part2 = id + "' ORDER BY FILEDATA.FILE_PATH DESC"      
      return query_part1 + query_part2

   def query_from_idrows(self, idlist):      
      list = 'WHERE '
      for i in idlist:
         where = "IDRESULTS.ID_ID=" + str(i[1]) + " OR "
         list = list + where
      list = list.rstrip(' OR ')
      
      SELECT_NAMESPACE_AND_IDS = """SELECT NSDATA.NS_NAME, IDDATA.ID, IDDATA.FORMAT_NAME, IDDATA.BASIS, IDDATA.FORMAT_VERSION
                                    FROM IDRESULTS
                                    JOIN NSDATA on IDDATA.NS_ID = NSDATA.NS_ID
                                    JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID"""
                                    
      SELECT_NAMESPACE_AND_IDS = SELECT_NAMESPACE_AND_IDS 
      return SELECT_NAMESPACE_AND_IDS + "\n" + list                                     

   #IT MIGHT BE WORTH PULLING THIS APART BUT WILL SEE...
   def query_from_ids(self, idlist, idmethod=False):      
      list = ''
      for i in idlist:
         if idmethod != False:
            where = "IDRESULTS.FILE_ID=" + str(i) + " OR "
         else:
            where = "FILEDATA.FILE_ID=" + str(i) + " OR "
         list = list + where
      list = list.rstrip(' OR ')

      SELECT_PATHS = """SELECT FILEDATA.FILE_PATH
                        FROM FILEDATA"""

      SELECT_NAMESPACE_AND_IDS = """SELECT NSDATA.NS_NAME, IDDATA.ID
                                    FROM IDRESULTS
                                    JOIN NSDATA on IDDATA.NS_ID = NSDATA.NS_ID
                                    JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                                    WHERE IDDATA.METHOD="""
      if idmethod != False:
         SELECT_NAMESPACE_AND_IDS = SELECT_NAMESPACE_AND_IDS + "'" + idmethod + "'"    #which method?   
         list = 'OR ' + list
         return SELECT_NAMESPACE_AND_IDS + "\n" + list                                     
      else:
         list = 'WHERE ' + list
         return SELECT_PATHS + "\n" + list

   #NAMESPACE QUERIES
   SELECT_NS_DATA = """SELECT * 
                        FROM NSDATA"""

   def get_ns_multiple_ids(self, nsid, nscount):
      SELECT_NAMESPACE_BINARY_IDS1 = """SELECT count(*)
                                          FROM (SELECT COUNT(FILEDATA.FILE_ID) AS FREQUENCY
                                          FROM IDRESULTS
                                          JOIN FILEDATA on IDRESULTS.FILE_ID = FILEDATA.FILE_ID
                                          JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                                          WHERE IDDATA.NS_ID="""
                                          
      SELECT_NAMESPACE_BINARY_IDS2 = """AND IDDATA.METHOD='Binary' or IDDATA.METHOD='Container'
                                          GROUP BY FILEDATA.FILE_ID
                                          ORDER BY COUNT(FILEDATA.FILE_ID) DESC)
                                          WHERE FREQUENCY >"""

      part1 = SELECT_NAMESPACE_BINARY_IDS1 + str(nsid) + "\n"
      part2 = SELECT_NAMESPACE_BINARY_IDS2 + str(nsid)
      query = part1 + part2
      return query.replace('  ', '')
      
   def get_ns_methods(self, id, binary=True, method=False):
      
      AND_NS = "AND NS_ID=" + str(id)

      COUNT_IDS_NS = """SELECT COUNT(*)
                        FROM IDDATA
                        WHERE IDDATA.METHOD='Signature' or IDDATA.METHOD='Container'
                        """ 

      ID_METHODS_COUNT = """SELECT COUNT(*)
                              FROM IDDATA
                              WHERE IDDATA.METHOD=""" 

      query = ''
      if binary is True:
         query = COUNT_IDS_NS + AND_NS
      elif method is not False:
         query = ID_METHODS_COUNT + "'" + method + "' " + AND_NS

      return query.replace('  ', '')

   #ERRORS, TODO: Place somewhere else?
   ERROR_NOHASH = "Unable to detect duplicates: No HASH algorithm used by identification tool."
