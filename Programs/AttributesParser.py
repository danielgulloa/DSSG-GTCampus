import Methods

try:
	Methods.ConvertEstimationResultsToDB("EstimationResultsJanToJune.csv")
	print "Done doing DB"
	Methods.MakeAttributes_parsed()
	print "File attributes_parsed.csv has been created"
	
	#These are the months that we have available:
try:
	months={'Jan':31, 'Feb':28, 'Mar':31, 'Apr':30, 'May':31, 'Jun':30}
	hours=range(0,24)
	minutes=['00','05','10','15','20','25','30','35','40','45','50','55']
	

	g=open('StarbucksCountsJantoJun.csv','a')
	for m in sorted(months):
		d=1
		while d < months[m]:
			for h in hours:
				for min in minutes:
					count=Methods.countAtTime(m,str(d),str(h),str(min))
					g.write(m+', '+str(d)+', '+str(h)+', '+str(min)+', '+str(count)+"\n")
			d+=1
		print "finished month:"+ m
		
try:	
	for m in sorted(months):
		d=1
		while d < months[m]:
			Methods.StatsAtTime(m,str(d),'00:00:00','23:30:00',15)					
			os.system('cat Stats_'+m+str(d)+'_00:00:00_23:30:00.tsv >> Aux')
			os.system('rm Stats_'+m+str(d)+'_00:00:00_23:30:00.tsv')
			d+=1
except:
	print "Problem doing DB"
	






		


			
	








	






