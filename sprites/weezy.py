import logging

import os
import pygame

from constants import SCREEN_X, SCREEN_Y, FACING_RIGHT, FACING_LEFT


logging.basicConfig(level=logging.INFO)
log = logging.getLogger("player")

# TODO: procedurally generate world coming towards the character
# TODO: througout the course there can be socks that the character can
# collect and avoid obstacles etc.

class Weezy(pygame.sprite.Sprite):
    """ The player is a sprite that can walk """

    X_VELOCITY = 6
    X_ACCELERATION = 0.2
    Y_VELOCITY = 6
    SPRITE_PATH = os.path.join('sprites', os.path.join('images', 'weez.gif'))

    def __init__(self, width, height):
        super().__init__()
        self.player_height = height
        self.player_width = width
        self.facing = FACING_RIGHT
        self.jumping = False

        if pygame.image.get_extended():
            self.image = pygame.Surface.convert(pygame.image.load(Weezy.SPRITE_PATH))
            self.right_sprite = pygame.transform.scale(self.image, (width, height))
            self.left_sprite = pygame.transform.flip(self.right_sprite, True, False)
            self.image = self.right_sprite
            self.rect = self.image.get_rect()
        else:
            raise NameError("no GIF support :(")

        self.change_x = 0
        self.change_y = 0

        self.keys_down = {pygame.K_DOWN: False,
                          pygame.K_UP: False,
                          pygame.K_RIGHT: False,
                          pygame.K_LEFT: False}
        self._score = 0
        self._on_platform = False

    @property
    def on_ground(self):
        return ((self.rect.y >= SCREEN_Y - self.rect.height) or self._on_platform) and self.change_y >= 0

    @property
    def can_jump(self):
        # if we are on the ground or another platform, should be allowed to
        # jump.
        if self.on_ground:
            return True

    @property
    def score(self):
        return self._score

    def _apply_forces(self):
        if self.change_y and not self.on_ground == 0:
            self.change_y = 1  # start falling
        else:
            self.change_y += .6

        if self.on_ground:
            self.change_y = 0
            # self.rect.y = SCREEN_Y - self.rect.height

    def on_platform(self):
        self._on_platform = True

    def off_platform(self):
        self._on_platform = False

    def _reset_sprite_if_outside_bounds(self):
        if self.rect.y > SCREEN_Y:
            log.debug(f"hit max y: {SCREEN_Y}")
            self.rect.y = SCREEN_Y - self.player_height  # you can't get out!
        if self.rect.x > SCREEN_X:
            log.debug(f"hit max x: {SCREEN_X}")
            self.rect.x = SCREEN_X - self.player_width
        if self.rect.y < 0:
            log.debug("hit min y: 0")
            self.rect.y = 0
        if self.rect.x < 0:
            log.debug("hit min x: 0")
            self.rect.x = 0

    def _set_sprite_for_current_direction(self):
        if self.facing == FACING_LEFT:
            self.image = self.left_sprite
        else:
            self.image = self.right_sprite

    def update(self):
        self._apply_forces()
        self._set_sprite_for_current_direction()

        # apply "pending jump"
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        # don't let player leave the screen
        self._reset_sprite_if_outside_bounds()

    def handle_movement_keydown(self, key):
        """ called when movement control button is pressed """
        try:
            log.debug(f'pressed: {key}')
            if key == pygame.K_LEFT:
                self.walk_left()
            elif key == pygame.K_RIGHT:
                self.walk_right()
            elif key == pygame.K_DOWN:
                pass
            elif key == pygame.K_UP:
                pass
            elif key == pygame.K_SPACE:
                self.jump()
            self.keys_down[key] = True
        except AttributeError:
            log.info("you didn't pass a keyboard event!!")

    def handle_movement_keyup(self, key):
        """ called when movement control button is released """
        def _opposite_dir(key):
            return {pygame.K_LEFT: pygame.K_RIGHT,
                    pygame.K_RIGHT: pygame.K_LEFT,
                    pygame.K_UP: pygame.K_DOWN}[key]
        try:
            log.debug(f'released: {key}')
            self.keys_down[key] = False
            if key in {pygame.K_LEFT, pygame.K_RIGHT} and \
                    not(self.keys_down[_opposite_dir(key)]):
                self.stop_movement()
            log.debug(f'keys down: {self.keys_down}')
        except AttributeError:
            log.error("you didn't pass a keyboard event!!")

    def walk_left(self):
        self.change_x = -Weezy.X_VELOCITY
        self.facing = FACING_LEFT

    def walk_right(self):
        self.change_x = Weezy.X_VELOCITY
        self.facing = FACING_RIGHT

    def stop_movement(self):
        self.change_x = 0
        if self.jumping:
            self.jumping = False

    def jump(self):
        if self.can_jump:
            self.change_y = -10
            self.jumping = True
