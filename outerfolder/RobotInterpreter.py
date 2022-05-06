from servoCTL import *
import time
import math
from threading import RLock


class RobotInterpreter:
	def __init__(self, robot, srAgent, vAgent):
		self.robot = robot 
		self.srAgent = srAgent
		self.vAgent = vAgent
		# self.lock = RLock()
		# self.speaklock = RLock()

	def handleCommand(self, json) -> str:


		command = json["command"]



		# if (command == "drive"):
		# 	command = "turn"
		# 	json["angle"] = "90"

		print(json)
		result = ""

		if (command == "move"):
			# Handle move body command
			part = json["part"] 
			position = float(json["position"])
			duration = int(json["time"])

			if("reset" in json and json["reset"].lower() == "true"):
				self.robot.resetValue(text_map[part])
			else:
				print("Moving to position %f" % position )
				self.robot.setValue(text_map[part], position)
				
			time.sleep(duration/1000.0)


			
			

		elif (command == "drive"):
			# if self.lock.acquire(blocking=False) == False:
			# 	return False, result
			# Handle drive command
			# del json["time"]
			# json["distance"] = 4

			# if "time" in json:
			# 	# speed = int(json["speed"])
			# 	speed = 1
			# 	turning = int(json["turning"])
			# 	# speed = 1 # TODO: remove this
			# 	# turning = -0.5  # TODO: remove this
			# 	duration = int(json["time"])


			# 	if not ("reset" in json and json["reset"].lower() == "true"):
			# 		self.robot.setSpeed(speed)
			# 		self.robot.setRightTurnSpeed(turning)
			# 		time.sleep(duration/1000.0)

			if "distance" in json:
				# speed = int(json["speed"])
				speed = 1
				distance = int(json["distance"])

				if not ("reset" in json and json["reset"].lower() == "true"):
					speed = math.copysign(speed, distance)
					self.robot.setSpeed(speed)
					self.robot.setRightTurnSpeed(0)
					duration,finish = getTimeToTravelFeet(1,abs(distance))
					print("Time to travel %d ft. at speed %d is %dms" % (distance,speed,duration))
					time.sleep(duration/1000)
					self.robot.safeStopMoving()
					time.sleep(finish/1000)
			# self.lock.release()

		elif (command == "turn"):
			
			# if self.lock.acquire(blocking=False) == False:
			# 	return False, result

			# +90 turn right
			# -90 turn left
			# +180 turn right
			# -180 turn left
			angle =  int(json["position"])

			self.robot.setRightTurnSpeed(math.copysign(0.7, angle))
			duration = getTimeToTurnAngle(angle)
			time.sleep(duration/1000)
			self.robot.safeStopMoving()


			# self.lock.release()
		
			
	

		elif (command == "speak"):

			
			# if self.speaklock.acquire(blocking=False) == False:
			# 	return False, result
			
			text = json["text"]
			self.vAgent.speak(text)


			# self.speaklock.release()

		elif (command == "delay" and int(json["time"]) == 0):
			
			# if self.speaklock.acquire(blocking=False) == False:
			# 	return False, result

			# Handle user voice input command
			# while True:
			result = self.srAgent.listen()
			print("I heard: %s" % result)
			if result is not None:
				if "go" in result or "start" in result or "oh" in result:
					return True, result
				if "hello" in result:
					self.vAgent.speak("Hello")
				else:
					self.srAgent.handle(result)
			return False, result
			# self.speaklock.release()
			

		elif (command == "stop"):
			self.robot.safeStopMoving()

		elif (command == "reset"):
			self.robot.reset()

		return True, result
