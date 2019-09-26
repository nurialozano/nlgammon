from Player import Player, PlayerType
from RuleBook import RuleBook
import random
from Testable import Testable


class ComputerPlayer(Player, Testable):

    def __init__(self, colour):
        super(ComputerPlayer, self).__init__(colour)
        self.type = PlayerType.COMPUTER

    def next_move(self, board, dice):
        """Returns a random ply from the list of legal plies"""
        rulebook = RuleBook(board, self, dice)
        legal_plies = rulebook.generate_legal_ply_list()
        return random.choice(legal_plies)
