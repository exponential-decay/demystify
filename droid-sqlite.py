import argparse
import sys
import sqlite3
import csv

def countFilesQuery(c):
	countfiles = "SELECT COUNT(NAME) FROM droid WHERE TYPE='File'"
	c.execute(countfiles)
	count = c.fetchone()
	print "Number of Files in collection: " + str(count[0])

def countFoldersQuery(c):
	countfiles = "SELECT COUNT(NAME) FROM droid WHERE TYPE='Folder'"
	c.execute(countfiles)
	count = c.fetchone()
	print "Number of Folders in collection: " + str(count[0])

def countUnidentifiedQuery(c):
	countfiles = "SELECT COUNT(NAME) FROM droid WHERE TYPE='File' AND (METHOD='no value' OR METHOD='Extension')"
	c.execute(countfiles)
	count = c.fetchone()
	print "Number of Unidentified Files in collection (ext only and zero ID method): " + str(count[0])

def countZeroIDMethod(c):
	countfiles = "SELECT COUNT(NAME) FROM droid WHERE TYPE='File' AND METHOD='no value'"
	c.execute(countfiles)
	count = c.fetchone()
	print "Number of Unidentified files (zero ID method): " + str(count[0])

def countExtensionIDOnly(c):
	countfiles = "SELECT COUNT(NAME) FROM droid WHERE TYPE='File' AND METHOD='Extension'"
	c.execute(countfiles)
	count = c.fetchone()
	print "Number of Extension only identifications: " + str(count[0])

def queryDB(c):
	countFilesQuery(c)
	countFoldersQuery(c)
	countUnidentifiedQuery(c)
	countZeroIDMethod(c)
	countExtensionIDOnly(c)

def droidDBSetup(droidcsv):

	DROID_COLUMNS = 18

	print sqlite3.version
	
	conn = sqlite3.connect(droidcsv.replace(".csv", "") + ".db")
	
	c = conn.cursor()

	c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='droid';")

	# Can't DROP something that doesn't exist...
	if c.fetchone() is not None:
		c.execute("DROP table droid")	# DROP just in case

	# Create table
	c.execute('''CREATE TABLE droid
					 (ID, PARENT_ID, URI, FILE_PATH, NAME, METHOD, STATUS, SIZE, TYPE, EXT, LAST_MODIFIED, EXTENSION_MISMATCH, MD5_HASH, FORMAT_COUNT, PUID, MIME_TYPE, FORMAT_NAME, FORMAT_VERSION)''')

	with open('droid-report.csv', 'rb') as csvfile:
		droidreader = csv.reader(csvfile)
		for row in droidreader:
			rowstr = ""
			if droidreader.line_num != 1:					# ignore headers
				for i,item in enumerate(row[0:DROID_COLUMNS]):
					if item == "":
						rowstr = rowstr + "'no value'"
					else:
						rowstr = rowstr + "'" + item + "'"
					
					if i < DROID_COLUMNS-1:
						rowstr = rowstr + ","
				
				#test = "INSERT INTO stocks VALUES (" + rowstr + ")"
				#print test
				
				c.execute("INSERT INTO droid VALUES (" + rowstr + ")")

	# Save (commit) the changes
	conn.commit()

	### TEMPORARY READ FUNCTIONS ###


	queryDB(c)




	### TEMPORARY READ FUNCTIONS ###


	# We can also close the connection if we are done with it.
	# Just be sure any changes have been committed or they will be lost.
	conn.close()

def handleDROIDCSV(droidcsv):
	droidDBSetup(droidcsv)

def main():

	#	Usage: 	--csv [jp2file]

	#	Handle command line arguments for the script
	parser = argparse.ArgumentParser(description='Place DROID profiles into a SQLite DB')
	parser.add_argument('--csv', help='Optional: Single DROID CSV to read.')
	
	#parser.add_argument('--pro', help='Optional: XML profile to validate against.', default=False)
	#parser.add_argument('--dif', help='Optional: Generate diff in errorlog if validation fails.', default=False)

	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(1)

	#	Parse arguments into namespace object to reference later in the script
	global args
	args = parser.parse_args()
	
	if args.csv:
		handleDROIDCSV(args.csv)			
	else:
		sys.exit(1)

if __name__ == "__main__":
	main()
