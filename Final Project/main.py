from Player import Player
from Map import Map

if __name__ == "__main__":

    p = Player(None, 100, 1, 5, 50)
    m = Map(p, 5)
    m.printMap()
