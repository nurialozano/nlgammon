from Testable import Testable
from Colour import Colour


class Move(Testable):
    from_point = 0
    to_point = 0
    colour = 0

    def __init__(self, colour, from_point, to_point):
        self.colour = colour
        self.from_point = from_point
        self.to_point = to_point

    def get_number_of_positions(self):
        """Returns the number of spaces traversed in a move"""
        return self.from_point - self.to_point

    def move_to_string(self):
        return Colour(self.colour).name + " checker moves from point " + str(self.from_point) + " to point " + \
            str(self.to_point)


