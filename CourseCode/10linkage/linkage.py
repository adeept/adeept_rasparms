import numpy as np 
from matplotlib import pyplot as plt 
import matplotlib.animation as animation

'''
Here defines the distance between the A-axis of the steering gear and the steering gear axis responsible for left and right swings. This distance is determined by the structure and cannot be changed
'''
linkageLenC = 40

'''
Define the position of the oscillating steering gear here to correct the initial position error, generally 0 is enough
'''
linkageLenD = 0
linkageLenE = 0

'''
Set the size of the text
'''
sizeFont = 7

'''
Define the number and direction of the servo
'''
servoNumCtrl = [0,1]
servoDirection = [1,-1]


'''
This function is used to input the three-dimensional coordinates of the end point of the connecting rod, and return the rotation angle of the left and right swing servo and the length of the yellow line segment
Important: The length of the yellow line segment is the X value of the link inverse solution function in the previous course, and the Z value here is the Y value in the link inverse solution function in the previous course
'''
def bodyCoordinatePointCtrl(x, y, z):
	x = x - linkageLenE/2
	y = y + linkageLenD/2
	y = -y

	if x == 0:
		angleGenC = 0.0
		endX = abs(y - linkageLenC)
	elif y == 0:
		angleGenC = 90
		endX = abs(x - linkageLenC)
	elif y < 0:
		angleGenC = -np.arctan(y/x)
		endX = abs(-y/np.sin(angleGenC)-linkageLenC)
		angleGenC = angleGenC*180/np.pi + 90
	else:
		angleGenC = np.arctan(x/y)
		endX = abs(x/np.sin(angleGenC)-linkageLenC)
		angleGenC = angleGenC*180/np.pi

	angleGenC = - angleGenC

	return -angleGenC, endX


'''
The function used to draw the line segment is the same as the previous lesson
'''
def animateLine(xInput, yInput, lineLen, angleInput, debugInput):
	angleOri = angleInput
	debugOri = debugInput

	aOut = angleInput + debugInput

	angleLine = aOut

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
Initialize animation segments
'''
fig = plt.figure(tight_layout=True)
line_1, = plt.plot([],[],'o-',lw=2)
line_2, = plt.plot([],[],'o-',lw=2)
line_3, = plt.plot([],[],'o-',lw=2)

'''
Initialize animated text
'''
textPoint_A = plt.text(4, 0.8, '', fontsize=sizeFont)
textPoint_B = plt.text(4, 0.8, '', fontsize=sizeFont)
textPoint_C = plt.text(4, 0.8, '', fontsize=sizeFont)
textPoint_D = plt.text(4, 0.8, '', fontsize=sizeFont)


'''
Generate animation, the i value inside the function is the input variable
'''
def animate(i):
	'''
	Return the rotation angle of the left and right swing servo and the length of the yellow line segment
	'''
	a = bodyCoordinatePointCtrl(100-i, -130, 60)

	'''
	Call the animateLine() function to draw the line segment
	'''
	[x1,y1,a1] = animateLine(linkageLenE/2, -linkageLenD/2, linkageLenC, a[0], -90)
	[x2,y2,a2] = animateLine(x1[1],y1[1],a[1],0,a1)

	'''
	Apply animation to linkage
	'''
	line_1.set_data(x1,y1)
	line_2.set_data(x2,y2)

	'''
	Show some key information on the connecting rod
	'''
	textPoint_A.set_text("x=%.1f, y=%.1f , ang=%.1f"%(linkageLenE/2, linkageLenD/2, a[0]*servoDirection[servoNumCtrl[0]]))
	textPoint_B.set_text("x=%.1f, y=%.1f , ang=%.1f"%(x1[1], y1[1], a[1]*servoDirection[servoNumCtrl[1]]))
	textPoint_C.set_text("x=%.1f, y=%.1f , angBase=%.1f"%(x2[1], y2[1], a2))

	'''
	Text application animation
	'''
	textPoint_A.set_position((linkageLenE/2, -linkageLenD/2))
	textPoint_B.set_position((x1[1], y1[1]))
	textPoint_C.set_position((x2[1], y2[1]))

	'''
	Note here that there must be a',' after the last return value
	'''
	return line_1,line_2,textPoint_A,textPoint_B,textPoint_C,

'''
Initialize animation
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