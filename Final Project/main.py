from Player import Player
from Map import Map
from Direction import Direction

if __name__ == "__main__":

    p = Player(None, 100, 1, 10, 50)
    m = Map(p, 5, 3, 2, 6, 5, 3)

    remainingMoves = 50

    while (p.isAlive() and not p.hasWon() and remainingMoves >= 1):
        remainingMoves -= 1

        m.printMap()

        curCell = m.getCell(p.getX(), p.getY())

        # Get available directions
        available = []
        for dir in list(Direction):
            if (curCell.getNeighbor(dir) != None):
                available.append(dir)

        query = "i can go"
        for dir in available:
            if (dir == Direction.NORTH):
                query += " north"
            elif (dir == Direction.EAST):
                query += " east"
            elif (dir == Direction.SOUTH):
                query += " south"
            elif (dir == Direction.WEST):
                query += " west"

        query += ". What direction should I go? "
        toGo = input(query)

        dirToGo = None
        if (toGo == "north"):
            dirToGo = Direction.NORTH
        elif (toGo == "south"):
            dirToGo = Direction.SOUTH
        elif (toGo == "east"):
            dirToGo = Direction.EAST
        elif (toGo == "west"):
            dirToGo = Direction.WEST

        if (dirToGo != None):
            if (p.move(dirToGo)):
                continue

        print("Invalid direction!")

    if (remainingMoves <= 0):
        print("You ran out of moves!")
        

        

# TODO:
# Proper output engine for robot
# Robot animations
# Screen animations
# User input loop
# Finish fun and puzzle cells