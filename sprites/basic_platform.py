import logging

import pygame
from constants import SCREEN_X, SCREEN_Y, RED


logging.basicConfig(level=logging.INFO)
log = logging.getLogger("basic_platform")


class BasicPlatform(pygame.sprite.Sprite):
    """ This is a test platform. mostly here to experiment."""

    SPRITE_PATH = "" # TODO:

    def __init__(self, width=100, height=20):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.image.fill(RED)

        # toss that sucker right in the middle of the screen
        self.rect.x = SCREEN_X / 2
        self.rect.y = SCREEN_Y / 2 + 150
    pass

    def update(self):
        pass