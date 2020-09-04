import numpy as np
import datetime as dt
import statistics as stat
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as md
from pylab import *
from tkinter import *
import math 
import sys

flagged = []
flagged1= []
offsets=[]
fincost=0

root = Tk()


#print 'Number of arguments:', len(sys.argv), 'arguments.'
for i in range(1,len(sys.argv)):
	flagged.append(int(sys.argv[i]))

for i in range(0,len(flagged)):
	if flagged[i]==1:
		flagged1.append(i)
#flagged.sort()
print (flagged1)

locations1 = [[0.0,0.0],
                [40.71,  -74.01], # Node 1
                [34.05, -118.24], # Node 2
                [41.88,  -87.63],] # Node 3 
locations=[]
tlen = len(flagged)

for i in range(0,tlen):
	temp = flagged[i]
	if temp==1:
                locations.append(locations1[i])
print (locations)

size = len(locations)
matrix={}

	

# Distance function
def distance(x1, y1, x2, y2):
	sq1 = (x1-x2)*(x1-x2)
	sq2 = (y1-y2)*(y1-y2)
	return math.sqrt(sq1 + sq2)

def creatematrix():

	for from_node in range(size):
		matrix[from_node] = {}
		for to_node in range(size):
			if from_node == to_node:
				matrix[from_node][to_node] = 0
			else:
				x1 = locations[from_node][0]
				y1 = locations[from_node][1]
				x2 = locations[to_node][0]
				y2 = locations[to_node][1]
				matrix[from_node][to_node] = distance(x1, y1, x2, y2)


def Printmat():
	print (matrix)

def dijkstra(matrix,m,n):
    k=0
    global fincost
    cost=[[0 for x in range(m)] for x in range(1)]
    global offsets 
    offsets.append(k)
    elepos=0
    for j in range(m):
        cost[0][j]=matrix[k][j]
    mini=999
    for x in range (m-1):
        mini=999
        for j in range (m):
                if cost[0][j]<=mini and j not in offsets:
                        mini=cost[0][j]
                        elepos=j
        fincost = fincost + mini
        offsets.append(elepos)
        for j in range (m):
            if cost[0][j] >cost[0][elepos]+matrix[elepos][j]:
                cost[0][j]=cost[0][elepos]+matrix[elepos][j]
		
    print ("The shortest path is")
    for y in range(len(offsets)):
    	print (flagged1[offsets[y]])
    print ("The Total Distance:",fincost)

creatematrix()
Printmat()
dijkstra(matrix,len(locations),len(locations))

z = 4

lbl1=Label(root,text="Shortest Path For Efficient Collection : ",font=("Arial",20,"bold"))
lbl1.grid(row=2,column=4,columnspan=2,sticky=W,pady=20,padx=20)

if len(offsets)>=1:
    lbl2=Label(root,text="    Node "+str(flagged1[offsets[0]]),font=("Arial",20,"bold"))
    lbl2.grid(row=z,column=4,columnspan=2,sticky=W,pady=20,padx=20)
    z=z+2
   
if len(offsets)>=2:
    lbl3=Label(root,text=" -> Node "+str(flagged1[offsets[1]]),font=("Arial",20,"bold"))
    lbl3.grid(row=z,column=4,columnspan=2,sticky=W,pady=20,padx=20)
    z=z+2    

if len(offsets)>=3:
    lbl4=Label(root,text=" -> Node "+str(flagged1[offsets[2]]),font=("Arial",20,"bold"))
    lbl4.grid(row=z,column=4,columnspan=2,sticky=W,pady=20,padx=20)
    z=z+2
    
if len(offsets)>=4:
    lbl5=Label(root,text=" -> Node "+str(flagged1[offsets[3]]),font=("Arial",20,"bold"))
    lbl5.grid(row=z,column=4,columnspan=2,sticky=W,pady=20,padx=20)
    z=z+2

lbl6=Label(root,text="Total Distance: "+str(fincost),font=("Arial",20,"bold"))
lbl6.grid(row=z,column=4,columnspan=2,sticky=W,pady=20,padx=20)


root.title("Shortest Path")
root.geometry("400x400")
root.mainloop()

