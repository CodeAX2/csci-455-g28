from tkinter import *
from MapCell import *
from Enemy import Enemy
from PIL import Image, ImageTk
from TTS import sayText
from Speech import getSpeechInput
from KeyboardInput import read_single_keypress
from main import useKeyboard

from RobotMovement import RobotMovement

def getActionFromKeyboard():
	while True:
		key = read_single_keypress()
		if(len(key) == 3): # Special Key codes for arrow keys
			print(key)
			print("Unknown Key: ", key[2])
		else:
			if(key[0] == "a"):
				return "attack"
				# robot.increaseSpeed()
			elif(key[0] == "r"):
				return "run"
				# robot.increaseSpeed(-1)
			else:
				# Unknown key
				print("Unknown key: ", key[0])

class FightCell(MapCell):
	def __init__(self, robot, map: Map, x: int, y: int, enemyHealthMin: int, enemyHealthMax: int, enemyAtkMin: int, enemyAtkMax: int, enemyImage: str):
		self._enemies: list[Enemy] = []

		self.robomover = RobotMovement(robot)
		numEnemies = random.randint(1, 1)
		for _ in range(numEnemies):
			enemy: Enemy = Enemy(random.randint(
				enemyHealthMin, enemyHealthMax), enemyAtkMin, enemyAtkMax)
			self._enemies.append(enemy)

		self.__img = ImageTk.PhotoImage(file=enemyImage)

		super().__init__(map, x, y)

	def handleInteraction(self):
		if (not self._completed):
			while len(self._enemies) > 0:
				self.__drawFight()
				totalHP = 0
				for enemy in self._enemies:
					totalHP += enemy.getHealth()
				numEnemies = len(self._enemies)

				# Tell the user about the number of enemies
				enemiesPronoun = "enemy" if numEnemies == 1 else "enemies"
				enemiesQuantifier = "is" if numEnemies == 1 else "are"
				sayText(
					"There %s %s with %s health vs your %s. Attack or run?" % 
						(str(enemiesQuantifier), enemiesPronoun, str(totalHP), str(self._map.getPlayer().getHealth()))
				)
				if useKeyboard:
					action = getActionFromKeyboard()
				else:
					action = getSpeechInput()

				# Actually fight the enemies
				attackResultSayStr = "" # Keep track of result to say
				if ("attack" in action):
					damageDone = self._map.getPlayer().generateAttack()
					self.robomover.attack()
					weakestEnemy = None

					for enemy in self._enemies:
						if (weakestEnemy is None):
							weakestEnemy = enemy
						else:
							if (enemy.getHealth() < weakestEnemy.getHealth()):
								weakestEnemy = enemy

					weakestEnemy.applyDamage(damageDone)
					killedEnemy = False

					if (not weakestEnemy.isAlive()):
						self._enemies.remove(weakestEnemy)
						killedEnemy = True

					self.__drawFight()

					# sayText("You did " + str(damageDone) + " damage!")
					# if (killedEnemy):
					# 	sayText("You killed an enemy!")                    
					attackResultSayStr += "You did " + str(damageDone) + " damage"
					if(killedEnemy):
						attackResultSayStr += ", killed an enemy "

				elif ("run" in action):
					runOutcome = random.random()
					if (len(self._enemies) > 2):
						attackResultSayStr += "Too many enemies to escape"
					elif (runOutcome < 0.75):
						# TODO don't teleport across map
						newX = random.randint(0, self._map.getSize() - 1)
						newY = random.randint(0, self._map.getSize() - 1)
						attackResultSayStr += "You ran away "
						sayText(attackResultSayStr)
						self._map.getPlayer().runToCell(newX, newY)
						break
					else:
						attackResultSayStr += "You got unlucky, couldn't escape"
				else:
					attackResultSayStr += "Invalid Option "
					sayText(attackResultSayStr)
					continue

				totalDamage = 0
				for enemy in self._enemies:
					totalDamage += enemy.generateAttack()
				self._map.getPlayer().applyDamage(totalDamage)
				self.__drawFight()
				attackResultSayStr += (", and took " + str(totalDamage) + " damage ")

				if (not self._map.getPlayer().isAlive()):
					self.__drawDeath()
					attackResultSayStr += " You died!"
					self._completed = True
					sayText(attackResultSayStr)
					break

				if (len(self._enemies) == 0):
					attackResultSayStr += ", defeating all the enemies"
					self._completed = True
				
				sayText(attackResultSayStr)

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

