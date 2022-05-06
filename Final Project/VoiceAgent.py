
import pyttsx3


class VoiceAgent():
	def __init__(self):
		engine = pyttsx3.init()
		self.voices = engine.getProperty('voices')     
		engine.setProperty('voice', self.voices[10].id)
		engine.setProperty('rate', 150)
		self.engine = engine


	def speak(self,text):
		self.engine.say(text)
		self.engine.runAndWait()
	