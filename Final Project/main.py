from concurrent.futures import process, thread
from os import fdopen

from MapCells import MapCells
from Player import Player
from Map import Map
from Direction import Direction
from tkinter import *
from TTS import sayText
from Speech import getSpeechInput
import threading
#from servoCTL import *

shouldDestroy = False


def playGame(window: Tk, canvas: Canvas):
    #ctl = ServoCTL()
    #ctl.reset()
    #robot = TangoBot(ctl, 1/30)

    p = Player(None, 100, 1, 10, 50)
    m = Map(p, 5, canvas, 3, 1, 2, 6, 5, 3, 3)
    remainingMoves = 50

    while (p.isAlive() and not p.hasWon() and remainingMoves >= 1):
        remainingMoves -= 1

        curCell = m.getCell(p.getX(), p.getY())

        m.printMap()
        p.drawExplored()

        # Get available directions
        available = []
        for dir in list(Direction):
            if (curCell.getNeighbor(dir) is not None):
                available.append(dir)

        query = "I can go"
        for dir in available:
            if (dir == Direction.NORTH):
                query += " north"
            elif (dir == Direction.EAST):
                query += " east"
            elif (dir == Direction.SOUTH):
                query += " south"
            elif (dir == Direction.WEST):
                query += " west"

        query += ". What direction should I go? "
        sayText(query)
        toGo = getSpeechInput()

        dirToGo = None
        if ("north" in toGo):
            dirToGo = Direction.NORTH
        elif ("south" in toGo):
            dirToGo = Direction.SOUTH
        elif ("east" in toGo):
            dirToGo = Direction.EAST
        elif ("west" in toGo):
            dirToGo = Direction.WEST
        elif ("exit" in toGo):
            sayText("Goodbye!")
            window.quit()
            return

        if (dirToGo is not None):
            if (p.move(dirToGo)):
                continue

        sayText("Invalid direction!")

    if (remainingMoves <= 0):
        print("You ran out of moves!")

    #ctl.reset()
    #robot.stop()


# test = MapCells.PuzzleCell(None, 0, 0)
# test.handleInteraction()

if __name__ == "__main__":
    window = Tk()
    # window.attributes("-fullscreen", True)
    window.geometry("1280x720")

    canvas = Canvas(window, width=1280, height=720)
    canvas.pack()

    drawThread = threading.Thread(target=playGame, args=(window, canvas))
    window.after(100, lambda : drawThread.start())

    window.mainloop()

    drawThread.join()


# TODO:
# Proper output engine for robot
# Robot animations
# Screen animations
# User input loop
# Finish fun and puzzle cells
