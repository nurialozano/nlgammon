from Player import Player, PlayerType
from Move import Move
from Testable import Testable
from RuleBook import RuleBook


class HumanPlayer(Player, Testable):

    def __init__(self, colour):
        super(HumanPlayer, self).__init__(colour)
        self.type = PlayerType.HUMAN

    def next_move(self, board, dice):
        user_input = input("What is your move? ").split(" ")

        if len(user_input) == 2 and int(user_input[0]) in list(range(0, 27)) and \
                int(user_input[1]) in list(range(0, 27)):
            move = Move(self.colour, int(user_input[0]), int(user_input[1]))

            possible_moves = RuleBook(board, self, dice).get_legal_moves()

            if move in possible_moves:
                return move

        else:
            return user_input
