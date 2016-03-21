import sys

class IdentifyExport:

   DROIDTYPE = "droid"  #backward compatibility for now... 
   
   #specific hashes
   DROIDMD5TYPE = "droid_md5"
   DROIDSHA1TYPE = "droid_md5"
   DROIDSHA256TYPE = "droid_md5"
   DROIDNOHASH  = "droid_nohash"
   DROIDTYPEBOM = 'droid_BOM'
   UNKTYPE = "unknown"

   droid_md5 = ('"ID","PARENT_ID","URI","FILE_PATH","NAME","METHOD","STATUS"' +
            ',"SIZE","TYPE","EXT","LAST_MODIFIED","EXTENSION_MISMATCH",' + 
            '"MD5_HASH","FORMAT_COUNT","PUID","MIME_TYPE","FORMAT_NAME",' +
            '"FORMAT_VERSION"')

   droid_sha1 = ('"ID","PARENT_ID","URI","FILE_PATH","NAME","METHOD","STATUS"' +
            ',"SIZE","TYPE","EXT","LAST_MODIFIED","EXTENSION_MISMATCH",' + 
            '"SHA1_HASH","FORMAT_COUNT","PUID","MIME_TYPE","FORMAT_NAME",' +
            '"FORMAT_VERSION"')
            
   droid_sha256 = ('"ID","PARENT_ID","URI","FILE_PATH","NAME","METHOD","STATUS"' +
            ',"SIZE","TYPE","EXT","LAST_MODIFIED","EXTENSION_MISMATCH",' + 
            '"SHA256_HASH","FORMAT_COUNT","PUID","MIME_TYPE","FORMAT_NAME",' +
            '"FORMAT_VERSION"')
            
   droid_nohash = ('"ID","PARENT_ID","URI","FILE_PATH","NAME","METHOD","STATUS"' +
            ',"SIZE","TYPE","EXT","LAST_MODIFIED","EXTENSION_MISMATCH",' + 
            '"HASH","FORMAT_COUNT","PUID","MIME_TYPE","FORMAT_NAME",' +
            '"FORMAT_VERSION"')

   #UTF8 with BOM
   droid_utf8 = "\xEF\xBB\xBF" 
   droid_utf8_md5 = droid_utf8 + droid_md5
   droid_utf8_sha1 = droid_utf8 + droid_sha1    
   droid_utf8_sha256 = droid_utf8 + droid_sha256    
   droid_utf8_nohash = droid_utf8 + droid_nohash    
   
   def exportid(self, export):

      f = open(export, 'rb')
      magic = f.readline()
      f.close()

      if magic.strip() == self.droid_md5 \
         or magic.strip() == self.droid_sha1 \
         or magic.strip() == self.droid_sha256 \
         or magic.strip() == self.droid_nohash:
         return self.DROIDTYPE
      if magic.strip() == self.droid_utf8_md5 \
         or magic.strip() == self.droid_utf8_sha1 \
         or magic.strip() == self.droid_utf8_sha256 \
         or magic.strip() == self.droid_utf8_nohash:
         return self.DROIDTYPEBOM
      else:
         return self.UNKTYPE
