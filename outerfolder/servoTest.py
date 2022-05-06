from servoCTL import ServoCTL
from servoCTL import *
import time


def main():
	servoCtl = ServoCTL()

	servoIdx = 0
	while True:
		key = read_single_keypress()
		if(len(key) == 3): # Special Keys
			if(key[2] == "A"):
				print("UP")
				servoCtl.increment(servoIdx, 200)
				print(servoCtl.get(servoIdx))
			elif(key[2] == "B"):
				print("DOWN")
				servoCtl.increment(servoIdx, -200)
				print(servoCtl.get(servoIdx))
			elif(key[2] == "C"):
				servoIdx += 1
				servoIdx %= NUM_SERVOS
				print("RIGHT ", servoIdx)
			elif(key[2] == "D"):
				servoIdx -= 1
				servoIdx %= NUM_SERVOS
				print("LEFT ", servoIdx)
		else:
			if(key[0] == " "):
				servoCtl.reset()
				print("SPACE")
			elif(key[0] == "\x1b"):
				# Stop all movement and exit
				servoCtl.reset()
				break
			else:
				print(key)
		



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
