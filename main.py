"""
A side scrollin' sock grabbin' adventure
starrin bincly
"""

import pygame
import logging

from sprites.weezy import Weezy
from sprites.world import World
from sprites.basic_platform import BasicPlatform

from constants import SCREEN_X, SCREEN_Y

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("weezy_world")


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_X, SCREEN_Y])

    player = Weezy(64, 64)
    world = World(screen)
    world.set_player(player)
    world.add_platform(BasicPlatform())

    # -------- Main Program Loop -----------
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                world.handle_key_pressed(event)
            elif event.type == pygame.KEYUP:
                world.handle_key_released(event)

        # world.turn() handles
        # - collision detection,
        # - any changes to world as a result of collisions
        # - display update
        world.turn()

    pygame.quit()
