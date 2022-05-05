import speech_recognition as sr

r = sr.Recognizer()

def getSpeechInput():

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source)
            word = r.recognize_google(audio)
            return str.lower(word).split(" ")
        except sr.UnknownValueError:
            return []
