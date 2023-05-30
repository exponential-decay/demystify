# -*- coding: utf-8 -*-

import configparser as ConfigParser
import io

import pytest

from src.demystify.demystify import analysis_from_csv
from src.demystify.libs.HandleDenylistClass import HandleDenylist
from src.demystify.libs.outputhandlers.roguesgalleryoutputclass import rogueoutputclass

DENYLIST_ROGUES = """[denylist]

ids=fmt/61,fmt/480

filenames='.DS_Store','Thumbs.db'

directorynames='Untitled Folder','New Folder'

fileextensions='.ini','.cfg'

[rogues]

; Output unidentified files.
unidentified=True

; Output PRONOM only identification.
pronomonly=True

; Output duplicate files.
duplicatechecksums=True

; Output denylist.
denylist=True

; Output non-ascii filenames.
nonasciifilenames=True

; Output non-ascii directories.
nonasciidirs=True

; Output zero-byte files.
zerobytefiles=True

; Output multiple IDs.
multipleids=True

; Output extension mismatches.
extensionmismatches=True
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

For the rogues testing, the two lists for Siegfried and DROID are
enhanced with data from their respective integration tests.

"""

DROID_CSV = """"ID","PARENT_ID","URI","FILE_PATH","NAME","METHOD","STATUS","SIZE","TYPE","EXT","LAST_MODIFIED","EXTENSION_MISMATCH","SHA256_HASH","FORMAT_COUNT","PUID","MIME_TYPE","FORMAT_NAME","FORMAT_VERSION"
"2","","file:/tmp/denylist/","/tmp/denylist","denylist","","Done","","Folder","","2022-01-09T15:27:07","false","","","","","",""
"8","2","file:/tmp/denylist/.DS_Store","/tmp/denylist/.DS_Store",",DS_Store","","Done","10","File","","2022-01-09T15:22:01","false","cf237c7aff44efbe6e502e645c3e06da03a69d7bdeb43392108ef3348143417e","0","","","",""
"3","2","file:/tmp/denylist/.git/","/tmp/denylist/.git",",git","","Done","","Folder","","2022-01-09T15:26:55","false","","","","","",""
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
"31","2","file:/X:/digital/objects/39080024060920_1of2.wav","X:\\digital\\objects\39080024060920_1of2.wav","39080024060920_1of2.wav","Signature","Done","1575017726","File","wav","2017-12-23T21:04:35","false",,"2","fmt/704","audio/x-wav","Broadcast WAVE","1 PCM Encoding","fmt/142","audio/x-wav","Waveform Audio (WAVEFORMATEX)",""
"32","2","file:/X:/digital/objects/39080024060920_2of2.wav","X:\\digital\\objects\39080024060920_2of2.wav","39080024060920_2of2.wav","Signature","Done","1602958526","File","wav","2017-12-23T21:04:35","true",,"3","fmt/704","audio/x-wav","Broadcast WAVE","1 PCM Encoding","fmt/142","audio/x-wav","Waveform Audio (WAVEFORMATEX)","","fmt/134","audio/mpeg","MPEG 1/2 Audio Layer 3",""
"29","2","file:/X:/digital/objects/39080024060938_1of2.wav","X:\\digital\\objects\39080024060938_1of2.wav","39080024060938_1of2.wav","Signature","Done","1599605894","File","wav","2017-12-23T21:13:25","false",,"2","fmt/704","audio/x-wav","Broadcast WAVE","1 PCM Encoding","fmt/142","audio/x-wav","Waveform Audio (WAVEFORMATEX)",""
"28","2","file:/X:/digital/objects/39080024060938_2of2.wav","X:\\digital\\objects\39080024060938_2of2.wav","39080024060938_2of2.wav","Signature","Done","1606280216","File","wav","2017-12-23T21:13:25","false",,"2","fmt/704","audio/x-wav","Broadcast WAVE","1 PCM Encoding","fmt/142","audio/x-wav","Waveform Audio (WAVEFORMATEX)",""
"27","2","file:/X:/digital/objects/39080024060946_1of2.wav","X:\\digital\\objects\39080024060946_1of2.wav","39080024060946_1of2.wav","Signature","Done","1600565990","File","wav","2017-12-23T21:13:25","false",,"2","fmt/704","audio/x-wav","Broadcast WAVE","1 PCM Encoding","fmt/142","audio/x-wav","Waveform Audio (WAVEFORMATEX)",""
"25","2","file:/X:/digital/objects/39080024060946_2of2.wav","X:\\digital\\objects\39080024060946_2of2.wav","39080024060946_2of2.wav","Signature","Done","1605847400","File","wav","2017-12-23T21:13:25","false",,"2","fmt/704","audio/x-wav","Broadcast WAVE","1 PCM Encoding","fmt/142","audio/x-wav","Waveform Audio (WAVEFORMATEX)",""
"33","2","file:/X:/digital/objects/39080024060953_1of2.wav","X:\\digital\\objects\39080024060953_1of2.wav","39080024060953_1of2.wav","Signature","Done","1594875284","File","wav","2017-12-23T21:16:46","false",,"2","fmt/704","audio/x-wav","Broadcast WAVE","1 PCM Encoding","fmt/142","audio/x-wav","Waveform Audio (WAVEFORMATEX)",""
"30","2","file:/X:/digital/objects/39080024060953_2of2.wav","X:\\digital\\objects\39080024060953_2of2.wav","39080024060953_2of2.wav","Signature","Done","1601212508","File","wav","2017-12-23T21:16:46","false",,"2","fmt/704","audio/x-wav","Broadcast WAVE","1 PCM Encoding","fmt/142","audio/x-wav","Waveform Audio (WAVEFORMATEX)",""
"95","66","file:/X:/digital/objects/access/39080024061027_1of2.mp3","X:\\digital\\objects\access\39080024061027_1of2.mp3","39080024061027_1of2.mp3","Signature","Done","41655895","File","mp3","2017-12-25T22:21:37","true",,"2","fmt/198","audio/mpeg","MPEG Audio Stream, Layer II","","fmt/134","audio/mpeg","MPEG 1/2 Audio Layer 3",""
"70","68","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji/hearts-%E2%9D%A4%F0%9F%92%96%F0%9F%92%99%F0%9F%92%9A%F0%9F%92%9B%F0%9F%92%9C%F0%9F%92%9D/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji/hearts-❤💖💙💚💛💜💝","hearts-❤💖💙💚💛💜💝","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"81","56","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/emoji/chess-%E2%99%95%E2%99%96%E2%99%97%E2%99%98%E2%99%99%E2%99%9A%E2%99%9B%E2%99%9C%E2%99%9D%E2%99%9E%E2%99%9F.txt","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/emoji/chess-♕♖♗♘♙♚♛♜♝♞♟.txt","chess-♕♖♗♘♙♚♛♜♝♞♟.txt","Extension","Done","54","File","txt","2020-06-22T19:38:21","false","1766219eb64113604a1fe2c003b10c8258bb1cbb","1","x-fmt/111","text/plain","Plain Text File",""
"62","60","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437/caf%C3%A9/midnight/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437/café/midnight/","café","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"""


@pytest.fixture(scope="function")
def denylist(tmp_path):
    """Return a processed Denylist to provide to Demystify analysis."""
    dir_ = tmp_path
    denylist = dir_ / "deny_💜_list.cfg"
    denylist.write_text(DENYLIST_ROGUES.strip(), encoding="UTF-8")
    config = ConfigParser.RawConfigParser()
    config.read(str(denylist))
    return HandleDenylist().denylist(config)


@pytest.fixture(scope="function")
def rogueconfig(tmp_path):
    """Read Rogues configuration and supply it to a function as a
    test fixture.
    """
    dir_ = tmp_path
    denylist = dir_ / "deny_💜_list.cfg"
    denylist.write_text(DENYLIST_ROGUES.strip(), encoding="UTF-8")
    config = ConfigParser.RawConfigParser()
    config.read(str(denylist))
    return config


SF_ROGUE_TEST = """---
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
---
filename : 'fixtures/files_with_various_encodings/emoji/hearts-❤💖💙💚💛💜💝.txt'
filesize : 54
modified : 2020-06-22T19:38:21+02:00
errors   :
md5      : 0653e4959fa11f1ffce974b092efdd00
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/111'
    format  : 'Plain Text File'
    version :
    mime    : 'text/plain'
    basis   : 'extension match txt; text match ASCII'
    warning :
---
filename : 'fixtures/dirs_with_various_encodings/shift_jis/ぽっぷるメイル/shift-jis_encoded_dirs.txt'
filesize : 101
modified : 2020-06-22T19:38:22+02:00
errors   :
md5      : 4071a2a321e8c429362483e98a80960b
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/111'
    format  : 'Plain Text File'
    version :
    mime    : 'text/plain'
    basis   : 'extension match txt; text match ASCII'
    warning :
---
filename : 'README'
filesize : 297
modified : 2021-12-05T20:26:13+01:00
errors   :
md5      : aa15e4959fa11f1ffce974b092efdd00
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/111'
    format  : 'Plain Text File One'
    mime    : 'text/plain'
    basis   : 'extension match pdf; byte match at [[0 8] [9290 44] [9342 73]]'
    warning :
  - ns      : 'pronom'
    id      : 'x-fmt/112'
    format  : 'Plain Text File Two'
    mime    : 'text/plain'
    basis   : 'extension match pdf; byte match at [[0 8] [9290 44] [9342 73]]'
    warning :
---
filename : 'fixtures/dirs_with_various_encodings/shift_jis/hero_only_test/shift-jis_encoded_dirs.txt'
filesize : 101
modified : 2020-06-22T19:38:22+02:00
errors   :
md5      : a171a2a321e8c429362483e98a80960b
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/111'
    format  : 'Plain Text File'
    version :
    mime    : 'text/plain'
    basis   : 'extension match txt; text match ASCII'
    warning :
"""


def _process_captured_out(out):
    """Process captured output into a list for the purpose of analyzing
    the Rogue output.

    :param out: string that looks like a line-separated list (string)
    :return: list based on the input data (list)
    """
    out = io.StringIO(out)
    out_list = []
    for line in out:
        out_list.append(line.strip())
    out_list.sort()
    return out_list


EXPECTED_DROID = [
    "/tmp/denylist/New Folder/plain_text",
    "/tmp/denylist/plain_text",
    "/tmp/denylist/.git/commit_data",
    "/tmp/denylist/config.cfg",
    "/tmp/denylist/Thumbs.db",
    "/tmp/denylist/ole2",
    "/tmp/denylist/.DS_Store",
    "/tmp/denylist/config.ini",
    "/tmp/denylist/Untitled Folder/plain_text",
    "/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/emoji/chess-♕♖♗♘♙♚♛♜♝♞♟.txt",
    "/tmp/denylist/plain_text",
    "/tmp/denylist/.git/commit_data",
    "/tmp/denylist/Untitled Folder/plain_text",
    "/tmp/denylist/New Folder/plain_text",
    "/tmp/denylist/ole2.xls",
    "/tmp/denylist/config.cfg",
    "/tmp/denylist/New Folder",
    "/tmp/denylist/Untitled Folder",
    "/tmp/denylist/.DS_Store",
    "/tmp/denylist/config.ini",
    "/tmp/denylist/pdf.pdf",
    "/tmp/denylist/Thumbs.db",
    "/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437/café/midnight/",
    "/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji/hearts-❤💖💙💚💛💜💝",
    "/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/emoji/chess-♕♖♗♘♙♚♛♜♝♞♟.txt",
    "/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437/café/midnight/",
    "/tmp/denylist/ole2",
    "X:\\digital\\objects\x039080024060920_1of2.wav",
    "X:\\digital\\objects\x039080024060920_2of2.wav",
    "X:\\digital\\objects\x039080024060938_1of2.wav",
    "X:\\digital\\objects\x039080024060938_2of2.wav",
    "X:\\digital\\objects\x039080024060946_1of2.wav",
    "X:\\digital\\objects\x039080024060946_2of2.wav",
    "X:\\digital\\objects\x039080024060953_1of2.wav",
    "X:\\digital\\objects\x039080024060953_2of2.wav",
    "X:\\digital\\objects\x07ccess\x039080024061027_1of2.mp3",
]


def test_rogues_droid_rogues(tmp_path, capsys, denylist, rogueconfig):
    """Make sure that rogues are output for the DROID report as
    expected and that totals add up.
    """

    dir_ = tmp_path
    droid_csv = dir_ / "droid_💜_test.csv"
    droid_csv.write_text(DROID_CSV.strip(), encoding="UTF-8")

    assert rogueconfig is not None

    # Analysis from CSV will currently read the results from the CSV
    # above and output an on-disk sqlite database at tmp_path. This
    # works perfectly for us. In future, if we need to create an
    # in-memory database for any reason we can but it will take some
    # further refactoring.
    res = analysis_from_csv(str(droid_csv), True, denylist, True, False)
    assert res.analysis_results.filecount == 22
    # Directory count is used by DROID because it uses absolute paths.
    assert res.analysis_results.directoryCount == 6
    rogue_output = rogueoutputclass(res.analysis_results, rogueconfig, False)
    rogue_output.printTextResults()
    captured = capsys.readouterr()
    assert captured.out != "", "stdout is empty"
    processed = _process_captured_out(captured.out)
    assert len(set(processed)) == len(set(EXPECTED_DROID))
    assert len(set(processed)) == 25
    assert set(processed) == set(EXPECTED_DROID)


EXPECTED_DROID_HEROES = [
    "/tmp/denylist/xlsx.xlsx",
    "/tmp/denylist",
    "/tmp/denylist/.git",
]


def test_rogues_droid_heroes(tmp_path, capsys, denylist, rogueconfig):
    """Make sure that heroes are output for the DROID report as
    expected and that totals add up.
    """

    dir_ = tmp_path
    droid_csv = dir_ / "droid_💜_test.csv"
    droid_csv.write_text(DROID_CSV.strip(), encoding="UTF-8")

    assert rogueconfig is not None

    # Analysis from CSV will currently read the results from the CSV
    # above and output an on-disk sqlite database at tmp_path. This
    # works perfectly for us. In future, if we need to create an
    # in-memory database for any reason we can but it will take some
    # further refactoring.
    res = analysis_from_csv(str(droid_csv), True, denylist, False, True)
    assert res.analysis_results.filecount == 22
    # Directory count is used by DROID because it uses absolute paths.
    assert res.analysis_results.directoryCount == 6
    heroes_output = rogueoutputclass(res.analysis_results, rogueconfig, True)
    heroes_output.printTextResults()
    captured = capsys.readouterr()
    assert captured.out != "", "stdout is empty"
    processed = _process_captured_out(captured.out)
    assert len(set(processed)) == len(set(EXPECTED_DROID_HEROES))
    assert len(set(processed)) == 3
    assert set(processed) == set(EXPECTED_DROID_HEROES)


EXPECTED_SIEGFRIED_ROGUES = [
    "denylist",
    "denylist/config.ini",
    "denylist/ole2",
    "denylist/Thumbs.db",
    "denylist/.git",
    "denylist/New Folder",
    "denylist/.DS_Store",
    "denylist/Untitled Folder",
    "denylist/.git/commit_data",
    "denylist/Untitled Folder/plain_text",
    "denylist/plain_text",
    "denylist/New Folder/plain_text",
    "denylist/config.ini",
    "denylist/pdf.pdf",
    "denylist/config.cfg",
    "denylist/.DS_Store",
    "denylist/Untitled Folder",
    "denylist/Thumbs.db",
    "denylist/New Folder",
    "fixtures/files_with_various_encodings/emoji/hearts-❤💖💙💚💛💜💝.txt",
    "fixtures/dirs_with_various_encodings/shift_jis/ぽっぷるメイル",
    "denylist/ole2",
    "README",
    "denylist/config.cfg",
    "denylist/Untitled Folder/plain_text",
    "denylist/New Folder/plain_text",
    "denylist/plain_text",
    "denylist/.git/commit_data",
    "fixtures/files_with_various_encodings/emoji",
    "fixtures/dirs_with_various_encodings/shift_jis/ぽっぷるメイル/shift-jis_encoded_dirs.txt",
    # Double-check folder handling, hero_only_test and a few others
    # I think are being picked up in the filename analysis as Unicode
    # but I am not sure.
    "fixtures/dirs_with_various_encodings/shift_jis/hero_only_test",
]


def test_rogues_sf(tmp_path, capsys, denylist, rogueconfig):
    """Ensure that rogues are output correctly."""

    dir_ = tmp_path
    sf_yaml = dir_ / "sf_💜_rogue_test.yaml"
    sf_yaml.write_text(SF_ROGUE_TEST.strip(), encoding="UTF-8")

    assert rogueconfig is not None

    # Analysis from YAML will currently read the results from the YAML
    # above and output an on-disk sqlite database at tmp_path. This
    # works perfectly for us. In future, if we need to create an
    # in-memory database for any reason we can but it will take some
    # further refactoring.
    res = analysis_from_csv(str(sf_yaml), True, denylist, True, False)

    assert res.analysis_results.filecount == 16
    # Directory count is not used by SF because it doesn't use absolute
    # paths. More names are removed when creating the set.
    assert res.analysis_results.uniqueDirectoryNames == 7

    rogue_output = rogueoutputclass(res.analysis_results, rogueconfig, False)
    rogue_output.printTextResults()
    captured = capsys.readouterr()
    assert captured.out != "", "stdout is empty"
    processed = _process_captured_out(captured.out)
    assert len(set(processed)) == len(set(EXPECTED_SIEGFRIED_ROGUES))
    assert len(set(processed)) == 20
    assert set(processed) == set(EXPECTED_SIEGFRIED_ROGUES)


EXPECTED_SIEGFRIED_HEROES = [
    "denylist/ole2.xls",
    "denylist/xlsx.xlsx",
    "fixtures/dirs_with_various_encodings/shift_jis/hero_only_test/shift-jis_encoded_dirs.txt",
]


def test_heroes_sf(tmp_path, capsys, denylist, rogueconfig):
    """Ensure that heroes are output correctly."""

    dir_ = tmp_path
    sf_yaml = dir_ / "sf_💜_rogue_test.yaml"
    sf_yaml.write_text(SF_ROGUE_TEST.strip(), encoding="UTF-8")

    assert rogueconfig is not None

    # Analysis from YAML will currently read the results from the YAML
    # above and output an on-disk sqlite database at tmp_path. This
    # works perfectly for us. In future, if we need to create an
    # in-memory database for any reason we can but it will take some
    # further refactoring.
    res = analysis_from_csv(str(sf_yaml), True, denylist, True, False)

    assert res.analysis_results.filecount == 16
    # Directory count is not used by SF because it doesn't use absolute
    # paths. More names are removed when creating the set.
    assert res.analysis_results.uniqueDirectoryNames == 7

    heroes_output = rogueoutputclass(res.analysis_results, rogueconfig, True)
    heroes_output.printTextResults()
    captured = capsys.readouterr()
    assert captured.out != "", "stdout is empty"
    processed = _process_captured_out(captured.out)
    assert len(set(processed)) == len(set(EXPECTED_SIEGFRIED_HEROES))
    assert len(set(processed)) == 3
    assert set(processed) == set(EXPECTED_SIEGFRIED_HEROES)
