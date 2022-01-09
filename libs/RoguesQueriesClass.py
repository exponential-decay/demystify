# -*- coding: utf-8 -*-

"""Rogue Queries for extracting information about Rogues and Heroes from
a format identification extract.
"""


class RogueQueries:

    SELECT_ALL_FILEPATHS = (
        """SELECT DISTINCT FILE_PATH FROM FILEDATA WHERE FILEDATA.TYPE != 'Folder'"""
    )
    SELECT_ALL_FOLDERS = (
        """SELECT DISTINCT FILE_PATH FROM FILEDATA WHERE FILEDATA.TYPE = 'Folder'"""
    )

    SELECT_EXTENSION_MISMATCHES = """SELECT DISTINCT FILEDATA.FILE_PATH
                                    FROM IDRESULTS
                                    JOIN FILEDATA on IDRESULTS.FILE_ID = FILEDATA.FILE_ID
                                    JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                                    AND (IDDATA.EXTENSION_MISMATCH='True')"""

    def get_pronom_identified_files(self, pro_ns):
        PRONOM_ONLY = """SELECT DISTINCT FILEDATA.FILE_PATH
                       FROM IDRESULTS
                       JOIN FILEDATA on IDRESULTS.FILE_ID = FILEDATA.FILE_ID
                       JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                       WHERE (IDDATA.METHOD != 'Container' AND IDDATA.METHOD != 'Signature')
                       AND FILEDATA.TYPE != 'Folder'
                       AND IDDATA.NS_ID="""
        query = PRONOM_ONLY + str(pro_ns)
        return query

    def get_all_non_ids(self, ids):
        ALL_IDS = """SELECT DISTINCT FILEDATA.FILE_PATH
                   FROM FILEDATA
                   WHERE FILE_ID NOT IN"""
        csv = ",".join(ids)
        csv = "(" + csv + ")"
        query = ALL_IDS + csv
        return query

    def count_multiple_ids(self, nscount, paths=False):
        count = "SELECT count(FREQUENCY)" + "\n"
        pathquery = "SELECT PATH" + "\n"
        body = """FROM (SELECT DISTINCT FILEDATA.FILE_PATH AS PATH, COUNT(FILEDATA.FILE_ID) AS FREQUENCY
                  FROM IDRESULTS
                  JOIN FILEDATA on IDRESULTS.FILE_ID = FILEDATA.FILE_ID
                  JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                  WHERE (IDDATA.METHOD='Signature' or IDDATA.METHOD='Container')
                  GROUP BY FILEDATA.FILE_ID
                  ORDER BY COUNT(FILEDATA.FILE_ID) DESC)
                  WHERE FREQUENCY > """

        query = ""
        if paths is False:
            query = count + body + str(nscount)
        else:
            query = pathquery + body + str(nscount)
        return query

    def get_rogue_name_paths(self, itemlist):
        PATHS = """SELECT DISTINCT FILEDATA.FILE_PATH FROM FILEDATA
                 WHERE NAME IN """
        csv = '","'.join(itemlist)
        csv = '("' + csv + '")'
        query = PATHS + csv
        return query

    def get_rogue_dir_paths(self, itemlist):
        query = ""
        if len(itemlist) > 0:
            PATHS = """SELECT DISTINCT FILEDATA.FILE_PATH FROM FILEDATA
                    WHERE DIR_NAME IN """
            csv = '","'.join(itemlist)
            csv = '("' + csv + '")'
            query = PATHS + csv
        return query
