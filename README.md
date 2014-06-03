droid-sqlite-analysis
=====================

Engine for analysis of DROID CSV export files. The tool has three purposes, 
break the DROID CSV export into its components and store them within a table in 
a SQLite database; create additional columns to augment the output where useful;
and query the SQLite database, outputting results in a readable form useful for
analysis by researchers and archivists within digital preservation departments
in memory institutions. 

See: http://www.openplanetsfoundation.org/blogs/2014-06-03-analysis-engine-droid-csv-export

There are three components to the tool:

#### droid2sqlite.py

Places DROID CSV export data into an SQLite database with the same filename
as the input. 

Single argument: --csv <input filename>

Augments DROID export data with two additional columns:

URI_SCHEME: Separates the URI_SCHEME from the DROID URI column. This is to
enable the identification of container objects found in the export specifically,
and the distinction of files stored in container objects from standalone files. 

DIR_NAME: Returns the base directory name from the filepath to enable
analysis of directory names, e.g. the number of directories in the collection.

#### droidsqliteanalysis.py

Combines the functions of droid2sqlite.py by calling droid2sqlite's primary
class. Further, queries a DROID sqlite database of the schema generated in 
droid2sqlite, and outputs the result to stdout. 

Three arguments:

* --csv <input filename>

Equivalent functionalty to droid2sqlite. Outputs a sqlite database. 

* --db <input filename>

Analyes a DROID sqlite database and outputs the results to stdout.

* --csva <input filename>

Wraps both --csv and --db into a single command. Useful for a one-off report. 
Will naturally be slower to output results. 

#### MsoftFnameAnalysis.py

Class to handle analysis of non-recommended filenames from Microsoft:
http://msdn.microsoft.com/en-us/library/aa365247(VS.85).aspx 

### TODO

* Everything is stored in the DB as a string, understand potential for typing
* Return more discrete values, ints, lists, etc. over formatted strings.
* Unit tests!

### License

Copyright (c) 2014 Ross Spencer

This software is provided 'as-is', without any express or implied warranty. In 
no event will the authors be held liable for any damages arising from the use of 
this software.

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
