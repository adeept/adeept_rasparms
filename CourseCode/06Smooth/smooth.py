'''
Import the library used to control the steering gear
'''
import Adafruit_PCA9685
import time

'''
Instantiate the steering gear control object
'''
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

'''
Define three positions and let the servo move slowly to these positions in sequence
'''
servoPos_1 = 150
servoPos_2 = 400
servoPos_3 = 300

'''
Put these positions into the array
'''
posList = [servoPos_1, servoPos_2, servoPos_3]

'''
Define the port number of the servo you want to control
'''
servoNum = 12

'''
This is the initial position and the variable used to store the end point of the last movement of the servo
'''
lastPos = 300

'''
Enter a new position in the parameter of this function, the rudder will move smoothly from lastPos to newPosInput
'''
def smoothServo(newPosInput):
	'''
	Declare lastPos as a global variable
	'''
	global lastPos

	'''
	Calculate the difference between lastPos and newPosInput
	'''
	errorPos = newPosInput - lastPos

	'''
	Control the servo to move from lastPos to newPosInput little by little
	'''
	for i in range(0, abs(errorPos)):
		nowPos = int(lastPos + errorPos*i/abs(errorPos))
		pwm.set_pwm(servoNum, 0, nowPos)
		time.sleep(0.01)

	'''
	Update lastPos as the starting point of the next exercise
	'''
	lastPos = newPosInput
	pwm.set_pwm(servoNum, 0, lastPos)


def main():
	'''
	Main function, used to control the servo to move slowly to the three points in posList
	'''
	for j in posList:
		smoothServo(j)


if __name__ == '__main__':
	main()