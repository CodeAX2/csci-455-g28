import random

class Enemy:

    def __init__(self, health, atkMin, atkMax):
        self._health = health
        self._atkMin = atkMin
        self._atkMax = atkMax

    def applyDamage(self, damage):
        self._health -= damage
        if (self._health < 0):
            self._health = 0

    def isAlive(self):
        return self._health > 0

    def getHealth(self):
        return self._health

    def generateAttack(self):
        return random.randint(self._atkMin, self._atkMax)