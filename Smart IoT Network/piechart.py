import numpy as np 
import datetime as dt
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as md
from pylab import *

tim = str(dt.datetime.now())
tim = tim[:10]
path = "/home/pi/logs/"+tim+"/"
path1 = path + "node1.txt"
path2 = path + "node2.txt"
path3 = path + "node3.txt"
path3 = str(path3)
path2 = str(path2)
path1 = str(path1)
print (path)

D=np.loadtxt(path1,delimiter="\t",usecols=[0],dtype=bytes).tolist()
Z= np.loadtxt(path1,delimiter="\t",usecols=[1],dtype='int').tolist()

D1=np.loadtxt(path2,delimiter="\t",usecols=[0],dtype=bytes).tolist()
Z1= np.loadtxt(path2,delimiter="\t",usecols=[1],dtype='int').tolist()

D2=np.loadtxt(path3,delimiter="\t",usecols=[0],dtype=bytes).tolist()
Z2= np.loadtxt(path3,delimiter="\t",usecols=[1],dtype='int').tolist()

print ("Mean 1")
mean1 = np.mean(Z)
print (mean1)

print ("Mean 2")
mean2 = np.mean(Z1)
print (mean2)

print ("Mean 3")
mean3 = np.mean(Z2)
print (mean3)

labels= 'Node 1','Node 2','Node 3'
sizes = [mean1,mean2,mean3]
colors= ['gold','yellowgreen','lightcoral']

explode = (0.1,0,0)

plt.pie(sizes,explode=explode,labels=labels,shadow=True,colors=colors,autopct='%1.1f%%',startangle=180)
plt.title("Comparison by Mean Content Levels")
#plt.legend(patches,labels,loc="best")
plt.axis('equal')
plt.show()
