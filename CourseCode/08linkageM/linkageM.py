import numpy as np 
'''
This program runs on the computer
pip install matplotlib
Install matplotlib
'''

'''
Import matplotlib
'''
from matplotlib import pyplot as plt 


'''
matplotlib itself has a library for drawing line segments. Enter a set of X and then enter a set of Y to draw the line
This routine is mainly used to test whether the library is installed successfully, and to understand the most basic operations of matplotlib
'''
def drawLine(pos1, pos2):
	'''
	Enter the coordinates pos1 of the initial point of the line segment and pos2 of the end point
	'''
	x = [pos1[0], pos2[0]]	# Array of X points
	y = [pos1[1], pos2[1]]	# Array of Y points
	plt.plot(x, y)			# Draw this line segment


drawLine([0,0], [2,2])	# Call the function and draw a line segment starting at (0,0) and ending at (2,2)
plt.show()	# show result