import random
from types import CellType
from Player import Player
from Direction import Direction
from tkinter import *


class Map:
    def __init__(self, player: Player, 
                size: int,
                canvas: Canvas,
                numRecharge: int,
                numCoffee: int,
                numEasy: int,
                numMedium: int,
                numHard: int
    ):
        from MapCell import MapCell
        self.__cells: list[list[MapCell]] = []
        self.__player = player
        self.__size = size
        self.__canvas = canvas

        self.__fillMap(numRecharge, numCoffee, numEasy, numMedium, numHard)

    def __fillMap(self,
                  numRecharge: int,
                  numCoffee: int,
                  numEasy: int,
                  numMedium: int,
                  numHard: int
                  ):
        from MapCells import MapCells
        from MapCell import MapCell

        # Create an empty map
        for x in range(self.__size):
            curCol: list[MapCell] = []
            for y in range(self.__size):
                curCol.append(MapCells.EmptyCell(self, x, y))
            self.__cells.append(curCol)

        # Set the start and treasure cells, yeah this is ugly, but oh well
        self.__treasureCell: MapCell = None

        startWallSide: Direction = random.choice(list(Direction))
        startPos = random.randint(0, 4)
        treasurePos = random.randint(0, 4)

        if (startWallSide == Direction.NORTH):
            self.__cells[startPos][0] = MapCells.StartCell(self, startPos, 0)
            self.__cells[treasurePos][self.__size - 1] = MapCells.TreasureCell(self, treasurePos, self.__size - 1)
            self.__treasureCell = self.__cells[treasurePos][self.__size - 1]
            self.__player.spawnPlayer(startPos, 0, self)
        elif (startWallSide == Direction.SOUTH):
            self.__cells[startPos][self.__size - 1] = MapCells.StartCell(self, startPos, self.__size - 1)
            self.__cells[treasurePos][0] = MapCells.TreasureCell(
                self, treasurePos, 0)
            self.__treasureCell = self.__cells[treasurePos][0]
            self.__player.spawnPlayer(startPos, self.__size - 1, self)
        elif (startWallSide == Direction.WEST):
            self.__cells[0][startPos] = MapCells.StartCell(self, 0, startPos)
            self.__cells[self.__size - 1][treasurePos] = MapCells.TreasureCell(self, self.__size - 1, treasurePos)
            self.__treasureCell = self.__cells[self.__size - 1][treasurePos]
            self.__player.spawnPlayer(0, startPos, self)
        else:
            self.__cells[self.__size - 1][startPos] = MapCells.StartCell(self, self.__size - 1, startPos)
            self.__cells[0][treasurePos] = MapCells.TreasureCell(self, 0, treasurePos)
            self.__treasureCell = self.__cells[0][treasurePos]
            self.__player.spawnPlayer(self.__size - 1, startPos, self)

        # Generate Coffee Shops
        self.__generateCellsApart(numCoffee, MapCells.CoffeeShopCell)

        # Generate recharge points
        self.__generateCellsApart(numRecharge, MapCells.RechargeCell)

        # Generate remaining cells
        self.__generateFightCells(numEasy, 1, 3, 1, 1)
        self.__generateFightCells(numMedium, 2, 4, 1, 2)
        self.__generateFightCells(numHard, 2, 5, 2, 3)

        # TODO: Other fun cells

        # Populate cell neighbors
        for x in range(self.__size):
            for y in range(self.__size):
                self.__cells[x][y].populateNeighbors()

        # Remove random edges, yes this is scuffed, but it works mostly
        toRemove = int(self.__size * self.__size / 2)
        while (toRemove != 0):
            x = random.randint(0, self.__size - 1)
            y = random.randint(0, self.__size - 1)

            cell: MapCell = self.__cells[x][y]
            if (cell.getNumNeighbors() > 1):

                smallNeighbor = False
                for i in range(len(cell.getNeighbors())):
                    if (cell.getNeighbors()[i] != None and cell.getNeighbors()[i].getNumNeighbors() <= 2):
                        smallNeighbor = True
                        break

                if (smallNeighbor):
                    continue

                cell.removeRandomNeighbor()
                toRemove -= 1

    def __generateCellsApart(self, count: int, cellType):
        from MapCells import MapCells
        insertedRecharges: list[tuple[int]] = []
        for _ in range(count):
            while True:
                x = random.randint(0, self.__size - 1)
                y = random.randint(0, self.__size - 1)
                foundClose = False
                for rech in insertedRecharges:
                    if (abs(rech[0] - x) <= 1 and abs(rech[1] - y) <= 1):
                        foundClose = True
                        break
                if (not foundClose and type(self.__cells[x][y]) is MapCells.EmptyCell):
                    self.__cells[x][y] = cellType(self, x, y)
                    insertedRecharges.append((x, y))
                    break

    def __generateFightCells(self, count: int, healthMin: int, healthMax: int, atkMin: int, atkMax: int):
        from MapCells import MapCells
        for _ in range(count):
            while True:
                x = random.randint(0, self.__size - 1)
                y = random.randint(0, self.__size - 1)
                if (type(self.__cells[x][y]) is MapCells.EmptyCell):
                    self.__cells[x][y] = MapCells.FightCell(
                        self, x, y, healthMin, healthMax, atkMin, atkMax)
                    break

    def getCanvas(self):
        return self.__canvas

    def getPlayer(self):
        return self.__player

    def getCell(self, x: int, y: int):
        return self.__cells[x][y]

    def getSize(self):
        return self.__size

    def getTreasureCellPosition(self):
        return (self.__treasureCell.getX(), self.__treasureCell.getY())

    def printMap(self):
        from MapCells import MapCells
        for y in range(self.__size):
            line = ""
            lineBelow = ""
            for x in range(self.__size):
                cell = self.getCell(x, y)
                if (self.__player.getX() == x and self.__player.getY() == y):
                    line += "P"
                elif (type(cell) is MapCells.StartCell):
                    line += "S"
                elif (type(cell) is MapCells.TreasureCell):
                    line += "T"
                elif (type(cell) is MapCells.CoffeeShopCell):
                    line += "C"
                elif (type(cell) is MapCells.RechargeCell):
                    line += "R"
                elif (type(cell) is MapCells.FightCell):
                    line += str(cell.getRemainingEnemies())
                else:
                    line += "X"

                if (cell.getNeighbor(Direction.EAST) != None):
                    line += "--"
                else:
                    line += "  "

                if (cell.getNeighbor(Direction.SOUTH) != None):
                    lineBelow += "|  "
                else:
                    lineBelow += "   "
            print(line)
            print(lineBelow)

