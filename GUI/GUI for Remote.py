#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# File name   : client.py
# Description : client  
# Website	 : www.adeept.com
# Author	  : William
# Date		: 2019/08/28

from socket import *
import sys
import time
import threading as thread
import tkinter as tk


def global_init():
	global color_bg, color_text, color_btn, color_line, color_can, color_oval, target_color, speed, ip_stu

	color_bg='#000000'		#Set background color
	color_text='#E1F5FE'	  #Set text color
	color_btn='#0277BD'	   #Set button color
	color_line='#01579B'	  #Set line color
	color_can='#212121'	   #Set canvas color
	color_oval='#2196F3'	  #Set oval color
	target_color='#FF6D00'
	speed = 100
	ip_stu=1


global_init()


def replace_num(initial,new_num):   #Call this function to replace data in '.txt' file
	newline=""
	str_num=str(new_num)
	with open("ip.txt","r") as f:
		for line in f.readlines():
			if(line.find(initial) == 0):
				line = initial+"%s" %(str_num)
			newline += line
	with open("ip.txt","w") as f:
		f.writelines(newline)	#Call this function to replace data in '.txt' file


def num_import(initial):			#Call this function to import data from '.txt' file
	with open("ip.txt") as f:
		for line in f.readlines():
			if(line.find(initial) == 0):
				r=line
	begin=len(list(initial))
	snum=r[begin:]
	n=snum
	return n	


def Info_receive():
	global CPU_TEP,CPU_USE,RAM_USE,CAR_DIR
	HOST = ''
	INFO_PORT = 2256							#Define port serial 
	ADDR = (HOST, INFO_PORT)
	InfoSock = socket(AF_INET, SOCK_STREAM)
	InfoSock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
	InfoSock.bind(ADDR)
	InfoSock.listen(5)					  #Start server,waiting for client
	InfoSock, addr = InfoSock.accept()
	print('Info connected')
	while 1:
		try:
			info_data = ''
			info_data = str(InfoSock.recv(BUFSIZ).decode())
			info_get = info_data.split()
			CPU_TEP,CPU_USE,RAM_USE,XI,YI,ZI,GI= info_get
			CPU_TEP_lab.config(text='CPU Temp: %s℃'%CPU_TEP)
			CPU_USE_lab.config(text='CPU Usage: %s'%CPU_USE)
			RAM_lab.config(text='RAM Usage: %s'%RAM_USE)
			osd_X.config(text='Xpos: %s'%XI)
			osd_Y.config(text='Xpos: %s'%YI)
			osd_Z.config(text='Xpos: %s'%ZI)
			osd_G.config(text='Xpos: %s'%GI)

		except:
			pass


def socket_connect():	 #Call this function to connect with the server
	global ADDR,tcpClicSock,BUFSIZ,ip_stu,ipaddr
	ip_adr=E1.get()	   #Get the IP address from Entry

	if ip_adr == '':	  #If no input IP address in Entry,import a default IP
		ip_adr=num_import('IP:')
		l_ip_4.config(text='Connecting')
		l_ip_4.config(bg='#FF8F00')
		l_ip_5.config(text='Default:%s'%ip_adr)
		pass
	
	SERVER_IP = ip_adr
	SERVER_PORT = 10223   #Define port serial 
	BUFSIZ = 1024		 #Define buffer size
	ADDR = (SERVER_IP, SERVER_PORT)
	tcpClicSock = socket(AF_INET, SOCK_STREAM) #Set connection value for socket

	for i in range (1,6): #Try 5 times if disconnected
		#try:
		if ip_stu == 1:
			print("Connecting to server @ %s:%d..." %(SERVER_IP, SERVER_PORT))
			print("Connecting")
			tcpClicSock.connect(ADDR)		#Connection with the server
		
			print("Connected")
		
			l_ip_5.config(text='IP:%s'%ip_adr)
			l_ip_4.config(text='Connected')
			l_ip_4.config(bg='#558B2F')

			replace_num('IP:',ip_adr)
			E1.config(state='disabled')	  #Disable the Entry
			Btn14.config(state='disabled')   #Disable the Entry
			
			ip_stu=0						 #'0' means connected

			info_threading=thread.Thread(target=Info_receive)		 #Define a thread for FPV and OpenCV
			info_threading.setDaemon(True)							 #'True' means it is a front thread,it would close when the mainloop() closes
			info_threading.start()									 #Thread starts
			break
		else:
			print("Cannot connecting to server,try it latter!")
			l_ip_4.config(text='Try %d/5 time(s)'%i)
			l_ip_4.config(bg='#EF6C00')
			print('Try %d/5 time(s)'%i)
			ip_stu=1
			time.sleep(1)
			continue

	if ip_stu == 1:
		l_ip_4.config(text='Disconnected')
		l_ip_4.config(bg='#F44336')


def connect(event):	   #Call this function to connect with the server
	if ip_stu == 1:
		sc=thread.Thread(target=socket_connect) #Define a thread for connection
		sc.setDaemon(True)					  #'True' means it is a front thread,it would close when the mainloop() closes
		sc.start()							  #Thread starts


def move_buttons(x,y):
	def savePos(event):
		tcpClicSock.send(('Save Pos').encode())

	def stop(event):
		tcpClicSock.send(('Stop').encode())

	def plan(event):
		tcpClicSock.send(('Plan').encode())

	def createPlan(event):
		tcpClicSock.send(('Create Plan').encode())

	def savePlan(event):
		tcpClicSock.send(('Save Plan').encode())

	# root.bind('<KeyPress-q>', handup)
	# root.bind('<KeyRelease-q>', servoStop)

	Btn_SavePos = tk.Button(root, width=8, text='Save Pos',fg=color_text,bg=color_btn,relief='ridge')
	Btn_SavePos.place(x=x,y=y)
	Btn_SavePos.bind('<ButtonPress-1>', savePos)

	Btn_Stop = tk.Button(root, width=8, text='Stop Plan',fg=color_text,bg=color_btn,relief='ridge')
	Btn_Stop.place(x=x+140,y=y)
	Btn_Stop.bind('<ButtonPress-1>', stop)

	Btn_plan = tk.Button(root, width=8, text='Plan',fg=color_text,bg=color_btn,relief='ridge')
	Btn_plan.place(x=x+70,y=y+35)
	Btn_plan.bind('<ButtonPress-1>', plan)

	Btn_CP = tk.Button(root, width=8, text='Create Plan',fg=color_text,bg=color_btn,relief='ridge')
	Btn_CP.place(x=x,y=y+35)
	Btn_CP.bind('<ButtonPress-1>', createPlan)

	Btn_SavePlan = tk.Button(root, width=8, text='Save Plan',fg=color_text,bg=color_btn,relief='ridge')
	Btn_SavePlan.place(x=x+140,y=y+35)
	Btn_SavePlan.bind('<ButtonPress-1>', savePlan)


def information_screen(x,y):
	global CPU_TEP_lab, CPU_USE_lab, RAM_lab, l_ip_4, l_ip_5
	CPU_TEP_lab=tk.Label(root,width=18,text='CPU Temp:',fg=color_text,bg='#212121')
	CPU_TEP_lab.place(x=x,y=y)						 #Define a Label and put it in position

	CPU_USE_lab=tk.Label(root,width=18,text='CPU Usage:',fg=color_text,bg='#212121')
	CPU_USE_lab.place(x=x,y=y+30)						 #Define a Label and put it in position

	RAM_lab=tk.Label(root,width=18,text='RAM Usage:',fg=color_text,bg='#212121')
	RAM_lab.place(x=x,y=y+60)						 #Define a Label and put it in position

	l_ip_4=tk.Label(root,width=18,text='Disconnected',fg=color_text,bg='#F44336')
	l_ip_4.place(x=x,y=y+95)						 #Define a Label and put it in position

	l_ip_5=tk.Label(root,width=18,text='Use default IP',fg=color_text,bg=color_btn)
	l_ip_5.place(x=x,y=y+130)						 #Define a Label and put it in position


def osd_screen(x,y):
	global osd_X, osd_Y, osd_Z, osd_G
	osd_X=tk.Label(root,width=18,text='Xpos: %s'%var_X.get(),fg=color_text,bg='#212121')
	osd_X.place(x=x,y=y)

	osd_Y=tk.Label(root,width=18,text='Ypos: %s'%var_Y.get(),fg=color_text,bg='#212121')
	osd_Y.place(x=x+140,y=y)

	osd_Z=tk.Label(root,width=18,text='Zpos: %s'%var_Z.get(),fg=color_text,bg='#212121')
	osd_Z.place(x=x+280,y=y)

	osd_G=tk.Label(root,width=18,text='Gpos: %s'%var_G.get(),fg=color_text,bg='#212121')
	osd_G.place(x=x+280,y=y-30)


def connent_input(x,y):
	global E1, Btn14
	E1 = tk.Entry(root,show=None,width=16,bg="#37474F",fg='#eceff1')
	E1.place(x=x+5,y=y+25)							 #Define a Entry and put it in position

	l_ip_3=tk.Label(root,width=10,text='IP Address:',fg=color_text,bg='#000000')
	l_ip_3.place(x=x,y=y)						 #Define a Label and put it in position

	Btn14= tk.Button(root, width=8,height=2, text='Connect',fg=color_text,bg=color_btn,relief='ridge')
	Btn14.place(x=x+130,y=y)						  #Define a Button and put it in position

	root.bind('<Return>', connect)
	Btn14.bind('<ButtonPress-1>', connect)


def switch_button(x,y):
	global Btn_Switch_1, Btn_Switch_2, Btn_Switch_3
	def call_Switch_1(event):
		tcpClicSock.send(('Switch_1').encode())

	def call_Switch_2(event):
		tcpClicSock.send(('Switch_2').encode())

	def call_Switch_3(event):
		tcpClicSock.send(('Switch_3').encode())

	Btn_Switch_1 = tk.Button(root, width=8, text='Port 1',fg=color_text,bg=color_btn,relief='ridge')
	Btn_Switch_2 = tk.Button(root, width=8, text='Port 2',fg=color_text,bg=color_btn,relief='ridge')
	Btn_Switch_3 = tk.Button(root, width=8, text='Port 3',fg=color_text,bg=color_btn,relief='ridge')

	Btn_Switch_1.place(x=x,y=y)
	Btn_Switch_2.place(x=x+70,y=y)
	Btn_Switch_3.place(x=x+140,y=y)

	Btn_Switch_1.bind('<ButtonPress-1>', call_Switch_1)
	Btn_Switch_2.bind('<ButtonPress-1>', call_Switch_2)
	Btn_Switch_3.bind('<ButtonPress-1>', call_Switch_3)


def scale_XYZ(x,y,w):
	def X_send(event):
		time.sleep(0.03)
		tcpClicSock.send(('Xpos %s'%var_X.get()).encode())

	def Y_send(event):
		time.sleep(0.03)
		tcpClicSock.send(('Ypos %s'%var_Y.get()).encode())

	def Z_send(event):
		time.sleep(0.03)
		tcpClicSock.send(('Zpos %s'%var_Z.get()).encode())

	def G_send(event):
		tcpClicSock.send(('Gpos %s'%var_G.get()).encode())


	Scale_X = tk.Scale(root,label=None,
	from_=-100,to=100,orient=tk.HORIZONTAL,length=w,
	showvalue=1,tickinterval=None,resolution=1,variable=var_X,troughcolor='#212121',command=X_send,fg=color_text,bg=color_bg,highlightthickness=0)
	Scale_X.place(x=x,y=y)							#Define a Scale and put it in position

	Scale_Y = tk.Scale(root,label=None,
	from_=50,to=150,orient=tk.HORIZONTAL,length=w,
	showvalue=1,tickinterval=None,resolution=1,variable=var_Y,troughcolor='#212121',command=Y_send,fg=color_text,bg=color_bg,highlightthickness=0)
	Scale_Y.place(x=x,y=y+30)							#Define a Scale and put it in position

	Scale_Z = tk.Scale(root,label=None,
	from_=-100,to=100,orient=tk.HORIZONTAL,length=w,
	showvalue=1,tickinterval=None,resolution=1,variable=var_Z,troughcolor='#212121',command=Z_send,fg=color_text,bg=color_bg,highlightthickness=0)
	Scale_Z.place(x=x,y=y+60)							#Define a Scale and put it in position

	Scale_G = tk.Scale(root,label=None,
	from_=-90,to=90,orient=tk.HORIZONTAL,length=w,
	showvalue=1,tickinterval=None,resolution=1,variable=var_G,troughcolor='#212121',command=G_send,fg=color_text,bg=color_bg,highlightthickness=0)
	Scale_G.place(x=x,y=y+90)							#Define a Scale and put it in position

	canvas_cover=tk.Canvas(root,bg=color_bg,height=30,width=510,highlightthickness=0)
	canvas_cover.place(x=x,y=y+120)


def function_buttons(x,y):
	def call_Xup(event):
		tcpClicSock.send(('X_add').encode())

	def call_Xdo(event):
		tcpClicSock.send(('X_minus').encode())

	def call_Xs(event):
		tcpClicSock.send(('XS').encode())


	def call_Yup(event):
		tcpClicSock.send(('Y_add').encode())

	def call_Ydo(event):
		tcpClicSock.send(('Y_minus').encode())

	def call_Ys(event):
		tcpClicSock.send(('YS').encode())


	def call_Zup(event):
		tcpClicSock.send(('Z_add').encode())

	def call_Zdo(event):
		tcpClicSock.send(('Z_minus').encode())

	def call_Zs(event):
		tcpClicSock.send(('ZS').encode())


	def call_Gup(event):
		tcpClicSock.send(('G_add').encode())

	def call_Gdo(event):
		tcpClicSock.send(('G_minus').encode())

	def call_Gs(event):
		tcpClicSock.send(('GS').encode())


	Btn_function_Xup = tk.Button(root, width=8, text='X+',fg=color_text,bg=color_btn,relief='ridge')
	Btn_function_Yup = tk.Button(root, width=8, text='Y+',fg=color_text,bg=color_btn,relief='ridge')
	Btn_function_Zup = tk.Button(root, width=8, text='Z+',fg=color_text,bg=color_btn,relief='ridge')
	Btn_function_Gup = tk.Button(root, width=8, text='G+',fg=color_text,bg=color_btn,relief='ridge')
	
	Btn_function_Xdo = tk.Button(root, width=8, text='X-',fg=color_text,bg=color_btn,relief='ridge')
	Btn_function_Ydo = tk.Button(root, width=8, text='Y-',fg=color_text,bg=color_btn,relief='ridge')
	Btn_function_Zdo = tk.Button(root, width=8, text='Z-',fg=color_text,bg=color_btn,relief='ridge')
	Btn_function_Gdo = tk.Button(root, width=8, text='G-',fg=color_text,bg=color_btn,relief='ridge')

	Btn_function_Xup.place(x=x+70,y=y)
	Btn_function_Yup.place(x=x+70,y=y+35)
	Btn_function_Zup.place(x=x+70,y=y+70)
	Btn_function_Gup.place(x=x+70,y=y+105)

	Btn_function_Xdo.place(x=x,y=y)
	Btn_function_Ydo.place(x=x,y=y+35)
	Btn_function_Zdo.place(x=x,y=y+70)
	Btn_function_Gdo.place(x=x,y=y+105)

	Btn_function_Xup.bind('<ButtonPress-1>', call_Xup)
	Btn_function_Yup.bind('<ButtonPress-1>', call_Yup)
	Btn_function_Zup.bind('<ButtonPress-1>', call_Zup)
	Btn_function_Gup.bind('<ButtonPress-1>', call_Gup)

	Btn_function_Xdo.bind('<ButtonPress-1>', call_Xdo)
	Btn_function_Ydo.bind('<ButtonPress-1>', call_Ydo)
	Btn_function_Zdo.bind('<ButtonPress-1>', call_Zdo)
	Btn_function_Gdo.bind('<ButtonPress-1>', call_Gdo)

	Btn_function_Xup.bind('<ButtonRelease-1>', call_Xs)
	Btn_function_Yup.bind('<ButtonRelease-1>', call_Ys)
	Btn_function_Zup.bind('<ButtonRelease-1>', call_Zs)
	Btn_function_Gup.bind('<ButtonRelease-1>', call_Gs)

	Btn_function_Xdo.bind('<ButtonRelease-1>', call_Xs)
	Btn_function_Ydo.bind('<ButtonRelease-1>', call_Ys)
	Btn_function_Zdo.bind('<ButtonRelease-1>', call_Zs)
	Btn_function_Gdo.bind('<ButtonRelease-1>', call_Gs)


def loop():
	global root, var_X, var_Y, var_Z, var_G, var_Speed
	root = tk.Tk()
	root.title('RaspArmS on Linux')
	root.geometry('495x460')
	root.config(bg=color_bg)  

	var_X = tk.StringVar()
	var_X.set(0)
	var_Y = tk.StringVar()
	var_Y.set(100)
	var_Z = tk.StringVar()
	var_Z.set(0)
	var_G = tk.StringVar()
	var_G.set(0)

	var_Speed = tk.StringVar() 
	var_Speed.set(0)			

	try:
		logo =tk.PhotoImage(file = 'logo.png')
		l_logo=tk.Label(root,image = logo,bg=color_bg)
		l_logo.place(x=30,y=13)
	except:
		pass

	move_buttons(30,105)

	information_screen(330,15)

	connent_input(125,15)

	switch_button(30,195)

	function_buttons(30,290)

	scale_XYZ(170,290,290)

	osd_screen(30,245)

	root.mainloop()


if __name__ == '__main__':
	loop()
