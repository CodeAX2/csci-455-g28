from MapCell import *
from TTS import sayText
from playsound import playsound

class RickRollCell(MapCell):
    def __init__(self, map: Map, x: int, y: int):
        super().__init__(map, x, y)

    def handleInteraction(self):
        if (not self._completed):
            sayText("Get Rick Rolled!")
            playsound("Final Project/audio/RickRoll.wav")            
            self._completed = True

