import csv
fh=open('attributes.txt')
#0:31
lines=fh.readlines()
final={}
for line in lines:
    if "Primary" in line:
        year=""

        if "faculty" in line[:52]:
            affliation="faculty"
        elif "staff" in line[:52]:
            affliation="staff"
        elif "student" in line[:52]:
            affliation="student"
            if "freshman" in line:
                year="freshman"
            elif "sophomore" in line:
                year="sophomore"
            elif "junior" in line:
                year="junior"
            elif "senior" in line:
                year="senior"
            elif "masters" in line:
                year="masters"
            elif "doctorate" in line:
                year="doctorate"
            else:
                year="unknown"
        else:
            affliation="other"
        final[line[:32]]=[affliation,year]
fh.close()
fh=open('EstimationResultsFallWithDuration.csv')
reader=csv.reader(fh)
c=0
lines=[['ID','Month','Day','Enter','Exit','Duration','Affiliation','Year']]
for item in reader:
    try:
        lines.append(item+final[item[0]])
    except:
        c+=1
print(c)
fh.close()
fh=open('EstimationWithAfflication.csv','w',newline='')
writer=csv.writer(fh)
writer.writerows(lines)
fh.close()


##fh=open("attributeParsed.csv",'w',newline='')
##writer=csv.writer(fh)
##writer.writerows(final)
##fh.close()
