"""Module for working with race track: rendering and interaction."""
import pygame
from pygame import Rect

from image_crop import image_crop
from map import GRID_SIZE, tile_to_abs, abs_to_tile

TILE_FILES = (
    '00_tile_botleft.png',
    '01_tile_botleft_midright.png',
    '02_tile_botleft_midtop.png',
    '03_tile_botleft_topright.png',
    '04_tile_botright.png',
    '05_tile_midbot_midright.png',
    '06_tile_midbot_topright.png',
    '07_tile_midleft_botright.png',
    '08_tile_midleft_midbot.png',
    '09_tile_midleft_midright.png',
    '10_tile_midleft_midtop.png',
    '11_tile_midleft_topright.png',
    '12_tile_midtop_botright.png',
    '13_tile_midtop_midbot.png',
    '14_tile_midtop_midright.png',
    '15_tile_topleft.png',
    '16_tile_topleft_botright.png',
    '17_tile_topleft_midbot.png',
    '18_tile_topleft_midright.png',
    '19_tile_topright.png',
    )

class Track():
    """The class provides methods for drawing a race track and finding
    collisions with player space ship. It encapsulates all the images
    of track tiles and corresponding bitmasks. Tile images are cropped
    for some optimization (i.e. transparent areas are removed)."""
    def __init__(self, scr, view_point):
        """Input parameters:
        scr - Surface for drawing;
        view_point - ViewPoint class instance."""
        self.scr = scr
        self.view_pt = view_point
        self.scr_rect = self.scr.get_rect()
        self.images = []
        self.masks = []
        self.tile_rects = []
        for filename in TILE_FILES:
            crop_result = image_crop(
                pygame.image.load(f"img/tiles/{filename}"))
            self.images.append(crop_result['image'])
            self.masks.append(pygame.mask.from_surface(crop_result['image']))
            tile_rect = {
                'x': crop_result['offset_x'],
                'y': crop_result['offset_y'],
                'w': crop_result['image'].get_rect().width,
                'h': crop_result['image'].get_rect().height
                }
            self.tile_rects.append(tile_rect)

        # Format: [{x-coord: tile-index,...},...]
        self.tiles = [{}]
        self._visible_tiles = None

    def get_track_height(self):
        """Returns height in pixels of entire track map."""
        return len(self.tiles) * GRID_SIZE

    def get_track_width(self):
        """Returns width in pixels of entire track map."""
        x_list = []
        for line in self.tiles:
            for x in line.keys():
                if x not in x_list:
                    x_list.append(x)
        return (max(x_list) - min(x_list) + 1) * GRID_SIZE

    def _get_track_borders_tile(self, y):
        """The same as get_track_borders() except the coordinates are
        in tile grid system."""
        x_list = self.tiles[y].keys()
        x_min = min(x_list)
        x_max = max(x_list)
        x_left = x_min
        x_right = x_max

        while x_left < x_max:
            if (x_left + 1) not in x_list:
                break
            else:
                x_left += 1

        while x_right > x_min:
            if (x_right - 1) not in x_list:
                break
            else:
                x_right -= 1

        return (x_left, x_right)

    def get_track_borders(self, y):
        """Returns tuple (x_left, x_right) with coordinates corresponding
        left and right inner borders of the track being intersected by
        horizontal line with coordinate y.
        Assuming all coordinates are absolute."""
        y_tile = abs_to_tile(y)
        if y_tile < 0 or y_tile > len(self.tiles) - 1:
            return None

        x_left, x_right = self._get_track_borders_tile(y_tile)

        # Special issue: too narrow track with no gap between borders.
        # In this case get_track_borders() returns outer borders (not inner)
        if x_left > x_right:
            x_tmp = x_left
            x_left = x_right
            x_right = x_tmp

        return (tile_to_abs(x_left) + GRID_SIZE, tile_to_abs(x_right))

    def get_track_inner_tiles(self):
        """Returns a list of all tiles between left and right track
        borders in format: [(x_tile, y_tile),...]. The coordinates are
        in tile grid system."""
        inner_tiles = []
        for y in range(0, len(self.tiles)):
            x_left, x_right = self._get_track_borders_tile(y)
            if x_right - x_left > 1:
                for x in range(x_left+1, x_right):
                    inner_tiles.append((x, y))
        return inner_tiles

    def set_tile_map(self, tiles):
        """Assigns already loaded tile map."""
        self.tiles = tiles
        self.update()

    def _get_visible_tiles(self):
        """Returns a list: [{'index': tile_index, 'rect': tile_rect},...]."""

        first_line = abs_to_tile(self.view_pt.y - self.view_pt.half_height)
        last_line = abs_to_tile(self.view_pt.y + self.view_pt.half_height)

        max_line = len(self.tiles) - 1
        if first_line > max_line or last_line < 0:
            return None

        tiles = []

        if first_line < 0:
            first_line = 0
        if last_line > max_line:
            last_line = max_line

        for line in range(first_line, last_line + 1):
            for x, index in self.tiles[line].items():
                tiles.append({
                    'index': index,
                    'rect': self._get_tile_rect(x, line, index)
                    })

        return tiles

    def _get_tile_rect(self, x_tile, y_tile, index):
        tile_rect = self.tile_rects[index]

        x = self.view_pt.x_to_scr(tile_to_abs(x_tile))
        x += tile_rect['x']

        # We need + GRID_SIZE for top corner of the tile
        y = self.view_pt.y_to_scr(tile_to_abs(y_tile) + GRID_SIZE)
        y += tile_rect['y']

        return Rect(x, y, tile_rect['w'], tile_rect['h'])

    def update(self):
        """Updates list of tiles to render.
        Call each time right after ViewPoint object is updated."""
        self._visible_tiles = self._get_visible_tiles()

    def draw(self):
        if self._visible_tiles:
            for tile in self._visible_tiles:
                self.scr.blit(self.images[tile['index']], tile['rect'])

    def colliderect(self, rect):
        """Checks a collision between given rect (pygame.Rect) and
        track borders.
        Return True if a collision occured. Otherwise - False."""
        if self._visible_tiles:
            for tile in self._visible_tiles:
                if tile['rect'].colliderect(rect):
                    return True

        return False

    def collidemask(self, mask, rect):
        """Checks a collision between given mask (pygame.mask.Mask)
        positioned with rect (pygame.Rect) and track borders.
        Returns point of collision in absolute coordinates if collision
        occurred and None otherwise."""
        if self._visible_tiles:
            for tile in self._visible_tiles:
                if tile['rect'].colliderect(rect):
                    offset = (rect.x - tile['rect'].x, rect.y - tile['rect'].y)
                    point = self.masks[tile['index']].overlap(mask, offset)
                    if point:
                        return self.view_pt.scr_to_point(
                            point[0] + tile['rect'].x,
                            point[1] + tile['rect'].y)

        return None
