# -*- coding: utf-8 -*-

import configparser as ConfigParser
import logging

try:
    from src.demystify.libs.HandleDenylistClass import HandleDenylist
except ModuleNotFoundError:
    # Needed for PyPi import.
    from demystify.libs.HandleDenylistClass import HandleDenylist


class rogueoutputclass:
    """Object to help encapsulate rogue output functions."""

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

    @staticmethod
    def _get_option(config, key, value):
        """Wrap handling of option getter to improve readability."""
        try:
            val = config.get(key, value)
            if val.lower() == "true":
                return True
        except (ConfigParser.NoOptionError, AttributeError):
            pass
        return False

    def handleconfig(self, config):
        if config is not False and config.has_section(HandleDenylist.CFG_ROGUES):
            self.unidentified = self._get_option(
                config, HandleDenylist.CFG_ROGUES, HandleDenylist.ROGUE_UNIDENTIFIED
            )
            self.dupes = self._get_option(
                config, HandleDenylist.CFG_ROGUES, HandleDenylist.ROGUE_DUPE
            )
            self.pro = self._get_option(
                config, HandleDenylist.CFG_ROGUES, HandleDenylist.ROGUE_PRO
            )
            self.denylist = self._get_option(
                config, HandleDenylist.CFG_ROGUES, HandleDenylist.ROGUE_DENY
            )
            self.fnames = self._get_option(
                config, HandleDenylist.CFG_ROGUES, HandleDenylist.ROGUE_FNAMES
            )
            self.dirs = self._get_option(
                config, HandleDenylist.CFG_ROGUES, HandleDenylist.ROGUE_DIRS
            )
            self.zero = self._get_option(
                config, HandleDenylist.CFG_ROGUES, HandleDenylist.ROGUE_ZERO
            )
            self.multi = self._get_option(
                config, HandleDenylist.CFG_ROGUES, HandleDenylist.ROGUE_MULTI
            )
            self.ext = self._get_option(
                config, HandleDenylist.CFG_ROGUES, HandleDenylist.ROGUE_EXT
            )

    @staticmethod
    def outputlist(path_list):
        for path in path_list:
            if path == "no value" or path == "" or path is None:
                continue
            print("{}".format(path))

    def rogueorhero(self, pathlist):
        if pathlist:
            self.roguelist = self.roguelist + pathlist

    def printTextResults(self):
        if self.dupes is True:
            if self.analysis_results.hashused is True:
                self.rogueorhero(self.analysis_results.rogue_duplicates)

        if self.zero is True:
            self.rogueorhero(self.analysis_results.zerobytelist)

        if self.ext is True:
            self.rogueorhero(self.analysis_results.rogue_extension_mismatches)

        if self.multi is True:
            if int(self.analysis_results.multipleidentificationcount) > 0:
                self.rogueorhero(
                    self.analysis_results.rogue_multiple_identification_list
                )
        # PRONOM ONLY UNIDENTIFIED
        # output all unidentified files, but also, only when not using DROID output
        if self.unidentified is True:
            if self.analysis_results.tooltype != "droid":
                if (
                    self.analysis_results.rogue_pronom_ns_id is not None
                    and self.pro == "true"
                ):
                    self.rogueorhero(self.analysis_results.rogue_identified_pronom)
                else:
                    self.rogueorhero(self.analysis_results.rogue_identified_all)
            else:
                if self.pro is True:
                    self.rogueorhero(self.analysis_results.rogue_identified_pronom)
        if self.fnames is True:
            self.rogueorhero(self.analysis_results.rogue_file_name_paths)
        if self.dirs is True:
            self.rogueorhero(self.analysis_results.rogue_dir_name_paths)
        if self.denylist is True:
            self.rogueorhero(self.analysis_results.rogue_denylist)

        try:
            number_allfiles = len(set(self.analysis_results.rogue_all_paths))
            number_alldirs = len(set(self.analysis_results.rogue_all_dirs))
        except TypeError:
            logging.warning(
                "Rogues and heroes lists not created: Check config for Rogues being turned off"
            )
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
