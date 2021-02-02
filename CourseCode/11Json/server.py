'''
Import libraries related to TCP communication
'''
import socket
import time
import json

'''
Initialize the TCP server
'''
HOST = ''
PORT = 10223                              #Define port serial 
BUFSIZ = 1024                             #Define buffer size
ADDR = (HOST, PORT)

'''
Establish a TCP server and monitor client connections
'''
tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpSerSock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)                      #Start server,waiting for client
print('waiting for connection...')

'''
Client connection is successful
'''
tcpCliSock, addr = tcpSerSock.accept()
print('...connected from :', addr)

'''
Define two arrays
'''
list_1 = [10, 20, 30, 40]
list_2 = [50, 60, 70, 80]

while 1:
	'''
	Encode array into json string
	'''
	s = json.dumps(list_1)

	'''
	Send this string
	'''
	tcpCliSock.send(str(s).encode())
	time.sleep(1)

	s = json.dumps(list_2)
	tcpCliSock.send(str(s).encode())
	time.sleep(1)