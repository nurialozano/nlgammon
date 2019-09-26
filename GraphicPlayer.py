from Player import Player, PlayerType
from Move import Move
from Testable import Testable
from RuleBook import RuleBook


class GraphicPlayer(Player, Testable):

    def __init__(self, colour):
        super(GraphicPlayer, self).__init__(colour)
        self.type = PlayerType.GRAPHIC

    def next_move(self, board, dice):
        return RuleBook(board, self, dice).get_legal_moves()
