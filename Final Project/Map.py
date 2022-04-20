from Player import Player

class Map:
    def __init__(self, player: Player):
        self.__cells = []
        self.__player = player
