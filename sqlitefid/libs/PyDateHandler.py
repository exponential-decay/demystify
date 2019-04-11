# -*- coding: utf-8 -*-
import re
import sys
import datetime


class PyDateHandler:
    def getYear(self, datestring):
        if datestring != "":
            datestring = self.get_datestring_without_timezone(datestring)
        if datestring == False:
            datestring = "None"
        return datestring

    def get_datestring_without_timezone(self, datestring):

        newdate = False

        datestring = datestring.replace(
            "Z", ""
        )  # TODO: Handle 'Z' (Nato: Zulu) time (ZIPs only?)
        if len(datestring) == len("0000-00-00T00:00:00+00:00"):
            if "+" in datestring:
                # sf example: 2016-04-02T20:45:12+13:00
                datestring = datestring.rsplit("+", 1)[0]
            else:
                # sf example: 2016-04-02T20:45:12-04:00
                datestring = datestring.rsplit("-", 1)[0]

        # validate the date format, else return exception
        try:
            newdate = int(
                datetime.datetime.strptime(datestring, "%Y-%m-%dT%H:%M:%S").year
            )

        # e.g. ValueError: unconverted data remains: -04:00
        except ValueError as e:
            errstr = (
                "Problem in getYear function, likely due to timezone issues: " + str(e)
            )
            sys.stderr.write(errstr + "\n")

        if newdate == False:
            testyear = datestring.split("-")[0]
            validyear = re.compile("^\d{4}$")
            if (
                len(testyear) == 4 and re.search(validyear, testyear) is not None
            ):  # we should have a year
                newdate = int(testyear)
                sys.stderr.write(
                    "Treating timestamp as a string and setting it to: "
                    + str(testyear)
                    + "\n"
                )

        return int(newdate)
