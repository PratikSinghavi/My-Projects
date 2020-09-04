import serial
import matplotlib 
import os,sys
from tkinter import * 
from datetime import datetime 
ser=serial.Serial("/dev/ttyAMA0") # the only stupid port that rasPi has
ser.baudrate = 9600 	 
ser.stopbits = serial.STOPBITS_ONE
ser.bytesize=serial.EIGHTBITS

os.system("sudo hwclock --hctosys")
dtch = input("Do you wish to change the date? (y/n)")

if dtch=='y' or dtch=='Y':
	dtt = input("Enter Date (YYYY-MM-DD) ")
	tms = input("Enter TIme (HH:MM::SS)")
	
	dtt = str(dtt)
	tms = str(tms)
	
	os.system("sudo date --set "+dtt)
	os.system("sudo date --set "+tms)


global getdata
getdata=0

global data1,data2
temp1=''
temp2=''
f0=1 #origin position
f1=0
f2=0
f3=0

matchstr1 = "A\r\n"
matchstr2 = "B\r\n"
matchstr3=  "C\r\n"
matchstr4=  "D\r\n"

flag1=0
flag2=0
flag3=0
flag4=0

tim = str(datetime.now())
tim = tim [:10]

path="/home/pi/logs/"+tim

os.system("mkdir "+path)

t1 = open(path+"/node1.txt",'a') # append
t2 = open(path+"/node2.txt",'a')
t3 = open(path+"/node3.txt",'a')
t4 = open(path+"/node4.txt",'a')

class Application(Frame):
	def __init__(self,master):
		Frame.__init__(self,master)
		self.grid()
		self.button_clicks=0
		self.createwidgets()

	def createwidgets(self):
		self.startstopbutton= Button(self,text = "Start\t ",command=self.action,font=("Arial",13,"bold"))
		self.startstopbutton.grid(row=15,column=6,columnspan=2,sticky=W,pady=10,padx=40)
		#self.startstopbutton.pack()
		self.stopbutton= Button(self,text = "Stop\t ",command=self.stopaction,font=("Arial",13,"bold"))
		self.stopbutton.grid(row=15,column=7,columnspan=2,sticky=W,pady=10,padx=0)
                
		self.tgraphbutton= Button(self,text = "Data\nGraph",command=self.tgraphaction,bg="red",font=("Arial",13,"bold"))
		self.tgraphbutton.grid(row=17,column=6,columnspan=2,sticky=W,pady=10,padx=40,ipadx=20)

		self.hgraphbutton= Button(self,text = "Shortest\nPath",command=self.shortestpath,bg="orange",font=("Arial",13,"bold"))
		self.hgraphbutton.grid(row=17,column=7,columnspan=2,sticky=W,pady=10,padx=0,ipadx=10)

		self.pgraphbutton= Button(self,text = "Pie\nChart",command=self.piedraw,bg="green",font=("Arial",13,"bold"))
		self.pgraphbutton.grid(row=17,column=9,columnspan=2,sticky=W,pady=10,padx=20,ipadx=20)

		templbl = Label(self,text="Waste Level\n(cms)",font=("Arial",14,"bold"))
		templbl.grid(sticky=W,pady=40,padx=40,column=6,row=7)
		humlbl = Label(self,text="Flagged",font=("Arial",14,"bold"))
		humlbl.grid(sticky=W,pady=0,padx=10,column=7,row=7,columnspan=2)
		 
		node1lbl = Label(self,text="Node 1",font=("Arial",14,"bold"))
		node1lbl.grid(row=8,column=4,columnspan=2,sticky=W,pady=10,padx=20)
		node2lbl = Label(self,text="Node 2",font=("Arial",14,"bold"))
		node2lbl.grid(row=10,column=4,columnspan=2,sticky=W,pady=10,padx=20)
		node3lbl = Label(self,text="Node 3",font=("Arial",14,"bold"))
		node3lbl.grid(row=12,column=4,columnspan=2,sticky=W,pady=10,padx=20)
		

		self.temp1 = Text(self,width = 10 , height = 1, wrap = WORD,font=("Arial",13,"bold"))
		self.temp1.grid(row=8,column=6,columnspan=2,sticky=W,pady=20,padx=40)
		self.temp1.insert(0.0,"Data 1\t ")

		self.temp2 = Text(self,width = 10 , height = 1, wrap = WORD,font=("Arial",13,"bold"))
		self.temp2.grid(row=10,column=6,columnspan=2,sticky=W,pady=20,padx=40)
		self.temp2.insert(0.0,"Data 2\t ")

		self.temp3 = Text(self,width = 10 , height = 1, wrap = WORD,font=("Arial",13,"bold"))
		self.temp3.grid(row=12,column=6,columnspan=2,sticky=W,pady=20,padx=40)
		self.temp3.insert(0.0,"Data 3\t ")

		self.hum1 = Text(self,width = 10 , height = 1, wrap = WORD,font=("Arial",13,"bold"))
		self.hum1.grid(row=8,column=7,columnspan=2,sticky=W,pady=10,padx=0)
		self.hum1.insert(0.0,"Flag Status\t ")

		self.hum2 = Text(self,width = 10 , height = 1, wrap = WORD,font=("Arial",13,"bold"))
		self.hum2.grid(row=10,column=7,columnspan=2,sticky=W,pady=10,padx=0)
		self.hum2.insert(0.0,"Flag Status\t ")

		self.hum3 = Text(self,width = 10 , height = 1, wrap = WORD,font=("Arial",13,"bold"))
		self.hum3.grid(row=12,column=7,columnspan=2,sticky=W,pady=10,padx=0)
		self.hum3.insert(0.0,"Flag Status\t ")

		self.r1button= Button(self,text = "Analysis 1",command=self.analysis1,bg="yellow",font=("Arial",13,"bold"))
		self.r1button.grid(row=8,column=9,columnspan=2,sticky=W,pady=10,padx=20,ipadx=10)		

		self.r2button= Button(self,text = "Analysis 2",command=self.analysis2,bg="yellow",font=("Arial",13,"bold"))
		self.r2button.grid(row=10,column=9,columnspan=2,sticky=W,pady=10,padx=20,ipadx=10)

		self.r3button= Button(self,text = "Analysis 3",command=self.analysis3,bg="yellow",font=("Arial",13,"bold"))
		self.r3button.grid(row=12,column=9,columnspan=2,sticky=W,pady=10,padx=20,ipadx=10)
	def action(self):
		global getdata
		getdata=1
		#self.temp1.insert(0.0,humw1)

	def stopaction(self):
		global getdata
		getdata=0
	
	def tgraphaction(self):
		os.system("python3.4 tempgraph.py")
		getdata=0
	
	def shortestpath(self):
		print (f0)
		print (f1)
		print (f2)
		print (f3)
		os.system("python3.4 shortestpath.py"+" "+str(f0)+" "+str(f1)+" "+str(f2)+" "+str(f3))
		getdata=0

	def analysis1(self):
		os.system("python3.4 analysis1.py")
		getdata=0	

	def analysis2(self):
		os.system("python3.4 analysis2.py")
		getdata=0

	def analysis3(self):
		os.system("python3.4 analysis3.py")
		getdata=0		

	def piedraw(self):
		os.system("python3.4 piechart.py")
		getdata=0		


root = Tk()
root.title("Sensor Network Monitor")
root.geometry("550x500")

app = Application(root)


def oldf():
	global flag1,flag2,flag3,flag4,getdata
	global temp1,temp2,humw1,hum2
	global f1,f2,f3,f4
	#print (getdata)
	if getdata==1:

		t1 = open(path+"/node1.txt",'a') # append
		t2 = open(path+"/node2.txt",'a')
		t3 = open(path+"/node3.txt",'a')
		t4 = open(path+"/node4.txt",'a')		

		data=ser.readline()
		data1 = data.decode('utf-8')
	
	#	print(data)
		
		if data1==matchstr1:
			data=ser.readline()
			content1=data.decode('utf-8')
			content1pc=((50-int(content1))/50)*100
			if content1pc > 60:
				app.hum1.insert(0.0,'YES\n')
				f1=1
			else:
				app.hum1.insert(0.0,'NO\n')
				f1=0
			#print (data2) # parantheses neccessary here
			flag1=1
		if flag1==1:
			#break
			print ("Data 1:")
			print (content1)
			temper1=47-int(content1)
			app.temp1.insert(0.0,str(temper1)+".00        ")
			tim = str(datetime.now())
			t1.write(tim+"\t"+str(temper1)+"\n")	
			flag1=0
	
		if data1==matchstr2:
			data=ser.readline()
			content2=data.decode('utf-8')
			content2pc=((50-int(content2))/50)*100
			if content2pc> 60:
				app.hum2.insert(0.0,'YES\n')
				f2=1
			else:
				app.hum2.insert(0.0,'NO\n')
				f2=0
			#print data2
			flag2=1
		if flag2==1:
			#break
			print ("Data 2:")
			print (content2)
			temper2=47-int(content2)
			app.temp2.insert(0.0,str(temper2)+".00        ")
			tim = str(datetime.now())
			t2.write(tim+"\t"+str(temper2)+"\n")	
			flag2=0

		if data1==matchstr3:
			data=ser.readline()
			content3=data.decode('utf-8')
			content3pc=((50-int(content3))/50)*100
			if content3pc> 60:
				app.hum3.insert(0.0,'YES\n')
				f3=1
			else:
				app.hum3.insert(0.0,'NO\n')
				f3=0
			#print data2
			flag3=1
		if flag3==1:
			#break
			print ("Data 3:")
			print (content3)
			temper3=47-int(content3)
			app.temp3.insert(0.0,str(temper3)+".00        ")
			tim = str(datetime.now())
			t3.write(tim+"\t"+str(temper3)+"\n")	
			flag3=0	


# FLAG STATUS BOX
		
		


		

		t1.close()
		t2.close()
		t3.close()
		t4.close()
	root.after(500,oldf)
		
	#root.update()




#root.mainloop()
	
#t1.write("Time \t\t\t\tTemp1\t\n")
#t2.write("Time \t\t\t\tTemp2\t\n")
#h1.write("Time \t\t\t\tHumid1\t\n")
#h2.write("Time \t\t\t\tHumid2\t\n")


#while True:

root.after(0,oldf)
root.mainloop()

#ser.close
