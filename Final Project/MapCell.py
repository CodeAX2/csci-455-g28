from pickle import TRUE
import random
from Direction import Direction
from Map import Map

class MapCell:

    def __init__(self, map: Map, x: int, y: int):
        self._completed = False

        self._north: MapCell = None
        self._south: MapCell = None
        self._east: MapCell = None
        self._west: MapCell = None

        self._map = map
        self._x = x
        self._y = y

    def isComplete(self):
        return self._completed

    def handleInteraction():
        pass

    def getNeighbors(self):
        return (self._north, self._east, self._south, self._west)

    def getNeighbor(self, direction: Direction):
        if (direction == Direction.NORTH):
            return self._north
        elif (direction == Direction.EAST):
            return self._east
        elif (direction == Direction.SOUTH):
            return self._south
        else:
            return self._west

    def getMap(self):
        return self._map

    # This assigns neighbors to this cell from the map
    def populateNeighbors(self):
        mapSize = self._map.getSize()

        # Populate North
        if (self._y > 0):
            self._north = self._map.getCell(self._x, self._y - 1)

        # Populate West
        if (self._x > 0):
            self._west = self._map.getCell(self._x - 1, self._y)

        # Populate South
        if (self._y < mapSize - 1):
            self._south = self._map.getCell(self._x, self._y + 1)

        # Populate East
        if (self._x < mapSize - 1):
            self._east = self._map.getCell(self._x + 1, self._y)

    def getNeighbor(self, direction: Direction):
        if (direction == Direction.NORTH):
            return self._north
        elif (direction == Direction.EAST):
            return self._east
        elif (direction == Direction.SOUTH):
            return self._south
        elif (direction == Direction.WEST):
            return self._west

    def removeNeighbor(self, direction: Direction):
        if (direction == Direction.NORTH):
            self._north = None
        elif (direction == Direction.EAST):
            self._east = None
        elif (direction == Direction.SOUTH):
            self._south = None
        elif (direction == Direction.WEST):
            self._west = None

    def removeRandomNeighbor(self):
        removed = False
        while (not removed):
            direction = random.randint(0,3)
            if (direction == 0 and self._north != None):
                self._north.removeNeighbor(Direction.SOUTH)
                self._north = None
                removed = True
            elif (direction == 1 and self._east != None):
                self._east.removeNeighbor(Direction.WEST)
                self._east = None
                removed = True
            elif (direction == 2 and self._south != None):
                self._south.removeNeighbor(Direction.NORTH)
                self._south = None
                removed = True
            elif (direction == 3 and self._west != None):
                self._west.removeNeighbor(Direction.EAST)
                self._west = None
                removed = True


    def getNumNeighbors(self):
        total = 0
        if (self._north != None):
            total += 1
        if (self._east != None):
            total += 1
        if (self._south != None):
            total += 1
        if (self._west != None):
            total += 1
        return total

    def getX(self):
        return self._x

    def getY(self):
        return self._y
