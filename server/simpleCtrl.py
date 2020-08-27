#!/usr/bin/env python3
#coding=utf-8
import raspArmS
import OLED
import time
import threading
from RPi import GPIO
from bottle import get,post,run,request,template,route
import socket
import info

clk = 19
dt = 16
btn = 20

number = 0
old_number = number
clkLastState = 0
PressI  = 7
PressII = 14

ctrlSpeed = 8

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

screen = OLED.OLED_ctrl()
screen.start()

pathLevel = 0
pathSaved = [0,0,0]

levelNameL0   = ['XYZ Ctrl', 'servoCtrl', 'planCtrl']
L0 = 3

levelNameL10 = ['X Axis Ctrl', 'Y Axis Ctrl', 'Z Axis Ctrl', 'G Axis Ctrl']
L10 = 4

levelNameL11 = ['A Servo', 'B Servo', 'C Servo', 'D Servo']
L11 = 4

levelNameL12 = ['planStart', 'createNew']
L12 = 2

levelNameL120 = ['X Axis Ctrl', 'Y Axis Ctrl', 'Z Axis Ctrl', 'G Axis Ctrl']
L120 = 4

L0_text_1 = 'IP:CONNECTING'
L0_text_2 = 'MODE SELECT'
L0_text_3 = '.....................'
L0_text_4 = 'XYZ CTRL   <<<'
L0_text_5 = 'Servo CTRL '
L0_text_6 = 'Plan CTRL  '
L0_text_7 = 'RaspArmS'

ras = raspArmS.RaspArmS()
ras.start()

aimXYZ = [0, 100, 100, 0]
servoAng = [0, 0, 0, 0]


def pathInit():
	global pathLevel, pathSaved
	pathLevel = 0
	pathSaved = [0,0,0]
	screen.screen_show(1, L0_text_1)
	screen.screen_show(2, L0_text_2)
	screen.screen_show(3, L0_text_3)
	screen.screen_show(4, L0_text_4)
	screen.screen_show(5, L0_text_5)
	screen.screen_show(6, L0_text_6)
	screen.screen_show(7, L0_text_7)


def oledUpdate():
	if pathLevel == 0:
		if pathSaved[0] == 0:
			INI1 = L0_text_1
			INI2 = 'MODE SELECT'
			INI3 = '.....................'
			TL0_1 = 'XYZ CTRL   <<<'
			TL0_2 = 'Servo CTRL '
			TL0_3 = 'Plan CTRL  '
		elif pathSaved[0] == 1:
			INI1 = L0_text_1
			INI2 = 'MODE SELECT'
			INI3 = '.....................'
			TL0_1 = 'XYZ CTRL   '
			TL0_2 = 'Servo CTRL <<<'
			TL0_3 = 'Plan CTRL  '
		elif pathSaved[0] == 2:
			INI1 = L0_text_1
			INI2 = 'MODE SELECT'
			INI3 = '.....................'
			TL0_1 = 'XYZ CTRL   '
			TL0_2 = 'Servo CTRL '
			TL0_3 = 'Plan CTRL  <<<'
		screen.screen_shows([1, 2, 3, 4, 5, 6], [INI1, INI2, INI3, TL0_1, TL0_2, TL0_3])

	elif pathLevel == 1:
		if pathSaved[0] == 0:
			TL10_1 = 'MODE: XYZ CTRL'
			TL10_2 = '.....................'
			if pathSaved[1] == 0:
				TL10_3 = 'X-AIXS <<<'
				TL10_4 = 'Y-AIXS '
				TL10_5 = 'Z-AIXS '
				TL10_6 = 'G-AIXS '
			elif pathSaved[1] == 1:
				TL10_3 = 'X-AIXS '
				TL10_4 = 'Y-AIXS <<<'
				TL10_5 = 'Z-AIXS '
				TL10_6 = 'G-AIXS '
			elif pathSaved[1] == 2:
				TL10_3 = 'X-AIXS '
				TL10_4 = 'Y-AIXS '
				TL10_5 = 'Z-AIXS <<<'
				TL10_6 = 'G-AIXS '
			elif pathSaved[1] == 3:
				TL10_3 = 'X-AIXS '
				TL10_4 = 'Y-AIXS '
				TL10_5 = 'Z-AIXS '
				TL10_6 = 'G-AIXS <<<'

		elif pathSaved[0] == 1:
			TL10_1 = 'MODE: SERVO CTRL'
			TL10_2 = '.....................'
			if pathSaved[1] == 0:
				TL10_3 = 'A-SERVO <<<'
				TL10_4 = 'B-SERVO '
				TL10_5 = 'C-SERVO '
				TL10_6 = 'D-SERVO '
			elif pathSaved[1] == 1:
				TL10_3 = 'A-SERVO '
				TL10_4 = 'B-SERVO <<<'
				TL10_5 = 'C-SERVO '
				TL10_6 = 'D-SERVO '
			elif pathSaved[1] == 2:
				TL10_3 = 'A-SERVO '
				TL10_4 = 'B-SERVO '
				TL10_5 = 'C-SERVO <<<'
				TL10_6 = 'D-SERVO '
			elif pathSaved[1] == 3:
				TL10_3 = 'A-SERVO '
				TL10_4 = 'B-SERVO '
				TL10_5 = 'C-SERVO '
				TL10_6 = 'D-SERVO <<<'

		elif pathSaved[0] == 2:
			TL10_1 = 'MODE: PLAN CTRL'
			TL10_2 = '.....................'
			if pathSaved[1] == 0:
				TL10_3 = 'PLAN START <<<'
				TL10_4 = 'CREATE NEW '
				TL10_5 = ' '
				TL10_6 = ' '
			elif pathSaved[1] == 1:
				TL10_3 = 'PLAN START '
				TL10_4 = 'CREATE NEW <<<'
				TL10_5 = ' '
				TL10_6 = ' '

		screen.screen_shows([1, 2, 3, 4, 5, 6], [TL10_1, TL10_2, TL10_3, TL10_4, TL10_5, TL10_6])


	elif pathLevel == 2:
		TL10_1 = 'MODE: XYZ CTRL'
		TL10_2 = '.....................'
		if pathSaved[2] == 0:
			TL10_3 = 'X-AIXS <<<'
			TL10_4 = 'Y-AIXS '
			TL10_5 = 'Z-AIXS '
			TL10_6 = 'G-AIXS '
		elif pathSaved[2] == 1:
			TL10_3 = 'X-AIXS '
			TL10_4 = 'Y-AIXS <<<'
			TL10_5 = 'Z-AIXS '
			TL10_6 = 'G-AIXS '
		elif pathSaved[2] == 2:
			TL10_3 = 'X-AIXS '
			TL10_4 = 'Y-AIXS '
			TL10_5 = 'Z-AIXS <<<'
			TL10_6 = 'G-AIXS '
		elif pathSaved[2] == 3:
			TL10_3 = 'X-AIXS '
			TL10_4 = 'Y-AIXS '
			TL10_5 = 'Z-AIXS '
			TL10_6 = 'G-AIXS <<<'

		screen.screen_shows([1, 2, 3, 4, 5, 6], [TL10_1, TL10_2, TL10_3, TL10_4, TL10_5, TL10_6])




	# print(pathLevel)
	# print(pathSaved)
	pass


def showPressTime(pressInput):
	showTimeText = ''
	if pressInput == '0':
		pass
	elif pressInput == 'I':
		showTimeText = '+++++++++++++++++++++'
		if pathLevel == 0:
			screen.screen_show(3, showTimeText)
		else:
			screen.screen_show(2, showTimeText)
	elif pressInput == 'II':
		showTimeText = 'XXXXXXXXXXXXXXXXXXXXX'
		if pathLevel == 0:
			screen.screen_show(3, showTimeText)
		else:
			screen.screen_show(2, showTimeText)
	pass


def pathCtrl(command):
	global pathLevel, pathSaved
	if command == '1':
		if pathLevel == 0:
			pathSaved[0] += 1
			if pathSaved[0] >= L0:
				pathSaved[0] = 0
			time.sleep(0.05)

		elif pathLevel == 1:
			if pathSaved[0] == 0:
				if pathSaved[1] == 0:
					aimXYZ[0] += ctrlSpeed

				elif pathSaved[1] == 1:
					aimXYZ[1] += ctrlSpeed

				elif pathSaved[1] == 2:
					aimXYZ[2] += ctrlSpeed

				elif pathSaved[1] == 3:
					aimXYZ[3] += ctrlSpeed

				ras.xyzInput(aimXYZ)

			elif pathSaved[0] == 1: 
				if pathSaved[1] == 0:
					servoAng[0] += ctrlSpeed

				elif pathSaved[1] == 1:
					servoAng[1] += ctrlSpeed

				elif pathSaved[1] == 2:
					servoAng[2] += ctrlSpeed

				elif pathSaved[1] == 3:
					servoAng[3] += ctrlSpeed

				ras.servoAngInput(servoAng)

			elif pathSaved[0] == 2:
				if pathSaved[1] == 0:
					pathSaved[1] = 1
				else:
					pathSaved[1] = 0

		elif pathLevel == 2:
			if pathSaved[2] == 0:
				aimXYZ[0] += ctrlSpeed
			elif pathSaved[2] == 1:
				aimXYZ[1] += ctrlSpeed
			elif pathSaved[2] == 2:
				aimXYZ[2] += ctrlSpeed
			elif pathSaved[2] == 3:
				aimXYZ[3] += ctrlSpeed

			ras.xyzInput(aimXYZ)

	elif command == '-1':
		if pathLevel == 0:
			pathSaved[0] -= 1
			if pathSaved[0] < 0:
				pathSaved[0] = L0 - 1
			time.sleep(0.05)

		elif pathLevel == 1:
			if pathSaved[0] == 0:
				if pathSaved[1] == 0:
					aimXYZ[0] -= ctrlSpeed

				elif pathSaved[1] == 1:
					aimXYZ[1] -= ctrlSpeed

				elif pathSaved[1] == 2:
					aimXYZ[2] -= ctrlSpeed

				elif pathSaved[1] == 3:
					aimXYZ[3] -= ctrlSpeed

				ras.xyzInput(aimXYZ)

			elif pathSaved[0] == 1: 
				if pathSaved[1] == 0:
					servoAng[0] -= ctrlSpeed
				elif pathSaved[1] == 1:
					servoAng[1] -= ctrlSpeed
				elif pathSaved[1] == 2:
					servoAng[2] -= ctrlSpeed
				elif pathSaved[1] == 3:
					servoAng[3] -= ctrlSpeed

				ras.servoAngInput(servoAng)

			elif pathSaved[0] == 2:
				if pathSaved[1] == 0:
					pathSaved[1] = 1
				else:
					pathSaved[1] = 0

		elif pathLevel == 2:
			if pathSaved[2] == 0:
				aimXYZ[0] -= ctrlSpeed
			elif pathSaved[2] == 1:
				aimXYZ[1] -= ctrlSpeed
			elif pathSaved[2] == 2:
				aimXYZ[2] -= ctrlSpeed
			elif pathSaved[2] == 3:
				aimXYZ[3] -= ctrlSpeed

			ras.xyzInput(aimXYZ)

	elif command == 'Press0':
		if pathLevel == 0:
			pathLevel += 1

		elif pathLevel == 1:
			if pathSaved[0] == 0:
				pathSaved[1] += 1
				if pathSaved[1] >= L10:
					pathSaved[1] = 0

			elif pathSaved[0] == 1:
				pathSaved[1] += 1
				if pathSaved[1] >= L11:
					pathSaved[1] = 0

			elif pathSaved[0] == 2:
				if pathSaved[1] > 2:
					pathSaved[1] = 0

				if pathSaved[1] == 0:
					ras.planGoes(ras.planData)
				elif pathSaved[1] == 1:
					ras.createNewPlan()
					pathLevel += 1

		elif pathLevel == 2:
			pathSaved[2] += 1
			if pathSaved[2] > L120:
				pathSaved[2] = 0
				print(pathSaved[2])

		oledUpdate()

	elif command == 'PressI':
		if pathLevel == 0:
			pass

		elif pathLevel == 1:
			pathLevel -= 1

		elif pathLevel == 2:
			ras.newPlanAppend()

		oledUpdate()


	elif command == 'PressII':
		if pathLevel == 2:
			ras.savePlanJson()
		pathLevel = 0
		pathInit()
		time.sleep(0.2)

		oledUpdate()


	if pathLevel == 1 and pathSaved[1] != 2:
		pass
	else:
		oledUpdate()


def rotaryInput():
	global clkLastState, old_number, number
	while 1:
		if GPIO.wait_for_edge(clk, GPIO.FALLING):
			clkState = GPIO.input(clk)
			dtState = GPIO.input(dt)
			if clkState != clkLastState:
				if dtState != clkState:
					number -= 1
					# menuCtrl('-1')
					pathCtrl('-1')
				else:
					number += 1
					# menuCtrl('1')
					pathCtrl('1')
			clkLastState = clkState
			if number != old_number:
				old_number = number
				time.sleep(0)


def buttonInput():
	while 1:
		if not GPIO.input(btn):
			timeCount = 0
			while not GPIO.input(btn):
				timeCount += 1
				if timeCount >= PressI:
					showPressTime('I')
					break
				time.sleep(0.1)

			while not GPIO.input(btn):
				timeCount += 1
				if timeCount >= PressII:
					showPressTime('II')
					pathCtrl('PressII')
					while not GPIO.input(btn):
						pass
					break
				time.sleep(0.1)

			if timeCount > PressI:
				pathCtrl('PressI')
			else:
				pathCtrl('Press0')
		time.sleep(0.1)


def info_send_client():
	SERVER_IP = addr[0]
	SERVER_PORT = 2256   #Define port serial 
	SERVER_ADDR = (SERVER_IP, SERVER_PORT)
	Info_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Set connection value for socket
	Info_Socket.connect(SERVER_ADDR)
	print(SERVER_ADDR)
	while 1:
		try:
			Info_Socket.send((info.get_cpu_tempfunc()+' '+info.get_cpu_use()+' '+info.get_ram_info()+' '+str(servo.get_direction())).encode())
			time.sleep(1)
		except:
			time.sleep(10)
			pass


def  ap_thread():
	os.system("sudo create_ap wlan0 eth0 MyRobot 12345678")


def runTcp():
	speed_set = 100
	posBuffer = [0,50,0,0]

	info_threading=threading.Thread(target=info_send_client)    #Define a thread for FPV and OpenCV
	info_threading.setDaemon(True)                             #'True' means it is a front thread,it would close when the mainloop() closes
	info_threading.start()                                     #Thread starts

	while True: 
		data = ''
		data = str(tcpCliSock.recv(BUFSIZ).decode())
		if not data:
			continue

		elif 'X_minus' == data:
			ras.simpleMoveStart("X", "-")
		elif 'X_add' == data:
			ras.simpleMoveStart("X", "+")
		elif 'XS' in data:
			ras.simpleMoveStart("X", "stop")

		elif 'Y_minus' == data:
			ras.simpleMoveStart("Y", "-")
		elif 'Y_add' == data:
			ras.simpleMoveStart("Y", "+")
		elif 'YS' in data:
			ras.simpleMoveStart("Y", "stop")

		elif 'Z_minus' == data:
			ras.simpleMoveStart("Z", "-")
		elif 'Z_add' == data:
			ras.simpleMoveStart("Z", "+")
		elif 'ZS' in data:
			ras.simpleMoveStart("Z", "stop")

		elif 'G_minus' == data:
			ras.simpleMoveStart("G", "-")
			# ras.gripper('catch')
		elif 'G_add' == data:
			ras.simpleMoveStart("G", "+")
			# ras.gripper('loose')
		elif 'GS' in data:
			ras.simpleMoveStart("G", "stop")


		elif 'Save Pos' == data:
			ras.newPlanAppend()
		elif 'Stop' == data:
			ras.moveThreadingStop()
		elif 'Create Plan' == data:
			ras.createNewPlan()
		elif 'Plan' == data:
			ras.planGoes(ras.planData)
		elif 'Save Plan' == data:
			ras.savePlanJson()

		print(data)


def wifi_check():
	global L0_text_1
	try:
		s =socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		s.connect(("1.1.1.1",80))
		ipaddr_check=s.getsockname()[0]
		s.close()
		print(ipaddr_check)
		L0_text_1 = 'IP:'+ipaddr_check+' '
		
		# screen.screen_show(2, 'IP:'+ipaddr_check)
		# screen.screen_show(3, 'AP MODE OFF')
	except:
		ap_threading=threading.Thread(target=ap_thread)   #Define a thread for data receiving
		ap_threading.setDaemon(True)                          #'True' means it is a front thread,it would close when the mainloop() closes
		ap_threading.start()                                  #Thread starts

	oledUpdate()


def tcpConnection():
	global tcpSerSock, tcpCliSock, addr, BUFSIZ
	while 1:
		HOST = ''
		PORT = 10223                              #Define port serial 
		BUFSIZ = 1024                             #Define buffer size
		ADDR = (HOST, PORT)

		# while  1:
		wifi_check()
		# try:
		tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		tcpSerSock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		tcpSerSock.bind(ADDR)
		tcpSerSock.listen(5)                      #Start server,waiting for client
		print('waiting for connection...')
		tcpCliSock, addr = tcpSerSock.accept()
		print('...connected from :', addr)
		break
		# except:
			# pass

		try:
			runTcp()
		except Exception as e:
			print(e)

		time.sleep(1)


def ipUpdate():
	global L0_text_1
	time.sleep(50)
	while 1:
		s =socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		s.connect(("1.1.1.1",80))
		ipaddr_check=s.getsockname()[0]
		s.close()
		print(ipaddr_check)
		L0_text_1 = 'IP:'+ipaddr_check+' '
		oledUpdate()
		time.sleep(15)


ipUpdateThreading=threading.Thread(target=ipUpdate)
ipUpdateThreading.setDaemon(True)
ipUpdateThreading.start()


tcpThreading=threading.Thread(target=tcpConnection)
tcpThreading.setDaemon(True)
tcpThreading.start()


rotaryInputThreading=threading.Thread(target=rotaryInput)
rotaryInputThreading.setDaemon(True)
rotaryInputThreading.start()


buttonInputThreading=threading.Thread(target=buttonInput)
buttonInputThreading.setDaemon(True)
buttonInputThreading.start()


def webserver(command):
	if command.isdigit():
		print(int(command))
	else:
		if command == "X_add":
			print("111")
			ras.simpleMoveStart("X", "+")
		elif command == "X_minus":
			ras.simpleMoveStart("X", "-")
		elif command == "XS":
			print("222")
			ras.simpleMoveStart("X", "stop")
		else:
			print("Command:%s" %command)


if __name__ == '__main__':
	# while 1:
	#   time.sleep(10)

	@get("/")
	def index():
		return template("index")

	@get("/value")
	def get_some():
		car = Car()
		value11 = car.post_value()
		# def p_value(value11):
		print(str(value11))
		return '<html><head></head><body id="bd"> {value} </body></html>'.format(value = str(value11))


	@post("/cmd")
	def cmd():
		adss=request.body.read().decode()
		print("pressinput:"+adss)
		webserver(adss)
		return "OK"
	run(host="0.0.0.0", port=5000)


