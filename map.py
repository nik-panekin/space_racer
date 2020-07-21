"""Module for reading game level map."""
from math import ceil
from statistics import mean

# Each map tile is actually a square which side is GRID_SIZE pixels
GRID_SIZE = 128

TILE_BOTLEFT = 0
TILE_BOTLEFT_MIDRIGHT = 1
TILE_BOTLEFT_MIDTOP = 2
TILE_BOTLEFT_TOPRIGHT = 3
TILE_BOTRIGHT = 4
TILE_MIDBOT_MIDRIGHT = 5
TILE_MIDBOT_TOPRIGHT = 6
TILE_MIDLEFT_BOTRIGHT = 7
TILE_MIDLEFT_MIDBOT = 8
TILE_MIDLEFT_MIDRIGHT = 9
TILE_MIDLEFT_MIDTOP = 10
TILE_MIDLEFT_TOPRIGHT = 11
TILE_MIDTOP_BOTRIGHT = 12
TILE_MIDTOP_MIDBOT = 13
TILE_MIDTOP_MIDRIGHT = 14
TILE_TOPLEFT = 15
TILE_TOPLEFT_BOTRIGHT = 16
TILE_TOPLEFT_MIDBOT = 17
TILE_TOPLEFT_MIDRIGHT = 18
TILE_TOPRIGHT = 19

def tile_to_abs(coord):
    """Converts map tile coordinate to absolute coordinate."""
    return float(coord * GRID_SIZE)

def abs_to_tile(coord):
    """Converts absolute coordinate to map tile coordinate."""
    return int(coord) // GRID_SIZE

def _recognize_pattern(left=None, topleft=None, top=None, topright=None,
                       right=None, bottomright=None, bottom=None,
                       bottomleft=None):
    """Returns tile index for junction tile. This tile connects a pair
    of related tiles adjacent to it."""
    if left == '-' and bottom == '|':
        return TILE_MIDLEFT_MIDBOT
    elif right == '-' and bottom == '|':
        return TILE_MIDBOT_MIDRIGHT
    elif left == '-' and top == '|':
        return TILE_MIDLEFT_MIDTOP
    elif right == '-' and top == '|':
        return TILE_MIDTOP_MIDRIGHT
    elif bottomleft == '/' and right == '-':
        return TILE_BOTLEFT_MIDRIGHT
    elif bottomright == '\\' and left == '-':
        return TILE_MIDLEFT_BOTRIGHT
    elif bottomleft == '/' and top == '|':
        return TILE_BOTLEFT_MIDTOP
    elif bottomright == '\\' and top == '|':
        return TILE_MIDTOP_BOTRIGHT
    elif left == '-' and topright == '/':
        return TILE_MIDLEFT_TOPRIGHT
    elif right == '-' and topleft == '\\':
        return TILE_TOPLEFT_MIDRIGHT
    elif bottom == '|' and topright == '/':
        return TILE_MIDBOT_TOPRIGHT
    elif bottom == '|' and topleft == '\\':
        return TILE_TOPLEFT_MIDBOT
    else:
        return None

def map_read(filename):
    """Reads game level map from special-formatted text file and
    converts it to list of tiles and asteroid spawn points.
    The file must contain only allowed symbols and correct connections
    between tile symbols. See file 'map/junctions.map' for reference.
    Output format:
    {
        'map': [{x-coord: tile-index,...},...],
        'spawns': [[x-coord, y-coord],...]
    }
    Where:
    'map' is a list of tile indexes and coordinates (in tile system),
    y-coordinate for the tile is the list index itself;
    'spawns' is a list of asteroid spawn points with its absolute
    coordinates."""
    with open(filename) as f:
        lines = f.readlines()

    lines.reverse()

    tiles = []
    spawns = []
    for y in range(0, len(lines)):
        line = lines[y]
        map_line = {}
        for x in range(0, len(lines[y])):
            # Preparing tile indexes from characters
            if line[x] == '-':
                map_line[x] = TILE_MIDLEFT_MIDRIGHT
            elif line[x] == '|':
                map_line[x] = TILE_MIDTOP_MIDBOT
            elif line[x] == '/':
                map_line[x] = TILE_BOTLEFT_TOPRIGHT
            elif line[x] == '\\':
                map_line[x] = TILE_TOPLEFT_BOTRIGHT
            elif line[x] == '*':
                # Assigning surrounding box characters
                left, topleft, top, topright = None, None, None, None
                right, bottomright, bottom, bottomleft = None, None, None, None

                if x > 0:
                    left = line[x-1]
                    if y > 0:
                        if x <= len(lines[y-1]):
                            bottomleft = lines[y-1][x-1]
                    if y < len(lines) - 1:
                        if x <= len(lines[y+1]):
                            topleft = lines[y+1][x-1]
                if x < len(line) - 1:
                    right = line[x+1]
                    if y > 0:
                        if x < len(lines[y-1]) - 1:
                            bottomright = lines[y-1][x+1]
                    if y < len(lines) - 1:
                        if x < len(lines[y+1]) - 1:
                            topright = lines[y+1][x+1]
                if y > 0:
                    if x < len(lines[y-1]):
                        bottom = lines[y-1][x]
                if y < len(lines) - 1:
                    if x < len(lines[y+1]):
                        top = lines[y+1][x]

                map_line[x] = _recognize_pattern(
                    left=left, topleft=topleft, top=top, topright=topright,
                    right=right, bottomright=bottomright, bottom=bottom,
                    bottomleft=bottomleft)

            elif line[x] == '+':
                # Asteroid spawn point
                spawns.append([x, y])

        tiles.append(map_line)

    # Processing diagonals
    for y in range(0, len(tiles)):
        map_line = tiles[y].copy()
        for x, index in map_line.items():
            if index == TILE_BOTLEFT_TOPRIGHT:
                tiles[y][x-1] = TILE_BOTRIGHT
                tiles[y][x+1] = TILE_TOPLEFT
                if y > 0:
                    tiles[y-1][x] = TILE_TOPLEFT
                if y < len(tiles) - 1:
                    tiles[y+1][x] = TILE_BOTRIGHT
            elif index == TILE_TOPLEFT_BOTRIGHT:
                tiles[y][x-1] = TILE_TOPRIGHT
                tiles[y][x+1] = TILE_BOTLEFT
                if y > 0:
                    tiles[y-1][x] = TILE_TOPRIGHT
                if y < len(tiles) - 1:
                    tiles[y+1][x] = TILE_BOTLEFT

    # Correcting x-coordinates
    offset = ceil(mean(tiles[0].keys()))
    for y in range(0, len(tiles)):
        map_line = tiles[y].copy()
        tiles[y] = {}
        for x, index in map_line.items():
            tiles[y][x-offset] = index

    # The same thing for asteroid spawns
    for spawn_point in spawns:
        spawn_point[0] -= offset
        # And converting spawns coordinates to absolute
        spawn_point[0] = tile_to_abs(spawn_point[0]) + GRID_SIZE/2
        spawn_point[1] = tile_to_abs(spawn_point[1]) + GRID_SIZE/2

    return {'map': tiles, 'spawns': spawns}
