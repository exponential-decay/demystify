# -*- coding: utf-8 -*-

from __future__ import absolute_import

import sys

from libs.HandleDenylistClass import HandleDenylist


class rogueoutputclass:
    def __init__(self, analysis_results, config, heroes=False):

        self.roguelist = []

        self.dupes = False
        self.pro = False
        self.denylist = False
        self.fnames = False
        self.dirs = False
        self.zero = False
        self.multi = False
        self.ext = False

        self.analysis_results = analysis_results
        self.heroes = heroes
        self.handleconfig(config)

    def handleconfig(self, config):
        if config is not False:
            if config.has_section(HandleDenylist.CFG_ROGUES):
                if config.has_option(
                    HandleDenylist.CFG_ROGUES, HandleDenylist.ROGUE_DUPE
                ):
                    self.dupes = config.get(
                        HandleDenylist.CFG_ROGUES, HandleDenylist.ROGUE_DUPE
                    ).lower()
                if config.has_option(
                    HandleDenylist.CFG_ROGUES, HandleDenylist.ROGUE_PRO
                ):
                    self.pro = config.get(
                        HandleDenylist.CFG_ROGUES, HandleDenylist.ROGUE_PRO
                    ).lower()
                if config.has_option(
                    HandleDenylist.CFG_ROGUES, HandleDenylist.ROGUE_DENY
                ):
                    self.denylist = config.get(
                        HandleDenylist.CFG_ROGUES, HandleDenylist.ROGUE_DENY
                    ).lower()
                if config.has_option(
                    HandleDenylist.CFG_ROGUES, HandleDenylist.ROGUE_FNAMES
                ):
                    self.fnames = config.get(
                        HandleDenylist.CFG_ROGUES, HandleDenylist.ROGUE_FNAMES
                    ).lower()
                if config.has_option(
                    HandleDenylist.CFG_ROGUES, HandleDenylist.ROGUE_DIRS
                ):
                    self.dirs = config.get(
                        HandleDenylist.CFG_ROGUES, HandleDenylist.ROGUE_DIRS
                    ).lower()
                if config.has_option(
                    HandleDenylist.CFG_ROGUES, HandleDenylist.ROGUE_ZERO
                ):
                    self.zero = config.get(
                        HandleDenylist.CFG_ROGUES, HandleDenylist.ROGUE_ZERO
                    ).lower()
                if config.has_option(
                    HandleDenylist.CFG_ROGUES, HandleDenylist.ROGUE_MULTI
                ):
                    self.multi = config.get(
                        HandleDenylist.CFG_ROGUES, HandleDenylist.ROGUE_MULTI
                    ).lower()
                if config.has_option(
                    HandleDenylist.CFG_ROGUES, HandleDenylist.ROGUE_EXT
                ):
                    self.ext = config.get(
                        HandleDenylist.CFG_ROGUES, HandleDenylist.ROGUE_EXT
                    ).lower()

    def outputlist(self, pathlist):
        for x in pathlist:
            if x != "no value":  # todo: no values in duplicates, why?
                sys.stdout.write(str(x) + "\n")

    def rogueorhero(self, pathlist):
        if pathlist is not False and pathlist is not None:
            self.roguelist = self.roguelist + pathlist

    def printTextResults(self):

        if self.dupes == "true":
            if self.analysis_results.hashused is True:
                self.rogueorhero(self.analysis_results.rogue_duplicates)

        if self.zero == "true":
            self.rogueorhero(self.analysis_results.zerobytelist)

        if self.ext == "true":
            self.rogueorhero(self.analysis_results.rogue_extension_mismatches)

        if self.multi == "true":
            if self.analysis_results.multipleidentificationcount > 0:
                self.rogueorhero(
                    self.analysis_results.rogue_multiple_identification_list
                )

        # PRONOM ONLY UNIDENTIFIED
        # output all unidentified files, but also, only when not using DROID output
        if self.analysis_results.tooltype != "droid":
            if (
                self.analysis_results.rogue_pronom_ns_id is not None
                and self.pro == "true"
            ):
                self.rogueorhero(self.analysis_results.rogue_identified_pronom)
            else:
                self.rogueorhero(self.analysis_results.rogue_identified_all)
        else:
            if self.pro == "true":
                self.rogueorhero(self.analysis_results.rogue_identified_pronom)

        if self.fnames == "true":
            self.rogueorhero(self.analysis_results.rogue_file_name_paths)
        if self.dirs == "true":
            self.rogueorhero(self.analysis_results.rogue_dir_name_paths)

        if self.denylist == "true":
            self.rogueorhero(self.analysis_results.rogue_denylist)

        number_allfiles = len(set(self.analysis_results.rogue_all_paths))
        number_alldirs = len(set(self.analysis_results.rogue_all_dirs))

        # Sets make it impossible to duplicate output... Also dealing with paths not files
        # so the numbers will add up slightly strangely if we don't think about folders too...
        if self.heroes is True:
            hfiles = set(self.analysis_results.rogue_all_paths) - set(self.roguelist)
            hfolders = set(self.analysis_results.rogue_all_dirs) - set(self.roguelist)
            hset = list(hfiles) + list(hfolders)

            foldercount = len(hfolders)
            filecount = len(hfiles)

            self.outputlist(hset)
            sys.stderr.write(
                "\n"
                + str(filecount)
                + " out of ("
                + str(number_allfiles)
                + ") files output in rogues gallery."
            )
            sys.stderr.write(
                "\n"
                + str(foldercount)
                + " out of ("
                + str(number_alldirs)
                + ") directories output in rogues gallery."
                + "\n"
            )

        else:
            rset = set(self.roguelist)
            nofolders = len(rset - set(self.analysis_results.rogue_all_dirs))
            foldercount = abs(len(rset) - nofolders)
            filecount = len(rset) - foldercount

            self.outputlist(rset)
            sys.stderr.write(
                "\n"
                + str(filecount)
                + " out of ("
                + str(number_allfiles)
                + ") files output in rogues gallery."
            )
            sys.stderr.write(
                "\n"
                + str(foldercount)
                + " out of ("
                + str(number_alldirs)
                + ") directories output in rogues gallery."
                + "\n"
            )
