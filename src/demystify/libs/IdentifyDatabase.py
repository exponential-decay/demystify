# -*- coding: utf-8 -*-

"""IdentifyDatabase

Enables identification of a sqlite3 database to ensure that the input
data for the calling application is correct.
"""


class IdentifyDB:
    """IdentifyDB."""

    SQLITE_DB = "SQLITE 3"
    UNKNOWN_DB = "unknown"

    # 'SQLite format 3'
    sqlite3 = b"\x53\x51\x4C\x69\x74\x65\x20\x66\x6F\x72\x6D\x61\x74\x20\x33"

    def identify_export(self, database_path):
        """Reads an input file and checks whether it is an sqlite3
        database.

        :param database_path: path to database to read (String)
        :return: `True` if sqlite3 or `False` if not (Boolean)
        """
        db_magic = None
        try:
            with open(database_path, "rb") as f:
                db_magic = f.read(len(self.sqlite3))
        except IOError:
            return False
        if db_magic == self.sqlite3:
            return True
        return False
