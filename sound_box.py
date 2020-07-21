"""Module for playing sounds. It encapsulates SoundBox class and its
only instance - sound_box. Don't create SoundBox objects manually, use
sound_box object instead."""
from random import randint
from pygame.mixer import Sound

EXPLOSION_VOLUME = 0.8
EXPLOSION_FILES = (
    'explosion_01.wav',
    'explosion_02.wav',
    'explosion_03.wav',
    'explosion_04.wav',
    )

MULTI_EXPLOSION_VOLUME = 0.8
MULTI_EXPLOSION_FILES = (
    'multi_explosion_01.wav',
    'multi_explosion_02.wav',
    )

LASER_VOLUME = 0.4
LASER_FILES = (
    'laser_01.wav',
    'laser_02.wav',
    'laser_03.wav',
    'laser_04.wav',
    )

EXTRA_LIFE_VOLUME = 1.0
EXTRA_LIFE_FILE = 'extra_life.wav'

sound_box = None

class SoundBox():
    def __init__(self):
        self.explosion_sounds = []
        for filename in EXPLOSION_FILES:
            sound = Sound(f"snd/{filename}")
            sound.set_volume(EXPLOSION_VOLUME)
            self.explosion_sounds.append(sound)

        self.multi_explosion_sounds = []
        for filename in MULTI_EXPLOSION_FILES:
            sound = Sound(f"snd/{filename}")
            sound.set_volume(MULTI_EXPLOSION_VOLUME)
            self.multi_explosion_sounds.append(sound)

        self.laser_sounds = []
        for filename in LASER_FILES:
            sound = Sound(f"snd/{filename}")
            sound.set_volume(LASER_VOLUME)
            self.laser_sounds.append(sound)

        self.extra_life_sound = Sound(f"snd/{EXTRA_LIFE_FILE}")
        self.extra_life_sound.set_volume(EXTRA_LIFE_VOLUME)

    def play_extra_life(self):
        self.extra_life_sound.play()

    def play_explosion(self):
        index = randint(0, len(self.explosion_sounds) - 1)
        self.explosion_sounds[index].play()

    def play_multi_explosion(self):
        index = randint(0, len(self.multi_explosion_sounds) - 1)
        self.multi_explosion_sounds[index].play()

    def play_laser(self):
        index = randint(0, len(self.laser_sounds) - 1)
        self.laser_sounds[index].play()


def init():
    """Initializes SoundBox instance for further using."""
    global sound_box
    sound_box = SoundBox()

def get_sound_box():
    """Returns SoundBox singleton."""
    global sound_box
    if sound_box == None:
        init()
    return sound_box
