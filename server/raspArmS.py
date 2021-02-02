#!/usr/bin/env python3
#coding=utf-8
import time
import Adafruit_PCA9685
import numpy as np
import json
import threading
import os

curpath = os.path.realpath(__file__)
thisPath = "/" + os.path.dirname(curpath) + "/"

ctrlRangeMax = 492
ctrlRangeMin = 295
angleRange = 90

planJsonFileHere = open(thisPath + 'plan.json', 'r')
print(thisPath + 'plan.json')
contentPlanGose  = planJsonFileHere.read()
planGoseList = json.loads(contentPlanGose)
'''
planDataNow
'''


def limitCheck(posInput, circlePos, circleLen, outline): #E
    circleRx = posInput[0]-circlePos[0]
    circleRy = posInput[1]-circlePos[1]
    realPosSquare = circleRx*circleRx+circleRy*circleRy
    shortRadiusSquare = np.square(circleLen[1]-circleLen[0])
    longRadiusSquare = np.square(circleLen[1]+circleLen[0])

    if realPosSquare >= shortRadiusSquare and realPosSquare <= longRadiusSquare:
        return posInput[0], posInput[1]

    else:
        lineK = (posInput[1]-circlePos[1])/((posInput[0]-circlePos[0])+0.00001)
        lineB = circlePos[1]-(lineK*circlePos[0])
        
        if realPosSquare < shortRadiusSquare:
            aX = 1 + lineK*lineK
            bX = 2*lineK*(lineB - circlePos[1]) - 2*circlePos[0]
            cX = circlePos[0]*circlePos[0] + (lineB - circlePos[1])*(lineB - circlePos[1]) - shortRadiusSquare

            resultX = bX*bX - 4*aX*cX
            x1 = (-bX + np.sqrt(resultX))/(2*aX)
            x2 = (-bX - np.sqrt(resultX))/(2*aX)

            y1 = lineK*x1 + lineB
            y2 = lineK*x2 + lineB

            if posInput[0] > circlePos[0]:
                if x1 > circlePos[0]:
                    xGenOut = x1+outline
                    yGenOut = y1
                else:
                    xGenOut = x2-outline
                    yGenOut = y2
            elif posInput[0] < circlePos[0]:
                if x1 < circlePos[0]:
                    xGenOut = x1-outline
                    yGenOut = y1
                else:
                    xGenOut = x2+outline
                    yGenOut = y2
            elif posInput[0] == circlePos[0]:
                if posInput[1] > circlePos[1]:
                    if y1 > circlePos[1]:
                        xGenOut = x1
                        yGenOut = y1+outline
                    else:
                        xGenOut = x2
                        yGenOut = y2-outline

            return xGenOut, yGenOut

        elif realPosSquare > longRadiusSquare:
            aX = 1 + lineK*lineK
            bX = 2*lineK*(lineB - circlePos[1]) - 2*circlePos[0]
            cX = circlePos[0]*circlePos[0] + (lineB - circlePos[1])*(lineB - circlePos[1]) - longRadiusSquare

            resultX = bX*bX - 4*aX*cX
            x1 = (-bX + np.sqrt(resultX))/(2*aX)
            x2 = (-bX - np.sqrt(resultX))/(2*aX)

            y1 = lineK*x1 + lineB
            y2 = lineK*x2 + lineB

            if posInput[0] > circlePos[0]:
                if x1 > circlePos[0]:
                    xGenOut = x1-outline
                    yGenOut = y1
                else:
                    xGenOut = x2+outline
                    yGenOut = y2
            elif posInput[0] < circlePos[0]:
                if x1 < circlePos[0]:
                    xGenOut = x1+outline
                    yGenOut = y1
                else:
                    xGenOut = x2-outline
                    yGenOut = y2
            elif posInput[0] == circlePos[0]:
                if posInput[1] > circlePos[1]:
                    if y1 > circlePos[1]:
                        xGenOut = x1
                        yGenOut = y1-outline
                    else:
                        xGenOut = x2
                        yGenOut = y2+outline

            return xGenOut, yGenOut


def planeLinkageReverse(linkageLen, linkageEnDe, debugPos, goalPos): #E
    goalPos[0] = goalPos[0] + debugPos[0]
    goalPos[1] = goalPos[1] + debugPos[1]

    AngleEnD = np.arctan(linkageEnDe/linkageLen[1])*180/np.pi

    linkageLenREAL = np.sqrt(((linkageLen[1]*linkageLen[1])+(linkageEnDe*linkageEnDe)))

    goalPos[0],goalPos[1] = limitCheck(goalPos, debugPos, [linkageLen[0],linkageLenREAL], 0.00001)

    if goalPos[0] < 0:
        goalPos[0] = - goalPos[0]
        mGenOut = linkageLenREAL*linkageLenREAL-linkageLen[0]*linkageLen[0]-goalPos[0]*goalPos[0]-goalPos[1]*goalPos[1]
        nGenOut = mGenOut/(2*linkageLen[0])

        angleGenA = np.arctan(goalPos[1]/goalPos[0])+np.arcsin(nGenOut/np.sqrt(goalPos[0]*goalPos[0]+goalPos[1]*goalPos[1]))
        angleGenB = np.arcsin((goalPos[1]-linkageLen[0]*np.cos(angleGenA))/linkageLenREAL)-angleGenA

        angleGenA = 90 - angleGenA*180/np.pi
        angleGenB = angleGenB*180/np.pi

        linkageLenC = np.sqrt((goalPos[0]*goalPos[0]+goalPos[1]*goalPos[1]))

        linkagePointC = np.arcsin(goalPos[0]/goalPos[1])*180/np.pi

        anglePosC = angleGenB + angleGenA

        return [int(angleGenA), int(angleGenB+AngleEnD), linkageLenC, linkagePointC, anglePosC]

    elif goalPos[0] == 0:
        angleGenA = np.arccos((linkageLen[0]*linkageLen[0]+goalPos[1]*goalPos[1]-linkageLenREAL*linkageLenREAL)/(2*linkageLen[0]*goalPos[1]))
        cGenOut = np.tan(angleGenA)*linkageLen[0]
        dGenOut = goalPos[1]-(linkageLen[0]/np.cos(angleGenA))
        angleGenB = np.arccos((cGenOut*cGenOut+linkageLenREAL*linkageLenREAL-dGenOut*dGenOut)/(2*cGenOut*linkageLenREAL))

        angleGenA = - angleGenA*180/np.pi + 90
        angleGenB = - angleGenB*180/np.pi

        linkageLenC = np.sqrt((goalPos[0]*goalPos[0]+goalPos[1]*goalPos[1]))

        linkagePointC = angleGenB + 90 - angleGenA

        anglePosC = angleGenB + angleGenA

        return [int(angleGenA), int(angleGenB+AngleEnD), linkageLenC, linkagePointC, anglePosC]

    elif goalPos[0] > 0:
        sqrtGenOut = np.sqrt(goalPos[0]*goalPos[0]+goalPos[1]*goalPos[1])
        nGenOut = (linkageLen[0]*linkageLen[0]+goalPos[0]*goalPos[0]+goalPos[1]*goalPos[1]-linkageLenREAL*linkageLenREAL)/(2*linkageLen[0]*sqrtGenOut)
        angleA = np.arccos(nGenOut)*180/np.pi

        AB = goalPos[1]/goalPos[0]

        angleB = np.arctan(AB)*180/np.pi
        angleGenA = angleB - angleA

        mGenOut = (linkageLen[0]*linkageLen[0]+linkageLenREAL*linkageLenREAL-goalPos[0]*goalPos[0]-goalPos[1]*goalPos[1])/(2*linkageLen[0]*linkageLenREAL)
        angleGenB = np.arccos(mGenOut)*180/np.pi - 90

        linkageLenC = np.sqrt((goalPos[0]*goalPos[0]+goalPos[1]*goalPos[1]))

        # linkagePointC = np.arcsin(goalPos[1]/goalPos[0])*180/np.pi*servoDirection[servoNumCtrl[0]]
        linkagePointC = 0

        anglePosC = angleGenB + angleGenA

        return [int(angleGenA), int(angleGenB+AngleEnD), linkageLenC, linkagePointC, anglePosC]


class RaspArmS(threading.Thread):

    def __init__(self, *args, **kwargs):
        super(RaspArmS, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()
        self.__flag.clear()

        '''
       	import config file.
        '''
        self.initPosIndex   = 0
        self.servoPortIndex = 1
        self.configJsonFile = open(thisPath + 'config.json', 'r')
        print(thisPath + 'config.json')
        self.contentJson  = self.configJsonFile.read()
        self.configJson   = json.loads(self.contentJson)
        print(self.configJson)

        '''
        Len:
             A  B/'\
            ___./   C---
        BASE           |D

        Servo:
             A  B/'\
            ___./   C-D-
        BASE             
        '''
        self.linkageLenA = 44.42
        self.linkageLenB = 67.00
        self.linkageLenC = 112.0
        self.linkageLenD = 9.0

        '''
        import config data.
        '''
        try:
            self.initPosA = int(self.configJson[self.initPosIndex]['initPosA'])
            self.initPosB = int(self.configJson[self.initPosIndex]['initPosB'])
            self.initPosC = int(self.configJson[self.initPosIndex]['initPosC'])
            self.initPosD = int(self.configJson[self.initPosIndex]['initPosD'])

            print('Import config [initPos]:\ninitPosA:%d\ninitPosB:%d\ninitPosC:%d\ninitPosD:%d'%(self.initPosA,self.initPosB,self.initPosC,self.initPosD))
            print('--- --- ---')
        except:
            self.initPosA = 300
            self.initPosB = 300
            self.initPosC = 300
            self.initPosD = 300

            print('Import config [initPos] failed.')
            print('--- --- ---')

        try:
            self.servoNumA = int(self.configJson[self.servoPortIndex]['servoNumA'])
            self.servoNumB = int(self.configJson[self.servoPortIndex]['servoNumB'])
            self.servoNumC = int(self.configJson[self.servoPortIndex]['servoNumC'])
            self.servoNumD = int(self.configJson[self.servoPortIndex]['servoNumD'])

            print('Import config [servoPort]:\nservoNumA:%d\nservoNumB:%d\nservoNumC:%d\nservoNumD:%d'%(self.servoNumA,self.servoNumB,self.servoNumC,self.servoNumD))
            print('--- --- ---')
        except:
            self.servoNumA = 12
            self.servoNumB = 13
            self.servoNumC = 14
            self.servoNumD = 15

            print('Import config [servoPort] failed.')

        '''
        'gripper' 'pen'
        '''
        self.modeNow = 'gripper'

        '''
        speed range 0-100
        '''
        self.moveSpeed = 100

        '''
        change direction here 0/1
        '''
        self.scDirection = [1, 1, 1, 1]

        '''
        servo initialization
        '''
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(50)

        '''
        pos data.
        '''
        self.oldXYZ = [0, 100, 0, 0]
        self.nowXYZ = [0, 100, 0, 0]
        self.aimXYZ = [0, 100, 0, 0]

        '''
        planDataSaved
        '''
        self.planJsonFile = open(thisPath + 'plan.json', 'r')
        print(thisPath + 'plan.json')
        self.contentPlan  = self.planJsonFile.read()
        self.planSave = json.loads(self.contentPlan)

        '''
        planDataNow
        '''
        self.planData = self.planSave

        '''
        axis commands.'+'/'-'/'stop'
        '''
        self.axisCommandX = 'stop'
        self.axisCommandY = 'stop'
        self.axisCommandZ = 'stop'
        self.axisCommandG = 'stop'

        '''
        mission:'stop'/'simpleMove'/'planMove'
        '''
        self.globalCommand = 'stop'

        '''
        pos saved here.
        '''
        self.nowPos = [0, 100, 0, 0]


    def savePlanJson(self):
        content2write = json.dumps(planGoseList)
        file2write = open('plan.json', 'w')
        file2write.write(content2write)
        print(content2write)
        file2write.close()


    def createNewPlan(self):
        global planGoseList
        planGoseList = []


    def newPlanAppend(self):
        global planGoseList
        print(planGoseList)
        posAppend = [None]*4
        for i in range(0, 4):
            posAppend[i] = self.nowPos[i]
        planGoseList.append(posAppend)
        print(planGoseList)


    def servoCtrl(self, initPos, servoNumInput, angleInput, directionInput):
        scOut = int(round(((ctrlRangeMax-ctrlRangeMin)/angleRange*angleInput),0))
        self.pwm.set_pwm(servoNumInput, 0, (initPos + scOut*directionInput))
        return scOut


    def servoAngInput(self, angleInput):
        self.servoCtrl(self.initPosA, self.servoNumA, angleInput[0], 1)
        self.servoCtrl(self.initPosB, self.servoNumB, angleInput[1], 1)
        self.servoCtrl(self.initPosC, self.servoNumC, angleInput[2], 1)
        self.servoCtrl(self.initPosD, self.servoNumD, angleInput[3], 1)


    def servoInitSet(self):
        print('Input your command here\n"w":pwm+\n"s":pwm-\n"q":servo+\n"a":servo-\n"x":set\n"c":cancel')
        servoList = [self.servoNumA, self.servoNumB, self.servoNumC, self.servoNumD]

        posBuffer = [self.initPosA, self.initPosB, self.initPosC, self.initPosD]
        servoNowSelected = 0
        while 1:
            command = input('"___"\nservoNum:%d is selected\nPWM:%d'%(servoList[servoNowSelected], posBuffer[servoNowSelected]))
            if command == 'w':
                posBuffer[servoNowSelected] += 1
            elif command == 's':
                posBuffer[servoNowSelected] -= 1
            elif command == 'q':
                servoNowSelected += 1
            elif command == 'a':
                servoNowSelected -= 1
            elif command == 'x':
                self.initPosA = posBuffer[0]
                self.initPosB = posBuffer[1]
                self.initPosC = posBuffer[2]
                self.initPosD = posBuffer[3]

                self.configJson[self.initPosIndex]['initPosA'] = self.initPosA
                self.configJson[self.initPosIndex]['initPosB'] = self.initPosB
                self.configJson[self.initPosIndex]['initPosC'] = self.initPosC
                self.configJson[self.initPosIndex]['initPosD'] = self.initPosD

                content2write = json.dumps(self.configJson)
                file2write = open(thisPath + 'config.json', 'w')
                file2write.write(content2write)
                file2write.close()

                print('Config New PWM.')
                break
            elif command == 'c':
                print('Config Cancel.')
                break
            else:
                print('Input your command here\n"w":pwm+\n"s":pwm-\n"q":servo+\n"a":servo-\n"x":set\n"c":cancel')
            
            if servoNowSelected > 3:
                servoNowSelected = 0
            elif servoNowSelected < 0:
                servoNowSelected = 3

            self.pwm.set_pwm(servoList[servoNowSelected], 0, posBuffer[servoNowSelected])


    def changeMode(self, modeNameInput):
        if modeNameInput == 'gripper' or modeNameInput == 'pen':
            self.modeName = modeNameInput
        else:
            print('Invalide modeNameInput.')


    def changeSpeed(self, moveSpeedInput):
        if moveSpeedInput <= 100 and moveSpeedInput > 0:
            self.moveSpeed = moveSpeedInput
        else:
            print('Invalide moveSpeedInput.')


    def moveXYZ(self, newXYZInput):
        oldXYZInput = self.oldXYZ
        offsetX = newXYZInput[0] - oldXYZInput[0]
        offsetY = newXYZInput[1] - oldXYZInput[1]
        offsetZ = newXYZInput[2] - oldXYZInput[2]

        self.gripper(newXYZInput[3])
        self.oldXYZ[3] = newXYZInput[3]
        maxOffset = max(abs(offsetX), abs(offsetY), abs(offsetZ))

        # print('---------')
        # print(newXYZInput)
        for i in range(0, int(maxOffset)):
            if self.globalCommand == 'stop':
                self.pause()
                break
            genX = newXYZInput[0]
            if offsetX:
                genX = oldXYZInput[0] + ((newXYZInput[0]-oldXYZInput[0])*(i/maxOffset))
            genY = newXYZInput[1]
            if offsetY:
                genY = oldXYZInput[1] + ((newXYZInput[1]-oldXYZInput[1])*(i/maxOffset))
            genZ = newXYZInput[2]
            if offsetZ:
                genZ = oldXYZInput[2] + ((newXYZInput[2]-oldXYZInput[2])*(i/maxOffset))

            # print([genX, genY, genZ, newXYZInput[3]])
            self.xyzInput([genX, genY, genZ, newXYZInput[3]])
            time.sleep(0.1/(self.moveSpeed+0.000001))

        self.oldXYZ[0] = newXYZInput[0]
        self.oldXYZ[1] = newXYZInput[1]
        self.oldXYZ[2] = newXYZInput[2]


    def gripper(self, command):
        if command == 'catch':
            ras.servoCtrl(ras.initPosD, ras.servoNumD, 90, 1)
            self.nowPos[3] = 90
        elif command == 'loose':
            ras.servoCtrl(ras.initPosD, ras.servoNumD, 0, -1)
            self.nowPos[3] = 0
        else:
            try:
                ras.servoCtrl(ras.initPosD, ras.servoNumD, command, 1)
                self.nowPos[3] = command
            except:
                pass


    def planGoes(self):
        self.globalCommand = 'planMove'
        for i in range(0, len(planGoseList)):
            # print(len(planGoseList))
            if self.globalCommand == 'stop':
                self.pause()
                break
            # print('-------------')
            # print(planGoseList)
            # print('=============')
            # print(planGoseList[i])
            self.moveXYZ(planGoseList[i])


    def xyzInput(self, xyzPosInput):
        allLengh = np.sqrt(xyzPosInput[0]*xyzPosInput[0] + xyzPosInput[1]*xyzPosInput[1])
        planeY   = allLengh - self.linkageLenA
        self.servoCtrl(self.initPosD, self.servoNumD, xyzPosInput[3], 1)
        self.nowPos[3] = int(xyzPosInput[3])

        if xyzPosInput[0] > 0:
            genoutA = np.arctan(xyzPosInput[1]/xyzPosInput[0])*180/np.pi-90
        elif xyzPosInput[0] < 0:
            genoutA = - np.arctan(abs(xyzPosInput[1])/abs(xyzPosInput[0]))*180/np.pi+90
        else:
            genoutA = 0
        try:
            genoutBC = planeLinkageReverse([self.linkageLenB, self.linkageLenC], self.linkageLenD, [0,0], [xyzPosInput[2], planeY])
            self.servoCtrl(self.initPosA, self.servoNumA, genoutA, 1)
            self.servoCtrl(self.initPosB, self.servoNumB, genoutBC[0], -1)
            self.servoCtrl(self.initPosC, self.servoNumC, genoutBC[1], 1)
            self.nowPos[0] = int(xyzPosInput[0])
            if xyzPosInput[1] > 150:
                self.nowPos[1] = 150
            else:
                self.nowPos[1] = int(xyzPosInput[1])
            self.nowPos[2] = int(xyzPosInput[2])
            if self.modeNow == 'pen':
                # self.nowPos[3] = int(90 - genoutBC[0] - genoutBC[1])
                self.nowPos[3] = int(90 - genoutBC[0] - genoutBC[1])
                # self.servoCtrl(self.initPosD, self.servoNumD, self.nowPos[3], 1)
                self.servoCtrl(self.initPosD, self.servoNumD, int(90 - genoutBC[0] - genoutBC[1]), 1)
            # print('done')
        except:
            pass


    def simpleMoveStart(self, axis, direction):
        if axis == 'X':
            self.axisCommandX = direction
        elif axis == 'Y':
            self.axisCommandY = direction
        elif axis == 'Z':
            self.axisCommandZ = direction
        elif axis == 'G':
            self.axisCommandG = direction

        if self.axisCommandX != 'stop' or self.axisCommandY != 'stop' or self.axisCommandZ != 'stop' or self.axisCommandG != 'stop':
            self.globalCommand = 'simpleMove'
            self.resume()
        else:
            self.globalCommand = 'stop'
            self.pause()


    def simpleMoveThreading(self):
        if self.axisCommandX == '+':
            self.aimXYZ[0] += 1
        elif self.axisCommandX == '-':
            self.aimXYZ[0] -= 1

        if self.axisCommandY == '+':
            self.aimXYZ[1] += 1
        elif self.axisCommandY == '-':
            self.aimXYZ[1] -= 1

        if self.axisCommandZ == '+':
            self.aimXYZ[2] += 1
        elif self.axisCommandZ == '-':
            self.aimXYZ[2] -= 1

        if self.axisCommandG == '+':
            self.aimXYZ[3] += 1
        elif self.axisCommandG == '-':
            self.aimXYZ[3] -= 1

        self.xyzInput(self.aimXYZ)


    def moveThreadingStop(self):
        self.globalCommand = 'stop'
        self.pause()


    def planThreadingStart(self):
        self.globalCommand = 'planMove'
        self.resume()


    def pause(self):
        self.__flag.clear()


    def resume(self):
        self.__flag.set()


    def run(self):
        while 1:
            self.__flag.wait()
            if self.globalCommand == 'simpleMove':
                self.simpleMoveThreading()
            if self.globalCommand == 'planMove':
                self.planGoes()
            if self.globalCommand == 'stop':
                self.pause()




if __name__ == '__main__':
    ras = RaspArmS()
    ras.start()

    while 1:

        # ras.simpleMoveStart('X','+')
        # time.sleep(1.5)
        # ras.moveThreadingStop()
        # ras.simpleMoveStart('X','stop')
        # time.sleep(1)
        # ras.simpleMoveStart('X','-')
        # time.sleep(1.5)
    #     ras.simpleMoveStart('X','stop')
    #     ras.gripper('catch')
    #     time.sleep(1)
    #     ras.gripper('loose')
    #     time.sleep(1)

        ras.planGoes(ras.planData)
        # ras.gripper(0)
        # time.sleep(1)
        # ras.gripper(-90)
        # time.sleep(1)



    # while 1：
    #     if websocket == 'X+':
    #         ras.simpleMoveStart('X','+')
    #     elif websocket == 'XS':
    #         ras.simpleMoveStart('X','stop')
    #     if websocket == 'S 50':
    #         ras.moveSpeed = intNum
        # print(ras.oldXYZ)
        # ras.moveXYZ([90, 140, 0])
        # print(ras.oldXYZ)
        # ras.moveXYZ([-90,140, 0])
        # ras.xyzInput([90, 140, 0])
        # time.sleep(1)
        # ras.xyzInput([0, 140, 0])
        # time.sleep(1)
        # ras.xyzInput([-90, 140, 0])
        # time.sleep(1)

        # for i in range(-90,90):
        #     ras.xyzInput([i, 140, 0])
        # time.sleep(1)
        # for i in range(90,-90,-1):
        #     ras.xyzInput([i, 140, 0])
        # time.sleep(1)

    # ras.servoInitSet()

    # while 1:
    #     a = planeLinkageReverse([67.00, 112.0], 9.0, [0,0], [-100, 120])
    #     print(a)
    #     print(ras.servoCtrl(ras.initPosB, ras.servoNumB, a[0], -1))
    #     print(ras.servoCtrl(ras.initPosC, ras.servoNumC, a[1], 1))
    #     time.sleep(1)
    #     a = planeLinkageReverse([67.00, 112.0], 9.0, [0,0], [-50, 120])
    #     print(a)
    #     print(ras.servoCtrl(ras.initPosB, ras.servoNumB, a[0], -1))
    #     print(ras.servoCtrl(ras.initPosC, ras.servoNumC, a[1], 1))
    #     time.sleep(1)
    #     a = planeLinkageReverse([67.00, 112.0], 9.0, [0,0], [0, 120])
    #     print(a)
    #     print(ras.servoCtrl(ras.initPosB, ras.servoNumB, a[0], -1))
    #     print(ras.servoCtrl(ras.initPosC, ras.servoNumC, a[1], 1))
    #     time.sleep(2)

        # for i in range(0,50):
        #     a = planeLinkageReverse([67.00, 112.0], 9.0, [0,0], [67-i, 112])
        #     print(a)
        #     print(ras.servoCtrl(ras.initPosB, ras.servoNumB, a[0], -1))
        #     print(ras.servoCtrl(ras.initPosC, ras.servoNumC, a[1], 1))
        #     time.sleep(0.01)
        # for i in range(0,50):
        #     a = planeLinkageReverse([67.00, 112.0], 9.0, [0,0], [17+i, 112])
        #     print(a)
        #     print(ras.servoCtrl(ras.initPosB, ras.servoNumB, a[0], -1))
        #     print(ras.servoCtrl(ras.initPosC, ras.servoNumC, a[1], 1))
        #     time.sleep(0.01)
        # time.sleep(2)
    # while 1:
    #     ras.servoCtrl(ras.initPosC, ras.servoNumC, 0, 1)
    #     time.sleep(1)
    #     ras.servoCtrl(ras.initPosC, ras.servoNumC, 45, 1)
    #     time.sleep(2)

    # newJson()