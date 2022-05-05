import pyttsx3

engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def sayText(text):
    engine.say(text)
    engine.runAndWait()