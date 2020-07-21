"""Module for drawing and keeping explosion animations."""
from random import randint

import pygame
from pygame.sprite import Group

from animated_sprite import AnimatedSprite

# Parameters of explosion animation images
FRAME_COLS = 8
FRAME_ROWS = 8

# The first file (index 0) is the smallest explosion
EXPLOSION_FILES = (
    'explosion_1.png',
    'explosion_2.png',
    'explosion_3.png',
    'explosion_4.png',
    )

SMALL_EXPLOSION_IND = 0
BLAST_EXPLOSION_IND = 1
BIG_EXPLOSION_IND = 2
DOUBLE_EXPLOSION_IND = 3

class Explosions():
    def __init__(self, scr, view_point):
        """Input parameters:
        scr - Surface for drawing;
        view_point - ViewPoint class instance."""
        self.scr = scr
        self.view_pt = view_point
        self.images = []
        for filename in EXPLOSION_FILES:
            self.images.append(pygame.image.load(f"img/{filename}"))
        self.items = pygame.sprite.Group()

    def add(self, center_x, center_y, explosion_ind=None):
        """Adds new explosion animation.
        Input parameters:
        center_x, center_y - absolute center coordinates of animation;
        explosion_ind - index of an animation in the list; if None then
        the animation is selected randomly (except small explosion)."""
        if explosion_ind == None:
            explosion_ind = randint(BLAST_EXPLOSION_IND, DOUBLE_EXPLOSION_IND)
        explosion = AnimatedSprite(self.images[explosion_ind], self.scr,
                                   self.view_pt, FRAME_COLS, FRAME_ROWS)
        explosion.set_center(center_x, center_y)
        explosion.repeat = False
        self.items.add(explosion)

    def update(self):
        """Updates screen positions of the animations and removes the
        finished ones."""
        for explosion in self.items.sprites()[:]:
            if explosion.stopped:
                self.items.remove(explosion)
        self.items.update()

    def draw(self):
        for explosion in self.items.sprites():
            explosion.draw()
            explosion.next_frame()
