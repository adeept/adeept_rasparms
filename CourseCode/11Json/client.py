from socket import *
import json

'''
The IP address here needs to be changed to the IP address of the server
'''
SERVER_IP = "192.168.3.187"
SERVER_PORT = 10223   #Define port serial
BUFSIZ = 1024		 #Define buffer size
ADDR = (SERVER_IP, SERVER_PORT)
tcpClicSock = socket(AF_INET, SOCK_STREAM) #Set connection value for socket
tcpClicSock.connect(ADDR)

while 1:
	'''
	Receive the Json string sent from the server
	'''
	data = (tcpClicSock.recv(BUFSIZ)).decode()

	'''
	Decode the Json string into the corresponding format
	'''
	output = json.loads(data)

	'''
	Print output, actually output can now be used as an array
	'''
	print(output)