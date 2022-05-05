import speech_recognition as sr


with sr.Microphone() as source:

    r = sr.Recognizer()
    r.adjust_for_ambient_noise(source)

    def getSpeechInput():

        try:
            audio = r.listen(source)
            word = r.recognize_google(audio)
            return str.lower(word).split(" ")
        except sr.UnknownValueError:
            return []
