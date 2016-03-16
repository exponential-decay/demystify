import sys

class IdentifyExport:

   DROIDTYPE = "droid"
   UNKTYPE = "unknown"

   droid = ('"ID","PARENT_ID","URI","FILE_PATH","NAME","METHOD","STATUS"' +
            ',"SIZE","TYPE","EXT","LAST_MODIFIED","EXTENSION_MISMATCH",' + 
            '"MD5_HASH","FORMAT_COUNT","PUID","MIME_TYPE","FORMAT_NAME",' +
            '"FORMAT_VERSION"')

   def exportid(self, export):

      f = open(export, 'rb')
      magic = f.readline()
      f.close()

      if magic.strip() == self.droid:
         return self.DROIDTYPE
      else:
         return self.UNKTYPE
