class ToolMapping:

   FILE_MAP = {
      "ID" : "INPUT_ID",
      "PARENT_ID" : "PARENT_ID",
      "URI" : "URI",
      "URI_SCHEME" : "URI_SCHEME",
      "FILE_PATH" : "FILE_PATH",
      "DIR_NAME" : "DIR_NAME",
      "NAME" : "NAME", 
      "SIZE" : "SIZE",
      "TYPE" : "TYPE",
      "EXT" : "EXT",
      "LAST_MODIFIED" : "LAST_MODIFIED",
      "YEAR" : "YEAR",
      "SHA1_HASH" : "HASH",
      "SHA256_HASH" : "HASH",
      "MD5_HASH" : "HASH"
   }

   #file count doesn't have a place yet...
   DROID_ID_MAP = {
      'METHOD' : 'METHOD',
      'STATUS' : 'STATUS',
      'PUID' : 'ID',
      'MIME_TYPE' : 'MIME_TYPE',
      'FORMAT_NAME' : 'FORMAT_NAME',
      'FORMAT_VERSION' : 'FORMAT_VERSION',
      'EXTENSION_MISMATCH' : 'EXTENSION_MISMATCH',
      'FORMAT_COUNT' : 'FORMAT_COUNT'  #TODO: Remove into namespace tables
      }