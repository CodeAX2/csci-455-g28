import random
import time
from Direction import Direction
from tkinter import *
from RobotMovement import RobotMovement


class Player:
    def __init__(self, robot, health, atkMin, atkMax, moves):
        from MapCell import MapCell
        self._robot = robot
        self.robomover = RobotMovement(robot)
        self._health = health
        self._maxHealth = health
        self._atkMin = atkMin
        self._atkMax = atkMax
        self._remainingMoves = moves

        self._posX = -1
        self._posY = -1

        self._lastDirection = Direction.NORTH

        self._hasKey = False
        self._won = False

        self._explored: list[MapCell] = []

    def applyDamage(self, damage):
        self._health -= damage
        if (self._health < 0):
            self._health = 0

    def isAlive(self):
        return self._health > 0

    def hasFoundKey(self):
        return self._hasKey

    def win(self):
        self._won = True

    def hasWon(self):
        return self._won

    def getHealth(self):
        return self._health

    def generateAttack(self):
        return random.randint(self._atkMin, self._atkMax)

    def getLastDirection(self):
        return self._lastDirection

    def getRemainingMoves(self):
        return self._remainingMoves

    def spawnPlayer(self, x, y, map):
        from Map import Map
        if (self._posX == -1 and self._posY == -1):
            self._posX = x
            self._posY = y
            self._map: Map = map
            self._explored = []
            self._explored.append(self._map.getCell(x, y))

    def getRobot(self):
        return self._robot

    def move(self, dir: Direction):
        from MapCell import MapCell
        cell: MapCell = self._map.getCell(self._posX, self._posY)
        neighbor = cell.getNeighbor(dir)
        if (neighbor != None):

            toRotate = 0
            
            if (dir == Direction.EAST):
                toRotate = 90
            elif (dir == Direction.SOUTH):
                toRotate = 180
            elif (dir == Direction.WEST):
                toRotate = 270

            if (self._lastDirection == Direction.EAST):
                toRotate -= 90
            elif (self._lastDirection == Direction.SOUTH):
                toRotate -= 180
            elif (self._lastDirection == Direction.WEST):
                toRotate -= 270

            if (abs(360 + toRotate) < abs(toRotate)):
                toRotate = 360 + toRotate
            elif (abs(-360 + toRotate) < abs(toRotate)):
                toRotate = -360 + toRotate


            # Rotate robot
            self.robomover.turn(toRotate)
            time.sleep(0.5)
            # Move robot forward
            self.robomover.move(1.5)

            self._posX = neighbor.getX()
            self._posY = neighbor.getY()
            self._lastDirection = dir

            if (neighbor not in self._explored):
                self._explored.append(neighbor)
            neighbor.handleInteraction()

            return True
        return False

    def setHealth(self, health):
        self._health = health
        if (self._health > self._maxHealth):
            self._health = self._maxHealth
        elif (self._health < 0):
            self._health = 0

    def getMaxHealth(self):
        return self._maxHealth

    def runToCell(self, x: int, y: int):
        self._posX = x
        self._posY = y

        cell = self._map.getCell(x, y)
        if (cell not in self._explored):
            self._explored.append(cell)

    def getX(self):
        return self._posX

    def getY(self):
        return self._posY

    def drawExplored(self):
        from MapCells import MapCells
        canvas = self._map.getCanvas()
        canvas.delete("all")

        for exploredCell in self._explored:

            cellX = exploredCell.getX()
            cellY = exploredCell.getY()

            color = "blue"

            if (type(exploredCell) is MapCells.TreasureCell):
                color = "gold"
            elif (type(exploredCell) is MapCells.FightCell):
                if (not exploredCell.isComplete()):
                    color = "red"

            canvas.create_rectangle(
                cellX * 50 + 10, cellY * 50 + 10, cellX * 50 + 40, cellY * 50 + 40, fill=color)

            if (exploredCell.getNeighbor(Direction.NORTH) != None):
                canvas.create_rectangle(
                    cellX * 50 + 20, cellY * 50, cellX * 50 + 30, cellY * 50 + 10, fill=color)

            if (exploredCell.getNeighbor(Direction.EAST) != None):
                canvas.create_rectangle(
                    cellX * 50 + 40, cellY * 50 + 20, cellX * 50 + 50, cellY * 50 + 30, fill=color)

            if (exploredCell.getNeighbor(Direction.SOUTH) != None):
                canvas.create_rectangle(
                    cellX * 50 + 20, cellY * 50 + 40, cellX * 50 + 30, cellY * 50 + 50, fill=color)

            if (exploredCell.getNeighbor(Direction.WEST) != None):
                canvas.create_rectangle(
                    cellX * 50, cellY * 50 + 20, cellX * 50 + 10, cellY * 50 + 30, fill=color)

        canvas.create_oval(self._posX * 50 + 15, self._posY * 50 +
                           15, self._posX * 50 + 35, self._posY * 50 + 35, fill="lime")

        canvas.create_text(
            10,
            self._map.getSize() * 50 + 10,
            text=("Player HP: " + str(self._health)),
            font=("Helvetica", "20", "bold"),
            anchor=NW
        )
