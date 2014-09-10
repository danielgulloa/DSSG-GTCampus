import pickle

into = pickle.load(open("into.pkl", "rb"))

cols = []
vals = into.keys()

print "id," + ",".join(vals)

for val1 in vals:
	tmp = []
	for val2 in vals:
		if val2 in into[val1]:
			tmp.append(str(into[val1][val2]))
		else:
			tmp.append("0")

	print val1 + "," + ",".join(tmp)





