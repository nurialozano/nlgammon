import numpy as np
import copy

from Player import Player, PlayerType
from RuleBook import RuleBook
from Testable import Testable
from Brain import Brain


class MLPlayer(Player, Testable):

    def __init__(self, colour):
        super(MLPlayer, self).__init__(colour)
        self.type = PlayerType.ML
        self.brain = Brain()

    def next_move(self, board, dice):
        """Returns the best ply for the player from the list of possible plies"""
        rulebook = RuleBook(board, self, dice)
        plies = rulebook.generate_legal_ply_list()
        return self.pick_best_move(plies, board)

    def pick_best_move(self, plies, board):
        """Goes through the list of possible plies and returns the one that
        would give the player the highest chances of winning depending on the player's colour"""
        probabilities = np.array([self.get_probability_of_whites_win(i, board) for i in plies])
        return plies[np.argmin(probabilities) if self.colour == 0 else np.argmax(probabilities)]

    def get_probability_of_whites_win(self, ply, board):
        """Executes the ply in a copy of the board and returns the neural network's prediction of the chances of
        the whites to win for the given move"""
        board_copy = copy.deepcopy(board)
        for move in ply:
            board_copy.move(move)
        board_vector = board_copy.board_to_vector(board.opponent_colour(self.colour))
        return self.brain.neural_network.predict(board_vector.reshape(1, -1))
