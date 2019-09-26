from ComputerGame import ComputerGame
from Evaluation import Evaluation
from Brain import Brain


class Training:

    def __init__(self, brain=None):
        self.brain = Brain()
        self.game_turns = []
        self.winner = dict()
        self.starting_player = dict()
        self.evaluation = Evaluation(self.winner, self.game_turns, self.starting_player)
        self.start_board_estimation = []
        self.white_20_estimation = []
        self.black_100_estimation = []

        if brain is None:
            self.initialize_neural_network()
        else:
            self.brain = self.brain.load_saved_brain(brain)

    def initialize_neural_network(self):
        init_game = ComputerGame('COMPUTER', 'COMPUTER')
        init_game.start()
        self.brain.train_brain(init_game.game_boards, init_game.who_won_the_game().colour)

    def train(self, iterations, names):

        name_index = 0

        for i in range(iterations[-1]):
            game = ComputerGame('ML', 'ML')
            game.player1.brain = self.brain
            game.player2.brain = self.brain
            game.start()

            self.brain.train_brain(game.game_boards, game.who_won_the_game().colour)
            self.brain.games_played += 1

            if i >= iterations[name_index]-1:
                self.brain.save_brain(names[name_index])
                name_index += 1

            start_board_estimation = self.brain.neural_network.predict([game.game_boards[0]])
            black, white = self.brain.black_white_scoring()
            self.start_board_estimation.append(start_board_estimation)
            self.white_20_estimation.append(white)
            self.black_100_estimation.append(black)
