#!/usr/bin/env python
# -*- coding: utf-8 -*-

# [blacklist]
# ids='fmt/111','fmt/682','fmt/394'
# filenames='.DS_Store','Untitled Document'
# directorynames='Untitled Folder','(copy','.git'
# fileextensions='exe','dll','.txt'

# create
class HandleBlacklist:

    CFG_BLACK = "blacklist"
    CFG_FNAMES = "filenames"
    CFG_DIRS = "directorynames"
    CFG_IDS = "ids"
    CFG_EXT = "fileextensions"

    CFG_ROGUES = "rogues"
    ROGUE_DUPE = "duplicatechecksums"
    ROGUE_PRO = "pronomonly"
    ROGUE_BLACK = "blacklist"
    ROGUE_FNAMES = "nonasciifilenames"
    ROGUE_DIRS = "nonasciidirs"
    ROGUE_ZERO = "zerobytefiles"
    ROGUE_MULTI = "multipleids"
    ROGUE_EXT = "extensionmismatches"

    FILENAMES = "FILENAMES"
    IDS = "IDS"
    DIRECTORIES = "DIRECTORIES"
    EXTENSIONS = "EXTENSIONS"

    def blacklist(self, config):
        # four section dictionary
        self.blacklist = {}
        if config.has_section(self.CFG_BLACK):
            if config.has_option(self.CFG_BLACK, self.CFG_IDS):
                self.blacklist[self.IDS] = (
                    config.get(self.CFG_BLACK, self.CFG_IDS).replace("'", "").split(",")
                )
                if "" in self.blacklist[self.IDS]:
                    self.blacklist[self.IDS].remove(
                        ""
                    )  # handle extraneous commas in cfg
            else:
                self.blacklist[self.IDS] = None
            if config.has_option(self.CFG_BLACK, self.CFG_FNAMES):
                self.blacklist[self.FILENAMES] = (
                    config.get(self.CFG_BLACK, self.CFG_FNAMES)
                    .replace("'", "")
                    .split(",")
                )
                if "" in self.blacklist[self.FILENAMES]:
                    self.blacklist[self.FILENAMES].remove(
                        ""
                    )  # handle extraneous commas in cfg
            else:
                self.blacklist[self.FILENAMES] = None
            if config.has_option(self.CFG_BLACK, self.CFG_DIRS):
                self.blacklist[self.DIRECTORIES] = (
                    config.get(self.CFG_BLACK, self.CFG_DIRS)
                    .replace("'", "")
                    .split(",")
                )
                if "" in self.blacklist[self.DIRECTORIES]:
                    self.blacklist[self.DIRECTORIES].remove(
                        ""
                    )  # handle extraneous commas in cfg
            else:
                self.blacklist[self.DIRECTORIES] = None
            if config.has_option(self.CFG_BLACK, self.CFG_EXT):
                self.blacklist[self.EXTENSIONS] = (
                    config.get(self.CFG_BLACK, self.CFG_EXT).replace("'", "").split(",")
                )
                if "" in self.blacklist[self.EXTENSIONS]:
                    self.blacklist[self.EXTENSIONS].remove(
                        ""
                    )  # handle extraneous commas in cfg
            else:
                self.blacklist[self.EXTENSIONS] = None
        return self.blacklist
