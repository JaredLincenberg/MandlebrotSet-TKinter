"""
By: Jared Lincenberg

Mandelbrot Set 
Create Project: 2017
Computer Science 101 - D
"""
from tkinter import *
from PIL import Image, ImageTk    
from numba import jit
import numpy as np
from turtle import *
import time
import datetime
from tkinter import simpledialog, Listbox
import tkinter as tk
import math

class Window(Frame):

	def __init__ (self, master=None):
		Frame.__init__(self,master)
		self.master = master
		self.pack()
		
		#Build Window
		self.init_window()
		

	def init_window(self):
		self.master.title("Create Project 2017: MandelbrotSet")
		self.pack(fill=BOTH, expand=1)
		#Set UP
		optionsFrame= LabelFrame(root)
		optionsFrame.pack(side=LEFT)
		

		self.xmin=StringVar(self, value='-2')
		self.xmax=StringVar(self, value='1')
		self.ymin=StringVar(self, value='-1.5')
		self.ymax=StringVar(self, value='1.5')
		self.iTmax=StringVar(self, value='1000')
		self.cRpoint=StringVar(self,value=-0.5)
		self.cIpoint=StringVar(self, value=-0.5)

		xminLb=Label(optionsFrame,text="Smallest X")
		xmaxLb=Label(optionsFrame,text="Largest X")
		xminEn=Entry(optionsFrame,textvariable=self.xmin)
		xmaxEn=Entry(optionsFrame,textvariable=self.xmax)
		yminLb=Label(optionsFrame,text="Smallest Y")
		ymaxLb=Label(optionsFrame,text="Largest Y")
		yminEn=Entry(optionsFrame,textvariable=self.ymin)
		ymaxEn=Entry(optionsFrame,textvariable=self.ymax)
		iTmaxLb=Label(optionsFrame,text="Max Iteration")
		iTmaxEn=Entry(optionsFrame,textvariable=self.iTmax)
		cRpointLb=Label(optionsFrame,text="Real part")
		cRpointEn=Entry(optionsFrame,textvariable=self.cRpoint)
		cIpointLb=Label(optionsFrame,text="Imaginary part")
		cIpointEn=Entry(optionsFrame,textvariable=self.cIpoint)

		#Lay Out
		xminLb.grid(row=0, column=0)
		xminEn.grid(row=0, column=1)
		xmaxLb.grid(row=1, column=0)
		xmaxEn.grid(row=1, column=1)
		yminLb.grid(row=2, column=0)
		yminEn.grid(row=2, column=1)
		ymaxLb.grid(row=3, column=0)
		ymaxEn.grid(row=3, column=1)
		iTmaxLb.grid(row=4, column=0)
		iTmaxEn.grid(row=4, column=1)
		
		cRpointLb.grid(row=6,column=0)
		cRpointEn.grid(row=6,column=1)
		cIpointLb.grid(row=7,column=0)
		cIpointEn.grid(row=7,column=1)
		canvasFrame= LabelFrame(root)
		canvasFrame.pack(side=RIGHT)
		
		#Canvas and Function Buttons
		self.canvasImage=Canvas(canvasFrame,width=500,height=500,bg="black")
		self.canvasImage.grid(columnspan=3, sticky=NW)
		RunButton = Button(canvasFrame, text="Run",command=self.clickRun)
		RunButton.grid(row=1, column=0)
		#Saves 2000x2000 image with parameters and time stamp
		SaveButtonImage = Button(canvasFrame, text="Save Image",command=lambda: self.clickSaveImage())
		SaveButtonImage.grid(row=1,column=1)
		#Saves x and y bounds and max iterations
		SaveButtonPar = Button(canvasFrame, text="Save Parameters",command=lambda: self.clickSavePar())
		SaveButtonPar.grid(row=1,column=2)
		#Creates canvas uses turtle to draw path of a point through the iterations of the Mandlebrot set
		self.hasTrace=False
		TraceButton = Button(canvasFrame, text="Trace", command=lambda: self.clickTrace())
		TraceButton.grid(row=2,column=0)
		#Save the point that is input to be traced
		SaveButtonPoint = Button(canvasFrame, text="Save Points",
			command=lambda: self.clickSavePoint())
		SaveButtonPoint.grid(row=2,column=1)
		#Load both saved parameters and point updates input, does not run
		LoadButton = Button(canvasFrame, text="Load", command= self.loadInfo)
		LoadButton.grid(row=2, column=2)

		#Old code for Menu bar
		menu = Menu(self.master)
		self.master.config(menu=menu)

		file = Menu(menu)
		file.add_command(label='Exit',command=self.quit)
		menu.add_cascade(label='File', menu=file)

		edit = Menu(menu)
		edit.add_command(label='Show Image', command=self.showImg)
		menu.add_cascade(label='Edit',menu=edit)
	def showImg(self):
		f=mandelbrotSet(-2,-1.5,1,1.5,250,250,1000)
		label = Label(image=f)
		label.image = f # keep a reference!
		label.pack()


	def clickRun(self, width=500,height=500):
		try:
			print("HELLO")
			f=mandelbrotSet(float(self.xmin.get()),float(self.ymin.get()),float(self.xmax.get()),float(self.ymax.get()),width,height,int(self.iTmax.get()))
			print("HELLO")
		except Exception as e:
			print("NO")
			print(e)
			pass
		self.f=ImageTk.PhotoImage(f)
		#self.canvasImage.delete("all")
		if self.hasTrace:
			self.image_on_canvas = self.canvasImage.create_image(0, 0, image = self.f)
			self.canvasImage.itemconfig(self.image_on_canvas, image = self.f)
		else:
			self.image_on_canvas = self.canvasImage.create_image( 250, 250, image = self.f)
			self.canvasImage.itemconfig(self.image_on_canvas, image = self.f)
		
			

	def clickTrace(self, width=500,height=500):
		s=TurtleScreen(self.canvasImage)
		self.hasTrace=True
		#rows=np.linspace(xmin,xmax, width)
		#col=np.linspace(ymin,ymax, height)
		
		mandelbrotSet(-1.5,-1.5,1.5,1.5,500,500,1000).convert("RGB").save("temp.gif","GIF")
		s.bgpic("temp.gif")
		t=RawTurtle(s)
		t.color("red")
		#t.goto(250,0)
		z=0+0*1j
		c=float(self.cRpoint.get())+float(self.cIpoint.get())*1j
		#xspan=int(xmax.get())-int(xmin.get())
		t.penup()
		t.goto(int((500/3)*c.real),int((500/3)*c.imag))
		t.pendown()
		t.color("blue")
		t.begin_fill()
		t.circle(3)
		t.end_fill()
		t.color("red")
		for i in range(int(self.iTmax.get())):
			if abs(z)>4:
				break
			p=mandelbrotPath(z,c)
			if abs(z-p)<0.01:
				break
			z=p
			t.goto(int((500/3)*p.real),int((500/3)*p.imag))
			# print(int((500/3)*p.real),int((500/3)*p.imag))
		print(i)

	def clickSaveImage(self, width=2000,height=2000):
		f=mandelbrotSet(float(self.xmin.get()),float(self.ymin.get()),float(self.xmax.get()),float(self.ymax.get()),width,height,int(self.iTmax.get()))
		f=f.convert("RGB")
		f.save("MandelbrotSet_{}_{}_{}_{}_{}-".format(self.xmin.get(),self.ymin.get(),self.xmax.get(),self.ymax.get(),self.iTmax.get())
			+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M')+".png","PNG")
		print("MandelbrotSet_{}_{}_{}_{}_{}".format(self.xmin.get(),self.ymin.get(),self.xmax.get(),self.ymax.get(),self.iTmax.get())
			+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M')+".png")

	def clickSavePar(self):
		file= open('Parameters.txt','a')
		file.write("{},{},{},{},{}\n".format(self.xmin.get(),self.ymin.get(),self.xmax.get(),self.ymax.get(),self.iTmax.get()))
		# print(self.xmin.get(),self.ymin.get(),self.xmax.get(),self.ymax.get(),self.iTmax.get())

	def clickSavePoint(self):
		file= open('Points.txt','a')
		file.write("{},{}\n".format(self.cRpoint.get(),self.cIpoint.get()))
		# print(self.cRpoint.get(),self.cIpoint.get())

	def loadInfo(self):
		self.loadInfo= Toplevel(self.master)
		self.app = Load(self.loadInfo)

	def changeParameters(self,parlist):
		self.xmin.set(parlist[0])
		self.ymin.set(parlist[1])
		self.xmax.set(parlist[2])
		self.ymax.set(parlist[3])
		self.iTmax.set(parlist[4])

	def changePoints(self,parlist):
		self.cRpoint.set(parlist[0])
		self.cIpoint.set(parlist[1])

class Load(Frame):
	def __init__(self, master):
		Frame.__init__(self,master)
		self.master = master
		self.frame = Frame(self.master,height=200,width=300)
		self.frame.pack()
		self.init_window()

	def init_window(self):
		self.master.title("Listbox")
		self.frame.pack(fill=BOTH, expand=1)
		filePar = open('Parameters.txt','r')
		filePoi = open('Points.txt', 'r')
		lb= Listbox(self.frame)
		label= Label(self.frame,text="Load Parameters and Points")
		label.pack()

		for l in filePar.readlines():
			lb.insert(END,str(l))
		for l in filePoi.readlines():
			lb.insert(END,str(l))
		lb.bind("<<ListboxSelect>>",self.onSelect)
		print(filePar.read(),filePoi.read())
		lb.pack()
		self.var = StringVar()
		self.label = Button(self.frame, text="Select",command=self.saveSelected)
		self.label.pack()

	def onSelect(self,val):
		sender = val.widget
		idx = sender.curselection()
		value = sender.get(idx)
		self.var.set(value)

	def saveSelected(self):
		#Calls main window object
		self.points=self.var.get().split(',')
		if len(self.points)==2:
			app.changePoints(self.points)
		else:
			app.changeParameters(self.points)
		self.close_window()

	def close_window(self):
		self.master.destroy()

def mandelbrotPath(z,c):
	z=z**2+c
	return z
@jit
def mandelbrotIt(c,maxIt):
	z=c
	for n in range(maxIt):
		if abs(z)>2:
			return n		
		z=z**2+c
	return maxIt

@jit
def mandelbrotSet(xmin,ymin,xmax,ymax,width,height,maxIt):
	rows=np.linspace(xmin,xmax, width)
	col=np.linspace(ymin,ymax, height)
	img=Image.new('HSV',(width,height),"black")
	pixels = img.load()
	range(width-1)
	for i in range(width):
		for j in range(height):
			it=mandelbrotIt(rows[i]+1j*col[j],maxIt)
			if it==maxIt:
				pixels[i,j]=(0,0,0)
			else:
				pixels[i,j]=(math.floor(it*6+180)%360,255,255)

	#print(img)
	#test=Image.fromarray(img)
	#return(ImageTk.PhotoImage(test))
	#img.show()
	return(img)

root = Tk()
root.geometry("800x600")
app = Window(root)

root.mainloop()