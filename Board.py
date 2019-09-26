from Testable import Testable
from Colour import Colour
import numpy as np


class Board(Testable):

    def __init__(self):
        """Constructor of board with initial checker layout"""
        self.board = [[0] * 26 for i in range(2)]
        for i in range(2):
            self.board[i][5] += 5
            self.board[i][7] += 3
            self.board[i][12] += 5
            self.board[i][23] += 2

    def print_board(self, colour):
        """Prints a user-friendly representation of the board from the point of view of the given colour"""
        print()
        print("        13  14  15  16  17  18  19  20  21  22  23  24")
        print("        ----------------------------------------------")

        print(Colour(colour).name, "|", end=" ")
        for i in range(12, 24):
            print(self.board[colour][i], end="   ")
        print()

        print(self.opponent_colour_to_string(colour), "|", end=" ")
        for i in range(11, -1, -1):
            print(self.board[self.opponent_colour(colour)][i], end="   ")
        print()
        print()
        print("        12  11  10  9   8   7   6   5   4   3   2   1")
        print("        ----------------------------------------------")

        print(Colour(colour).name, "|", end=" ")
        for i in range(11, -1, -1):
            print(self.board[colour][i], end="   ")
        print()

        print(self.opponent_colour_to_string(colour), "|", end=" ")
        for i in range(12, 24):
            print(self.board[self.opponent_colour(colour)][i], end="   ")
        print()
        print()
        print("        BORNE-OFF   BAR")
        print("        -------------------")
        print(Colour(colour).name, "|", end=" ")
        print(self.board[colour][24], end="\t\t\t")
        print(self.board[colour][25])
        print(self.opponent_colour_to_string(colour), "|", end=" ")
        print(self.board[self.opponent_colour(colour)][24], end="\t\t\t")
        print(self.board[self.opponent_colour(colour)][25])
        print()

    def get_opponent_board(self, colour):
        if colour == 0:
            return self.board[1]
        else:
            return self.board[0]

    def get_point_value(self, colour, point):
        """Returns the number of checkers at a specified point"""
        return self.board[colour][point - 1]

    def at(self, colour, point):
        """Returns a tuple with the number of checkers for each player at a given point"""
        if 0 <= point <= 24:
            if colour == 0:
                b, w = self.board[0][point - 1], self.board[1][24 - point]
            else:
                b, w = self.board[0][24 - point], self.board[1][point - 1]

        elif 24 < point <= 26:
            b, w = self.board[0][point - 1], self.board[1][point - 1]

        else:
            raise ValueError

        return (b, w)

    def is_empty(self, colour, point):
        """Indicates whether a point has no checkers from either player"""
        return self.at(colour, point) == (0, 0)

    def bar_is_empty(self, colour):
        """Returns true if there are no checkers on the bar of the given player, false otherwise"""
        return self.board[colour][25] == 0

    def contains_own_checkers(self, colour, point):
        """Returns whether a point contains checkers of the given player"""
        b, w = self.at(colour, point)
        if colour == 0:
            return b > 0
        else:
            return w > 0

    def one_opponent_checker(self, colour, point):
        """Returns whether a point contains only one opponent checker"""
        b, w = self.at(colour, point)
        if colour == 0:
            return w == 1
        else:
            return b == 1

    def add_checker(self, colour, point):
        """Adds a checker at the given point for the given player"""
        self.board[colour][point - 1] += 1

    def remove_checker(self, colour, point):
        """Removes a checker from the given point for the given player"""
        if self.board[colour][point - 1] == 0:
            raise ValueError
        else:
            self.board[colour][point - 1] -= 1

    def move(self, move):
        """Alters the board to reflect the player's move"""
        if move.to_point == 0:
            self.add_checker(move.colour, 25)
        else:
            self.add_checker(move.colour, move.to_point)
        self.remove_checker(move.colour, move.from_point)

    def apply_hit(self, move):
        """Moves the opponent's blot that has been hit to the bar"""
        self.remove_checker(self.opponent_colour(move.colour), 25 - move.to_point)
        self.add_checker(self.opponent_colour(move.colour), 26)

    @staticmethod
    def opponent_colour_to_string(colour):
        for clr in Colour:
            if clr.value != colour:
                return clr.name

    @staticmethod
    def opponent_colour(colour):
        for clr in Colour:
            if clr.value != colour:
                return clr.value

    @staticmethod
    def hit_to_string(player):
        return Colour(player.colour).name + " checker is hit"

    def board_to_vector(self, colour):
        """Returns the board into a vector for the neural network,
        colour corresponds to the player whose turn it is to play"""
        onedboard = []
        for i in range(2):
            for j in range(24):
                n = self.board[i][j]
                if n == 0:
                    onedboard += [0, 0, 0, 0]
                elif n == 1:
                    onedboard += [1, 0, 0, 0]
                elif n == 2:
                    onedboard += [0, 1, 0, 0]
                elif n == 3:
                    onedboard += [0, 0, 1, 0]
                elif n > 3:
                    onedboard += [0, 0, 0]
                    onedboard += [(n-3) / 2]

        for i in range(2):
            onedboard += [self.board[i][24] / 15]
            onedboard += [self.board[i][25] / 2]

        onedboard += [int(colour == 0)]
        onedboard += [int(colour == 1)]

        return np.array(onedboard)
