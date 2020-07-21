"""Module for showing title screen and playing title music."""
import pygame
import pygame.mixer

from text_label import TYPEFACE_3D
from sliding_label import SlidingLabel, SLIDE_RIGHT, SLIDE_LEFT
from fading_label import FadingLabel
from blinking_label import BlinkingLabel

MUSIC_FILENAME = 'title.ogg'
BACKGROUND_FILENAME = 'bg_08.png'
FONT_SIZE_TITLE = 192
FONT_SIZE_START = 24
TOP_TITLE_TEXT = 'SPACE'
BOTTOM_TITLE_TEXT = 'RACER'
START_TEXT = "PRESS ENTER TO START"
TITLE_COLOR_PRIMARY = (158, 11, 14)
TITLE_COLOR_SECONDARY = (246, 150, 121)
START_COLOR_PRIMARY = (109, 207, 246)
START_COLOR_SECONDARY = (0, 0, 0)
SLIDING_SPEED = 16

class TitleScreen():
    def __init__(self, scr, view_point, stars):
        """Input parameters:
        scr - Surface for drawing;
        view_point - ViewPoint class instance;
        stars - Stars class instance for drawing."""
        self.scr = scr
        self.view_pt = view_point
        self.stars = stars
        self.background = pygame.image.load(
            f"img/bg/{BACKGROUND_FILENAME}").convert()
        scr_rect = self.scr.get_rect()

        self.top_sliding_label = SlidingLabel(
            scr=self.scr,
            text=TOP_TITLE_TEXT,
            color=TITLE_COLOR_PRIMARY,
            size=FONT_SIZE_TITLE,
            typeface=TYPEFACE_3D,
            slide=SLIDE_RIGHT)
        self.top_sliding_label.set_origin_center((
            -self.top_sliding_label.rect.width // 2,
            scr_rect.centery - FONT_SIZE_TITLE // 2))
        self.top_sliding_label.set_max_progress(
            (scr_rect.width + self.top_sliding_label.rect.width) // 2)
        self.top_sliding_label.set_speed(SLIDING_SPEED)
        self.top_sliding_label.set_repeat(False)

        self.bottom_sliding_label = SlidingLabel(
            scr=self.scr,
            text=BOTTOM_TITLE_TEXT,
            color=TITLE_COLOR_PRIMARY,
            size=FONT_SIZE_TITLE,
            typeface=TYPEFACE_3D,
            slide=SLIDE_LEFT)
        self.bottom_sliding_label.set_origin_center((
            scr_rect.width + self.bottom_sliding_label.rect.width // 2,
            scr_rect.centery + FONT_SIZE_TITLE // 2))
        self.bottom_sliding_label.set_max_progress(
            (scr_rect.width + self.bottom_sliding_label.rect.width) // 2)
        self.bottom_sliding_label.set_speed(SLIDING_SPEED)
        self.bottom_sliding_label.set_repeat(False)

        self.top_blinking_label = BlinkingLabel(
            scr=self.scr,
            text=TOP_TITLE_TEXT,
            color=TITLE_COLOR_PRIMARY,
            second_color=TITLE_COLOR_SECONDARY,
            size=FONT_SIZE_TITLE,
            typeface=TYPEFACE_3D)
        self.top_blinking_label.rect.center = (
            scr_rect.centerx,
            scr_rect.centery - FONT_SIZE_TITLE // 2)
        self.top_blinking_label.set_speed(0.5)

        self.bottom_blinking_label = BlinkingLabel(
            scr=self.scr,
            text=BOTTOM_TITLE_TEXT,
            color=TITLE_COLOR_PRIMARY,
            second_color=TITLE_COLOR_SECONDARY,
            size=FONT_SIZE_TITLE,
            typeface=TYPEFACE_3D)
        self.bottom_blinking_label.rect.center = (
            scr_rect.centerx,
            scr_rect.centery + FONT_SIZE_TITLE // 2)
        self.bottom_blinking_label.set_speed(0.5)

        self.start_fading_label = FadingLabel(
            scr=self.scr,
            text=START_TEXT,
            color=START_COLOR_PRIMARY,
            size=FONT_SIZE_START)
        self.start_fading_label.rect.midbottom = (
            scr_rect.centerx,
            scr_rect.bottom - FONT_SIZE_START * 2)
        self.start_fading_label.set_repeat(False)

        self.start_blinking_label = BlinkingLabel(
            scr=self.scr,
            text=START_TEXT,
            color=START_COLOR_PRIMARY,
            second_color=START_COLOR_SECONDARY,
            size=FONT_SIZE_START)
        self.start_blinking_label.rect.midbottom = (
            self.start_fading_label.rect.midbottom)

    def restart(self):
        """Prepares all animation effects for playing again."""
        self.top_sliding_label.restart()
        self.bottom_sliding_label.restart()
        self.top_blinking_label.restart()
        self.bottom_blinking_label.restart()
        self.start_fading_label.restart()
        self.start_blinking_label.restart()

        self.view_pt.set_center(0, self.scr.get_rect().centery)
        self.stars.respawn(visible_only=True)

    def _get_active_labels(self):
        labels = []

        if self.top_sliding_label.finished:
            if self.bottom_sliding_label.finished:
                labels.append(self.top_blinking_label)
                labels.append(self.bottom_blinking_label)
                if self.start_fading_label.finished:
                    labels.append(self.start_blinking_label)
                else:
                    labels.append(self.start_fading_label)
            else:
                labels.append(self.top_sliding_label)
                labels.append(self.bottom_sliding_label)
        else:
            labels.append(self.top_sliding_label)

        return labels

    def update(self):
        """Updates screen positions for text labels."""
        for label in self._get_active_labels():
            label.update()

    def draw(self):
        """Renders background image, stars and text labels to the
        specified surface."""
        self.scr.blit(self.background, (0, 0))
        self.stars.draw()
        for label in self._get_active_labels():
            label.draw()

    def play_music(self):
        """Starts playing music for title screen."""
        pygame.mixer.music.load(f"mus/{MUSIC_FILENAME}")
        pygame.mixer.music.play(loops=-1)
