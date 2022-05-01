import time

from MapCell import *

class PuzzleCell(MapCell):
    def __init__(self, map: Map, x: int, y: int):
        super().__init__(map, x, y)

    def handleInteraction(self):
        SLEEP = 0.5
        print("Congratulations? You found the key to the treasure.")
        time.sleep(SLEEP)
        print("Well, almost...")
        time.sleep(SLEEP)
        print("The key is in a treasure chest, and it is locked.")
        time.sleep(SLEEP)
        print("The combination lock reads [0] [0] [0]")
        print("The lock is 100% TIGHT")
        # TODO:
        # The lock's tightness depends on how far the farthest dial is from the correct, randomly chosen number
        # When the tightness is zero, the lock is open and the Player gets the Key to the Treasure

        self._completed = True
