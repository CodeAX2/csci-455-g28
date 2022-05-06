import pyttsx3
from gtts import gTTS
from playsound import playsound

tts = gTTS(text="This is the pc speaking", lang='en')

engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[5].id)
engine.setProperty('rate', 150)


def sayText(text):
    print("Say: %s" % text)
    tts = gTTS(text,slow=False)
    tts.save('speak.mp3')
    playsound('speak.mp3')
    # engine.say(text)
    # engine.runAndWait()