"""Module for working with list of asteroid objects."""
from random import randint, choice

import pygame
from pygame.sprite import Group

from sound_box import get_sound_box
import explosions
import track
from animated_sprite import AnimatedSprite
from masked_sprite import MaskedSprite
from map import GRID_SIZE, tile_to_abs

# Parameters of asteroid animation images
FRAME_COLS = 4
FRAME_ROWS = 4
ANIMATION_SPEED = 0.1

# At first come full-sized asteroids and then small ones
# Small asteroid images have '_s' suffix in filename
ASTEROID_FILES = (
    'asteroid_1.png',
    'asteroid_2.png',
    'asteroid_3.png',
    'asteroid_4.png',
    'asteroid_5.png',
    'asteroid_6.png',
    'asteroid_7.png',
    'asteroid_1_s.png',
    'asteroid_2_s.png',
    'asteroid_3_s.png',
    'asteroid_4_s.png',
    'asteroid_5_s.png',
    'asteroid_6_s.png',
    'asteroid_7_s.png',
    )

# First index for small asteroid in the image list
ASTEROID_INDEX_SMALL = 7

ASTEROID_SIZE_ANY = 0
ASTEROID_SIZE_FULL = 1
ASTEROID_SIZE_SMALL = 2

class Asteroids():
    """The class encapsulates a list of asteroid animations
    (AnimatedSprite instances), images for animations and their bitmasks
    for checking collisions. It provides methods for spawning and adding
    new asteroids, deleting destroyed and 'out-of-order' ones, checking
    collisions and drawing all the asteroids at once."""
    def __init__(self, scr, view_point, explosions, track):
        """Input parameters:
        scr - Surface for drawing;
        view_point - ViewPoint class instance;
        explosions - Explosions class instance for asteroid blowing;
        track - Track class instance (needed for spawning)."""
        self.scr = scr
        self.view_pt = view_point
        self.explosions = explosions
        self.track = track
        self.spawn_density = 0
        # Format: [(center_x, center_y),...]
        self.spawns = []
        self.images = []
        self.masks = []
        for filename in ASTEROID_FILES:
            image = pygame.image.load(f"img/{filename}")
            self.images.append(image)

            # Creating bitmasks for each frame of each asteroid image
            asteroid = AnimatedSprite(image, self.scr, self.view_pt,
                                      FRAME_COLS, FRAME_ROWS)
            asteroid_masks = []
            for frame in range(0, asteroid.get_max_frame() + 1):
                mask_image = pygame.Surface(asteroid.rect.size,
                                            pygame.SRCALPHA, image)
                mask_image.fill((0, 0, 0, 0))
                mask_image.blit(image, (0, 0), asteroid._get_frame_rect(frame))
                asteroid_masks.append(pygame.mask.from_surface(mask_image))
            self.masks.append(asteroid_masks)

        self.items = pygame.sprite.Group()

    def set_spawn_density(self, spawn_density):
        """Sets asteroid random spawn density. Valid value is positive
        float or zero (no random spawns); value 1.0 means one asteroid
        per screen (i.e. average of distribution)."""
        self.spawn_density = spawn_density

    def _prepare_spawns(self):
        scr_height = int(self.scr.get_rect().height)
        map_height = int(self.track.get_track_height())
        spawn_count = int(
            (map_height - 2*scr_height) / scr_height * self.spawn_density)
        self.spawns = []
        tiles = self.track.get_track_inner_tiles()
        # Don't spawn on first and last screens
        for tile in tiles[:]:
            if ((tile_to_abs(tile[1]) < scr_height) or
                (tile_to_abs(tile[1]) > map_height - scr_height)):
                tiles.remove(tile)

        for i in range(0, spawn_count - 1):
            spawn_point = tiles.pop(randint(0, len(tiles) - 1))
            spawn_point = (tile_to_abs(spawn_point[0]) + GRID_SIZE/2,
                           tile_to_abs(spawn_point[1]) + GRID_SIZE/2)
            self.spawns.append(spawn_point)

    def respawn(self, spawns=None):
        """Respawns asteroids on the track. The number of randomly
        generated asteroids depends on self.spawn_density attribute;
        spawns parameter contains additional list of spawning points
        in format of absolute coordinates [(center_x, center_y),...]."""
        self.items.empty()
        self._prepare_spawns()
        if spawns:
            self.spawns += spawns

    def add(self, center_x, center_y, asteroid_size=ASTEROID_SIZE_ANY):
        """Creates new asteroid and adds it to the list. The animation
        of the asteroid is selected randomly.
        Input parameters:
        center_x, center_y - absolute coordinates for asteroid center;
        asteroid_size - determines whether small, large or random-sized
        asteroid will be created (see constants section)."""
        if asteroid_size == ASTEROID_SIZE_FULL:
            asteroid_ind = randint(0, ASTEROID_INDEX_SMALL - 1)
        elif asteroid_size == ASTEROID_SIZE_SMALL:
            asteroid_ind = randint(ASTEROID_INDEX_SMALL, len(self.images) - 1)
        else:
            asteroid_ind = randint(0, len(self.images) - 1)

        reverse = choice((True, False))

        asteroid = MaskedSprite(
            self.images[asteroid_ind], self.masks[asteroid_ind], self.scr,
            self.view_pt, FRAME_COLS, FRAME_ROWS, reverse)
        asteroid.set_center(center_x, center_y)
        asteroid.set_speed(ANIMATION_SPEED)
        self.items.add(asteroid)

    def update(self):
        """Updates asteroid list (spawns new asteroids, deletes
        'out-of-order' ones) and calls update() method for each active
        asteroid."""
        scr_height = self.scr.get_rect().height

        for spawn_point in self.spawns[:]:
            if spawn_point[1] < self.view_pt.y + scr_height:
                self.add(spawn_point[0], spawn_point[1])
                self.spawns.remove(spawn_point)
                break

        for asteroid in self.items.sprites()[:]:
            if asteroid.stopped or (asteroid.get_center()[1] <
                                    self.view_pt.y - scr_height):
                self.items.remove(asteroid)

        self.items.update()

    def draw(self):
        """Draws all asteroids at one go."""
        for asteroid in self.items.sprites():
            asteroid.draw()
            asteroid.next_frame()

    def collidemask(self, mask, rect, explode=False):
        """Checks a collision between given mask (pygame.mask.Mask)
        positioned with rect (pygame.Rect) and each asteroid in list.
        If explode parameter is True, then blow up the asteroid with
        collision detected.
        Returns point of the first detected collision in absolute
        coordinates if collision occurred and None otherwise."""
        for asteroid in self.items.sprites():
            point = asteroid.collidemask(mask, rect)
            if point:
                if explode:
                    self.explode(asteroid, point)
                return point

        return None

    def explode(self, asteroid, collide_point=None):
        """Explodes the asteroid.
        Input parameters:
        asteroid - AnimatedSprite object to be blown up;
        collide_point - the point of absolute coordinates (x, y) where
        collision with asteroid was detected; if specified then addition
        small explosion with collide_point coordinates will be created
        and one more explosion - with random coordinates."""
        get_sound_box().play_explosion()
        asteroid.stop()
        rect = asteroid.rect

        if collide_point:
            self.explosions.add(collide_point[0], collide_point[1],
                                explosions.SMALL_EXPLOSION_IND)

            x = self.view_pt.scr_to_x(randint(rect.left, rect.right))
            y = self.view_pt.scr_to_y(randint(rect.top, rect.bottom))
            self.explosions.add(x, y)

        x = self.view_pt.scr_to_x(rect.centerx)
        y = self.view_pt.scr_to_y(rect.centery)
        self.explosions.add(x, y, explosions.DOUBLE_EXPLOSION_IND)

    def explode_all(self):
        """Explodes all the asteroids in the list."""
        for asteroid in self.items.sprites():
            self.explode(asteroid)

    def explode_nearest(self, center_point):
        """Blows up nearest to the given point asteroids. Method is
        useful when player ship is restoring after crushing.
        Parameter center_point contains absolute coordinates
        of the epicentre of explosions in format (center_x, center_y)."""
        for asteroid in self.items.sprites():
            asteroid_center = asteroid.get_center()
            distance = ((center_point[0] - asteroid_center[0]) ** 2 +
                        (center_point[1] - asteroid_center[1]) ** 2) ** 0.5
            if distance < GRID_SIZE * 2:
                self.explode(asteroid)
