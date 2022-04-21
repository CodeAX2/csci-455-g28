import random
from Direction import Direction


class Player:
    def __init__(self, robot, health, atkMin, atkMax, moves):
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

    def getX(self):
        return self.__posX

    def getY(self):
        return self.__posY
