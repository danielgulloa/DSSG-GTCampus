import Methods
import datetime
import time
from datetime import datetime

initialY=2013
initialM=8 #Aug
initialD=1
initialT=0
finalY=2013
finalM=12 #Dec
finalD=31
finalT=23


lapse = 5
from datetime import timedelta
d=timedelta(0,60*lapse)
initialdate=datetime(initialY,initialM,initialD)
finaldate=datetime(finalY,finalM,finalD,finalT,59)



monthdict={1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
current=initialdate
g=open('StarbucksCountsFall.csv','a')
while(current<=finaldate):
	c= Methods.countAtTime(monthdict[current.month],str(current.day),str(current.hour),str(current.minute))
	g.write(str(current)+", "+str(c)+"\n")
	current+=timedelta(0,60*lapse)
g.close()



