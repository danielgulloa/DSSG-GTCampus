import os
import datetime
import csv
import sqlite3

#os.chdir('/Users/Daniel/Google Drive/DSSG14')
os.chdir('C:\\Users\\Richard\\Google Drive\\DSSG-Wifi')
class PopEstimation():
    def __init__(self):
        self.sqliteconnect()
        self.selectRecord()
        self.calculatePath()

        pass

    def sqliteconnect(self):
        self.con=sqlite3.connect('sampleDB.db')

    def selectRecord(self):
        sql="SELECT userMAC, day, time, router FROM mytable ORDER BY day ASC, time ASC, router ASC"
        c=self.con.cursor()
        c.execute(sql)
        self.data=c.fetchall()
        print('Done with selecting!')


    def calculatePath(self):
        currentMAC = None
        currentLocation = None
        stats = dict()

        for entry in self.data:
            if currentMAC == None:
                currentMAC = entry[0]
                currentLocation = entry[3]
                continue

            if entry[0] == currentMAC:  #same device
                try:
                    stats[currentLocation]
                    try:
                        stats[currentLocation][entry[3]] += 1
                    except:
                        stats[currentLocation][entry[3]] = 1
                except:
                    stats[currentLocation] = {entry[3]:1}

            else: #do work calculating edge stats
                currentMAC = entry[0]




            currentLocation = entry[3]

        for s in stats:
            #print s,
            for d in stats[s]:
                pass
                #print "," + d + "\t" + str(stats[s][d]) + "," ,

            #print ""
a=PopEstimation()
