from MapCell import *
from Enemy import Enemy

class FightCell(MapCell):
    def __init__(self, map: Map, x: int, y: int, enemyHealthMin: int, enemyHealthMax: int, enemyAtkMin: int, enemyAtkMax: int):
        self._enemies: list[Enemy] = []

        numEnemies = random.randint(3, 6)
        for _ in range(numEnemies):
            enemy: Enemy = Enemy(random.randint(
                enemyHealthMin, enemyHealthMax), enemyAtkMin, enemyAtkMax)
            self._enemies.append(enemy)

        super().__init__(map, x, y)

    def handleInteraction(self):

        # TODO: Replace print statements with proper dialog, and add animations
        if (not self._completed):
            while len(self._enemies) > 0:
                totalHP = 0
                for enemy in self._enemies:
                    totalHP += enemy.getHealth()
                print(
                    "There are",
                    len(self._enemies),
                    "enemies in this room! They have",
                    totalHP,
                    "health left! You have",
                    self._map.getPlayer().getHealth(),
                    "health left!"
                )

                action = input("What do you do? attack or run: ")

                if (action == "attack"):
                    damageDone = self._map.getPlayer().generateAttack()
                    weakestEnemy = None

                    for enemy in self._enemies:
                        if (weakestEnemy == None):
                            weakestEnemy = enemy
                        else:
                            if (enemy.getHealth() < weakestEnemy.getHealth()):
                                weakestEnemy = enemy

                    weakestEnemy.applyDamage(damageDone)
                    print("You did", damageDone, "damage!")

                    if (not weakestEnemy.isAlive()):
                        print("You killed an enemy!")
                        self._enemies.remove(weakestEnemy)

                elif (action == "run"):
                    runOutcome = random.random()
                    if (len(self._enemies) > 2):
                        print("Too many enemies to run away!")
                    elif (runOutcome < 0.75):
                        newX = random.randint(0, self._map.getSize() - 1)
                        newY = random.randint(0, self._map.getSize() - 1)
                        print("You ran away!")
                        self._map.getPlayer().runToCell(newX, newY)
                        break
                    else:
                        print("You couldn't escape!")

                totalDamage = 0
                for enemy in self._enemies:
                    totalDamage += enemy.generateAttack()
                self._map.getPlayer().applyDamage(totalDamage)
                print("You took", totalDamage, "damage!")

                if (not self._map.getPlayer().isAlive()):
                    print("You died!")
                    break

            if (len(self._enemies) == 0):
                print("You defeated all the enemies!")
                self._completed = True

    def getRemainingEnemies(self):
        return len(self._enemies)