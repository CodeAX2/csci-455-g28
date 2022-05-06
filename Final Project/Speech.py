import speech_recognition as sr
r = sr.Recognizer()


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


def getSpeechInput():
    print("Listening...")
    with ignoreStderr():
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            returned = []
            try:
                audio = r.listen(source)
                word = r.recognize_google(audio)
                returned = str.lower(word) #.split(" ")
            except sr.UnknownValueError:
                returned = ""

            print("Heard:", returned)
            return returned
