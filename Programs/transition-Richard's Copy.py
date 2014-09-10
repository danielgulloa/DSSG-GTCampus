import os
import datetime
import csv
import sqlite3
import pickle

# os.chdir('/Users/Daniel/Google Drive/DSSG-WiFi')
#os.chdir('C:\\Users\\Richard\\Google Drive\\DSSG-Wifi')
class PopEstimation():
    def __init__(self):
        self.sqliteconnect()
        for mon in ['01','02','03','04','05','06']:
            self.selectRecord(mon)
            self.calculatePath()
            self.calculatePathReverse()

        pass

    def sqliteconnect(self):
        self.con=sqlite3.connect('sampleDB.db')

    def selectRecord(self,mon):
        sql="SELECT userMAC, day, time, router FROM month"+mon+" ORDER BY userMAC ASC, day ASC, time ASC"
        c=self.con.cursor()
        c.execute(sql)
        self.data=c.fetchall()
        #print 'Done with selecting!'+mon
        #print(self.data[:10])


    def calculatePath(self):
        currentMAC = None
        currentLocation = None
        try:
            self.stats
        except:
            self.stats = dict()

        for entry in self.data:
            if currentMAC == None:
                currentMAC = entry[0]
                currentLocation = entry[3]
                continue

            if entry[0] == currentMAC:  #same device
                try:
                    self.stats[currentLocation]
                    try:
                        self.stats[currentLocation][entry[3]] += 1
                        #print(currentLocation,entry[3])
                    except:
                        #print('MEH')
                        self.stats[currentLocation][entry[3]] = 1
                except:
                    self.stats[currentLocation] = {entry[3]:1}

            else: #do work calculating edge stats
                currentMAC = entry[0]




            currentLocation = entry[3]

    def calculatePathReverse(self):
        currentMAC = None
        currentLocation = None
        try:
            self.statsReverse
        except:
            self.statsReverse = dict()

        for entry in self.data:
            if currentMAC == None:
                currentMAC = entry[0]
                currentLocation = entry[3]
                continue

            if entry[0] == currentMAC:  #same device
                try:
                    self.statsReverse[entry[3]]
                    try:
                        self.statsReverse[entry[3]][currentLocation] += 1
                        #print(currentLocation,entry[3])
                    except:
                        #print('MEH')
                        self.statsReverse[entry[3]][currentLocation] = 1
                except:
                    self.statsReverse[entry[3]] = {currentLocation:1}

            else: #do work calculating edge stats
                currentMAC = entry[0]




            currentLocation = entry[3]

a=PopEstimation()
print(sorted(a.stats['166-223'].items(), key=lambda x: x[1]))
print(sorted(a.statsReverse['166-223'].items(), key=lambda x: x[1]))


o1=open('into.pkl','wb')
pickle.dump(a.stats, o1)
o1.close()

o1=open('out.pkl','wb')
pickle.dump(a.statsReverse, o1)
o1.close()



