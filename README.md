# Analysis and reporting engine for digital preservation tools DROID and Siegfried

Working example __Siegfried__: [Siegfried Govdocs Select Results...][SF-1]
<br/>
Working example __DROID__: [DROID Govdocs Select Results...][DROID-1]

## Introduction

Engine for analysis of [DROID CSV][DROID-CSV] and [Seigfried][SF-2] export
files. The tool has three purposes, break the export into its components and
store them within a set of tables in a SQLite database; create additional
columns to augment the output where useful; and query the SQLite database,
outputting results in a readable form useful for analysis by researchers and
archivists within digital preservation departments in memory institutions.

### 2020/2021 refactor

This utility was first written in 2013. The code was pretty bad, but worked.
It wrapped a lot of technical debt into a small package.

The 2020/2021 refactor tries to do three things:

1. Fix minor issues.
2. Make compatible with Python 3 and temporarily, one last time with Python 2.
3. Add unit tests.

Adding unit tests is the key to your contributions and greater flexibility with
refactoring. One a release candidate is available of this work, there is more
freedom to think about next steps including exposing queries more generically
so that more folk can work with sqlitefid. And finding more generic API-like
abstractions in general so the utility is less like a monolith and more like
a configurable static analysis engine analogous to something you might work
with in Python or Golang.

## More information

See the following blogs for more information:

* [2014-06-03] [On the creation of this tool][OPF-1]
* [2015-08-25] [Creating a digital preservation rogues gallery][OPF-2]
* [2016-05-23] [Consistent and repeatable digital preservation reporting][OPF-3]
* [2016-05-24] [A multi-lingual lingua-franca and exploring ID methods][OPF-4]

COPTR Link: http://coptr.digipres.org/DROID_sqlite_analysis

## Components

There are three components to the tool.

### sqlitefid

Adds identification data to an SQLite database that forms the basis of the
entire analysis. There are five tables.

- DBMD - Database Metadata
- FILEDATA - File manifest and filesystem metadata
- IDDATA - Identification metadata
- IDRESULTS - FILEDATA/IDRESULTS junction table
- NSDATA - Namespace metadata, also secondary key (NS_ID) in IDDATA table

Will also augment DROID or Siegfried export data with additional columns:

* URI_SCHEME: Separates the URI_SCHEME from the DROID URI column. This is to
enable the identification of container objects found in the export
specifically, and the distinction of files stored in container objects from
standalone files.
* DIR_NAME: Returns the base directory name from the file path to enable
analysis of directory names, e.g. the number of directories in the collection.

### demystify

Outputs an analysis from extensive querying of the SQLite database created by
sqlitefid,

HTML is the default report output, with plain-text, and file-listings also
available.

It is a good idea to run the analysis and `>` pipe the result to a file, e.g.
`python demystify.py --export my_export.csv > my_analysis.htm`.

### Rogues Gallery (v.0.2.0, v0.5.0+)

The following flags provide Rogue or Hero output:

* `--rogues`

Outputs a list of files returned by the identification tool that might require
more analysis e.g. non-IDs, multiple IDs, extension mismatches, zero-byte
objects and duplicate files.

* `--heroes`

Outputs a list of files considered to need less analysis.

The options can be configured by looking at `denylist.cfg`. More information
can be found [here][OPF-2].

![Rogues Gallery Animation](documentation/rogues-gallery.gif)

### pathlesstaken

A string analysis engine created to highlight when string values, e.g. file
paths might need more care taken of them in a digital preservation environment,
e.g. so we don't lose diacritics during transfer - providing a checklist of
items to look at.

Includes:

* Class to handle analysis of non-recommended filenames from [Microsoft][MS-1].
* Copy of a library from Cooper Hewitt to enable writing of plain text
descriptions of [Unicode characters][UNICODE-1].

## Architecture

The tool is designed to be easily modified to create your own output by using
the Analysis Results class as a further abstraction layer (API).

![Analysis Engine Architecture](documentation/analysis-engine-architecture.png)

The recent re-factor resulted in more generic python data structures being
returned from queries and less (if not zero) formatted output. This means a
little more work has to be put into presentation of results, but it is more
flexible to what you want to do.

Tests are being implemented to promote the reliability of data returned.

## Design Decisions

There should be no dependencies associated with this tool. That being said,
you may need `lxml` for HTML output. An alternative may be found as the tool is
refactored.

If we can maintain a state of few repositories then it should promote use across
a wide-number of institutions. This has been driven by my previous two working
environments where installing Python was the first challenge... PIP and the
ability to get hold of code dependencies another - especially on multiple
user's machines where we want this tool to be successful.

## Usage Notes

Summary/Aggregate Binary / Text / Filename identification statistics are output
with the following priority:

Namespace (e.g. ordered by PRONOM first [configurable])

1. Binary and Container Identifiers
2. XML Identifiers
3. Text Identifiers
4. Filename Identifiers
5. Extension Identifiers

We need to monitor how well this works. Namespace specific statistics are also
output further down the report.

## TODO, and how you can get involved

* Internationalizing archivist descriptions [here][TRANSL-1].
* Additional typing of database fields.
* Improved container listing/handling.
* Improved 'directory' listing and handling.
* Unit tests!

As you use the tool or find problems, please report them. If you find you are
missing summaries that might be useful to you please let me know. The more the
utility is used, the more we can all benefit.

## Releases

See [Releases...][REL-1]

## License

Copyright (c) 2013 Ross Spencer

This software is provided 'as-is', without any express or implied warranty. In
no event will the authors be held liable for any damages arising from the use
of this software.

Permission is granted to anyone to use this software for any purpose, including
commercial applications, and to alter it and redistribute it freely, subject to
the following restrictions:

The origin of this software must not be misrepresented; you must not claim that
you wrote the original software. If you use this software in a product, an
acknowledgment in the product documentation would be appreciated but is not
required.

Altered source versions must be plainly marked as such, and must not be
misrepresented as being the original software.

This notice may not be removed or altered from any source distribution.

[SF-1]: https://htmlpreview.github.io/?https://github.com/exponential-decay/droid-siegfried-sqlite-analysis-engine/blob/master/govdocs-selected-corpus-output/govdocs-select-sqlite-sf.htm
[DROID-1]: https://htmlpreview.github.io/?https://github.com/exponential-decay/droid-siegfried-sqlite-analysis-engine/blob/master/govdocs-selected-corpus-output/govdocs-select-sqlite-droid.htm
[DROID-CSV]: https://github.com/digital-preservation/droid
[SF-2]: https://github.com/richardlehane/siegfried
[OPF-1]: https://openpreservation.org/blog/2014/06/03/analysis-engine-droid-csv-export/
[OPF-2]: http://openpreservation.org/blog/2015/08/25/hero-or-villain-a-tool-to-create-a-digital-preservation-rogues-gallery/
[OPF-3]: http://openpreservation.org/blog/2016/05/23/whats-in-a-namespace-the-marriage-of-droid-and-siegfried-analysis/
[OPF-4]: http://openpreservation.org/blog/2016/05/24/while-were-on-the-subject-a-few-more-points-of-interest-about-the-siegfrieddroid-analysis-tool/
[REL-1]: https://github.com/exponential-decay/droid-sqlite-analysis/releases
[MS-1]: http://msdn.microsoft.com/en-us/library/aa365247(VS.85).aspx
[UNICODE-1]: https://github.com/cooperhewitt/py-cooperhewitt-unicode
[TRANSL-1]: https://docs.google.com/spreadsheets/d/1dVsRsXgD9V2GarNHHpf6Tzhrfx99_MXt3LjSSDrNLOY/edit?usp=sharing
