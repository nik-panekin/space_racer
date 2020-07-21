"""Module for rendering animated stars."""
from random import randint

import pygame

from animated_sprite import AnimatedSprite

class Star(AnimatedSprite):
    """The class represents animated star which has z-coordinate
    for 'depth' effect. While game 'camera' is moving, far stars
    changes their visual position more slowly than near ones. And thus
    'parallax' effect is created."""
    def __init__(self, image, scr, view_point, cols=1, rows=1):
        """The parameters are the same as for AnimatedSprite."""
        self.z = 1
        super().__init__(image, scr, view_point, cols, rows)
        self.frame = randint(0, self.get_max_frame())

    def _update_rect(self):
        """Translates 3-d coordinates to screen 2-d."""
        self.rect.x = int(self.view_pt.x_to_scr(self.x) / self.z)
        self.rect.y = int(self.view_pt.y_to_scr(self.y) / self.z)

    def set_center_scr(self, center_x, center_y):
        """Sets the center of animation in screen coordinates system."""
        left = center_x - (self.rect.width / 2)
        top = center_y - (self.rect.height / 2)
        self.x = self.view_pt.scr_to_x(left * self.z)
        self.y = self.view_pt.scr_to_y(top * self.z)

        self._update_rect()

    def get_center_scr(self):
        """Returns point (x, y) with the center of animation in
        screen coordinates system."""
        return self.rect.center

    def set_depth(self, z):
        """Sets z-coordinate of the star animation. Correct input value
        is positive float and may vary from 1 to +inf."""
        self.z = z
        self._update_rect()
