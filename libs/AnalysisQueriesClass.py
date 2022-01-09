# -*- coding: utf-8 -*-

import logging


class AnalysisQueries:

    SELECT_FILENAMES = "SELECT FILEDATA.NAME FROM FILEDATA"
    SELECT_DIRNAMES = "SELECT DISTINCT FILEDATA.DIR_NAME FROM FILEDATA"

    SELECT_HASH = "SELECT DBMD.HASH_TYPE FROM DBMD"
    SELECT_TOOL = "SELECT DBMD.TOOL_TYPE FROM DBMD"

    SELECT_COLLECTION_SIZE = "SELECT SUM(FILEDATA.SIZE) FROM FILEDATA"
    SELECT_COUNT_FILES = "SELECT COUNT(FILEDATA.FILE_ID) FROM FILEDATA WHERE (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container')"

    SELECT_COUNT_CONTAINERS = (
        "SELECT COUNT(FILEDATA.FILE_ID) FROM FILEDATA WHERE FILEDATA.TYPE='Container'"
    )
    SELECT_CONTAINER_TYPES = (
        "SELECT DISTINCT FILEDATA.EXT FROM FILEDATA WHERE FILEDATA.TYPE='Container'"
    )
    SELECT_COUNT_FILES_IN_CONTAINERS = "SELECT COUNT(FILEDATA.FILE_ID) FROM FILEDATA WHERE (FILEDATA.URI_SCHEME!='file') AND (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container')"

    SELECT_COUNT_ZERO_BYTE_FILES = "SELECT COUNT(FILEDATA.SIZE) FROM FILEDATA WHERE (FILEDATA.TYPE!='Folder') AND (FILEDATA.SIZE='0')"
    SELECT_ZERO_BYTE_FILEPATHS = "SELECT FILEDATA.FILE_PATH FROM FILEDATA WHERE FILEDATA.TYPE='File' AND FILEDATA.SIZE='0'"

    SELECT_COUNT_FOLDERS = (
        "SELECT COUNT(FILEDATA.FILE_ID) FROM FILEDATA WHERE FILEDATA.TYPE='Folder'"
    )

    SELECT_COUNT_UNIQUE_FILENAMES = "SELECT COUNT(DISTINCT FILEDATA.NAME) FROM FILEDATA WHERE (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container')"
    SELECT_COUNT_UNIQUE_DIRNAMES = (
        "SELECT COUNT(DISTINCT FILEDATA.DIR_NAME) FROM FILEDATA"
    )

    SELECT_COUNT_NAMESPACES = "SELECT COUNT(NSDATA.NS_ID) FROM NSDATA"

    SELECT_FREQUENCY_ERRORS = """SELECT FILEDATA.ERROR, COUNT(*) AS TOTAL
                                 FROM FILEDATA
                                 WHERE FILEDATA.TYPE!='Folder'
                                 AND FILEDATA.ERROR!=''
                                 GROUP BY FILEDATA.ERROR ORDER BY TOTAL DESC"""

    ns_pattern = "{{ ns_id }}"
    SELECT_COUNT_ID_METHODS_PATTERN = (
        "SELECT IDRESULTS.FILE_ID, IDDATA.ID_ID, IDDATA.METHOD, IDDATA.NS_ID\n"
        "FROM IDRESULTS\n"
        "JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID\n"
        "ORDER BY\n"
        "CASE IDDATA.NS_ID\n"
        "WHEN '{{ ns_id }}' THEN 1\n"
        "ELSE 2\n"
        "END\n"
    )

    # Prority of results is based on order input to database...
    SELECT_COUNT_ID_METHODS_NONE = """SELECT IDRESULTS.FILE_ID, IDDATA.ID_ID, IDDATA.METHOD, IDDATA.NS_ID
                                    FROM IDRESULTS
                                    JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID"""

    def methods_return_ns_sort(self, ns_id):
        if ns_id is not None:
            return self.SELECT_COUNT_ID_METHODS_PATTERN.replace(
                self.ns_pattern, str(ns_id)
            )
        else:
            return self.SELECT_COUNT_ID_METHODS_NONE

    SELECT_COUNT_EXT_MISMATCHES = """SELECT COUNT(distinct(IDRESULTS.FILE_ID))
                                       FROM IDRESULTS
                                       JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                                       WHERE IDDATA.EXTENSION_MISMATCH='True'"""

    # TODO: Currency is PUID, what do we do for Tika and Freedesktop and others?
    SELECT_COUNT_FORMAT_COUNT = """SELECT COUNT(DISTINCT IDDATA.ID)
                                    FROM IDRESULTS
                                    JOIN NSDATA on IDDATA.NS_ID = NSDATA.NS_ID
                                    JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                                    WHERE (NSDATA.NS_NAME='pronom')
                                    AND (IDDATA.METHOD='Signature' OR IDDATA.METHOD='Container')"""

    SELECT_COUNT_OTHER_FORMAT_COUNT = """SELECT COUNT(DISTINCT IDDATA.ID)
                                       FROM IDRESULTS
                                       JOIN NSDATA on IDDATA.NS_ID = NSDATA.NS_ID
                                       JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                                       WHERE (NSDATA.NS_NAME!='pronom')
                                       AND (IDDATA.METHOD='Signature' OR IDDATA.METHOD='Container')"""

    # PRONOM and OTHERS Text identifiers as one result
    # PRONOM and OTHERS Text identifiers as one result
    def select_count_identifiers(self, method):
        # XML, Text, Filename
        method_pattern = "{{ method }}"
        SELECT_METHOD_IDENTIFIER = """SELECT COUNT(DISTINCT IDMETHOD)
                                    FROM (SELECT IDRESULTS.FILE_ID, IDDATA.ID as IDMETHOD
                                    FROM IDRESULTS
                                    JOIN NSDATA on IDDATA.NS_ID = NSDATA.NS_ID
                                    JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                                    AND (IDDATA.METHOD='{{ method }}'))"""
        return SELECT_METHOD_IDENTIFIER.replace(method_pattern, method)

    def select_frequency_identifier_types(self, method):
        # treating new identifer capabilities as first class citizens
        # %match on filename%    %xml match%    %text match%
        identifier_pattern = "{{ identifier }}"
        identifier_text = ""

        method = method.lower()
        if method == "xml":
            identifier_text = "%xml match%"
        elif method == "text":
            identifier_text = "%text match%"
        elif method == "filename":
            identifier_text = "%match on filename%"

        SELECT_IDENTIFIER_COUNT = """SELECT "ns:" || NSDATA.NS_NAME || " " || IDDATA.ID, count(IDDATA.ID) as TOTAL
                                    FROM IDDATA
                                    JOIN NSDATA on IDDATA.NS_ID = NSDATA.NS_ID
                                    WHERE IDDATA.BASIS LIKE '{{ identifier }}' OR IDDATA.WARNING LIKE '{{ identifier }}'
                                    GROUP BY NSDATA.NS_NAME, IDDATA.iD
                                    ORDER BY TOTAL DESC"""

        return SELECT_IDENTIFIER_COUNT.replace(identifier_pattern, identifier_text)

    SELECT_COUNT_EXTENSION_RANGE = """SELECT COUNT(DISTINCT FILEDATA.EXT)
                                       FROM FILEDATA
                                       WHERE (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container')"""

    SELECT_METHOD_FREQUENCY_COUNT = """SELECT IDDATA.METHOD, COUNT(*) AS total
                                       FROM IDRESULTS
                                       JOIN FILEDATA on IDRESULTS.FILE_ID = FILEDATA.FILE_ID
                                       JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                                       WHERE (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container')
                                       GROUP BY IDDATA.METHOD ORDER BY TOTAL DESC"""

    def getmimes(self, idids):
        """Construct mime query using a set of IDs provided to the
        function.

            NB. Select the gamut of MIMEs in the accession/extract, not
                counts.
        """
        mimes = [id_[1] for id_ in idids]
        query1 = (
            "SELECT IDDATA.MIME_TYPE, COUNT(*) AS total\n"
            "FROM IDRESULTS\n"
            "JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID\n"
            "WHERE IDRESULTS.ID_ID IN"
        )
        query2 = (
            "AND (IDDATA.MIME_TYPE!='None' and IDDATA.MIME_TYPE!='none' and IDDATA.MIME_TYPE!='')\n"
            "GROUP BY IDDATA.MIME_TYPE ORDER BY TOTAL DESC\n"
        )
        listing = "({})".format(", ".join(mimes))
        query = "{}{}{}".format(query1, listing, query2)
        return query

    SELECT_BINARY_MATCH_COUNT = (
        "SELECT NSDATA.NS_NAME, IDDATA.ID, COUNT(IDDATA.ID) as TOTAL\n"
        "FROM IDRESULTS\n"
        "JOIN NSDATA on IDDATA.NS_ID = NSDATA.NS_ID\n"
        "JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID\n"
        "WHERE (IDDATA.METHOD='Signature' OR IDDATA.METHOD='Container')\n"
        "GROUP BY IDDATA.ID ORDER BY NSDATA.NS_NAME, TOTAL DESC"
    )

    SELECT_YEAR_FREQUENCY_COUNT = (
        "SELECT FILEDATA.YEAR, COUNT(FILEDATA.YEAR) AS total\n"
        "FROM FILEDATA\n"
        "WHERE (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container')\n"
        "GROUP BY FILEDATA.YEAR ORDER BY TOTAL DESC\n"
    )

    # TODO: THIS STAT NEEDS REVISITING IN LIGHT OF SIEGFRIED
    # MULTIPLE IDS WILL BE REFLECTED USING MULTIPLE NAMESPACE PLACES - HOW TO REPORT ON?
    SELECT_PUIDS_EXTENSION_ONLY = """SELECT DISTINCT IDDATA.ID, IDDATA.FORMAT_NAME
                                    FROM IDDATA
                                    WHERE (IDDATA.METHOD='Extension')"""

    SELECT_ALL_UNIQUE_EXTENSIONS = """SELECT DISTINCT FILEDATA.EXT
                                    FROM FILEDATA
                                    WHERE (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container')
                                    AND FILEDATA.EXT!=''"""

    SELECT_COUNT_EXTENSION_FREQUENCY = """SELECT FILEDATA.EXT, COUNT(*) AS total
                                       FROM FILEDATA
                                       WHERE (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container')
                                       AND FILEDATA.EXT!=''
                                       GROUP BY FILEDATA.EXT ORDER BY TOTAL DESC"""

    # TODO: REMOVE THIS? IT DOESN'T SEEM TO BE USED...
    # MULTIPLE ID FOR FILES GREATER THAN ZERO BYTES
    '''
    SELECT_MULTIPLE_ID_PATHS = """SELECT FILEDATA.FILE_PATH
                                 FROM IDRESULTS
                                 JOIN FILEDATA on IDRESULTS.FILE_ID = FILEDATA.FILE_ID
                                 JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                                 WHERE (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container')
                                 AND (IDDATA.FORMAT_COUNT > 1)
                                 AND (FILEDATA.SIZE > 0)"""
    '''

    SELECT_COUNT_DUPLICATE_CHECKSUMS = """SELECT FILEDATA.HASH, COUNT(*) AS TOTAL
                                          FROM FILEDATA
                                          WHERE FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container'
                                          AND FILEDATA.HASH != ''
                                          GROUP BY FILEDATA.HASH
                                          HAVING TOTAL > 1
                                          ORDER BY TOTAL DESC"""
    # Siegfried only queries...
    SELECT_BYTE_MATCH_BASIS = (
        "SELECT DISTINCT IDDATA.BASIS, IDDATA.ID, FILEDATA.NAME, FILEDATA.SIZE\n"
        "FROM IDRESULTS\n"
        "JOIN FILEDATA on IDRESULTS.FILE_ID = FILEDATA.FILE_ID\n"
        "JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID\n"
        "WHERE IDDATA.METHOD!='Container'\n"
        "AND IDDATA.BASIS LIKE '%byte match%'\n"
    )

    def count_multiple_ids(self, nscount, paths=False):
        """Count multiple entries for identification where the count is
        greater than the namespace count. E.g. a file has a multiple ID
        if it uses 3 namespaces and the frequency is 4, but not if the
        frequency is 3.
        """
        if paths is False:
            body = (
                "SELECT count(FREQUENCY)\n"
                "FROM (SELECT FILEDATA.FILE_PATH AS PATH, COUNT(FILEDATA.FILE_ID) AS FREQUENCY\n"
                "FROM IDRESULTS\n"
                "JOIN FILEDATA on IDRESULTS.FILE_ID = FILEDATA.FILE_ID\n"
                "JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID\n"
                "WHERE (IDDATA.METHOD='Signature' or IDDATA.METHOD='Container')\n"
                "GROUP BY FILEDATA.FILE_ID\n"
                "ORDER BY COUNT(FILEDATA.FILE_ID) DESC)\n"
                "WHERE FREQUENCY > "
            )
            query = "{}{}".format(body, nscount)
            return query
        body = (
            "SELECT PATH\n"
            "FROM (SELECT FILEDATA.FILE_PATH AS PATH, COUNT(FILEDATA.FILE_ID) AS FREQUENCY\n"
            "FROM IDRESULTS\n"
            "JOIN FILEDATA on IDRESULTS.FILE_ID = FILEDATA.FILE_ID\n"
            "JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID\n"
            "WHERE (IDDATA.METHOD='Signature' or IDDATA.METHOD='Container')\n"
            "GROUP BY FILEDATA.FILE_ID\n"
            "ORDER BY COUNT(FILEDATA.FILE_ID) DESC)\n"
            "WHERE FREQUENCY > "
        )
        query = "{}{}".format(body, nscount)
        return query

    def list_duplicate_paths(self, checksum):
        return "SELECT FILE_PATH FROM FILEDATA WHERE FILEDATA.HASH='{}' ORDER BY FILEDATA.FILE_PATH;".format(
            checksum
        )

    def count_id_instances(self, id):
        return "SELECT COUNT(*) AS total FROM IDDATA WHERE (IDDATA.ID='" + id + "')"

    def search_id_instance_filepaths(self, id):
        query_part1 = """SELECT FILEDATA.FILE_PATH
                        FROM IDRESULTS
                        JOIN FILEDATA on IDRESULTS.FILE_ID = FILEDATA.FILE_ID
                        JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                        WHERE IDDATA.ID='"""

        query_part2 = id + "' ORDER BY FILEDATA.FILE_PATH DESC"
        return query_part1 + query_part2

    def query_from_idrows(self, idlist, priority=None):
        list_ = "WHERE IDRESULTS.ID_ID IN "
        where = "("
        for i in idlist:
            where = "{}{}, ".format(where, i[1])
        list_ = "{}{})\n".format(list_, where.strip(", "))
        SELECT_NAMESPACE_AND_IDS = (
            "SELECT 'ns:' || NSDATA.NS_NAME || ' ', IDDATA.ID, IDDATA.FORMAT_NAME, IDDATA.BASIS, IDDATA.FORMAT_VERSION, IDDATA.NS_ID, COUNT(IDDATA.ID) AS TOTAL\n"
            "FROM IDRESULTS\n"
            "JOIN NSDATA on IDDATA.NS_ID = NSDATA.NS_ID\n"
            "JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID\n"
        )
        PRIORITY_ID = (
            "GROUP BY IDDATA.ID\n"
            "ORDER BY\n"
            "CASE IDDATA.NS_ID\n"
            "WHEN '{{ ns_id }}' THEN 1\n"
            "ELSE 2\n"
            "END\n"
        )
        GROUP_TOTAL = """GROUP BY IDDATA.ID ORDER BY TOTAL DESC"""
        SELECT_NAMESPACE_AND_IDS = SELECT_NAMESPACE_AND_IDS
        query = "{}\n{}".format(SELECT_NAMESPACE_AND_IDS, list_)
        if priority is not None:
            query = "{}{}".format(
                query, PRIORITY_ID.replace(self.ns_pattern, str(priority))
            )
        else:
            query = "{}{}".format(query, GROUP_TOTAL)
        return query

    def query_from_idrows_(self, idlist, priority=None):
        list = "WHERE IDRESULTS.ID_ID IN "
        where = "("
        for i in idlist:
            where = where + str(i[1]) + ", "
        list = list + where.strip(", ") + ")"

        SELECT_NAMESPACE_AND_IDS = """SELECT 'ns:' || NSDATA.NS_NAME || ' ', IDDATA.ID, IDDATA.FORMAT_NAME, IDDATA.BASIS, IDDATA.FORMAT_VERSION, IDDATA.NS_ID
                                    FROM IDRESULTS
                                    JOIN NSDATA on IDDATA.NS_ID = NSDATA.NS_ID
                                    JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID"""

        PRIORITY_ID = """ORDER BY
                        CASE IDDATA.NS_ID
                           WHEN '{{ ns_id }}' THEN 1
                           ELSE 2
                        END"""
        # print list
        SELECT_NAMESPACE_AND_IDS = SELECT_NAMESPACE_AND_IDS
        query = SELECT_NAMESPACE_AND_IDS + "\n" + list
        if priority is not None:
            query = query + PRIORITY_ID.replace(self.ns_pattern, str(priority))
        return query

    # IT MIGHT BE WORTH PULLING THIS APART BUT WILL SEE...
    def query_from_ids(self, idlist, idmethod=False):

        if idmethod is not False:
            list = "IDRESULTS.FILE_ID IN "
            where = "("
            for i in idlist:
                where = where + str(i) + ", "
        else:
            list = "FILEDATA.FILE_ID IN "
            where = "("
            for i in idlist:
                where = where + str(i) + ", "
        list = list + where.strip(", ") + ")"

        SELECT_PATHS = """SELECT FILEDATA.FILE_PATH
                        FROM FILEDATA"""

        SELECT_NAMESPACE_AND_IDS = """SELECT 'ns:' || NSDATA.NS_NAME || " ", IDDATA.ID
                                    FROM IDRESULTS
                                    JOIN NSDATA on IDDATA.NS_ID = NSDATA.NS_ID
                                    JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                                    WHERE IDDATA.METHOD="""
        if idmethod is not False:
            SELECT_NAMESPACE_AND_IDS = (
                SELECT_NAMESPACE_AND_IDS + "'" + idmethod + "'"
            )  # which method?
            list = "OR " + list
            return SELECT_NAMESPACE_AND_IDS + "\n" + list
        else:
            list = "WHERE " + list
            return SELECT_PATHS + "\n" + list

    # NAMESPACE QUERIES
    SELECT_NS_DATA = "SELECT * FROM NSDATA"

    def get_ns_gap_count_lists(self, nsid):
        """Return a query for files not identified through Signature or
        Container methods for a given namespace ID.
        """
        return (
            "SELECT IDRESULTS.FILE_ID\n"
            "FROM IDRESULTS\n"
            "JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID\n"
            "WHERE (IDDATA.METHOD!='Signature' AND IDDATA.METHOD!='Container')\n"
            "AND IDDATA.NS_ID={}"
        ).format(nsid)

    def get_ns_multiple_ids(self, nsid, nscount):
        SELECT_NAMESPACE_BINARY_IDS1 = """SELECT count(*)
                                          FROM (SELECT COUNT(FILEDATA.FILE_ID) AS FREQUENCY
                                          FROM IDRESULTS
                                          JOIN FILEDATA on IDRESULTS.FILE_ID = FILEDATA.FILE_ID
                                          JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
                                          WHERE IDDATA.NS_ID="""

        SELECT_NAMESPACE_BINARY_IDS2 = """AND (IDDATA.METHOD='Signature' or IDDATA.METHOD='Container')
                                          GROUP BY FILEDATA.FILE_ID
                                          ORDER BY COUNT(FILEDATA.FILE_ID) DESC)
                                          WHERE FREQUENCY >"""

        part1 = SELECT_NAMESPACE_BINARY_IDS1 + str(nsid) + "\n"
        part2 = SELECT_NAMESPACE_BINARY_IDS2 + str(nsid)
        query = part1 + part2
        return query

    def get_ns_methods(self, id_, binary=True, method=False):
        """Retrieve various counts about the data in the report based
        on namespace. E.g.

          SELECT COUNT(DISTINCT IDRESULTS.FILE_ID)
          FROM IDRESULTS
          JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID
          WHERE NS_ID=1
          AND (IDDATA.METHOD='Signature' or IDDATA.METHOD='Container')

        """
        WHERE_NS = "WHERE NS_ID={}".format(id_)
        COUNT_IDS_NS = (
            "SELECT COUNT(DISTINCT IDRESULTS.FILE_ID)\n"
            "FROM IDRESULTS\n"
            "JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID\n"
        )
        COUNT_IDS_METHODS = (
            "AND (IDDATA.METHOD='Signature' or IDDATA.METHOD='Container')"
        )
        ID_METHODS_COUNT = "SELECT COUNT(*) " "FROM IDDATA\n"
        ID_METHODS_METHOD = "AND IDDATA.METHOD="
        query = ""
        if binary is True:
            query = "{}{}\n{}".format(COUNT_IDS_NS, WHERE_NS, COUNT_IDS_METHODS)
        elif method is not False:
            query = "{}{}\n{}'{}'".format(
                ID_METHODS_COUNT, WHERE_NS, ID_METHODS_METHOD, method
            )
        logging.debug("get_ns_methods: %s", query)
        return query

    # ERRORS, TODO: Place somewhere else?
    ERROR_NOHASH = (
        "Unable to detect duplicates: No HASH algorithm used by identification tool"
    )
