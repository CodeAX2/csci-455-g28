import random
from Direction import Direction
from tkinter import *

class Player:
    def __init__(self, robot, health, atkMin, atkMax, moves):
        from MapCell import MapCell
        self.__robot = robot
        self.__health = health
        self.__maxHealth = health
        self.__atkMin = atkMin
        self.__atkMax = atkMax
        self.__remainingMoves = moves

        self.__posX = -1
        self.__posY = -1

        self.__lastDirection = Direction.NORTH

        self.__hasKey = False
        self.__won = False

        self.__explored: list[MapCell] = []

    def applyDamage(self, damage):
        self.__health -= damage
        if (self.__health < 0):
            self.__health = 0

    def isAlive(self):
        return self.__health > 0

    def hasFoundKey(self):
        return self.__hasKey

    def win(self):
        self.__won = True

    def hasWon(self):
        return self.__won

    def getHealth(self):
        return self.__health

    def generateAttack(self):
        return random.randint(self.__atkMin, self.__atkMax)

    def getLastDirection(self):
        return self.__lastDirection

    def getRemainingMoves(self):
        return self.__remainingMoves

    def spawnPlayer(self, x, y, map):
        from Map import Map
        if (self.__posX == -1 and self.__posY == -1):
            self.__posX = x
            self.__posY = y
            self.__map: Map = map
            self.__explored = []
            self.__explored.append(self.__map.getCell(x, y))

    def getRobot(self):
        return self.__robot

    def move(self, dir: Direction):
        from MapCell import MapCell
        cell: MapCell = self.__map.getCell(self.__posX, self.__posY)
        neighbor = cell.getNeighbor(dir)
        if (neighbor != None):
            self.__posX = neighbor.getX()
            self.__posY = neighbor.getY()
            self.__lastDirection = dir

            # TODO: Robot animation

            if (neighbor not in self.__explored):
                self.__explored.append(neighbor)
            neighbor.handleInteraction()

            return True
        return False

    def setHealth(self, health):
        self.__health = health
        if (self.__health > self.__maxHealth):
            self.__health = self.__maxHealth
        elif (self.__health < 0):
            self.__health = 0

    def getMaxHealth(self):
        return self.__maxHealth

    def runToCell(self, x: int, y: int):
        self.__posX = x
        self.__posY = y

        cell = self.__map.getCell(x, y)
        if (cell not in self.__explored):
            self.__explored.append(cell)

    def getX(self):
        return self.__posX

    def getY(self):
        return self.__posY

    def drawExplored(self):
        from MapCells import MapCells
        canvas = self.__map.getCanvas()
        canvas.delete("all")

        for exploredCell in self.__explored:
            
            cellX = exploredCell.getX()
            cellY = exploredCell.getY()

            color = "blue"

            if (type(exploredCell) is MapCells.TreasureCell):
                color = "gold"
            elif (type(exploredCell) is MapCells.FightCell):
                if (not exploredCell.isComplete()):
                    color = "red"

            canvas.create_rectangle(cellX * 50 + 10, cellY * 50 + 10, cellX * 50 + 40, cellY * 50 + 40, fill=color)

            if (exploredCell.getNeighbor(Direction.NORTH) != None):
                canvas.create_rectangle(cellX * 50 + 20, cellY * 50, cellX * 50 + 30, cellY * 50 + 10, fill=color)

            if (exploredCell.getNeighbor(Direction.EAST) != None):
                canvas.create_rectangle(cellX * 50 + 40, cellY * 50 + 20, cellX * 50 + 50, cellY * 50 + 30, fill=color)

            if (exploredCell.getNeighbor(Direction.SOUTH) != None):
                canvas.create_rectangle(cellX * 50 + 20, cellY * 50 + 40, cellX * 50 + 30, cellY * 50 + 50, fill=color)

            if (exploredCell.getNeighbor(Direction.WEST) != None):
                canvas.create_rectangle(cellX * 50, cellY * 50 + 20, cellX * 50 + 10, cellY * 50 + 30, fill=color)

        canvas.create_oval(self.__posX * 50 + 15, self.__posY * 50 + 15, self.__posX * 50 + 35, self.__posY * 50 + 35, fill="lime")

        canvas.create_text(
            10, 
            self.__map.getSize() * 50 + 10,
            text=("Player HP: " + str(self.__health)), 
            font=("Helvetica","20","bold"),
            anchor=NW
        )
