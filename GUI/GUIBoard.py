import pygame
from pygame.locals import *
from GUI.Colours import Colours
from GUI.Measures import Measures
from GUI.Point import Point
from GUI.BarPoint import BarPoint
from GUI.BearoffPoint import BearoffPoint
from GUI.Checker import Checker


class GUIBoard:
    def __init__(self):
        pass

    def generate_board_surface(self):
        boardSurf = pygame.Surface((Measures.BOARDWIDTH.value, Measures.BOARDHEIGHT.value))
        boardSurf.fill(Colours.SOFT_TEAL.value)

        # quadrants
        leftHalf = Rect(Measures.BORDERSIZE.value, Measures.BORDERSIZE.value, Measures.QUADRANTWIDTH.value,
                        Measures.QUADRANTHEIGHT.value)
        rightHalf = Rect(Measures.BORDERSIZE.value + Measures.QUADRANTWIDTH.value + Measures.BARSIZE.value,
                         Measures.BORDERSIZE.value, Measures.QUADRANTWIDTH.value, Measures.QUADRANTHEIGHT.value)

        pygame.draw.rect(boardSurf, Colours.TEAL.value, leftHalf)
        pygame.draw.rect(boardSurf, Colours.TEAL.value, rightHalf)

        self.draw_board_triangles(boardSurf)

        self.create_points()

        return boardSurf

    def draw_board_triangles(self, surface):
        width = ['left', 'right']
        height = ['top', 'bottom']

        for i in range(2):
            for j in range(2):
                self.draw_triangles(surface, width[i], height[j])

    @staticmethod
    def draw_triangles(surface, width, height):
        if width == 'left':
            x = Measures.BORDERSIZE.value
        else:
            x = Measures.BORDERSIZE.value + Measures.QUADRANTWIDTH.value + Measures.BARSIZE.value

        if height == 'top':
            y = Measures.BORDERSIZE.value
            tip = y + Measures.TRIANGLEHEIGHT.value
        else:
            y = Measures.BORDERSIZE.value + Measures.QUADRANTHEIGHT.value
            tip = y - Measures.TRIANGLEHEIGHT.value

        left_point = (x, y)
        right_point = (x + Measures.TRIANGLEWIDTH.value, y)
        tip_point = (x + (Measures.TRIANGLEWIDTH.value / 2), tip)

        for i in range(6):
            points = [left_point, right_point, tip_point]
            if i % 2 == 0 and height == 'top' or i % 2 != 0 and height == 'bottom':
                pygame.draw.polygon(surface, Colours.ORANGE.value, points)
            else:
                pygame.draw.polygon(surface, Colours.ORANGE.value, points, 2)

            left_point = right_point
            right_point = (left_point[0] + Measures.TRIANGLEWIDTH.value, y)
            tip_point = (tip_point[0] + Measures.TRIANGLEWIDTH.value, tip)

    @staticmethod
    def create_points():
        points = []

        point = BearoffPoint(((Measures.QUADRANTWIDTH.value * 2) + Measures.BARSIZE.value,
                                     Measures.BOTTOMHEIGHT.value - Measures.BORDERSIZE.value),
                             0, (Measures.BORDERSIZE.value, Measures.BOARDHEIGHT.value + Measures.BORDERSIZE.value))
        points.append(point)

        x = Measures.BOARDWIDTH.value - Measures.BORDERSIZE.value - Measures.TRIANGLEWIDTH.value
        y = Measures.BOARDHEIGHT.value - Measures.BORDERSIZE.value - Measures.TRIANGLEHEIGHT.value
        for i in range(1, 7):
            point = Point((50, 200), i, (x, y))
            points.append(point)
            x = x - Measures.TRIANGLEWIDTH.value

        x = Measures.BOARDWIDTH.value - Measures.BORDERSIZE.value - Measures.QUADRANTWIDTH.value \
            - Measures.BARSIZE.value - Measures.TRIANGLEWIDTH.value
        y = Measures.BOARDHEIGHT.value - Measures.BORDERSIZE.value - Measures.TRIANGLEHEIGHT.value
        for i in range(7, 13):
            point = Point((50, 200), i, (x, y))
            points.append(point)
            x = x - Measures.TRIANGLEWIDTH.value

        x = Measures.BORDERSIZE.value
        y = Measures.BORDERSIZE.value
        for i in range(13, 19):
            point = Point((50, 200), i, (x, y))
            points.append(point)
            x = x + Measures.TRIANGLEWIDTH.value

        x = Measures.BORDERSIZE.value + Measures.QUADRANTWIDTH.value + Measures.BARSIZE.value
        y = Measures.BORDERSIZE.value
        for i in range(19, 25):
            point = Point((50, 200), i, (x, y))
            points.append(point)
            x = x + Measures.TRIANGLEWIDTH.value

        point = BarPoint((Measures.BARSIZE.value, Measures.QUADRANTHEIGHT.value), 25,
                         (Measures.BORDERSIZE.value + Measures.QUADRANTWIDTH.value, Measures.BORDERSIZE.value))
        points.append(point)

        return points

    @staticmethod
    def create_checkers(points):
        board = [[0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
                 [0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0]]

        for i in range(24):
            if board[0][i] > 0:
                for c in range(board[0][i]):
                    checker = Checker(Colours.BLACK.value)
                    points[i+1].checkers.append(checker)

        for i in range(24):
            if board[1][i] > 0:
                for c in range(board[1][i]):
                    checker = Checker(Colours.WHITE.value)
                    points[24-i].checkers.append(checker)

    @staticmethod
    def draw_point_numbers(surface):
        font = pygame.font.Font(None, 18)

        x, y = Measures.BORDERSIZE.value + 20, 15
        for i in range(12, 18):
            number = font.render(str(i + 1), True, Colours.BLACK.value)
            surface.blit(number, (x, y))
            x = x + Measures.TRIANGLEWIDTH.value

        x, y = Measures.BORDERSIZE.value + Measures.QUADRANTWIDTH.value + Measures.BARSIZE.value + 20, 15
        for i in range(18, 24):
            number = font.render(str(i + 1), True, Colours.BLACK.value)
            surface.blit(number, (x, y))
            x = x + Measures.TRIANGLEWIDTH.value

        x, y = Measures.BOARDWIDTH.value - Measures.BORDERSIZE.value - 28, Measures.BOARDHEIGHT.value - 25
        for i in range(0, 6):
            number = font.render(str(i + 1), True, Colours.BLACK.value)
            surface.blit(number, (x, y))
            x = x - Measures.TRIANGLEWIDTH.value

        x = Measures.BOARDWIDTH.value - Measures.BORDERSIZE.value - Measures.QUADRANTWIDTH.value - \
            Measures.BARSIZE.value - 30
        y = Measures.BOARDHEIGHT.value - 25
        for i in range(6, 12):
            number = font.render(str(i + 1), True, Colours.BLACK.value)
            surface.blit(number, (x, y))
            x = x - Measures.TRIANGLEWIDTH.value
