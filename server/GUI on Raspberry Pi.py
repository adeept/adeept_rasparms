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
import info


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

	Btn_SavePos = tk.Button(root, width=6, text='Save Pos',fg=color_text,bg=color_btn,relief='ridge')
	Btn_SavePos.place(x=x,y=y)
	Btn_SavePos.bind('<ButtonPress-1>', savePos)

	Btn_Stop = tk.Button(root, width=6, text='Stop Plan',fg=color_text,bg=color_btn,relief='ridge')
	Btn_Stop.place(x=x+160,y=y)
	Btn_Stop.bind('<ButtonPress-1>', stop)

	Btn_plan = tk.Button(root, width=6, text='Plan',fg=color_text,bg=color_btn,relief='ridge')
	Btn_plan.place(x=x+80,y=y+35)
	Btn_plan.bind('<ButtonPress-1>', plan)

	Btn_CP = tk.Button(root, width=6, text='CreatePlan',fg=color_text,bg=color_btn,relief='ridge')
	Btn_CP.place(x=x,y=y+35)
	Btn_CP.bind('<ButtonPress-1>', createPlan)

	Btn_SavePlan = tk.Button(root, width=6, text='Save Plan',fg=color_text,bg=color_btn,relief='ridge')
	Btn_SavePlan.place(x=x+160,y=y+35)
	Btn_SavePlan.bind('<ButtonPress-1>', savePlan)


def information_screen(x,y):
	global CPU_TEP_lab, CPU_USE_lab, RAM_lab, l_ip_4, l_ip_5
	CPU_TEP_lab=tk.Label(root,width=18,text='CPU Temp:',fg=color_text,bg='#212121')
	CPU_TEP_lab.place(x=x,y=y)						 #Define a Label and put it in position

	CPU_USE_lab=tk.Label(root,width=18,text='CPU Usage:',fg=color_text,bg='#212121')
	CPU_USE_lab.place(x=x,y=y+30)						 #Define a Label and put it in position

	RAM_lab=tk.Label(root,width=18,text='RAM Usage:',fg=color_text,bg='#212121')
	RAM_lab.place(x=x,y=y+60)						 #Define a Label and put it in position

	l_ip_4=tk.Label(root,width=18,text='GUI on RPi',fg=color_text,bg='#F44336')
	l_ip_4.place(x=x,y=y+95)						 #Define a Label and put it in position

	l_ip_5=tk.Label(root,width=18,text='Using Python-TkInter',fg=color_text,bg=color_btn)
	l_ip_5.place(x=x,y=y+130)						 #Define a Label and put it in position

RPi_info = 0
def infoUpdate():
	while 1:
		CPU_TEP_lab.config(text='CPU Temp: '+info.get_cpu_tempfunc())
		CPU_USE_lab.config(text='CPU Usage: '+info.get_cpu_use())
		RAM_lab.config(text='RAM Usage: '+info.get_ram_info())
		time.sleep(2)


def osd_screen(x,y):
	osd_X=tk.Label(root,width=16,text='Xpos: %s'%var_X.get(),fg=color_text,bg='#212121')
	osd_X.place(x=x,y=y)

	osd_Y=tk.Label(root,width=16,text='Ypos: %s'%var_Y.get(),fg=color_text,bg='#212121')
	osd_Y.place(x=x+160,y=y)

	osd_Z=tk.Label(root,width=16,text='Zpos: %s'%var_Z.get(),fg=color_text,bg='#212121')
	osd_Z.place(x=x+320,y=y)

	osd_G=tk.Label(root,width=16,text='Gpos: %s'%var_G.get(),fg=color_text,bg='#212121')
	osd_G.place(x=x+320,y=y-30)


def switch_button(x,y):
	global Btn_Switch_1, Btn_Switch_2, Btn_Switch_3
	def call_Switch_1(event):
		if Switch_1 == 0:
			tcpClicSock.send(('Switch_1_on').encode())
		else:
			tcpClicSock.send(('Switch_1_off').encode())


	def call_Switch_2(event):
		if Switch_2 == 0:
			tcpClicSock.send(('Switch_2_on').encode())
		else:
			tcpClicSock.send(('Switch_2_off').encode())


	def call_Switch_3(event):
		if Switch_3 == 0:
			tcpClicSock.send(('Switch_3_on').encode())
		else:
			tcpClicSock.send(('Switch_3_off').encode())

	Btn_Switch_1 = tk.Button(root, width=6, text='Port 1',fg=color_text,bg=color_btn,relief='ridge')
	Btn_Switch_2 = tk.Button(root, width=6, text='Port 2',fg=color_text,bg=color_btn,relief='ridge')
	Btn_Switch_3 = tk.Button(root, width=6, text='Port 3',fg=color_text,bg=color_btn,relief='ridge')

	Btn_Switch_1.place(x=x,y=y)
	Btn_Switch_2.place(x=x+80,y=y)
	Btn_Switch_3.place(x=x+160,y=y)

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
	Scale_X.place(x=x+20,y=y)							#Define a Scale and put it in position

	Scale_Y = tk.Scale(root,label=None,
	from_=50,to=250,orient=tk.HORIZONTAL,length=w,
	showvalue=1,tickinterval=None,resolution=1,variable=var_Y,troughcolor='#212121',command=Y_send,fg=color_text,bg=color_bg,highlightthickness=0)
	Scale_Y.place(x=x+20,y=y+30)							#Define a Scale and put it in position

	Scale_Z = tk.Scale(root,label=None,
	from_=-100,to=100,orient=tk.HORIZONTAL,length=w,
	showvalue=1,tickinterval=None,resolution=1,variable=var_Z,troughcolor='#212121',command=Z_send,fg=color_text,bg=color_bg,highlightthickness=0)
	Scale_Z.place(x=x+20,y=y+60)							#Define a Scale and put it in position

	Scale_G = tk.Scale(root,label=None,
	from_=-90,to=90,orient=tk.HORIZONTAL,length=w,
	showvalue=1,tickinterval=None,resolution=1,variable=var_G,troughcolor='#212121',command=G_send,fg=color_text,bg=color_bg,highlightthickness=0)
	Scale_G.place(x=x+20,y=y+90)							#Define a Scale and put it in position

	canvas_cover=tk.Canvas(root,bg=color_bg,height=30,width=510,highlightthickness=0)
	canvas_cover.place(x=x+20,y=y+120)


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


	Btn_function_Xup = tk.Button(root, width=6, text='X+',fg=color_text,bg=color_btn,relief='ridge')
	Btn_function_Yup = tk.Button(root, width=6, text='Y+',fg=color_text,bg=color_btn,relief='ridge')
	Btn_function_Zup = tk.Button(root, width=6, text='Z+',fg=color_text,bg=color_btn,relief='ridge')
	Btn_function_Gup = tk.Button(root, width=6, text='G+',fg=color_text,bg=color_btn,relief='ridge')
	
	Btn_function_Xdo = tk.Button(root, width=6, text='X-',fg=color_text,bg=color_btn,relief='ridge')
	Btn_function_Ydo = tk.Button(root, width=6, text='Y-',fg=color_text,bg=color_btn,relief='ridge')
	Btn_function_Zdo = tk.Button(root, width=6, text='Z-',fg=color_text,bg=color_btn,relief='ridge')
	Btn_function_Gdo = tk.Button(root, width=6, text='G-',fg=color_text,bg=color_btn,relief='ridge')

	Btn_function_Xup.place(x=x+80,y=y)
	Btn_function_Yup.place(x=x+80,y=y+35)
	Btn_function_Zup.place(x=x+80,y=y+70)
	Btn_function_Gup.place(x=x+80,y=y+105)

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
	root.title('RaspArmS GUI on Raspberry Pi')
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

	move_buttons(30,30)

	information_screen(330,15)

	# connent_input(30,15)

	switch_button(30,150)

	function_buttons(30,290)

	scale_XYZ(170,290,290)

	osd_screen(30,245)

	global RPi_info
	if not RPi_info:
		info_threading=thread.Thread(target=infoUpdate)
		info_threading.setDaemon(True)
		info_threading.start()
		RPi_info = 1

	root.mainloop()


if __name__ == '__main__':
	loop()