class AnalysisQueries:
   
   SELECT_ALL_NAMES = "SELECT FILEDATA.NAME FROM FILEDATA"
   SELECT_FILENAMES_AND_DIRNAMES = "SELECT FILEDATA.DIR_NAME, FILEDATA.NAME FROM FILEDATA"
   
   SELECT_HASH = "SELECT DBMD.HASH_TYPE FROM DBMD"
   
   SELECT_COLLECTION_SIZE = "SELECT SUM(FILEDATA.SIZE) FROM FILEDATA"
   SELECT_COUNT_FILES = "SELECT COUNT(FILEDATA.NAME) FROM FILEDATA WHERE (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container')"
   SELECT_COUNT_CONTAINERS = "SELECT COUNT(FILEDATA.NAME) FROM FILEDATA WHERE FILEDATA.TYPE='Container'"
   
   SELECT_COUNT_FILES_IN_CONTAINERS = "SELECT COUNT(FILEDATA.NAME) FROM FILEDATA WHERE (FILEDATA.URI_SCHEME!='file') AND (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container')"
   
   SELECT_COUNT_FOLDERS = "SELECT COUNT(FILEDATA.NAME) FROM FILEDATA WHERE FILEDATA.TYPE='Folder'"
   
   SELECT_COUNT_UNIQUE_FILENAMES = "SELECT COUNT(DISTINCT FILEDATA.NAME) FROM FILEDATA WHERE (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container')"
   SELECT_COUNT_UNIQUE_DIRNAMES =  "SELECT COUNT(DISTINCT FILEDATA.DIR_NAME) FROM FILEDATA"
   
   SELECT_COUNT_IDENTIFIED_FILES = """SELECT COUNT(FILEDATA.NAME)
                                       FROM IDRESULTS
                                       JOIN FILEDATA on IDRESULTS.FILE_ID = FILEDATA.FILE_ID
                                       JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                                       WHERE (FILEDATA.TYPE='File' or FILEDATA.TYPE='Container')
                                       AND (IDDATA.METHOD='Signature' or IDDATA.METHOD='Container');"""
                                       
   SELECT_COUNT_MULTIPLE_ID = """SELECT COUNT(IDDATA.FORMAT_COUNT) 
                                    FROM IDRESULTS
                                    JOIN FILEDATA on IDRESULTS.FILE_ID = FILEDATA.FILE_ID
                                    JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                                    WHERE (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container') 
                                    AND (IDDATA.FORMAT_COUNT!='1' AND IDDATA.FORMAT_COUNT!='0') 
                                    AND (CAST(FILEDATA.SIZE AS INT) > 0)"""
   
   SELECT_COUNT_UNIDENTIFIED = """SELECT COUNT(FILEDATA.NAME) 
                                    FROM IDRESULTS 
                                    JOIN FILEDATA on IDRESULTS.FILE_ID = FILEDATA.FILE_ID
                                    JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID   
                                    WHERE (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container') 
                                    AND (IDDATA.METHOD='' OR IDDATA.METHOD='Extension')"""

   SELECT_COUNT_EXTENSION_ONLY = """SELECT COUNT(FILEDATA.NAME) 
                                       FROM IDRESULTS 
                                       JOIN FILEDATA on IDRESULTS.FILE_ID = FILEDATA.FILE_ID
                                       JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                                       WHERE IDDATA.METHOD='Extension' 
                                       AND(FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container')"""

   #ERRORS, TODO: Place somewhere else?
   ERROR_NOHASH = "Unable to detect duplicates: No HASH algorithm used by identification tool."