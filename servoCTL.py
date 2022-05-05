from numpy import deprecate, intp
import maestro
import time
import threading

SERVO_TORSO = 0
SERVO_THROTTLE= 1
SERVO_STEERING = 2
SERVO_HEAD_YAW = 3
SERVO_HEAD_PITCH = 4
SERVO_R_ARM_PITCH = 5
SERVO_R_ARM_YAW = 6
SERVO_R_ELBOW_PITCH = 7
SERVO_R_WRIST_PITCH = 8
SERVO_R_WRIST_ROLL = 9
SERVO_R_GRAB = 10
SERVO_11 = 11
SERVO_L_ARM_PTICH = 12
SERVO_L_ARM_YAW = 13
SERVO_L_ELBOW_PITCH = 14
SERVO_L_WRIST_PITCH = 15
SERVO_L_WRIST_ROLL = 16
SERVO_L_GRAB = 17

POSITIONAL = 0
MOTOR = 1

		
# Constants for how the robot's servos are wired
NUM_SERVOS = 18
SERVO_ZERO = 6000


text_map = {
	"torso": SERVO_TORSO,
	"head pitch" : SERVO_HEAD_PITCH,
	"head yaw": SERVO_HEAD_YAW,
}

feet_map = {
		# At speed 0.5, need to get 2000ms to finish accelerating from 0, at 5 ft
	"speedup": [
		(0.5,900,0.5), 
		(0.7,1200,0.8),
		(1.0,1550,1.4)
	],
		# At speed 0.5, in 1000ms you travel 1ft.
	"fullspeed": [
		(0.5,4000,12),
		(0.7,3500,12),
		(1.0,2900,12)
	],

		# At speed 0.5 intially, 400ms to stop,
	"slowdown":[
		(0.5,500,0.4),
		(1.0,1600,1.2),
	]
}

def add(a,b):
	return tuple(sum(x) for x in zip(a,b))

def sub(a,b):
	return tuple(x[0]-x[1] for x in zip(a,b))

def mult(p,a):
	return tuple(p*x for x in a)

def intpTable(key,table):
	initial = (0,0,0)
	preinit = initial
	# Interpolate
	for e in table:
		if key <= e[0]:
			p = (key-initial[0])/(e[0]-initial[0])
			print(p, e, initial, preinit,sub(e,initial),mult(p,sub(e,initial)))
			return add(initial,mult(p,sub(e,initial)))
		preinit = initial
		initial = e
	# Use last two to extrapolate
	e = initial
	initial = preinit
	p = (e[0]-key)/(e[0]-initial[0])
	return add(initial,mult(p,sub(e,initial)))
	


def getTimeToTravelFeet(speedF,feet):
	slow = intpTable(speedF,feet_map["slowdown"])
	speed = intpTable(speedF,feet_map["speedup"])
	full = intpTable(speedF,feet_map["fullspeed"])
	print("Interpolated Tables:")
	print(slow,speed,full)


	time = 0

	feet -= slow[2]
	# time += slow[1]
	print("Slowing down: %fft in %dms" % (slow[2],slow[1]))

	feet -= speed[2]
	time += speed[1]
	print("Speeding up: %fft in %dms" % (speed[2],speed[1]))

	t = feet/(full[2]/full[1])
	time += t
	print("Traveling: %fft in %dms" % (feet,t))

	return time,slow[1]

# At 0.7 speed currently.
def getTimeToTurnAngle(angle):
	time = 0
	if abs(angle) == 45:
		time = 600
	if abs(angle) == 90:
		time = 1100
	if abs(angle) == 180:
		time = 1800
	if abs(angle) == 360:
		time = 2800

	return time


servoRanges = {
	SERVO_TORSO:{
		"type":POSITIONAL,
		"min":4500,
		"max":7500,
		"center":6000
	},
	SERVO_THROTTLE:{
		"type":MOTOR,
		"max":SERVO_ZERO+1600,
		"min":SERVO_ZERO-1600,
		"center":SERVO_ZERO,
		"inv":True,
		"acc":25
	},
	SERVO_STEERING:{
		"type":MOTOR,
		"max":SERVO_ZERO+1600,
		"min":SERVO_ZERO-1600,
		"center":SERVO_ZERO,
		"acc":47
	},
	SERVO_HEAD_YAW:{
		"type":POSITIONAL,
		"min":4500,
		"max":7500,
		"center":6000,
		"inv":True
	},
	SERVO_HEAD_PITCH:{
		"type":POSITIONAL,
		"min":4500,
		"max":7500,
		"center":6000
	},
	SERVO_L_ARM_PTICH:{
		"type":POSITIONAL,
		"min":4500,
		"max":7500,
		"center":6000
	},
	SERVO_R_ARM_PITCH:{
		"type":POSITIONAL,
		"min":4500,
		"max":7500,
		"center":6000
	},
	SERVO_R_ELBOW_PITCH:{
		"type":POSITIONAL,
		"min":6000-1800,
		"max":7500+1600,
		"center":6000,
		"inv":True
	}
}


class TangoBot:

	def __init__(self,ctl, tickPeriod):
		self.reset()

		self.ctl = ctl
		self.thread = threading.Thread(target=self.run,args=(tickPeriod,))
		self.thread.start()
		
	
	def headUp(self, mult=1):
		# Rotate head up
		self.headPitch += mult * 0.2
		if (self.headPitch > 1):
			self.headPitch = 1
		if (self.headPitch < -1):
			self.headPitch = -1
		self.setValue(SERVO_HEAD_PITCH, self.headPitch)


	def setHeadPitch(self, pos):
		self.headPitch = pos
		self.setValue(SERVO_HEAD_PITCH, self.headPitch)

	def headRight(self, mult=1):
		self.headYaw += mult*0.2
		if (self.headYaw > 1):
			self.headYaw = 1
		if (self.headYaw < -1):
			self.headYaw = -1
		self.setValue(SERVO_HEAD_YAW, self.headYaw)

	def setHeadYaw(self, pos):
		self.headYaw = pos
		self.setValue(SERVO_HEAD_YAW, self.headYaw)

	def safeStopMoving(self):
		self.setValue(SERVO_THROTTLE, 0)
		self.setValue(SERVO_STEERING, 0)
		self.forwardSpeed = 0
		self.turnSpeed = 0

	def reset(self):
		self.forwardSpeed = 0
		self.turnSpeed = 0
		self.headYaw = 0
		self.headPitch = 0
		self.bodyYaw = 0

		self.target = [SERVO_ZERO for _ in range(NUM_SERVOS)]


	def setSpeed(self, value):
		self.forwardSpeed = value
		self.setValue(SERVO_THROTTLE, self.forwardSpeed)

	def setRightTurnSpeed(self,value):
		self.turnSpeed = -1*value
		self.setValue(SERVO_STEERING, self.turnSpeed)

	def bodyRight(self, mult=1):
		mult *= -1
		self.bodyYaw += 0.3 * mult
		if (self.bodyYaw > 0.9):
			self.bodyYaw = 0.9
		if (self.bodyYaw < -0.9):
			self.bodyYaw = -0.9
		self.setValue(SERVO_TORSO, self.bodyYaw)

	def setBodyPos(self, pos):
		pos *= -1
		self.bodyYaw = pos
		self.setValue(SERVO_TORSO, self.bodyYaw)
	
	def stop(self):
		self.running = False
		self.thread.join()

	def run(self,tickPeriod):
		self.condition_obj = threading.Condition()
		self.running = True
		while self.running:
			self.tick()
			time.sleep(tickPeriod)
			# self.condition_obj.acquire()
			# self.condition_obj.wait(tickPeriod)
			# self.condition_obj.release()
 
	def notify(self):
		self.condition_obj.notify()


	def setValue(self,channel,float):
		ranges = servoRanges[channel]
		if "inv" in ranges and ranges["inv"] == True:
			float*=-1
		domain = ranges["max"]-ranges["center"]
		val = ranges["center"]+ float*domain
		val = int(max(min(val,ranges["max"]),ranges["min"]))
		self.target[channel] = val
		print("Target value for channel %d is %d with range %f" % (channel,val,float))

	def resetValue(self,channel):
		ranges = servoRanges[channel]
		val = ranges["center"]
		self.target[channel] = val
		print("Target value for channel %d is %d with range 0" % (channel,val))


	def incValue(self,channel,float):
		ranges = servoRanges[channel]
		if "inv" in ranges and ranges["inv"] == True:
			float*=-1
		domain = ranges["max"]-ranges["center"]
		val = ranges["center"]+float*domain
		val = self.target[channel]+val
		self.target[channel] = max(min(val,ranges["max"]),ranges["min"])

	def tick(self):
		for channel in range(NUM_SERVOS):
			target = self.target[channel]
			current = self.ctl.servos[channel]
			if self.ctl.servos[channel] != self.target[channel]:
				ranges = servoRanges[channel]
				if "acc" in ranges:
					if target > current:
						inc = min(target-current,ranges["acc"])
						self.ctl.increment(channel,inc)
					else:
						dec = min(current-target,ranges["acc"])
						self.ctl.increment(channel,-dec)
				else:
					print(self.target[channel])
					self.ctl.set(channel,self.target[channel])
				


class ServoCTL:
	ctl = maestro.Controller()
	
	def __init__(self):
		self.servos = [SERVO_ZERO for x in range(NUM_SERVOS)]
		self.wheelMax = 6000
		self.wheelAcc = 0

	def __del__(self):
		self.reset()
		
	def set(self,channel,value):
		self.servos[channel] = value
		self.ctl.setTarget(channel, value)
	
	def increment(self, channel, amount):
		self.servos[channel] += amount
		self.ctl.setTarget(channel, self.servos[channel])
		
	def reset(self):
		for i in range(NUM_SERVOS):
			self.servos[i] = SERVO_ZERO
			self.ctl.setTarget(i, SERVO_ZERO)
		

	def stop_wheel_movement(self):
		deltaThrottle = int((self.servos[SERVO_THROTTLE] - self.SERVO_ZERO) / 10)
		deltaSteering = int((self.servos[SERVO_STEERING] - self.SERVO_ZERO) / 10)
		for _ in range(10):
			self.ctl.setTarget(SERVO_THROTTLE, self.servos[SERVO_THROTTLE] + deltaThrottle)
			self.servos[SERVO_THROTTLE] -= deltaThrottle
			self.ctl.setTarget(SERVO_STEERING, self.servos[SERVO_STEERING] + deltaSteering)
			self.servos[SERVO_STEERING] -= deltaSteering
			print(self.servos[SERVO_THROTTLE], self.servos[SERVO_STEERING])
			time.sleep(0.05)
			
		self.ctl.setTarget(SERVO_THROTTLE, self.SERVO_ZERO)
		self.ctl.setTarget(SERVO_STEERING, self.SERVO_ZERO)

