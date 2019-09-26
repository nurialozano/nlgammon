import pygame


class Point(pygame.Surface):

    def __init__(self, size, point_number, point_position):
        super(Point, self).__init__((size[0], size[1]), pygame.SRCALPHA)
        self.point_position = point_position
        self.point_number = point_number
        self.checkers = []

    def place_checkers(self):
        x = 5
        if self.point_number > 12:
            y = 0
            for checker in self.checkers:
                checker.x, checker.y = x, y
                y = y + 40
        else:
            y = 160
            for checker in self.checkers:
                checker.x, checker.y = x, y
                y = y - 40

    def draw_checkers(self):
        self.place_checkers()
        for checker in self.checkers:
            self.blit(checker, (checker.x, checker.y))

    def remove_point_checker(self, parent_surface):
        del self.checkers[-1]
        self.blit(parent_surface, (0, 0), pygame.Rect(self.point_position[0], self.point_position[1],
                                                      self.get_width(), self.get_height()))
        self.draw_checkers()
