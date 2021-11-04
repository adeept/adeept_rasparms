#!/usr/bin/env/python
# File name   : server.py
# Production  : GWR
# Website     : www.gewbot.com
# E-mail      : gewubot@163.com
# Author      : William
# Date        : 2019/07/24

import socket
import time
import threading
import info
import raspArmS

ras = raspArmS.RaspArmS()
ras.start()

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


def run():
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

        # elif 'forward' == data:
        #     pass
        elif data == "X_add":
            ras.simpleMoveStart("X", "+")
        elif data == "X_minus":
            ras.simpleMoveStart("X", "-")
        elif data == "XS":
            ras.simpleMoveStart("X", "stop")

        elif data == 'Y_add':
            ras.simpleMoveStart("Y", "+")
        elif data == 'Y_minus':
            ras.simpleMoveStart("Y", "-")
        elif data == 'YS':
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


        elif 'save_pos' == data:
            ras.newPlanAppend()
            time.sleep(0.5)
        elif 'stop' == data:
            ras.moveThreadingStop()
        elif 'create_Plan' == data:
            ras.createNewPlan()
        elif 'plan' == data:
            ras.planThreadingStart()
        elif 'save_Plan' == data:
            ras.savePlanJson()


        else:
            print("Command:%s" %data)


        print(data)


def wifi_check():
    try:
        s =socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(("1.1.1.1",80))
        ipaddr_check=s.getsockname()[0]
        s.close()
        print(ipaddr_check)
        # screen.screen_show(2, 'IP:'+ipaddr_check)
        # screen.screen_show(3, 'AP MODE OFF')
    except:
        ap_threading=threading.Thread(target=ap_thread)   #Define a thread for data receiving
        ap_threading.setDaemon(True)                          #'True' means it is a front thread,it would close when the mainloop() closes
        ap_threading.start()                                  #Thread starts



if __name__ == '__main__':
    while 1:
        HOST = ''
        PORT = 10223                              #Define port serial 
        BUFSIZ = 1024                             #Define buffer size
        ADDR = (HOST, PORT)

        while  1:
            wifi_check()
            try:
                tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tcpSerSock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
                tcpSerSock.bind(ADDR)
                tcpSerSock.listen(5)                      #Start server,waiting for client
                print('waiting for connection...')
                tcpCliSock, addr = tcpSerSock.accept()
                print('...connected from :', addr)
                break
            except Exception as e:
                print(e)

        try:
            run()
        except Exception as e:
            print(e)

        time.sleep(1)
