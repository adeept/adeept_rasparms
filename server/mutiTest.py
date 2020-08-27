import socket
import threading
import time
import raspArmS


ras = raspArmS.RaspArmS()
ras.start()


def runTcp():
	speed_set = 100
	posBuffer = [0,50,0,0]

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
			time.sleep(0.5)
		elif 'Stop' == data:
			ras.moveThreadingStop()
		elif 'Create Plan' == data:
			ras.createNewPlan()
		elif 'Plan' == data:
			ras.planThreadingStart()
		elif 'Save Plan' == data:
			ras.savePlanJson()

		print(ras.nowPos)


def tcpConnection():
	global tcpSerSock, tcpCliSock, addr, BUFSIZ
	while 1:
		HOST = ''
		PORT = 10223                              #Define port serial 
		BUFSIZ = 1024                             #Define buffer size
		ADDR = (HOST, PORT)

		while  1:
			try:
				tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				tcpSerSock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
				tcpSerSock.bind(ADDR)
				tcpSerSock.listen(5)                      #Start server,waiting for client
				print('waiting for connection...')
				tcpCliSock, addr = tcpSerSock.accept()
				print('...connected from :', addr)
				break
			except:
				pass

		try:
			runTcp()
		except Exception as e:
			print(e)

		time.sleep(1)


rotaryInputThreading=threading.Thread(target=tcpConnection)
rotaryInputThreading.setDaemon(True)
rotaryInputThreading.start()


if __name__ == '__main__':
	print('you can add something else here.')

	while 1:
		time.sleep(100)
		pass