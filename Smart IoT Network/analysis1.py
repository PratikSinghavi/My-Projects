import numpy as np
import datetime as dt
import statistics as stat
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as md
from pylab import *
from tkinter import *

root = Tk()



tim = str(dt.datetime.now())
tim = tim[:10]
path = "/home/pi/logs/"+tim+"/"
path1 = path + "node1.txt"
path1 = str(path1)
print (path)

D=np.loadtxt(path1,delimiter="\t",usecols=[0],dtype=bytes).tolist()
Z= np.loadtxt(path1,delimiter="\t",usecols=[1],dtype='int').tolist()

#print (D)
#print (Z)

print ("max level: ")
maxlev = max(Z)
print (maxlev)
indmax = np.argmax(Z)

print ("Time max: ")
timemax= D[indmax][10:19]
print (timemax)

print ("min level: ")
minlev = (min(Z))
print (minlev)
indmin = np.argmin(Z)

print ("Time min: ")
timemin = D[indmin][10:19]
print (timemin)

print ("Mean")
mean1 = np.mean(Z)
print (mean1)
#print (mean(Z))


lbl1=Label(root,text="MAX LEVEL : ",font=("Arial",20,"bold"))
lbl1.grid(row=2,column=4,columnspan=2,sticky=W,pady=20,padx=20)

val1 = Text(root,width = 10 , height = 1, wrap = WORD,font=("Arial",20,"bold"))
val1.grid(row=2,column=7,columnspan=2,sticky=W,pady=10,padx=0)
val1.insert(0.0,maxlev)

lbl2=Label(root,text="TIME(MAX) : ",font=("Arial",20,"bold"))
lbl2.grid(row=4,column=4,columnspan=2,sticky=W,pady=20,padx=20)

val2 = Text(root,width = 10 , height = 1, wrap = WORD,font=("Arial",20,"bold"))
val2.grid(row=4,column=7,columnspan=2,sticky=W,pady=10,padx=0)
val2.insert(0.0,timemax)

lbl3=Label(root,text="MIN LEVEL : ",font=("Arial",20,"bold"))
lbl3.grid(row=6,column=4,columnspan=2,sticky=W,pady=20,padx=20)

val3 = Text(root,width = 10 , height = 1, wrap = WORD,font=("Arial",20,"bold"))
val3.grid(row=6,column=7,columnspan=2,sticky=W,pady=10,padx=0)
val3.insert(0.0,minlev)

lbl4=Label(root,text="TIME(MIN) : ",font=("Arial",20,"bold"))
lbl4.grid(row=8,column=4,columnspan=2,sticky=W,pady=20,padx=20)

val4 = Text(root,width = 10 , height = 1, wrap = WORD,font=("Arial",20,"bold"))
val4.grid(row=8,column=7,columnspan=2,sticky=W,pady=10,padx=0)
val4.insert(0.0,timemin)

lbl5=Label(root,text="MEAN LEVEL : ",font=("Arial",20,"bold"))
lbl5.grid(row=10,column=4,columnspan=2,sticky=W,pady=20,padx=20)

val5 = Text(root,width = 10 , height = 1, wrap = WORD,font=("Arial",20,"bold"))
val5.grid(row=10,column=7,columnspan=2,sticky=W,pady=10,padx=0)
val5.insert(0.0,mean1)




#root.mainloop()
root.title("ANALYSIS NODE 1")
root.geometry("400x400")
root.mainloop()
