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

D=np.loadtxt(path1,delimiter="\t",usecols=[0],dtype=bytes)
Z= np.loadtxt(path1,delimiter="\t",usecols=[1],dtype='int')

D1=np.loadtxt(path2,delimiter="\t",usecols=[0],dtype=bytes)
Z1= np.loadtxt(path2,delimiter="\t",usecols=[1],dtype='int')

D2=np.loadtxt(path3,delimiter="\t",usecols=[0],dtype=bytes)
Z2= np.loadtxt(path3,delimiter="\t",usecols=[1],dtype='int')


print (D)
print (Z)
Dates = [dt.datetime.strptime(d.decode('ascii')[:19],'%Y-%m-%d %H:%M:%S') for d in D]
Dates1 = [dt.datetime.strptime(d1.decode('ascii')[:19],'%Y-%m-%d %H:%M:%S') for d1 in D1]
Dates2 = [dt.datetime.strptime(d2.decode('ascii')[:19],'%Y-%m-%d %H:%M:%S') for d2 in D2]

plt.grid()

plt.plot(Dates,Z,'o-',label='Content 1')
plt.plot(Dates1,Z1,'o-',label='Content 2')
plt.plot(Dates2,Z2,'o-',label='Content 3')
plt.legend(loc=1)
plt.xlabel(Dates[1].strftime('%Y-%m-%d'))
plt.gcf().autofmt_xdate()
plt.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%H:%M:%S"))
plt.gca().set_ylim([0.0,50.0])
plt.gcf().suptitle("Waste Monitoring Graph")

plt.show()
