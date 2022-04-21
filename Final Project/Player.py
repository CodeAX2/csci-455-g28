import random
from Direction import Direction

class Player:
    def __init__(self, robot, health, atkMin, atkMax, moves):
        self.__robot = robot
        self.__health = health
        self.__atkMin = atkMin
        self.__atkMax = atkMax
        self.__remainingMoves = moves

        self.__posX = -1
        self.__posY = -1

        self.__lastDirection = Direction.NORTH

        self.__hasKey = False

    def applyDamage(self, damage):
        self.__health -= damage
        if (self.__health < 0):
            self.__health = 0

    def isAlive(self):
        return self.__health > 0

    def hasFoundKey(self):
        return self.__hasKey

    def getHealth(self):
        return self.__health

    def generateAttack(self):
        return random.randint(self.__atkMin, self.__atkMax)

    def getLastDirection(self):
        return self.__lastDirection

    def getRemainingMoves(self):
        return self.__remainingMoves

    def spawnPlayer(self, x, y):
        if (self.__posX == -1 and self.__posY == -1):
            self.__posX = x
            self.__posY = y
    
    def getRobot(self):
        return self.__robot
