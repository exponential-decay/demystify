# -*- coding: utf-8 -*-

"""Rogue Queries for extracting information about Rogues and Heroes from
a format identification extract.
"""


class RogueQueries(object):
    """Object for holding queries associated with rogue identification."""

    SELECT_ALL_FILEPATHS = (
        """SELECT DISTINCT FILE_PATH FROM FILEDATA WHERE FILEDATA.TYPE != 'Folder'"""
    )
    SELECT_ALL_FOLDERS = (
        """SELECT DISTINCT FILE_PATH FROM FILEDATA WHERE FILEDATA.TYPE = 'Folder'"""
    )

    SELECT_EXTENSION_MISMATCHES = (
        "SELECT DISTINCT FILEDATA.FILE_PATH\n"
        "FROM IDRESULTS\n"
        "JOIN FILEDATA on IDRESULTS.FILE_ID = FILEDATA.FILE_ID\n"
        "JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID\n"
        "AND (IDDATA.EXTENSION_MISMATCH='True')"
    )

    @staticmethod
    def get_pronom_identified_files(pro_ns):
        PRONOM_ONLY = (
            "SELECT DISTINCT FILEDATA.FILE_PATH\n"
            "FROM IDRESULTS\n"
            "JOIN FILEDATA on IDRESULTS.FILE_ID = FILEDATA.FILE_ID\n"
            "JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID\n"
            "WHERE (IDDATA.METHOD != 'Container' AND IDDATA.METHOD != 'Signature')\n"
            "AND FILEDATA.TYPE != 'Folder'\n"
            "AND IDDATA.NS_ID="
        )
        query = "{}{}".format(PRONOM_ONLY, pro_ns)
        return query

    @staticmethod
    def get_all_non_ids(ids):
        csv = ",".join(ids)
        csv = "({})".format(csv)
        ALL_IDS = (
            "SELECT DISTINCT FILEDATA.FILE_PATH\n"
            "FROM FILEDATA\n"
            "WHERE FILE_ID NOT IN"
        )
        query = "{}{}".format(ALL_IDS, csv)
        return query

    @staticmethod
    def count_multiple_ids(nscount, paths=False):
        count = "SELECT count(FREQUENCY)\n"
        pathquery = "SELECT PATH\n"
        body = (
            "FROM (SELECT DISTINCT FILEDATA.FILE_PATH AS PATH, COUNT(FILEDATA.FILE_ID) AS FREQUENCY\n"
            "FROM IDRESULTS\n"
            "JOIN FILEDATA on IDRESULTS.FILE_ID = FILEDATA.FILE_ID\n"
            "JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID\n"
            "WHERE (IDDATA.METHOD='Signature' or IDDATA.METHOD='Container')\n"
            "GROUP BY FILEDATA.FILE_ID\n"
            "ORDER BY COUNT(FILEDATA.FILE_ID) DESC)\n"
            "WHERE FREQUENCY > "
        )
        if paths is False:
            query = "{}{}{}".format(count, body, nscount)
            return query
        query = "{}{}{}".format(pathquery, body, nscount)
        return query

    @staticmethod
    def get_rogue_name_paths(itemlist):
        csv = '","'.join(itemlist)
        csv = '("{}")'.format(csv)
        PATHS = "SELECT DISTINCT FILEDATA.FILE_PATH FROM FILEDATA WHERE NAME IN "
        query = "{}{}".format(PATHS, csv)
        return query

    @staticmethod
    def get_rogue_dir_paths(itemlist):
        if len(itemlist) <= 0:
            return ""
        csv = '","'.join(itemlist)
        csv = '("{}")'.format(csv)
        PATHS = "SELECT DISTINCT FILEDATA.FILE_PATH FROM FILEDATA WHERE DIR_NAME IN "
        query = "{}{}".format(PATHS, csv)
        return query
