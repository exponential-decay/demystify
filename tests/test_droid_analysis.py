# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import sys

from demystify import analysis_from_csv

DROID_CSV = u""""ID","PARENT_ID","URI","FILE_PATH","NAME","METHOD","STATUS","SIZE","TYPE","EXT","LAST_MODIFIED","EXTENSION_MISMATCH","SHA1_HASH","FORMAT_COUNT","PUID","MIME_TYPE","FORMAT_NAME","FORMAT_VERSION"
"2","","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures","fixtures","","Done","","Folder","","2021-07-25T10:44:03","false","","","","","",""
"86","2","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings","dirs_with_various_encodings","","Done","","Folder","","2021-07-25T10:40:16","false","","","","","",""
"90","86","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/big5/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/big5","big5","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"93","90","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/big5/%E5%BB%A3%E5%B7%9E/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/big5/廣州","廣州","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"94","93","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/big5/%E5%BB%A3%E5%B7%9E/big5_encoded_dirs.txt","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/big5/廣州/big5_encoded_dirs.txt","big5_encoded_dirs.txt","Extension","Done","96","File","txt","2020-06-22T19:38:22","false","57573bf4b57e9215f598d97469bf5fcf0046ee73","1","x-fmt/111","text/plain","Plain Text File",""
"87","86","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437","cp437","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"88","87","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437/a%C3%B1o/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437/año","año","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"91","88","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437/a%C3%B1o/cp437_encoded_dirs.txt","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437/año/cp437_encoded_dirs.txt","cp437_encoded_dirs.txt","Extension","Done","97","File","txt","2020-06-22T19:38:22","false","0c391e403302385e9d227733fc477bf440f978d2","1","x-fmt/111","text/plain","Plain Text File",""
"89","87","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437/caf%C3%A9/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437/café","café","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"92","89","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437/caf%C3%A9/cp437_encoded_dirs.txt","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/cp437/café/cp437_encoded_dirs.txt","cp437_encoded_dirs.txt","Extension","Done","97","File","txt","2020-06-22T19:38:22","false","0c391e403302385e9d227733fc477bf440f978d2","1","x-fmt/111","text/plain","Plain Text File",""
"95","86","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji","emoji","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"96","95","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji/chess-%E2%99%95%E2%99%96%E2%99%97%E2%99%98%E2%99%99%E2%99%9A%E2%99%9B%E2%99%9C%E2%99%9D%E2%99%9E%E2%99%9F/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji/chess-♕♖♗♘♙♚♛♜♝♞♟","chess-♕♖♗♘♙♚♛♜♝♞♟","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"99","96","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji/chess-%E2%99%95%E2%99%96%E2%99%97%E2%99%98%E2%99%99%E2%99%9A%E2%99%9B%E2%99%9C%E2%99%9D%E2%99%9E%E2%99%9F/utf-8_encoded_dirs.txt","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji/chess-♕♖♗♘♙♚♛♜♝♞♟/utf-8_encoded_dirs.txt","utf-8_encoded_dirs.txt","Extension","Done","97","File","txt","2020-06-22T19:38:22","false","d0e093259ce05cde2b326e418ac547359b91ee5f","1","x-fmt/111","text/plain","Plain Text File",""
"97","95","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji/hearts-%E2%9D%A4%F0%9F%92%96%F0%9F%92%99%F0%9F%92%9A%F0%9F%92%9B%F0%9F%92%9C%F0%9F%92%9D/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji/hearts-❤💖💙💚💛💜💝","hearts-❤💖💙💚💛💜💝","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"100","97","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji/hearts-%E2%9D%A4%F0%9F%92%96%F0%9F%92%99%F0%9F%92%9A%F0%9F%92%9B%F0%9F%92%9C%F0%9F%92%9D/utf-8_encoded_dirs.txt","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/emoji/hearts-❤💖💙💚💛💜💝/utf-8_encoded_dirs.txt","utf-8_encoded_dirs.txt","Extension","Done","97","File","txt","2020-06-22T19:38:22","false","d0e093259ce05cde2b326e418ac547359b91ee5f","1","x-fmt/111","text/plain","Plain Text File",""
"102","86","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/shift_jis/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/shift_jis","shift_jis","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"105","102","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/shift_jis/%E3%81%BD%E3%81%A3%E3%81%B7%E3%82%8B%E3%83%A1%E3%82%A4%E3%83%AB/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/shift_jis/ぽっぷるメイル","ぽっぷるメイル","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"106","105","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/shift_jis/%E3%81%BD%E3%81%A3%E3%81%B7%E3%82%8B%E3%83%A1%E3%82%A4%E3%83%AB/shift-jis_encoded_dirs.txt","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/shift_jis/ぽっぷるメイル/shift-jis_encoded_dirs.txt","shift-jis_encoded_dirs.txt","Extension","Done","101","File","txt","2020-06-22T19:38:22","false","023d81c0f5767ffa9eae763479bda378d5be4c4d","1","x-fmt/111","text/plain","Plain Text File",""
"98","86","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/windows_1252/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/windows_1252","windows_1252","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"101","98","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/windows_1252/s%C3%B8ster/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/windows_1252/søster","søster","","Done","","Folder","","2020-06-22T19:38:22","false","","","","","",""
"103","101","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/windows_1252/s%C3%B8ster/cp1252_encoded_dirs.txt","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/dirs_with_various_encodings/windows_1252/søster/cp1252_encoded_dirs.txt","cp1252_encoded_dirs.txt","Extension","Done","98","File","txt","2020-06-22T19:38:22","false","4bc1d53ee7d365094fde303fec365b4fdec34c80","1","x-fmt/111","text/plain","Plain Text File",""
"70","2","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings","files_with_various_encodings","","Done","","Folder","","2020-06-22T19:38:21","false","","","","","",""
"79","70","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/emoji/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/emoji","emoji","","Done","","Folder","","2020-06-22T19:38:21","false","","","","","",""
"82","79","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/emoji/chess-%E2%99%95%E2%99%96%E2%99%97%E2%99%98%E2%99%99%E2%99%9A%E2%99%9B%E2%99%9C%E2%99%9D%E2%99%9E%E2%99%9F.txt","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/emoji/chess-♕♖♗♘♙♚♛♜♝♞♟.txt","chess-♕♖♗♘♙♚♛♜♝♞♟.txt","Extension","Done","54","File","txt","2020-06-22T19:38:21","false","1766219eb64113604a1fe2c003b10c8258bb1cbb","1","x-fmt/111","text/plain","Plain Text File",""
"81","79","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/emoji/hearts-%E2%9D%A4%F0%9F%92%96%F0%9F%92%99%F0%9F%92%9A%F0%9F%92%9B%F0%9F%92%9C%F0%9F%92%9D.txt","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/files_with_various_encodings/emoji/hearts-❤💖💙💚💛💜💝.txt","hearts-❤💖💙💚💛💜💝.txt","Extension","Done","54","File","txt","2020-06-22T19:38:21","false","1766219eb64113604a1fe2c003b10c8258bb1cbb","1","x-fmt/111","text/plain","Plain Text File",""
"3","2","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus","opf-format-corpus","","Done","","Folder","","2021-07-25T10:41:15","false","","","","","",""
"4","3","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video","video","","Done","","Folder","","2019-01-30T11:48:01","false","","","","","",""
"5","4","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime","Quicktime","","Done","","Folder","","2019-01-30T11:48:01","false","","","","","",""
"31","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/README.md","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/README.md","README.md","Extension","Done","1693","File","md","2019-01-30T11:48:01","false","df0c5f820602a7381c3f88c9b8d8ea07561adfaf","1","fmt/1149","text/markdown","Markdown",""
"48","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/animation.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/animation.mov","animation.mov","Signature","Done","1020209","File","mov","2019-01-30T11:48:01","false","edb5226b963f449ce58054809149cb812bdf8c0a","1","x-fmt/384","video/quicktime","Quicktime",""
"13","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/apple-intermediate-codec.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/apple-intermediate-codec.mov","apple-intermediate-codec.mov","Signature","Done","319539","File","mov","2019-01-30T11:48:01","false","d097cf36467373f52b974542d48bec134279fa3f","1","x-fmt/384","video/quicktime","Quicktime",""
"17","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/apple-prores-422-hq.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/apple-prores-422-hq.mov","apple-prores-422-hq.mov","Signature","Done","701111","File","mov","2019-01-30T11:48:01","false","484591affcae8ef5d896289db75503b603092ef8","1","x-fmt/384","video/quicktime","Quicktime",""
"29","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/apple-prores-422-lt.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/apple-prores-422-lt.mov","apple-prores-422-lt.mov","Signature","Done","476503","File","mov","2019-01-30T11:48:01","false","4dacced1685746d8e39bb6dc36d01bf2a60a17e2","1","x-fmt/384","video/quicktime","Quicktime",""
"65","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/apple-prores-422-proxy.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/apple-prores-422-proxy.mov","apple-prores-422-proxy.mov","Signature","Done","242855","File","mov","2019-01-30T11:48:01","false","0e18911984ac1cd4721b4d3c9e0914cc98da3ab4","1","x-fmt/384","video/quicktime","Quicktime",""
"19","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/apple-prores-422.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/apple-prores-422.mov","apple-prores-422.mov","Signature","Done","564775","File","mov","2019-01-30T11:48:01","false","faf81ab4a815cf0cd7c9b01d8ea950971d38dad1","1","x-fmt/384","video/quicktime","Quicktime",""
"33","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dv-dvchd-ntsc-interlaced.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dv-dvchd-ntsc-interlaced.mov","dv-dvchd-ntsc-interlaced.mov","Signature","Done","3001365","File","mov","2019-01-30T11:48:01","false","b9d45fd2e79a83c69afe95d89a846b96bf1778b7","1","x-fmt/384","video/quicktime","Quicktime",""
"12","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dv-dvchd-ntsc-progressive.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dv-dvchd-ntsc-progressive.mov","dv-dvchd-ntsc-progressive.mov","Signature","Done","3001365","File","mov","2019-01-30T11:48:01","false","a9caed081ab55ff1ea1b32d3eb30dab2841a9785","1","x-fmt/384","video/quicktime","Quicktime",""
"10","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dv-pal-interlaced.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dv-pal-interlaced.mov","dv-pal-interlaced.mov","Signature","Done","3601749","File","mov","2019-01-30T11:48:01","false","2ab26184bc937de129640574e75d01ed420cc19f","1","x-fmt/384","video/quicktime","Quicktime",""
"38","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dv-pal-progressive.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dv-pal-progressive.mov","dv-pal-progressive.mov","Signature","Done","3601749","File","mov","2019-01-30T11:48:01","false","7955c4e67b84f67bab77eff241a81ceba0177bf4","1","x-fmt/384","video/quicktime","Quicktime",""
"47","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-1080i50.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-1080i50.mov","dvcpro-hd-1080i50.mov","Signature","Done","14401365","File","mov","2019-01-30T11:48:01","false","a0629e27b3a4ba34e3a39d8525dcf8d3187df833","1","x-fmt/384","video/quicktime","Quicktime",""
"107","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-1080i60.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-1080i60.mov","dvcpro-hd-1080i60.mov","Signature","Done","12001365","File","mov","2019-01-30T11:48:01","false","d36ba66836ccc9a011e1517121648a1ba9b2f9e6","1","x-fmt/384","video/quicktime","Quicktime",""
"26","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-1080p25.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-1080p25.mov","dvcpro-hd-1080p25.mov","Signature","Done","14401365","File","mov","2019-01-30T11:48:01","false","1ed7801d801562d05a1b0e8d75c3ddad0cffd14e","1","x-fmt/384","video/quicktime","Quicktime",""
"32","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-1080p30.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-1080p30.mov","dvcpro-hd-1080p30.mov","Signature","Done","12001365","File","mov","2019-01-30T11:48:01","false","89c41cf838e2c5762985f7696c3964189b67b7d1","1","x-fmt/384","video/quicktime","Quicktime",""
"43","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-720p50.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-720p50.mov","dvcpro-hd-720p50.mov","Signature","Done","7201357","File","mov","2019-01-30T11:48:01","false","e8f149fd7f008ddd46e24127f36c72851f476755","1","x-fmt/384","video/quicktime","Quicktime",""
"39","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-720p60.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-hd-720p60.mov","dvcpro-hd-720p60.mov","Signature","Done","6001485","File","mov","2019-01-30T11:48:01","false","bf886861b087e6f823dfe967c28ee2e522acf252","1","x-fmt/384","video/quicktime","Quicktime",""
"56","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-pal-interlaced.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-pal-interlaced.mov","dvcpro-pal-interlaced.mov","Signature","Done","3601749","File","mov","2019-01-30T11:48:01","false","c3bc3d41c73024f5e12e661de693f78d673c700e","1","x-fmt/384","video/quicktime","Quicktime",""
"24","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-pal-progressive.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro-pal-progressive.mov","dvcpro-pal-progressive.mov","Signature","Done","3601749","File","mov","2019-01-30T11:48:01","false","8f92210bd09f17bd40ac9dc17712abf271f4e346","1","x-fmt/384","video/quicktime","Quicktime",""
"22","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro50-ntsc-interlaced.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro50-ntsc-interlaced.mov","dvcpro50-ntsc-interlaced.mov","Signature","Done","6001377","File","mov","2019-01-30T11:48:01","false","db295931426af172f28724a9520b0a5c54b8ba80","1","x-fmt/384","video/quicktime","Quicktime",""
"23","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro50-ntsc-progressive.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro50-ntsc-progressive.mov","dvcpro50-ntsc-progressive.mov","Signature","Done","6001377","File","mov","2019-01-30T11:48:01","false","ddf277694ce7e023156f878fda3ce18f24630225","1","x-fmt/384","video/quicktime","Quicktime",""
"59","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro50-pal-interlaced.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro50-pal-interlaced.mov","dvcpro50-pal-interlaced.mov","Signature","Done","7203433","File","mov","2019-01-30T11:48:01","false","8889f04906ab0b6944b52b5a53c91d0180f47806","1","x-fmt/384","video/quicktime","Quicktime",""
"58","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro50-pal-progressive.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/dvcpro50-pal-progressive.mov","dvcpro50-pal-progressive.mov","Signature","Done","7203433","File","mov","2019-01-30T11:48:01","false","992d536199aedd26bfe9a1cf10535b931b20ad21","1","x-fmt/384","video/quicktime","Quicktime",""
"11","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/hdv-1080i50.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/hdv-1080i50.mov","hdv-1080i50.mov","Signature","Done","3126319","File","mov","2019-01-30T11:48:01","false","6b56ed491972f5c70048b06e74a0c5019fbc1677","1","x-fmt/384","video/quicktime","Quicktime",""
"53","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/hdv-1080i60.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/hdv-1080i60.mov","hdv-1080i60.mov","Signature","Done","2607767","File","mov","2019-01-30T11:48:01","false","ee1ea9938b1fdbfa19f9b1b19f6a46a84641ad3d","1","x-fmt/384","video/quicktime","Quicktime",""
"34","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/hdv-1080p24.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/hdv-1080p24.mov","hdv-1080p24.mov","Signature","Done","3259865","File","mov","2019-01-30T11:48:01","false","7cac2e4b336a5db6b262894df06366dd6f168929","1","x-fmt/384","video/quicktime","Quicktime",""
"36","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/hdv-1080p25.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/hdv-1080p25.mov","hdv-1080p25.mov","Signature","Done","3126319","File","mov","2019-01-30T11:48:01","false","a4ff826f0b4252c611c41a625ce3403e8a50f632","1","x-fmt/384","video/quicktime","Quicktime",""
"55","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/hdv-1080p30.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/hdv-1080p30.mov","hdv-1080p30.mov","Signature","Done","2607767","File","mov","2019-01-30T11:48:01","false","f168fbd2c9031dac51bf0291efbf1d1fc16f9d5a","1","x-fmt/384","video/quicktime","Quicktime",""
"44","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/hdv-720p24.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/hdv-720p24.mov","hdv-720p24.mov","Signature","Done","2387457","File","mov","2019-01-30T11:48:01","false","a64eb9b39f672cc93b66ceb2d31734ba9e0c0879","1","x-fmt/384","video/quicktime","Quicktime",""
"49","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/hdv-720p25.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/hdv-720p25.mov","hdv-720p25.mov","Signature","Done","2289384","File","mov","2019-01-30T11:48:01","false","9aab7387dbb9fa63cb6c39f08aaab752a4255d89","1","x-fmt/384","video/quicktime","Quicktime",""
"37","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/hdv-720p30.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/hdv-720p30.mov","hdv-720p30.mov","Signature","Done","1909786","File","mov","2019-01-30T11:48:01","false","294ef6e370f9424b44319a1021cf22cb4d94ec62","1","x-fmt/384","video/quicktime","Quicktime",""
"60","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/hdv-720p50.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/hdv-720p50.mov","hdv-720p50.mov","Signature","Done","1170099","File","mov","2019-01-30T11:48:01","false","fc4da537cd375d910bae33a935363c9d47d0ebb0","1","x-fmt/384","video/quicktime","Quicktime",""
"63","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/hdv-720p60.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/hdv-720p60.mov","hdv-720p60.mov","Signature","Done","987697","File","mov","2019-01-30T11:48:01","false","a6019383b2669b0407cd75567615824538d1ae06","1","x-fmt/384","video/quicktime","Quicktime",""
"41","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/jpeg2000.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/jpeg2000.mov","jpeg2000.mov","Signature","Done","383905","File","mov","2019-01-30T11:48:01","true","1b799ef725179db58bc7972d976eca892a2d6aae","2","x-fmt/384","video/quicktime","Quicktime","","fmt/1280","","NCH Dictation Audio File",""
"35","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/mpeg-imx-525-60.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/mpeg-imx-525-60.mov","mpeg-imx-525-60.mov","Signature","Done","3137357","File","mov","2019-01-30T11:48:01","false","1802444cd6e6493570c2e6837be583041d393a00","1","x-fmt/384","video/quicktime","Quicktime",""
"8","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/photo-jpeg.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/photo-jpeg.mov","photo-jpeg.mov","Signature","Done","575929","File","mov","2019-01-30T11:48:01","false","fdcca488ab2d26e7981490c0200fe1d8d07519d5","1","x-fmt/384","video/quicktime","Quicktime",""
"15","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/png.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/png.mov","png.mov","Signature","Done","47700","File","mov","2019-01-30T11:48:01","false","1b605376ddd378705f0f33a3414e08504eb6d353","1","x-fmt/384","video/quicktime","Quicktime",""
"51","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-ex-1080i50.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-ex-1080i50.mov","xdcam-ex-1080i50.mov","Signature","Done","699984","File","mov","2019-01-30T11:48:01","false","58e7dedccc95a93367ac3f0d238e2b5965eea212","1","x-fmt/384","video/quicktime","Quicktime",""
"30","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-ex-1080i60.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-ex-1080i60.mov","xdcam-ex-1080i60.mov","Signature","Done","597533","File","mov","2019-01-30T11:48:01","false","77d7658f937afc8b7f7d009ea1e2d1f3aee0bf2e","1","x-fmt/384","video/quicktime","Quicktime",""
"42","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-ex-1080p24.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-ex-1080p24.mov","xdcam-ex-1080p24.mov","Signature","Done","790594","File","mov","2019-01-30T11:48:01","false","02e9a6af2f6bb92691ecd09a6893a4c520521ba0","1","x-fmt/384","video/quicktime","Quicktime",""
"18","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-ex-1080p25.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-ex-1080p25.mov","xdcam-ex-1080p25.mov","Signature","Done","790594","File","mov","2019-01-30T11:48:01","false","36fc1a999edc619bfe0d5d444c9c89282e2ac6c2","1","x-fmt/384","video/quicktime","Quicktime",""
"52","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-ex-1080p30.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-ex-1080p30.mov","xdcam-ex-1080p30.mov","Signature","Done","670768","File","mov","2019-01-30T11:48:01","false","6ee43071769d5184debaba67be970ce6fd8d43a4","1","x-fmt/384","video/quicktime","Quicktime",""
"28","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-ex-720p24.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-ex-720p24.mov","xdcam-ex-720p24.mov","Signature","Done","409394","File","mov","2019-01-30T11:48:01","false","2646608303f08c57c8a22282044d2042d7a5f8aa","1","x-fmt/384","video/quicktime","Quicktime",""
"27","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-ex-720p25.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-ex-720p25.mov","xdcam-ex-720p25.mov","Signature","Done","409394","File","mov","2019-01-30T11:48:01","false","96ec0a49920de869f4214559fbc147d02d8c8701","1","x-fmt/384","video/quicktime","Quicktime",""
"64","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-ex-720p30.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-ex-720p30.mov","xdcam-ex-720p30.mov","Signature","Done","344932","File","mov","2019-01-30T11:48:01","false","35b465575ec40cdf42a0fa18820474d86dee3bb2","1","x-fmt/384","video/quicktime","Quicktime",""
"46","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-ex-720p50.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-ex-720p50.mov","xdcam-ex-720p50.mov","Signature","Done","409394","File","mov","2019-01-30T11:48:01","false","79ed0ed98759b59ca5962ef8fd685e8263e386ba","1","x-fmt/384","video/quicktime","Quicktime",""
"6","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-ex-720p60.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-ex-720p60.mov","xdcam-ex-720p60.mov","Signature","Done","409394","File","mov","2019-01-30T11:48:01","false","00eab4d5225b326ba632d585a4b98efe4c341cb9","1","x-fmt/384","video/quicktime","Quicktime",""
"14","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd-1080i50.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd-1080i50.mov","xdcam-hd-1080i50.mov","Signature","Done","623616","File","mov","2019-01-30T11:48:01","false","9ec98c093d42f3660eb077c7686d9a625a9a8f16","1","x-fmt/384","video/quicktime","Quicktime",""
"61","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd-1080i60.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd-1080i60.mov","xdcam-hd-1080i60.mov","Signature","Done","530058","File","mov","2019-01-30T11:48:01","false","170f4a64be4c4d2a1fb0c2d8d5ba22b9c3525b91","1","x-fmt/384","video/quicktime","Quicktime",""
"7","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd-1080p24.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd-1080p24.mov","xdcam-hd-1080p24.mov","Signature","Done","694863","File","mov","2019-01-30T11:48:01","false","8db676f9908b2bdb0c636aba969fbecab1bcef6c","1","x-fmt/384","video/quicktime","Quicktime",""
"9","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd-1080p25.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd-1080p25.mov","xdcam-hd-1080p25.mov","Signature","Done","694863","File","mov","2019-01-30T11:48:01","false","2d87b7896bd817f05ff0fdf272a099bce9d51989","1","x-fmt/384","video/quicktime","Quicktime",""
"45","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd-1080p30.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd-1080p30.mov","xdcam-hd-1080p30.mov","Signature","Done","583993","File","mov","2019-01-30T11:48:01","false","0cb012a44825a2b79c448477e4bbef16e49626ee","1","x-fmt/384","video/quicktime","Quicktime",""
"50","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-1080i50.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-1080i50.mov","xdcam-hd422-1080i50.mov","Signature","Done","6251203","File","mov","2019-01-30T11:48:01","false","95b15f2563753553a027216b404a81647c8fdf0d","1","x-fmt/384","video/quicktime","Quicktime",""
"20","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-1080i60.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-1080i60.mov","xdcam-hd422-1080i60.mov","Signature","Done","5215055","File","mov","2019-01-30T11:48:01","false","d945f00c85080386b11099a51cd4bf254598a1dd","1","x-fmt/384","video/quicktime","Quicktime",""
"21","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-1080p24.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-1080p24.mov","xdcam-hd422-1080p24.mov","Signature","Done","6518304","File","mov","2019-01-30T11:48:01","false","0a19e7e1b316f80364f628b1a665464e2385d84a","1","x-fmt/384","video/quicktime","Quicktime",""
"40","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-1080p25.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-1080p25.mov","xdcam-hd422-1080p25.mov","Signature","Done","6251203","File","mov","2019-01-30T11:48:01","false","264b489f52f90d12150e2606112d50c5f617e9b8","1","x-fmt/384","video/quicktime","Quicktime",""
"16","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-1080p30.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-1080p30.mov","xdcam-hd422-1080p30.mov","Signature","Done","5215055","File","mov","2019-01-30T11:48:01","false","a65d5d46d9ea600a437bc4c497e3d38c141696b3","1","x-fmt/384","video/quicktime","Quicktime",""
"104","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-720p24.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-720p24.mov","xdcam-hd422-720p24.mov","Signature","Done","6518304","File","mov","2019-01-30T11:48:01","false","148bd09ab70b2f1fec93305c85e598bf882a4f00","1","x-fmt/384","video/quicktime","Quicktime",""
"25","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-720p25.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-720p25.mov","xdcam-hd422-720p25.mov","Signature","Done","6251203","File","mov","2019-01-30T11:48:01","false","602747ba3740e6fd9236f3c338a20d7eb4a78f66","1","x-fmt/384","video/quicktime","Quicktime",""
"54","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-720p30.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-720p30.mov","xdcam-hd422-720p30.mov","Signature","Done","5215055","File","mov","2019-01-30T11:48:01","false","020173c0d295ec2fc46f180d24d808218df471bd","1","x-fmt/384","video/quicktime","Quicktime",""
"57","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-720p50.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-720p50.mov","xdcam-hd422-720p50.mov","Signature","Done","3125967","File","mov","2019-01-30T11:48:01","false","8f5c817fb3f87306d228c953a0e0a94420166876","1","x-fmt/384","video/quicktime","Quicktime",""
"75","5","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-720p60.mov","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-720p60.mov","xdcam-hd422-720p60.mov","Signature","Done","2607739","File","mov","2019-01-30T11:48:01","false","b8f3a3a714e33a805e3c31d36382a35898f7baf2","1","x-fmt/384","video/quicktime","Quicktime",""
"62","2","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats","synthetically_unknown_formats","","Done","","Folder","","2020-01-15T20:17:02","false","","","","","",""
"69","62","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/README.md","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/README.md","README.md","Extension","Done","1257","File","md","2020-01-15T20:17:02","false","7d64e7c306839b7c515859e2424a499e368644f3","1","fmt/1149","text/markdown","Markdown",""
"67","62","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/baseball.format","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/baseball.format","baseball.format","","Done","52","File","format","2020-01-15T20:17:02","false","98653b8ba394cce54882085b364bef3901175fbc","0","","","",""
"73","62","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/caboose.format","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/caboose.format","caboose.format","","Done","52","File","format","2020-01-15T20:17:02","false","bee62ff431a072f6f6932ba081e60697f3d38ef7","0","","","",""
"72","62","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/cassette.format","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/cassette.format","cassette.format","","Done","52","File","format","2020-01-15T20:17:02","false","2a7a5004b42079f79ce5616f68173f7e30f96a65","0","","","",""
"66","62","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/debateable.format","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/debateable.format","debateable.format","","Done","52","File","format","2020-01-15T20:17:02","false","f5ae2731456e03aa5af537f66542ba08ee4c7bc0","0","","","",""
"68","62","file:/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/looseleaf.format","/home/ross-spencer/git/exponential-decay/demystify/tests/fixtures/synthetically_unknown_formats/looseleaf.format","looseleaf.format","","Done","52","File","format","2020-01-15T20:17:02","false","89f55e08287c1d34a900c2974039c5b3088461c4","0","","","",""
"""

SIEGFRIED_YAML = u"""---
siegfried   : 1.9.1
scandate    : 2021-07-25T10:51:33+02:00
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
filename : 'fixtures/dirs_with_various_encodings/big5/廣州/big5_encoded_dirs.txt'
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
filename : 'fixtures/dirs_with_various_encodings/cp437/año/cp437_encoded_dirs.txt'
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
filename : 'fixtures/dirs_with_various_encodings/cp437/café/cp437_encoded_dirs.txt'
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
filename : 'fixtures/dirs_with_various_encodings/emoji/chess-♕♖♗♘♙♚♛♜♝♞♟/utf-8_encoded_dirs.txt'
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
filename : 'fixtures/dirs_with_various_encodings/emoji/hearts-❤💖💙💚💛💜💝/utf-8_encoded_dirs.txt'
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
filename : 'fixtures/dirs_with_various_encodings/windows_1252/søster/cp1252_encoded_dirs.txt'
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
filename : 'fixtures/files_with_various_encodings/emoji/chess-♕♖♗♘♙♚♛♜♝♞♟.txt'
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/README.md'
filesize : 1693
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 67d8097d818ad37cc87a74d4022e67c4
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/apple-prores-422-hq.mov'
filesize : 701111
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 77e088fa5cc4d0a292e0f8f9f5f36cf0
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/apple-prores-422-lt.mov'
filesize : 476503
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 61d192151181b8449ccf738e26337ef0
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/apple-prores-422-proxy.mov'
filesize : 242855
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 7a9644967e86ef8efc4de7e3d357370a
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/dv-pal-progressive.mov'
filesize : 3601749
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : c234c2e13aefbcd7c46b35d048c9fa76
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/dvcpro50-ntsc-interlaced.mov'
filesize : 6001377
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 6ddcba13e200d0432bc86e5920e2d267
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/dvcpro50-ntsc-progressive.mov'
filesize : 6001377
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 92b9b27c3ba194dc54d82c41b35a50a8
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/hdv-1080i50.mov'
filesize : 3126319
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 3517df0865f7a4c22285f2aa86741b5f
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/hdv-1080i60.mov'
filesize : 2607767
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 8750b0a29daddf8d9e8b807c4936bf1f
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/hdv-1080p24.mov'
filesize : 3259865
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : cbdce5b8efed06755d4600ded9113644
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/hdv-1080p25.mov'
filesize : 3126319
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : fed5e9043e284b716c9bc09ca06966be
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/hdv-1080p30.mov'
filesize : 2607767
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : b58212cff6952f6df4b0e01c8f6ca853
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/hdv-720p24.mov'
filesize : 2387457
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : d485fa6f7627cda72b29380e1d5232f1
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/hdv-720p25.mov'
filesize : 2289384
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 8ff28e345695e7a8a6f6c0f593e44ecd
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/hdv-720p30.mov'
filesize : 1909786
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 9524b5eb29d6a9e33399e4ca54eede7a
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/hdv-720p50.mov'
filesize : 1170099
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 8595127c38b5aefef0ab12273ad3410e
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/hdv-720p60.mov'
filesize : 987697
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 2e22a0cf599fa35112eed32d99d348a4
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/mpeg-imx-525-60.mov'
filesize : 3137357
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 72afdc76f72e769782ff2e6dc08c7adf
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/png.mov'
filesize : 47700
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 99e52d360b50484d879af9fbc43261b7
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/xdcam-ex-1080i50.mov'
filesize : 699984
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : fd4ae1dbe8635a81e8eaa84e5310ce0f
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/xdcam-ex-1080i60.mov'
filesize : 597533
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : c06e8587f528e970602a1dab63c7301e
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/xdcam-ex-1080p24.mov'
filesize : 790594
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 491a28657ad8dfd77e7cc0be37897c3f
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/xdcam-ex-1080p25.mov'
filesize : 790594
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : dd1fe14b732fa6375d23c0c306d563e9
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/xdcam-ex-1080p30.mov'
filesize : 670768
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : e512ff90fc55d33d5d53f32c7e555af3
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/xdcam-ex-720p24.mov'
filesize : 409394
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 7cf2404c3832d1789a489e8f1273ecba
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/xdcam-ex-720p25.mov'
filesize : 409394
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 5b40236d10a339cb87f9921e6375e733
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/xdcam-ex-720p30.mov'
filesize : 344932
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : c165e2eb75ba952203df0e6fb053be91
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/xdcam-ex-720p50.mov'
filesize : 409394
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 68c3c9c210cb11d1dcf7214056a20af8
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/xdcam-ex-720p60.mov'
filesize : 409394
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 4a71531b6bbeb34841d0ce1b68a7ef34
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/xdcam-hd-1080i50.mov'
filesize : 623616
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 148f300662e04504a34ef5f1a642ff5d
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/xdcam-hd-1080i60.mov'
filesize : 530058
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 607dca4e14c2d792e310b975648c6286
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/xdcam-hd-1080p24.mov'
filesize : 694863
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 54c55beef19db426c2a0ef8799ac8815
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-1080p24.mov'
filesize : 6518304
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 57fecbeb347cc16ded2ab87d3b957a3d
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-1080p25.mov'
filesize : 6251203
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : 5ef708aa13aa301f446610646ad38a94
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-1080p30.mov'
filesize : 5215055
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : efaafd4445bed1e4d15d854f866155ad
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-720p24.mov'
filesize : 6518304
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : d407fe22cdcae5ffe2c7cf49bdc898a6
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
filename : 'fixtures/opf-format-corpus/video/Quicktime/xdcam-hd422-720p25.mov'
filesize : 6251203
modified : 2019-01-30T11:48:01+01:00
errors   :
md5      : a57b120db38453ca403454522ef59067
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
"""  # noqa: W605

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
