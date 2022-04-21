from MapCell import *

class CoffeeShopCell(MapCell):
    def __init__(self, map: Map, x: int, y: int):
        super().__init__(map, x, y)

    def handleInteraction(self):
        if (not self._completed):
            treasurePos = self._map.getTreasureCellPosition()
            dx = treasurePos[0] - self._x
            dy = treasurePos[1] - self._y

            # TODO: Convert print to dialog
            if (abs(dx) > abs(dy)):
                # Treasure is more east/west
                if (dx > 0):
                    print("Treasure is East")
                else:
                    print("Treasure is West")
            else:
                # Treasure is more north/south
                if (dy > 0):
                    print("Treasure is South")
                else:
                    print("Treasure is North")

            self._completed = True
