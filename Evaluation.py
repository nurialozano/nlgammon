class Evaluation:

    def __init__(self, winner, game_turns, starting_player):
        self.winner = winner
        self.game_turns = game_turns
        self.starting_player = starting_player

    def get_average_turns(self):
        total_turns = 0
        for result in self.game_turns:
            total_turns += result
        return total_turns/len(self.game_turns)

    def evaluate(self):
        print("Number of times BLACK won:", self.winner[0])
        print("Number of times BLACK started:", self.starting_player[0])
        print("Number of times WHITE won:", self.winner[1])
        print("Number of times WHITE started:", self.starting_player[1])
        print(self.game_turns)
        print("Average number of turns: ", self.get_average_turns())
