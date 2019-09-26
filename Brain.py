from sklearn.neural_network import MLPRegressor
from sklearn.exceptions import NotFittedError
import os
import pickle
import numpy as np
from Board import Board


class Brain:
    def __init__(self):
        self.neural_network = MLPRegressor(hidden_layer_sizes=(50, 1,), activation='logistic', solver='sgd',
                                           learning_rate_init=1, max_iter=1)
        self.neural_network.warm_start = True
        self.games_played = 0
        self.name = None
        self.lambda_value = 0.7

    def save_brain(self, file_name=None):
        if file_name is None:
            file_name = input("Please give a name to the brain: ")
        self.name = file_name
        full_file_name = os.getcwd() + "\\" + file_name + ".txt"
        file = open(full_file_name, 'wb')
        pickle.dump(self, file)
        file.close()

    @staticmethod
    def load_saved_brain(file_name):
        path = os.getcwd() + "\\" + file_name + ".txt"
        file = open(path, 'rb')
        saved_brain = pickle.load(file)
        file.close()
        return saved_brain

    def train_brain(self, game_boards, game_winner_colour):
        to_fit = self.generate_to_fit_vector(game_boards, game_winner_colour).ravel()
        self.neural_network.fit(game_boards, to_fit)

    def generate_to_fit_vector(self, game_boards, game_winner_colour):

        try:
            initial_probability_array = [self.neural_network.predict(i.reshape(1, -1)) for i in game_boards]
        except NotFittedError:
            self.neural_network.fit(game_boards, np.ones((len(game_boards),)) * game_winner_colour)
            initial_probability_array = [self.neural_network.predict(i.reshape(1, -1)) for i in game_boards]

        computed_probability_array = [0] * len(initial_probability_array)

        sum_distance = 0
        next_value = game_winner_colour

        for i in range(len(initial_probability_array)-1, -1, -1):
            current_value = initial_probability_array[i]
            sum_distance += (next_value - current_value)
            computed_probability_array[i] = current_value + 0.05 * sum_distance

            sum_distance *= self.lambda_value

            next_value = initial_probability_array[i]

        return np.array(computed_probability_array)

    def black_white_scoring(self):
        test_board = Board()
        test_board.board = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 0]]
        return self.neural_network.predict([test_board.board_to_vector(0)]), \
               self.neural_network.predict([test_board.board_to_vector(1)])
