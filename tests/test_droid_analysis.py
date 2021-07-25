# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import sys

from demystify import analysis_from_csv

# "ID","PARENT_ID","URI","FILE_PATH","NAME","METHOD","STATUS","SIZE","TYPE","EXT","LAST_MODIFIED","EXTENSION_MISMATCH","SHA1_HASH","FORMAT_COUNT","PUID","MIME_TYPE","FORMAT_NAME","FORMAT_VERSION"
# "354","350","path_uri","path","fname","Container","Done","2044416","File","text","2012-07-26T23:02:40","trueX","b8be9dc84881300fd68b5d591d9a2a0fbef92757","1","fmt/126","MIME","Microsoft Powerpoint Presentation","97-2003"
# "29X","25X","path_uri","path","fname","Container","Done","4096XXX","File","dppX","2020-11-30T03:21:37","false","b0f15c05ab430a7c0c62c20e6665b4e34f2f393a","1","fmt/853","MIME","Serif DrawPlus DrawingXXXXXXXXXXX","5"


DROID_CSV = u""""ID","PARENT_ID","URI","FILE_PATH","NAME","METHOD","STATUS","SIZE","TYPE","EXT","LAST_MODIFIED","EXTENSION_MISMATCH","SHA1_HASH","FORMAT_COUNT","PUID","MIME_TYPE","FORMAT_NAME","FORMAT_VERSION"
"2","","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures","fixtures","","Done","","Folder","","2021-07-25T14:22:48","false","","","","","",""
"38","2","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types","archive-types","","Done","","Folder","","2021-07-25T14:05:08","false","","","","","",""
"47","38","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/fmt-1281-signature-id-1661.warc","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/fmt-1281-signature-id-1661.warc","fmt-1281-signature-id-1661.warc","Signature","Done","280","File","warc","2020-01-25T03:00:29","false","9e274dc22c244808be4673189c709f1817db0a10","1","fmt/1281","application/warc","WARC","1.1"
"41","38","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/fmt-289-signature-id-305.warc","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/fmt-289-signature-id-305.warc","fmt-289-signature-id-305.warc","Signature","Done","832","File","warc","2020-01-25T03:00:31","false","fdd6a6b1c3c39f7b6b52508fbcceb5eaabdfa5e9","1","fmt/289","application/warc","WARC",""
"45","38","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/fmt-410-signature-id-580.arc","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/fmt-410-signature-id-580.arc","fmt-410-signature-id-580.arc","Signature","Done","205","File","arc","2020-11-30T03:25:18","false","4da73922efb9e703c1b6e44f9eec57601261950f","1","fmt/410","","Internet Archive","1.1"
"43","38","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/x-fmt-219-signature-id-525.arc","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/x-fmt-219-signature-id-525.arc","x-fmt-219-signature-id-525.arc","Signature","Done","205","File","arc","2020-01-25T03:00:31","false","90c3f2741429079eb12a2dc270a067c1a643d1be","1","x-fmt/219","application/x-internet-archive","Internet Archive","1.0"
"77","38","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/x-fmt-263-signature-id-200.zip","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/x-fmt-263-signature-id-200.zip","x-fmt-263-signature-id-200.zip","Signature","Done","65572","File","zip","2020-11-30T03:25:20","false","a282da4e7700f342c80799f9eaff8a2181ef9c81","1","x-fmt/263","application/zip","ZIP Format",""
"44","38","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/x-fmt-266-signature-id-201.gz","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/archive-types/x-fmt-266-signature-id-201.gz","x-fmt-266-signature-id-201.gz","Signature","Done","3","File","gz","2020-11-30T03:25:20","false","c1df680e393d04a2a3b050a06db652e9ab37f761","1","x-fmt/266","application/gzip","GZIP Format",""
"25","2","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/container-objects/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/container-objects","container-objects","","Done","","Folder","","2021-07-25T14:07:30","false","","","","","",""
"30","25","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/container-objects/fmt-412-container-signature-id-1050.docx","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/container-objects/fmt-412-container-signature-id-1050.docx","fmt-412-container-signature-id-1050.docx","Container","Done","49476","File","docx","2020-11-30T03:21:35","false","874586e61e15f9ee4c563514c85dbc36c6043382","1","fmt/412","application/vnd.openxmlformats-officedocument.wordprocessingml.document","Microsoft Word for Windows","2007 onwards"
"36","25","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/container-objects/fmt-443-container-signature-id-13020.vsd","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/container-objects/fmt-443-container-signature-id-13020.vsd","fmt-443-container-signature-id-13020.vsd","Container","Done","2560","File","vsd","2020-11-30T03:21:36","false","87ddd36d2c1a58aefee26fdf51c2c2d01f70d222","1","fmt/443","application/vnd.visio","Microsoft Visio Drawing","2003-2010"
"31","25","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/container-objects/fmt-631-container-signature-id-3080.potx","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/container-objects/fmt-631-container-signature-id-3080.potx","fmt-631-container-signature-id-3080.potx","Container","Done","2276","File","potx","2020-11-30T03:21:36","false","6bf762330931ffef2508cf447f047cf39e19702f","1","fmt/631","application/vnd.openxmlformats-officedocument.presentationml.template","Microsoft PowerPoint Template","2007"
"29","25","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/container-objects/fmt-853-container-signature-id-22520.dpp","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/container-objects/fmt-853-container-signature-id-22520.dpp","fmt-853-container-signature-id-22520.dpp","Container","Done","4096","File","dpp","2020-11-30T03:21:37","false","b0f15c05ab430a7c0c62c20e6665b4e34f2f393a","1","fmt/853","","Serif DrawPlus Drawing","5"
"27","25","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/container-objects/fmt-999-container-signature-id-32010.kra","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/container-objects/fmt-999-container-signature-id-32010.kra","fmt-999-container-signature-id-32010.kra","Container","Done","133","File","kra","2020-11-30T03:21:37","false","5781bbf44a3e3bb43a9e583c8a06661070330ef6","1","fmt/999","application/x-krita","Krita Document Format",""
"28","25","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/container-objects/x-fmt-401-container-signature-id-23125.sda","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/container-objects/x-fmt-401-container-signature-id-23125.sda","x-fmt-401-container-signature-id-23125.sda","Container","Done","2560","File","sda","2020-11-30T03:21:37","false","660ca1d7ce34caba8be18203018d9555d937cf0f","1","x-fmt/401","application/vnd.stardivision.draw","StarOffice Draw","5.x"
"26","25","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/container-objects/x-fmt-88-container-signature-id-3130.ppt","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/container-objects/x-fmt-88-container-signature-id-3130.ppt","x-fmt-88-container-signature-id-3130.ppt","Container","Done","2560","File","ppt","2020-11-30T03:21:36","false","2fd03bafdcf3d9d9d60f773efa37115c322e5175","1","x-fmt/88","application/vnd.ms-powerpoint","Microsoft Powerpoint Presentation","4.0"
"54","2","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings","dirs_with_various_encodings","","Done","","Folder","","2021-07-25T10:40:16","false","","","","","",""
"58","54","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/big5/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/big5","big5","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"59","58","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/big5/%E5%BB%A3%E5%B7%9E/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/big5/廣州","廣州","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"65","59","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/big5/%E5%BB%A3%E5%B7%9E/big5_encoded_dirs.txt","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/big5/廣州/big5_encoded_dirs.txt","big5_encoded_dirs.txt","Extension","Done","96","File","txt","2020-06-22T19:38:22","false","57573bf4b57e9215f598d97469bf5fcf0046ee73","1","x-fmt/111","text/plain","Plain Text File",""
"55","54","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437","cp437","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"56","55","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437/a%C3%B1o/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437/año","año","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"60","56","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437/a%C3%B1o/cp437_encoded_dirs.txt","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437/año/cp437_encoded_dirs.txt","cp437_encoded_dirs.txt","Extension","Done","97","File","txt","2020-06-22T19:38:22","false","0c391e403302385e9d227733fc477bf440f978d2","1","x-fmt/111","text/plain","Plain Text File",""
"57","55","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437/caf%C3%A9/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437/café","café","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"64","57","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437/caf%C3%A9/cp437_encoded_dirs.txt","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437/café/cp437_encoded_dirs.txt","cp437_encoded_dirs.txt","Extension","Done","97","File","txt","2020-06-22T19:38:22","false","0c391e403302385e9d227733fc477bf440f978d2","1","x-fmt/111","text/plain","Plain Text File",""
"61","54","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji","emoji","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"62","61","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji/chess-%E2%99%95%E2%99%96%E2%99%97%E2%99%98%E2%99%99%E2%99%9A%E2%99%9B%E2%99%9C%E2%99%9D%E2%99%9E%E2%99%9F/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji/chess-♕♖♗♘♙♚♛♜♝♞♟","chess-♕♖♗♘♙♚♛♜♝♞♟","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"68","62","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji/chess-%E2%99%95%E2%99%96%E2%99%97%E2%99%98%E2%99%99%E2%99%9A%E2%99%9B%E2%99%9C%E2%99%9D%E2%99%9E%E2%99%9F/utf-8_encoded_dirs.txt","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji/chess-♕♖♗♘♙♚♛♜♝♞♟/utf-8_encoded_dirs.txt","utf-8_encoded_dirs.txt","Extension","Done","97","File","txt","2020-06-22T19:38:22","false","d0e093259ce05cde2b326e418ac547359b91ee5f","1","x-fmt/111","text/plain","Plain Text File",""
"63","61","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji/hearts-%E2%9D%A4%F0%9F%92%96%F0%9F%92%99%F0%9F%92%9A%F0%9F%92%9B%F0%9F%92%9C%F0%9F%92%9D/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji/hearts-❤💖💙💚💛💜💝","hearts-❤💖💙💚💛💜💝","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"72","63","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji/hearts-%E2%9D%A4%F0%9F%92%96%F0%9F%92%99%F0%9F%92%9A%F0%9F%92%9B%F0%9F%92%9C%F0%9F%92%9D/utf-8_encoded_dirs.txt","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji/hearts-❤💖💙💚💛💜💝/utf-8_encoded_dirs.txt","utf-8_encoded_dirs.txt","Extension","Done","97","File","txt","2020-06-22T19:38:22","false","d0e093259ce05cde2b326e418ac547359b91ee5f","1","x-fmt/111","text/plain","Plain Text File",""
"69","54","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/shift_jis/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/shift_jis","shift_jis","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"70","69","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/shift_jis/%E3%81%BD%E3%81%A3%E3%81%B7%E3%82%8B%E3%83%A1%E3%82%A4%E3%83%AB/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/shift_jis/ぽっぷるメイル","ぽっぷるメイル","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"74","70","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/shift_jis/%E3%81%BD%E3%81%A3%E3%81%B7%E3%82%8B%E3%83%A1%E3%82%A4%E3%83%AB/shift-jis_encoded_dirs.txt","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/shift_jis/ぽっぷるメイル/shift-jis_encoded_dirs.txt","shift-jis_encoded_dirs.txt","Extension","Done","101","File","txt","2020-06-22T19:38:22","false","023d81c0f5767ffa9eae763479bda378d5be4c4d","1","x-fmt/111","text/plain","Plain Text File",""
"66","54","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/windows_1252/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/windows_1252","windows_1252","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"67","66","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/windows_1252/s%C3%B8ster/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/windows_1252/søster","søster","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"71","67","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/windows_1252/s%C3%B8ster/cp1252_encoded_dirs.txt","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/windows_1252/søster/cp1252_encoded_dirs.txt","cp1252_encoded_dirs.txt","Extension","Done","98","File","txt","2020-06-22T19:38:22","false","4bc1d53ee7d365094fde303fec365b4fdec34c80","1","x-fmt/111","text/plain","Plain Text File",""
"48","2","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings","files_with_various_encodings","","Done","","Folder","","2021-07-25T14:05:46","false","","","","","",""
"49","48","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/emoji/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/emoji","emoji","","Done","","Folder","","2020-06-22T19:38:21","false","","","","","",""
"53","49","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/emoji/chess-%E2%99%95%E2%99%96%E2%99%97%E2%99%98%E2%99%99%E2%99%9A%E2%99%9B%E2%99%9C%E2%99%9D%E2%99%9E%E2%99%9F.txt","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/emoji/chess-♕♖♗♘♙♚♛♜♝♞♟.txt","chess-♕♖♗♘♙♚♛♜♝♞♟.txt","Extension","Done","54","File","txt","2020-06-22T19:38:21","false","1766219eb64113604a1fe2c003b10c8258bb1cbb","1","x-fmt/111","text/plain","Plain Text File",""
"50","49","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/emoji/hearts-%E2%9D%A4%F0%9F%92%96%F0%9F%92%99%F0%9F%92%9A%F0%9F%92%9B%F0%9F%92%9C%F0%9F%92%9D.txt","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/emoji/hearts-❤💖💙💚💛💜💝.txt","hearts-❤💖💙💚💛💜💝.txt","Extension","Done","54","File","txt","2020-06-22T19:38:21","false","1766219eb64113604a1fe2c003b10c8258bb1cbb","1","x-fmt/111","text/plain","Plain Text File",""
"51","48","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/windows_1252/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/windows_1252","windows_1252","","Done","","Folder","","2020-06-22T19:38:21","false","","","","","",""
"52","51","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/windows_1252/s%EF%BF%BDster","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/windows_1252/s�ster","s�ster","","Access denied","55","File","","2020-06-22T19:38:21","false","","0","","","",""
"3","2","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus","opf-format-corpus","","Done","","Folder","","2021-07-25T10:41:15","false","","","","","",""
"4","3","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video","video","","Done","","Folder","","2019-01-30T11:48:01","false","","","","","",""
"5","4","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime","Quicktime","","Done","","Folder","","2021-07-25T14:24:58","false","","","","","",""
"20","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/animation.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/animation.mov","animation.mov","Signature","Done","1020209","File","mov","2019-01-30T11:48:01","false","edb5226b963f449ce58054809149cb812bdf8c0a","1","x-fmt/384","video/quicktime","Quicktime",""
"8","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/apple-intermediate-codec.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/apple-intermediate-codec.mov","apple-intermediate-codec.mov","Signature","Done","319539","File","mov","2019-01-30T11:48:01","false","d097cf36467373f52b974542d48bec134279fa3f","1","x-fmt/384","video/quicktime","Quicktime",""
"9","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/apple-prores-422.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/apple-prores-422.mov","apple-prores-422.mov","Signature","Done","564775","File","mov","2019-01-30T11:48:01","false","faf81ab4a815cf0cd7c9b01d8ea950971d38dad1","1","x-fmt/384","video/quicktime","Quicktime",""
"12","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dv-dvchd-ntsc-interlaced.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dv-dvchd-ntsc-interlaced.mov","dv-dvchd-ntsc-interlaced.mov","Signature","Done","3001365","File","mov","2019-01-30T11:48:01","false","b9d45fd2e79a83c69afe95d89a846b96bf1778b7","1","x-fmt/384","video/quicktime","Quicktime",""
"10","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dv-dvchd-ntsc-progressive.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dv-dvchd-ntsc-progressive.mov","dv-dvchd-ntsc-progressive.mov","Signature","Done","3001365","File","mov","2019-01-30T11:48:01","false","a9caed081ab55ff1ea1b32d3eb30dab2841a9785","1","x-fmt/384","video/quicktime","Quicktime",""
"11","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dv-pal-interlaced.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dv-pal-interlaced.mov","dv-pal-interlaced.mov","Signature","Done","3601749","File","mov","2019-01-30T11:48:01","false","2ab26184bc937de129640574e75d01ed420cc19f","1","x-fmt/384","video/quicktime","Quicktime",""
"24","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-1080i50.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-1080i50.mov","dvcpro-hd-1080i50.mov","Signature","Done","14401365","File","mov","2019-01-30T11:48:01","false","a0629e27b3a4ba34e3a39d8525dcf8d3187df833","1","x-fmt/384","video/quicktime","Quicktime",""
"81","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-1080i60.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-1080i60.mov","dvcpro-hd-1080i60.mov","Signature","Done","12001365","File","mov","2019-01-30T11:48:01","false","d36ba66836ccc9a011e1517121648a1ba9b2f9e6","1","x-fmt/384","video/quicktime","Quicktime",""
"15","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-1080p25.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-1080p25.mov","dvcpro-hd-1080p25.mov","Signature","Done","14401365","File","mov","2019-01-30T11:48:01","false","1ed7801d801562d05a1b0e8d75c3ddad0cffd14e","1","x-fmt/384","video/quicktime","Quicktime",""
"21","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-1080p30.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-1080p30.mov","dvcpro-hd-1080p30.mov","Signature","Done","12001365","File","mov","2019-01-30T11:48:01","false","89c41cf838e2c5762985f7696c3964189b67b7d1","1","x-fmt/384","video/quicktime","Quicktime",""
"16","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-720p50.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-720p50.mov","dvcpro-hd-720p50.mov","Signature","Done","7201357","File","mov","2019-01-30T11:48:01","false","e8f149fd7f008ddd46e24127f36c72851f476755","1","x-fmt/384","video/quicktime","Quicktime",""
"17","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-720p60.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-720p60.mov","dvcpro-hd-720p60.mov","Signature","Done","6001485","File","mov","2019-01-30T11:48:01","false","bf886861b087e6f823dfe967c28ee2e522acf252","1","x-fmt/384","video/quicktime","Quicktime",""
"22","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-pal-interlaced.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-pal-interlaced.mov","dvcpro-pal-interlaced.mov","Signature","Done","3601749","File","mov","2019-01-30T11:48:01","false","c3bc3d41c73024f5e12e661de693f78d673c700e","1","x-fmt/384","video/quicktime","Quicktime",""
"13","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-pal-progressive.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-pal-progressive.mov","dvcpro-pal-progressive.mov","Signature","Done","3601749","File","mov","2019-01-30T11:48:01","false","8f92210bd09f17bd40ac9dc17712abf271f4e346","1","x-fmt/384","video/quicktime","Quicktime",""
"46","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro50-pal-interlaced.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro50-pal-interlaced.mov","dvcpro50-pal-interlaced.mov","Signature","Done","7203433","File","mov","2019-01-30T11:48:01","false","8889f04906ab0b6944b52b5a53c91d0180f47806","1","x-fmt/384","video/quicktime","Quicktime",""
"80","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro50-pal-progressive.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro50-pal-progressive.mov","dvcpro50-pal-progressive.mov","Signature","Done","7203433","File","mov","2019-01-30T11:48:01","false","992d536199aedd26bfe9a1cf10535b931b20ad21","1","x-fmt/384","video/quicktime","Quicktime",""
"18","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/jpeg2000.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/jpeg2000.mov","jpeg2000.mov","Signature","Done","383905","File","mov","2019-01-30T11:48:01","true","1b799ef725179db58bc7972d976eca892a2d6aae","2","fmt/1280","","NCH Dictation Audio File","","x-fmt/384","video/quicktime","Quicktime",""
"7","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/photo-jpeg.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/photo-jpeg.mov","photo-jpeg.mov","Signature","Done","575929","File","mov","2019-01-30T11:48:01","false","fdcca488ab2d26e7981490c0200fe1d8d07519d5","1","x-fmt/384","video/quicktime","Quicktime",""
"6","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd-1080p25.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd-1080p25.mov","xdcam-hd-1080p25.mov","Signature","Done","694863","File","mov","2019-01-30T11:48:01","false","2d87b7896bd817f05ff0fdf272a099bce9d51989","1","x-fmt/384","video/quicktime","Quicktime",""
"19","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd-1080p30.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd-1080p30.mov","xdcam-hd-1080p30.mov","Signature","Done","583993","File","mov","2019-01-30T11:48:01","false","0cb012a44825a2b79c448477e4bbef16e49626ee","1","x-fmt/384","video/quicktime","Quicktime",""
"42","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-1080i50.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-1080i50.mov","xdcam-hd422-1080i50.mov","Signature","Done","6251203","File","mov","2019-01-30T11:48:01","false","95b15f2563753553a027216b404a81647c8fdf0d","1","x-fmt/384","video/quicktime","Quicktime",""
"14","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-1080i60.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-1080i60.mov","xdcam-hd422-1080i60.mov","Signature","Done","5215055","File","mov","2019-01-30T11:48:01","false","d945f00c85080386b11099a51cd4bf254598a1dd","1","x-fmt/384","video/quicktime","Quicktime",""
"78","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-720p30.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-720p30.mov","xdcam-hd422-720p30.mov","Signature","Done","5215055","File","mov","2019-01-30T11:48:01","false","020173c0d295ec2fc46f180d24d808218df471bd","1","x-fmt/384","video/quicktime","Quicktime",""
"23","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-720p50.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-720p50.mov","xdcam-hd422-720p50.mov","Signature","Done","3125967","File","mov","2019-01-30T11:48:01","false","8f5c817fb3f87306d228c953a0e0a94420166876","1","x-fmt/384","video/quicktime","Quicktime",""
"79","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-720p60.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-720p60.mov","xdcam-hd422-720p60.mov","Signature","Done","2607739","File","mov","2019-01-30T11:48:01","false","b8f3a3a714e33a805e3c31d36382a35898f7baf2","1","x-fmt/384","video/quicktime","Quicktime",""
"73","2","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/possible-multiples/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/possible-multiples","possible-multiples","","Done","","Folder","","2021-07-25T14:35:40","false","","","","","",""
"75","73","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/possible-multiples/fmt-140-signature-id-207.odb","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/possible-multiples/fmt-140-signature-id-207.odb","fmt-140-signature-id-207.odb","Signature","Done","105","File","odb","2020-01-25T03:00:27","false","2ea0aec422c06b7911aecce2d765f26ad13ff46f","2","fmt/444","","OpenDocument Database Format","1.1","fmt/424","","OpenDocument Database Format","1.2"
"76","73","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/possible-multiples/fmt-641-signature-id-970.erf","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/possible-multiples/fmt-641-signature-id-970.erf","fmt-641-signature-id-970.erf","Signature","Done","348","File","erf","2020-01-25T03:00:30","false","cb78e44553459826e0acfbf2c1a86a188d643e6b","1","fmt/641","","Epson Raw Image Format",""
"32","2","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats","synthetically_unknown_formats","","Done","","Folder","","2020-01-15T20:17:02","false","","","","","",""
"40","32","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/README.md","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/README.md","README.md","Extension","Done","1257","File","md","2020-01-15T20:17:02","false","7d64e7c306839b7c515859e2424a499e368644f3","1","fmt/1149","text/markdown","Markdown",""
"37","32","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/baseball.format","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/baseball.format","baseball.format","","Done","52","File","format","2020-01-15T20:17:02","false","98653b8ba394cce54882085b364bef3901175fbc","0","","","",""
"34","32","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/caboose.format","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/caboose.format","caboose.format","","Done","52","File","format","2020-01-15T20:17:02","false","bee62ff431a072f6f6932ba081e60697f3d38ef7","0","","","",""
"39","32","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/cassette.format","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/cassette.format","cassette.format","","Done","52","File","format","2020-01-15T20:17:02","false","2a7a5004b42079f79ce5616f68173f7e30f96a65","0","","","",""
"35","32","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/debateable.format","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/debateable.format","debateable.format","","Done","52","File","format","2020-01-15T20:17:02","false","f5ae2731456e03aa5af537f66542ba08ee4c7bc0","0","","","",""
"33","32","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/looseleaf.format","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/looseleaf.format","looseleaf.format","","Done","52","File","format","2020-01-15T20:17:02","false","89f55e08287c1d34a900c2974039c5b3088461c4","0","","","",""
"""

SIEGFRIED_YAML = u"""---
siegfried   : 1.9.1
scandate    : 2021-07-25T14:37:43+02:00
signature   : default.sig
created     : 2020-10-06T19:15:15+02:00
identifiers :
  - name    : 'pronom'
    details : 'DROID_SignatureFile_V97.xml; container-signature-20201001.xml'
  - name    : 'tika'
    details : 'tika-mimetypes.xml (1.24, 2020-04-17)'
  - name    : 'freedesktop.org'
    details : 'freedesktop.org.xml (2.0, 2020-06-05)'
  - name    : 'loc'
    details : 'fddXML.zip (2020-09-02, DROID_SignatureFile_V97.xml, container-signature-20201001.xml)'
---
filename : 'fixtures/archive-types/fmt-1281-signature-id-1661.warc'
filesize : 280
modified : 2020-01-25T03:00:29+01:00
errors   :
md5      : 2102b96008741e77b4d2e31c7ea3fe70
matches  :
  - ns      : 'pronom'
    id      : 'fmt/1281'
    format  : 'WARC'
    version : '1.1'
    mime    : 'application/warc'
    basis   : 'extension match warc; byte match at 0, 280'
    warning :
  - ns      : 'tika'
    id      : 'application/warc'
    format  : 'WARC'
    mime    : 'application/warc'
    basis   : 'extension match warc; byte match at 0, 5'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'UNKNOWN'
    format  :
    mime    : 'UNKNOWN'
    basis   :
    warning : 'no match'
  - ns      : 'loc'
    id      : 'fdd000236'
    format  : 'WARC, Web ARChive file format'
    full    : 'WARC (Web ARChive) file format'
    mime    : 'application/warc'
    basis   : 'extension match warc; byte match at 0, 280'
    warning :
---
filename : 'fixtures/archive-types/fmt-289-signature-id-305.warc'
filesize : 832
modified : 2020-01-25T03:00:31+01:00
errors   :
md5      : 83becbc69c96130d249a82105b9f428a
matches  :
  - ns      : 'pronom'
    id      : 'fmt/289'
    format  : 'WARC'
    version :
    mime    : 'application/warc'
    basis   : 'extension match warc; byte match at 0, 19'
    warning :
  - ns      : 'tika'
    id      : 'application/warc'
    format  : 'WARC'
    mime    : 'application/warc'
    basis   : 'extension match warc; byte match at 0, 5'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'UNKNOWN'
    format  :
    mime    : 'UNKNOWN'
    basis   :
    warning : 'no match'
  - ns      : 'loc'
    id      : 'fdd000236'
    format  : 'WARC, Web ARChive file format'
    full    : 'WARC (Web ARChive) file format'
    mime    : 'application/warc'
    basis   : 'extension match warc; byte match at 0, 19'
    warning :
---
filename : 'fixtures/archive-types/fmt-410-signature-id-580.arc'
filesize : 205
modified : 2020-11-30T03:25:18+01:00
errors   :
md5      : 8e910e85838fd4cd7fc8e70159d198a0
matches  :
  - ns      : 'pronom'
    id      : 'fmt/410'
    format  : 'Internet Archive'
    version : '1.1'
    mime    :
    basis   : 'extension match arc; byte match at [[0 129] [149 56]]'
    warning :
  - ns      : 'tika'
    id      : 'application/x-internet-archive'
    format  : 'ARC'
    mime    : 'application/x-internet-archive'
    basis   : 'extension match arc; byte match at 0, 11'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'UNKNOWN'
    format  :
    mime    : 'UNKNOWN'
    basis   :
    warning : 'no match'
  - ns      : 'loc'
    id      : 'fdd000235'
    format  : 'ARC_IA, Internet Archive ARC file format'
    full    : 'ARC_IA, Internet Archive ARC file format.'
    mime    :
    basis   : 'extension match arc'
    warning : 'match on extension only'
---
filename : 'fixtures/archive-types/x-fmt-219-signature-id-525.arc'
filesize : 205
modified : 2020-01-25T03:00:31+01:00
errors   :
md5      : bb430b824544bc4250461f3c61de3be8
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/219'
    format  : 'Internet Archive'
    version : '1.0'
    mime    : 'application/x-internet-archive'
    basis   : 'extension match arc; byte match at [[0 129] [149 56]]'
    warning :
  - ns      : 'tika'
    id      : 'application/x-internet-archive'
    format  : 'ARC'
    mime    : 'application/x-internet-archive'
    basis   : 'extension match arc; byte match at 0, 11'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'UNKNOWN'
    format  :
    mime    : 'UNKNOWN'
    basis   :
    warning : 'no match'
  - ns      : 'loc'
    id      : 'fdd000235'
    format  : 'ARC_IA, Internet Archive ARC file format'
    full    : 'ARC_IA, Internet Archive ARC file format.'
    mime    :
    basis   : 'extension match arc'
    warning : 'match on extension only'
---
filename : 'fixtures/archive-types/x-fmt-263-signature-id-200.zip'
filesize : 65572
modified : 2020-11-30T03:25:20+01:00
errors   :
md5      : ae7688484c891d3c27e65367988ef270
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/263'
    format  : 'ZIP Format'
    version :
    mime    : 'application/zip'
    basis   : 'extension match zip; container match with trigger and default extension'
    warning :
  - ns      : 'tika'
    id      : 'application/zip'
    format  : 'Compressed Archive File'
    mime    : 'application/zip'
    basis   : 'extension match zip; byte match at 0, 4 (signature 1/3)'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'application/zip'
    format  : 'Zip archive'
    mime    : 'application/zip'
    basis   : 'extension match zip; byte match at 0, 4'
    warning :
  - ns      : 'loc'
    id      : 'fdd000354'
    format  : 'ZIP File Format (PKWARE)'
    full    : 'ZIP File Format (PKWARE)'
    mime    : 'application/zip'
    basis   : 'extension match zip; extension match zip; container match with trigger and default extension'
    warning : 'extension mismatch'
---
filename : 'fixtures/archive-types/x-fmt-266-signature-id-201.gz'
filesize : 3
modified : 2020-11-30T03:25:20+01:00
errors   :
md5      : 613ffd2ae0a8828aa573ce62bf2e30c3
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/266'
    format  : 'GZIP Format'
    version :
    mime    : 'application/gzip'
    basis   : 'extension match gz; byte match at 0, 3'
    warning :
  - ns      : 'tika'
    id      : 'application/gzip'
    format  : 'Gzip Compressed Archive'
    mime    : 'application/gzip'
    basis   : 'extension match gz; byte match at 0, 2 (signature 1/2); byte match at 0, 2 (signature 2/2)'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'application/gzip'
    format  : 'Gzip archive'
    mime    : 'application/gzip'
    basis   : 'extension match gz; byte match at 0, 2'
    warning :
  - ns      : 'loc'
    id      : 'UNKNOWN'
    format  :
    full    :
    mime    :
    basis   :
    warning : 'no match'
---
filename : 'fixtures/container-objects/fmt-412-container-signature-id-1050.docx'
filesize : 49476
modified : 2020-11-30T03:21:35+01:00
errors   :
md5      : badba9781fbe694c1296dc642f70fd5d
matches  :
  - ns      : 'pronom'
    id      : 'fmt/412'
    format  : 'Microsoft Word for Windows'
    version : '2007 onwards'
    mime    : 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    basis   : 'extension match docx; container name [Content_Types].xml with byte match at 16384, 188 (signature 3/3)'
    warning :
  - ns      : 'tika'
    id      : 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    format  : 'Office Open XML Document'
    mime    : 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    basis   : 'extension match docx; byte match at [[0 4] [30 19]] (signature 1/2)'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    format  : 'Word 2007 document'
    mime    : 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    basis   : 'extension match docx; byte match at 0, 4'
    warning :
  - ns      : 'loc'
    id      : 'fdd000514'
    format  : 'Microsoft XML Paper Specification, (XPS)'
    full    : 'Microsoft XML Paper Specification, (XPS)'
    mime    : 'application/vnd.ms-xpsdocument'
    basis   : 'byte match at 0, 4'
    warning : 'extension mismatch'
---
filename : 'fixtures/container-objects/fmt-443-container-signature-id-13020.vsd'
filesize : 2560
modified : 2020-11-30T03:21:36+01:00
errors   :
md5      : 318a3848eb0829c1f6e2e2ce0575fc33
matches  :
  - ns      : 'pronom'
    id      : 'fmt/443'
    format  : 'Microsoft Visio Drawing'
    version : '2003-2010'
    mime    : 'application/vnd.visio'
    basis   : 'extension match vsd; container name VisioDocument with byte match at 0, 27'
    warning :
  - ns      : 'tika'
    id      : 'application/vnd.visio'
    format  : 'Microsoft Visio Diagram'
    mime    : 'application/vnd.visio'
    basis   : 'extension match vsd; byte match at 0, 8'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'application/vnd.visio'
    format  : 'Microsoft Visio document'
    mime    : 'application/vnd.visio'
    basis   : 'extension match vsd; byte match at 0, 4 (signature 2/2); byte match at 0, 8 (signature 1/2)'
    warning :
  - ns      : 'loc'
    id      : 'fdd000380'
    format  : 'Microsoft Compound File Binary File Format, Version 3'
    full    : 'Microsoft Compound File Binary File Format, Version 3'
    mime    :
    basis   : 'byte match at 0, 8'
    warning :
---
filename : 'fixtures/container-objects/fmt-631-container-signature-id-3080.potx'
filesize : 2276
modified : 2020-11-30T03:21:36+01:00
errors   :
md5      : fcd5800db9fcc15dbb2fb3f04e7627ac
matches  :
  - ns      : 'pronom'
    id      : 'fmt/631'
    format  : 'Microsoft PowerPoint Template'
    version : '2007'
    mime    : 'application/vnd.openxmlformats-officedocument.presentationml.template'
    basis   : 'extension match potx; container name [Content_Types].xml with byte match at 2048, 92'
    warning :
  - ns      : 'tika'
    id      : 'application/vnd.openxmlformats-officedocument.presentationml.template'
    format  : 'Office Open XML Presentation Template'
    mime    : 'application/vnd.openxmlformats-officedocument.presentationml.template'
    basis   : 'extension match potx; byte match at [[0 4] [30 19]] (signature 1/2)'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'application/vnd.openxmlformats-officedocument.presentationml.template'
    format  : 'PowerPoint 2007 presentation template'
    mime    : 'application/vnd.openxmlformats-officedocument.presentationml.template'
    basis   : 'extension match potx; byte match at 0, 4'
    warning :
  - ns      : 'loc'
    id      : 'fdd000514'
    format  : 'Microsoft XML Paper Specification, (XPS)'
    full    : 'Microsoft XML Paper Specification, (XPS)'
    mime    : 'application/vnd.ms-xpsdocument'
    basis   : 'byte match at 0, 4'
    warning : 'extension mismatch'
---
filename : 'fixtures/container-objects/fmt-853-container-signature-id-22520.dpp'
filesize : 4096
modified : 2020-11-30T03:21:37+01:00
errors   :
md5      : 1e729d44750c2ad9b59d069504edff22
matches  :
  - ns      : 'pronom'
    id      : 'fmt/853'
    format  : 'Serif DrawPlus Drawing'
    version : '5'
    mime    :
    basis   : 'extension match dpp; container name SummaryInformation with byte match at 512, 16'
    warning :
  - ns      : 'tika'
    id      : 'application/x-tika-msoffice'
    format  :
    mime    : 'application/x-tika-msoffice'
    basis   : 'byte match at 0, 8'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'application/x-ole-storage'
    format  : 'OLE2 compound document storage'
    mime    : 'application/x-ole-storage'
    basis   : 'byte match at 0, 4 (signature 2/2); byte match at 0, 8 (signature 1/2)'
    warning :
  - ns      : 'loc'
    id      : 'fdd000380'
    format  : 'Microsoft Compound File Binary File Format, Version 3'
    full    : 'Microsoft Compound File Binary File Format, Version 3'
    mime    :
    basis   : 'byte match at 0, 8'
    warning :
---
filename : 'fixtures/container-objects/fmt-999-container-signature-id-32010.kra'
filesize : 133
modified : 2020-11-30T03:21:37+01:00
errors   :
md5      : a1348398bc6ed5fda5c01034f0747e1a
matches  :
  - ns      : 'pronom'
    id      : 'fmt/999'
    format  : 'Krita Document Format'
    version :
    mime    : 'application/x-krita'
    basis   : 'extension match kra; container name mimetype with byte match at 0, 19'
    warning :
  - ns      : 'tika'
    id      : 'application/zip'
    format  : 'Compressed Archive File'
    mime    : 'application/zip'
    basis   : 'byte match at 0, 4 (signature 1/3)'
    warning : 'filename mismatch'
  - ns      : 'freedesktop.org'
    id      : 'application/x-krita'
    format  : 'Krita document'
    mime    : 'application/x-krita'
    basis   : 'extension match kra; byte match at [[0 4] [30 8] [38 19]] (signature 2/2)'
    warning :
  - ns      : 'loc'
    id      : 'fdd000514'
    format  : 'Microsoft XML Paper Specification, (XPS)'
    full    : 'Microsoft XML Paper Specification, (XPS)'
    mime    : 'application/vnd.ms-xpsdocument'
    basis   : 'byte match at 0, 4'
    warning : 'extension mismatch'
---
filename : 'fixtures/container-objects/x-fmt-401-container-signature-id-23125.sda'
filesize : 2560
modified : 2020-11-30T03:21:37+01:00
errors   :
md5      : 254d1ed4e37720b38437661769339789
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/401'
    format  : 'StarOffice Draw'
    version : '5.x'
    mime    : 'application/vnd.stardivision.draw'
    basis   : 'extension match sda; container name CompObj with byte match at 64, 16 (signature 2/2)'
    warning :
  - ns      : 'tika'
    id      : 'application/vnd.stardivision.draw'
    format  :
    mime    : 'application/vnd.stardivision.draw'
    basis   : 'extension match sda; byte match at [[0 8] [2117 8]]'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'application/x-ole-storage'
    format  : 'OLE2 compound document storage'
    mime    : 'application/x-ole-storage'
    basis   : 'byte match at 0, 4 (signature 2/2); byte match at 0, 8 (signature 1/2)'
    warning :
  - ns      : 'loc'
    id      : 'fdd000380'
    format  : 'Microsoft Compound File Binary File Format, Version 3'
    full    : 'Microsoft Compound File Binary File Format, Version 3'
    mime    :
    basis   : 'byte match at 0, 8'
    warning :
---
filename : 'fixtures/container-objects/x-fmt-88-container-signature-id-3130.ppt'
filesize : 2560
modified : 2020-11-30T03:21:36+01:00
errors   :
md5      : 082ffda1984467ec4febe8dbe354e4ce
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/88'
    format  : 'Microsoft Powerpoint Presentation'
    version : '4.0'
    mime    : 'application/vnd.ms-powerpoint'
    basis   : 'extension match ppt; container name PP40 with name only'
    warning :
  - ns      : 'tika'
    id      : 'application/vnd.ms-powerpoint'
    format  : 'Microsoft Powerpoint Presentation'
    mime    : 'application/vnd.ms-powerpoint'
    basis   : 'extension match ppt; byte match at 0, 8 (signature 2/2)'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'application/x-ole-storage'
    format  : 'OLE2 compound document storage'
    mime    : 'application/x-ole-storage'
    basis   : 'byte match at 0, 4 (signature 2/2); byte match at 0, 8 (signature 1/2)'
    warning :
  - ns      : 'loc'
    id      : 'fdd000380'
    format  : 'Microsoft Compound File Binary File Format, Version 3'
    full    : 'Microsoft Compound File Binary File Format, Version 3'
    mime    :
    basis   : 'byte match at 0, 8'
    warning :
---
filename : 'fixtures/dirs_with_various_encodings/big5/å»£å·ž/big5_encoded_dirs.txt'
filesize : 96
modified : 2020-06-22T19:38:22+02:00
errors   :
md5      : 5d2cd701d4735045d108c762240002ec
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/111'
    format  : 'Plain Text File'
    version :
    mime    : 'text/plain'
    basis   : 'extension match txt; text match ASCII'
    warning :
  - ns      : 'tika'
    id      : 'text/plain'
    format  :
    mime    : 'text/plain'
    basis   : 'extension match txt; text match ASCII'
    warning : 'match on filename and text only; byte/xml signatures for this format did not match'
  - ns      : 'freedesktop.org'
    id      : 'text/plain'
    format  : 'plain text document'
    mime    : 'text/plain'
    basis   : 'extension match txt; text match ASCII'
    warning : 'match on filename and text only; byte/xml signatures for this format did not match'
  - ns      : 'loc'
    id      : 'fdd000284'
    format  : 'ESRI ArcInfo Coverage'
    full    : 'ESRI ArcInfo Coverage'
    mime    :
    basis   : 'extension match txt'
    warning : 'match on extension only'
---
filename : 'fixtures/dirs_with_various_encodings/cp437/aÃ±o/cp437_encoded_dirs.txt'
filesize : 97
modified : 2020-06-22T19:38:22+02:00
errors   :
md5      : a2530a3d32134654f0bef01cf252afd7
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/111'
    format  : 'Plain Text File'
    version :
    mime    : 'text/plain'
    basis   : 'extension match txt; text match ASCII'
    warning :
  - ns      : 'tika'
    id      : 'text/plain'
    format  :
    mime    : 'text/plain'
    basis   : 'extension match txt; text match ASCII'
    warning : 'match on filename and text only; byte/xml signatures for this format did not match'
  - ns      : 'freedesktop.org'
    id      : 'text/plain'
    format  : 'plain text document'
    mime    : 'text/plain'
    basis   : 'extension match txt; text match ASCII'
    warning : 'match on filename and text only; byte/xml signatures for this format did not match'
  - ns      : 'loc'
    id      : 'fdd000284'
    format  : 'ESRI ArcInfo Coverage'
    full    : 'ESRI ArcInfo Coverage'
    mime    :
    basis   : 'extension match txt'
    warning : 'match on extension only'
---
filename : 'fixtures/dirs_with_various_encodings/cp437/cafÃ©/cp437_encoded_dirs.txt'
filesize : 97
modified : 2020-06-22T19:38:22+02:00
errors   :
md5      : a2530a3d32134654f0bef01cf252afd7
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/111'
    format  : 'Plain Text File'
    version :
    mime    : 'text/plain'
    basis   : 'extension match txt; text match ASCII'
    warning :
  - ns      : 'tika'
    id      : 'text/plain'
    format  :
    mime    : 'text/plain'
    basis   : 'extension match txt; text match ASCII'
    warning : 'match on filename and text only; byte/xml signatures for this format did not match'
  - ns      : 'freedesktop.org'
    id      : 'text/plain'
    format  : 'plain text document'
    mime    : 'text/plain'
    basis   : 'extension match txt; text match ASCII'
    warning : 'match on filename and text only; byte/xml signatures for this format did not match'
  - ns      : 'loc'
    id      : 'fdd000284'
    format  : 'ESRI ArcInfo Coverage'
    full    : 'ESRI ArcInfo Coverage'
    mime    :
    basis   : 'extension match txt'
    warning : 'match on extension only'
---
filename : 'fixtures/dirs_with_various_encodings/emoji/chess-â™•â™–â™—â™˜â™™â™šâ™›â™œâ™â™žâ™Ÿ/utf-8_encoded_dirs.txt'
filesize : 97
modified : 2020-06-22T19:38:22+02:00
errors   :
md5      : 2e58bf86585ae31fcd7112f1beee358b
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/111'
    format  : 'Plain Text File'
    version :
    mime    : 'text/plain'
    basis   : 'extension match txt; text match ASCII'
    warning :
  - ns      : 'tika'
    id      : 'text/plain'
    format  :
    mime    : 'text/plain'
    basis   : 'extension match txt; text match ASCII'
    warning : 'match on filename and text only; byte/xml signatures for this format did not match'
  - ns      : 'freedesktop.org'
    id      : 'text/plain'
    format  : 'plain text document'
    mime    : 'text/plain'
    basis   : 'extension match txt; text match ASCII'
    warning : 'match on filename and text only; byte/xml signatures for this format did not match'
  - ns      : 'loc'
    id      : 'fdd000284'
    format  : 'ESRI ArcInfo Coverage'
    full    : 'ESRI ArcInfo Coverage'
    mime    :
    basis   : 'extension match txt'
    warning : 'match on extension only'
---
filename : 'fixtures/dirs_with_various_encodings/emoji/hearts-â¤ðŸ’–ðŸ’™ðŸ’šðŸ’›ðŸ’œðŸ’/utf-8_encoded_dirs.txt'
filesize : 97
modified : 2020-06-22T19:38:22+02:00
errors   :
md5      : 2e58bf86585ae31fcd7112f1beee358b
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/111'
    format  : 'Plain Text File'
    version :
    mime    : 'text/plain'
    basis   : 'extension match txt; text match ASCII'
    warning :
  - ns      : 'tika'
    id      : 'text/plain'
    format  :
    mime    : 'text/plain'
    basis   : 'extension match txt; text match ASCII'
    warning : 'match on filename and text only; byte/xml signatures for this format did not match'
  - ns      : 'freedesktop.org'
    id      : 'text/plain'
    format  : 'plain text document'
    mime    : 'text/plain'
    basis   : 'extension match txt; text match ASCII'
    warning : 'match on filename and text only; byte/xml signatures for this format did not match'
  - ns      : 'loc'
    id      : 'fdd000284'
    format  : 'ESRI ArcInfo Coverage'
    full    : 'ESRI ArcInfo Coverage'
    mime    :
    basis   : 'extension match txt'
    warning : 'match on extension only'
---
filename : 'fixtures/dirs_with_various_encodings/shift_jis/ã½ã£ã·ã‚‹ãƒ¡ã‚¤ãƒ«/shift-jis_encoded_dirs.txt'
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
  - ns      : 'tika'
    id      : 'text/plain'
    format  :
    mime    : 'text/plain'
    basis   : 'extension match txt; text match ASCII'
    warning : 'match on filename and text only; byte/xml signatures for this format did not match'
  - ns      : 'freedesktop.org'
    id      : 'text/plain'
    format  : 'plain text document'
    mime    : 'text/plain'
    basis   : 'extension match txt; text match ASCII'
    warning : 'match on filename and text only; byte/xml signatures for this format did not match'
  - ns      : 'loc'
    id      : 'fdd000284'
    format  : 'ESRI ArcInfo Coverage'
    full    : 'ESRI ArcInfo Coverage'
    mime    :
    basis   : 'extension match txt'
    warning : 'match on extension only'
---
filename : 'fixtures/dirs_with_various_encodings/windows_1252/sÃ¸ster/cp1252_encoded_dirs.txt'
filesize : 98
modified : 2020-06-22T19:38:22+02:00
errors   :
md5      : b2d9653a8be9d9501789cdb55cf3c3f1
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/111'
    format  : 'Plain Text File'
    version :
    mime    : 'text/plain'
    basis   : 'extension match txt; text match ASCII'
    warning :
  - ns      : 'tika'
    id      : 'text/plain'
    format  :
    mime    : 'text/plain'
    basis   : 'extension match txt; text match ASCII'
    warning : 'match on filename and text only; byte/xml signatures for this format did not match'
  - ns      : 'freedesktop.org'
    id      : 'text/plain'
    format  : 'plain text document'
    mime    : 'text/plain'
    basis   : 'extension match txt; text match ASCII'
    warning : 'match on filename and text only; byte/xml signatures for this format did not match'
  - ns      : 'loc'
    id      : 'fdd000284'
    format  : 'ESRI ArcInfo Coverage'
    full    : 'ESRI ArcInfo Coverage'
    mime    :
    basis   : 'extension match txt'
    warning : 'match on extension only'
---
filename : 'fixtures/files_with_various_encodings/emoji/chess-â™•â™–â™—â™˜â™™â™šâ™›â™œâ™â™žâ™Ÿ.txt'
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
  - ns      : 'tika'
    id      : 'text/plain'
    format  :
    mime    : 'text/plain'
    basis   : 'extension match txt; text match ASCII'
    warning : 'match on filename and text only; byte/xml signatures for this format did not match'
  - ns      : 'freedesktop.org'
    id      : 'text/plain'
    format  : 'plain text document'
    mime    : 'text/plain'
    basis   : 'extension match txt; text match ASCII'
    warning : 'match on filename and text only; byte/xml signatures for this format did not match'
  - ns      : 'loc'
    id      : 'fdd000284'
    format  : 'ESRI ArcInfo Coverage'
    full    : 'ESRI ArcInfo Coverage'
    mime    :
    basis   : 'extension match txt'
    warning : 'match on extension only'
---
filename : 'fixtures/files_with_various_encodings/emoji/hearts-â¤ðŸ’–ðŸ’™ðŸ’šðŸ’›ðŸ’œðŸ’.txt'
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
  - ns      : 'tika'
    id      : 'text/plain'
    format  :
    mime    : 'text/plain'
    basis   : 'extension match txt; text match ASCII'
    warning : 'match on filename and text only; byte/xml signatures for this format did not match'
  - ns      : 'freedesktop.org'
    id      : 'text/plain'
    format  : 'plain text document'
    mime    : 'text/plain'
    basis   : 'extension match txt; text match ASCII'
    warning : 'match on filename and text only; byte/xml signatures for this format did not match'
  - ns      : 'loc'
    id      : 'fdd000284'
    format  : 'ESRI ArcInfo Coverage'
    full    : 'ESRI ArcInfo Coverage'
    mime    :
    basis   : 'extension match txt'
    warning : 'match on extension only'
---
filename : 'fixtures/files_with_various_encodings/windows_1252/søster'
filesize : 55
modified : 2020-06-22T19:38:21+02:00
errors   :
md5      : da53eb270f3ce333e91f0d742adb0e24
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/111'
    format  : 'Plain Text File'
    version :
    mime    : 'text/plain'
    basis   : 'text match ASCII'
    warning : 'match on text only; extension mismatch'
  - ns      : 'tika'
    id      : 'text/plain'
    format  :
    mime    : 'text/plain'
    basis   : 'text match ASCII'
    warning : 'match on text only; byte/xml signatures for this format did not match; filename mismatch'
  - ns      : 'freedesktop.org'
    id      : 'text/plain'
    format  : 'plain text document'
    mime    : 'text/plain'
    basis   : 'text match ASCII'
    warning : 'match on text only; byte/xml signatures for this format did not match; filename mismatch'
  - ns      : 'loc'
    id      : 'UNKNOWN'
    format  :
    full    :
    mime    :
    basis   :
    warning : 'no match'
---
filename : 'fixtures/opf-format-corpus/video/Quicktime/animation.mov'
filesize : 1020209
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 7c845af9f5aa44be9590067758760a8c
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/384'
    format  : 'Quicktime'
    version :
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 8 (signature 4/8)'
    warning :
  - ns      : 'tika'
    id      : 'video/quicktime'
    format  : 'QuickTime Video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 4 (signature 6/7)'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'video/quicktime'
    format  : 'QuickTime video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 6 (signature 4/4)'
    warning :
  - ns      : 'loc'
    id      : 'fdd000254'
    format  : 'AMR, Adaptive Multi-Rate Speech Codec'
    full    : 'AMR, Adaptive Multi-Rate Speech Codec'
    mime    : 'audio/AMR'
    basis   : 'byte match at 0, 3 (signature 2/2)'
    warning : 'extension mismatch'
---
filename : 'fixtures/opf-format-corpus/video/Quicktime/apple-intermediate-codec.mov'
filesize : 319539
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 627fba96fbcaaa50d02f0d33cc3fb361
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/384'
    format  : 'Quicktime'
    version :
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 8 (signature 4/8)'
    warning :
  - ns      : 'tika'
    id      : 'video/quicktime'
    format  : 'QuickTime Video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 4 (signature 6/7)'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'video/quicktime'
    format  : 'QuickTime video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 6 (signature 4/4)'
    warning :
  - ns      : 'loc'
    id      : 'fdd000254'
    format  : 'AMR, Adaptive Multi-Rate Speech Codec'
    full    : 'AMR, Adaptive Multi-Rate Speech Codec'
    mime    : 'audio/AMR'
    basis   : 'byte match at 0, 3 (signature 2/2)'
    warning : 'extension mismatch'
---
filename : 'fixtures/opf-format-corpus/video/Quicktime/apple-prores-422.mov'
filesize : 564775
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 44e2f4eee4b062179db7d7eb694fb453
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/384'
    format  : 'Quicktime'
    version :
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 8 (signature 4/8)'
    warning :
  - ns      : 'tika'
    id      : 'video/quicktime'
    format  : 'QuickTime Video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 4 (signature 6/7)'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'video/quicktime'
    format  : 'QuickTime video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 6 (signature 4/4)'
    warning :
  - ns      : 'loc'
    id      : 'fdd000254'
    format  : 'AMR, Adaptive Multi-Rate Speech Codec'
    full    : 'AMR, Adaptive Multi-Rate Speech Codec'
    mime    : 'audio/AMR'
    basis   : 'byte match at 0, 3 (signature 2/2)'
    warning : 'extension mismatch'
---
filename : 'fixtures/opf-format-corpus/video/Quicktime/dv-dvchd-ntsc-interlaced.mov'
filesize : 3001365
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 38d98389ff914344fa1074fc023c4494
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/384'
    format  : 'Quicktime'
    version :
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 8 (signature 4/8)'
    warning :
  - ns      : 'tika'
    id      : 'video/quicktime'
    format  : 'QuickTime Video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 4 (signature 6/7)'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'video/quicktime'
    format  : 'QuickTime video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 6 (signature 4/4)'
    warning :
  - ns      : 'loc'
    id      : 'fdd000254'
    format  : 'AMR, Adaptive Multi-Rate Speech Codec'
    full    : 'AMR, Adaptive Multi-Rate Speech Codec'
    mime    : 'audio/AMR'
    basis   : 'byte match at 0, 3 (signature 2/2)'
    warning : 'extension mismatch'
---
filename : 'fixtures/opf-format-corpus/video/Quicktime/dv-dvchd-ntsc-progressive.mov'
filesize : 3001365
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 7123e7a33c9026324b553a434efadff3
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/384'
    format  : 'Quicktime'
    version :
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 8 (signature 4/8)'
    warning :
  - ns      : 'tika'
    id      : 'video/quicktime'
    format  : 'QuickTime Video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 4 (signature 6/7)'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'video/quicktime'
    format  : 'QuickTime video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 6 (signature 4/4)'
    warning :
  - ns      : 'loc'
    id      : 'fdd000254'
    format  : 'AMR, Adaptive Multi-Rate Speech Codec'
    full    : 'AMR, Adaptive Multi-Rate Speech Codec'
    mime    : 'audio/AMR'
    basis   : 'byte match at 0, 3 (signature 2/2)'
    warning : 'extension mismatch'
---
filename : 'fixtures/opf-format-corpus/video/Quicktime/dv-pal-interlaced.mov'
filesize : 3601749
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 042cc2c0db16b60eb6f7eddd3dc118ac
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/384'
    format  : 'Quicktime'
    version :
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 8 (signature 4/8)'
    warning :
  - ns      : 'tika'
    id      : 'video/quicktime'
    format  : 'QuickTime Video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 4 (signature 6/7)'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'video/quicktime'
    format  : 'QuickTime video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 6 (signature 4/4)'
    warning :
  - ns      : 'loc'
    id      : 'fdd000254'
    format  : 'AMR, Adaptive Multi-Rate Speech Codec'
    full    : 'AMR, Adaptive Multi-Rate Speech Codec'
    mime    : 'audio/AMR'
    basis   : 'byte match at 0, 3 (signature 2/2)'
    warning : 'extension mismatch'
---
filename : 'fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-1080i50.mov'
filesize : 14401365
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 23279d7284c946767602072fc2f48a94
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/384'
    format  : 'Quicktime'
    version :
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 8 (signature 4/8)'
    warning :
  - ns      : 'tika'
    id      : 'video/quicktime'
    format  : 'QuickTime Video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 4 (signature 6/7)'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'video/quicktime'
    format  : 'QuickTime video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 6 (signature 4/4)'
    warning :
  - ns      : 'loc'
    id      : 'fdd000254'
    format  : 'AMR, Adaptive Multi-Rate Speech Codec'
    full    : 'AMR, Adaptive Multi-Rate Speech Codec'
    mime    : 'audio/AMR'
    basis   : 'byte match at 0, 3 (signature 2/2)'
    warning : 'extension mismatch'
---
filename : 'fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-1080i60.mov'
filesize : 12001365
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 033dfe66d1fa70a827007bed284d703b
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/384'
    format  : 'Quicktime'
    version :
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 8 (signature 4/8)'
    warning :
  - ns      : 'tika'
    id      : 'video/quicktime'
    format  : 'QuickTime Video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 4 (signature 6/7)'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'video/quicktime'
    format  : 'QuickTime video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 6 (signature 4/4)'
    warning :
  - ns      : 'loc'
    id      : 'fdd000254'
    format  : 'AMR, Adaptive Multi-Rate Speech Codec'
    full    : 'AMR, Adaptive Multi-Rate Speech Codec'
    mime    : 'audio/AMR'
    basis   : 'byte match at 0, 3 (signature 2/2)'
    warning : 'extension mismatch'
---
filename : 'fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-1080p25.mov'
filesize : 14401365
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : a461c14eaf56c34477d646b0c3dc27ad
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/384'
    format  : 'Quicktime'
    version :
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 8 (signature 4/8)'
    warning :
  - ns      : 'tika'
    id      : 'video/quicktime'
    format  : 'QuickTime Video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 4 (signature 6/7)'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'video/quicktime'
    format  : 'QuickTime video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 6 (signature 4/4)'
    warning :
  - ns      : 'loc'
    id      : 'fdd000254'
    format  : 'AMR, Adaptive Multi-Rate Speech Codec'
    full    : 'AMR, Adaptive Multi-Rate Speech Codec'
    mime    : 'audio/AMR'
    basis   : 'byte match at 0, 3 (signature 2/2)'
    warning : 'extension mismatch'
---
filename : 'fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-1080p30.mov'
filesize : 12001365
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 0812184da1c85eae2f27bf5763277f3f
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/384'
    format  : 'Quicktime'
    version :
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 8 (signature 4/8)'
    warning :
  - ns      : 'tika'
    id      : 'video/quicktime'
    format  : 'QuickTime Video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 4 (signature 6/7)'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'video/quicktime'
    format  : 'QuickTime video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 6 (signature 4/4)'
    warning :
  - ns      : 'loc'
    id      : 'fdd000254'
    format  : 'AMR, Adaptive Multi-Rate Speech Codec'
    full    : 'AMR, Adaptive Multi-Rate Speech Codec'
    mime    : 'audio/AMR'
    basis   : 'byte match at 0, 3 (signature 2/2)'
    warning : 'extension mismatch'
---
filename : 'fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-720p50.mov'
filesize : 7201357
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : a02f51b2d4340d3a650822b980010e41
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/384'
    format  : 'Quicktime'
    version :
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 8 (signature 4/8)'
    warning :
  - ns      : 'tika'
    id      : 'video/quicktime'
    format  : 'QuickTime Video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 4 (signature 6/7)'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'video/quicktime'
    format  : 'QuickTime video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 6 (signature 4/4)'
    warning :
  - ns      : 'loc'
    id      : 'fdd000254'
    format  : 'AMR, Adaptive Multi-Rate Speech Codec'
    full    : 'AMR, Adaptive Multi-Rate Speech Codec'
    mime    : 'audio/AMR'
    basis   : 'byte match at 0, 3 (signature 2/2)'
    warning : 'extension mismatch'
---
filename : 'fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-720p60.mov'
filesize : 6001485
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 75aeb7ffd2f1bf156f3fc355e589dae5
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/384'
    format  : 'Quicktime'
    version :
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 8 (signature 4/8)'
    warning :
  - ns      : 'tika'
    id      : 'video/quicktime'
    format  : 'QuickTime Video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 4 (signature 6/7)'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'video/quicktime'
    format  : 'QuickTime video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 6 (signature 4/4)'
    warning :
  - ns      : 'loc'
    id      : 'fdd000254'
    format  : 'AMR, Adaptive Multi-Rate Speech Codec'
    full    : 'AMR, Adaptive Multi-Rate Speech Codec'
    mime    : 'audio/AMR'
    basis   : 'byte match at 0, 3 (signature 2/2)'
    warning : 'extension mismatch'
---
filename : 'fixtures/opf-format-corpus/video/Quicktime/dvcpro-pal-interlaced.mov'
filesize : 3601749
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : a5a350848af8d4056426aecc0077827c
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/384'
    format  : 'Quicktime'
    version :
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 8 (signature 4/8)'
    warning :
  - ns      : 'tika'
    id      : 'video/quicktime'
    format  : 'QuickTime Video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 4 (signature 6/7)'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'video/quicktime'
    format  : 'QuickTime video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 6 (signature 4/4)'
    warning :
  - ns      : 'loc'
    id      : 'fdd000254'
    format  : 'AMR, Adaptive Multi-Rate Speech Codec'
    full    : 'AMR, Adaptive Multi-Rate Speech Codec'
    mime    : 'audio/AMR'
    basis   : 'byte match at 0, 3 (signature 2/2)'
    warning : 'extension mismatch'
---
filename : 'fixtures/opf-format-corpus/video/Quicktime/dvcpro-pal-progressive.mov'
filesize : 3601749
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : a005a1ccd6997d0fffce6e9b161c4324
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/384'
    format  : 'Quicktime'
    version :
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 8 (signature 4/8)'
    warning :
  - ns      : 'tika'
    id      : 'video/quicktime'
    format  : 'QuickTime Video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 4 (signature 6/7)'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'video/quicktime'
    format  : 'QuickTime video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 6 (signature 4/4)'
    warning :
  - ns      : 'loc'
    id      : 'fdd000254'
    format  : 'AMR, Adaptive Multi-Rate Speech Codec'
    full    : 'AMR, Adaptive Multi-Rate Speech Codec'
    mime    : 'audio/AMR'
    basis   : 'byte match at 0, 3 (signature 2/2)'
    warning : 'extension mismatch'
---
filename : 'fixtures/opf-format-corpus/video/Quicktime/dvcpro50-pal-interlaced.mov'
filesize : 7203433
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : a4f33762d95651446e84c32e181e19c2
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/384'
    format  : 'Quicktime'
    version :
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 8 (signature 4/8)'
    warning :
  - ns      : 'tika'
    id      : 'video/quicktime'
    format  : 'QuickTime Video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 4 (signature 6/7)'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'video/quicktime'
    format  : 'QuickTime video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 6 (signature 4/4)'
    warning :
  - ns      : 'loc'
    id      : 'fdd000254'
    format  : 'AMR, Adaptive Multi-Rate Speech Codec'
    full    : 'AMR, Adaptive Multi-Rate Speech Codec'
    mime    : 'audio/AMR'
    basis   : 'byte match at 0, 3 (signature 2/2)'
    warning : 'extension mismatch'
---
filename : 'fixtures/opf-format-corpus/video/Quicktime/dvcpro50-pal-progressive.mov'
filesize : 7203433
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 6e26144f9b0580f884114d4da7a43e74
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/384'
    format  : 'Quicktime'
    version :
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 8 (signature 4/8)'
    warning :
  - ns      : 'tika'
    id      : 'video/quicktime'
    format  : 'QuickTime Video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 4 (signature 6/7)'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'video/quicktime'
    format  : 'QuickTime video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 6 (signature 4/4)'
    warning :
  - ns      : 'loc'
    id      : 'fdd000254'
    format  : 'AMR, Adaptive Multi-Rate Speech Codec'
    full    : 'AMR, Adaptive Multi-Rate Speech Codec'
    mime    : 'audio/AMR'
    basis   : 'byte match at 0, 3 (signature 2/2)'
    warning : 'extension mismatch'
---
filename : 'fixtures/opf-format-corpus/video/Quicktime/jpeg2000.mov'
filesize : 383905
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : bfff74cd3b020f281512829cca291063
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/384'
    format  : 'Quicktime'
    version :
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 8 (signature 4/8)'
    warning :
  - ns      : 'tika'
    id      : 'video/quicktime'
    format  : 'QuickTime Video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 4 (signature 6/7)'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'video/quicktime'
    format  : 'QuickTime video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 6 (signature 4/4)'
    warning :
  - ns      : 'loc'
    id      : 'fdd000254'
    format  : 'AMR, Adaptive Multi-Rate Speech Codec'
    full    : 'AMR, Adaptive Multi-Rate Speech Codec'
    mime    : 'audio/AMR'
    basis   : 'byte match at 0, 3 (signature 2/2)'
    warning : 'extension mismatch'
---
filename : 'fixtures/opf-format-corpus/video/Quicktime/photo-jpeg.mov'
filesize : 575929
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 0a67f830ab31a6d0a7b213e2273593a6
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/384'
    format  : 'Quicktime'
    version :
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 8 (signature 4/8)'
    warning :
  - ns      : 'tika'
    id      : 'video/quicktime'
    format  : 'QuickTime Video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 4 (signature 6/7)'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'video/quicktime'
    format  : 'QuickTime video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 6 (signature 4/4)'
    warning :
  - ns      : 'loc'
    id      : 'fdd000254'
    format  : 'AMR, Adaptive Multi-Rate Speech Codec'
    full    : 'AMR, Adaptive Multi-Rate Speech Codec'
    mime    : 'audio/AMR'
    basis   : 'byte match at 0, 3 (signature 2/2)'
    warning : 'extension mismatch'
---
filename : 'fixtures/opf-format-corpus/video/Quicktime/xdcam-hd-1080p25.mov'
filesize : 694863
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : ccf4aebd86a2d81ae9ad2544e90abe52
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/384'
    format  : 'Quicktime'
    version :
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 8 (signature 4/8)'
    warning :
  - ns      : 'tika'
    id      : 'video/quicktime'
    format  : 'QuickTime Video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 4 (signature 6/7)'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'video/quicktime'
    format  : 'QuickTime video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 6 (signature 4/4)'
    warning :
  - ns      : 'loc'
    id      : 'fdd000254'
    format  : 'AMR, Adaptive Multi-Rate Speech Codec'
    full    : 'AMR, Adaptive Multi-Rate Speech Codec'
    mime    : 'audio/AMR'
    basis   : 'byte match at 0, 3 (signature 2/2)'
    warning : 'extension mismatch'
---
filename : 'fixtures/opf-format-corpus/video/Quicktime/xdcam-hd-1080p30.mov'
filesize : 583993
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : a1ea1b20fca6e65e48454c7793f4be2a
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/384'
    format  : 'Quicktime'
    version :
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 8 (signature 4/8)'
    warning :
  - ns      : 'tika'
    id      : 'video/quicktime'
    format  : 'QuickTime Video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 4 (signature 6/7)'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'video/quicktime'
    format  : 'QuickTime video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 6 (signature 4/4)'
    warning :
  - ns      : 'loc'
    id      : 'fdd000254'
    format  : 'AMR, Adaptive Multi-Rate Speech Codec'
    full    : 'AMR, Adaptive Multi-Rate Speech Codec'
    mime    : 'audio/AMR'
    basis   : 'byte match at 0, 3 (signature 2/2)'
    warning : 'extension mismatch'
---
filename : 'fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-1080i50.mov'
filesize : 6251203
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 5281f430744681ce4d5667aec30021df
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/384'
    format  : 'Quicktime'
    version :
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 8 (signature 4/8)'
    warning :
  - ns      : 'tika'
    id      : 'video/quicktime'
    format  : 'QuickTime Video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 4 (signature 6/7)'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'video/quicktime'
    format  : 'QuickTime video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 6 (signature 4/4)'
    warning :
  - ns      : 'loc'
    id      : 'fdd000254'
    format  : 'AMR, Adaptive Multi-Rate Speech Codec'
    full    : 'AMR, Adaptive Multi-Rate Speech Codec'
    mime    : 'audio/AMR'
    basis   : 'byte match at 0, 3 (signature 2/2)'
    warning : 'extension mismatch'
---
filename : 'fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-1080i60.mov'
filesize : 5215055
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 7b8c215c05e46eaa68b1477cd0ca0082
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/384'
    format  : 'Quicktime'
    version :
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 8 (signature 4/8)'
    warning :
  - ns      : 'tika'
    id      : 'video/quicktime'
    format  : 'QuickTime Video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 4 (signature 6/7)'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'video/quicktime'
    format  : 'QuickTime video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 6 (signature 4/4)'
    warning :
  - ns      : 'loc'
    id      : 'fdd000254'
    format  : 'AMR, Adaptive Multi-Rate Speech Codec'
    full    : 'AMR, Adaptive Multi-Rate Speech Codec'
    mime    : 'audio/AMR'
    basis   : 'byte match at 0, 3 (signature 2/2)'
    warning : 'extension mismatch'
---
filename : 'fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-720p30.mov'
filesize : 5215055
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : a9ef25f92febe9f2cd3b895fe38818af
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/384'
    format  : 'Quicktime'
    version :
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 8 (signature 4/8)'
    warning :
  - ns      : 'tika'
    id      : 'video/quicktime'
    format  : 'QuickTime Video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 4 (signature 6/7)'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'video/quicktime'
    format  : 'QuickTime video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 6 (signature 4/4)'
    warning :
  - ns      : 'loc'
    id      : 'fdd000254'
    format  : 'AMR, Adaptive Multi-Rate Speech Codec'
    full    : 'AMR, Adaptive Multi-Rate Speech Codec'
    mime    : 'audio/AMR'
    basis   : 'byte match at 0, 3 (signature 2/2)'
    warning : 'extension mismatch'
---
filename : 'fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-720p50.mov'
filesize : 3125967
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : b4c6a638f5463139c80bdd63a5aedf53
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/384'
    format  : 'Quicktime'
    version :
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 8 (signature 4/8)'
    warning :
  - ns      : 'tika'
    id      : 'video/quicktime'
    format  : 'QuickTime Video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 4 (signature 6/7)'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'video/quicktime'
    format  : 'QuickTime video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 6 (signature 4/4)'
    warning :
  - ns      : 'loc'
    id      : 'fdd000254'
    format  : 'AMR, Adaptive Multi-Rate Speech Codec'
    full    : 'AMR, Adaptive Multi-Rate Speech Codec'
    mime    : 'audio/AMR'
    basis   : 'byte match at 0, 3 (signature 2/2)'
    warning : 'extension mismatch'
---
filename : 'fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-720p60.mov'
filesize : 2607739
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 2251ba9a965f591e34ca061d4d707ff4
matches  :
  - ns      : 'pronom'
    id      : 'x-fmt/384'
    format  : 'Quicktime'
    version :
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 8 (signature 4/8)'
    warning :
  - ns      : 'tika'
    id      : 'video/quicktime'
    format  : 'QuickTime Video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 4 (signature 6/7)'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'video/quicktime'
    format  : 'QuickTime video'
    mime    : 'video/quicktime'
    basis   : 'extension match mov; byte match at 4, 6 (signature 4/4)'
    warning :
  - ns      : 'loc'
    id      : 'fdd000254'
    format  : 'AMR, Adaptive Multi-Rate Speech Codec'
    full    : 'AMR, Adaptive Multi-Rate Speech Codec'
    mime    : 'audio/AMR'
    basis   : 'byte match at 0, 3 (signature 2/2)'
    warning : 'extension mismatch'
---
filename : 'fixtures/possible-multiples/fmt-140-signature-id-207.odb'
filesize : 105
modified : 2020-01-25T03:00:27+01:00
errors   : 'zip: not a valid zip file'
md5      : 434240eb119cf0564eb3ab13b7b8cf3f
matches  :
  - ns      : 'pronom'
    id      : 'UNKNOWN'
    format  :
    version :
    mime    :
    basis   :
    warning : 'no match; possibilities based on extension are fmt/140, fmt/424, fmt/444'
  - ns      : 'tika'
    id      : 'application/zip'
    format  : 'Compressed Archive File'
    mime    : 'application/zip'
    basis   : 'byte match at 0, 4 (signature 1/3)'
    warning : 'filename mismatch'
  - ns      : 'freedesktop.org'
    id      : 'application/vnd.oasis.opendocument.database'
    format  : 'ODB database'
    mime    : 'application/vnd.oasis.opendocument.database'
    basis   : 'extension match odb; byte match at 0, 4 (signature 2/2)'
    warning :
  - ns      : 'loc'
    id      : 'fdd000514'
    format  : 'Microsoft XML Paper Specification, (XPS)'
    full    : 'Microsoft XML Paper Specification, (XPS)'
    mime    : 'application/vnd.ms-xpsdocument'
    basis   : 'byte match at 0, 4'
    warning : 'extension mismatch'
---
filename : 'fixtures/possible-multiples/fmt-641-signature-id-970.erf'
filesize : 348
modified : 2020-01-25T03:00:30+01:00
errors   :
md5      : 4425a5f4b078e9b716969a856c1015f6
matches  :
  - ns      : 'pronom'
    id      : 'fmt/641'
    format  : 'Epson Raw Image Format'
    version :
    mime    :
    basis   : 'extension match erf; byte match at 0, 348'
    warning :
  - ns      : 'tika'
    id      : 'image/tiff'
    format  : 'Tagged Image File Format'
    mime    : 'image/tiff'
    basis   : 'byte match at 0, 4 (signature 1/3)'
    warning : 'filename mismatch'
  - ns      : 'freedesktop.org'
    id      : 'image/tiff'
    format  : 'TIFF image'
    mime    : 'image/tiff'
    basis   : 'byte match at 0, 4 (signature 1/2)'
    warning : 'filename mismatch'
  - ns      : 'loc'
    id      : 'fdd000022'
    format  : 'TIFF, Revision 6.0'
    full    : 'TIFF (Tagged Image File Format), Revision 6.0'
    mime    : 'image/tiff'
    basis   : 'byte match at 0, 4 (signature 3/5)'
    warning : 'extension mismatch'
---
filename : 'fixtures/synthetically_unknown_formats/README.md'
filesize : 1257
modified : 2020-01-15T20:17:02+01:00
errors   :
md5      : cdde5e89dcb9b17e11780acd06bae840
matches  :
  - ns      : 'pronom'
    id      : 'fmt/1149'
    format  : 'Markdown'
    version :
    mime    : 'text/markdown'
    basis   : 'extension match md'
    warning : 'match on extension only'
  - ns      : 'tika'
    id      : 'text/x-web-markdown'
    format  : 'Markdown source code'
    mime    : 'text/x-web-markdown'
    basis   : 'extension match md; text match ASCII'
    warning : 'match on filename and text only'
  - ns      : 'freedesktop.org'
    id      : 'text/markdown'
    format  : 'Markdown document'
    mime    : 'text/markdown'
    basis   : 'extension match md; text match ASCII'
    warning : 'match on filename and text only'
  - ns      : 'loc'
    id      : 'UNKNOWN'
    format  :
    full    :
    mime    :
    basis   :
    warning : 'no match'
---
filename : 'fixtures/synthetically_unknown_formats/baseball.format'
filesize : 52
modified : 2020-01-15T20:17:02+01:00
errors   :
md5      : 1a6c6441a82f19ffcb604e02a57d0bf4
matches  :
  - ns      : 'pronom'
    id      : 'UNKNOWN'
    format  :
    version :
    mime    :
    basis   :
    warning : 'no match'
  - ns      : 'tika'
    id      : 'UNKNOWN'
    format  :
    mime    : 'UNKNOWN'
    basis   :
    warning : 'no match'
  - ns      : 'freedesktop.org'
    id      : 'UNKNOWN'
    format  :
    mime    : 'UNKNOWN'
    basis   :
    warning : 'no match'
  - ns      : 'loc'
    id      : 'UNKNOWN'
    format  :
    full    :
    mime    :
    basis   :
    warning : 'no match'
---
filename : 'fixtures/synthetically_unknown_formats/caboose.format'
filesize : 52
modified : 2020-01-15T20:17:02+01:00
errors   :
md5      : 8757e8a7cea74eab1510d84f89f78bed
matches  :
  - ns      : 'pronom'
    id      : 'UNKNOWN'
    format  :
    version :
    mime    :
    basis   :
    warning : 'no match'
  - ns      : 'tika'
    id      : 'UNKNOWN'
    format  :
    mime    : 'UNKNOWN'
    basis   :
    warning : 'no match'
  - ns      : 'freedesktop.org'
    id      : 'UNKNOWN'
    format  :
    mime    : 'UNKNOWN'
    basis   :
    warning : 'no match'
  - ns      : 'loc'
    id      : 'UNKNOWN'
    format  :
    full    :
    mime    :
    basis   :
    warning : 'no match'
---
filename : 'fixtures/synthetically_unknown_formats/cassette.format'
filesize : 52
modified : 2020-01-15T20:17:02+01:00
errors   :
md5      : d81cfa5d4fd884ee6f5631229bbf4a3e
matches  :
  - ns      : 'pronom'
    id      : 'UNKNOWN'
    format  :
    version :
    mime    :
    basis   :
    warning : 'no match'
  - ns      : 'tika'
    id      : 'UNKNOWN'
    format  :
    mime    : 'UNKNOWN'
    basis   :
    warning : 'no match'
  - ns      : 'freedesktop.org'
    id      : 'UNKNOWN'
    format  :
    mime    : 'UNKNOWN'
    basis   :
    warning : 'no match'
  - ns      : 'loc'
    id      : 'UNKNOWN'
    format  :
    full    :
    mime    :
    basis   :
    warning : 'no match'
---
filename : 'fixtures/synthetically_unknown_formats/debateable.format'
filesize : 52
modified : 2020-01-15T20:17:02+01:00
errors   :
md5      : 4c1a6c57613aaf221e4d5ea9b4920c6d
matches  :
  - ns      : 'pronom'
    id      : 'UNKNOWN'
    format  :
    version :
    mime    :
    basis   :
    warning : 'no match'
  - ns      : 'tika'
    id      : 'UNKNOWN'
    format  :
    mime    : 'UNKNOWN'
    basis   :
    warning : 'no match'
  - ns      : 'freedesktop.org'
    id      : 'UNKNOWN'
    format  :
    mime    : 'UNKNOWN'
    basis   :
    warning : 'no match'
  - ns      : 'loc'
    id      : 'UNKNOWN'
    format  :
    full    :
    mime    :
    basis   :
    warning : 'no match'
---
filename : 'fixtures/synthetically_unknown_formats/looseleaf.format'
filesize : 52
modified : 2020-01-15T20:17:02+01:00
errors   :
md5      : 34d8c18805e54a3cdffd6d4f018ee9d4
matches  :
  - ns      : 'pronom'
    id      : 'UNKNOWN'
    format  :
    version :
    mime    :
    basis   :
    warning : 'no match'
  - ns      : 'tika'
    id      : 'UNKNOWN'
    format  :
    mime    : 'UNKNOWN'
    basis   :
    warning : 'no match'
  - ns      : 'freedesktop.org'
    id      : 'UNKNOWN'
    format  :
    mime    : 'UNKNOWN'
    basis   :
    warning : 'no match'
  - ns      : 'loc'
    id      : 'UNKNOWN'
    format  :
    full    :
    mime    :
    basis   :
    warning : 'no match'
"""

if sys.version_info[0] == 3:
    PY3 = True
else:
    PY3 = False


def test_run_droid_analysis(tmp_path):
    """Test analysis output for DROID."""

    dir_ = tmp_path
    droid_csv = dir_ / "droid_💜_test.csv"
    droid_csv.write_text(DROID_CSV.strip())

    # Analysis from CSV will currently read the results from the CSV
    # above and output an on-disk sqlite database at tmp_path. This
    # works perfectly for us. In future, if we need to create an
    # in-memory database for any reason we can but it will take some
    # further refactoring.
    res = analysis_from_csv(str(droid_csv), True)

    assert res.analysis_results.namespacecount == 1

    assert res.namespacedata[0][0] == 1
    assert res.namespacedata[0][1] == "pronom"
    assert res.namespacedata[0][2].endswith("droid_💜_test.csv")

    assert res.analysis_results.filename.endswith("droid_💜_test")
    assert res.analysis_results.tooltype == "droid"

    assert res.analysis_results.denylist is None
    assert res.analysis_results.denylist_filenames == []
    assert res.analysis_results.denylist_directories == []
    assert res.analysis_results.denylist_ids == []
    assert res.analysis_results.denylist_exts == []

    '''
    assert res.analysis_results.collectionsize == 123914951
    assert res.analysis_results.filecount == 56
    assert res.analysis_results.directoryCount == 24
    assert res.analysis_results.uniqueFileNames == 54
    assert res.analysis_results.uniqueDirectoryNames == 24
    assert res.analysis_results.identifiedfilecount == 40
    assert res.analysis_results.multipleidentificationcount == 2
    assert res.analysis_results.unidentifiedfilecount == 16
    assert res.analysis_results.distinctSignaturePuidcount == 18
    assert res.analysis_results.extensionIDOnlyCount == 10
    assert res.analysis_results.distinctextensioncount == 18
    assert res.analysis_results.zeroidcount == 6
    '''

    assert res.analysis_results.containercount == 2

    # TODO, is this count something useful?
    assert res.analysis_results.filesincontainercount == 0

    '''
    assert res.analysis_results.hashused is True
    assert res.analysis_results.totalHASHduplicates == 6
    assert len(res.analysis_results.duplicateHASHlisting) == 3
    assert res.analysis_results.duplicateHASHlisting == [
        {
            "checksum": "0c391e403302385e9d227733fc477bf440f978d2",
            "count": 2,
            "examples": [
                "/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437/año/cp437_encoded_dirs.txt",
                "/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437/café/cp437_encoded_dirs.txt",
            ],
        },
        {
            "checksum": "1766219eb64113604a1fe2c003b10c8258bb1cbb",
            "count": 2,
            "examples": [
                "/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/emoji/chess-♕♖♗♘♙♚♛♜♝♞♟.txt",
                "/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/emoji/hearts-❤💖💙💚💛💜💝.txt",
            ],
        },
        {
            "checksum": "d0e093259ce05cde2b326e418ac547359b91ee5f",
            "count": 2,
            "examples": [
                "/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji/chess-♕♖♗♘♙♚♛♜♝♞♟/utf-8_encoded_dirs.txt",
                "/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji/hearts-❤💖💙💚💛💜💝/utf-8_encoded_dirs.txt",
            ],
        },
    ]
    '''

def test_run_siegfried_analysis(tmp_path):
    """Test analysis output for Siegfried."""

    dir_ = tmp_path
    sf_yaml = dir_ / "sf_💜_test.yaml"
    sf_yaml.write_text(SIEGFRIED_YAML.strip())

    # Analysis from CSV will currently read the results from the CSV
    # above and output an on-disk sqlite database at tmp_path. This
    # works perfectly for us. In future, if we need to create an
    # in-memory database for any reason we can but it will take some
    # further refactoring.
    res = analysis_from_csv(str(sf_yaml), True)

    assert res.namespacedata[0] == (
        1,
        "pronom",
        "DROID_SignatureFile_V97.xml; container-signature-20201001.xml",
    )
    assert res.namespacedata[1] == (2, "tika", "tika-mimetypes.xml (1.24, 2020-04-17)")
    assert res.namespacedata[2] == (
        3,
        "freedesktop.org",
        "freedesktop.org.xml (2.0, 2020-06-05)",
    )
    assert res.namespacedata[3] == (
        4,
        "loc",
        "fddXML.zip (2020-09-02, DROID_SignatureFile_V97.xml, container-signature-20201001.xml)",
    )

    # Siegfried only instance results.
    assert res.priority_ns_id == 4
    assert res.pronom_ns_id == 4

    # Anticipating PRONOM so lets confirm our PRONOM index and priority
    # IDs are correct.
    assert res.priority_ns_id == res.pronom_ns_id

    assert res.tika_ns_id == 2
    assert res.freedesktop_ns_id == 3

    assert res.analysis_results.filename.endswith("sf_💜_test")
    assert res.analysis_results.tooltype == "siegfried: 1.9.1"

    assert res.analysis_results.denylist is None
    assert res.analysis_results.denylist_filenames == []
    assert res.analysis_results.denylist_directories == []
    assert res.analysis_results.denylist_ids == []
    assert res.analysis_results.denylist_exts == []

    assert res.analysis_results.collectionsize == 123914951
    assert res.analysis_results.filecount == 56
    assert res.analysis_results.directoryCount == 14
    assert res.analysis_results.uniqueFileNames == 54
    assert res.analysis_results.uniqueDirectoryNames == 13
    assert res.analysis_results.identifiedfilecount == 47
    assert res.analysis_results.multipleidentificationcount == 0
    assert res.analysis_results.unidentifiedfilecount == 9
    assert res.analysis_results.distinctSignaturePuidcount == 15
    assert res.analysis_results.extensionIDOnlyCount == 0
    assert res.analysis_results.distinctextensioncount == 18
    assert res.analysis_results.zeroidcount == 5
    assert res.analysis_results.containercount == 5

    # TODO, is this count something useful?
    assert res.analysis_results.filesincontainercount == 5

    '''
    assert res.analysis_results.hashused is True
    assert res.analysis_results.totalHASHduplicates == 6
    assert len(res.analysis_results.duplicateHASHlisting) == 3
    assert res.analysis_results.duplicateHASHlisting == [
        {
            "checksum": "0653e4959fa11f1ffce974b092efdd00",
            "count": 2,
            "examples": [
                "fixtures/files_with_various_encodings/emoji/chess-♕♖♗♘♙♚♛♜♝♞♟.txt",
                "fixtures/files_with_various_encodings/emoji/hearts-❤💖💙💚💛💜💝.txt",
            ],
        },
        {
            "checksum": "2e58bf86585ae31fcd7112f1beee358b",
            "count": 2,
            "examples": [
                "fixtures/dirs_with_various_encodings/emoji/chess-♕♖♗♘♙♚♛♜♝♞♟/utf-8_encoded_dirs.txt",
                "fixtures/dirs_with_various_encodings/emoji/hearts-❤💖💙💚💛💜💝/utf-8_encoded_dirs.txt",
            ],
        },
        {
            "checksum": "a2530a3d32134654f0bef01cf252afd7",
            "count": 2,
            "examples": [
                "fixtures/dirs_with_various_encodings/cp437/año/cp437_encoded_dirs.txt",
                "fixtures/dirs_with_various_encodings/cp437/café/cp437_encoded_dirs.txt",
            ],
        },
    ]
    '''
