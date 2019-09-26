import pygame

from GUI.Measures import Measures
from GUI.Colours import Colours
from GUI.Point import Point


class BearoffPoint(Point):

    def __init__(self, size, point_number, point_position):
        super(BearoffPoint, self).__init__((size[0], size[1]), point_number, point_position)
        self.point_position = point_position
        self.point_number = point_number
        self.checkers = []

    def place_checkers(self):
        x_black, y_black = 5, 5
        x_white, y_white = 5, 45

        for checker in self.checkers:
            if checker.colour == Colours.BLACK.value:
                checker.x, checker.y = x_black, y_black
                x_black = x_black + 40
            if checker.colour == Colours.WHITE.value:
                checker.x, checker.y = x_white, y_white
                x_white = x_white + 40

    def remove_point_checker(self, parent_surface):
        del self.checkers[-1]
        self.blit(parent_surface, (0, 0), pygame.Rect(Measures.BORDERSIZE.value, Measures.BORDERSIZE.value,
                                                    (Measures.QUADRANTWIDTH.value * 2) + 10,
                                                    Measures.BOTTOMHEIGHT.value - (Measures.BORDERSIZE.value * 2)))
        self.draw_checkers()