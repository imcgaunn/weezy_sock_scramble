"""
A side scrollin' sock grabbin' adventure
starrin bincly
"""

import pygame
import random
import logging

from sprites.block import Block
from sprites.weezy import Weezy
from sprites.world import World

from constants import BLACK, RED, SCREEN_X, SCREEN_Y

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("weezy_world")


def spawn_blocks(world, n=50):
    for _ in range(n):
        new_block = Block(BLACK, 20, 15)

        new_block.rect.x = random.randrange(SCREEN_X)
        new_block.rect.y = random.randrange(SCREEN_Y)

        world.add_block(new_block)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_X, SCREEN_Y])

    player = Weezy(RED, 10, 20)
    world = World(screen)
    world.set_player(player)

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
