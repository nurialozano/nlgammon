from abc import ABC, abstractmethod
import enum


class PlayerType(enum.Enum):
    HUMAN = 0
    COMPUTER = 1
    ML = 2
    GRAPHIC = 3


class Player(ABC):

    def __init__(self, colour):
        self.colour = colour

    @abstractmethod
    def next_move(self, board, dice): pass
