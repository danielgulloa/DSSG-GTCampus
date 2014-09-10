import csv, sqlite3, time

def chunks(data, rows=10000):
    """ Divides the data into 10000 rows each """

    #for i in xrange(0, len(data), rows):
    #   yield data[i:i+rows]



if __name__ == "__main__":

    t = time.time()

    conn = sqlite3.connect( "sampleDB.db" )
    conn.text_factory = str  #bugger 8-bit bytestrings
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS mytable (month VARCHAR, day VARCHAR, time VARCHAR, userID VARCHAR, userMAC VARCHAR, VLAN VARCHAR, IP VARCHAR, routerMAC VARCHAR, router VARCHAR, status VARCHAR)')

    csvData = csv.reader(open("log_parsed.csv", "r"))

    #divData = chunks(csvData) # divide into 10000 rows each

    #cur.execute('BEGIN TRANSACTION')

    for field1,field2,field3,field4,field5,field6,field7,field8,field9,field10 in csvData:
        cur.execute('INSERT OR IGNORE INTO mytable (month,day,time,userID,userMAC,VLAN,IP,routerMAC,router,status) VALUES (?,?,?,?,?,?,?,?,?,?)', (field1, field2, field3,field4, field5,field6,field7, field8, field9,field10))

    #cur.execute('COMMIT')
    conn.commit()

    #print "\n Time Taken: %.3f sec" % (time.time()-t)
