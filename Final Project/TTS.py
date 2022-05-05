import pyttsx3

engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[14].id)
engine.setProperty('rate', 150)


def sayText(text):
    engine.say(text)
    engine.runAndWait()