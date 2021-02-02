'''
This program can be run by double clicking on the computer

Import math function library
'''
import numpy as np 




import time

'''
As shown in the pictures in this folder
ABCD constitutes a simple connecting rod, where the rotation of point A and point B is driven by the servo
The connecting rod CD and the connecting rod BC are at a fixed right angle, and the connecting rod CD is used to compensate the error of the end point of the connecting rod
'''
linkageLenA = 70		# AB length
linkageLenB = 150.0		# BC length

linkageLenDebug = 10	# CD length

servoNumCtrl = [0,1]	# AB Two Servo Number
servoDirection = [1,-1]	# Corresponding to the direction of movement of the two servos AB, set by 1 and -1

# Array of connecting rod AB and BC length
linkageLenCtrl = [linkageLenA, linkageLenB]


'''
This function is used to input the length of the connecting rod and the error parameters, the end position of the connecting rod and the number of the servos, and the rotation angle of the two servos AB of this connecting rod mechanism can be obtained.
'''
def planeLinkageReverse(linkageLen, linkageEnDe, servoNum, debugPos, goalPos):
	'''
	Incremental error calculation, use debugPos to correct the initial position error, generally debugPos is [0,0]
	'''
	goalPos[0] = goalPos[0] + debugPos[0]
	goalPos[1] = goalPos[1] + debugPos[1]

	'''
	Used to calculate the angle error between the end point of the connecting rod and the rotation axis of the steering gear B
	'''
	AngleEnD = np.arctan(linkageEnDe/linkageLen[1])*180/np.pi

	'''
	Abstract the input links AB, BC, and CD into AB, BD, which is convenient for subsequent calculations
	'''
	linkageLenREAL = np.sqrt(((linkageLen[1]*linkageLen[1])+(linkageEnDe*linkageEnDe)))

	'''
	Here is the trigonometric function calculation
	'''
	if goalPos[0] < 0:
		goalPos[0] = - goalPos[0]
		mGenOut = linkageLenREAL*linkageLenREAL-linkageLen[0]*linkageLen[0]-goalPos[0]*goalPos[0]-goalPos[1]*goalPos[1]
		nGenOut = mGenOut/(2*linkageLen[0])

		angleGenA = np.arctan(goalPos[1]/goalPos[0])+np.arcsin(nGenOut/np.sqrt(goalPos[0]*goalPos[0]+goalPos[1]*goalPos[1]))
		angleGenB = np.arcsin((goalPos[1]-linkageLen[0]*np.cos(angleGenA))/linkageLenREAL)-angleGenA

		angleGenA = 90 - angleGenA*180/np.pi
		angleGenB = angleGenB*180/np.pi

		linkageLenC = np.sqrt((goalPos[0]*goalPos[0]+goalPos[1]*goalPos[1]))

		linkagePointC = np.arcsin(goalPos[0]/goalPos[1])*180/np.pi*servoDirection[servoNumCtrl[0]]

		anglePosC = angleGenB + angleGenA

		return [angleGenA*servoDirection[servoNumCtrl[0]], (angleGenB+AngleEnD)*servoDirection[servoNumCtrl[1]], linkageLenC, linkagePointC, anglePosC]

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

		return [angleGenA*servoDirection[servoNumCtrl[0]], (angleGenB+AngleEnD)*servoDirection[servoNumCtrl[1]], linkageLenC, linkagePointC, anglePosC]

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

		linkagePointC = 0

		anglePosC = angleGenB + angleGenA

		return [angleGenA*servoDirection[servoNumCtrl[0]], (angleGenB+AngleEnD)*servoDirection[servoNumCtrl[1]], linkageLenC, linkagePointC, anglePosC]


while 1:
	for i in range(0,200,10):
		output = planeLinkageReverse(linkageLenCtrl, linkageLenDebug, servoNumCtrl, [0,0], [150,-100+i])
		print('-----------------------')
		print('servoA:%f'%output[0])	# The rotation angle of servo A
		print('servoB:%f'%output[1])	# The rotation angle of steering gear B
		print('Length:%f'%output[2])	# AD length
		print('angleC:%f'%output[4])	# AD perspective
		time.sleep(1)