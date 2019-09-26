import pygame


class Checker(pygame.Surface):

    #  x,y is the center of the checker

    def __init__(self, colour):
        super(Checker, self).__init__((40, 40), pygame.SRCALPHA)
        self.x, self.y = 20, 20
        self.colour = colour
        pygame.draw.circle(self, self.colour, (self.x, self.y), 20, 0)
