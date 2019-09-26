import os
import pickle
import enum
from abc import ABC, abstractmethod
from Board import Board
from Dice import Dice
from RuleBook import RuleBook
from Colour import Colour
from Player import PlayerType
from HumanPlayer import HumanPlayer
from ComputerPlayer import ComputerPlayer
from MLPlayer import MLPlayer
from GraphicPlayer import GraphicPlayer
from Move import Move


class GameType(enum.Enum):
    HUMAN = 0
    COMPUTER = 1
    GRAPHIC = 2


class Game(ABC):

    def __init__(self, player_type_1, player_type_2, player1_brain=None,  player2_brain=None):
        self.board = Board()
        self.dice = Dice()
        self.player1 = self.create_player(player_type_1, 0)
        self.player2 = self.create_player(player_type_2, 1)
        self.is_turn_of = None
        self.game_boards = []
        self.available_moves = 0
        self.type = None
        self.starting_player = None

        if player1_brain is not None:
            self.player1.brain = self.player1.brain.load_saved_brain(player1_brain)

        if player2_brain is not None:
            self.player2.brain = self.player2.brain.load_saved_brain(player2_brain)

    @staticmethod
    def create_player(player_type, colour):
        if player_type == PlayerType.HUMAN.name:
            return HumanPlayer(colour)
        elif player_type == PlayerType.COMPUTER.name:
            return ComputerPlayer(colour)
        elif player_type == PlayerType.ML.name:
            return MLPlayer(colour)
        elif player_type == PlayerType.GRAPHIC.name:
            return GraphicPlayer(colour)

    @abstractmethod
    def start(self): pass

    def play(self):
        while not self.is_game_over():
            self.dice.roll()

            if self.type == GameType.HUMAN:
                print(self.roll_to_string())

            if self.has_some_legal_move(self.is_turn_of):
                self.get_player_moves()

            else:
                if self.type == GameType.HUMAN:
                    print(Colour(self.is_turn_of.colour).name + " has no legal moves available.")

            self.change_player()
            self.game_boards.append(self.board.board_to_vector(self.is_turn_of.colour))

        if self.type == GameType.HUMAN:
            self.print_summary()

    def roll_start_roll(self):
        """Sets dice to unique values and selects the starting player"""
        self.dice.start_roll()
        if self.dice.die1 > self.dice.die2:
            self.is_turn_of = self.player1
            self.starting_player = self.player1
        else:
            self.is_turn_of = self.player2
            self.starting_player = self.player2

    def start_to_string(self):
        """Returns a string describing the start roll and who plays first"""
        return Colour(self.player1.colour).name + " rolled " + str(self.dice.die1) + ", " + \
            Colour(self.player2.colour).name + " rolled " + str(self.dice.die2) + ". " + \
            Colour(self.is_turn_of.colour).name + " starts."

    def change_player(self):
        """Swaps the value of the active player"""
        if self.is_turn_of == self.player1:
            self.is_turn_of = self.player2
        else:
            self.is_turn_of = self.player1

    def is_not_turn_of(self):
        """Returns the player that is not active"""
        if self.is_turn_of == self.player1:
            return self.player2
        else:
            return self.player1

    def roll_to_string(self):
        return Colour(self.is_turn_of.colour).name + " rolls " + str(self.dice.die1) + " and " + \
            str(self.dice.die2)

    def is_game_over(self):
        return self.board.get_point_value(0, 25) == 15 or self.board.get_point_value(1, 25) == 15

    def who_won_the_game(self):
        if self.board.get_point_value(self.player1.colour, 25) == 15:
            return self.player1
        else:
            return self.player2

    def winner_to_string(self):
        return Colour(self.who_won_the_game().colour).name + " wins the game"

    def player_move_quantity(self):
        if self.is_turn_of.type == PlayerType.HUMAN and self.available_moves != 0:
            return self.available_moves
        else:
            return self.dice.get_roll_move_quantity()

    def is_blot_hit(self, move):
        return self.board.one_opponent_checker(self.is_turn_of.colour, move.to_point) and move.to_point != 0

    def has_some_legal_move(self, player):
        rulebook = RuleBook(self.board, player, self.dice)
        some_legal_move = rulebook.get_legal_moves()
        return len(some_legal_move) > 0

    def print_summary(self):
        print(self.winner_to_string())
        print("Number of turns in this game:", str(len(self.game_boards)))

    def execute_move(self, move):
        """Executes the move on the board"""
        self.board.move(move)

        if self.is_blot_hit(move):

            if self.type == GameType.HUMAN:
                print(self.board.hit_to_string(self.is_not_turn_of()))

            self.board.apply_hit(move)

        if not self.dice.is_double_dice():
            self.dice.mark_used_die(move)

    def execute_ply(self, ply):
        """Executes the moves contained in a ply"""
        for i in range(len(ply)):
            if self.type == GameType.HUMAN:
                print(ply[i].move_to_string())
            self.execute_move(ply[i])

    def get_player_moves(self):

        if self.type == GameType.HUMAN:
            self.board.print_board(self.is_turn_of.colour)

        if self.is_turn_of.type == PlayerType.COMPUTER or self.is_turn_of.type == PlayerType.ML:
            moves = self.is_turn_of.next_move(self.board, self.dice)
            self.execute_ply(moves)

        if self.is_turn_of.type == PlayerType.HUMAN:
            available_moves = self.player_move_quantity()
            while available_moves > 0 and self.has_some_legal_move(self.is_turn_of):

                move = self.is_turn_of.next_move(self.board, self.dice)

                if isinstance(move, Move):
                    if self.type == GameType.HUMAN:
                        print(move.move_to_string())
                    self.execute_move(move)
                    available_moves -= 1
                else:
                    if move is None or move[0].upper() not in ['S', 'R', 'E']:
                        print("Not a valid move. Please try again.")
                    else:
                        if move[0].upper() == 'S':
                            self.available_moves = available_moves
                            self.save_game()
                            quit()
                        elif move[0].upper() == 'R':
                            if self.dice.is_double_dice():
                                print("Doubles:", str(available_moves), "times", str(self.dice.die1))
                            else:
                                print(self.dice.dice_status_to_string())
                        elif move[0].upper() == 'E':
                            leave_game = input("Are you sure you want to leave the game without saving it? (Y/N) ")
                            if leave_game.upper() == 'Y':
                                quit()

    def save_game(self):
        full_file_name = os.getcwd() + "\\" + \
                         input("Please give a name to the file where you want to save the game: ") + ".txt"
        file = open(full_file_name, 'wb')
        pickle.dump(self, file)
        file.close()

    @staticmethod
    def load_saved_game(file_name):
        path = os.getcwd() + "\\" + file_name + ".txt"
        file = open(path, 'rb')
        saved_game = pickle.load(file)
        file.close()
        return saved_game
