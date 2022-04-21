import random
from Player import Player
from Direction import Direction

class Map:
    def __init__(self, player: Player, size: int):
        from MapCell import MapCell
        self.__cells: list[list[MapCell]] = []
        self.__player = player
        self.__size = size

        self.__fillMap()

    def __fillMap(self):
        # Create the map
        # TODO: Fill map with different cell types, and start on perimeter
        from MapCell import MapCell
        for x in range(self.__size):
            curCol: list[MapCell] = []
            for y in range(self.__size):
                curCol.append(MapCell(self, x, y))
            self.__cells.append(curCol)

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

    def getPlayer(self):
        return self.__player

    def getCell(self, x: int, y: int):
        return self.__cells[x][y]

    def getSize(self):
        return self.__size

    def printMap(self):
        for y in range(self.__size):
            line = ""
            lineBelow = ""
            for x in range(self.__size):
                cell = self.getCell(x, y)
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
