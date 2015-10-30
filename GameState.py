from enum import Enum

__author__ = 'reneb_000'

class GameState():

    def __init__(self, state):
        self.state = state

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state


class GameStateEnum(Enum):
    running = 0
    mainmenu = 2
    shop = 3