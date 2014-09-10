import pickle
o1=open('into.pkl','rb')
into=pickle.load(o1)
o1.close()
print(into['166-233'])