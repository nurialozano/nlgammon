import pygame
import os
from pygame.locals import *
from GUI.Colours import Colours
from GUI.Measures import Measures


class GUIDice:
    def __init__(self):
        pass

    @staticmethod
    def generate_dice_surface():
        diceSurf = pygame.Surface((Measures.DICEWIDTH.value, Measures.DICEHEIGHT.value))
        diceSurf.fill(Colours.WHITE.value)
        diceRect = Rect(Measures.BORDERSIZE.value, Measures.BORDERSIZE.value, Measures.DICEWIDTH.value -
                        (Measures.BORDERSIZE.value * 2), Measures.DICEHEIGHT.value - (Measures.BORDERSIZE.value * 2))
        pygame.draw.rect(diceSurf, Colours.TEAL.value, diceRect)

        return diceSurf

    @staticmethod
    def draw_dice(die1, die2, surface, parent_surface):
        die1_name = "die" + str(die1) + ".gif"
        die2_name = "die" + str(die2) + ".gif"

        current_path = os.path.dirname(__file__)
        image_path = os.path.join(current_path, 'img')

        die1_img = pygame.image.load(os.path.join(image_path, die1_name))
        die1_img = pygame.transform.scale(die1_img, (50, 50))

        die2_img = pygame.image.load(os.path.join(image_path, die2_name))
        die2_img = pygame.transform.scale(die2_img, (50, 50))

        surface.blit(die1_img, (75, 180))
        surface.blit(die2_img, (75, 260))

        parent_surface.blit(surface, (Measures.BOARDWIDTH.value, 0))
