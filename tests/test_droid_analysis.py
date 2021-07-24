# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

from demystify import analysis_from_csv

DROID_CSV = u""""ID","PARENT_ID","URI","FILE_PATH","NAME","METHOD","STATUS","SIZE","TYPE","EXT","LAST_MODIFIED","EXTENSION_MISMATCH","SHA1_HASH","FORMAT_COUNT","PUID","MIME_TYPE","FORMAT_NAME","FORMAT_VERSION"
"2","0","file:////10.1.4.222/gda/archives-sample-files/opf-format-corpus/format-corpus/","\\10.1.4.222\\gda\archives-sample-files\\opf-format-corpus\format-corpus","🖤format-corpus",,"Done","","Folder",,"2014-02-28T15:49:11","false",,"",,"","",""
"3","2","file:////10.1.4.222/gda/archives-sample-files/opf-format-corpus/format-corpus/video/","\\10.1.4.222\\gda\archives-sample-files\\opf-format-corpus\format-corpus\video","video",,"Done","","Folder",,"2014-02-28T15:48:47","false",,"",,"","",""
"4","3","file:////10.1.4.222/gda/archives-sample-files/opf-format-corpus/format-corpus/video/Quicktime/","\\10.1.4.222\\gda\archives-sample-files\\opf-format-corpus\format-corpus\video\\Quicktime","Quicktime",,"Done","","Folder",,"2014-02-28T15:48:59","false",,"",,"","",""
"5","4","file:////10.1.4.222/gda/archives-sample-files/opf-format-corpus/format-corpus/video/Quicktime/apple-intermediate-codec.mov","\\10.1.4.222\\gda\archives-sample-files\\opf-format-corpus\format-corpus\video\\Quicktime\apple-intermediate-codec.mov","apple-intermediate-codec.mov","Signature","Done","319539","File","mov","2014-02-18T16:58:16","false","d097cf36467373f52b974542d48bec134279fa3f","1","x-fmt/384","video/quicktime","Quicktime",""
"6","4","file:////10.1.4.222/gda/archives-sample-files/opf-format-corpus/format-corpus/video/Quicktime/animation.mov","\\10.1.4.222\\gda\archives-sample-files\\opf-format-corpus\format-corpus\video\\Quicktime\animation.mov","animation.mov","Signature","Done","1020209","File","mov","2014-02-18T16:58:16","false","edb5226b963f449ce58054809149cb812bdf8c0a","1","x-fmt/384","video/quicktime","Quicktime",""
"7","4","file:////10.1.4.222/gda/archives-sample-files/opf-format-corpus/format-corpus/video/Quicktime/apple-prores-422-hq.mov","\\10.1.4.222\\gda\archives-sample-files\\opf-format-corpus\format-corpus\video\\Quicktime\apple-prores-422-hq.mov","apple-prores-422-hq.mov","Signature","Done","701111","File","mov","2014-02-18T16:58:16","false","484591affcae8ef5d896289db75503b603092ef8","1","x-fmt/384","video/quicktime","Quicktime",""
"8","4","file:////10.1.4.222/gda/archives-sample-files/opf-format-corpus/format-corpus/video/Quicktime/apple-prores-422-lt.mov","\\10.1.4.222\\gda\archives-sample-files\\opf-format-corpus\format-corpus\video\\Quicktime\apple-prores-422-lt.mov","apple-prores-422-lt.mov","Signature","Done","476503","File","mov","2014-02-18T16:58:16","false","4dacced1685746d8e39bb6dc36d01bf2a60a17e2","1","x-fmt/384","video/quicktime","Quicktime",""
"9","4","file:////10.1.4.222/gda/archives-sample-files/opf-format-corpus/format-corpus/video/Quicktime/apple-prores-422-proxy.mov","\\10.1.4.222\\gda\archives-sample-files\\opf-format-corpus\format-corpus\video\\Quicktime\apple-prores-422-proxy.mov","apple-prores-422-proxy.mov","Signature","Done","242855","File","mov","2014-02-18T16:58:16","false","b9d45fd2e79a83c69afe95d89a846b96bf1778b7","1","x-fmt/384","video/quicktime","Quicktime",""
"10","4","file:////10.1.4.222/gda/archives-sample-files/opf-format-corpus/format-corpus/video/Quicktime/apple-prores-422.mov","\\10.1.4.222\\gda\archives-sample-files\\opf-format-corpus\format-corpus\video\\Quicktime\apple-prores-422.mov","apple-prores-422.mov","Signature","Done","564775","File","mov","2014-02-18T16:58:16","false","faf81ab4a815cf0cd7c9b01d8ea950971d38dad1","1","x-fmt/384","video/quicktime","Quicktime",""
"11","4","file:////10.1.4.222/gda/archives-sample-files/opf-format-corpus/format-corpus/video/Quicktime/dv-dvchd-ntsc-interlaced.mov","\\10.1.4.222\\gda\archives-sample-files\\opf-format-corpus\format-corpus\video\\Quicktime\\dv-dvchd-ntsc-interlaced.mov","dv-dvchd-ntsc-interlaced.mov","Signature","Done","3001365","File","mov","2014-02-18T16:58:16","false","b9d45fd2e79a83c69afe95d89a846b96bf1778b7","1","x-fmt/384","video/quicktime","Quicktime",""
"12","4","éfile:////10.1.4.222/gda/archives-sample-files/opf-format-corpus/format-corpus/video/Quicktime/🖤dv-dvchd-ntsc-progressive.mov","\\10.1.4.222\\gda\archives-sample-files\\opf-format-corpus\format-corpus\video\\Quicktime\\dv-dvchd-ntsc-progressive.mov","🖤dv-dvchd-ntsc-progressive.mov","Signature","Done","3001365","File","mov","2014-02-18T16:58:16","false","a9caed081ab55ff1ea1b32d3eb30dab2841a9785","1","x-fmt/384","video/quicktime","Quicktime",""
"13","4","file:////10.1.4.222/gda/archives-sample-files/opf-format-corpus/format-corpus/video/Quicktime/dv-pal-interlaced.mov","\\10.1.4.222\\gda\archives-sample-files\\opf-format-corpus\format-corpus\video\\Quicktime\\dv-pal-interlaced.mov","dv-pal-interlaced.mov","Signature","Done","3601749","File","mov","2014-02-18T16:58:16","false","2ab26184bc937de129640574e75d01ed420cc19f","1","x-fmt/384","video/quicktime","Quicktime",""
"14","4","file:////10.1.4.222/gda/archives-sample-files/opf-format-corpus/format-corpus/video/Quicktime/dv-pal-progressive.mov","\\10.1.4.222\\gda\archives-sample-files\\opf-format-corpus\format-corpus\video\\Quicktime\\dv-pal-progressive.mov","dv-pal-progressive.mov","Signature","Done","3601749","File","mov","2014-02-18T16:58:16","false","7955c4e67b84f67bab77eff241a81ceba0177bf4","1","x-fmt/384","video/quicktime","Quicktime",""
"15","4","file:////10.1.4.222/gda/archives-sample-files/opf-format-corpus/format-corpus/video/Quicktime/dvcpro-hd-1080i60.mov","\\10.1.4.222\\gda\archives-sample-files\\opf-format-corpus\format-corpus\video\\Quicktime\\dvcpro-hd-1080i60.mov","dvcpro-hd-1080i60.mov","Signature","Done","12001365","File","mov","2014-02-18T16:58:17","false","d36ba66836ccc9a011e1517121648a1ba9b2f9e6","1","x-fmt/384","video/quicktime","Quicktime",""
7684,7681,"file:/home/café/HTML_143/558860.html","/home/café/HTML_143/558860.html","558860.html","Signature","Done",10701,"File","html","2012-07-26T23:22:11","true","6750b28fde934d7418c8908c55c9ef98",2,"fmt/99","text/html","Hypertext Markup Language",4,"x-fmt/394","application/vnd.wordperfect","WordPerfect for MS-DOS/Windows Document",5.1,,,,,,,,,,,,,,,,,,,,,,,,,,,,
"2","","file:/home/TestTransfers/dirs_with_various_encodings/","/home/TestTransfers/dirs_with_various_encodings","dirs_with_various_encodings",,"Done","","Folder",,"2021-07-18T17:22:24","false",,"",,"","",""
"6","2","file:/home/TestTransfers/dirs_with_various_encodings/big5/","/home/TestTransfers/dirs_with_various_encodings/big5","big5",,"Done","","Folder",,"2020-06-22T19:38:22","false",,"",,"","",""
"7","6","file:/home/TestTransfers/dirs_with_various_encodings/big5/%E5%BB%A3%E5%B7%9E/","/home/TestTransfers/dirs_with_various_encodings/big5/廣州","廣州",,"Done","","Folder",,"2020-06-22T19:38:22","false",,"",,"","",""
"16","7","file:/home/TestTransfers/dirs_with_various_encodings/big5/%E5%BB%A3%E5%B7%9E/big5_encoded_dirs.txt","/home/TestTransfers/dirs_with_various_encodings/big5/廣州/big5_encoded_dirs.txt","big5_encoded_dirs.txt","Extension","Done","96","File","txt","2020-06-22T19:38:22","false",,"1","x-fmt/111","text/plain","Plain Text File",""
"3","2","file:/home/TestTransfers/dirs_with_various_encodings/cp437/","/home/TestTransfers/dirs_with_various_encodings/cp437","cp437",,"Done","","Folder",,"2020-06-22T19:38:22","false",,"",,"","",""
"4","3","file:/home/TestTransfers/dirs_with_various_encodings/cp437/a%C3%B1o/","/home/TestTransfers/dirs_with_various_encodings/cp437/año","año",,"Done","","Folder",,"2020-06-22T19:38:22","false",,"",,"","",""
"21","4","file:/home/TestTransfers/dirs_with_various_encodings/cp437/a%C3%B1o/cp437_encoded_dirs.txt","/home/TestTransfers/dirs_with_various_encodings/cp437/año/cp437_encoded_dirs.txt","cp437_encoded_dirs.txt","Extension","Done","97","File","txt","2020-06-22T19:38:22","false",,"1","x-fmt/111","text/plain","Plain Text File",""
"5","3","file:/home/TestTransfers/dirs_with_various_encodings/cp437/caf%C3%A9/","/home/TestTransfers/dirs_with_various_encodings/cp437/café","café",,"Done","","Folder",,"2020-06-22T19:38:22","false",,"",,"","",""
"15","5","file:/home/TestTransfers/dirs_with_various_encodings/cp437/caf%C3%A9/cp437_encoded_dirs.txt","/home/TestTransfers/dirs_with_various_encodings/cp437/café/cp437_encoded_dirs.txt","cp437_encoded_dirs.txt","Extension","Done","97","File","txt","2020-06-22T19:38:22","false",,"1","x-fmt/111","text/plain","Plain Text File",""
"8","2","file:/home/TestTransfers/dirs_with_various_encodings/emoji/","/home/TestTransfers/dirs_with_various_encodings/emoji","emoji",,"Done","","Folder",,"2020-06-22T19:38:22","false",,"",,"","",""
"9","8","file:/home/TestTransfers/dirs_with_various_encodings/emoji/chess-%E2%99%95%E2%99%96%E2%99%97%E2%99%98%E2%99%99%E2%99%9A%E2%99%9B%E2%99%9C%E2%99%9D%E2%99%9E%E2%99%9F/","/home/TestTransfers/dirs_with_various_encodings/emoji/chess-♕♖♗♘♙♚♛♜♝♞♟","chess-♕♖♗♘♙♚♛♜♝♞♟",,"Done","","Folder",,"2020-06-22T19:38:22","false",,"",,"","",""
"19","9","file:/home/TestTransfers/dirs_with_various_encodings/emoji/chess-%E2%99%95%E2%99%96%E2%99%97%E2%99%98%E2%99%99%E2%99%9A%E2%99%9B%E2%99%9C%E2%99%9D%E2%99%9E%E2%99%9F/utf-8_encoded_dirs.txt","/home/TestTransfers/dirs_with_various_encodings/emoji/chess-♕♖♗♘♙♚♛♜♝♞♟/utf-8_encoded_dirs.txt","utf-8_encoded_dirs.txt","Extension","Done","97","File","txt","2020-06-22T19:38:22","false",,"1","x-fmt/111","text/plain","Plain Text File",""
"10","8","file:/home/TestTransfers/dirs_with_various_encodings/emoji/hearts-%E2%9D%A4%F0%9F%92%96%F0%9F%92%99%F0%9F%92%9A%F0%9F%92%9B%F0%9F%92%9C%F0%9F%92%9D/","/home/TestTransfers/dirs_with_various_encodings/emoji/hearts-❤💖💙💚💛💜💝","hearts-❤💖💙💚💛💜💝",,"Done","","Folder",,"2020-06-22T19:38:22","false",,"",,"","",""
"17","10","file:/home/TestTransfers/dirs_with_various_encodings/emoji/hearts-%E2%9D%A4%F0%9F%92%96%F0%9F%92%99%F0%9F%92%9A%F0%9F%92%9B%F0%9F%92%9C%F0%9F%92%9D/utf-8_encoded_dirs.txt","/home/TestTransfers/dirs_with_various_encodings/emoji/hearts-❤💖💙💚💛💜💝/utf-8_encoded_dirs.txt","utf-8_encoded_dirs.txt","Extension","Done","97","File","txt","2020-06-22T19:38:22","false",,"1","x-fmt/111","text/plain","Plain Text File",""
"22","2","file:/home/TestTransfers/dirs_with_various_encodings/sf-all.yml","/home/TestTransfers/dirs_with_various_encodings/sf-all.yml","sf-all.yml","","Done","8333","File","yml","2021-07-18T17:22:24","false",,"0",,"","",""
"13","2","file:/home/TestTransfers/dirs_with_various_encodings/shift_jis/","/home/TestTransfers/dirs_with_various_encodings/shift_jis","shift_jis",,"Done","","Folder",,"2020-06-22T19:38:22","false",,"",,"","",""
"14","13","file:/home/TestTransfers/dirs_with_various_encodings/shift_jis/%E3%81%BD%E3%81%A3%E3%81%B7%E3%82%8B%E3%83%A1%E3%82%A4%E3%83%AB/","/home/TestTransfers/dirs_with_various_encodings/shift_jis/ぽっぷるメイル","ぽっぷるメイル",,"Done","","Folder",,"2020-06-22T19:38:22","false",,"",,"","",""
"20","14","file:/home/TestTransfers/dirs_with_various_encodings/shift_jis/%E3%81%BD%E3%81%A3%E3%81%B7%E3%82%8B%E3%83%A1%E3%82%A4%E3%83%AB/shift-jis_encoded_dirs.txt","/home/TestTransfers/dirs_with_various_encodings/shift_jis/ぽっぷるメイル/shift-jis_encoded_dirs.txt","shift-jis_encoded_dirs.txt","Extension","Done","101","File","txt","2020-06-22T19:38:22","false",,"1","x-fmt/111","text/plain","Plain Text File",""
"11","2","file:/home/TestTransfers/dirs_with_various_encodings/windows_1252/","/home/TestTransfers/dirs_with_various_encodings/windows_1252","windows_1252",,"Done","","Folder",,"2020-06-22T19:38:22","false",,"",,"","",""
"12","11","file:/home/TestTransfers/dirs_with_various_encodings/windows_1252/s%C3%B8ster/","/home/TestTransfers/dirs_with_various_encodings/windows_1252/søster","søster",,"Done","","Folder",,"2020-06-22T19:38:22","false",,"",,"","",""
"18","12","file:/home/TestTransfers/dirs_with_various_encodings/windows_1252/s%C3%B8ster/cp1252_encoded_dirs.txt","/home/TestTransfers/dirs_with_various_encodings/windows_1252/søster/cp1252_encoded_dirs.txt","cp1252_encoded_dirs.txt","Extension","Done","98","File","txt","2020-06-22T19:38:22","false",,"1","x-fmt/111","text/plain","Plain Text File",""
"""

SIEGFRIED_YAML = u"""---
siegfried   : 1.9.1
scandate    : 2021-07-17T22:11:59+02:00
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
filename : 'Q10287816.gz'
filesize : 3
modified : 2021-05-24T19:26:56+02:00
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
filename : 'Q28205479🖤.info'
filesize : 8
modified : 2021-05-24T19:26:56+02:00
errors   :
md5      : bf40928c61f376064b110ff59d604160
matches  :
  - ns      : 'pronom'
    id      : 'UNKNOWN'
    format  :
    version :
    mime    :
    basis   :
    warning : 'no match; possibilities based on extension are fmt/1202'
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
filename : 'test_dir/Q42332.pdf'
filesize : 4
modified : 2021-07-08T23:21:40+02:00
errors   :
md5      : bfa4b10a76324b166cfdad5e02a63730
matches  :
  - ns      : 'pronom'
    id      : 'UNKNOWN'
    format  :
    version :
    mime    :
    basis   :
    warning : 'extension mismatch; possibilities based on extension are fmt/14, fmt/15, fmt/16, fmt/17, fmt/18, fmt/19, fmt/20, fmt/95, fmt/144, fmt/145, fmt/146, fmt/147, fmt/148, fmt/157, fmt/158, fmt/276, fmt/354, fmt/476, fmt/477, fmt/478, fmt/479, fmt/480, fmt/481, fmt/488, fmt/489, fmt/490, fmt/491, fmt/492, fmt/493, fmt/558, fmt/559, fmt/560, fmt/561, fmt/562, fmt/563, fmt/564, fmt/565, fmt/1129'
  - ns      : 'tika'
    id      : 'application/pdf'
    format  : 'Portable Document Format'
    mime    : 'application/pdf'
    basis   : 'extension match pdf'
    warning : 'match on filename only; byte/xml signatures for this format did not match'
  - ns      : 'freedesktop.org'
    id      : 'text/x-matlab'
    format  : 'MATLAB file'
    mime    : 'text/x-matlab'
    basis   : 'byte match at 0, 1 (signature 1/3); text match ASCII'
    warning : 'filename mismatch'
  - ns      : 'freedesktop.org'
    id      : 'text/x-tex'
    format  : 'TeX document'
    mime    : 'text/x-tex'
    basis   : 'byte match at 0, 1 (signature 1/2); text match ASCII'
    warning : 'filename mismatch'
  - ns      : 'loc'
    id      : 'fdd000030'
    format  : 'PDF (Portable Document Format) Family'
    full    : 'PDF (Portable Document Format) Family'
    mime    : 'application/pdf'
    basis   : 'extension match pdf; byte match at 0, 4'
    warning :
---
filename : 'test_dir/test_dir/Q42591.mp3'
filesize : 3
modified : 2021-07-08T23:21:40+02:00
errors   :
md5      : c0f44879dc0d4eae7b3f0b3e801e373c
matches  :
  - ns      : 'pronom'
    id      : 'UNKNOWN'
    format  :
    version :
    mime    :
    basis   :
    warning : 'no match; possibilities based on extension are fmt/134'
  - ns      : 'tika'
    id      : 'audio/mpeg'
    format  : 'MPEG-1 Audio Layer 3'
    mime    : 'audio/mpeg'
    basis   : 'extension match mp3; byte match at 0, 3 (signature 12/12)'
    warning :
  - ns      : 'freedesktop.org'
    id      : 'audio/mpeg'
    format  : 'MP3 audio'
    mime    : 'audio/mpeg'
    basis   : 'extension match mp3; byte match at 0, 3 (signature 2/2)'
    warning :
  - ns      : 'loc'
    id      : 'UNKNOWN'
    format  :
    full    :
    mime    :
    basis   :
    warning : 'no match; possibilities based on extension are fdd000052, fdd000053, fdd000105, fdd000111, fdd000256, fdd000275'
---
filename : 'big5/廣州/big5_encoded_dirs.txt'
filesize : 96
modified : 2020-06-22T19:38:22+02:00
errors   :
md5     : 57573bf4b57e9215f598d97469bf5fcf0046ee73
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
filename : 'cp437/año/cp437_encoded_dirs.txt'
filesize : 97
modified : 2020-06-22T19:38:22+02:00
errors   :
md5      : 0c391e403302385e9d227733fc477bf440f978d2
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
filename : 'cp437/café/cp437_encoded_dirs.txt'
filesize : 97
modified : 2020-06-22T19:38:22+02:00
errors   :
md5      : 0c391e403302385e9d227733fc477bf440f978d2
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
filename : 'emoji/chess-♕♖♗♘♙♚♛♜♝♞♟/utf-8_encoded_dirs.txt'
filesize : 97
modified : 2020-06-22T19:38:22+02:00
errors   :
md5      : d0e093259ce05cde2b326e418ac547359b91ee5f
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
filename : 'emoji/hearts-❤💖💙💚💛💜💝/utf-8_encoded_dirs.txt'
filesize : 97
modified : 2020-06-22T19:38:22+02:00
errors   :
md5      : d0e093259ce05cde2b326e418ac547359b91ee5f
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
filename : 'shift_jis/ぽっぷるメイル/shift-jis_encoded_dirs.txt'
filesize : 101
modified : 2020-06-22T19:38:22+02:00
errors   :
md5      : 4bc1d53ee7d365094fde303fec365b4fdec34c80
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
filename : 'windows_1252/søster/cp1252_encoded_dirs.txt'
filesize : 98
modified : 2020-06-22T19:38:22+02:00
errors   :
md5      : 4bc1d53ee7d365094fde303fec365b4fdec34c80
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
"""


def test_run_droid_analysis(tmp_path):
    """Test...."""
    # Read export.
    # Need a database.
    # Run analysis on database.
    # Get results.

    '''
    dir_ = tmp_path
    droid_csv = dir_ / "droid_💜_test.csv"
    droid_csv.write_text(DROID_CSV.strip())

    # Analysis from CSV will currently read the results from the CSV
    # above and output an on-disk sqlite database at tmp_path. This
    # works perfectly for us. In future, if we need to create an
    # in-memory database for any reason we can but it will take some
    # further refactoring.
    res = analysis_from_csv(str(droid_csv), True, {})

    assert res.filename.endswith("droid_💜_test")
    assert res.hashused is True
    assert res.totalmd5duplicates == 0
    '''


def test_run_siegfried_analysis(tmp_path):
    """Test...."""
    # Read export.
    # Need a database.
    # Run analysis on database.
    # Get results.

    dir_ = tmp_path
    sf_yaml = dir_ / "sf_💜_test.yaml"
    sf_yaml.write_text(SIEGFRIED_YAML.strip())

    # Analysis from CSV will currently read the results from the CSV
    # above and output an on-disk sqlite database at tmp_path. This
    # works perfectly for us. In future, if we need to create an
    # in-memory database for any reason we can but it will take some
    # further refactoring.
    res = analysis_from_csv(str(sf_yaml), True, {})

    assert res.filename.endswith("sf_💜_test")
    assert res.hashused is True

    print(res.duplicatemd5listing)
    print(res.duplicatemd5altlisting)

    assert res.totalmd5duplicates == 0
