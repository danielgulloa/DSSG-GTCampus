import os
import csv
os.chdir('C:\\Users\\Richard\\Google Drive\\DSSG-Wifi')
def parser(fn):
    ind=[0,2,3,7,9,13,15,17,19,21]
    fh=open(fn)
    final=[]
    lines=fh.readlines()
    for item in lines[1:]:
        if len(item)<3:
            break
        item=item[:-1].split(' ')
        temp=[]
        if item[1]=='':
            ind=[0,2,3,7,9,13,15,17,19,21]
        else:
            ind=[0,1,2,6,8,12,14,16,18,20]
        for i in ind:
            try:
                th=item[i].replace(',','')
                temp.append(th)
            except:
                print(item)
                return
        final.append(temp)
    fh.close()

    fh=open('log_parsed.csv','w',newline='')
    writer=csv.writer(fh)
    writer.writerows(final)
    fh.close()
parser('log.log')

