import pygame
from pygame.locals import *
from GUI.Colours import Colours
from GUI.Measures import Measures
from Colour import Colour


class GUIBottom:
    def __init__(self):
        pass

    @staticmethod
    def generate_bottom_surface():
        bottomSurf = pygame.Surface((Measures.BOTTOMWIDTH.value, Measures.BOTTOMHEIGHT.value))
        bottomSurf.fill(Colours.WHITE.value)

        # left, top, width, height
        bearoffRect = Rect(Measures.BORDERSIZE.value, Measures.BORDERSIZE.value,
                           (Measures.QUADRANTWIDTH.value * 2) + 10,
                           Measures.BOTTOMHEIGHT.value - (Measures.BORDERSIZE.value * 2))

        pygame.draw.rect(bottomSurf, Colours.TEAL.value, bearoffRect)
        return bottomSurf

    @staticmethod
    def draw_title(surface):
        font = pygame.font.Font(None, 18)
        black_title = font.render("BORNE-OFF CHECKERS", True, Colours.BLACK.value)
        surface.blit(black_title, (Measures.BORDERSIZE.value, Measures.BOTTOMHEIGHT.value - Measures.BORDERSIZE.value + 5))

    def display_text(self, surface, player, text, parent_surface):

        self.empty_text_box(surface, None)

        font = pygame.font.Font(None, 25)

        if text == 'START':
            display_text = Colour(player.colour).name + " starts"
            second_line = None

        elif text == 'MOVE':
            display_text = Colour(player.colour).name + " has no"
            second_line = "moves available"

        if text == 'OVER':
            for clr in Colour:
                if clr.value != player.colour:
                    colour = clr.name
            display_text = colour + " wins"
            second_line = "GAME OVER"

        display_text = font.render(display_text, True, Colours.BLACK.value)
        surface.blit(display_text, (Measures.BOARDWIDTH.value + Measures.BORDERSIZE.value, 0))

        if second_line is not None:
            second_line = font.render(second_line, True, Colours.BLACK.value)
            surface.blit(second_line, (Measures.BOARDWIDTH.value + Measures.BORDERSIZE.value, 20))

        parent_surface.blit(surface, (0, Measures.BOARDHEIGHT.value))

    @staticmethod
    def display_move_string(surface, text, step, parent_surface):
        font = pygame.font.Font(None, 18)
        display_text = font.render(text, True, Colours.BLACK.value)

        height = 30
        for i in range(step):
            height = height + 20

        surface.blit(display_text, (Measures.BOARDWIDTH.value + 5, height))
        parent_surface.blit(surface, (0, Measures.BOARDHEIGHT.value))

    @staticmethod
    def empty_text_box(surface, parent_surface):
        # left, top, width, height
        text_box = Rect(Measures.BOARDWIDTH.value, 0, Measures.DICEWIDTH.value, Measures.BOTTOMHEIGHT.value)
        surface.fill(Colours.WHITE.value, text_box)

        if parent_surface is not None:
            parent_surface.blit(surface, (0, Measures.BOARDHEIGHT.value))
