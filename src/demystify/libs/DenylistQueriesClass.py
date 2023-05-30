# -*- coding: utf-8 -*-

"""Denylist queries for filtering denylist items from a format
identification extract.
"""


class DenylistQueries:
    """Queries for deny list functionality."""

    @staticmethod
    def getfilenames(filenamelist):
        newlist = '%" or FILEDATA.NAME LIKE "%'.join(filenamelist)
        newlist = 'FILEDATA.NAME LIKE "%{}%")'.format(newlist)
        fnamequery = (
            "SELECT DISTINCT FILEDATA.FILE_PATH, FILEDATA.NAME\n"
            "FROM FILEDATA\n"
            "WHERE FILEDATA.TYPE != 'Folder'\n"
            "AND ("
        )
        return "{}{}".format(fnamequery, newlist)

    @staticmethod
    def getdirnames(dirlist):
        newlist = '%" or FILEDATA.NAME LIKE "%'.join(dirlist)
        newlist = 'FILEDATA.NAME LIKE "%{}%")'.format(newlist)
        dirquery = (
            "SELECT DISTINCT FILEDATA.FILE_PATH, FILEDATA.NAME\n"
            "FROM FILEDATA\n"
            "WHERE FILEDATA.TYPE = 'Folder'\n"
            "AND ("
        )
        return "{}{}".format(dirquery, newlist)

    @staticmethod
    def getexts(extlist):
        newlist = '","'.join(extlist)
        newlist = '("{}")'.format(newlist)
        newlist = newlist.replace(".", "")
        extquery = (
            "SELECT DISTINCT FILEDATA.FILE_PATH, FILEDATA.NAME, FILEDATA.EXT\n"
            "FROM FILEDATA\n"
            "WHERE FILEDATA.TYPE != 'Folder'\n"
            "AND FILEDATA.EXT in "
        )
        return "{}{}".format(extquery, newlist)

    @staticmethod
    def getids(idlist):
        newlist = '","'.join(idlist)
        newlist = '("{}")'.format(newlist)
        idquery = (
            "SELECT DISTINCT FILEDATA.FILE_PATH, FILEDATA.NAME, IDDATA.ID || ': ' || IDDATA.FORMAT_NAME || ' ' || IDDATA.FORMAT_VERSION\n"
            "FROM IDRESULTS\n"
            "JOIN FILEDATA on IDRESULTS.FILE_ID = FILEDATA.FILE_ID\n"
            "JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID\n"
            "WHERE IDDATA.METHOD in ('Text','XML','Container','Signature')\n"
            "AND IDDATA.ID in "
        )
        return "{}{}".format(idquery, newlist)
