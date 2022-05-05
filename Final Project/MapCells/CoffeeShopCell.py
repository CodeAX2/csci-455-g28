from MapCell import *
from TTS import sayText

class CoffeeShopCell(MapCell):
    def __init__(self, map: Map, x: int, y: int):
        super().__init__(map, x, y)

    def handleInteraction(self):
        if (not self._completed):
            treasurePos = self._map.getTreasureCellPosition()
            dx = treasurePos[0] - self._x
            dy = treasurePos[1] - self._y

            if (abs(dx) > abs(dy)):
                # Treasure is more east/west
                if (dx > 0):
                    sayText("Treasure is East")
                else:
                    sayText("Treasure is West")
            else:
                # Treasure is more north/south
                if (dy > 0):
                    sayText("Treasure is South")
                else:
                    sayText("Treasure is North")

            self._completed = True
