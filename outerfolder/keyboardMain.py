from servoCTL import * 
import time
import signal




def main():

	servoCtl = ServoCTL()
	servoCtl.reset()
	robot = TangoBot(servoCtl,1/30)

	# If program crashes, attempt to stop the motors
	def ctrl_handler(signum, frm):
		servoCtl.reset()
		exit()
	signal.signal(signal.SIGINT, ctrl_handler)

	forwardSpeed = 0
	turnSpeed = 0

	headYaw = 0
	headPitch = 0
	bodyYaw = 0

	while True:
		key = read_single_keypress() 
		if(len(key) == 3): # Special Key codes for arrow keys
			print(key)
			if(key[2] == "A"): # Up arrow key
				# Rotate head up
				headPitch += 0.2
				if (headPitch > 1):
					headPitch = 1
				robot.setValue(SERVO_HEAD_PITCH, headPitch)
			elif(key[2] == "B"): # Down arrow key
				# Rotate head down
				headPitch -= 0.2
				if (headPitch < -1):
					headPitch = -1
				robot.setValue(SERVO_HEAD_PITCH, headPitch)
			elif(key[2] == "C"): # Right arrow key
				# Turn head right
				headYaw += 0.2
				if (headYaw > 1):
					headYaw = 1
				robot.setValue(SERVO_HEAD_YAW, headYaw)
			elif(key[2] == "D"): # Left arrow key
				# Turn head left
				headYaw -= 0.2
				if (headYaw < -1):
					headYaw = -1
				robot.setValue(SERVO_HEAD_YAW, headYaw)
			else:
				print("Unknown Key: ", key[2])
		else:
			if(key[0] == " "):
				# Stop moving
				robot.setValue(SERVO_THROTTLE, 0)
				robot.setValue(SERVO_STEERING, 0)
				forwardSpeed = 0
				turnSpeed = 0
			elif(key[0] == "w"):
				# Increment forward speed
				forwardSpeed += 1
				if (forwardSpeed > 3):
					forwardSpeed = 3
				robot.setValue(SERVO_THROTTLE, get_speed(forwardSpeed))
			elif(key[0] == "s"):
				# Decrement forward speed
				forwardSpeed -= 1
				if (forwardSpeed < -3):
					forwardSpeed = -3
				robot.setValue(SERVO_THROTTLE, get_speed(forwardSpeed))
			elif(key[0] == "a"):
				# Increment left turn speed
				turnSpeed += 1
				if (turnSpeed > 3):
					turnSpeed = 3
				robot.setValue(SERVO_STEERING, get_speed(turnSpeed))
			elif(key[0] == "d"):
				# Decrement left turn speed
				turnSpeed -= 1
				if (turnSpeed < -3):
					turnSpeed = -3
				robot.setValue(SERVO_STEERING, get_speed(turnSpeed))
			elif(key[0] == "q"):
				# Rotate body left
				bodyYaw += 0.3
				if (bodyYaw > 0.9):
					bodyYaw = 0.9
				robot.setValue(SERVO_TORSO, bodyYaw)
			elif(key[0] == "e"):
				# Rotate body right
				bodyYaw -= 0.3
				if (bodyYaw < -0.9):
					bodyYaw = -0.9
				robot.setValue(SERVO_TORSO, bodyYaw)
			elif(key[0] == "\x1b"):
				# Stop all movement and exit
				servoCtl.reset()
				break
			else:
				# Unknown key
				print("Unknown key: ", key[0])

	print("STOP")
	servoCtl.reset()
	robot.stop()

def get_speed(speedIndex):
	speedVals = [0, 0.5, 0.75, 1]
	isNegative = speedIndex < 0

	val = speedVals[abs(speedIndex)]
	if (isNegative):
		val *= -1
	return val 
		
# Keyboard input functionality sources from: 
# https://www.editcode.net/forum.php?mod=viewthread&tid=249333&extra=&mobile=1
def read_single_keypress():
	import termios, fcntl, sys, os
	fd = sys.stdin.fileno()
	# save old state
	flags_save = fcntl.fcntl(fd, fcntl.F_GETFL)
	attrs_save = termios.tcgetattr(fd)
	# make raw - the way to do this comes from the termios(3) man page.
	attrs = list(attrs_save) # copy the stored version to update
	# iflag
	attrs[0] &= ~(termios.IGNBRK | termios.BRKINT | termios.PARMRK
				  | termios.ISTRIP | termios.INLCR | termios. IGNCR
				  | termios.ICRNL | termios.IXON )
	# oflag
	attrs[1] &= ~termios.OPOST
	# cflag
	attrs[2] &= ~(termios.CSIZE | termios. PARENB)
	attrs[2] |= termios.CS8
	# lflag
	attrs[3] &= ~(termios.ECHONL | termios.ECHO | termios.ICANON
				  | termios.ISIG | termios.IEXTEN)
	termios.tcsetattr(fd, termios.TCSANOW, attrs)
	# turn off non-blocking
	fcntl.fcntl(fd, fcntl.F_SETFL, flags_save & ~os.O_NONBLOCK)
	# read a single keystroke
	ret = []
	try:
		ret.append(sys.stdin.read(1)) # returns a single character
		fcntl.fcntl(fd, fcntl.F_SETFL, flags_save | os.O_NONBLOCK)
		c = sys.stdin.read(1) # returns a single character
		while len(c) > 0:
			ret.append(c)
			c = sys.stdin.read(1)
	except KeyboardInterrupt:
		ret.append('\x03')
	finally:
		# restore old state
		termios.tcsetattr(fd, termios.TCSAFLUSH, attrs_save)
		fcntl.fcntl(fd, fcntl.F_SETFL, flags_save)
	return tuple(ret)
	

time.sleep(1)
main()
exit()
