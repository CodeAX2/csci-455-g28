import pyttsx3

engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 50)


def sayText(text):
    engine.say(text)
    engine.runAndWait()