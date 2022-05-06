import random
from types import CellType
from Player import Player
from Direction import Direction
from BColors import BColors
from tkinter import *


class Map:
    def __init__(self,
                robot,
                player: Player,
                 size: int,
                 canvas: Canvas,
                 numRecharge: int,
                 numPuzzle: int,
                 numCoffee: int,
                 numEasy: int,
                 numMedium: int,
                 numHard: int,
                 numRickRoll: int
                 ):
        
        from MapCell import MapCell
        self.robot = robot
        self._cells: list[list[MapCell]] = []
        self._player = player
        self._size = size
        self._canvas = canvas

        self._fillMap(numRecharge, numPuzzle, numCoffee, numEasy, numMedium, numHard, numRickRoll)

    def _fillMap(self,
                  numRecharge: int,
                  numPuzzle: int,
                  numCoffee: int,
                  numEasy: int,
                  numMedium: int,
                  numHard: int,
                  numRickRoll: int
                  ):
        from MapCells import MapCells
        from MapCell import MapCell

        # Create an empty map
        for x in range(self._size):
            curCol: list[MapCell] = []
            for y in range(self._size):
                curCol.append(MapCells.EmptyCell(self, x, y))
            self._cells.append(curCol)

        # Set the start and treasure cells, yeah this is ugly, but oh well
        self._treasureCell: MapCell = None

        startWallSide: Direction = random.choice(list(Direction))
        startPos = random.randint(0, 4)
        treasurePos = random.randint(0, 4)

        if (startWallSide == Direction.NORTH):
            self._cells[startPos][0] = MapCells.StartCell(self, startPos, 0)
            self._cells[treasurePos][self._size - 1] = MapCells.TreasureCell(self, treasurePos, self._size - 1)
            self._treasureCell = self._cells[treasurePos][self._size - 1]
            self._player.spawnPlayer(startPos, 0, self)
        elif (startWallSide == Direction.SOUTH):
            self._cells[startPos][self._size - 1] = MapCells.StartCell(self, startPos, self._size - 1)
            self._cells[treasurePos][0] = MapCells.TreasureCell(
                self, treasurePos, 0)
            self._treasureCell = self._cells[treasurePos][0]
            self._player.spawnPlayer(startPos, self._size - 1, self)
        elif (startWallSide == Direction.WEST):
            self._cells[0][startPos] = MapCells.StartCell(self, 0, startPos)
            self._cells[self._size - 1][treasurePos] = MapCells.TreasureCell(self, self._size - 1, treasurePos)
            self._treasureCell = self._cells[self._size - 1][treasurePos]
            self._player.spawnPlayer(0, startPos, self)
        else:
            self._cells[self._size - 1][startPos] = MapCells.StartCell(self, self._size - 1, startPos)
            self._cells[0][treasurePos] = MapCells.TreasureCell(self, 0, treasurePos)
            self._treasureCell = self._cells[0][treasurePos]
            self._player.spawnPlayer(self._size - 1, startPos, self)

        # Generate Coffee Shops
        self._generateCellsApart(numCoffee, MapCells.CoffeeShopCell)

        # Generate recharge points
        self._generateCellsApart(numRecharge, MapCells.RechargeCell)

        # Generate puzzle points
        self._generateCellsApart(numPuzzle, MapCells.PuzzleCell)

        # Generate rick roll
        self._generateCellsApart(numRickRoll, MapCells.RickRollCell)

        # Generate remaining cells
        self._generateFightCells(numEasy, 1, 1, 1, 1, "Final Project/images/EnemyEasy.png")
        self._generateFightCells(numMedium, 2, 4, 1, 2, "Final Project/images/EnemyMedium.png")
        self._generateFightCells(numHard, 2, 5, 2, 3, "Final Project/images/EnemyHard.png")

        # Populate cell neighbors
        for x in range(self._size):
            for y in range(self._size):
                self._cells[x][y].populateNeighbors()

        # Remove random edges, yes this is scuffed, but it works mostly
        toRemove = int(self._size * self._size / 2)
        while (toRemove != 0):
            x = random.randint(0, self._size - 1)
            y = random.randint(0, self._size - 1)

            cell: MapCell = self._cells[x][y]
            if (cell.getNumNeighbors() > 1):

                smallNeighbor = False
                for i in range(len(cell.getNeighbors())):
                    if (cell.getNeighbors()[i] is not None and cell.getNeighbors()[i].getNumNeighbors() <= 2):
                        smallNeighbor = True
                        break

                if (smallNeighbor):
                    continue

                cell.removeRandomNeighbor()
                toRemove -= 1

    def _generateCellsApart(self, count: int, cellType):
        from MapCells import MapCells
        insertedRecharges: list[tuple[int]] = []
        for _ in range(count):
            while True:
                x = random.randint(0, self._size - 1)
                y = random.randint(0, self._size - 1)
                foundClose = False
                for rech in insertedRecharges:
                    if (abs(rech[0] - x) <= 1 and abs(rech[1] - y) <= 1):
                        foundClose = True
                        break
                if (not foundClose and type(self._cells[x][y]) is MapCells.EmptyCell):
                    self._cells[x][y] = cellType(self, x, y)
                    insertedRecharges.append((x, y))
                    break

    def _generateFightCells(self, count: int, healthMin: int, healthMax: int, atkMin: int, atkMax: int,
                             imagePath: str):
        from MapCells import MapCells
        for _ in range(count):
            while True:
                x = random.randint(0, self._size - 1)
                y = random.randint(0, self._size - 1)
                if (type(self._cells[x][y]) is MapCells.EmptyCell):
                    self._cells[x][y] = MapCells.FightCell(self.robot,
                        self, x, y, healthMin, healthMax, atkMin, atkMax, imagePath)
                    break

    def getCanvas(self):
        return self._canvas

    def getPlayer(self):
        return self._player

    def getCell(self, x: int, y: int):
        return self._cells[x][y]

    def getSize(self):
        return self._size

    def getTreasureCellPosition(self):
        return (self._treasureCell.getX(), self._treasureCell.getY())

    def printMap(self):
        from MapCells import MapCells
        for y in range(self._size):
            line = ""
            lineBelow = ""
            for x in range(self._size):
                cell = self.getCell(x, y)
                if (self._player.getX() == x and self._player.getY() == y):
                    line += BColors.BOLD + "▇" + BColors.ENDC
                elif (type(cell) is MapCells.StartCell):
                    line += BColors.BOLD + "S" + BColors.ENDC
                elif (type(cell) is MapCells.TreasureCell):
                    line += "T"
                elif (type(cell) is MapCells.CoffeeShopCell):
                    line += "C"
                elif (type(cell) is MapCells.RechargeCell):
                    line += BColors.GREEN + "R" + BColors.ENDC
                elif (type(cell) is MapCells.FightCell):
                    line += BColors.RED + str(cell.getRemainingEnemies()) + BColors.ENDC
                elif (type(cell) is MapCells.PuzzleCell):
                    line += BColors.BLUE + "?" + BColors.ENDC
                elif(type(cell) is MapCells.RickRollCell):
                    line += BColors.YELLOW + "!" + BColors.ENDC
                else:
                    line += "X"

                if (cell.getNeighbor(Direction.EAST) is not None):
                    line += "--"
                else:
                    line += "  "

                if (cell.getNeighbor(Direction.SOUTH) is not None):
                    lineBelow += "|  "
                else:
                    lineBelow += "   "
            print(line)
            print(lineBelow)
