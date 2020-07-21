"""This module contains Ship class which represents space ship."""
from random import randint
import pygame

from sound_box import get_sound_box
import explosions
from view_point import ViewPoint
from laser import Laser
from animated_sprite import AnimatedSprite

SHIP_FILE = 'ship.png'
SHIP_MOVEMENT = 4

LASER_OFFSET_X = 4
LASER_OFFSET_Y = 64

JET_FILE = 'jet.png'
JET_FRAME_COLS = 8
JET_FRAME_ROWS = 4
JET_OFFSET_X = 48
JET_OFFSET_Y = 2

STATUS_NORMAL = 0
STATUS_INACTIVE = 1
STATUS_EXPLODING = 2
STATUS_RESTORING = 3
STATUS_AUTO = 4

PROGRESS_MAX = 90
EXPLOSIONS_MAX = 3
BLINKING_GAP = 5

class Ship():
    """The ship class encapsulates absolute coordinates (x, y) of the
    upper-left corner, image, bitmask for collision detection, vertical
    speed, moving and shooting status, ship status itself, laser and
    jets objects."""
    def __init__(self, scr, view_point, explosions):
        """Input parameters:
        scr - Surface for drawing;
        view_point - ViewPoint class instance;
        explosions - Explosions class instance for ship destroying."""
        self.scr = scr
        self.view_pt = view_point
        self.explosions = explosions
        self.image = pygame.image.load(f'img/{SHIP_FILE}')
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.x = - (self.rect.width / 2)
        self.y = self.rect.height
        self._update_rect()
        self.laser = Laser(self.scr, self.view_pt)
        self._update_laser_pos()
        self.jet_image = pygame.image.load(f'img/{JET_FILE}')
        self.jets = {
            'left': AnimatedSprite(
                self.jet_image, self.scr, self.view_pt, JET_FRAME_COLS,
                JET_FRAME_ROWS, reverse=True),
            'right': AnimatedSprite(
                self.jet_image, self.scr, self.view_pt, JET_FRAME_COLS,
                JET_FRAME_ROWS, reverse=True),
            }
        self._update_jets_pos()
        self.speed = 0
        self._reset_user_control()
        self.status = STATUS_NORMAL
        self._reset_progress()

    def _reset_user_control(self):
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False
        self.shooting = False

    def _reset_progress(self):
        # Ship destructive explosion is continuous process which status
        # keeps self.progress attribute
        self.progress = 0
        # Keeps key points of the progress where explosions must be created
        self.key_frames = []

    def _update_laser_pos(self):
        self.laser.set_origin(self.x + (self.rect.width / 2) + LASER_OFFSET_X,
                              self.y - LASER_OFFSET_Y)

    def _update_rect(self):
        self.rect.x = self.view_pt.x_to_scr(self.x)
        self.rect.y = self.view_pt.y_to_scr(self.y)

    def get_center(self):
        """Returns point (x, y) with absolute ship center coordinates."""
        return (self.x + self.rect.width / 2, self.y - self.rect.height / 2)

    def update(self):
        """Call before any collision detection, drawing ship, etc."""
        full_speed = self.speed + self.acceleration * (self.y ** 1.2)

        if self.status in (STATUS_NORMAL, STATUS_RESTORING, STATUS_AUTO):
            self.y += full_speed

        if self.status == STATUS_NORMAL and self.shooting:
            self.laser.shoot()

        if self.status == STATUS_NORMAL or self.status == STATUS_RESTORING:
            if self.moving_left:
                self.x -= SHIP_MOVEMENT
            if self.moving_right:
                self.x += SHIP_MOVEMENT
            if self.acceleration == 0:
                # Don't move vertically if acceleration > 0
                if self.moving_up:
                    self.y += SHIP_MOVEMENT
                if self.moving_down:
                    self.y -= SHIP_MOVEMENT

        if self.status == STATUS_EXPLODING:
            self.progress += 1
            if self.progress in self.key_frames:
                self._add_explosion()
            if self.progress >= PROGRESS_MAX:
                self._add_explosion(
                    self.rect.center,
                    explosion_ind=explosions.DOUBLE_EXPLOSION_IND)
                self._reset_progress()
                self.status = STATUS_INACTIVE

        if self.status == STATUS_RESTORING:
            self.progress += 1
            if self.progress >= PROGRESS_MAX:
                self._reset_progress()
                self.status = STATUS_NORMAL

        self.view_pt.set_speed(full_speed)
        self.view_pt.set_trace_point(self.get_center())
        self._update_rect()
        self._update_laser_pos()
        self.laser.update()
        self._update_jets_pos()

    def set_speed(self, speed):
        self.speed = speed

    def set_acceleration(self, acceleration):
        self.acceleration = acceleration

    def _update_jets_pos(self):
        bottom = self.y - self.rect.height
        centerx = self.x + (self.rect.width - self.jets['left'].rect.width) / 2

        self.jets['left'].x = centerx - JET_OFFSET_X
        self.jets['right'].x = centerx + JET_OFFSET_X
        self.jets['left'].y = bottom - JET_OFFSET_Y
        self.jets['right'].y = bottom - JET_OFFSET_Y

        self.jets['left'].update()
        self.jets['right'].update()

    def is_visible(self):
        """This method helps with implementing 'blinking' effect."""
        if self.status == STATUS_INACTIVE:
            return False
        elif self.status == STATUS_EXPLODING:
            return (self.progress % int(self.progress / 10 + 1)) == 0
        elif self.status == STATUS_RESTORING:
            return ((self.progress // BLINKING_GAP) % 2) == 0
        else:
            #At this point self.status in [STATUS_NORMAL, STATUS_AUTO]
            return True

    def draw(self):
        if self.is_visible():
            self.laser.draw()
            for jet in self.jets.values():
                jet.draw()
                jet.next_frame()
            self.scr.blit(self.image, self.rect)

    def _add_explosion(self, point=None, explosion_ind=None):
        """If specified - point parameter contains screen coordinates
        of explosion."""
        if point:
            x = self.view_pt.scr_to_x(point[0])
            y = self.view_pt.scr_to_y(point[1])
        else:
            x = self.view_pt.scr_to_x(randint(self.rect.left, self.rect.right))
            y = self.view_pt.scr_to_y(randint(self.rect.top, self.rect.bottom))

        if explosion_ind:
            self.explosions.add(x, y, explosion_ind)
        else:
            self.explosions.add(x, y)

    def explode(self, collide_point=None):
        """Starts ship explosion process. If specified collide_point
        has absolute coordinates of destructive collision."""
        if self.status != STATUS_NORMAL:
            return False

        get_sound_box().play_multi_explosion()
        self.status = STATUS_EXPLODING
        self._reset_progress()
        self._add_explosion()
        if collide_point:
            self.explosions.add(collide_point[0], collide_point[1],
                                explosions.SMALL_EXPLOSION_IND)

        for i in range(EXPLOSIONS_MAX - 1):
            self.key_frames.append(randint(1, PROGRESS_MAX - 1))

        return True

    def set_autopilot(self):
        """Imperatively disables player control of the ship.
        The only way to return the control is to call restore()."""
        self.status = STATUS_AUTO

    def set_center(self, center_x, center_y):
        """Sets the absolute center coordinates of the ship."""
        self.x = center_x - (self.rect.width / 2)
        self.y = center_y + (self.rect.height / 2)
        self._update_rect()

    def restore(self, center_point=None, reset_control=False):
        """Restores ship after destruction or just assigning special
        'restoring' status (blinking and temporary invincibility).
        Input parameters:
        center_point - new absolute coordinates of the ship
        (no changing position if None);
        reset_control - if True then stops moving left/right/up/down
        and shooting; useful to avoid glitch when game level starts."""
        if self.status not in [STATUS_NORMAL, STATUS_INACTIVE, STATUS_AUTO]:
            return False

        self.status = STATUS_RESTORING
        self._reset_progress()
        if reset_control:
            self._reset_user_control()
        if center_point:
            self.set_center(center_point[0], center_point[1])

        return True
