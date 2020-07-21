"""Module for drawing space full of stars."""
from random import randint, uniform, choice

import pygame

from star import Star

# Parameters of star animation images
FRAME_COLS = 6
FRAME_ROWS = 5
ANIMATION_SPEED = 0.25

STAR_FILES = (
    'stars_00.png',
    'stars_01.png',
    'stars_02.png',
    'stars_03.png',
    'stars_04.png',
    'stars_05.png',
    'stars_06.png',
    'stars_07.png',
    'stars_08.png',
    )

# Maximum stars generated
STAR_LIMIT = 60

class Stars():
    """The class encapsulates a list of star animations (Star class
    instances) and images for animations. It provides methods for
    spawning and adding new stars, deleting 'out-of-order' ones and
    drawing all the stars at once."""
    def __init__(self, scr, view_point):
        """Input parameters:
        scr - Surface for drawing;
        view_point - ViewPoint class instance."""
        self.scr = scr
        self.view_pt = view_point
        self.images = []
        for filename in STAR_FILES:
            image = pygame.image.load(f"img/{filename}")
            self.images.append(image)
        self.items = pygame.sprite.Group()
        self.respawn()

    def spawn_single(self, rect):
        """Creates single star inside bounding rect (pygame.Rect) in
        screen coordinates system at random position."""
        center_x = randint(rect.left, rect.right)
        center_y = randint(rect.top, rect.bottom)
        z = uniform(1, 5)
        self.add(center_x, center_y, z)

    def respawn(self, visible_only=False):
        """Initial spawn of the stars. If visible_only is set to True,
        then stars are created only on viewport."""
        if visible_only:
            rect = self.scr.get_rect()
        else:
            scr_height = self.scr.get_rect().height
            scr_width = self.scr.get_rect().width
            rect = pygame.Rect(int(-scr_width/2), int(-scr_height/2),
                               scr_width * 2, scr_height * 2)
        self.clear()
        for i in range(0, STAR_LIMIT):
            self.spawn_single(rect)

    def spawn(self):
        """Spawns new stars."""
        scr_height = self.scr.get_rect().height
        scr_width = self.scr.get_rect().width
        while len(self.items) < STAR_LIMIT:
            # Double propability for spawning stars in front of the ship
            area = choice(('left', 'right', 'front', 'top'))
            if area == 'left':
                rect = pygame.Rect(-scr_width, -scr_height,
                                   int(scr_width/2), scr_height * 2)
            elif area == 'right':
                rect = pygame.Rect(int(1.5 * scr_width), -scr_height,
                                   int(scr_width/2), scr_height * 2)
            else:
                rect = pygame.Rect(int(-scr_width/2), -scr_height,
                                   scr_width * 2, int(scr_height/2))
            self.spawn_single(rect)

    def clear(self):
        """Removes all the stars."""
        self.items.empty()

    def add(self, center_x, center_y, z):
        """Creates new star and adds it to the list. The animation
        of the star is selected randomly.
        Input parameters:
        center_x, center_y - the center of star animation in screen
        coordinates system;
        z - depth coordinate of the star (see Star.set_depth())."""
        star_ind = randint(0, len(self.images) - 1)
        star = Star(self.images[star_ind], self.scr, self.view_pt,
                    FRAME_COLS, FRAME_ROWS)
        star.set_depth(z)
        star.set_center_scr(center_x, center_y)
        star.set_speed(ANIMATION_SPEED)
        self.items.add(star)

    def update(self):
        """Updates star list (spawns new stars, deletes 'out-of-order'
        ones) and calls update() method for each active star."""
        self.spawn()

        scr_height = self.scr.get_rect().height
        scr_width = self.scr.get_rect().width
        for star in self.items.sprites()[:]:
            center_x, center_y = star.get_center_scr()
            if ((center_x < -scr_width) or (center_x > 2 * scr_width) or
                                           (center_y > scr_height * 1.5)):
                self.items.remove(star)

        self.items.update()

    def draw(self):
        """Draws all stars at one go."""
        for star in self.items.sprites():
            star.draw()
            star.next_frame()
