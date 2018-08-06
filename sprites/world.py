import pygame
import logging

from constants import WHITE

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("world")


class World(object):
    """ Holds all the sprite groups """
    def __init__(self, screen):
        self._all = pygame.sprite.Group()
        self._player = pygame.sprite.GroupSingle()
        self._platforms = pygame.sprite.Group()
        self._screen = screen
        self._score = 0
        self._clock = pygame.time.Clock()

    def set_player(self, player):
        self._player.add(player)
        self._all.add(player)

    def add_platform(self, platform):
        self._platforms.add(platform)
        self._all.add(platform)

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

    def check_collisions(self):
        player_platform_collisions = pygame.sprite.groupcollide(groupa=self._player,
                                                                groupb=self._platforms,
                                                                dokilla=False,
                                                                dokillb=False)
        if player_platform_collisions:
            log.debug(f"binky landed on a platform: {player_platform_collisions}")
            self._player.sprite.on_platform()
        else:
            log.debug(f"binky isn't on a platform: {player_platform_collisions}")
            self._player.sprite.off_platform()

    def turn(self):
        self._screen.fill(WHITE)
        self.check_collisions()
        self._all.update()
        self._all.draw(self._screen)
        self._clock.tick(60)
        pygame.display.flip()