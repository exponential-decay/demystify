# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging

from libs.HandleDenylistClass import HandleDenylist


class rogueoutputclass:
    def __init__(self, analysis_results, config, heroes=False):

        self.roguelist = []

        self.unidentified = False
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
                    HandleDenylist.CFG_ROGUES, HandleDenylist.ROGUE_UNIDENTIFIED
                ):
                    self.unidentified = config.get(
                        HandleDenylist.CFG_ROGUES, HandleDenylist.ROGUE_UNIDENTIFIED
                    ).lower()
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

    def outputlist(self, path_list):
        for path in path_list:
            if path == "no value" or path == "" or path == None:
                continue
            print("{}".format(path))
        assert False, "stuck here"

    def rogueorhero(self, pathlist):
        if pathlist:
            self.roguelist = self.roguelist + pathlist

    def printTextResults(self):
        if self.dupes == "true":
            print("dupes")
            if self.analysis_results.hashused is True:
                self.rogueorhero(self.analysis_results.rogue_duplicates)

        if self.zero == "true":
            print("zero")
            self.rogueorhero(self.analysis_results.zerobytelist)

        if self.ext == "true":
            print("ext")
            self.rogueorhero(self.analysis_results.rogue_extension_mismatches)

        if self.multi == "true":
            print('multi')
            if self.analysis_results.multipleidentificationcount > 0:
                self.rogueorhero(
                    self.analysis_results.rogue_multiple_identification_list
                )
        # PRONOM ONLY UNIDENTIFIED
        # output all unidentified files, but also, only when not using DROID output
        if self.unidentified == "true":
            if self.analysis_results.tooltype != "droid":
                print("blah")
                if (
                    self.analysis_results.rogue_pronom_ns_id is not None
                    and self.pro == "true"
                ):
                    self.rogueorhero(self.analysis_results.rogue_identified_pronom)
                else:
                    self.rogueorhero(self.analysis_results.rogue_identified_all)
            else:
                print("blah2")
                if self.pro == "true":
                    self.rogueorhero(self.analysis_results.rogue_identified_pronom)
        if self.fnames == "true":
            print("fnames")
            self.rogueorhero(self.analysis_results.rogue_file_name_paths)
        if self.dirs == "true":
            print("dirs")
            self.rogueorhero(self.analysis_results.rogue_dir_name_paths)

        if self.denylist == "true":
            print("deny")
            print("XXXXX", self.denylist)
            self.rogueorhero(self.analysis_results.rogue_denylist)

        try:
            number_allfiles = len(set(self.analysis_results.rogue_all_paths))
            number_alldirs = len(set(self.analysis_results.rogue_all_dirs))
        except TypeError:
            logging.warning("Rogues and heroes lists not created: Check config for Rogues being turned off")
            return

        if self.heroes is True:
            hero_files = set(self.analysis_results.rogue_all_paths) - set(
                self.roguelist
            )
            hero_folders = set(self.analysis_results.rogue_all_dirs) - set(
                self.roguelist
            )
            hero_set = list(hero_files) + list(hero_folders)
            foldercount = len(hero_folders)
            filecount = len(hero_files)
            self.outputlist(hero_set)
            logging.info(
                "%s out of (%s) files output in heroes gallery",
                filecount,
                number_allfiles,
            )
            logging.info(
                "%s out of (%s) directories output in heroes gallery",
                foldercount,
                number_alldirs,
            )
            return
        rogue_set = set(self.roguelist)
        nofolders = len(rogue_set - set(self.analysis_results.rogue_all_dirs))
        foldercount = abs(len(rogue_set) - nofolders)
        filecount = len(rogue_set) - foldercount
        self.outputlist(rogue_set)
        logging.info(
            "%s out of (%s) files output in rogues gallery", filecount, number_allfiles
        )
        logging.info(
            "%s out of (%s) directories output in rogues gallery",
            foldercount,
            number_alldirs,
        )
