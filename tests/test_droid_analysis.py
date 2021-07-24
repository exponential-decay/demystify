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
"9","4","file:////10.1.4.222/gda/archives-sample-files/opf-format-corpus/format-corpus/video/Quicktime/apple-prores-422-proxy.mov","\\10.1.4.222\\gda\archives-sample-files\\opf-format-corpus\format-corpus\video\\Quicktime\apple-prores-422-proxy.mov","apple-prores-422-proxy.mov","Signature","Done","242855","File","mov","2014-02-18T16:58:16","false","0e18911984ac1cd4721b4d3c9e0914cc98da3ab4","1","x-fmt/384","video/quicktime","Quicktime",""
"10","4","file:////10.1.4.222/gda/archives-sample-files/opf-format-corpus/format-corpus/video/Quicktime/apple-prores-422.mov","\\10.1.4.222\\gda\archives-sample-files\\opf-format-corpus\format-corpus\video\\Quicktime\apple-prores-422.mov","apple-prores-422.mov","Signature","Done","564775","File","mov","2014-02-18T16:58:16","false","faf81ab4a815cf0cd7c9b01d8ea950971d38dad1","1","x-fmt/384","video/quicktime","Quicktime",""
"11","4","file:////10.1.4.222/gda/archives-sample-files/opf-format-corpus/format-corpus/video/Quicktime/dv-dvchd-ntsc-interlaced.mov","\\10.1.4.222\\gda\archives-sample-files\\opf-format-corpus\format-corpus\video\\Quicktime\\dv-dvchd-ntsc-interlaced.mov","dv-dvchd-ntsc-interlaced.mov","Signature","Done","3001365","File","mov","2014-02-18T16:58:16","false","b9d45fd2e79a83c69afe95d89a846b96bf1778b7","1","x-fmt/384","video/quicktime","Quicktime",""
"12","4","éfile:////10.1.4.222/gda/archives-sample-files/opf-format-corpus/format-corpus/video/Quicktime/🖤dv-dvchd-ntsc-progressive.mov","\\10.1.4.222\\gda\archives-sample-files\\opf-format-corpus\format-corpus\video\\Quicktime\\dv-dvchd-ntsc-progressive.mov","🖤dv-dvchd-ntsc-progressive.mov","Signature","Done","3001365","File","mov","2014-02-18T16:58:16","false","a9caed081ab55ff1ea1b32d3eb30dab2841a9785","1","x-fmt/384","video/quicktime","Quicktime",""
"13","4","file:////10.1.4.222/gda/archives-sample-files/opf-format-corpus/format-corpus/video/Quicktime/dv-pal-interlaced.mov","\\10.1.4.222\\gda\archives-sample-files\\opf-format-corpus\format-corpus\video\\Quicktime\\dv-pal-interlaced.mov","dv-pal-interlaced.mov","Signature","Done","3601749","File","mov","2014-02-18T16:58:16","false","2ab26184bc937de129640574e75d01ed420cc19f","1","x-fmt/384","video/quicktime","Quicktime",""
"14","4","file:////10.1.4.222/gda/archives-sample-files/opf-format-corpus/format-corpus/video/Quicktime/dv-pal-progressive.mov","\\10.1.4.222\\gda\archives-sample-files\\opf-format-corpus\format-corpus\video\\Quicktime\\dv-pal-progressive.mov","dv-pal-progressive.mov","Signature","Done","3601749","File","mov","2014-02-18T16:58:16","false","7955c4e67b84f67bab77eff241a81ceba0177bf4","1","x-fmt/384","video/quicktime","Quicktime",""
"15","4","file:////10.1.4.222/gda/archives-sample-files/opf-format-corpus/format-corpus/video/Quicktime/dvcpro-hd-1080i60.mov","\\10.1.4.222\\gda\archives-sample-files\\opf-format-corpus\format-corpus\video\\Quicktime\\dvcpro-hd-1080i60.mov","dvcpro-hd-1080i60.mov","Signature","Done","12001365","File","mov","2014-02-18T16:58:17","false","d36ba66836ccc9a011e1517121648a1ba9b2f9e6","1","x-fmt/384","video/quicktime","Quicktime",""
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
sha1     : 57573bf4b57e9215f598d97469bf5fcf0046ee73
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
sha1     : 0c391e403302385e9d227733fc477bf440f978d2
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
sha1     : 0c391e403302385e9d227733fc477bf440f978d2
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
sha1     : d0e093259ce05cde2b326e418ac547359b91ee5f
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
sha1     : d0e093259ce05cde2b326e418ac547359b91ee5f
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
sha1     : 023d81c0f5767ffa9eae763479bda378d5be4c4d
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
sha1     : 4bc1d53ee7d365094fde303fec365b4fdec34c80
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
