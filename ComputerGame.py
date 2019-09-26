from Game import Game, GameType


class ComputerGame(Game):

    def __init__(self, player_type_1, player_type_2, player1_brain=None, player2_brain=None):
        super(ComputerGame, self).__init__(player_type_1, player_type_2, player1_brain, player2_brain)
        self.type = GameType.COMPUTER

    def start(self):
        self.roll_start_roll()
        self.get_player_moves()
        self.change_player()
        self.play()
