class AnalysisQueries:
   
   SELECT_ALL_NAMES = "SELECT FILEDATA.NAME FROM FILEDATA"
   SELECT_FILENAMES_AND_DIRNAMES = "SELECT FILEDATA.DIR_NAME, FILEDATA.NAME FROM FILEDATA"
   
   SELECT_HASH = "SELECT DBMD.HASH_TYPE FROM DBMD"
   
   
   
   
   
   #ERRORS, TODO: Place somewhere else?
   ERROR_NOHASH = "Unable to detect duplicates: No HASH algorithm used by identification tool."