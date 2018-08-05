import logging
import pygame

from constants import SCREEN_X, SCREEN_Y

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("platform")


class Platform(pygame.sprite.Sprite):
    def __init__(self, color, width, height=10, initial_x=0, initial_y=0):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()

        self.rect.x = initial_x
        self.rect.y = initial_y
