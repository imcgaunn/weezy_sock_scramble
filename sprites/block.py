import pygame
import random

from constants import SCREEN_X


class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()

    def reset_pos(self):
        self.rect.y = random.randrange(-300, -20)
        self.rect.x = random.randrange(0, SCREEN_X)

    def update(self):
        """ Called each frame. """

        # Move block down one pixel
        self.rect.y += 1

        # If block is too far down, reset to top of screen.
        if self.rect.y > 410:
            self.reset_pos()
