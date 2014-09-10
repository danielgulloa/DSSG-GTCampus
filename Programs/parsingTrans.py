from datetime import datetime
from datetime import timedelta

import csv, os

os.chdir("/Users/Daniel/Desktop")

with open("starbucks_transactions_fall_2013_spring_2014_no_charge_data.csv", "r") as csvfile:
	reader = csv.reader(csvfile, delimiter=",")
	next(reader, None) #skip header

	count = 0

	window = datetime(2013,8,1,0,0,0)
	delta = timedelta(minutes=5)

	for row in reader:
		time = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.000')

		while(time > window + delta):
			print str(window+delta) + " " + str(count)
			window = window + delta
			count = 0
			
		count += int(row[3])

		#minutes = timedelta(minutes=5)
		