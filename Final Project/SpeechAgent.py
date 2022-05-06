import threading
import time

import speech_recognition as sr

from servoCTL import *


import os, sys, contextlib

@contextlib.contextmanager
def ignoreStderr():
	devnull = os.open(os.devnull, os.O_WRONLY)
	old_stderr = os.dup(2)
	sys.stderr.flush()
	os.dup2(devnull, 2)
	os.close(devnull)
	try:
		yield
	finally:
		os.dup2(old_stderr, 2)
		os.close(old_stderr)


def _anyin(phrases,string):
	for val in phrases:
		# if val in string:
		if val in string:
			return True, val
	return False, None


def anyin(phrases,string):
	find,_ = _anyin(phrases,string)
	return find


confusables = {
	"left":["lap","lak"],
	"look":["luck"],
	"backward":["back work"],
	"small":["smile"]
}

def confusableMatch(a,b):
	build = ""
	for word in a.split(" "):
		# print(word)
		test = build + " " + word
		if test in b:
			build = test
			continue

		if word in confusables:
			find,confus = _anyin(confusables[word],b)
			if find:
				test = (build + " " + confus)
				if test in b:
					build = test
					continue
		return False
	return True


class SpeechAgent:
	def __init__(self,robot,ctl):
		self.robot = robot
		self.ctl = ctl

	def start(self):
		self.thread = threading.Thread(target=self.run,args=())
		self.thread.start()
	
	def listen(self):
		with ignoreStderr():
			with sr.Microphone() as source:
				recognizer = sr.Recognizer()
				recognizer.adjust_for_ambient_noise(source)
				recognizer.dynamic_energythreshold = 3000
				print("listening...")
				try:
					audio = recognizer.listen(source)
					voiceCommand = recognizer.recognize_google(audio)
					voiceCommand = voiceCommand.lower()
					return voiceCommand


				except sr.UnknownValueError:
					print("Unknown Command")


	def handle(self,voiceCommand):
		if "stop" in voiceCommand: # Maybe not needed, stops automatically
			self.robot.safeStopMoving()
		elif anyin(["do the harlem shake","frolic","dance"],voiceCommand):
			def audio():
				import os
				# os.system("speaker-test -c2 -t sine")
				os.system("aplay harlem.wav")
			def shakeHead():
				for _ in range(15):
					self.robot.setValue(SERVO_HEAD_PITCH, -1)
					time.sleep(1)
					self.robot.setValue(SERVO_HEAD_PITCH, 1)
					time.sleep(1)
				self.robot.setValue(SERVO_HEAD_PITCH, 0)

			def shakeLimbs():
				for _ in range(10):
					self.robot.setValue(SERVO_L_ARM_PTICH, 1)
					self.robot.setValue(SERVO_R_ELBOW_PITCH, -1)
					time.sleep(1)
					self.robot.setValue(SERVO_L_ARM_PTICH, -1)
					self.robot.setValue(SERVO_R_ELBOW_PITCH, 1)
					time.sleep(1)
				self.robot.setValue(SERVO_L_ARM_PTICH, 0)
				self.robot.setValue(SERVO_R_ELBOW_PITCH, 0)

			aud = threading.Thread(target=audio,args=())
			aud.start()

			head = threading.Thread(target=shakeHead,args=())
			head.start()

			time.sleep(15.5)

			hands = threading.Thread(target=shakeLimbs,args=())
			hands.start()


			for _ in range(2):
				self.robot.setBodyPos(-0.7)
				self.robot.setRightTurnSpeed(1)
				self.robot.setHeadYaw(0.7)
				self.ctl
				time.sleep(4.5)
				self.robot.setBodyPos(0.7)
				self.robot.setRightTurnSpeed(-1)
				self.robot.setHeadYaw(-0.7)
				time.sleep(4.5)
			self.robot.safeStopMoving()
			self.robot.setBodyPos(0)
			self.robot.setHeadYaw(0)
			hands.join()
			head.join()
			aud.join()
		elif anyin(["go far","long forward"],voiceCommand):
			self.robot.setSpeed(2)
			time.sleep(4)
			self.robot.safeStopMoving()
		elif anyin(["tiny forward"],voiceCommand):
			self.robot.setSpeed(1)
			time.sleep(1)
			self.robot.safeStopMoving()
		elif "small forward" in voiceCommand:
			self.robot.setSpeed(1)
			time.sleep(1.7)
			self.robot.safeStopMoving()
		elif "go forward" in voiceCommand:
			self.robot.setSpeed(1)
			time.sleep(2)
			self.robot.safeStopMoving()
		elif "tiny backward" in voiceCommand:
			self.robot.setSpeed(-1)
			time.sleep(1.7)
			self.robot.safeStopMoving()
		elif "small backward" in voiceCommand:
			self.robot.setSpeed(-1)
			time.sleep(1)
			self.robot.safeStopMoving()
		elif "go backward" in voiceCommand:
			self.robot.setSpeed(-1)
			time.sleep(2)
			self.robot.safeStopMoving()
		elif anyin(["turn around","about face"],voiceCommand):
			self.robot.setRightTurnSpeed(0.75)
			time.sleep(1.6)
			self.robot.safeStopMoving()
		elif "turn right" in voiceCommand:
			self.robot.setRightTurnSpeed(0.75)
			time.sleep(1.2)
			self.robot.safeStopMoving()
		elif anyin(["small right","smile right"], voiceCommand):
			self.robot.setRightTurnSpeed(0.75)
			time.sleep(0.83)
			self.robot.safeStopMoving()
		elif "turn left" in voiceCommand:
			self.robot.setRightTurnSpeed(-0.75)
			time.sleep(1.2)
			self.robot.safeStopMoving()
		elif anyin(["small left","smile left", "small lap"], voiceCommand):
			self.robot.setRightTurnSpeed(-0.75)
			time.sleep(0.83)
			self.robot.safeStopMoving()
		elif "body right" in voiceCommand:
			self.robot.setBodyPos(1)
		elif "body left" in voiceCommand:
			self.robot.setBodyPos(-1)
		elif "body center" in voiceCommand:
			self.robot.setBodyPos(0)
		elif anyin(["look left", "look lak", "look lap", "luck left", "luck lak", "luck lap"],voiceCommand):
			self.robot.setHeadYaw(-1)
		elif anyin(["look right","luok right"],voiceCommand):
			self.robot.setHeadYaw(1)
		elif anyin(["look up","luck up"],voiceCommand):
			self.robot.setHeadPitch(1)
		elif anyin(["look down","luck down"],voiceCommand):
			self.robot.setHeadPitch(-1)
		elif anyin(["look center","look straight"],voiceCommand):
			self.robot.setHeadYaw(0)
			self.robot.setHeadPitch(0)

	def run(self):
		while self.robot.running:
			self.handle(self.listen())
