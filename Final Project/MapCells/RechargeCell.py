from MapCell import *

class RechargeCell(MapCell):
    def __init__(self, map: Map, x: int, y: int):
        super().__init__(map, x, y)

    def handleInteraction(self):
        if (not self._completed):
            # TODO: Convert print to dialog
            self._map.getPlayer().setHealth(self._map.getPlayer().getMaxHealth())
            print("You have been healed. You are now at " + str(self._map.getPlayer().getHealth()) + "HP")            
            self._completed = True

