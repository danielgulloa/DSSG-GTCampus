import os
import datetime
import csv
import sqlite3

#os.chdir('C:\\Users\\Richard\\Google Drive\\DSSG-Wifi\\Starbucks population estimation')

class PopEstimation():
    def __init__(self):
        self.sqliteconnect()
        months=['10']
        for month in months:
            self.selectRecord(month)
            self.calculate()
            self.writeToCSV('EstimationResultsFall.csv')
            print(month + " imported!")
        pass

    def sqliteconnect(self):
        self.con=sqlite3.connect('SampleDBFall.db')

    def selectRecord(self,month):
        sql="SELECT month, day, time, userID, router FROM month"+month+" ORDER BY userID ASC, month ASC, day ASC, time ASC "
        c=self.con.cursor()
        c.execute(sql)
        self.data=c.fetchall()
        print('Done with selecting!'+str(len(self.data))+' rows selected')

    def calculate(self, st=100, field=['223','208','125','325','226','323']):
        user=self.data[0][3]
        month=self.data[0][0]
        day=self.data[0][1]
        time=self.data[0][2]
        self.DataDict={}
        T=[]
        for item in self.data:
            try:
                self.DataDict[item[3]]
            except:
                self.DataDict[item[3]]=[]
            if user==item[3]:
                if month==item[0] and day==item[1]:
                    location=item[-1][4:7]
                    if location in field:
                        T.append(item[2])
                        ###check the duration!!!!!
                        if len(T)>1:
                            T1=datetime.datetime(2014,1,1,int(T[-2][:2]),int(T[-2][3:5]),int(T[-2][6:8]))
                            T2=datetime.datetime(2014,1,1,int(T[-1][:2]),int(T[-1][3:5]),int(T[-1][6:8]))
                            dur=(T2-T1).total_seconds()
                            if dur>60*45:
                                try:
                                    self.DataDict[user].append([item[0], item[1],T[0],T[-2]])
                                except:
                                    pass
                                T=[]

                        continue
                    else:
                        if len(T)>1:
                            T1=datetime.datetime(2014,1,1,int(T[0][:2]),int(T[0][3:5]),int(T[0][6:8]))
                            T2=datetime.datetime(2014,1,1,int(T[-1][:2]),int(T[-1][3:5]),int(T[-1][6:8]))
                            dur=(T2-T1).total_seconds()
                            if T[0]!=T[-1] and dur>st:
                                self.DataDict[user].append([item[0], item[1],T[0],T[-1]])
                        T=[]

                else:
                    if len(T)>1:
                        T1=datetime.datetime(2014,1,1,int(T[0][:2]),int(T[0][3:5]),int(T[0][6:8]))
                        T2=datetime.datetime(2014,1,1,int(T[-1][:2]),int(T[-1][3:5]),int(T[-1][6:8]))
                        dur=(T2-T1).total_seconds()
                        if T[0]!=T[-1] and dur>st:
                            self.DataDict[user].append([item[0], item[1],T[0],T[-1]])
                    T=[]
                    day=item[1]
                    month=item[0]
            else:###
                if len(T)>0:
                    T1=datetime.datetime(2014,1,1,int(T[0][:2]),int(T[0][3:5]),int(T[0][6:8]))
                    T2=datetime.datetime(2014,1,1,int(T[-1][:2]),int(T[-1][3:5]),int(T[-1][6:8]))
                    dur=(T2-T1).total_seconds()
                    if T[0]!=T[-1] and dur>st:
                        self.DataDict[user].append([month, day,T[0],T[-1]])
                T=[]
                day=item[1]
                month=item[0]
                user=item[3]



    def writeToCSV(self,fn):
        try:
            fh=open(fn,'a', newline='')
        except:
            fh=open(fn,'w', newline='')
        writer=csv.writer(fh)
        final=[]
        for key in self.DataDict:
            for value in self.DataDict[key]:
                final.append([key]+value)
        writer.writerows(final)
        fh.close()








a=PopEstimation()