import numpy as np 
'''
This program runs on the computer, just double click it
'''

'''
Import matplotlib
'''
from matplotlib import pyplot as plt 

'''
Import the library for animation
'''
import matplotlib.animation as animation

'''
The variables here are the same as those introduced in Chapter 24
'''
linkageLenA = 70
linkageLenB = 150.0

linkageLenDebug = 10

'''
This defines the initial position deviation of the robotic arm
'''
debugPosA = 0.0
debugPosB = 0.0

'''
Define the text size displayed here
'''
sizeFont = 7

servoNumCtrl = [0,1]
servoDirection = [1,-1]

linkageLenCtrl = [linkageLenA, linkageLenB]

'''
This function is the same as that introduced in Lesson 24, so I won’t introduce more here
'''
def planeLinkageReverse(linkageLen, linkageEnDe, servoNum, debugPos, goalPos): #E
	goalPos[0] = goalPos[0] + debugPos[0]
	goalPos[1] = goalPos[1] + debugPos[1]

	AngleEnD = np.arctan(linkageEnDe/linkageLen[1])*180/np.pi

	linkageLenREAL = np.sqrt(((linkageLen[1]*linkageLen[1])+(linkageEnDe*linkageEnDe)))

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


'''
This function is used to draw line segments
The input parameters are the initial coordinate point X and Y values of the line segment, the length of the line segment, the angle of the line segment, and the angle deviation
'''
def animateLine(xInput, yInput, lineLen, angleInput, debugInput):
	angleOri = angleInput
	debugOri = debugInput

	aOut = angleInput + debugInput

	angleLine = aOut
	# print(angleLine)
	'''
	Trigonometric calculation
	'''
	if angleLine < -360:
		angleLine = (-angleLine-360)*np.pi/180
		xOut = np.cos(angleLine)*lineLen + xInput
		yOut = -np.sin(angleLine)*lineLen + yInput

	elif angleLine < -180 and angleLine >= -360:
		angleLine = (-angleLine-180)*np.pi/180
		xOut = xInput - np.cos(angleLine)*lineLen
		yOut = yInput + np.sin(angleLine)*lineLen

	elif angleLine >= -180 and angleLine < -90:
		angleLine = (180+angleLine)*np.pi/180
		xOut = xInput - np.cos(angleLine)*lineLen
		yOut = yInput - np.sin(angleLine)*lineLen

	elif angleLine <=90 and angleLine >= -90:
		angleLine = angleLine*np.pi/180
		xOut = np.cos(angleLine)*lineLen + xInput
		yOut = np.sin(angleLine)*lineLen + yInput

	elif angleLine > 90 and angleLine <= 180:
		angleLine = (180 - angleLine)*np.pi/180
		xOut = xInput - np.cos(angleLine)*lineLen
		yOut = yInput + np.sin(angleLine)*lineLen

	elif angleLine > 180 and angleLine <= 360:
		angleLine = (angleLine - 180)*np.pi/180
		xOut = xInput - np.cos(angleLine)*lineLen
		yOut = yInput - np.sin(angleLine)*lineLen

	elif angleLine > 360:
		angleLine = (angleLine-360)*np.pi/180
		xOut = np.cos(angleLine)*lineLen + xInput
		yOut = np.sin(angleLine)*lineLen + yInput

	else:
		print('Out of Range')

	return [[xInput,xOut],[yInput,yOut],aOut]


'''
Here initialize the link segment to be moved
'''
fig = plt.figure(tight_layout=True)
line_1, = plt.plot([],[],'o-',lw=2)
line_2, = plt.plot([],[],'o-',lw=2)
line_3, = plt.plot([],[],'o-',lw=2)

'''
Initialize the text to be displayed here
'''
textPoint_A = plt.text(4, 0.8, '', fontsize=sizeFont)
textPoint_B = plt.text(4, 0.8, '', fontsize=sizeFont)
textPoint_C = plt.text(4, 0.8, '', fontsize=sizeFont)
textPoint_D = plt.text(4, 0.8, '', fontsize=sizeFont)

'''
Animation function
'''
def animate(i):
	'''
	Call the planeLinkageReverse() function to get the rotation angle of the A and B servos. Note that there is a variable i, which is used to make animations, which will be explained later
	'''
	a = planeLinkageReverse(linkageLenCtrl, linkageLenDebug, servoNumCtrl, [20,20], [150,-100+i])

	'''
	Call the animateLine() function to draw the line segment
	'''
	[x1,y1,a1] = animateLine(20, 20, linkageLenA, a[0], 180)
	[x2,y2,a2] = animateLine(x1[1],y1[1],linkageLenB,a[1],a1+90)
	[x3,y3,a3] = animateLine(x2[1],y2[1],linkageLenDebug,a2,90)

	'''
	Apply animation to linkage
	'''
	line_1.set_data(x1,y1)
	line_2.set_data(x2,y2)
	line_3.set_data(x3,y3)

	'''
	Show some key information on the connecting rod
	'''
	textPoint_A.set_text("x=%.1f, y=%.1f , ang=%.1f"%(debugPosA, debugPosB, a[0]*servoDirection[servoNumCtrl[0]]))
	textPoint_B.set_text("x=%.1f, y=%.1f , ang=%.1f"%(x1[1], y1[1], a[1]*servoDirection[servoNumCtrl[1]]))
	textPoint_C.set_text("x=%.1f, y=%.1f , angBase=%.1f"%(x2[1], y2[1], a2))
	textPoint_D.set_text("x=%.1f, y=%.1f , angBase=%.1f"%(x3[1], y3[1], a3))

	'''
	Text application animation
	'''
	textPoint_A.set_position((20, 20))
	textPoint_B.set_position((x1[1], y1[1]))
	textPoint_C.set_position((x2[1], y2[1]))
	textPoint_D.set_position((x3[1], y3[1]))

	'''
	Note here that there must be a',' after the last return value
	'''
	return line_1,line_2,line_3,textPoint_A,textPoint_B,textPoint_C,textPoint_D,

'''
Animation initialization
'''
def initAnimate():
	line_1.set_data([],[])
	line_2.set_data([],[])
	return line_1,line_2,

'''
Create a new artboard for animation drawing
'''
plt.axis("equal")
plt.grid()
plt.grid(ls="--")
plt.xlim(-200,200)
plt.ylim(-200,200)

'''
Apply animation here, define range(), determine the range of animation variables
'''
ani = animation.FuncAnimation(fig, animate, range(0, 200),
                interval=10, blit=True, init_func=initAnimate)

'''
Display simulation motion model
'''
plt.show()
