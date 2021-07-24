# -*- coding: utf-8 -*-


class DenylistQueries:
    def getfilenames(self, filenamelist):
        fnamequery = """SELECT DISTINCT FILEDATA.FILE_PATH, FILEDATA.NAME
                      FROM FILEDATA
                      WHERE FILEDATA.TYPE != 'Folder'
                      AND ("""
        newlist = '%" or FILEDATA.NAME LIKE "%'.join(filenamelist)
        newlist = 'FILEDATA.NAME LIKE "%' + newlist + '%")'
        return fnamequery + newlist

    def getdirnames(self, dirlist):
        dirquery = """SELECT DISTINCT FILEDATA.FILE_PATH, FILEDATA.NAME
                    FROM FILEDATA
                    WHERE FILEDATA.TYPE = 'Folder'
                    AND ("""
        newlist = '%" or FILEDATA.NAME LIKE "%'.join(dirlist)
        newlist = 'FILEDATA.NAME LIKE "%' + newlist + '%")'
        return dirquery + newlist

    def getexts(self, extlist):
        extquery = """SELECT DISTINCT FILEDATA.FILE_PATH, FILEDATA.NAME, FILEDATA.EXT
                    FROM FILEDATA
                    WHERE FILEDATA.TYPE != 'Folder'
                    AND FILEDATA.EXT in """
        newlist = '","'.join(extlist)
        newlist = '("' + newlist + '")'
        newlist = newlist.replace(".", "")
        return extquery + newlist

    def getids(self, idlist):
        idquery = """SELECT DISTINCT FILEDATA.FILE_PATH, FILEDATA.NAME, IDDATA.ID || ": " || IDDATA.FORMAT_NAME || " " || IDDATA.FORMAT_VERSION
                   FROM IDRESULTS
                   JOIN FILEDATA on IDRESULTS.FILE_ID = FILEDATA.FILE_ID
                   JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                   WHERE IDDATA.METHOD in ("Text","XML","Container","Signature")
                   AND IDDATA.ID in """
        newlist = '","'.join(idlist)
        newlist = '("' + newlist + '")'
        return idquery + newlist
