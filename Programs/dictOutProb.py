import pickle

into = pickle.load(open("into.pkl", "rb"))

cols = []
vals = into.keys()

print "id," + ",".join(vals)

for val1 in vals:
	tmp = []
	total = 0.0
	for val2 in vals:
		if val2 in into[val1]:
			tmp.append(into[val1][val2])
			total += into[val1][val2]
		else:
			tmp.append(0)

	  

	print val1 + "," + ",".join(map(lambda x: str(x/total), tmp)) #scale all elements by total sum





