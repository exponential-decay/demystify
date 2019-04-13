# -*- coding: utf-8 -*-

"""Denylist module."""

# [denylist]
# ids='fmt/111','fmt/682','fmt/394'
# filenames='.DS_Store','Untitled Document'
# directorynames='Untitled Folder','(copy','.git'
# fileextensions='exe','dll','.txt'


class HandleDenylist:
    """Object to encapsulate the denylist functions and helpers needed
    by Demystify.
    """

    CFG_DENY = "denylist"
    CFG_FNAMES = "filenames"
    CFG_DIRS = "directorynames"
    CFG_IDS = "ids"
    CFG_EXT = "fileextensions"

    CFG_ROGUES = "rogues"
    ROGUE_UNIDENTIFIED = "unidentified"
    ROGUE_DUPE = "duplicatechecksums"
    ROGUE_PRO = "pronomonly"
    ROGUE_DENY = "denylist"
    ROGUE_FNAMES = "nonasciifilenames"
    ROGUE_DIRS = "nonasciidirs"
    ROGUE_ZERO = "zerobytefiles"
    ROGUE_MULTI = "multipleids"
    ROGUE_EXT = "extensionmismatches"

    FILENAMES = "FILENAMES"
    IDS = "IDS"
    DIRECTORIES = "DIRECTORIES"
    EXTENSIONS = "EXTENSIONS"

    def denylist(self, config):
        # four section dictionary
        self.denylist_ = {}
        if config.has_section(self.CFG_DENY):
            if config.has_option(self.CFG_DENY, self.CFG_IDS):
                self.denylist_[self.IDS] = (
                    config.get(self.CFG_DENY, self.CFG_IDS).replace("'", "").split(",")
                )
                if "" in self.denylist_[self.IDS]:
                    self.denylist_[self.IDS].remove(
                        ""
                    )  # handle extraneous commas in cfg
            else:
                self.denylist_[self.IDS] = None
            if config.has_option(self.CFG_DENY, self.CFG_FNAMES):
                self.denylist_[self.FILENAMES] = (
                    config.get(self.CFG_DENY, self.CFG_FNAMES)
                    .replace("'", "")
                    .split(",")
                )
                if "" in self.denylist_[self.FILENAMES]:
                    self.denylist_[self.FILENAMES].remove(
                        ""
                    )  # handle extraneous commas in cfg
            else:
                self.denylist_[self.FILENAMES] = None
            if config.has_option(self.CFG_DENY, self.CFG_DIRS):
                self.denylist_[self.DIRECTORIES] = (
                    config.get(self.CFG_DENY, self.CFG_DIRS).replace("'", "").split(",")
                )
                if "" in self.denylist_[self.DIRECTORIES]:
                    self.denylist_[self.DIRECTORIES].remove(
                        ""
                    )  # handle extraneous commas in cfg
            else:
                self.denylist_[self.DIRECTORIES] = None
            if config.has_option(self.CFG_DENY, self.CFG_EXT):
                self.denylist_[self.EXTENSIONS] = (
                    config.get(self.CFG_DENY, self.CFG_EXT).replace("'", "").split(",")
                )
                if "" in self.denylist_[self.EXTENSIONS]:
                    self.denylist_[self.EXTENSIONS].remove(
                        ""
                    )  # handle extraneous commas in cfg
            else:
                self.denylist_[self.EXTENSIONS] = None
        return self.denylist_
