"""Module providing data and settings for game levels."""
import pygame
import pygame.mixer

from map import map_read

LEVELS = (
    {
    'mapfile': 'track_01.map',
    'background': 'bg_01.png',
    'music': 'level_01.ogg',
    'description': 'WALK IN THE PARK',
    'asteroids': 0,
    'speed': 6,
    'acceleration': 0,
    },
    {
    'mapfile': 'track_02.map',
    'background': 'bg_02.png',
    'music': 'level_02.ogg',
    'description': 'BRAKING TIME',
    'asteroids': 0,
    'speed': 4.9,
    'acceleration': 0,
    },
    {
    'mapfile': 'track_03.map',
    'background': 'bg_03.png',
    'music': 'level_03.ogg',
    'description': 'ASTEROID FIELD. FLY FAST AND DO NOT STOP!',
    'asteroids': 5,
    'speed': 6,
    'acceleration': 1.0E-5,
    },
    {
    'mapfile': 'track_04.map',
    'background': 'bg_04.png',
    'music': 'level_04.ogg',
    'description': 'BLAST YOUR WAY OUT!',
    'asteroids': 0,
    'speed': 8,
    'acceleration': 0,
    },
    {
    'mapfile': 'track_05.map',
    'background': 'bg_05.png',
    'music': 'level_05.ogg',
    'description': 'SERPENTINE',
    'asteroids': 0,
    'speed': 8,
    'acceleration': 0,
    },
    {
    'mapfile': 'track_06.map',
    'background': 'bg_06.png',
    'music': 'level_06.ogg',
    'description': "ACCELERATE! NO SLOW DOWN!",
    'asteroids': 0,
    'speed': 6,
    'acceleration': 1.0E-5,
    },
    )

class GameLevel():
    """The class loads data for game level and keeps level-wide settings
    and parameters."""
    def __init__(self):
        self.restart()

    def _reload(self):
        map_read_result = map_read(f"map/{LEVELS[self.level]['mapfile']}")
        self.map = map_read_result['map']
        self.spawns = map_read_result['spawns']
        self.background = pygame.image.load(
            f"img/bg/{LEVELS[self.level]['background']}").convert()

    def restart(self):
        """Resets level counter and reloads game resources for the
        first level."""
        self.level = 0
        self._reload()

    def play_music(self):
        """Starts playing background music for current level."""
        pygame.mixer.music.load(f"mus/{LEVELS[self.level]['music']}")
        pygame.mixer.music.play(loops=-1)

    def get_level(self):
        """Returns current level number."""
        # Internal level number begins from 0
        return self.level + 1

    def get_map(self):
        """Returns already loaded level map (for Track object,
        see map_read() definition) for current level."""
        return self.map

    def get_asteroid_spawns(self):
        """Returns asteroid spawn points (for Asteroids object,
        see map_read() definition) for current level."""
        return self.spawns

    def get_background(self):
        """Returns already loaded background (pygame.Surface)
        for current level."""
        return self.background

    def get_description(self):
        """Returns description for current level."""
        return LEVELS[self.level]['description']

    def get_asteroids_density(self):
        """Returns spawn density of asteroids for current level."""
        return LEVELS[self.level]['asteroids']

    def get_ship_speed(self):
        """Returns ship vertical constant speed for current level."""
        return LEVELS[self.level]['speed']

    def get_ship_acceleration(self):
        """Returns ship vertical acceleration for current level."""
        return LEVELS[self.level]['acceleration']

    def next_level(self):
        """Increments level counter and reloads game resources."""
        if self.level < len(LEVELS) - 1:
            self.level += 1
            self._reload()
            return True
        else:
            return False

    def get_level_count(self):
        """Returns total number of levels."""
        return len(LEVELS)

    def last_level(self):
        """Returns True if current level is the last level and
        False otherwise."""
        return self.level == len(LEVELS) - 1
