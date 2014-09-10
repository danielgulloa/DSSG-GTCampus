#This python code converts the table from EstimationResults.csv into a database, so that queries such as:
#SELECT * FROM mytable WHERE timeEntry > '10:00:00' AND timeExit < '11:00:00' AND day = '10';
#can be performed

import csv, sqlite3, time

if __name__ == "__main__":
	t = time.time()
	conn = sqlite3.connect( "TimesEntryExit.db" )
	conn.text_factory = str  #bugger 8-bit bytestrings
	cur = conn.cursor()
	cur.execute('CREATE TABLE IF NOT EXISTS mytable (userID VARCHAR, month VARCHAR, day VARCHAR, timeEntry VARCHAR, timeExit VARCHAR)')
	csvData = csv.reader(open("../DGU_Data/EstimationResultsFall.csv", "rb"))
	for field1,field2,field3,field4,field5 in csvData:    
		cur.execute('INSERT OR IGNORE INTO mytable (userID, month,day,timeEntry,timeExit) VALUES (?,?,?,?,?)', (field1, field2, field3,field4, field5))
	conn.commit()
