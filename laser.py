"""Module for drawing laser animated effect."""
import pygame

from sound_box import get_sound_box
from animated_sprite import AnimatedSprite

LASER_FRAME_COLS = 4
LASER_FRAME_ROWS = 3
LASER_FILE = 'laser.png'
CHARGE_MAX = 50

class Laser(AnimatedSprite):
    """The class represents laser animated effect. It encapsulates
    image with animation and corresponding bitmask for checking
    collisions (which means hitting the aim). Also it provides
    shooting and charging mechanism: laser shoots and then reloads."""
    def __init__(self, scr, view_point):
        """Input parameters:
        scr - Surface for drawing;
        view_point - ViewPoint class instance."""
        self.image = pygame.image.load(f'img/{LASER_FILE}')
        super().__init__(self.image, scr, view_point,
                         LASER_FRAME_COLS, LASER_FRAME_ROWS)
        self.repeat = False
        self.stopped = True
        mask_image = pygame.Surface(self.rect.size,
                                    pygame.SRCALPHA, self.image)
        mask_image.fill((0, 0, 0, 0))
        mask_image.blit(self.image, (0, 0), self._get_frame_rect())
        self.mask = pygame.mask.from_surface(mask_image)
        self.charge = CHARGE_MAX

    def set_origin(self, origin_x, origin_y):
        """Sets the absolute coordinates for the point where laser
        starts shooting (i.e. bottom-center of the animation)."""
        self.x = origin_x - (self.rect.width / 2)
        self.y = origin_y + self.rect.height
        self._update_rect()

    def update(self):
        """Updates screen position and charging status of the laser."""
        super().update()
        if self.stopped and self.charge < CHARGE_MAX:
            self.charge += 1

    def draw(self):
        """Renders laser animation and proceeds to next frame."""
        if not self.stopped:
            super().draw()
            self.next_frame()

    def shoot(self):
        """Starts laser shooting if possible. Returns True if shooting
        was successful and False if laser is still charging or already
        shooting."""
        if self.charge < CHARGE_MAX:
            return False
        if not self.stopped:
            return False
        get_sound_box().play_laser()
        self.charge = 0
        self.play()
        return True

    def shooting(self):
        """Returns True if the laser is shooting and False otherwise."""
        return not self.stopped
