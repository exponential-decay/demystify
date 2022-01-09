# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import io
import sys

import pytest

from demystify import analysis_from_csv
from libs.HandleDenylistClass import HandleDenylist
from libs.outputhandlers.roguesgalleryoutputclass import rogueoutputclass

try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser


if sys.version_info[0] == 3:
    PY3 = True
else:
    PY3 = False

DENYLIST_DENY = u"""[denylist]

ids=fmt/61,fmt/480

filenames='.DS_Store','Thumbs.db'

directorynames='Untitled Folder','New Folder'

fileextensions='.ini','.cfg'
"""

DENYLIST_DENY_TIKA = u"""[denylist]

ids='application/vnd.ms-excel',text/x-ini

filenames='.DS_Store','Thumbs.db'

directorynames='Untitled Folder','New Folder'

fileextensions='.ini','.cfg'
"""


DENYLIST_ROGUES = u"""[denylist]

ids=fmt/111,fmt/682,fmt/394,x-fmt/409,x-fmt/410,x-fmt/411,fmt/688,fmt/689,fmt/690,fmt/691,fmt/468,fmt/473,fmt/474,fmt/503,fmt/523,fmt/819,x-fmt/157,x-fmt/418,x-fmt/419,x-fmt/428,x-fmt/429,x-fmt/453,application/x-sh,application/vnd.ms-tnef,application/x-stuffit,application/x-pak,application/x-mswinurl,application/x-executable,x-fmt/263,x-fmt/266,fmt/583,fmt/524

filenames='.DS_Store','Untitled Document','desktop.ini','(copy','ZbThumbnail.info','lorem','New Microsoft Word Document','Bin.dat','Thumbs.db', 'vitae', 'Appointments', 'CV', 'Application', 'Resume', 'Appointment', 'Test', 'list', 'member', 'people', 'address', 'phone'

directorynames='Untitled Folder','New Folder','(copy','.git','lorem'

fileextensions='.ini','.exe','.cfg','.dll','.lnk','.tmp'

[rogues]

; Output duplicate files.
duplicatechecksums=False

; Output PRONOM only identification.
pronomonly=True

; Output denylist.
denylist=True

; Output non-ascii filenames.
nonasciifilenames=True

; Output non-ascii directories.
nonasciidirs=True

; Output zero-byte files.
zerobytefiles=True

; Output multiple IDs.
multiple-ids=False

; Output extension mismatches.
extension-mismatches=True
"""

"""Example layout for denylist.

    denylist/
    ├── config.cfg
    ├── config.ini
    ├── .DS_Store
    ├── .git
    │   └── commit_data
    ├── New Folder
    │   └── plain_text
    ├── ole2
    ├── ole2.xls
    ├── pdf.pdf
    ├── plain_text
    ├── Thumbs.db
    ├── Untitled Folder
    │   └── plain_text
    └── xlsx.xlsx

"""

DROID_CSV = u""""ID","PARENT_ID","URI","FILE_PATH","NAME","METHOD","STATUS","SIZE","TYPE","EXT","LAST_MODIFIED","EXTENSION_MISMATCH","SHA256_HASH","FORMAT_COUNT","PUID","MIME_TYPE","FORMAT_NAME","FORMAT_VERSION"
"2","","file:/tmp/denylist/","/tmp/denylist","denylist","","Done","","Folder","","2022-01-09T15:27:07","false","","","","","",""
"8","2","file:/tmp/denylist/.DS_Store","/tmp/denylist/.DS_Store",".DS_Store","","Done","10","File","","2022-01-09T15:22:01","false","cf237c7aff44efbe6e502e645c3e06da03a69d7bdeb43392108ef3348143417e","0","","","",""
"3","2","file:/tmp/denylist/.git/","/tmp/denylist/.git",".git","","Done","","Folder","","2022-01-09T15:26:55","false","","","","","",""
"13","3","file:/tmp/denylist/.git/commit_data","/tmp/denylist/.git/commit_data","commit_data","","Done","5","File","","2022-01-09T15:26:55","false","6667b2d1aab6a00caa5aee5af8ad9f1465e567abf1c209d15727d57b3e8f6e5f","0","","","",""
"4","2","file:/tmp/denylist/New%20Folder/","/tmp/denylist/New Folder","New Folder","","Done","","Folder","","2022-01-09T15:27:27","false","","","","","",""
"10","4","file:/tmp/denylist/New%20Folder/plain_text","/tmp/denylist/New Folder/plain_text","plain_text","","Done","5","File","","2022-01-09T15:27:27","false","6667b2d1aab6a00caa5aee5af8ad9f1465e567abf1c209d15727d57b3e8f6e5f","0","","","",""
"9","2","file:/tmp/denylist/Thumbs.db","/tmp/denylist/Thumbs.db","Thumbs.db","Extension","Done","10","File","db","2022-01-09T15:21:46","false","1a1f7418a8c1958445426095999dc2b44bbfbab9ca8b867b57e051443cf2d3eb","1","fmt/682","application/vnd.microsoft.windows.thumbnail-cache","Thumbs DB file","XP"
"5","2","file:/tmp/denylist/Untitled%20Folder/","/tmp/denylist/Untitled Folder","Untitled Folder","","Done","","Folder","","2022-01-09T15:23:27","false","","","","","",""
"11","5","file:/tmp/denylist/Untitled%20Folder/plain_text","/tmp/denylist/Untitled Folder/plain_text","plain_text","","Done","5","File","","2022-01-09T15:22:38","false","6667b2d1aab6a00caa5aee5af8ad9f1465e567abf1c209d15727d57b3e8f6e5f","0","","","",""
"15","2","file:/tmp/denylist/config.cfg","/tmp/denylist/config.cfg","config.cfg","","Done","4","File","cfg","2022-01-09T15:23:05","false","4d523dee6bc8c17a3e283570526d8d6ed3d1edda07c53e94c55e491bbf780337","0","","","",""
"14","2","file:/tmp/denylist/config.ini","/tmp/denylist/config.ini","config.ini","Extension","Done","4","File","ini","2022-01-09T15:22:58","false","15c40f09661589c7b57e0ccc44ef1d94a1624859b8dade3790c9eab313dba02e","1","x-fmt/421","","Text Configuration file",""
"7","2","file:/tmp/denylist/ole2","/tmp/denylist/ole2","ole2","","Done","0","File","","2022-01-09T15:23:57","false","e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","0","","","",""
"17","2","file:/tmp/denylist/ole2.xls","/tmp/denylist/ole2.xls","ole2.xls","Container","Done","5632","File","xls","2022-01-09T15:25:33","false","3bd273e1939f95bd35de3455b2bba1483bd70826820e9617f6915529c3ea2b30","1","fmt/61","application/vnd.ms-excel","Microsoft Excel 97 Workbook (xls)","8"
"12","2","file:/tmp/denylist/pdf.pdf","/tmp/denylist/pdf.pdf","pdf.pdf","Signature","Done","15078","File","pdf","2022-01-09T15:26:09","false","06ba5beefb64e6647da2137492f615419739d549d7cc0b3f550464803b694559","1","fmt/480","application/pdf","Acrobat PDF/A - Portable Document Format","3b"
"6","2","file:/tmp/denylist/plain_text","/tmp/denylist/plain_text","plain_text","","Done","5","File","","2022-01-09T15:21:02","false","6667b2d1aab6a00caa5aee5af8ad9f1465e567abf1c209d15727d57b3e8f6e5f","0","","","",""
"16","2","file:/tmp/denylist/xlsx.xlsx","/tmp/denylist/xlsx.xlsx","xlsx.xlsx","Container","Done","4349","File","xlsx","2022-01-09T15:25:56","false","790e07bca72cffbb60ea80beb3e8d023f30ced0ce920d8b9d4520019521a2120","1","fmt/214","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet","Microsoft Excel for Windows","2007 onwards"
"""


@pytest.fixture(scope="function")
def denylist(tmp_path):
    """Return a processed Denylist to provide to Demystify analysis."""
    dir_ = tmp_path
    denylist = dir_ / "deny_💜_list.cfg"
    denylist.write_text(DENYLIST_DENY.strip())
    config = ConfigParser.RawConfigParser()
    config.read(str(denylist))
    return HandleDenylist().denylist(config)


@pytest.fixture(scope="function")
def denylist_tika(tmp_path):
    """Return a processed Denylist to provide to Demystify analysis."""
    dir_ = tmp_path
    denylist = dir_ / "deny_💜_list.cfg"
    denylist.write_text(DENYLIST_DENY_TIKA.strip())
    config = ConfigParser.RawConfigParser()
    config.read(str(denylist))
    return HandleDenylist().denylist(config)


def test_denylist_droid(tmp_path, denylist):
    """Test basic configuration of Denylist and rogues here."""

    dir_ = tmp_path
    droid_csv = dir_ / "droid_💜_test.csv"
    droid_csv.write_text(DROID_CSV.strip())

    assert denylist == {
        "IDS": ["fmt/61", "fmt/480"],
        "FILENAMES": [".DS_Store", "Thumbs.db"],
        "DIRECTORIES": ["Untitled Folder", "New Folder"],
        "EXTENSIONS": [".ini", ".cfg"],
    }

    # Analysis from CSV will currently read the results from the CSV
    # above and output an on-disk sqlite database at tmp_path. This
    # works perfectly for us. In future, if we need to create an
    # in-memory database for any reason we can but it will take some
    # further refactoring.
    res = analysis_from_csv(str(droid_csv), True, denylist, False, False)

    assert res.analysis_results.denylist == True
    assert res.analysis_results.rogue_pronom_ns_id == None
    res.analysis_results.denylist_filenames.sort()
    assert res.analysis_results.denylist_filenames == [
        (".DS_Store", 1),
        ("Thumbs.db", 1),
    ]
    res.analysis_results.denylist_directories.sort()
    assert res.analysis_results.denylist_directories == [
        ("New Folder", 1),
        ("Untitled Folder", 1),
    ]
    res.analysis_results.denylist_ids.sort()
    assert res.analysis_results.denylist_ids == [
        ("fmt/480: Acrobat PDF/A - Portable Document Format 3b", 1),
        ("fmt/61: Microsoft Excel 97 Workbook (xls) 8", 1),
    ]
    res.analysis_results.denylist_exts.sort()
    assert res.analysis_results.denylist_exts == [("cfg", 1), ("ini", 1)]
    res.analysis_results.rogue_denylist.sort()
    assert res.analysis_results.rogue_denylist == [
        "/tmp/denylist/.DS_Store",
        "/tmp/denylist/New Folder",
        "/tmp/denylist/Thumbs.db",
        "/tmp/denylist/Untitled Folder",
        "/tmp/denylist/config.cfg",
        "/tmp/denylist/config.ini",
        "/tmp/denylist/ole2.xls",
        "/tmp/denylist/pdf.pdf",
    ]


SF_DENY_TEST = u"""---
siegfried   : 1.9.1
scandate    : 2022-01-09T16:44:18+01:00
signature   : default.sig
created     : 2020-10-06T19:13:40+02:00
identifiers :
  - name    : 'pronom'
    details : 'DROID_SignatureFile_V97.xml; container-signature-20201001.xml'
---
filename : 'denylist/.DS_Store'
filesize : 10
modified : 2022-01-09T15:22:01+01:00
errors   :
md5      : 952fd44d14cee87882239b707231609d
matches  :
  - ns      : 'pronom'
    id      : 'UNKNOWN'
    format  :
    version :
    mime    :
    basis   :
    warning : 'no match; possibilities based on extension are fmt/394'
---
filename : 'denylist/.git/commit_data'
filesize : 5
modified : 2022-01-09T15:26:55+01:00
errors   :
md5      : 6137cde4893c59f76f005a8123d8e8e6
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/111'
    format  : 'Plain Text File'
    version :
    mime    : 'text/plain'
    basis   : 'text match ASCII'
    warning : 'match on text only; extension mismatch'
---
filename : 'denylist/New Folder/plain_text'
filesize : 5
modified : 2022-01-09T15:27:27+01:00
errors   :
md5      : 6137cde4893c59f76f005a8123d8e8e6
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/111'
    format  : 'Plain Text File'
    version :
    mime    : 'text/plain'
    basis   : 'text match ASCII'
    warning : 'match on text only; extension mismatch'
---
filename : 'denylist/Thumbs.db'
filesize : 10
modified : 2022-01-09T15:21:46+01:00
errors   :
md5      : 0103e4d92d15e0ed2e630ff1c1a4d539
matches  :
  - ns      : 'pronom'
    id      : 'UNKNOWN'
    format  :
    version :
    mime    :
    basis   :
    warning : 'no match; possibilities based on extension are x-fmt/147, fmt/350, fmt/351, fmt/352, fmt/682, fmt/729, fmt/1135'
---
filename : 'denylist/Untitled Folder/plain_text'
filesize : 5
modified : 2022-01-09T15:22:38+01:00
errors   :
md5      : 6137cde4893c59f76f005a8123d8e8e6
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/111'
    format  : 'Plain Text File'
    version :
    mime    : 'text/plain'
    basis   : 'text match ASCII'
    warning : 'match on text only; extension mismatch'
---
filename : 'denylist/config.cfg'
filesize : 4
modified : 2022-01-09T15:23:05+01:00
errors   :
md5      : 9aedcb5a60b973955799b7611c449977
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/111'
    format  : 'Plain Text File'
    version :
    mime    : 'text/plain'
    basis   : 'text match ASCII'
    warning : 'match on text only; extension mismatch'
---
filename : 'denylist/config.ini'
filesize : 4
modified : 2022-01-09T15:22:58+01:00
errors   :
md5      : 08cac458dcf75bb748c8bcd37b5c11d2
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/421'
    format  : 'Text Configuration file'
    version :
    mime    :
    basis   : 'extension match ini'
    warning : 'match on extension only'
---
filename : 'denylist/ole2'
filesize : 0
modified : 2022-01-09T15:23:57+01:00
errors   : 'empty source'
md5      : d41d8cd98f00b204e9800998ecf8427e
matches  :
  - ns      : 'pronom'
    id      : 'UNKNOWN'
    format  :
    version :
    mime    :
    basis   :
    warning : 'no match'
---
filename : 'denylist/ole2.xls'
filesize : 5632
modified : 2022-01-09T15:25:33+01:00
errors   :
md5      : 102ded970d557ebd81a785b5418c12dd
matches  :
  - ns      : 'pronom'
    id      : 'fmt/111'
    format  : 'OLE2 Compound Document Format'
    version :
    mime    :
    basis   : 'byte match at 0, 30'
    warning :
---
filename : 'denylist/pdf.pdf'
filesize : 15078
modified : 2022-01-09T15:26:09+01:00
errors   :
md5      : 690be6aff4ef6525c034b9559b5c9d76
matches  :
  - ns      : 'pronom'
    id      : 'fmt/480'
    format  : 'Acrobat PDF/A - Portable Document Format'
    version : '3b'
    mime    : 'application/pdf'
    basis   : 'extension match pdf; byte match at [[0 8] [9290 44] [9342 73]]'
    warning :
---
filename : 'denylist/plain_text'
filesize : 5
modified : 2022-01-09T15:21:02+01:00
errors   :
md5      : 6137cde4893c59f76f005a8123d8e8e6
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/111'
    format  : 'Plain Text File'
    version :
    mime    : 'text/plain'
    basis   : 'text match ASCII'
    warning : 'match on text only; extension mismatch'
---
filename : 'denylist/xlsx.xlsx'
filesize : 4349
modified : 2022-01-09T15:25:56+01:00
errors   :
md5      : c613fa13ee1662454843ce86642ebd69
matches  :
  - ns      : 'pronom'
    id      : 'fmt/214'
    format  : 'Microsoft Excel for Windows'
    version : '2007 onwards'
    mime    : 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    basis   : 'extension match xlsx; container name [Content_Types].xml with byte match at 636, 88 (signature 1/3)'
    warning :
"""


def test_denylist_sf(tmp_path, denylist):
    """..."""

    dir_ = tmp_path
    sf_yaml = dir_ / "sf_💜_test.yaml"
    sf_yaml.write_text(SF_DENY_TEST.strip())

    # Analysis from YAML will currently read the results from the YAML
    # above and output an on-disk sqlite database at tmp_path. This
    # works perfectly for us. In future, if we need to create an
    # in-memory database for any reason we can but it will take some
    # further refactoring.
    res = analysis_from_csv(str(sf_yaml), True, denylist, False, False)

    assert res.analysis_results.denylist == True
    assert res.analysis_results.rogue_pronom_ns_id == None
    res.analysis_results.denylist_filenames.sort()
    assert res.analysis_results.denylist_filenames == [
        (".DS_Store", 1),
        ("Thumbs.db", 1),
    ]
    res.analysis_results.denylist_directories.sort()
    assert res.analysis_results.denylist_directories == [
        ("New Folder", 1),
        ("Untitled Folder", 1),
    ]
    res.analysis_results.denylist_ids.sort()
    assert res.analysis_results.denylist_ids == [
        ("fmt/480: Acrobat PDF/A - Portable Document Format 3b", 1)
    ]
    res.analysis_results.denylist_exts.sort()
    assert res.analysis_results.denylist_exts == [("cfg", 1), ("ini", 1)]
    res.analysis_results.rogue_denylist.sort()
    assert res.analysis_results.rogue_denylist == [
        "denylist/.DS_Store",
        "denylist/New Folder",
        "denylist/Thumbs.db",
        "denylist/Untitled Folder",
        "denylist/config.cfg",
        "denylist/config.ini",
        "denylist/pdf.pdf",
    ]


SF_DENY_TEST_TIKA = u"""---
siegfried   : 1.9.1
scandate    : 2022-01-09T16:42:53+01:00
signature   : default.sig
created     : 2020-10-06T19:14:01+02:00
identifiers :
  - name    : 'tika'
    details : 'tika-mimetypes.xml (1.24, 2020-04-17)'
---
filename : 'denylist/.DS_Store'
filesize : 10
modified : 2022-01-09T15:22:01+01:00
errors   :
md5      : 952fd44d14cee87882239b707231609d
matches  :
  - ns      : 'tika'
    id      : 'text/plain'
    format  :
    mime    : 'text/plain'
    basis   : 'text match ASCII'
    warning : 'match on text only; byte/xml signatures for this format did not match; filename mismatch'
---
filename : 'denylist/.git/commit_data'
filesize : 5
modified : 2022-01-09T15:26:55+01:00
errors   :
md5      : 6137cde4893c59f76f005a8123d8e8e6
matches  :
  - ns      : 'tika'
    id      : 'text/plain'
    format  :
    mime    : 'text/plain'
    basis   : 'text match ASCII'
    warning : 'match on text only; byte/xml signatures for this format did not match; filename mismatch'
---
filename : 'denylist/New Folder/plain_text'
filesize : 5
modified : 2022-01-09T15:27:27+01:00
errors   :
md5      : 6137cde4893c59f76f005a8123d8e8e6
matches  :
  - ns      : 'tika'
    id      : 'text/plain'
    format  :
    mime    : 'text/plain'
    basis   : 'text match ASCII'
    warning : 'match on text only; byte/xml signatures for this format did not match; filename mismatch'
---
filename : 'denylist/Thumbs.db'
filesize : 10
modified : 2022-01-09T15:21:46+01:00
errors   :
md5      : 0103e4d92d15e0ed2e630ff1c1a4d539
matches  :
  - ns      : 'tika'
    id      : 'text/plain'
    format  :
    mime    : 'text/plain'
    basis   : 'text match ASCII'
    warning : 'match on text only; byte/xml signatures for this format did not match; filename mismatch'
---
filename : 'denylist/Untitled Folder/plain_text'
filesize : 5
modified : 2022-01-09T15:22:38+01:00
errors   :
md5      : 6137cde4893c59f76f005a8123d8e8e6
matches  :
  - ns      : 'tika'
    id      : 'text/plain'
    format  :
    mime    : 'text/plain'
    basis   : 'text match ASCII'
    warning : 'match on text only; byte/xml signatures for this format did not match; filename mismatch'
---
filename : 'denylist/config.cfg'
filesize : 4
modified : 2022-01-09T15:23:05+01:00
errors   :
md5      : 9aedcb5a60b973955799b7611c449977
matches  :
  - ns      : 'tika'
    id      : 'text/plain'
    format  :
    mime    : 'text/plain'
    basis   : 'extension match cfg; text match ASCII'
    warning : 'match on filename and text only; byte/xml signatures for this format did not match'
---
filename : 'denylist/config.ini'
filesize : 4
modified : 2022-01-09T15:22:58+01:00
errors   :
md5      : 08cac458dcf75bb748c8bcd37b5c11d2
matches  :
  - ns      : 'tika'
    id      : 'text/x-ini'
    format  : 'Configuration file'
    mime    : 'text/x-ini'
    basis   : 'extension match ini; text match ASCII'
    warning : 'match on filename and text only'
---
filename : 'denylist/ole2'
filesize : 0
modified : 2022-01-09T15:23:57+01:00
errors   : 'empty source'
md5      : d41d8cd98f00b204e9800998ecf8427e
matches  :
  - ns      : 'tika'
    id      : 'UNKNOWN'
    format  :
    mime    : 'UNKNOWN'
    basis   :
    warning : 'no match'
---
filename : 'denylist/ole2.xls'
filesize : 5632
modified : 2022-01-09T15:25:33+01:00
errors   :
md5      : 102ded970d557ebd81a785b5418c12dd
matches  :
  - ns      : 'tika'
    id      : 'application/vnd.ms-excel'
    format  : 'Microsoft Excel Spreadsheet'
    mime    : 'application/vnd.ms-excel'
    basis   : 'extension match xls; byte match at 0, 8 (signature 6/6)'
    warning :
---
filename : 'denylist/pdf.pdf'
filesize : 15078
modified : 2022-01-09T15:26:09+01:00
errors   :
md5      : 690be6aff4ef6525c034b9559b5c9d76
matches  :
  - ns      : 'tika'
    id      : 'application/pdf'
    format  : 'Portable Document Format'
    mime    : 'application/pdf'
    basis   : 'extension match pdf; byte match at 0, 5 (signature 1/4)'
    warning :
---
filename : 'denylist/plain_text'
filesize : 5
modified : 2022-01-09T15:21:02+01:00
errors   :
md5      : 6137cde4893c59f76f005a8123d8e8e6
matches  :
  - ns      : 'tika'
    id      : 'text/plain'
    format  :
    mime    : 'text/plain'
    basis   : 'text match ASCII'
    warning : 'match on text only; byte/xml signatures for this format did not match; filename mismatch'
---
filename : 'denylist/xlsx.xlsx'
filesize : 4349
modified : 2022-01-09T15:25:56+01:00
errors   :
md5      : c613fa13ee1662454843ce86642ebd69
matches  :
  - ns      : 'tika'
    id      : 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    format  : 'Office Open XML Workbook'
    mime    : 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    basis   : 'extension match xlsx; byte match at [[0 4] [30 11]] (signature 2/2)'
    warning :
"""


def test_denylist_sf_tika(tmp_path, denylist_tika):
    """..."""

    dir_ = tmp_path
    sf_yaml = dir_ / "sf_💜_test.yaml"
    sf_yaml.write_text(SF_DENY_TEST_TIKA.strip())

    # Analysis from YAML will currently read the results from the YAML
    # above and output an on-disk sqlite database at tmp_path. This
    # works perfectly for us. In future, if we need to create an
    # in-memory database for any reason we can but it will take some
    # further refactoring.
    res = analysis_from_csv(str(sf_yaml), True, denylist_tika, False, False)

    assert res.analysis_results.denylist == True
    assert res.analysis_results.rogue_pronom_ns_id == None
    res.analysis_results.denylist_filenames.sort()
    assert res.analysis_results.denylist_filenames == [
        (".DS_Store", 1),
        ("Thumbs.db", 1),
    ]
    res.analysis_results.denylist_directories.sort()
    assert res.analysis_results.denylist_directories == [
        ("New Folder", 1),
        ("Untitled Folder", 1),
    ]
    res.analysis_results.denylist_ids.sort()
    assert res.analysis_results.denylist_ids == [
        ("application/vnd.ms-excel: Microsoft Excel Spreadsheet None", 1),
        ("text/x-ini: Configuration file None", 1),
    ]
    assert res.analysis_results.denylist_exts == [("cfg", 1)]
    res.analysis_results.rogue_denylist.sort()
    assert len(res.analysis_results.rogue_denylist) == 7
    assert res.analysis_results.rogue_denylist == [
        "denylist/.DS_Store",
        "denylist/New Folder",
        "denylist/Thumbs.db",
        "denylist/Untitled Folder",
        "denylist/config.cfg",
        "denylist/config.ini",
        "denylist/ole2.xls",
    ]


@pytest.fixture(scope="function")
def rogueconfig(tmp_path):
    """Read Rogues configuration and supply it to a function as a
    test fixture.
    """
    dir_ = tmp_path
    denylist = dir_ / "deny_💜_list.cfg"
    denylist.write_text(DENYLIST_ROGUES.strip())
    config = ConfigParser.RawConfigParser()
    config.read(str(denylist))
    return config


def test_rogues_droid(tmp_path, denylist, rogueconfig):
    """..."""

    dir_ = tmp_path
    droid_csv = dir_ / "droid_💜_test.csv"
    droid_csv.write_text(DROID_CSV.strip())

    assert rogueconfig is not None

    # Analysis from CSV will currently read the results from the CSV
    # above and output an on-disk sqlite database at tmp_path. This
    # works perfectly for us. In future, if we need to create an
    # in-memory database for any reason we can but it will take some
    # further refactoring.
    res = analysis_from_csv(str(droid_csv), True, denylist, False, False)

    rogue_output = rogueoutputclass(res, rogueconfig, False)
    # assert rogue_output == None
    hero_output = rogueoutputclass(res, rogueconfig, True)
    # assert hero_output == None


def test_rogues_sf(tmp_path, capsys, denylist, rogueconfig):
    """..."""

    dir_ = tmp_path
    sf_yaml = dir_ / "sf_💜_test.yaml"
    sf_yaml.write_text(SF_DENY_TEST.strip())

    assert rogueconfig is not None

    # Analysis from YAML will currently read the results from the YAML
    # above and output an on-disk sqlite database at tmp_path. This
    # works perfectly for us. In future, if we need to create an
    # in-memory database for any reason we can but it will take some
    # further refactoring.
    res = analysis_from_csv(str(sf_yaml), True, denylist, True, False)

    rogue_output = rogueoutputclass(res.analysis_results, rogueconfig, False)
    rogue_output.printTextResults()
    captured = capsys.readouterr()
    # assert captured.out == ""

    hero_output = rogueoutputclass(res.analysis_results, rogueconfig, True)
    hero_output.printTextResults()
    captured = capsys.readouterr()
    out = io.StringIO(captured.out)
    out_list = []
    for line in out:
        out_list.append(line.strip())
    out_list.sort()

    """assert out_list == [
        "one_dupe_one",
        "one_dupe_two",
        "two_dupe_one",
        "two_dupe_three",
        "two_dupe_two",
    ]"""


"""
        # Rogue related values.
        self.rogue_pronom_ns_id = None
        self.rogue_all_paths = None
        self.rogue_all_dirs = None
        self.rogue_duplicates = []
        self.rogue_identified_all = []
        self.rogue_identified_pronom = []
        self.rogue_extension_mismatches = []
        self.rogue_file_name_paths = []  # non-ascii file names
        self.rogue_dir_name_paths = []  # non-ascii dir names


        # Rogue related values.
        self.rogue_pronom_ns_id = None
        self.rogue_all_paths = None
        self.rogue_all_dirs = None
        self.rogue_denylist = []
        self.rogue_duplicates = []
        self.rogue_identified_all = []
        self.rogue_identified_pronom = []
        self.rogue_extension_mismatches = []
        self.rogue_multiple_identification_list = []
        self.rogue_file_name_paths = []  # non-ascii file names
        self.rogue_dir_name_paths = []  # non-ascii dir names

"""
