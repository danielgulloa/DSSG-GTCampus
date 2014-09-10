import csv, sqlite3, time, datetime,os
#------------------------------------------------
def addZero(str_number):
	if int(str_number)<10:
		str_number='0'+str_number
	return str_number

# ---------------------------------------
def countNewVsStayingAtTime(month='Jun',day='10',hour='10',minute='00'):
	from datetime import timedelta
	conector=sqlite3.connect('TimesEntryExit.db')

	year=2013

	month_dict = {"Jan":1,"Feb":2,"Mar":3,"Apr":4, "May":5, "Jun":6, "Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}
	newcomerCurrent=datetime.datetime(year,month_dict[month],int(day),int(hour),int(minute)) 
	d=timedelta(minutes=5)
	newcomerEntry=newcomerCurrent-d
	
	currenthour=addZero(str(newcomerCurrent.hour))
	currentmin=addZero(str(newcomerCurrent.minute))
	currentsec=addZero(str(newcomerCurrent.second))
	newhour=addZero(str(newcomerEntry.hour))
	newmin=addZero(str(newcomerEntry.minute))
	newsec=addZero(str(newcomerEntry.second))
	


	query='SELECT DISTINCT * FROM mytable WHERE month = \'' + month +  '\' AND day = \''+day+'\' AND timeEntry > \''+newhour+':'+newmin+':'+newsec+'\' AND timeEntry <= \''+currenthour+':'+currentmin+':'+currentsec+'\''
	con=conector.cursor()
        con.execute(query)
        data=con.fetchall()      
        newones= len(data)
	total=countAtTime(month,day,hour,minute)
	return newones,(total-newones),total






#-------------------------------------------------------
def ConvertEstimationResultsToDB(input_file):
	t = time.time()
	os.system("rm TimesEntryExit.db")
	conn = sqlite3.connect( "TimesEntryExit.db" )
	conn.text_factory = str  #bugger 8-bit bytestrings
	cur = conn.cursor()
	cur.execute('CREATE TABLE IF NOT EXISTS mytable (userID VARCHAR, month VARCHAR, day VARCHAR, timeEntry VARCHAR, timeExit VARCHAR)')
	csvData = csv.reader(open(input_file, "rb"))
	for field1,field2,field3,field4,field5 in csvData:    
		cur.execute('INSERT OR IGNORE INTO mytable (userID, month,day,timeEntry,timeExit) VALUES (?,?,?,?,?)', (field1, field2, field3,field4, field5))
	conn.commit()


#-------------------------------------------------------
def countAtTime(month='Jun',day='10',hour='10',minute='00',seconds='00'):
	conector=sqlite3.connect('TimesEntryExit.db')	
	if int(hour)<10:
		hour='0'+hour
	
	query='SELECT DISTINCT * FROM mytable WHERE month = \''+month+'\' AND day = \''+day+'\' AND timeEntry < \''+hour+':'+minute+':'+seconds+'\' AND timeExit > \''+hour+':'+minute+':'+seconds+'\''
	con=conector.cursor()
	con.execute(query)
	data=con.fetchall()
	#print "Date: "+month+" "+day+", Time: "+hour+":"+minute+":"+seconds+" Count: "+str(len(data))
	return len(data)


#-------------------------------------------------------	
def StatsAtTime(month='Jun',day='10',init_time='09:00:00',final_time='12:00:00',lapse=5):
	from datetime import timedelta
	from datetime import datetime
	month_dict = {"Jan":1,"Feb":2,"Mar":3,"Apr":4, "May":5, "Jun":6, "Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}
	d=timedelta(0,60*lapse)
	t=init_time.split(":")
	start=datetime(2014,month_dict[month],int(day),int(t[0]), int(t[1]))
	t=final_time.split(":")
	end=datetime(2014,month_dict[month],int(day),int(t[0]), int(t[1]))
	current=start
	Matrix={}
	allMajors=[]
	while current<end:
		Prim,Type,Year,Major=typeAtTime(month,day,str(current.hour),str(current.min))
		date=str(current)
		Matrix[date]={}
		for key in Prim.keys():
			Matrix[date][key]=Prim[key]
		for key in Type.keys():
			Matrix[date][key]=Type[key]
		for key in Year.keys():
			Matrix[date][key]=Year[key]
		for key in Major.keys():
			Matrix[date][key]=Major[key]
			allMajors.append(key)
			allMajors=list(set(allMajors))		
		current+=d
	try:
		os.system('rm Stats_'+month+day+'_'+init_time+'_'+final_time+'.tsv')
	except:
		print "No file"
	g=open('Stats_'+month+day+'_'+init_time+'_'+final_time+'.tsv','a')
	g.write('table\t')
	XAxis=Prim.keys()+Type.keys()+Year.keys()+allMajors
	for element in XAxis:
		g.write(element+"\t")
	g.write("\n")
	for timestamp in sorted(Matrix.keys()):
		g.write(timestamp+"\t")
		for element in XAxis:
			if element in Matrix[timestamp]:
				g.write(str(Matrix[timestamp][element])+"\t")
			else:
				g.write("0\t")
		g.write("\n")
	g.close()

#---------------------------------------------------------------------
def typeAtTime(month='Jun',day='10',hour='10',minute='00',seconds='00'):
	if int(hour)<10:
		hour='0'+hour
		
	conector=sqlite3.connect('TimesEntryExit.db')	
	query='SELECT DISTINCT * FROM mytable WHERE month = \''+month+'\' AND day = \''+day+'\' AND timeEntry < \''+hour+':'+minute+':'+seconds+'\' AND timeExit > \''+hour+':'+minute+':'+seconds+'\''
	con=conector.cursor()
	con.execute(query)
	data=con.fetchall()
	
	f=open('attributes_parsed.csv','r')
	attributes=f.readlines()
	
	
	allUsers=[]
	for i in range(0,len(attributes)):
		allUsers.append(attributes[i].split(",")[0])
	
	
	Primary={"student": 0, "faculty": 0, "employee": 0, "staff": 0, "affiliate": 0, "guest": 0, "member": 0}
	Student_Type={"undergrad-student": 0, "masters-student": 0, "doctorate-student": 0}
	Student_Year={"freshman-student": 0, "sophomore-student": 0, "junior-student": 0, "senior-student": 0}
	Student_Major={}
	import re
	
	for i in range(0,len(data)):
		user = data[i][0].encode('ascii').replace(",","")
		ind=allUsers.index(user)
		List=attributes[ind].split(", ")
		if List[1] in Primary.keys():
			Primary[List[1]]+=1
		else: #i.e. if it finds something that is not student, faculty, etc...
			Primary[List[1]]=1
		if List[1]=='student':
			for key in Student_Type.keys():
				if key in List[3]:
					Student_Type[key]+=1
			for key in Student_Year.keys():
				if key in List[2]:				
					Student_Year[key]+=1
			lookFor=',student@'
			if lookFor in List[3]:
				starts = [match.start() for match in re.finditer(re.escape(lookFor), attributes[ind])]
				starts=[x+len(lookFor) for x in starts]
				for s in starts:
					try:
						ends=attributes[ind][s:].index(",")+s
					except:
						ends=attributes[ind][s:].index("\\")+s
					k = attributes[ind][s:ends]
					if k in Student_Major.keys():
						Student_Major[k]+=1
					else:
						Student_Major[k]=1
	return Primary, Student_Type, Student_Year, Student_Major
	
	
	
# -----  Parser. Makes attributes_parsed.csv  -------------
def MakeAttributes_parsed():
	os.system("rm attributes_parsed.csv")
	f = open('../RawData/attributes.txt','r')
	f.readline() #Get rid of the first line

	g=open('attributes_parsed.csv','a')
	for line in f:
		List=line.split("|")
		user=List[0]
		try:
			primary=List[1].split(":")[1]
			all=List[2].split(":")[1]		
			scope=List[3].split(":")[1:]
		except:
			primary=''
			all=''
			scope=''
		g.write(user+", "+primary+", "+str(all)+", "+str(scope)+"\n")


	f.close()
	g.close()



#---------------------------------------------------------
def getAllAndScoped():
	f = open('../RawData/attributes.txt','r')
	f.readline() #Get rid of the first line

	#Get features for All and Scoped
	All=[]
	Scoped=[]
	for line in f:	
		try:
			List=line.split("|")
			tmp_all=List[2].split(":")[1].split(",")
			All=list(set(tmp_all+All))
		except:	
			print line
		
		try:	
			scoped_tmp=List[-1].split(":")[1].split(",")
			Scoped=list(set(scoped_tmp+Scoped))
		except:
			print line

	f.close()
	return All,Scoped

