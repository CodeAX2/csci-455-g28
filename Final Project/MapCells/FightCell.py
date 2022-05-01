from tkinter import *
from MapCell import *
from Enemy import Enemy
from PIL import Image, ImageTk

class FightCell(MapCell):
    def __init__(self, map: Map, x: int, y: int, enemyHealthMin: int, enemyHealthMax: int, enemyAtkMin: int, enemyAtkMax: int, enemyImage: str):
        self._enemies: list[Enemy] = []

        numEnemies = random.randint(3, 6)
        for _ in range(numEnemies):
            enemy: Enemy = Enemy(random.randint(
                enemyHealthMin, enemyHealthMax), enemyAtkMin, enemyAtkMax)
            self._enemies.append(enemy)

        self.__img = ImageTk.PhotoImage(file=enemyImage)

        super().__init__(map, x, y)

    def handleInteraction(self):

        # TODO: Replace print statements with proper dialog, and add animations
        if (not self._completed):
            while len(self._enemies) > 0:
                self.__drawFight()
                totalHP = 0
                for enemy in self._enemies:
                    totalHP += enemy.getHealth()
                numEnemies = len(self._enemies)
                enemiesPronoun = "enemy" if numEnemies == 1 else "enemies"
                enemiesQuantifier = "is" if numEnemies == 1 else "are"
                print(
                    "There",
                    enemiesQuantifier,
                    numEnemies,
                    enemiesPronoun,
                    "in this room! They have",
                    totalHP,
                    "health left! You have",
                    self._map.getPlayer().getHealth(),
                    "health left!"
                )

                action = input("What do you do? attack or run: ")

                if (action == "attack" or action == "a"):
                    damageDone = self._map.getPlayer().generateAttack()
                    weakestEnemy = None

                    for enemy in self._enemies:
                        if (weakestEnemy is None):
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
                    self.__drawDeath()
                    self._completed = True
                    break

            if (len(self._enemies) == 0):
                print("You defeated all the enemies!")
                self._completed = True

    def getRemainingEnemies(self):
        return len(self._enemies)

    def __drawFight(self):
        canvas = self._map.getCanvas()
        canvas.delete("all")

        totalHP = 0

        for i in range(len(self._enemies)):
            canvas.create_image(10 + i * (self.__img.width() + 10), 0, anchor=NW, image=self.__img)
            totalHP += self._enemies[i].getHealth()

        canvas.create_text(
            10, 
            self.__img.height() + 25,
            text=("Enemy HP: " + str(totalHP)), 
            font=("Helvetica","20","bold"),
            anchor=NW
        )

        canvas.create_text(
            10, 
            self.__img.height() + 55,
            text=("Player HP: " + str(self._map.getPlayer().getHealth())), 
            font=("Helvetica","20","bold"),
            anchor=NW
        )

    def __drawDeath(self):
        canvas = self._map.getCanvas()
        canvas.delete("all")

        canvas.create_text(
            canvas.winfo_width()/2, 
            canvas.winfo_height()/2,
            text="YOU DIED!", 
            font=("Helvetica","50","bold"),
            fill="red"
        )

