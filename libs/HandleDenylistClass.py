# -*- coding: utf-8 -*-

# [denylist]
# ids='fmt/111','fmt/682','fmt/394'
# filenames='.DS_Store','Untitled Document'
# directorynames='Untitled Folder','(copy','.git'
# fileextensions='exe','dll','.txt'

# create
class HandleDenylist:

    CFG_DENY = "denylist"
    CFG_FNAMES = "filenames"
    CFG_DIRS = "directorynames"
    CFG_IDS = "ids"
    CFG_EXT = "fileextensions"

    CFG_ROGUES = "rogues"
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
        self.denylist = {}
        if config.has_section(self.CFG_DENY):
            if config.has_option(self.CFG_DENY, self.CFG_IDS):
                self.denylist[self.IDS] = (
                    config.get(self.CFG_DENY, self.CFG_IDS).replace("'", "").split(",")
                )
                if "" in self.denylist[self.IDS]:
                    self.denylist[self.IDS].remove(
                        ""
                    )  # handle extraneous commas in cfg
            else:
                self.denylist[self.IDS] = None
            if config.has_option(self.CFG_DENY, self.CFG_FNAMES):
                self.denylist[self.FILENAMES] = (
                    config.get(self.CFG_DENY, self.CFG_FNAMES)
                    .replace("'", "")
                    .split(",")
                )
                if "" in self.denylist[self.FILENAMES]:
                    self.denylist[self.FILENAMES].remove(
                        ""
                    )  # handle extraneous commas in cfg
            else:
                self.denylist[self.FILENAMES] = None
            if config.has_option(self.CFG_DENY, self.CFG_DIRS):
                self.denylist[self.DIRECTORIES] = (
                    config.get(self.CFG_DENY, self.CFG_DIRS).replace("'", "").split(",")
                )
                if "" in self.denylist[self.DIRECTORIES]:
                    self.denylist[self.DIRECTORIES].remove(
                        ""
                    )  # handle extraneous commas in cfg
            else:
                self.denylist[self.DIRECTORIES] = None
            if config.has_option(self.CFG_DENY, self.CFG_EXT):
                self.denylist[self.EXTENSIONS] = (
                    config.get(self.CFG_DENY, self.CFG_EXT).replace("'", "").split(",")
                )
                if "" in self.denylist[self.EXTENSIONS]:
                    self.denylist[self.EXTENSIONS].remove(
                        ""
                    )  # handle extraneous commas in cfg
            else:
                self.denylist[self.EXTENSIONS] = None
        return self.denylist
