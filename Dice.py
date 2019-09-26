import random
from Testable import Testable


class Dice(Testable):

    def __init__(self):
        self.die1 = random.randint(1, 6)
        self.die2 = random.randint(1, 6)

    def set_dice(self, die1, die2):
        """Useful for tests"""
        self.die1 = die1
        self.die2 = die2

    def get_lowest_die(self):
        if self.die1 > self.die2:
            return self.die2
        else:
            return self.die1

    def get_roll_move_quantity(self):
        """Returns the number of times the player can play in a turn according to the roll of the dice"""
        if self.is_double_dice():
            return 4
        elif self.die1 == 0 or self.die2 == 0:
            return 1
        else:
            return 2

    def is_double_dice(self):
        return self.die1 == self.die2

    def roll(self):
        """Assigns new random values to the dice"""
        self.die1 = random.randint(1, 6)
        self.die2 = random.randint(1, 6)

    def start_roll(self):
        """Assigns unique values to each die"""
        self.die1, self.die2 = random.sample(range(1, 7), 2)

    def dice_status_to_string(self):
        """Returns a string with the value of the dice that can still be played"""
        dice_status = "Dice to play: "

        if self.die1 != 0 and self.die2 != 0:
            dice_status += str(self.die1) + " and " + str(self.die2)

        elif self.die1 == 0:
            dice_status += str(self.die2)

        else:
            dice_status += str(self.die1)

        return dice_status

    def mark_used_die(self, move):
        """Sets the value of the die used in the move to 0"""
        if move.from_point == 26:
            die_value = move.from_point - move.to_point - 1
        else:
            die_value = move.from_point - move.to_point

        if self.die1 == die_value:
            self.die1 = 0
        else:
            self.die2 = 0
