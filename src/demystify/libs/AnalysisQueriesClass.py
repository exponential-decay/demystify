# -*- coding: utf-8 -*-

"""Analysis Queries to be used by Demystify to extract as much
information as possible from a format identification extract.
"""

import logging


class AnalysisQueries:
    """Object to hold all queries and helpers related to standard
    analysis functions in Demystify.
    """

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

    SELECT_FREQUENCY_ERRORS = (
        "SELECT FILEDATA.ERROR, COUNT(*) AS TOTAL\n"
        "FROM FILEDATA\n"
        "WHERE FILEDATA.TYPE!='Folder'\n"
        "AND FILEDATA.ERROR!=''\n"
        "AND FILEDATA.ERROR!='None'\n"
        "GROUP BY FILEDATA.ERROR ORDER BY TOTAL DESC"
    )

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
    SELECT_COUNT_ID_METHODS_NONE = (
        "SELECT IDRESULTS.FILE_ID, IDDATA.ID_ID, IDDATA.METHOD, IDDATA.NS_ID\n"
        "FROM IDRESULTS\n"
        "JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID"
    )

    def methods_return_ns_sort(self, ns_id):
        if ns_id is not None:
            return self.SELECT_COUNT_ID_METHODS_PATTERN.replace(
                self.ns_pattern, str(ns_id)
            )
        return self.SELECT_COUNT_ID_METHODS_NONE

    SELECT_COUNT_EXT_MISMATCHES = (
        "SELECT COUNT(distinct(IDRESULTS.FILE_ID))\n"
        "FROM IDRESULTS\n"
        "JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID\n"
        "WHERE IDDATA.EXTENSION_MISMATCH='True'"
    )

    SELECT_COUNT_FORMAT_COUNT = (
        "SELECT COUNT(DISTINCT IDDATA.ID)\n"
        "FROM IDRESULTS\n"
        "JOIN NSDATA on IDDATA.NS_ID = NSDATA.NS_ID\n"
        "JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID\n"
        "WHERE (NSDATA.NS_NAME='pronom')\n"
        "AND (IDDATA.METHOD='Signature' OR IDDATA.METHOD='Container')"
    )

    SELECT_COUNT_OTHER_FORMAT_COUNT = (
        "SELECT COUNT(DISTINCT IDDATA.ID)\n"
        "FROM IDRESULTS\n"
        "JOIN NSDATA on IDDATA.NS_ID = NSDATA.NS_ID\n"
        "JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID\n"
        "WHERE (NSDATA.NS_NAME!='pronom')\n"
        "AND (IDDATA.METHOD='Signature' OR IDDATA.METHOD='Container')"
    )

    # PRONOM and OTHERS Text identifiers as one result
    # PRONOM and OTHERS Text identifiers as one result
    @staticmethod
    def select_count_identifiers(method):
        # XML, Text, Filename
        method_pattern = "{{ method }}"
        SELECT_METHOD_IDENTIFIER = (
            "SELECT COUNT(DISTINCT IDMETHOD)\n"
            "FROM (SELECT IDRESULTS.FILE_ID, IDDATA.ID as IDMETHOD\n"
            "FROM IDRESULTS\n"
            "JOIN NSDATA on IDDATA.NS_ID = NSDATA.NS_ID\n"
            "JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID\n"
            "AND (IDDATA.METHOD='{{ method }}'))"
        )
        return SELECT_METHOD_IDENTIFIER.replace(method_pattern, method)

    @staticmethod
    def select_frequency_identifier_types(method):
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

        SELECT_IDENTIFIER_COUNT = (
            "SELECT 'ns:' || NSDATA.NS_NAME || ' ' || IDDATA.ID, count(IDDATA.ID) as TOTAL\n"
            "FROM IDDATA\n"
            "JOIN NSDATA on IDDATA.NS_ID = NSDATA.NS_ID\n"
            "WHERE IDDATA.BASIS LIKE '{{ identifier }}' OR IDDATA.WARNING LIKE '{{ identifier }}'\n"
            "GROUP BY NSDATA.NS_NAME, IDDATA.iD\n"
            "ORDER BY TOTAL DESC"
        )

        return SELECT_IDENTIFIER_COUNT.replace(identifier_pattern, identifier_text)

    SELECT_COUNT_EXTENSION_RANGE = (
        "SELECT COUNT(DISTINCT FILEDATA.EXT)\n"
        "FROM FILEDATA\n"
        "WHERE (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container')"
    )

    @staticmethod
    def getmimes(idids):
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

    SELECT_PUIDS_EXTENSION_ONLY = (
        "SELECT DISTINCT IDDATA.ID, IDDATA.FORMAT_NAME\n"
        "FROM IDDATA\n"
        "WHERE (IDDATA.METHOD='Extension')"
    )

    SELECT_ALL_UNIQUE_EXTENSIONS = (
        "SELECT DISTINCT FILEDATA.EXT\n"
        "FROM FILEDATA\n"
        "WHERE (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container')\n"
        "AND FILEDATA.EXT!=''"
        "ORDER BY FILEDATA.EXT ASC"
    )

    SELECT_COUNT_EXTENSION_FREQUENCY = (
        "SELECT FILEDATA.EXT, COUNT(*) AS total\n"
        "FROM FILEDATA\n"
        "WHERE (FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container')\n"
        "AND FILEDATA.EXT!=''\n"
        "GROUP BY FILEDATA.EXT ORDER BY TOTAL DESC"
    )

    SELECT_COUNT_DUPLICATE_CHECKSUMS = (
        "SELECT FILEDATA.HASH, COUNT(*) AS TOTAL\n"
        "FROM FILEDATA\n"
        "WHERE FILEDATA.TYPE='File' OR FILEDATA.TYPE='Container'\n"
        "AND FILEDATA.HASH != ''\n"
        "GROUP BY FILEDATA.HASH\n"
        "HAVING TOTAL > 1\n"
        "ORDER BY TOTAL DESC\n"
    )

    # Siegfried only queries...
    SELECT_BYTE_MATCH_BASIS = (
        "SELECT DISTINCT IDDATA.BASIS, IDDATA.ID, FILEDATA.NAME, FILEDATA.SIZE\n"
        "FROM IDRESULTS\n"
        "JOIN FILEDATA on IDRESULTS.FILE_ID = FILEDATA.FILE_ID\n"
        "JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID\n"
        "WHERE IDDATA.METHOD!='Container'\n"
        "AND IDDATA.BASIS LIKE '%byte match%'\n"
    )

    @staticmethod
    def count_multiple_ids(nscount, paths=False):
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

    @staticmethod
    def list_duplicate_paths(checksum):
        return "SELECT FILE_PATH FROM FILEDATA WHERE FILEDATA.HASH='{}' ORDER BY FILEDATA.FILE_PATH;".format(
            checksum
        )

    @staticmethod
    def count_id_instances(id_):
        return "SELECT COUNT(*) AS total FROM IDDATA WHERE (IDDATA.ID='{}'".format(id_)

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
        query = "{}\n{}".format(SELECT_NAMESPACE_AND_IDS, list_)
        if priority is not None:
            query = "{}{}".format(
                query, PRIORITY_ID.replace(self.ns_pattern, str(priority))
            )
        else:
            query = "{}{}".format(query, GROUP_TOTAL)
        return query

    @staticmethod
    def query_from_ids(idlist, idmethod=False):
        if idmethod is not False:
            list_ = "IDRESULTS.FILE_ID IN "
            where = "("
            for i in idlist:
                where = where + str(i) + ", "
        else:
            list_ = "FILEDATA.FILE_ID IN "
            where = "("
            for i in idlist:
                where = where + str(i) + ", "
        list_ = list_ + where.strip(", ") + ")"

        SELECT_PATHS = "SELECT FILEDATA.FILE_PATH\nFROM FILEDATA\n"

        SELECT_NAMESPACE_AND_IDS = (
            "SELECT 'ns:' || NSDATA.NS_NAME || ' ', IDDATA.ID\n"
            "FROM IDRESULTS\n"
            "JOIN NSDATA on IDDATA.NS_ID = NSDATA.NS_ID\n"
            "JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID\n"
            "WHERE IDDATA.METHOD="
        )
        if idmethod is not False:
            SELECT_NAMESPACE_AND_IDS = (
                SELECT_NAMESPACE_AND_IDS + "'" + idmethod + "'"
            )  # which method?
            list_ = "OR {}".format(list_)
            return "{}\n{}".format(SELECT_NAMESPACE_AND_IDS, list_)
        list_ = "WHERE {}".format(list_)
        return SELECT_PATHS + "\n" + list_

    # NAMESPACE QUERIES
    SELECT_NS_DATA = "SELECT * FROM NSDATA"

    @staticmethod
    def get_ns_gap_count_lists(nsid):
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

    @staticmethod
    def get_ns_multiple_ids(nsid):
        SELECT_NAMESPACE_BINARY_IDS1 = (
            "SELECT count(*)\n"
            "FROM (SELECT COUNT(FILEDATA.FILE_ID) AS FREQUENCY\n"
            "FROM IDRESULTS\n"
            "JOIN FILEDATA on IDRESULTS.FILE_ID = FILEDATA.FILE_ID\n"
            "JOIN IDDATA on IDRESULTS.ID_ID = IDDATA.ID_ID\n"
            "WHERE IDDATA.NS_ID="
        )
        SELECT_NAMESPACE_BINARY_IDS2 = (
            "AND (IDDATA.METHOD='Signature' or IDDATA.METHOD='Container')\n"
            "GROUP BY FILEDATA.FILE_ID\n"
            "ORDER BY COUNT(FILEDATA.FILE_ID) DESC)\n"
            "WHERE FREQUENCY >"
        )
        part1 = "{}{}\n".format(SELECT_NAMESPACE_BINARY_IDS1, nsid)
        part2 = "{}{}".format(SELECT_NAMESPACE_BINARY_IDS2, nsid)
        query = "{}{}".format(part1, part2)
        return query

    @staticmethod
    def get_ns_methods(id_, binary=True, method=False):
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
        ID_METHODS_COUNT = "SELECT COUNT(*) FROM IDDATA\n"
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

    ERROR_NOHASH = (
        "Unable to detect duplicates: No HASH algorithm used by identification tool"
    )
