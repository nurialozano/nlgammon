from GUI.Colours import Colours
from GUI.Point import Point


class BarPoint(Point):

    def __init__(self, size, point_number, point_position):
        super(BarPoint, self).__init__((size[0], size[1]), point_number, point_position)
        self.point_position = point_position
        self.point_number = point_number
        self.checkers = []

    def place_checkers(self):
        x_black, y_black = 5, 200
        x_white, y_white = 5, 240

        for checker in self.checkers:
            if checker.colour == Colours.BLACK.value:
                checker.x, checker.y = x_black, y_black
                y_black = y_black - 40
            elif checker.colour == Colours.WHITE.value:
                checker.x, checker.y = x_white, y_white
                y_white = y_white + 40
