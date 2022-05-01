import time

from BColors import BColors
from MapCell import *


class PuzzleCell(MapCell):
    def __init__(self, map: Map, x: int, y: int):
        super().__init__(map, x, y)
        self.combo = [random.randint(0, 9), random.randint(0, 9), random.randint(0, 9)]
        self.guess = [0, 0, 0]

    def getLockTightness(self, num1, num2):
        return min(abs(num1 - num2), 10 - abs(num1 - num2))

    def handleInteraction(self):
        if(self._completed):
            return
        SLEEP = 0.5
        print("Congratulations? You found the key to the treasure.")
        time.sleep(SLEEP)
        print("Well, almost...")
        time.sleep(SLEEP)
        print("The key is in a treasure chest, and it is locked.")
        time.sleep(SLEEP)
        while (True):
            tightness = 0
            for i in range(len(self.combo)):
                tightness = max(tightness, 20 * self.getLockTightness(self.combo[i], self.guess[i]))

            lockTextColor = BColors.RED if tightness > 0 else BColors.GREEN
            print(("The combination lock reads " + lockTextColor + "[%d] [%d] [%d]" + BColors.ENDC)
                  % (self.guess[0], self.guess[1], self.guess[2]))
            # print(("The combination lock CHEAT " + lockTextColor + "[%d] [%d] [%d]" + BColors.ENDC)
            #      % (self.combo[0], self.combo[1], self.combo[2]))
            print(("The lock is " + lockTextColor + "%d%% TIGHT" + BColors.ENDC) % tightness)
            if (tightness > 0):
                dial = None
                num = None
                quit = False
                help = False
                try:
                    dial = input("Dial to move? [1, 2, 3, q=quit, h=help]? ")
                    if (dial == 'q' or dial == "quit"):
                        quit = True
                    if (dial == 'h' or dial == "help"):
                        help = True
                    dial = int(dial)
                    num = int(input("Move it to? [0 - 9]? "))
                except:
                    pass
                if (dial is not None and num is not None and 1 <= dial <= 3 and 0 <= num <= 9):
                    self.guess[dial - 1] = num
                if (quit):
                    break
                if (help):
                    print("To get to the key to the treasure, you have to pick a 3-dial combination lock.")
                    print("Each dial can take on the value from 1 to 9.")
                    print("The tightness of each dial is equal to the distance between it and the correct value.")
                    print("The tightness of the lock is equal to its tightest dial.")
                    print("When the tightness of the lock is zero, the lock is open.")
            else:  # Lock is open
                print(BColors.RED + "K" + BColors.YELLOW + "A" + BColors.GREEN + "C" + BColors.CYAN + "H" +
                      BColors.BLUE + "I" + BColors.RED + "N" + BColors.YELLOW + "G" + BColors.GREEN + "!" + BColors.ENDC)
                print("The chest pops open, revealing an intricate key, which you keep in a safe place.\n")
                self._map.getPlayer().__hasKey = True
                self._completed = True
                break
