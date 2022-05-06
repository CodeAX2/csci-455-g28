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

from KeyboardInput import read_single_keypress
from servoCTL import *

useKeyboard = False


def getDirFromKeyboard():
	while True:
		key = read_single_keypress()
		if(len(key) == 3): # Special Key codes for arrow keys
			print(key)
			if(key[2] == "A"): # Up arrow key
				return "north"
			elif(key[2] == "B"): # Down arrow key
				return "south"
			elif(key[2] == "C"): # Right arrow key
				return "east"
			elif(key[2] == "D"): # Left arrow key
				return "west"
			else:
				print("Unknown Key: ", key[2])
		else:
			if(key[0] == "w"):
				return "north"
				# robot.increaseSpeed()
			elif(key[0] == "s"):
				return "south"
				# robot.increaseSpeed(-1)
			elif(key[0] == "a"):
				return "west"
				# robot.rightTurnSpeed(-1)
			elif(key[0] == "d"):
				return "east"
				# robot.rightTurnSpeed(1)
			elif(key[0] == "\x1b"):
				# Stop all movement and exit
				# servoCtl.reset()
				break
			else:
				# Unknown key
				print("Unknown key: ", key[0])

def playGame(window: Tk, canvas: Canvas):
	
	servoCtl = ServoCTL()
	robot = TangoBot(servoCtl,1/30)


	p = Player(robot, 100, 100, 100, 50)
	m = Map(robot, p, 5, canvas, 3, 1, 2, 6, 5, 3, 3)
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
		if useKeyboard:
			toGo = getDirFromKeyboard()
		else:
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
# Robot animations
# Finish puzzle cells
