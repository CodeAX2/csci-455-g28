from MapCell import *
from TTS import sayText

class TreasureCell(MapCell):
    def __init__(self, map: Map, x: int, y: int):
        super().__init__(map, x, y)

    def handleInteraction(self):
        if (self._map.getPlayer().hasFoundKey()):
            sayText("You Win!")
            self._completed = True
            self._map.getPlayer().win()
        else:
            sayText("You need a key to open the treasure!")