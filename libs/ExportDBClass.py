﻿# -*- coding: utf-8 -*-

from __future__ import absolute_import

import sqlite3
import sys


class ExportDB:
    def exportDB(self, db):
        connection = sqlite3.connect(db)

        cursor = connection.cursor()

        cursor.execute(
            "PRAGMA table_info(droid)"
        )  # get table structure, column2 our headers
        header = ""
        for row in cursor.fetchall():
            header = header + '"' + row[1].encode("utf-8") + '",'
        header = header.strip(",") + "\n"
        sys.stdout.write(header)

        cursor.execute("select * from droid")  # get content of DB
        for row in cursor.fetchall():
            str = ""
            for x in range(len(row)):
                str = str + '"' + row[x].encode("utf-8") + '"' + ","
            str = str.strip(",") + "\n"
            sys.stdout.write(str)

        cursor.close()
        connection.close()
