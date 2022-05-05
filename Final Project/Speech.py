import speech_recognition as sr

def getSpeechInput():
    with sr.Microphone() as source:
        r= sr.Recognizer()
        r.adjust_for_ambient_noise(source)
        
        try:
            audio = r.listen(source)            
            word = r.recognize_google(audio)
            return word
        except sr.UnknownValueError:
            return None