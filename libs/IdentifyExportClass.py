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

   SFTYPE = "siegfried"

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

   sf_orig = ('---' + '\x0A' + 'siegfried   :')

   #UTF8 with BOM
   droid_utf8 = "\xEF\xBB\xBF" 
   droid_utf8_md5 = droid_utf8 + droid_md5
   droid_utf8_sha1 = droid_utf8 + droid_sha1    
   droid_utf8_sha256 = droid_utf8 + droid_sha256    
   droid_utf8_nohash = droid_utf8 + droid_nohash    
   
   def exportid(self, export):

      f = open(export, 'rb')
      droid_magic = f.readline()
      sf_magic = droid_magic + f.readline()
      f.close()

      if droid_magic.strip() == self.droid_md5 \
         or droid_magic.strip() == self.droid_sha1 \
         or droid_magic.strip() == self.droid_sha256 \
         or droid_magic.strip() == self.droid_nohash:
         return self.DROIDTYPE
      if droid_magic.strip() == self.droid_utf8_md5 \
         or droid_magic.strip() == self.droid_utf8_sha1 \
         or droid_magic.strip() == self.droid_utf8_sha256 \
         or droid_magic.strip() == self.droid_utf8_nohash:
         return self.DROIDTYPEBOM
      if self.sf_orig in sf_magic.strip():
         return self.SFTYPE
      else:
         return self.UNKTYPE
