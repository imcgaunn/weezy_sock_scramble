import pygame
import logging

from constants import WHITE

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("world")


class World(object):
    """ Holds all the sprite groups """
    def __init__(self, screen):
        self._all = pygame.sprite.Group()
        self._blocks = pygame.sprite.Group()
        self._player = pygame.sprite.GroupSingle()
        self._screen = screen
        self._score = 0
        self._clock = pygame.time.Clock()

    def add_block(self, block):
        self._blocks.add(block)
        self._all.add(block)

    def set_player(self, player):
        self._player.add(player)
        self._all.add(player)

    def handle_key_pressed(self, kb_event):
        try:
            log.info(f'pressed: {kb_event}')
            self._player.sprite.handle_movement_keydown(kb_event.key)
        except AttributeError:
            log.info("you didn't pass a keyboard event!!")
        finally:
            return

    def handle_key_released(self, kb_event):
        try:
            log.info(f"released: {kb_event}")
            if kb_event.key in {pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN}:
                self._player.sprite.handle_movement_keyup(kb_event.key)
        except AttributeError:
            log.info("you didn't pass a keyboard event!!")
        finally:
            return

    def turn(self):
        self._screen.fill(WHITE)

        blocks_hit_list = pygame.sprite.spritecollide(self._player.sprite,
                                                      self._blocks, False)
        for block in blocks_hit_list:
            self._score += 1
            block.reset_pos()

        self._all.update()
        self._all.draw(self._screen)
        self._clock.tick(60)
        pygame.display.flip()