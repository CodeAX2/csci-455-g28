from servoCTL import * 
import time
import signal
import threading
from RoboGrammar import RoboGrammar
from VoiceAgent import VoiceAgent
from SpeechAgent import SpeechAgent


import speech_recognition as sr

import time, os, sys, contextlib

# @contextlib.contextmanager
# def ignoreStderr():
# 	devnull = os.open(os.devnull, os.O_WRONLY)
# 	old_stderr = os.dup(2)
# 	sys.stderr.flush()
# 	os.dup2(devnull, 2)
# 	os.close(devnull)
# 	try:
# 		yield
# 	finally:
# 		os.dup2(old_stderr, 2)
# 		os.close(old_stderr)




def main():
	
	# If program crashes, attempt to stop the motors
	def ctrl_handler(signum, frm):
		servoCtl.reset()
		exit()
	signal.signal(signal.SIGINT, ctrl_handler)
	
	servoCtl = ServoCTL()
	robot = TangoBot(servoCtl,1/30)

	srAgent = SpeechAgent(robot, servoCtl)
	vAgent = VoiceAgent()
	

	grammar = RoboGrammar(robot,srAgent,vAgent)


	servoCtl.reset()

	while True:
		
		key = read_single_keypress()
		time.sleep(1)

		if(key == None):
			continue
		if(len(key) == 3): # Special Key codes for arrow keys
			print(key)
			if(key[2] == "A"): # Up arrow key
				robot.headUp(1)
			elif(key[2] == "B"): # Down arrow key
				robot.headUp(-1)
			elif(key[2] == "C"): # Right arrow key
				robot.headRight(1)
			elif(key[2] == "D"): # Left arrow key
				robot.headRight(-1)
			else:
				print("Unknown Key: ", key[2])
		else:
			if(key[0] == " "):
				# Stop moving
				robot.safeStopMoving()
			elif(key[0] == "w"):
				_
				# robot.increaseSpeed()
			elif(key[0] == "s"):
				_
				# robot.increaseSpeed(-1)
			elif(key[0] == "a"):
				_
				# robot.rightTurnSpeed(-1)
			elif(key[0] == "d"):
				_
				# robot.rightTurnSpeed(1)
			elif(key[0] == "q"):
				_
				robot.bodyRight(-1)
			elif(key[0] == "e"):
				robot.bodyRight(1)
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
		
# Keyboard input functionality sources from: 
# https://www.editcode.net/forum.php?mod=viewthread&tid=249333&extra=&mobile=1
def read_single_keypress():
	return None
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
