import csv
fh=open("StayersFall.csv")
reader=csv.reader(fh)
final=[['Datetime','HourMin','Tot','T5','T10','T15','T20','T25','T30','T35','T40','T45','T50','T55','T60','Rest']]
for item in reader:
    #print(item)
    rest=int(item[1])-int(item[-1])
    temp=item[2]
    hour=item[0][11:13]
    Min=item[0][14:16]
    tempList=[item[2]]
    for j in item[3:]:
        tempList.append(int(j)-int(temp))
        temp=j
    if Min=='00' or Min == '30':
        final.append([item[0],hour+':'+Min,item[1]]+tempList+[rest])
fh.close()
fh=open('StayerFallParsed(0030).csv','w',newline='')
writer=csv.writer(fh)
writer.writerows(final)
fh.close()