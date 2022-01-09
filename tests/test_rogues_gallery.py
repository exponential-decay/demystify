# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import io
import sys

import pytest

from demystify import analysis_from_csv
from libs.outputhandlers.roguesgalleryoutputclass import rogueoutputclass

try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser


if sys.version_info[0] == 3:
    PY3 = True
else:
    PY3 = False

DENYLIST = u"""[denylist]

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


DROID_CSV = u""""ID","PARENT_ID","URI","FILE_PATH","NAME","METHOD","STATUS","SIZE","TYPE","EXT","LAST_MODIFIED","EXTENSION_MISMATCH","SHA1_HASH","FORMAT_COUNT","PUID","MIME_TYPE","FORMAT_NAME","FORMAT_VERSION"
"2","","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures","fixtures","","Done","","Folder","","2021-07-25T17:04:51","false","","","","","",""
"40","2","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types","archive-types","","Done","","Folder","","2021-07-25T17:04:59","false","","","","","",""
"41","40","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-four.tar.gz","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-four.tar.gz","container-example-four.tar.gz","Signature","Done","726","Container","gz","2021-07-25T17:04:42","false","bc1e24e8a86dc7286df56ee5e474d31bc8b29b4b","1","x-fmt/266","application/gzip","GZIP Format",""
"43","40","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-one.zip","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-one.zip","container-example-one.zip","Signature","Done","3411","Container","zip","2021-07-25T17:02:27","false","530b757a613967c37369ef1f8a11748e3a4a9b31","1","x-fmt/263","application/zip","ZIP Format",""
"44","40","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-three.7z","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-three.7z","container-example-three.7z","Signature","Error","1070","Container","7z","2021-07-25T17:02:52","false","d3cde37a197b2660e16769376bde5cef15d7b66a","1","fmt/484","","7Zip format",""
"50","40","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-two.tar.xz","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-two.tar.xz","container-example-two.tar.xz","Signature","Done","348","File","xz","2021-07-25T17:02:45","false","7a9ba7d5208f1d3a2b3629e86eaf64e6ededb789","1","fmt/1098","","XZ File Format",""
"53","40","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/fmt-1281-signature-id-1661.warc","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/fmt-1281-signature-id-1661.warc","fmt-1281-signature-id-1661.warc","Signature","Done","280","File","warc","2020-01-25T03:00:29","false","9e274dc22c244808be4673189c709f1817db0a10","1","fmt/1281","application/warc","WARC","1.1"
"42","40","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/fmt-289-signature-id-305.warc","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/fmt-289-signature-id-305.warc","fmt-289-signature-id-305.warc","Signature","Done","832","File","warc","2020-01-25T03:00:31","false","fdd6a6b1c3c39f7b6b52508fbcceb5eaabdfa5e9","1","fmt/289","application/warc","WARC",""
"71","40","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/fmt-410-signature-id-580.arc","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/fmt-410-signature-id-580.arc","fmt-410-signature-id-580.arc","Signature","Done","205","File","arc","2020-11-30T03:25:18","false","4da73922efb9e703c1b6e44f9eec57601261950f","1","fmt/410","","Internet Archive","1.1"
"52","40","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/x-fmt-219-signature-id-525.arc","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/x-fmt-219-signature-id-525.arc","x-fmt-219-signature-id-525.arc","Signature","Done","205","File","arc","2020-01-25T03:00:31","false","90c3f2741429079eb12a2dc270a067c1a643d1be","1","x-fmt/219","application/x-internet-archive","Internet Archive","1.0"
"72","40","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/x-fmt-263-signature-id-200.zip","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/x-fmt-263-signature-id-200.zip","x-fmt-263-signature-id-200.zip","Signature","Done","65572","Container","zip","2020-11-30T03:25:20","false","a282da4e7700f342c80799f9eaff8a2181ef9c81","1","x-fmt/263","application/zip","ZIP Format",""
"48","40","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/x-fmt-266-signature-id-201.gz","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/x-fmt-266-signature-id-201.gz","x-fmt-266-signature-id-201.gz","Signature","Error","3","Container","gz","2020-11-30T03:25:20","false","c1df680e393d04a2a3b050a06db652e9ab37f761","1","x-fmt/266","application/gzip","GZIP Format",""
"26","2","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/container-objects/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/container-objects","container-objects","","Done","","Folder","","2021-07-25T14:07:30","false","","","","","",""
"31","26","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/container-objects/fmt-412-container-signature-id-1050.docx","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/container-objects/fmt-412-container-signature-id-1050.docx","fmt-412-container-signature-id-1050.docx","Container","Done","49476","File","docx","2020-11-30T03:21:35","false","874586e61e15f9ee4c563514c85dbc36c6043382","1","fmt/412","application/vnd.openxmlformats-officedocument.wordprocessingml.document","Microsoft Word for Windows","2007 onwards"
"29","26","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/container-objects/fmt-443-container-signature-id-13020.vsd","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/container-objects/fmt-443-container-signature-id-13020.vsd","fmt-443-container-signature-id-13020.vsd","Container","Done","2560","File","vsd","2020-11-30T03:21:36","false","87ddd36d2c1a58aefee26fdf51c2c2d01f70d222","1","fmt/443","application/vnd.visio","Microsoft Visio Drawing","2003-2010"
"30","26","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/container-objects/fmt-631-container-signature-id-3080.potx","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/container-objects/fmt-631-container-signature-id-3080.potx","fmt-631-container-signature-id-3080.potx","Container","Done","2276","File","potx","2020-11-30T03:21:36","false","6bf762330931ffef2508cf447f047cf39e19702f","1","fmt/631","application/vnd.openxmlformats-officedocument.presentationml.template","Microsoft PowerPoint Template","2007"
"32","26","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/container-objects/fmt-853-container-signature-id-22520.dpp","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/container-objects/fmt-853-container-signature-id-22520.dpp","fmt-853-container-signature-id-22520.dpp","Container","Done","4096","File","dpp","2020-11-30T03:21:37","false","b0f15c05ab430a7c0c62c20e6665b4e34f2f393a","1","fmt/853","","Serif DrawPlus Drawing","5"
"27","26","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/container-objects/fmt-999-container-signature-id-32010.kra","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/container-objects/fmt-999-container-signature-id-32010.kra","fmt-999-container-signature-id-32010.kra","Container","Done","133","File","kra","2020-11-30T03:21:37","false","5781bbf44a3e3bb43a9e583c8a06661070330ef6","1","fmt/999","application/x-krita","Krita Document Format",""
"34","26","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/container-objects/x-fmt-401-container-signature-id-23125.sda","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/container-objects/x-fmt-401-container-signature-id-23125.sda","x-fmt-401-container-signature-id-23125.sda","Container","Done","2560","File","sda","2020-11-30T03:21:37","false","660ca1d7ce34caba8be18203018d9555d937cf0f","1","x-fmt/401","application/vnd.stardivision.draw","StarOffice Draw","5.x"
"28","26","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/container-objects/x-fmt-88-container-signature-id-3130.ppt","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/container-objects/x-fmt-88-container-signature-id-3130.ppt","x-fmt-88-container-signature-id-3130.ppt","Container","Done","2560","File","ppt","2020-11-30T03:21:36","false","2fd03bafdcf3d9d9d60f773efa37115c322e5175","1","x-fmt/88","application/vnd.ms-powerpoint","Microsoft Powerpoint Presentation","4.0"
"59","2","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings","dirs_with_various_encodings","","Done","","Folder","","2021-07-25T10:40:16","false","","","","","",""
"66","59","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/big5/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/big5","big5","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"67","66","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/big5/%E5%BB%A3%E5%B7%9E/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/big5/廣州","廣州","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"73","67","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/big5/%E5%BB%A3%E5%B7%9E/big5_encoded_dirs.txt","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/big5/廣州/big5_encoded_dirs.txt","big5_encoded_dirs.txt","Extension","Done","96","File","txt","2020-06-22T19:38:22","false","57573bf4b57e9215f598d97469bf5fcf0046ee73","1","x-fmt/111","text/plain","Plain Text File",""
"60","59","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437","cp437","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"61","60","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437/a%C3%B1o/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437/año","año","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"64","61","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437/a%C3%B1o/cp437_encoded_dirs.txt","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437/año/cp437_encoded_dirs.txt","cp437_encoded_dirs.txt","Extension","Done","97","File","txt","2020-06-22T19:38:22","false","0c391e403302385e9d227733fc477bf440f978d2","1","x-fmt/111","text/plain","Plain Text File",""
"62","60","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437/caf%C3%A9/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437/café","café","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"65","62","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437/caf%C3%A9/cp437_encoded_dirs.txt","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437/café/cp437_encoded_dirs.txt","cp437_encoded_dirs.txt","Extension","Done","97","File","txt","2020-06-22T19:38:22","false","0c391e403302385e9d227733fc477bf440f978d2","1","x-fmt/111","text/plain","Plain Text File",""
"68","59","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji","emoji","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"69","68","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji/chess-%E2%99%95%E2%99%96%E2%99%97%E2%99%98%E2%99%99%E2%99%9A%E2%99%9B%E2%99%9C%E2%99%9D%E2%99%9E%E2%99%9F/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji/chess-♕♖♗♘♙♚♛♜♝♞♟","chess-♕♖♗♘♙♚♛♜♝♞♟","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"75","69","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji/chess-%E2%99%95%E2%99%96%E2%99%97%E2%99%98%E2%99%99%E2%99%9A%E2%99%9B%E2%99%9C%E2%99%9D%E2%99%9E%E2%99%9F/utf-8_encoded_dirs.txt","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji/chess-♕♖♗♘♙♚♛♜♝♞♟/utf-8_encoded_dirs.txt","utf-8_encoded_dirs.txt","Extension","Done","97","File","txt","2020-06-22T19:38:22","false","d0e093259ce05cde2b326e418ac547359b91ee5f","1","x-fmt/111","text/plain","Plain Text File",""
"70","68","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji/hearts-%E2%9D%A4%F0%9F%92%96%F0%9F%92%99%F0%9F%92%9A%F0%9F%92%9B%F0%9F%92%9C%F0%9F%92%9D/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji/hearts-❤💖💙💚💛💜💝","hearts-❤💖💙💚💛💜💝","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"74","70","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji/hearts-%E2%9D%A4%F0%9F%92%96%F0%9F%92%99%F0%9F%92%9A%F0%9F%92%9B%F0%9F%92%9C%F0%9F%92%9D/utf-8_encoded_dirs.txt","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji/hearts-❤💖💙💚💛💜💝/utf-8_encoded_dirs.txt","utf-8_encoded_dirs.txt","Extension","Done","97","File","txt","2020-06-22T19:38:22","false","d0e093259ce05cde2b326e418ac547359b91ee5f","1","x-fmt/111","text/plain","Plain Text File",""
"78","59","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/shift_jis/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/shift_jis","shift_jis","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"79","78","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/shift_jis/%E3%81%BD%E3%81%A3%E3%81%B7%E3%82%8B%E3%83%A1%E3%82%A4%E3%83%AB/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/shift_jis/ぽっぷるメイル","ぽっぷるメイル","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"85","79","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/shift_jis/%E3%81%BD%E3%81%A3%E3%81%B7%E3%82%8B%E3%83%A1%E3%82%A4%E3%83%AB/shift-jis_encoded_dirs.txt","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/shift_jis/ぽっぷるメイル/shift-jis_encoded_dirs.txt","shift-jis_encoded_dirs.txt","Extension","Done","101","File","txt","2020-06-22T19:38:22","false","023d81c0f5767ffa9eae763479bda378d5be4c4d","1","x-fmt/111","text/plain","Plain Text File",""
"76","59","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/windows_1252/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/windows_1252","windows_1252","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"77","76","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/windows_1252/s%C3%B8ster/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/windows_1252/søster","søster","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"83","77","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/windows_1252/s%C3%B8ster/cp1252_encoded_dirs.txt","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/windows_1252/søster/cp1252_encoded_dirs.txt","cp1252_encoded_dirs.txt","Extension","Done","98","File","txt","2020-06-22T19:38:22","false","4bc1d53ee7d365094fde303fec365b4fdec34c80","1","x-fmt/111","text/plain","Plain Text File",""
"54","2","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings","files_with_various_encodings","","Done","","Folder","","2021-07-25T14:05:46","false","","","","","",""
"56","54","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/emoji/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/emoji","emoji","","Done","","Folder","","2020-06-22T19:38:21","false","","","","","",""
"81","56","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/emoji/chess-%E2%99%95%E2%99%96%E2%99%97%E2%99%98%E2%99%99%E2%99%9A%E2%99%9B%E2%99%9C%E2%99%9D%E2%99%9E%E2%99%9F.txt","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/emoji/chess-♕♖♗♘♙♚♛♜♝♞♟.txt","chess-♕♖♗♘♙♚♛♜♝♞♟.txt","Extension","Done","54","File","txt","2020-06-22T19:38:21","false","1766219eb64113604a1fe2c003b10c8258bb1cbb","1","x-fmt/111","text/plain","Plain Text File",""
"63","56","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/emoji/hearts-%E2%9D%A4%F0%9F%92%96%F0%9F%92%99%F0%9F%92%9A%F0%9F%92%9B%F0%9F%92%9C%F0%9F%92%9D.txt","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/emoji/hearts-❤💖💙💚💛💜💝.txt","hearts-❤💖💙💚💛💜💝.txt","Extension","Done","54","File","txt","2020-06-22T19:38:21","false","1766219eb64113604a1fe2c003b10c8258bb1cbb","1","x-fmt/111","text/plain","Plain Text File",""
"57","54","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/windows_1252/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/windows_1252","windows_1252","","Done","","Folder","","2020-06-22T19:38:21","false","","","","","",""
"58","57","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/windows_1252/s%EF%BF%BDster","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/windows_1252/s�ster","s�ster","","Access denied","55","File","","2020-06-22T19:38:21","false","","0","","","",""
"3","2","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus","opf-format-corpus","","Done","","Folder","","2021-07-25T10:41:15","false","","","","","",""
"4","3","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video","video","","Done","","Folder","","2019-01-30T11:48:01","false","","","","","",""
"5","4","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime","Quicktime","","Done","","Folder","","2021-07-25T14:24:58","false","","","","","",""
"19","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/animation.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/animation.mov","animation.mov","Signature","Done","1020209","File","mov","2019-01-30T11:48:01","false","edb5226b963f449ce58054809149cb812bdf8c0a","1","x-fmt/384","video/quicktime","Quicktime",""
"8","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/apple-intermediate-codec.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/apple-intermediate-codec.mov","apple-intermediate-codec.mov","Signature","Done","319539","File","mov","2019-01-30T11:48:01","false","d097cf36467373f52b974542d48bec134279fa3f","1","x-fmt/384","video/quicktime","Quicktime",""
"11","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/apple-prores-422.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/apple-prores-422.mov","apple-prores-422.mov","Signature","Done","564775","File","mov","2019-01-30T11:48:01","false","faf81ab4a815cf0cd7c9b01d8ea950971d38dad1","1","x-fmt/384","video/quicktime","Quicktime",""
"14","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dv-dvchd-ntsc-interlaced.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dv-dvchd-ntsc-interlaced.mov","dv-dvchd-ntsc-interlaced.mov","Signature","Done","3001365","File","mov","2019-01-30T11:48:01","false","b9d45fd2e79a83c69afe95d89a846b96bf1778b7","1","x-fmt/384","video/quicktime","Quicktime",""
"9","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dv-dvchd-ntsc-progressive.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dv-dvchd-ntsc-progressive.mov","dv-dvchd-ntsc-progressive.mov","Signature","Done","3001365","File","mov","2019-01-30T11:48:01","false","a9caed081ab55ff1ea1b32d3eb30dab2841a9785","1","x-fmt/384","video/quicktime","Quicktime",""
"10","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dv-pal-interlaced.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dv-pal-interlaced.mov","dv-pal-interlaced.mov","Signature","Done","3601749","File","mov","2019-01-30T11:48:01","false","2ab26184bc937de129640574e75d01ed420cc19f","1","x-fmt/384","video/quicktime","Quicktime",""
"24","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-1080i50.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-1080i50.mov","dvcpro-hd-1080i50.mov","Signature","Done","14401365","File","mov","2019-01-30T11:48:01","false","a0629e27b3a4ba34e3a39d8525dcf8d3187df833","1","x-fmt/384","video/quicktime","Quicktime",""
"114","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-1080i60.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-1080i60.mov","dvcpro-hd-1080i60.mov","Signature","Done","12001365","File","mov","2019-01-30T11:48:01","false","d36ba66836ccc9a011e1517121648a1ba9b2f9e6","1","x-fmt/384","video/quicktime","Quicktime",""
"23","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-1080p25.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-1080p25.mov","dvcpro-hd-1080p25.mov","Signature","Done","14401365","File","mov","2019-01-30T11:48:01","false","1ed7801d801562d05a1b0e8d75c3ddad0cffd14e","1","x-fmt/384","video/quicktime","Quicktime",""
"49","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-1080p30.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-1080p30.mov","dvcpro-hd-1080p30.mov","Signature","Done","12001365","File","mov","2019-01-30T11:48:01","false","89c41cf838e2c5762985f7696c3964189b67b7d1","1","x-fmt/384","video/quicktime","Quicktime",""
"16","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-720p50.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-720p50.mov","dvcpro-hd-720p50.mov","Signature","Done","7201357","File","mov","2019-01-30T11:48:01","false","e8f149fd7f008ddd46e24127f36c72851f476755","1","x-fmt/384","video/quicktime","Quicktime",""
"21","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-720p60.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-720p60.mov","dvcpro-hd-720p60.mov","Signature","Done","6001485","File","mov","2019-01-30T11:48:01","false","bf886861b087e6f823dfe967c28ee2e522acf252","1","x-fmt/384","video/quicktime","Quicktime",""
"25","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-pal-interlaced.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-pal-interlaced.mov","dvcpro-pal-interlaced.mov","Signature","Done","3601749","File","mov","2019-01-30T11:48:01","false","c3bc3d41c73024f5e12e661de693f78d673c700e","1","x-fmt/384","video/quicktime","Quicktime",""
"18","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-pal-progressive.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-pal-progressive.mov","dvcpro-pal-progressive.mov","Signature","Done","3601749","File","mov","2019-01-30T11:48:01","false","8f92210bd09f17bd40ac9dc17712abf271f4e346","1","x-fmt/384","video/quicktime","Quicktime",""
"20","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro50-pal-interlaced.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro50-pal-interlaced.mov","dvcpro50-pal-interlaced.mov","Signature","Done","7203433","File","mov","2019-01-30T11:48:01","false","8889f04906ab0b6944b52b5a53c91d0180f47806","1","x-fmt/384","video/quicktime","Quicktime",""
"39","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro50-pal-progressive.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro50-pal-progressive.mov","dvcpro50-pal-progressive.mov","Signature","Done","7203433","File","mov","2019-01-30T11:48:01","false","992d536199aedd26bfe9a1cf10535b931b20ad21","1","x-fmt/384","video/quicktime","Quicktime",""
"12","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/jpeg2000.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/jpeg2000.mov","jpeg2000.mov","Signature","Done","383905","File","mov","2019-01-30T11:48:01","true","1b799ef725179db58bc7972d976eca892a2d6aae","2","fmt/1280","","NCH Dictation Audio File","","x-fmt/384","video/quicktime","Quicktime",""
"6","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/photo-jpeg.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/photo-jpeg.mov","photo-jpeg.mov","Signature","Done","575929","File","mov","2019-01-30T11:48:01","false","fdcca488ab2d26e7981490c0200fe1d8d07519d5","1","x-fmt/384","video/quicktime","Quicktime",""
"7","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd-1080p25.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd-1080p25.mov","xdcam-hd-1080p25.mov","Signature","Done","694863","File","mov","2019-01-30T11:48:01","false","2d87b7896bd817f05ff0fdf272a099bce9d51989","1","x-fmt/384","video/quicktime","Quicktime",""
"17","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd-1080p30.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd-1080p30.mov","xdcam-hd-1080p30.mov","Signature","Done","583993","File","mov","2019-01-30T11:48:01","false","0cb012a44825a2b79c448477e4bbef16e49626ee","1","x-fmt/384","video/quicktime","Quicktime",""
"22","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-1080i50.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-1080i50.mov","xdcam-hd422-1080i50.mov","Signature","Done","6251203","File","mov","2019-01-30T11:48:01","false","95b15f2563753553a027216b404a81647c8fdf0d","1","x-fmt/384","video/quicktime","Quicktime",""
"13","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-1080i60.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-1080i60.mov","xdcam-hd422-1080i60.mov","Signature","Done","5215055","File","mov","2019-01-30T11:48:01","false","d945f00c85080386b11099a51cd4bf254598a1dd","1","x-fmt/384","video/quicktime","Quicktime",""
"15","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-720p30.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-720p30.mov","xdcam-hd422-720p30.mov","Signature","Done","5215055","File","mov","2019-01-30T11:48:01","false","020173c0d295ec2fc46f180d24d808218df471bd","1","x-fmt/384","video/quicktime","Quicktime",""
"51","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-720p50.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-720p50.mov","xdcam-hd422-720p50.mov","Signature","Done","3125967","File","mov","2019-01-30T11:48:01","false","8f5c817fb3f87306d228c953a0e0a94420166876","1","x-fmt/384","video/quicktime","Quicktime",""
"89","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-720p60.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-720p60.mov","xdcam-hd422-720p60.mov","Signature","Done","2607739","File","mov","2019-01-30T11:48:01","false","b8f3a3a714e33a805e3c31d36382a35898f7baf2","1","x-fmt/384","video/quicktime","Quicktime",""
"80","2","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/possible-multiples/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/possible-multiples","possible-multiples","","Done","","Folder","","2021-07-25T14:35:40","false","","","","","",""
"82","80","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/possible-multiples/fmt-140-signature-id-207.odb","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/possible-multiples/fmt-140-signature-id-207.odb","fmt-140-signature-id-207.odb","Extension","Done","105","File","odb","2020-01-25T03:00:27","false","2ea0aec422c06b7911aecce2d765f26ad13ff46f","2","fmt/444","","OpenDocument Database Format","1.1","fmt/424","","OpenDocument Database Format","1.2"
"84","80","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/possible-multiples/fmt-641-signature-id-970.erf","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/possible-multiples/fmt-641-signature-id-970.erf","fmt-641-signature-id-970.erf","Signature","Done","348","File","erf","2020-01-25T03:00:30","false","cb78e44553459826e0acfbf2c1a86a188d643e6b","1","fmt/641","","Epson Raw Image Format",""
"33","2","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats","synthetically_unknown_formats","","Done","","Folder","","2020-01-15T20:17:02","false","","","","","",""
"38","33","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/README.md","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/README.md","README.md","Extension","Done","1257","File","md","2020-01-15T20:17:02","false","7d64e7c306839b7c515859e2424a499e368644f3","1","fmt/1149","text/markdown","Markdown",""
"35","33","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/baseball.format","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/baseball.format","baseball.format","","Done","52","File","format","2020-01-15T20:17:02","false","98653b8ba394cce54882085b364bef3901175fbc","0","","","",""
"46","33","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/caboose.format","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/caboose.format","caboose.format","","Done","52","File","format","2020-01-15T20:17:02","false","bee62ff431a072f6f6932ba081e60697f3d38ef7","0","","","",""
"36","33","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/cassette.format","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/cassette.format","cassette.format","","Done","52","File","format","2020-01-15T20:17:02","false","2a7a5004b42079f79ce5616f68173f7e30f96a65","0","","","",""
"45","33","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/debateable.format","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/debateable.format","debateable.format","","Done","52","File","format","2020-01-15T20:17:02","false","f5ae2731456e03aa5af537f66542ba08ee4c7bc0","0","","","",""
"37","33","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/looseleaf.format","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/looseleaf.format","looseleaf.format","","Done","52","File","format","2020-01-15T20:17:02","false","89f55e08287c1d34a900c2974039c5b3088461c4","0","","","",""
"55","41","gz:file:///home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-four.tar.gz!/container-example-four.tar","","container-example-four.tar","Signature","Done","20480","Container","tar","","false","85d25d3668c2dbc287c345e787789a179018c89e","1","x-fmt/265","application/x-tar","Tape Archive Format",""
"86","55","tar:gz:file:///home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-four.tar.gz!/container-example-four.tar!/dirs_with_various_encodings/","","dirs_with_various_encodings","","Done","","Folder","","2021-07-25T17:09:09","false","","","","","",""
"92","86","tar:gz:file:///home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-four.tar.gz!/container-example-four.tar!/dirs_with_various_encodings/big5/","","big5","","Done","","Folder","","2021-07-25T17:09:09","false","","","","","",""
"93","92","tar:gz:file:///home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-four.tar.gz!/container-example-four.tar!/dirs_with_various_encodings/big5/廣州/","","廣州","","Done","","Folder","","2021-07-25T17:09:09","false","","","","","",""
"99","93","tar:gz:file:///home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-four.tar.gz!/container-example-four.tar!/dirs_with_various_encodings/big5/廣州/big5_encoded_dirs.txt","","big5_encoded_dirs.txt","Extension","Done","96","File","txt","2020-06-22T19:38:22","false","57573bf4b57e9215f598d97469bf5fcf0046ee73","1","x-fmt/111","text/plain","Plain Text File",""
"87","86","tar:gz:file:///home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-four.tar.gz!/container-example-four.tar!/dirs_with_various_encodings/cp437/","","cp437","","Done","","Folder","","2021-07-25T17:09:09","false","","","","","",""
"88","87","tar:gz:file:///home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-four.tar.gz!/container-example-four.tar!/dirs_with_various_encodings/cp437/año/","","año","","Done","","Folder","","2021-07-25T17:09:09","false","","","","","",""
"91","88","tar:gz:file:///home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-four.tar.gz!/container-example-four.tar!/dirs_with_various_encodings/cp437/año/cp437_encoded_dirs.txt","","cp437_encoded_dirs.txt","Extension","Done","97","File","txt","2020-06-22T19:38:22","false","0c391e403302385e9d227733fc477bf440f978d2","1","x-fmt/111","text/plain","Plain Text File",""
"90","87","tar:gz:file:///home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-four.tar.gz!/container-example-four.tar!/dirs_with_various_encodings/cp437/café/","","café","","Done","","Folder","","2021-07-25T17:09:09","false","","","","","",""
"107","90","tar:gz:file:///home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-four.tar.gz!/container-example-four.tar!/dirs_with_various_encodings/cp437/café/cp437_encoded_dirs.txt","","cp437_encoded_dirs.txt","Extension","Done","97","File","txt","2020-06-22T19:38:22","false","0c391e403302385e9d227733fc477bf440f978d2","1","x-fmt/111","text/plain","Plain Text File",""
"94","86","tar:gz:file:///home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-four.tar.gz!/container-example-four.tar!/dirs_with_various_encodings/emoji/","","emoji","","Done","","Folder","","2021-07-25T17:09:09","false","","","","","",""
"96","94","tar:gz:file:///home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-four.tar.gz!/container-example-four.tar!/dirs_with_various_encodings/emoji/chess-♕♖♗♘♙♚♛♜♝♞♟/","","chess-♕♖♗♘♙♚♛♜♝♞♟","","Done","","Folder","","2021-07-25T17:09:09","false","","","","","",""
"98","96","tar:gz:file:///home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-four.tar.gz!/container-example-four.tar!/dirs_with_various_encodings/emoji/chess-♕♖♗♘♙♚♛♜♝♞♟/utf-8_encoded_dirs.txt","","utf-8_encoded_dirs.txt","Extension","Done","97","File","txt","2020-06-22T19:38:22","false","d0e093259ce05cde2b326e418ac547359b91ee5f","1","x-fmt/111","text/plain","Plain Text File",""
"97","94","tar:gz:file:///home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-four.tar.gz!/container-example-four.tar!/dirs_with_various_encodings/emoji/hearts-❤💖💙💚💛💜💝/","","hearts-❤💖💙💚💛💜💝","","Done","","Folder","","2021-07-25T17:09:09","false","","","","","",""
"100","97","tar:gz:file:///home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-four.tar.gz!/container-example-four.tar!/dirs_with_various_encodings/emoji/hearts-❤💖💙💚💛💜💝/utf-8_encoded_dirs.txt","","utf-8_encoded_dirs.txt","Extension","Done","97","File","txt","2020-06-22T19:38:22","false","d0e093259ce05cde2b326e418ac547359b91ee5f","1","x-fmt/111","text/plain","Plain Text File",""
"104","86","tar:gz:file:///home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-four.tar.gz!/container-example-four.tar!/dirs_with_various_encodings/shift_jis/","","shift_jis","","Done","","Folder","","2021-07-25T17:09:09","false","","","","","",""
"105","104","tar:gz:file:///home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-four.tar.gz!/container-example-four.tar!/dirs_with_various_encodings/shift_jis/ぽっぷるメイル/","","ぽっぷるメイル","","Done","","Folder","","2021-07-25T17:09:09","false","","","","","",""
"113","105","tar:gz:file:///home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-four.tar.gz!/container-example-four.tar!/dirs_with_various_encodings/shift_jis/ぽっぷるメイル/shift-jis_encoded_dirs.txt","","shift-jis_encoded_dirs.txt","Extension","Done","101","File","txt","2020-06-22T19:38:22","false","023d81c0f5767ffa9eae763479bda378d5be4c4d","1","x-fmt/111","text/plain","Plain Text File",""
"101","86","tar:gz:file:///home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-four.tar.gz!/container-example-four.tar!/dirs_with_various_encodings/windows_1252/","","windows_1252","","Done","","Folder","","2021-07-25T17:09:09","false","","","","","",""
"102","101","tar:gz:file:///home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-four.tar.gz!/container-example-four.tar!/dirs_with_various_encodings/windows_1252/søster/","","søster","","Done","","Folder","","2021-07-25T17:09:09","false","","","","","",""
"108","102","tar:gz:file:///home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-four.tar.gz!/container-example-four.tar!/dirs_with_various_encodings/windows_1252/søster/cp1252_encoded_dirs.txt","","cp1252_encoded_dirs.txt","Extension","Done","98","File","txt","2020-06-22T19:38:22","false","4bc1d53ee7d365094fde303fec365b4fdec34c80","1","x-fmt/111","text/plain","Plain Text File",""
"47","43","zip:file:///home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-one.zip!/container-objects/","","container-objects","","Done","","Folder","","","false","","","","","",""
"95","47","zip:file:///home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-one.zip!/container-objects/fmt-412-container-signature-id-1050.docx","","fmt-412-container-signature-id-1050.docx","Container","Done","49476","File","docx","2020-11-30T03:21:34","false","874586e61e15f9ee4c563514c85dbc36c6043382","1","fmt/412","application/vnd.openxmlformats-officedocument.wordprocessingml.document","Microsoft Word for Windows","2007 onwards"
"103","47","zip:file:///home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-one.zip!/container-objects/fmt-443-container-signature-id-13020.vsd","","fmt-443-container-signature-id-13020.vsd","Container","Done","2560","File","vsd","2020-11-30T03:21:36","false","87ddd36d2c1a58aefee26fdf51c2c2d01f70d222","1","fmt/443","application/vnd.visio","Microsoft Visio Drawing","2003-2010"
"112","47","zip:file:///home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-one.zip!/container-objects/fmt-631-container-signature-id-3080.potx","","fmt-631-container-signature-id-3080.potx","Container","Done","2276","File","potx","2020-11-30T03:21:36","false","6bf762330931ffef2508cf447f047cf39e19702f","1","fmt/631","application/vnd.openxmlformats-officedocument.presentationml.template","Microsoft PowerPoint Template","2007"
"106","47","zip:file:///home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-one.zip!/container-objects/fmt-853-container-signature-id-22520.dpp","","fmt-853-container-signature-id-22520.dpp","Container","Done","4096","File","dpp","2020-11-30T03:21:36","false","b0f15c05ab430a7c0c62c20e6665b4e34f2f393a","1","fmt/853","","Serif DrawPlus Drawing","5"
"110","47","zip:file:///home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-one.zip!/container-objects/fmt-999-container-signature-id-32010.kra","","fmt-999-container-signature-id-32010.kra","Container","Done","133","File","kra","2020-11-30T03:21:36","false","5781bbf44a3e3bb43a9e583c8a06661070330ef6","1","fmt/999","application/x-krita","Krita Document Format",""
"111","47","zip:file:///home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-one.zip!/container-objects/x-fmt-401-container-signature-id-23125.sda","","x-fmt-401-container-signature-id-23125.sda","Container","Done","2560","File","sda","2020-11-30T03:21:36","false","660ca1d7ce34caba8be18203018d9555d937cf0f","1","x-fmt/401","application/vnd.stardivision.draw","StarOffice Draw","5.x"
"109","47","zip:file:///home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/container-example-one.zip!/container-objects/x-fmt-88-container-signature-id-3130.ppt","","x-fmt-88-container-signature-id-3130.ppt","Container","Done","2560","File","ppt","2020-11-30T03:21:36","false","2fd03bafdcf3d9d9d60f773efa37115c322e5175","1","x-fmt/88","application/vnd.ms-powerpoint","Microsoft Powerpoint Presentation","4.0"
"""


def setup_denylist():
    """Return a processed Denylist to provide to Demystify analysis."""
    return {"denylist": "denylist"}


def test_denylist_droid(tmp_path):
    """Test basic configuration of Denylist and rogues here."""

    dir_ = tmp_path
    droid_csv = dir_ / "droid_💜_test.csv"
    droid_csv.write_text(DROID_CSV.strip())

    denylist = setup_denylist()
    assert denylist == {"denylist": "denylist"}

    # Analysis from CSV will currently read the results from the CSV
    # above and output an on-disk sqlite database at tmp_path. This
    # works perfectly for us. In future, if we need to create an
    # in-memory database for any reason we can but it will take some
    # further refactoring.
    res = analysis_from_csv(str(droid_csv), True, denylist, False, False)
    assert res.analysis_results.rogue_pronom_ns_id == None


SF_DUPES_TEST = u"""---
siegfried   : 1.9.1
scandate    : 2022-01-08T19:11:23+01:00
signature   : default.sig
created     : 2020-10-06T19:13:40+02:00
identifiers :
  - name    : 'pronom'
    details : 'DROID_SignatureFile_V97.xml; container-signature-20201001.xml'
---
filename : 'one_dupe_one'
filesize : 5
modified : 2022-01-08T19:10:40+01:00
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
filename : 'one_dupe_two'
filesize : 5
modified : 2022-01-08T19:10:42+01:00
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
filename : 'two_dupe_one'
filesize : 9
modified : 2022-01-08T19:10:56+01:00
errors   :
md5      : 64565b5c3348238da6cdc749a1bf2206
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/111'
    format  : 'Plain Text File'
    version :
    mime    : 'text/plain'
    basis   : 'text match ASCII'
    warning : 'match on text only; extension mismatch'
---
filename : 'two_dupe_three'
filesize : 9
modified : 2022-01-08T19:11:05+01:00
errors   :
md5      : 64565b5c3348238da6cdc749a1bf2206
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/111'
    format  : 'Plain Text File'
    version :
    mime    : 'text/plain'
    basis   : 'text match ASCII'
    warning : 'match on text only; extension mismatch'
---
filename : 'two_dupe_two'
filesize : 9
modified : 2022-01-08T19:11:14+01:00
errors   :
md5      : 64565b5c3348238da6cdc749a1bf2206
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/111'
    format  : 'Plain Text File'
    version :
    mime    : 'text/plain'
    basis   : 'text match ASCII'
    warning : 'match on text only; extension mismatch'
"""


def test_denylist_sf(tmp_path):
    """Ensure that duplicates when checksums are enabled in Siegfried
    are picked up as expected.
    """

    dir_ = tmp_path
    sf_yaml = dir_ / "sf_💜_test.yaml"
    sf_yaml.write_text(SF_DUPES_TEST.strip())

    denylist = setup_denylist()
    assert denylist == {"denylist": "denylist"}

    # Analysis from YAML will currently read the results from the YAML
    # above and output an on-disk sqlite database at tmp_path. This
    # works perfectly for us. In future, if we need to create an
    # in-memory database for any reason we can but it will take some
    # further refactoring.
    res = analysis_from_csv(str(sf_yaml), True, denylist, False, False)


@pytest.fixture(scope="function")
def rogueconfig(tmp_path):
    """Read Rogues configuration and supply it to a function as a
    test fixture.
    """
    dir_ = tmp_path
    denylist = dir_ / "deny_💜_list.cfg"
    denylist.write_text(DENYLIST.strip())
    config = ConfigParser.RawConfigParser()
    config.read(str(denylist))
    return config


def test_rogues_droid(tmp_path, rogueconfig):
    """pass"""

    dir_ = tmp_path
    droid_csv = dir_ / "droid_💜_test.csv"
    droid_csv.write_text(DROID_CSV.strip())

    denylist = setup_denylist()
    assert denylist == {"denylist": "denylist"}

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


def test_rogues_sf(tmp_path, capsys, rogueconfig):
    """pass"""

    dir_ = tmp_path
    sf_yaml = dir_ / "sf_💜_test.yaml"
    sf_yaml.write_text(SF_DUPES_TEST.strip())

    denylist = setup_denylist()
    assert denylist == {"denylist": "denylist"}

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
    assert captured.out == ""

    hero_output = rogueoutputclass(res.analysis_results, rogueconfig, True)
    hero_output.printTextResults()
    captured = capsys.readouterr()
    out = io.StringIO(captured.out)
    out_list = []
    for line in out:
        out_list.append(line.strip())
    out_list.sort()
    assert out_list == [
        "one_dupe_one",
        "one_dupe_two",
        "two_dupe_one",
        "two_dupe_three",
        "two_dupe_two",
    ]


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
